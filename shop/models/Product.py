from django.core.checks import messages
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.db import connection

from shop.models.Stock import Stock
from shop.models.ProductLog import ProductLog

def my_custom_sql(sql):
    with connection.cursor() as cursor:
        cursor.execute(sql)
        row = cursor.fetchone()
    return row

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
        verbose_name = '003 - Product'
        verbose_name_plural = '003 - Products'

    @property
    def marginValue(self):
        return "%.2f%%" %self.margin

    def delete(self):

        stock = Stock.objects.filter(product__id=self.id).exclude(amount=0)
        if stock:
            raise ValidationError('product in stock, please verify.')
        
        documentProduct = my_custom_sql(f'select 1 from shop_documentproduct where product_id = {self.id}')
        if documentProduct:
            raise ValidationError('document open with product, verify.')

        self.deletedAt = timezone.now()
        self.save()
        log = ProductLog()
        log.register(id=self.id, table='product', transaction='del', message='deleted')

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()

@receiver(pre_save,sender=Product)
def save_product(sender, instance, **kwargs):
    
    if len(instance.name.strip()) < 10:
        raise ValidationError('minimum size of name is 10.')

    if instance.margin < 0:
        raise ValidationError('dont accept negative values')

    product = Product.objects.filter(id=instance.id)
    if product:
        if instance.deletedAt is None and product[0].deletedAt:
            log = ProductLog()
            log.register(id=instance.id, table='product', transaction='upd', message='return product')
            return True

        if product[0].deletedAt:
            raise ValidationError('don\'t alter product inactive, please verify.')
        
    else:
        if instance.deletedAt != None:
            raise ValidationError('don\'t create product inactive, please verify.')

    # for logs...
    if product:
        messages = []
        if product[0].name != instance.name:
            messages.append(f'name_from={product[0].name}, name_to={instance.name}')

        if product[0].margin != instance.margin:
            messages.append(f'margin_from={product[0].margin}, margin_to={instance.margin}')

        if messages:
            log = ProductLog()
            log.register(id=instance.id, table='product', transaction='upd', message='|'.join(messages))
            

@receiver(post_save, sender=Product)
def post_save_product(sender, instance, created, *args, **kwargs):
    if created:
        log = ProductLog()
        log.register(id=instance.id, table='product', transaction='cre', message='created')