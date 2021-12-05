from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from shop.models.Document import Document
from shop.models.DocumentFolder import DocumentFolder
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Entity import Entity

from shop.models.InventoryLog import InventoryLog
from shop.models.InventoryProduct import InventoryProduct


class Inventory(models.Model):

    name = models.CharField(max_length=50)
    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE)
    startedAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    isOpen = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name','deposit','createdAt'),)
        pass

    def delete(self):
        if self.pk:
            obj = Inventory.objects.get(id=self.id)
            if obj.isOpen is False:
                raise ValidationError('don\'t delete closed inventory' )
            self.deletedAt = timezone.now()
            self.save()
        else:
            raise ValidationError('don\'t create inventory deleted')

    def save(self, *args, **kwargs):
        if self.deposit.deletedAt:
            raise ValidationError('don\'t open inventory with deposit closed')

        created = False
        obj = None
        if self.pk:
            obj = Inventory.objects.get(id=self.id)
            if obj.startedAt and self.startedAt and self.isOpen:
                raise ValidationError('don\'t alter inventory if started')
            
            if obj.isOpen is False and self.isOpen:
                raise ValidationError('don\'t open inventory closed')

            if self.isOpen is False:
                inventoryProduct = InventoryProduct.objects.filter(inventory=self)
                if inventoryProduct is None:
                    raise ValidationError('inventory without product, verify')

            if obj.startedAt is None and self.startedAt:
                inventoryProduct = InventoryProduct.objects.filter(inventory=self)
                if inventoryProduct:
                    for ip in inventoryProduct:
                        ip.startedAt = self.startedAt
                        ip.save()
                else:
                    raise ValidationError('don\'t start inventory without product')
            
            if obj.isOpen and self.isOpen is False and obj.startedAt is None:
                raise ValidationError('don\'t close inventory without start')

            if obj.isOpen and self.isOpen is False:
                inventoryProduct = InventoryProduct.objects.filter(inventory=self)
                obj2upd = {}
                obj2upd['IN'] = []
                obj2upd['OUT'] = []
                for p in inventoryProduct:
                    if p.valueBefore < p.value:
                        amount = p.value - p.valueBefore
                        obj2upd['IN'].append({'product':p.product.id, 'amount': amount})
                    elif p.valueBefore > p.value:
                        amount = p.valueBefore - p.value
                        obj2upd['OUT'].append({'product':p.product.id, 'amount': amount})

                if obj2upd['IN']:
                    folder = DocumentFolder.objects.filter(name__contains='INVENTARIO ENTRADA',documentType='IN')
                    if not folder:
                        raise ValidationError('please, add folder "INVENTARIO ENTRADA" with TYPE "IN"')
                    entity = Entity.objects.filter(name__contains=f'{self.deposit.name}INVIN',entityType='FOR')
                    if not entity:
                        raise ValidationError(f'please, add entity "{self.deposit.name}INVIN" with TYPE "FOR"')
                                      
                    document = Document()
                    document.key = f'[INV]-{timezone.now().strftime("%Y%m%d%H%M%S")}'
                    document.deposit = self.deposit
                    document.entity = entity[0]
                    document.folder = folder[0]
                    document.save()

                    for p in obj2upd['IN']:
                        dp = DocumentProduct()
                        dp.document = document
                        dp.product_id = p.get('product')
                        dp.amount = p.get('amount')
                        dp.value = 1
                        dp.save()

                    document = Document.objects.get(id=document.id)
                    document.close()

                if obj2upd['OUT']:
                    folder = DocumentFolder.objects.filter(name__contains='INVENTARIO SAIDA',documentType='OUT')
                    if not folder:
                        raise ValidationError('please, add folder "INVENTARIO SAIDA" with TYPE "OUT"')
                    entity = Entity.objects.filter(name__contains=f'{self.deposit.name}INVOUT',entityType='CLI')
                    if not entity:
                        raise ValidationError(f'please, add entity "{self.deposit.name}INVOUT" with TYPE "CLI"')
                                      
                    document = Document()
                    document.key = f'[INV]-{timezone.now().strftime("%Y%m%d%H%M%S")}'
                    document.deposit = self.deposit
                    document.entity = entity[0]
                    document.folder = folder[0]
                    document.save()

                    for p in obj2upd['OUT']:
                        dp = DocumentProduct()
                        dp.document = document
                        dp.product_id = p.get('product')
                        dp.amount = p.get('amount')
                        dp.value = 1
                        dp.save()
                    
                    document.isOpen = False
                    document.save()
                
                for ip in inventoryProduct:
                    ip.isOpen = False
                    ip.save()
                self.isOpen = False
        else:
            created = True
            if self.startedAt:
                raise ValidationError('don\'t create and start inventory in same time')

        super().save(*args, **kwargs)

        #for logs
        messages = []
        if self.pk and obj:
            if obj.name != self.name:
                messages.append(f'name_from={obj.name}, name_to={self.name}')
            if obj.deposit != self.deposit:
                messages.append(f'deposit_from={obj.deposit}, deposit_to={self.deposit}')

            if obj.startedAt != self.startedAt:
                messages.append(f'startedAt_from={obj.startedAt}, startedAt_to={self.startedAt}')

            if obj.createdAt != self.createdAt:
                messages.append(f'createdAt_from={obj.createdAt}, createdAt_to={self.createdAt}')

            if obj.updatedAt != self.updatedAt:
                messages.append(f'updatedAt_from={obj.updatedAt}, updatedAt_to={self.updatedAt}')

            if obj.deletedAt != self.deletedAt:
                messages.append(f'deletedAt_from={obj.deletedAt}, deletedAt_to={self.deletedAt}')

            if obj.isOpen != self.isOpen:
                messages.append(f'isOpen_from={obj.isOpen}, isOpen_to={self.isOpen}')


            if messages:
                log = InventoryLog()
                log.inventory = self
                log.table = 'inventory'
                log.transaction = 'upd' if self.deletedAt is None else 'del'
                log.message = '|'.join(messages)
                log.save()
        
        if created:
            inventory = Inventory.objects.get(deposit=self.deposit, name=self.name, createdAt=self.createdAt)
            if self.deletedAt is None:
                log = InventoryLog()
                log.inventory = inventory
                log.table = 'inventory'
                log.transaction = 'cre'
                log.message = 'created'
                log.save()