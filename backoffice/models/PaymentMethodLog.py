from django.db import models
from django.utils import timezone

class PaymentMethodLog(models.Model):

    TRANSACTION = (
        ('CRE','Create'),
        ('UPD','Update'),
        ('DEL','Delete'),
    )

    paymentMethod = models.ForeignKey('PaymentMethod',on_delete=models.CASCADE)
    table = models.CharField(max_length=50)
    transaction = models.CharField(max_length=3)
    message = models.TextField()

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(blank=True, null=True)

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()
   
    def register(self, id, table, transaction, message):
        self.paymentMethod_id = id
        self.table = table
        self.transaction = transaction
        self.message = message
        self.save()