from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.dispatch import receiver
import traceback

class Stock(models.Model):

    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def isValid(self):
        if self.deletedAt:
            return False
        else:
            return True
    
    def total(self):
        return self.value * self.amount

    def __str__(self):
        return f'o deposito {self.deposit.name} tem {self.amount} do produto {self.product}'

    def delete(self):
        if self.amount == 0:
            self.deletedAt = timezone.now()
            self.save()
            return True
        else:
            raise ValidationError(f'don\'t delete stock if amount is greater zero.[{self.amount}]')

    def open(self):
        self.deletedAt = None
        self.save()
    
    def close(self):
        self.delete()


@receiver(pre_save, sender=Stock)
def pre_save_stock(sender, instance, *args, **kwargs):

    if instance.deposit.company.deletedAt:
        raise ValidationError('company is close, verify.')
    
    if instance.deposit.deletedAt:
        raise ValidationError('deposit is close, verify.')
    
    if instance.product.deletedAt:
        raise ValidationError('product deleted, verify.')
    
    if instance.value < 0:
        raise ValidationError('don\'t use negative values.')

    stock = Stock.objects.filter(id=instance.id)
    if stock:
        if instance.deletedAt and stock[0].amount != 0:
            raise ValidationError('don\'t delete stock if amount is greater zero.')
        
        if stock[0].deletedAt is None and instance.deletedAt:
            return True
        
        if stock[0].deletedAt is not None and instance.deletedAt is None:
            return True

    else:
        if instance.deletedAt:
            raise ValidationError('don\'t create stock deleted.')

    stack = [x.name for x in traceback.extract_stack()]
    if 'pre_save_DocumentProduct' not in stack:
        raise ValidationError('only alter stock with document')
