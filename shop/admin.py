from django.contrib import admin
from django.db.models import fields

from shop.models.Company import Company
from shop.models.Deposit import Deposit
from shop.models.Product import Product
from shop.models.Price import Price
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement
from shop.models.Entity import Entity
from shop.models.Document import Document
from shop.models.DocumentProduct import DocumentProduct

# Register your models here.

#actions
@admin.action(description='Marcar sugestão de preço como ativo')
def price_isValidTrue(modeladmin, request, queryset):
    queryset.update(isValid=True)

@admin.action(description='Marcar sugestão de preço como inativo')
def price_isValidFalse(modeladmin, request, queryset):
    queryset.update(isValid=False)


class MainAdmin(admin.ModelAdmin):
    exclude = ['deletedAt']

class DepositAdmin(MainAdmin):
    list_display = ('name','total','totalAmount')

class StockMovementInline(admin.TabularInline):
    model = StockMovement
    exclude = ('deletedAt',)

class StockAdmin(MainAdmin):
    list_display = ('deposit','product','value','amount','total','isValid')

class StockMovementAdmin(MainAdmin):
    list_display = ('deposit','product','movementType','value','amount')

class DocumentProductInline(admin.TabularInline):
    model = DocumentProduct
    exclude = ('deletedAt','delete')

class DocumentAdmin(MainAdmin):
    list_display = ('key','deposit','entity','total')
    inlines = [DocumentProductInline,]

class DocumentProductAdmin(MainAdmin):
    exclude = ['deletedAt','isOpen']
    list_display = ('document','product','amount','value')

class PriceAdmin(MainAdmin):
    list_display = ('deposit','product','value','priceType','startedAt','finishedAt','isValid','stockNow')
    actions = [price_isValidTrue,price_isValidFalse]

class ProductAdmin(MainAdmin):
    list_display = ('name','margin')

admin.site.register(Company, MainAdmin)
admin.site.register(Deposit, DepositAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Entity, MainAdmin)
admin.site.register(Document, DocumentAdmin)
