from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

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


@receiver(pre_save, sender=DocumentFolder)
def pre_save_DocumentProduct(sender, instance, *args, **kwargs):
    pass

@receiver(post_save, sender=DocumentFolder)
def post_save_DocumentProduct(sender, instance, created, *args, **kwargs):
    pass