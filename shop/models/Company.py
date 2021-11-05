from django.db import models
from django.utils import timezone
import decimal
from django.db.models.signals import pre_save
from django.dispatch import receiver

from shop.models.Deposit import Deposit
from shop.models.Document import Document
from shop.models.Stock import Stock

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
                return False
        
        document = Document.objects.filter(deposit__in=deposits,isOpen=True)
        if document:
            return False

        self.deletedAt = timezone.now()
        self.save()
        return True


@receiver(pre_save,sender=Company)
def pre_save_company(sender, instance, *args, **kwargs):

    company = Company.objects.filter(id=instance.id)
    if company:
        if instance.deletedAt is None and company[0].deletedAt:
            return True

        if company[0].deletedAt:
            raise Exception('company is deleted, to alter this, reopen.')