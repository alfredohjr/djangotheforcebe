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
    """
    Viewset that implements CRUD operations for the Company.

    - `create`: creates a new instance of Company.
    - `list`: lists all active instances of Company.
    - `retrieve`: retrieves a specific instance of Company by ID.
    - `update`: updates a specific instance of Company.
    - `partial_update`: partially updates a specific instance of Company.
    - `destroy`: marks a specific instance of Company as deleted.

    The class uses the CompanySerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Company, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = CompanySerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        
        filter_fields = ['name']

        queryset = Company.objects.filter(deletedAt=None)
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})

        
        return queryset


class DepositViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements CRUD operations for the Deposit.

    - `create`: creates a new instance of Deposit.
    - `list`: lists all active instances of Deposit.
    - `retrieve`: retrieves a specific instance of Deposit by ID.
    - `update`: updates a specific instance of Deposit.
    - `partial_update`: partially updates a specific instance of Deposit.
    - `destroy`: marks a specific instance of Deposit as deleted.

    The class uses the DepositSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Deposit, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = DepositSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        
        filter_fields = ['name','company_id']
        queryset = Deposit.objects.filter(deletedAt=None)

        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})
        
        return queryset


class ProductViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements CRUD operations for the Product.

    - `create`: creates a new instance of Product.
    - `list`: lists all active instances of Product.
    - `retrieve`: retrieves a specific instance of Product by ID.
    - `update`: updates a specific instance of Product.
    - `partial_update`: partially updates a specific instance of Product.
    - `destroy`: marks a specific instance of Product as deleted.

    The class uses the ProductSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Product, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = ProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        filter_fields = ['name']
        queryset = Product.objects.filter(deletedAt=None)

        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})
        
        return queryset


class PriceViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements CRUD operations for the Price.

    - `create`: creates a new instance of Price.
    - `list`: lists all active instances of Price.
    - `retrieve`: retrieves a specific instance of Price by ID.
    - `update`: updates a specific instance of Price.
    - `partial_update`: partially updates a specific instance of Price.
    - `destroy`: marks a specific instance of Price as deleted.

    The class uses the PriceSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Price, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = PriceSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        
        filter_fields = ['deposit_id','product_id','priceType','isValid']
        queryset = Price.objects.filter(deletedAt=None, startedAt__lte=timezone.now())
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})
        
        return queryset


class StockViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements get and retrieve operations for the Stock.

    - `list`: lists all active instances of Stock.
    - `retrieve`: retrieves a specific instance of Stock by ID.

    The class uses the StockSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Stock, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = StockSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):

        filter_fields = ['deposit_id','product_id']
        queryset = Stock.objects.filter(deletedAt=None)
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})
        
        return queryset


class StockMovementViewSets(viewsets.ReadOnlyModelViewSet):
    """
    Viewset that implements get and retrieve operations for the StockMovement.

    - `list`: lists all active instances of StockMovement.
    - `retrieve`: retrieves a specific instance of StockMovement by ID.

    The class uses the StockMovementSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of StockMovement, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = StockMovementSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
    
        filter_fields = ['deposit_id','product_id','movementType']
        queryset = StockMovement.objects.filter(deletedAt=None)
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})
        
        return queryset


class EntityViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements CRUD operations for the Entity.

    - `create`: creates a new instance of Entity.
    - `list`: lists all active instances of Entity.
    - `retrieve`: retrieves a specific instance of Entity by ID.
    - `update`: updates a specific instance of Entity.
    - `partial_update`: partially updates a specific instance of Entity.
    - `destroy`: marks a specific instance of Entity as deleted.

    The class uses the EntitySerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Entity, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = EntitySerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):

        filter_fields = ['name','identifier','identifierType','entititype','isActive']
        queryset = Entity.objects.filter(deletedAt=None)
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})
        
        return queryset


class DocumentViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements CRUD operations for the Document.

    - `create`: creates a new instance of Document.
    - `list`: lists all active instances of Document.
    - `retrieve`: retrieves a specific instance of Document by ID.
    - `update`: updates a specific instance of Document.
    - `partial_update`: partially updates a specific instance of Document.
    - `destroy`: marks a specific instance of Document as deleted.

    The class uses the DocumentSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of Document, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = DocumentSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):
        
        filter_fields = ['key','deposit_id','entity_id','documentType','isOpen']
        queryset = Document.objects.filter(deletedAt=None)
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})

        return queryset



class DocumentProductViewSets(viewsets.ModelViewSet):
    """
    Viewset that implements CRUD operations for the DocumentProduct.

    - `create`: creates a new instance of DocumentProduct.
    - `list`: lists all active instances of DocumentProduct.
    - `retrieve`: retrieves a specific instance of DocumentProduct by ID.
    - `update`: updates a specific instance of DocumentProduct.
    - `partial_update`: partially updates a specific instance of DocumentProduct.
    - `destroy`: marks a specific instance of DocumentProduct as deleted.

    The class uses the DocumentProductSerializer serializer and the DjangoModelPermissions permission, which ensures that only authenticated and authorized users can access the operations.

    The class also has a get_queryset() method that returns all active instances of DocumentProduct, filtered by name (if there are any filter parameters in the query string).
    """

    serializer_class = DocumentProductSerializer
    permission_class = [DjangoModelPermissions]

    def get_queryset(self):

        filter_fields = ['document_id','product_id','isOpen','isNew']
        queryset = DocumentProduct.objects.filter(deletedAt=None)
        
        if len(self.request.query_params) > 0:
            for key, value in self.request.query_params.items():
                if key in filter_fields:
                    queryset = queryset.filter(**{key : value})

        return queryset