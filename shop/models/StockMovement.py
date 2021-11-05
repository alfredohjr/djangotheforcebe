from django.db import models

datetime_format = '%d/%m/%Y %H:%M'

class StockMovement(models.Model):

    TYPE_CHOICES = (
    ('IN','Entrada'),
    ('OUT','Saida'),)

    deposit = models.ForeignKey('Deposit', on_delete=models.CASCADE)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=3)
    amount = models.DecimalField(max_digits=10, decimal_places=3)
    movementType = models.CharField(max_length=3,choices=TYPE_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        ret = f'Houve uma movimentação de {self.movementType} no produto '
        ret += f'{self.product.name} dentro do deposito {self.deposit.name} '
        ret += f'na data {self.createdAt.strftime(datetime_format)}'
        return ret
    
    def delete(self):
        return True