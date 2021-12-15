from django.conf.urls import url
from django.urls import path
from django.urls.conf import include
from rest_framework import routers

from shop import views
from shop.api.viewsets import (
    CompanyViewSets
    , DepositViewSets
    , DocumentProductViewSets
    , DocumentViewSets
    , EntityViewSets
    , PriceViewSets
    , ProductViewSets
    , ShopProductViewSet
    , StockMovementViewSets
    , StockViewSets
    , CompanyImageViewSet
    , DepositImageViewSet
    , EntityImageViewSet
    , ProductImageViewSet)

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
    path('api/company/logo/<int:pk>/', CompanyImageViewSet.as_view(), name='shopcompanylogo'),
    path('api/deposit/logo/<int:pk>/', DepositImageViewSet.as_view(), name='shopdepositlogo'),
    path('api/entity/logo/<int:pk>/', EntityImageViewSet.as_view(), name='shopentitylogo'),
    path('api/product/logo/<int:pk>/', ProductImageViewSet.as_view(), name='shopproductlogo'),

    path('api/',include(router.urls)),
    path('order/<int:document_id>/', views.createOrder, name='order2pdf'),
    path('sale/document/<int:document_id>/', views.createSaleDocument, name='doc2pdf'),
    path('report/product/', views.reportProduct, name='repProduct'),
    path('report/price/', views.reportPrice, name='repPrice'),


]