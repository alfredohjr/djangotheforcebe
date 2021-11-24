from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from shop import views
from shop.api.viewsets import CompanyViewSets, DepositViewSets, DocumentProductViewSets, DocumentViewSets, EntityViewSets, PriceViewSets, ProductViewSets, ShopProductViewSet, StockMovementViewSets, StockViewSets

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
router.register('shop', ShopProductViewSet, basename='shop4ecommerce')

urlpatterns = [
    path('api/',include(router.urls)),
    path('order/<int:document_id>/', views.createOrder, name='order2pdf'),
]