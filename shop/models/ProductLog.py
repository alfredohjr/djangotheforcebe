from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

class ProductLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '003.001 - Product Log'
        verbose_name_plural = '003.001 - Products Log'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.createdAt} - [{self.table}].[{self.transaction}].[{self.product_id} - {self.product}] -> {self.message}"

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()
    
    def register(self, id, table, transaction, message):
        self.product_id = id
        self.table = table
        self.transaction = transaction
        self.message = message
        self.save()


@receiver(pre_save, sender=ProductLog)
def pre_save_productLog(sender, instance, *args, **kwargs):

    productLog = ProductLog.objects.filter(id=instance.id)
    if productLog:
        raise ValidationError('don\'t alter log.')
    
    instance.table = instance.table.upper()
    instance.transaction = instance.transaction.upper()
    
