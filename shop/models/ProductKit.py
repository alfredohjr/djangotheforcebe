from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

class ProductKit(models.Model):

    productMain = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='productMain')
    productChild = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='productChild')
    amount = models.IntegerField(default=1)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{} -> {}'.format(self.productMain, self.productChild)

    class Meta:
        unique_together = ('productMain', 'productChild')

    def delete(self):
        self.deletedAt = timezone.now()
        self.save()

    def save(self, *args, **kwargs):
        
        if self.productMain == self.productChild:
            raise ValidationError('ProductMain and ProductChild must be different')
        
        if self.productMain.productType == 'NOR':
            raise ValidationError('ProductMain must be kit')

        productKit = ProductKit.objects.filter(productChild=self.productMain)
        if productKit:
            for pk in productKit:
                pk = ProductKit.objects.filter(productChild=pk.productMain)
                if pk:
                    raise ValidationError('ProductMain must be kit')


        super().save(*args, **kwargs)
    