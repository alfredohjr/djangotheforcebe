from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from shop.models.DocumentProduct import DocumentProduct
from shop.models.DocumentLog import DocumentLog

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

    @property
    def total(self):
        products = DocumentProduct.objects.filter(document__id=self.id)
        total = 0
        for p in products:
            total += p.value * p.amount
        return "$%.2f" %total

    def __str__(self):
        return self.key

    class Meta:
        unique_together = (('key','documentType'),)
        verbose_name = '007 - Document'
        verbose_name_plural = '007 - Document'

    def delete(self):

        if self.isOpen:
            self.deletedAt = timezone.now()
            self.save()
            log = DocumentLog()
            log.register(id=self.id, table='document', transaction='del', message='delete')

    def open(self):
        self.isOpen = True
        self.save()

    def close(self):
        self.isOpen = False
        self.save()


@receiver(pre_save, sender=Document)
def save_document(sender, instance, **kwargs):
    
    if instance.deposit.deletedAt:
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

    if queryset:
        if queryset[0].deletedAt:
            if instance.deletedAt != None:
                raise ValidationError('don\'t alter document closed.')

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
    else:
        if instance.deletedAt:
            raise ValidationError('don\'t create document deleted.')

    # for log
    if queryset:
        message = []
        if queryset[0].key != instance.key:
            message.append(f'key_from={queryset[0].key}, key_to={instance.key}')
        
        if queryset[0].deposit != instance.deposit:
            message.append(f'deposit_from={queryset[0].deposit}, deposit_to={instance.deposit}')

        if queryset[0].entity != instance.entity:
            message.append(f'entity_from={queryset[0].entity}, entity_to={instance.entity}')

        if queryset[0].documentType != instance.documentType:
            message.append(f'documentType_from={queryset[0].documentType}, documentType={instance.documentType}')

        if queryset[0].isOpen != instance.isOpen:
            message.append(f'isOpen_from={queryset[0].isOpen}, isOpen_to={instance.isOpen}')

        if message:
            log = DocumentLog()
            log.register(id=instance.id, table='document', transaction='UPD', message='|'.join(message))

@receiver(post_save, sender=Document)
def post_save_document(sender, instance, created, *args, **kwargs):
    if created:
        log = DocumentLog()
        log.register(id=instance.id, table='document', transaction='CRE', message='created')