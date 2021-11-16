from django.db import models
from django.utils import timezone
import decimal
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from shop.models.Deposit import Deposit
from shop.models.Document import Document
from shop.models.Stock import Stock
from shop.models.CompanyLog import CompanyLog

class Company(models.Model):

    name = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name'),)

    def delete(self):
        deposits = Deposit.objects.filter(company_id=self.id)
        stocks = Stock.objects.filter(deposit__in=deposits)
        for stock in stocks:
            if stock.amount != decimal.Decimal(0):
                raise ValidationError(('don\'t delete company if product stock is not 0.'))
        
        document = Document.objects.filter(deposit__in=deposits,isOpen=True)
        if document:
            return False

        self.deletedAt = timezone.now()
        self.save()
    
    def close(self):
        self.delete()
    
    def open(self):
        self.deletedAt = None
        self.save()


@receiver(pre_save,sender=Company)
def pre_save_company(sender, instance, *args, **kwargs):

    log = CompanyLog()

    if len(instance.name.strip()) < 10:
        raise ValidationError(('minumum size is 10'))

    if instance.deletedAt:
        deposits = Deposit.objects.filter(company_id=instance.id)
        if deposits:
            stocks = Stock.objects.filter(deposit__in=deposits)
            if stocks:
                for stock in stocks:
                    if stock.amount != 0:
                        raise ValidationError('don\'t delete company if product stock is not 0.')


    company = Company.objects.filter(id=instance.id)
    if company:
        if instance.deletedAt is None and company[0].deletedAt:
            log.register(id=instance.id, table='company', transaction='update', message='return company')
            return True

        if company[0].deletedAt:
            raise ValidationError('company is deleted, to alter this, reopen.')
        
        # for log
        message = []
        if company[0].name != instance.name:
            message.append(f'name_from={company[0].name},name_to={instance.name} ')

        if message:
            log.register(id=instance.id,table='company',transaction='upd',message='|'.join(message))


@receiver(post_save,sender=Company)
def post_save_company(sender, instance, created, *args, **kwargs):
    if created:
        if instance.deletedAt != None:
            log = CompanyLog()
            log.register(id=instance.id,table='company',transaction='cre',message='created')
            company = Company.objects.get(id=instance.id)
            company.deletedAt = None
            company.save()