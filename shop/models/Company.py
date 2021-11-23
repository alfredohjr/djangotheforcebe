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
    email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(upload_to='company', null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    complement = models.CharField(max_length=200, null=True, blank=True)
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

        if company[0].email != instance.email:
            message.append(f'email_from={company[0].email},email_to={instance.email} ')

        if company[0].logo != instance.logo:
            message.append(f'logo_from={company[0].logo},logo_to={instance.logo} ')

        if company[0].cep != instance.cep:
            message.append(f'cep_from={company[0].cep},cep_to={instance.cep} ')

        if company[0].state != instance.state:
            message.append(f'state_from={company[0].state},state_to={instance.state} ')

        if company[0].city != instance.city:
            message.append(f'city_from={company[0].city},city_to={instance.city} ')

        if company[0].address != instance.address:
            message.append(f'address_from={company[0].address},address_to={instance.address} ')

        if company[0].complement != instance.complement:
            message.append(f'complement_from={company[0].complement},complement_to={instance.complement} ')

        if message:
            log.register(id=instance.id,table='company',transaction='upd',message='|'.join(message))

        if instance.deletedAt and company[0].deletedAt is None:
            log = CompanyLog()
            log.register(id=instance.id, table='company', transaction='del',message='delete')


@receiver(post_save,sender=Company)
def post_save_company(sender, instance, created, *args, **kwargs):
    if created:
        log = CompanyLog()
        log.register(id=instance.id,table='company',transaction='cre',message='created')
        if instance.deletedAt != None:
            company = Company.objects.get(id=instance.id)
            company.deletedAt = None
            company.save()