from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions
from django.utils import timezone

from shop.api.serializers import CompanySerializer, DepositSerializer, DocumentProductSerializer, DocumentSerializer, EntitySerializer, PriceSerializer, ProductSerializer, StockMovementSerializer, StockSerializer

from shop.models.Company import Company
from shop.models.Deposit import Deposit
from shop.models.Document import Document
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Entity import Entity
from shop.models.Price import Price
from shop.models.Product import Product
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement

class CompanyViewSets(viewsets.ModelViewSet):

    serializer_class = CompanySerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Company.objects.filter(deletedAt=None)
        return queryset


class DepositViewSets(viewsets.ModelViewSet):

    serializer_class = DepositSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Deposit.objects.filter(deletedAt=None)
        return queryset


class ProductViewSets(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Product.objects.filter(deletedAt=None)
        return queryset


class PriceViewSets(viewsets.ModelViewSet):

    serializer_class = PriceSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Price.objects.filter(deletedAt=None, startedAt__lte=timezone.now())
        return queryset


class StockViewSets(viewsets.ModelViewSet):

    serializer_class = StockSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Stock.objects.filter(deletedAt=None)
        return queryset


class StockMovementViewSets(viewsets.ModelViewSet):

    serializer_class = StockMovementSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = StockMovement.objects.filter(deletedAt=None)
        return queryset


class EntityViewSets(viewsets.ModelViewSet):

    serializer_class = EntitySerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Entity.objects.filter(deletedAt=None)
        return queryset


class DocumentViewSets(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Document.objects.filter(deletedAt=None)
        return queryset


class DocumentProductViewSets(viewsets.ModelViewSet):

    serializer_class = DocumentProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = DocumentProduct.objects.filter(deletedAt=None)
        return queryset