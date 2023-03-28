from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import pre_save

class DocumentLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    document = models.ForeignKey('Document',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = '007.001 - Document Log'
        verbose_name_plural = '007.001 - Documents Log'
        ordering = ['-createdAt']

    def __str__(self):
        return f"{self.createdAt} - [{self.table}].[{self.transaction}].[{self.document_id} - {self.document}] -> {self.message}"

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()
    
    def register(self, id, table, transaction, message):
        self.document_id = id
        self.table = table
        self.transaction = transaction
        self.message = message
        self.save()


@receiver(pre_save, sender=DocumentLog)
def pre_save_documentLog(sender, instance, *args, **kwargs):

    documentLog = DocumentLog.objects.filter(id=instance.id)
    if documentLog:
        raise ValidationError('don\'t alter log.')
    
    instance.table = instance.table.upper()
    instance.transaction = instance.transaction.upper()
    
