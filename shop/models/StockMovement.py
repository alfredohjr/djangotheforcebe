import traceback
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save

from shop.models.Stock import Stock

datetime_format = '%d/%m/%Y %H:%M'

class StockMovement(models.Model):

    TYPE_CHOICES = (
    ('IN','Entrada'),
    ('OUT','Saida'),)

    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    movementType = models.CharField(max_length=3,choices=TYPE_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        ret = f'Houve uma movimentação de {self.movementType} no produto '
        ret += f'{self.product.name} dentro do deposito {self.deposit.name} '
        ret += f'na data {self.createdAt.strftime(datetime_format)}'
        return ret
    
    def delete(self):
        return True
    

@receiver(pre_save, sender=StockMovement)
def pre_save_stockMovement(sender, instance, *args, **kwargs):

    stockMovement = StockMovement.objects.filter(id=instance.id)
    if stockMovement:
        raise ValidationError('don\'t update stock movement.')

    if instance.deposit.company.deletedAt:
        raise ValidationError('don\'t create stock movement with company is closed.')
    
    if instance.deposit.deletedAt:
        raise ValidationError('don\'t create stock movement with deposit is closed.')

    if instance.product.deletedAt:
        raise ValidationError('don\'t create stock movement with product deleted.')
    
    stock = Stock.objects.filter(deposit=instance.deposit, product=instance.product)
    if stock:
        if stock[0].deletedAt:
            raise ValidationError('stock is closed, verify.')
    else:
        raise ValidationError('don\'t create stock movement without stock, verify.')

    stack = [x.name for x in traceback.extract_stack()]
    if 'pre_save_DocumentProduct' not in stack:
        raise ValidationError('only create/update stock movement with document.')