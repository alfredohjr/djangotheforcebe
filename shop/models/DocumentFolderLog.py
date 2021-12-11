from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class DocumentFolderLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    documentFolder = models.ForeignKey('DocumentFolder',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.pk:
            raise ValidationError('This object is not editable')
        super().save(*args, **kwargs)

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()
    
    def register(self, id, table, transaction, message):
        self.documentFolder_id = id
        self.table = table
        self.transaction = transaction
        self.message = message
        self.save()
    
