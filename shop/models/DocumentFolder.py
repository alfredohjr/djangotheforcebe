from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from shop.models.Document import Document
from shop.models.DocumentLog import DocumentLog

class DocumentFolder(models.Model):

    DOCUMENT_TYPE = (
        ('IN','Entrada'),
        ('OUT','Saida')
    )

    name = models.CharField(max_length=50)
    documentType = models.CharField(max_length=3,choices=DOCUMENT_TYPE)
    stock = models.BooleanField(default=False)
    product = models.BooleanField(default=False)
    financial = models.BooleanField(default=False)
    order = models.BooleanField(default=False)
    updateCost = models.BooleanField(default=False)
    createPrice = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):

        created = False
        obj = None
        if self.pk:
            document = Document.objects.filter(folder=self)
            obj = DocumentFolder.objects.get(id=self.id)
            if document and obj.deletedAt == self.deletedAt:
                raise ValidationError('don\'t update folder if document exists')

            document = document.filter(isOpen=True)
            if document:
                raise ValidationError('don\'t close folder with document open')
        else:
            created = True
            
        if self.stock and self.product is False:
            raise ValidationError('only created flag stock with product')
        
        if self.createPrice and self.product is False:
            raise ValidationError('only created flag createPrice with product')

        super().save(*args, **kwargs)

        #for logs
        if created:
            pass
        else:
            messages = []
            if obj.name != self.name:
                messages.append(f'name_from={obj.name}, name_to={self.name}')

            
            if messages:
                pass

    
    def delete(self):
        self.deletedAt = timezone.now()
        self.save()