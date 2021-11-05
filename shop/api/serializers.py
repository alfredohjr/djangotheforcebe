from rest_framework import serializers

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


class DepositSerializer(serializers.ModelSerializer):

    class Meta:
        model=Deposit
        exclude=['deletedAt']


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=Product
        exclude=['deletedAt']


class PriceSerializer(serializers.ModelSerializer):

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


class DocumentSerializer(serializers.ModelSerializer):

    class Meta:
        model=Document
        exclude=['deletedAt']


class DocumentProductSerializer(serializers.ModelSerializer):

    class Meta:
        model=DocumentProduct
        exclude=['deletedAt']