from django.contrib import admin

# Register your models here.

from backoffice.models.PaymentMethod import PaymentMethod

admin.site.register(PaymentMethod)