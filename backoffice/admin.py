from django.contrib import admin

# Register your models here.

from backoffice.models.PaymentMethod import PaymentMethod
from backoffice.models.PayReceive import PayReceive

admin.site.register(PaymentMethod)
admin.site.register(PayReceive)