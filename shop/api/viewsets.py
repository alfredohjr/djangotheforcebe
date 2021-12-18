from django.http.response import HttpResponse
from django.test.testcases import _AssertTemplateUsedContext
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.permissions import DjangoModelPermissions
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
import json

from shop.api.serializers import (
    CompanySerializer
    , DepositSerializer
    , DocumentProductSerializer
    , DocumentSerializer
    , EntitySerializer
    , PriceSerializer
    , ProductSerializer
    , ShopProductSerializer
    , StockMovementSerializer
    , StockSerializer
    , CompanyImageSerializer
    , DepositImageSerializer
    , EntityImageSerializer
    , ProductImageSerializer)

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
    """
    Manage company.

    """

    serializer_class = CompanySerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Company.objects.filter(deletedAt=None)
        return queryset


class CompanyImageViewSet(UpdateAPIView):
    
    queryset = Company.objects.filter(deletedAt=None)
    serializer_class = CompanyImageSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        file = request.data['file']
        company = Company.objects.get(pk=kwargs['pk'])
        company.logo = file
        company.save()
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class DepositViewSets(viewsets.ModelViewSet):

    serializer_class = DepositSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Deposit.objects.filter(deletedAt=None)
        return queryset


class DepositImageViewSet(UpdateAPIView):
    
    queryset = Deposit.objects.filter(deletedAt=None)
    serializer_class = DepositImageSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        file = request.data['file']
        company = Deposit.objects.get(pk=kwargs['pk'])
        company.logo = file
        company.save()
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class ProductViewSets(viewsets.ModelViewSet):

    serializer_class = ProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Product.objects.filter(deletedAt=None)
        return queryset


class ProductImageViewSet(UpdateAPIView):
    
    queryset = Product.objects.filter(deletedAt=None)
    serializer_class = ProductImageSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        file = request.data['file']
        company = Product.objects.get(pk=kwargs['pk'])
        company.logo = file
        company.save()
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class PriceViewSets(viewsets.ModelViewSet):

    serializer_class = PriceSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Price.objects.filter(deletedAt=None, startedAt__lte=timezone.now())
        return queryset


class StockViewSets(viewsets.ReadOnlyModelViewSet):

    serializer_class = StockSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Stock.objects.filter(deletedAt=None)
        return queryset


class StockMovementViewSets(viewsets.ReadOnlyModelViewSet):

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


class EntityImageViewSet(UpdateAPIView):
    
    queryset = Entity.objects.filter(deletedAt=None)
    serializer_class = EntityImageSerializer
    lookup_field = 'pk'

    def update(self, request, *args, **kwargs):
        file = request.data['file']
        company = Entity.objects.get(pk=kwargs['pk'])
        company.logo = file
        company.save()
        return HttpResponse(json.dumps({'message': "Uploaded"}), status=200)


class DocumentViewSets(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = Document.objects.filter(deletedAt=None)
        return queryset


class DocumentCloseViewSet(UpdateAPIView):

    queryset = Document.objects.filter(deletedAt=None)

    def update(self, request, *args, **kwargs):
        document = Document.objects.get(pk=kwargs['pk'])
        document.close()
        return HttpResponse(json.dumps({'message': "Closed"}), status=200)


class DocumentReOpenViewSet(UpdateAPIView):

    queryset = Document.objects.filter(deletedAt=None)

    def update(self, request, *args, **kwargs):
        if 'reason' in request.data:
            document = Document.objects.get(pk=kwargs['pk'])
            document.reOpenDocument(reason=request.data['reason'])
            return HttpResponse(json.dumps({'message': "open"}), status=200)
        else:
            return HttpResponse(json.dumps({'message': "Reason is required"}), status=400)


class DocumentProductViewSets(viewsets.ModelViewSet):

    serializer_class = DocumentProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        queryset = DocumentProduct.objects.filter(deletedAt=None)
        return queryset


class ShopProductViewSet(viewsets.ReadOnlyModelViewSet):

    serializer_class = ShopProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        
        queryset = Stock.objects.filter(deletedAt=None).exclude(amount=0)
        for q in queryset:
            price = Price.objects.filter(
                product=q.product
                , deposit=q.deposit
                , startedAt__lte=timezone.now()
                , isValid=True
                , priceType='NO').first()
            if not price:
                queryset = queryset.exclude(id=q.id)

        return queryset
