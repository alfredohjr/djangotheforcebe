from django.db import models

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