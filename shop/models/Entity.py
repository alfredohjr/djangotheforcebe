from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone
from shop.core.validators.cnpj import ValidateCNPJ
from shop.core.validators.cpf import ValidateCPF

from shop.models.Document import Document

class Entity(models.Model):

    IDENTIFIER_TYPE = (
        ('FI','Fisica'),
        ('JU','Juridica')
    )

    ENTITY_TYPE = (
        ('CLI','Cliente'),
        ('FOR','Fornecedor')
    )

    name = models.CharField(max_length=50)
    identifier = models.CharField(max_length=30)
    identifierType = models.CharField(max_length=3,choices=IDENTIFIER_TYPE)
    entityType = models.CharField(max_length=3,choices=ENTITY_TYPE)
    isActive = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name','identifier','identifierType','entityType'),)

    def delete(self):

        document = Document.objects.filter(isOpen=True,entity__id=self.id)
        if document:
            raise ValidationError('document is open, verify.')

        self.deletedAt = timezone.now()
        self.save()


@receiver(pre_save,sender=Entity)
def pre_save_entity(sender, instance, *args, **kwargs):

    if len(instance.name.strip()) < 10:
        raise ValidationError('minimum size of name is 10, please check.')

    if instance.identifierType not in ['JU','FI']:
        raise ValidationError('Please, only types (FI) fisica and (JU) juridica is valid')

    if instance.identifierType == 'JU':
        cnpj = ValidateCNPJ(instance.identifier)
        if not cnpj.run():
            raise ValidationError('invalid CNPJ number, please verify.')
    elif instance.identifierType == 'FI':
        cpf = ValidateCPF(instance.identifier)
        if cpf.run():
            pass
        else:
            raise ValidationError('invalid CPF number, please verify.')

    entity = Entity.objects.filter(id=instance.id)
    if entity:
        if instance.deletedAt is None and entity[0].deletedAt:
            return True

        if entity[0].deletedAt:
            raise ValidationError('company is deleted, to alter this, reopen.')
    else:
        if instance.deletedAt != None:
            raise ValidationError('don\'t create entity with deleted or closed, please verify.')