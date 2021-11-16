from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

class CompanyLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    company = models.ForeignKey('Company',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()
    
    def register(self, id, table, transaction, message):
        self.company_id = id
        self.table = table
        self.transaction = transaction
        self.message = message
        self.save()


@receiver(pre_save, sender=CompanyLog)
def pre_save_companyLog(sender, instance, *args, **kwargs):

    companyLog = CompanyLog.objects.filter(id=instance.id)
    if companyLog:
        raise ValidationError('don\'t alter log.')
    
    instance.table = instance.table.upper()
    instance.transaction = instance.transaction.upper()
    
