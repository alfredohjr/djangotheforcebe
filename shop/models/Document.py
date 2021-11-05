from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from shop.models.DocumentProduct import DocumentProduct

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


@receiver(pre_save, sender=Document)
def save_document(sender, instance, **kwargs):
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
