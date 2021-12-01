from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from shop.models.Inventory import Inventory

from shop.models.Stock import Stock
from shop.models.DepositLog import DepositLog

class Deposit(models.Model):

    name = models.CharField(max_length=30)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    logo = models.ImageField(upload_to='deposit', null=True, blank=True)
    cep = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    complement = models.CharField(max_length=200, null=True, blank=True)
    phone1 = models.CharField(max_length=30, null=True, blank=True)
    phone2 = models.CharField(max_length=30, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    deletedAt = models.DateTimeField(null=True, blank=True)

    def total(self):
        total = 0
        stock = Stock.objects.filter(deposit_id = self.id)
        for s in stock:
            total += s.value * s.amount
        return total

    def totalAmount(self):
        total = 0
        stock = Stock.objects.filter(deposit_id = self.id)
        for s in stock:
            total += s.amount
        return total

    def __str__(self):
        return self.name

    class Meta:
        unique_together = (('name'),)

    def open(self):
        self.deletedAt = None
        self.save()

    def close(self):
        self.delete()

    def delete(self):
        stocks = Stock.objects.filter(deposit__id=self.id)
        for stock in stocks:
            if stock.amount != 0:
                raise ValidationError('don\'t delete deposit with product stock.')

        inventory = Inventory.objects.filter(deposit__id=self.id, isOpen=True)
        if inventory:
            raise ValidationError('don\'t delete deposit with inventory open')

        self.deletedAt = timezone.now()
        self.save()
        log = DepositLog()
        log.register(id=self.id, table='deposit', transaction='del', message='delete')

@receiver(pre_save,sender=Deposit)
def pre_save_deposit(sender, instance, *args, **kwargs):
    
    if len(instance.name) < 10:
        raise ValidationError('minimum size is 10.')
    
    if instance.company.deletedAt != None:
        raise ValidationError('company is inactive, please check.')
    
    if instance.deletedAt:
        stocks = Stock.objects.filter(deposit__id=instance.id)
        if stocks:
            for stock in stocks:
                if stock.amount != 0:
                    raise ValidationError('don\'t delete deposit with product stock.')

    deposit = Deposit.objects.filter(id=instance.id)
    if deposit:
        log = DepositLog()
        if instance.deletedAt is None and deposit[0].deletedAt:
            log.register(id=instance.id, table='deposit', transaction='UPD', message='return deleted deposit')
            return True

        if deposit[0].deletedAt:
            raise ValidationError('deposit is deleted, to alter this, reopen.')

        # for log
        message = []
        if deposit[0].name != instance.name:
            message.append(f'name_from={deposit[0].name}, name_to={instance.name}')
        
        if deposit[0].company != instance.company:
            message.append(f'company_from={deposit[0].company.id}, company_to={instance.company.id}')

        if deposit[0].email != instance.email:
            message.append(f'email_from={deposit[0].email},email_to={instance.email} ')

        if deposit[0].logo != instance.logo:
            message.append(f'logo_from={deposit[0].logo},logo_to={instance.logo} ')

        if deposit[0].cep != instance.cep:
            message.append(f'cep_from={deposit[0].cep},cep_to={instance.cep} ')

        if deposit[0].state != instance.state:
            message.append(f'state_from={deposit[0].state},state_to={instance.state} ')

        if deposit[0].city != instance.city:
            message.append(f'city_from={deposit[0].city},city_to={instance.city} ')

        if deposit[0].address != instance.address:
            message.append(f'address_from={deposit[0].address},address_to={instance.address} ')

        if deposit[0].complement != instance.complement:
            message.append(f'complement_from={deposit[0].complement},complement_to={instance.complement} ')

        if deposit[0].phone1 != instance.phone1:
            message.append(f'phone1_from={deposit[0].phone1},phone1_to={instance.phone1} ')

        if deposit[0].phone2 != instance.phone2:
            message.append(f'phone2_from={deposit[0].phone2},phone2_to={instance.phone2} ')

        if message:
            log.register(id=instance.id,table='deposit',transaction='UPD', message='|'.join(message))
    else:
        if instance.deletedAt:
            raise ValidationError('don\'t create deposit with closed flag.')


@receiver(post_save,sender=Deposit)
def post_save_deposit(sender, instance, created, *args, **kwargs):
    if created:
        log = DepositLog()
        log.register(id=instance.id,table='deposit',transaction='cre',message='created')
        if instance.deletedAt != None:
            company = Deposit.objects.get(id=instance.id)
            company.deletedAt = None
            company.save()
            return True