from django.db import models
from django.utils import timezone

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