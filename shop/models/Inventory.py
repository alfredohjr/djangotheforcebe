from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

from shop.models.Deposit import Deposit

class Inventory(models.Model):

    name = models.CharField(max_length=50)
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    startedAt = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)
    isOpen = models.BooleanField(default=False)


@receiver(pre_save, sender=Inventory)
def pre_save_inventory(sender, instance, *args, **kwargs):
    pass

@receiver(post_save, sender=Inventory)
def pre_save_inventory(sender, instance, *args, **kwargs):
    pass