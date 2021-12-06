from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.expressions import F
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from shop.models.Price import Price
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement
from shop.models.DocumentLog import DocumentLog

import decimal

class DocumentProduct(models.Model):

    document = models.ForeignKey('Document',on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE,related_name='documentproducts')
    amount = models.DecimalField(max_digits=10,decimal_places=3)
    value = models.DecimalField(max_digits=10,decimal_places=3)
    isOpen = models.BooleanField(default=True)
    isNew = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    @property
    def total(self):
        return self.amount * self.value

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()
        log = DocumentLog()
        log.register(id=self.document.id, table='DOCUMENTPRODUCT', transaction='DEL', message=f'deleted, documentProduct_id={self.id}')

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()


@receiver(pre_save,sender=DocumentProduct)
def pre_save_DocumentProduct(sender, instance, **kwargs):

    if instance.document.folder.product is False:
        raise ValidationError('document don\'t accept products, verify')

    documentProduct = DocumentProduct.objects.filter(id=instance.id)
    if not documentProduct:
        if instance.deletedAt is not None:
            raise ValidationError('don\'t create document product with delete.')
        if not instance.isOpen:
            raise ValidationError('don\'t create document product closed flag.')
        if not instance.document.isOpen:
            raise ValidationError('don\'t add products in document closed')
        return 0

    if instance.document.isOpen == False and instance.isOpen == False:
        raise ValidationError('document is closed, verify.')

    if instance.value <= 0:
        raise ValidationError('negative value not allowed.')
    
    if instance.amount <= 0:
        raise ValidationError('negative value not allowed.')

    if documentProduct[0].deletedAt and instance.deletedAt:
        raise ValidationError('don\'t alter document product deleted')
    
    if documentProduct[0].isOpen != instance.isOpen and instance.document.folder.stock:

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
            if instance.document.folder.documentType == 'IN':
                stockMovement.movementType = 'OUT'
                stock.amount= F('amount') - instance.amount
            elif instance.document.folder.documentType == 'OUT':
                stockMovement.movementType = 'IN'
                stock.amount= F('amount') + instance.amount
        else:
            if instance.document.folder.documentType == 'IN':
                stockMovement.movementType = 'IN'
                stock.amount= F('amount') + instance.amount
            elif instance.document.folder.documentType == 'OUT':
                stockMovement.movementType = 'OUT'
                stock.amount= F('amount') - instance.amount

        if instance.document.folder.documentType == 'IN':
            stock.value = instance.value
        
        stock.save()
        stockMovement.save()

    # send price to admin.
    if not instance.isOpen and instance.document.folder.createPrice:
        if instance.document.folder.documentType == 'IN':
            margin = 1 if instance.product.margin == 0 else instance.product.margin
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

    # for logs
    if documentProduct:
        message = []

        if documentProduct[0].document != instance.document:
            message.append(f'document_from={documentProduct[0].document}, document_to={instance.document}')

        if documentProduct[0].product != instance.product:
            message.append(f'product_from={documentProduct[0].product}, product_to={instance.product}')

        if documentProduct[0].amount != instance.amount:
            message.append(f'amount_from={documentProduct[0].product}, amount_to={instance.product}')

        if documentProduct[0].value != instance.value:
            message.append(f'value_from={documentProduct[0].value}, value_to={instance.value}')

        if documentProduct[0].isOpen != instance.isOpen:
            message.append(f'isOpen_from={documentProduct[0].isOpen}, isOpen_to={instance.isOpen}')
        
        if documentProduct[0].isNew != instance.isNew:
            message.append(f'isNew_from={documentProduct[0].isNew}, isNew_to={instance.isNew}')


        if message:
            message.append(f'documentProduct_id={instance.id}')
            log = DocumentLog()
            log.register(
                id=instance.document.id
                ,table='documentproduct'
                ,transaction='UPD'
                ,message='|'.join(message))

@receiver(post_save, sender=DocumentProduct)
def post_save_DocumentProduct(sender, instance, created, *args, **kwargs):
    if created:
        log = DocumentLog()
        log.register(id=instance.document.id, table='documentproduct', transaction='cre', message=f'created, documentProduct_id={instance.id}')