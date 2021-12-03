from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save


class InventoryProduct(models.Model):

    inventory = models.ForeignKey('Inventory', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    value = models.IntegerField()
    valueBefore = models.IntegerField()
    startedAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    isOpen = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.product.isDocumentOpen():
            raise ValidationError('don\'t open inventory with document open')
        return super().save(*args, **kwargs)


@receiver(pre_save, sender=InventoryProduct)
def pre_save_inventoryProduct(sender, instance, *args, **kwargs):
    pass

@receiver(post_save, sender=InventoryProduct)
def pre_save_inventoryProduct(sender, instance, *args, **kwargs):
    pass