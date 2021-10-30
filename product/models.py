from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

import datetime

# Create your models here.

class Product(models.Model):

    name = models.CharField(max_length=30)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class Log(models.Model):

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)


@receiver(post_save,sender=Product)
def save_product(sender, instance, created, **kwargs):
    
    log = Log(product=instance)
    
    if created:
        log.message = 'produto criado'
    else:
        log.message = 'produto alterado'

    log.save()