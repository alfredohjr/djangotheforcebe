from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

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

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        if self.portionAmount < 0:
            raise ValidationError('Portion amount must be greater than 0')

        if self.inCash:
            if self.portionAmount != 1:
                raise ValidationError('Portion amount must be 1 when inCash is True')

            if self.isPortion:
                raise ValidationError('Portion must be False when inCash is True')

        super().save(*args, **kwargs)