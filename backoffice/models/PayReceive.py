from django.db import models


class PayReceive(models.Model):

    document = models.ForeignKey('shop.Document', on_delete=models.CASCADE)
    paymentMethod = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)
    portionNumber = models.IntegerField()
    value = models.DecimalField(max_digits=10,decimal_places=3)
    valueExtra = models.DecimalField(max_digits=10, decimal_places=3)
    valueDiscount = models.DecimalField(max_digits=10, decimal_places=3)
    paymentDateFixed = models.DateTimeField()
    paymentDateAccomplished = models.DateTimeField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.document.key} parcela {self.portionNumber}X de R${round(self.value,2)}'