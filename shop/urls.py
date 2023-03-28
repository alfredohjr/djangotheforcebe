from django.urls import path
from django.urls.conf import include
from rest_framework import routers
from rest_framework.schemas import get_schema_view

from shop.api.viewsets import CompanyViewSets, DepositViewSets, DocumentProductViewSets, DocumentViewSets, EntityViewSets, PriceViewSets, ProductViewSets, StockMovementViewSets, StockViewSets

router = routers.DefaultRouter()
router.register('company', CompanyViewSets, basename='shopcompany')
router.register('deposit', DepositViewSets, basename='shopdeposit')
router.register('product', ProductViewSets, basename='shopproduct')
router.register('price', PriceViewSets, basename='shopprice')
router.register('stock', StockViewSets, basename='shopstock')
router.register('stockmovement', StockMovementViewSets, basename='shopstockmovement')
router.register('entity', EntityViewSets, basename='shopentity')
router.register('document', DocumentViewSets, basename='shopdocument')
router.register('documentproduct', DocumentProductViewSets, basename='shopdocumentproduct')

urlpatterns = [
    path('api/',include(router.urls)),
]