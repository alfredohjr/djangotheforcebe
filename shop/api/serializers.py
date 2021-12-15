from rest_framework import serializers
from django.utils import timezone

from shop.models.Company import Company
from shop.models.Deposit import Deposit
from shop.models.Document import Document
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Entity import Entity
from shop.models.Price import Price
from shop.models.Product import Product
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement


class CompanySerializer(serializers.ModelSerializer):

    class Meta:
        model=Company
        exclude=['deletedAt']


class CompanyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'logo')


class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model=Deposit
        exclude=['deletedAt']


class DepositImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ('name', 'logo')


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        exclude=['deletedAt']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'logo')


class PriceSerializer(serializers.ModelSerializer):

    value = serializers.FloatField()

    class Meta:
        model=Price
        exclude=['deletedAt']


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model=Stock
        exclude=['deletedAt']


class StockMovementSerializer(serializers.ModelSerializer):

    class Meta:
        model=StockMovement
        exclude=['deletedAt']


class EntitySerializer(serializers.ModelSerializer):

    class Meta:
        model=Entity
        exclude=['deletedAt']


class EntityImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = ('name', 'logo')


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Document
        exclude=['deletedAt']


class DocumentProductSerializer(serializers.ModelSerializer):

    amount = serializers.FloatField()

    class Meta:
        model=DocumentProduct
        exclude=['deletedAt']


class forShopProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        exclude = ['deletedAt','margin','createdAt','updatedAt']


class forShopDepositSerializer(serializers.ModelSerializer):

    class Meta:
        model = Deposit
        exclude = ['deletedAt','createdAt','updatedAt']


class ShopProductSerializer(serializers.ModelSerializer):

    amount = serializers.IntegerField()
    product = forShopProductSerializer()
    deposit = forShopDepositSerializer()
    price1 = serializers.SerializerMethodField()
    price2 = serializers.SerializerMethodField()

    def get_price1(self, obj):
        queryset = Price.objects.filter(deposit=obj.deposit, product=obj.product, deletedAt=None)
        queryset = queryset.filter(priceType='NO')
        queryset = queryset.filter(isValid=True)
        queryset = queryset.filter(startedAt__lte=timezone.now())

        queryset = queryset.order_by('-updatedAt').first()
        if queryset:
            return queryset.value
        return None

    def get_price2(self, obj):
        queryset = Price.objects.filter(deposit=obj.deposit, product=obj.product, deletedAt=None)
        queryset = queryset.filter(priceType='OF')
        queryset = queryset.filter(isValid=True)
        queryset = queryset.filter(startedAt__lte=timezone.now(),finishedAt__gte=timezone.now())

        queryset = queryset.order_by('-updatedAt').first()
        if queryset:
            return queryset.value
        return None

    class Meta:
        model=Stock
        exclude=['deletedAt','createdAt','updatedAt','value']