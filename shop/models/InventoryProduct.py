from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from shop.models.Stock import Stock
from shop.models.InventoryLog import InventoryLog


class InventoryProduct(models.Model):

    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    value = models.IntegerField()
    valueBefore = models.IntegerField(default=0)
    startedAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    isOpen = models.BooleanField(default=True)

    def save(self, *args, **kwargs):

        created = False
        obj = None
        if self.pk:
            obj = InventoryProduct.objects.get(id=self.id)
            if self.product.isDocumentOpen() and self.startedAt:
                raise ValidationError('don\'t open inventory with document open')

            if obj.startedAt is None and self.startedAt:
                stock = Stock.objects.filter(deposit=self.inventory.deposit, product=self.product)
                if stock:
                    self.valueBefore = stock[0].amount
                else:
                    self.valueBefore = 0
            
            if obj.isOpen is False and self.isOpen is False:
                raise ValidationError('don\'t alter closed inventory')
            
            if obj.isOpen is False and self.deletedAt:
                raise ValidationError('don\'t delete if inventory is closed')

            if obj.isOpen is False and self.isOpen:
                raise ValidationError('don\'t alter closed inventory')
            
            if obj.isOpen and self.valueBefore != obj.valueBefore and obj.startedAt:
                raise ValidationError('don\'t alter valueBefore after started inventory')
                
        else:
            created = True

        super().save(*args, **kwargs)

        #for logs
        if created:            
            log = InventoryLog()
            log.inventory = self.inventory
            log.table = 'INVENTORYPRODUCT'
            log.transaction = 'cre'
            log.message = f'created,inventoryProduct_id={self.id}'
            log.save()
        else:
            messages = []
            if obj.inventory != self.inventory:
                messages.append(f'inventory_from={obj.inventory}, inventory_to={self.inventory}')

            if obj.product != self.product:
                messages.append(f'product_from={obj.product}, product_to={self.product}')

            if obj.value != self.value:
                messages.append(f'value_from={obj.value}, value_to={self.value}')

            if obj.valueBefore != self.valueBefore:
                messages.append(f'valueBefore_from={obj.valueBefore}, valueBefore_to={self.valueBefore}')

            if obj.startedAt != self.startedAt:
                messages.append(f'startedAt_from={obj.startedAt}, startedAt_to={self.startedAt}')

            if obj.createdAt != self.createdAt:
                messages.append(f'createdAt_from={obj.createdAt}, createdAt_to={self.createdAt}')

            if obj.isOpen != self.isOpen:
                messages.append(f'isOpen_from={obj.isOpen}, isOpen_to={self.isOpen}')

            if obj.deletedAt and self.deletedAt is None:
                messages.append(f'deletedAt_from={obj.deletedAt}, deletedAt_to={self.deletedAt}')           

            if messages:
                log = InventoryLog()
                log.inventory = self.inventory
                log.table = 'INVENTORYPRODUCT'
                log.transaction = 'upd'
                log.message = '|'.join(messages) + f'|inventoryProduct_id={self.id}'
                log.save()

            if obj.deletedAt is None and self.deletedAt:
                message = f'deletedAt_from={obj.deletedAt}, deletedAt_to={self.deletedAt}|inventoryProduct_id={self.id}'
                
                log = InventoryLog()
                log.inventory = self.inventory
                log.table = 'INVENTORYPRODUCT'
                log.transaction = 'del'
                log.message = message
                log.save()
    
    def delete(self):
        self.deletedAt = timezone.now()
        self.save()
