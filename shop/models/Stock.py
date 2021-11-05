from django.db import models
from django.utils import timezone

class Stock(models.Model):

    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=3,default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def isValid(self):
        if self.deletedAt:
            return False
        else:
            return True
    
    def total(self):
        return self.value * self.amount

    def __str__(self):
        return f'o deposito {self.deposit.name} tem {self.amount} do produto {self.product}'

    def delete(self):
        if self.amount == 0:
            self.deletedAt = timezone.now()
            self.save()
            return True
        else:
            return False