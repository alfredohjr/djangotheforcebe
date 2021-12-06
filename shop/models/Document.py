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
    folder = models.ForeignKey('DocumentFolder', on_delete=models.CASCADE)
    isOpen = models.BooleanField(default=True)
    deliveryValue = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    sendMail = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def subtotal(self):
        products = DocumentProduct.objects.filter(document__id=self.id)
        total = 0
        for p in products:
            total += p.value * p.amount
        return total

    def total(self):
        return self.subtotal() + self.deliveryValue

    def __str__(self):
        return self.key

    class Meta:
        unique_together = (('key','deposit','entity','folder'),)

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
    
    if instance.folder.order and instance.folder.documentType == 'OUT':
        instance.sendMail = True

    if instance.isOpen == False:
        documentProduct = DocumentProduct.objects.filter(document=instance.id,deletedAt=None)
        if not documentProduct and instance.folder.product:
            raise ValidationError('document don\'t close without product.')    
    
    if (instance.folder.documentType == 'IN') and (instance.entity.entityType == 'CLI'):
        raise ValidationError('Document is IN and entity is client, please, verify')
    
    if (instance.folder.documentType == 'OUT') and (instance.entity.entityType == 'FOR'):
        raise ValidationError('Document is OUT and entity is For, please, verify')

    queryset = Document.objects.filter(id=instance.id)

    if queryset:
        if queryset[0].deletedAt:
            if instance.deletedAt != None:
                raise ValidationError('don\'t alter document closed.')

        if not queryset[0].isOpen and not instance.isOpen:
            if queryset[0].sendMail == instance.sendMail:
                raise ValidationError('document is closed, don\'t alter this.')

        if not queryset[0].isOpen and instance.isOpen:
            instance.key = queryset[0].key
            instance.deposit = queryset[0].deposit
            instance.entity = queryset[0].entity
            instance.folder.documentType = queryset[0].folder.documentType
            instance.deliveryValue = queryset[0].deliveryValue

            documentProduct = DocumentProduct.objects.filter(document__id=instance.id)
            if documentProduct:
                for docprod in documentProduct:
                    if docprod.product.isInventoryOpen():
                        raise ValidationError('don\'t reopen document with product inventory')

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
        if instance.entity.entityType == 'FOR' and instance.folder.documentType == 'OUT':
            raise ValidationError('don\'t create document OUT with entity FOR')

    # for log
    if queryset:
        message = []
        if queryset[0].key != instance.key:
            message.append(f'key_from={queryset[0].key}, key_to={instance.key}')
        
        if queryset[0].deposit != instance.deposit:
            message.append(f'deposit_from={queryset[0].deposit}, deposit_to={instance.deposit}')

        if queryset[0].entity != instance.entity:
            message.append(f'entity_from={queryset[0].entity}, entity_to={instance.entity}')

        if queryset[0].folder.documentType != instance.folder.documentType:
            message.append(f'documentType_from={queryset[0].documentType}, documentType={instance.documentType}')

        if queryset[0].isOpen != instance.isOpen:
            message.append(f'isOpen_from={queryset[0].isOpen}, isOpen_to={instance.isOpen}')

        if queryset[0].deliveryValue != instance.deliveryValue:
            message.append(f'deliveryValue_from={queryset[0].deliveryValue}, deliveryValue_to={instance.deliveryValue}')

        if message:
            log = DocumentLog()
            log.register(id=instance.id, table='document', transaction='UPD', message='|'.join(message))

@receiver(post_save, sender=Document)
def post_save_document(sender, instance, created, *args, **kwargs):
    if created:
        log = DocumentLog()
        log.register(id=instance.id, table='document', transaction='CRE', message='created')