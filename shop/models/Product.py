from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Product(models.Model):

    name = models.CharField(max_length=30)
    margin = models.DecimalField(max_digits=5,decimal_places=3,default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name'),)

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()
        return True

@receiver(post_save,sender=Product)
def save_product(sender, instance, created, **kwargs):
    if created:
        pass