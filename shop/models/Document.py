from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

from shop.models.DocumentProduct import DocumentProduct
from shop.models.Deposit import Deposit

class Document(models.Model):

    DOCUMENT_TYPE = (
        ('IN','Entrada'),
        ('OUT','Saida')
    )

    key = models.CharField(max_length=100)
    deposit = models.ForeignKey('Deposit',on_delete=models.CASCADE)
    entity = models.ForeignKey('Entity',on_delete=models.CASCADE)
    documentType = models.CharField(max_length=3,choices=DOCUMENT_TYPE)
    isOpen = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def total(self):
        products = DocumentProduct.objects.filter(document__id=self.id)
        total = 0
        for p in products:
            total += p.value * p.amount
        return total

    def __str__(self):
        return self.key

    class Meta:
        unique_together = (('key','documentType'),)

    def delete(self):

        if self.isOpen:
            self.deletedAt = timezone.now()
            self.save()


@receiver(pre_save, sender=Document)
def save_document(sender, instance, **kwargs):
    
    deposit = Deposit.objects.filter(id=instance.deposit.id).exclude(deletedAt=None)
    if deposit:
        raise ValidationError('deposit is closed, verify.')

    if instance.entity.deletedAt:
        raise ValidationError('entity is closed, verify.')

    if instance.isOpen == False:
        documentProduct = DocumentProduct.objects.filter(document=instance.id,deletedAt=None)
        if not documentProduct:
            raise ValidationError('document don\'t close without product.')    
    
    if (instance.documentType == 'IN') and (instance.entity.entityType == 'CLI'):
        raise ValidationError('Document is IN and entity is client, please, verify')
    
    if (instance.documentType == 'OUT') and (instance.entity.entityType == 'FOR'):
        raise ValidationError('Document is OUT and entity is For, please, verify')

    queryset = Document.objects.filter(id=instance.id)

    if not queryset:
        return 0
    

    if queryset[0].isOpen == instance.isOpen:
        pass
    else:
        queryset_docprod = DocumentProduct.objects.filter(document__id=instance.id)
        if queryset_docprod:
            for product in queryset_docprod:
                toUpdate = DocumentProduct.objects.get(id=product.id)
                if instance.isOpen:
                    toUpdate.isOpen = True
                else:
                    toUpdate.isOpen = False

                toUpdate.save()
