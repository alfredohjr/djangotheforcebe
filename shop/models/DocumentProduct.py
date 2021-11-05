from django.db import models
from django.db.models.expressions import F
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shop.models.Price import Price
from shop.models.Product import Product
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement

import decimal

class DocumentProduct(models.Model):

    document = models.ForeignKey('Document',on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10,decimal_places=3)
    value = models.DecimalField(max_digits=10,decimal_places=3)
    isOpen = models.BooleanField(default=True)
    isNew = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)



@receiver(pre_save,sender=DocumentProduct)
def pre_save_DocumentProduct(sender, instance, **kwargs):

    documentProduct = DocumentProduct.objects.filter(id=instance.id)
    if not documentProduct:
        return 0

    if documentProduct[0].isOpen != instance.isOpen:

        queryset_stock = Stock.objects.filter(deposit=instance.document.deposit,product=instance.product)

        #create stock case not exists
        if not queryset_stock:
            stock = Stock(deposit=instance.document.deposit,product=instance.product,amount=0,value=0)
            stock.save()

        stock = Stock.objects.get(deposit=instance.document.deposit,product=instance.product)
        stockMovement = StockMovement(deposit = instance.document.deposit
                                    , product = instance.product
                                    , value = instance.value
                                    , amount = instance.amount)

        if instance.isOpen:
            if instance.document.documentType == 'IN':
                stockMovement.movementType = 'IN'
                stock.amount= F('amount') - instance.amount
            elif instance.document.documentType == 'OUT':
                stockMovement.movementType = 'OUT'
                stock.amount= F('amount') + instance.amount
        else:
            if instance.document.documentType == 'IN':
                stockMovement.movementType = 'OUT'
                stock.amount= F('amount') + instance.amount
            elif instance.document.documentType == 'OUT':
                stockMovement.movementType = 'IN'
                stock.amount= F('amount') - instance.amount

        stock.value = instance.value
        stock.save()
        stockMovement.save()

        # send price to admin.
        if not instance.isOpen:
            if instance.document.documentType == 'IN':
                product = Product.objects.get(id=instance.product.id)
                margin = 1 if product.margin == 0 else product.margin
                if margin != 1:
                    margin = decimal.Decimal((margin/100)+1)

                Price.objects.filter(deposit = instance.document.deposit
                                   , product = instance.product
                                   , isValid = False).delete()
                now = timezone.now()
                now = now - timezone.timedelta(hours=now.hour
                                                ,minutes=now.minute
                                                ,seconds=now.second
                                                , microseconds=now.microsecond)
                tomorrow = now + timezone.timedelta(days=1)
                price = Price(deposit = instance.document.deposit
                            , product = instance.product
                            , value = instance.value * margin
                            , startedAt = tomorrow
                            , priceType='NO')
                price.save()