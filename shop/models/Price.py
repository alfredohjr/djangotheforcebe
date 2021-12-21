from datetime import time
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.dispatch import receiver

from shop.models.Stock import Stock
from shop.models.ProductLog import ProductLog
from shop.models.ProductKit import ProductKit

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
        log = ProductLog()
        log.register(id=self.product.id, table='price', transaction='del', message=f'delete, price_id={self.id}')

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()
    
    def forKit(self):
        productKit = ProductKit.objects.filter(productChild=self.product).values('productMain').distinct()
        for product in productKit:
            productKitN2 = ProductKit.objects.filter(productMain=product['productMain'])
            value = 0
            for productN2 in productKitN2:
                stock = Stock.objects.get(deposit=self.deposit, product=productN2.productChild)
                value += (productN2.amount * stock.value)*((stock.product.margin/100)+1)
            price = Price()
            price.deposit = self.deposit
            price.product_id = product['productMain']
            price.value = value
            price.priceType = 'NO'
            price.startedAt = timezone.now()
            price.save()


@receiver(pre_save, sender=Price)
def pre_save_price(sender, instance, *args, **kwargs):

    price = Price.objects.filter(id=instance.id)
    if price:
        if price[0].deletedAt and instance.deletedAt:
            raise ValidationError('don\'t update deleted price.')
        
        if price[0].isValid and instance.isValid:
            raise ValidationError('don\'t alter active price')
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
    
    if not instance.startedAt:
        raise ValidationError('don\'t create price without startedAt')
    
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

    # for logs...
    if price:
        messages = []
        if price[0].deposit != instance.deposit:
            messages.append(f'deposit_from={price[0].deposit}, deposit_to={instance.deposit}')

        if price[0].product != instance.product:
            messages.append(f'product_from={price[0].product}, product_to={instance.product}')

        if price[0].value != instance.value:
            messages.append(f'value_from={price[0].value}, value_to={instance.value}')

        if price[0].priceType != instance.priceType:
            messages.append(f'priceType_from={price[0].priceType}, priceType_to={instance.priceType}')

        if price[0].startedAt != instance.startedAt:
            messages.append(f'startedAt_from={price[0].startedAt}, startedAt_to={instance.startedAt}')

        if price[0].finishedAt != instance.finishedAt:
            messages.append(f'finishedAt_from={price[0].finishedAt}, finishedAt_to={instance.finishedAt}')

        if price[0].isValid != instance.isValid:
            messages.append(f'isValid_from={price[0].isValid}, isValid_to={instance.isValid}')


        if messages:
            messages.append(f'price_id={instance.id}')
            log = ProductLog()
            log.register(id=instance.product.id, table='price', transaction='upd', message='|'.join(messages))


@receiver(post_save, sender=Price)
def post_save_price(sender, instance, created, *args, **kwargs):
    if created:
        log = ProductLog()
        log.register(id=instance.product.id, table='price', transaction='cre', message=f'created, price_id={instance.id}')