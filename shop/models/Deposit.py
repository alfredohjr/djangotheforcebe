from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shop.models.Stock import Stock

class Deposit(models.Model):

    name = models.CharField(max_length=30)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def total(self):
        total = 0
        stock = Stock.objects.filter(deposit_id = self.id)
        for s in stock:
            total += s.value * s.amount
        return total

    def totalAmount(self):
        total = 0
        stock = Stock.objects.filter(deposit_id = self.id)
        for s in stock:
            total += s.amount
        return total

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name'),)

    def delete(self):
        stocks = Stock.objects.filter(deposit__id=self.id)
        for stock in stocks:
            if stock.amount != 0:
                return False

        self.deletedAt = timezone.now()
        self.save()
        return True

@receiver(pre_save,sender=Deposit)
def pre_save_deposit(sender, instance, *args, **kwargs):
    
    if len(instance.name) < 10:
        raise ValidationError('minimum size is 10.')
    
    if instance.company.deletedAt != None:
        raise ValidationError('company is inactive, please check.')

    deposit = Deposit.objects.filter(id=instance.id)
    if deposit:
        if instance.deletedAt is None and deposit[0].deletedAt:
            return True

        if deposit[0].deletedAt:
            raise ValidationError('deposit is deleted, to alter this, reopen.')


@receiver(post_save,sender=Deposit)
def post_save_company(sender, instance, created, *args, **kwargs):
    if created:
        if instance.deletedAt != None:
            company = Deposit.objects.get(id=instance.id)
            company.deletedAt = None
            company.save()
            return True