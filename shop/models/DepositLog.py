from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

class DepositLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    deposit = models.ForeignKey('Deposit',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '002.001 - Deposit Log'
        verbose_name_plural = '002.001 - Deposits Log'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.createdAt} - [{self.table}].[{self.transaction}].[{self.deposit_id} - {self.deposit}] -> {self.message}"

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()
    
    def register(self, id, table, transaction, message):
        self.deposit_id = id
        self.table = table
        self.transaction = transaction
        self.message = message
        self.save()


@receiver(pre_save, sender=DepositLog)
def pre_save_depositLog(sender, instance, *args, **kwargs):

    depositLog = DepositLog.objects.filter(id=instance.id)
    if depositLog:
        raise ValidationError('don\'t alter log.')
    
    instance.table = instance.table.upper()
    instance.transaction = instance.transaction.upper()
    
