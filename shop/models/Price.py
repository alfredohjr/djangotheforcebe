from datetime import time
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver

from shop.models.Stock import Stock

datetime_format = '%d/%m/%Y %H:%M'

class Price(models.Model):

    PRICE_TYPES = (
        ('OF','Oferta'),
        ('NO','Normal')
    )

    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    priceType = models.CharField(max_length=3,choices=PRICE_TYPES,default='NO')
    startedAt = models.DateTimeField(null=True, blank=True)
    finishedAt = models.DateTimeField(null=True, blank=True)
    isValid = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def stockBefore(self):
        pass

    def stockNow(self):
        return Stock.objects.get(deposit=self.deposit, product=self.product).amount

    def __str__(self):
        return self.product.name
    
    def delete(self):
        self.deletedAt = timezone.now()
        self.save()
        return True


@receiver(pre_save, sender=Price)
def pre_save_price(sender, instance, *args, **kwargs):

    price = Price.objects.filter(id=instance.id)
    if price:
        if price[0].deletedAt and instance.deletedAt:
            raise ValidationError('don\'t update deleted price.')
    else:
        if instance.deletedAt:
            raise ValidationError('don\'t create deleted price.')

    if instance.deposit.company.deletedAt:
        raise ValidationError('company is closed, verify.')
    
    if instance.deposit.deletedAt:
        raise ValidationError('deposit is closed, verify.')
    
    if instance.value <= 0:
        raise ValidationError('don\'t use negative values.')

    if instance.priceType == 'NO' and instance.finishedAt:
        raise ValidationError('don\'t create normal price and finishedAt')
    
    if instance.priceType == 'OF' and instance.startedAt is None:
        raise ValidationError('don\'t create oferta price without startedAt')

    if instance.priceType == 'OF' and instance.finishedAt is None:
        raise ValidationError('don\'t create oferta price without finishedAt')
    
    trunc = timezone.now()
    trunc = timezone.datetime(trunc.year,trunc.month,trunc.day)
    trunc = timezone.make_aware(trunc, timezone.get_current_timezone())

    if instance.startedAt < trunc:
        raise ValidationError('only create price started today.')
    
    if instance.finishedAt is not None and instance.priceType == 'OF':
        if instance.finishedAt <= trunc: 
            raise ValidationError('only create price started today.')

    if instance.product.deletedAt:
        raise ValidationError('product is deleted, verify.')