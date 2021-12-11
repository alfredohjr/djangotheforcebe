from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save


class InventoryLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    inventory = models.ForeignKey('Inventory',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError('Inventory Log cannot be updated')
        super().save(*args, **kwargs)

@receiver(pre_save, sender=InventoryLog)
def pre_save_entityLog(sender, instance, *args, **kwargs):
    pass