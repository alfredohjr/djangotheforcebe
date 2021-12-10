from django.db import models


class PaymentMethod(models.Model):

    name = models.CharField(max_length=50)
    inCash = models.BooleanField(default=False)
    isPortion = models.BooleanField(default=False)
    portionAmount = models.IntegerField()
    portionRegex = models.TextField(default='NA')
    dueDate = models.IntegerField()
    percentagePerDelay = models.DecimalField(max_digits=6, decimal_places=3)
    percentageDiscount = models.DecimalField(max_digits=6, decimal_places=3)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name