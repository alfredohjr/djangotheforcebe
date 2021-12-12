from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.module_loading import autodiscover_modules
from shop.models.Stock import Stock
from shop.tests.tests_models import AutoCreate as ShopAutoCreate
from rest_framework.test import APIClient

class AutoCreate:

    def __init__(self,name=None) -> None:
        User.objects.create_user(username='test', password='test', is_superuser=True)
        client = APIClient()
        response = client.post('/api/token/', {'username': 'test', 'password': 'test'}, format='json')
        self.token = response.data['access']
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        if name:
            self.name = name

    def get(self,url,id=None):
        if id:
            url = f'{url}{id}/'
        return self.client.get(url)

    def post(self,url,data):
        return self.client.post(url, data=data, format='json')

    def put(self,url,id,data):
        return self.client.put(f'{url}{id}/', data=data, format='json')

    def delete(self,url,id):
        return self.client.delete(f'{url}{id}/')



class TestCase_001_Shop(TestCase):

    def test_001_price1_is_valid(self):
        autoShop = ShopAutoCreate(name='test_000001')
        priceValue = 1522
        autoShop.createPrice(value=priceValue)
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        
        auto = AutoCreate()
        response = auto.get('/shop/api/shop/')
        self.assertEqual(response.status_code, 200)
        for item in response.data:
            if item['id'] == stock.id:
                self.assertEqual(item['price1'], priceValue)
                break

    def test_002_price2_is_valid(self):
        autoShop = ShopAutoCreate(name='test_000001')
        priceValue = 1322.50
        autoShop.createPrice(value=priceValue)
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        
        auto = AutoCreate()
        response = auto.get('/shop/api/shop/')
        self.assertEqual(response.status_code, 200)
        for item in response.data:
            if item['id'] == stock.id:
                self.assertEqual(item['price2'], priceValue)
                break

    def test_003_price1_dont_show_isValid_false(self):
        self.skipTest('empty')

    def test_004_price2_dont_show_isValid_false(self):
        self.skipTest('empty')

    def test_005_dont_show_if_stock_lte_zero(self):
        self.skipTest('empty')
    
    def test_006_dont_show_price1_is_None(self):
        self.skipTest('empty')

    def test_007_dont_update_shop(self):
        self.skipTest('empty')

    def test_008_dont_delete_shop(self):
        self.skipTest('empty')

    def test_009_dont_insert_shop(self):
        self.skipTest('empty')

    def test_010_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_002_Company(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')        

    def test_002_get_company(self):
        shopAuto = ShopAutoCreate(name='test_000002')
        company = shopAuto.createCompany()

        auto = AutoCreate()
        response = auto.get('/shop/api/company/', company.id)
        self.assertEqual(response.status_code, 200)

    def test_004_update_company(self):
        shopAuto = ShopAutoCreate(name='test_000004')
        company = shopAuto.createCompany()

        auto = AutoCreate()
        auto.put('/shop/api/company/', company.id, {'name': 'test_000004_001'})

        response = auto.get('/shop/api/company/',company.id)
        self.assertEqual(response.data['name'], 'test_000004_001')

    def test_005_delete_company(self):
        shopAuto = ShopAutoCreate(name='test_000005')
        company = shopAuto.createCompany()

        auto = AutoCreate()
        response = auto.delete('/shop/api/company/', id=company.id)

        response = auto.get('/shop/api/company/', {'name': 'test_000005'})
        self.assertEqual(response.status_code, 404)
        

    def test_006_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_007_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_008_dont_show_deletedAt(self):
        self.skipTest('empty')
    
    def test_009_create_company(self):
        auto = AutoCreate()
        response = auto.post('/shop/api/company/', {'name': 'test_000009'})
        self.assertEqual(response.status_code, 201)

class TestCase_003_Deposit(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_deposit(self):
        self.skipTest('empty')

    def test_003_post_deposit(self):
        self.skipTest('empty')

    def test_004_update_deposit(self):
        self.skipTest('empty')

    def test_005_delete_deposit(self):
        self.skipTest('empty')

    def test_006_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_007_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_008_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_004_Document(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_document(self):
        self.skipTest('empty')

    def test_003_post_document(self):
        self.skipTest('empty')

    def test_004_update_document(self):
        self.skipTest('empty')

    def test_005_delete_document(self):
        self.skipTest('empty')

    def test_006_close_document(self):
        self.skipTest('empty')

    def test_007_reopen_document(self):
        self.skipTest('empty')

    def test_008_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_009_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_010_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_005_DocumentProduct(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_documentProduct(self):
        self.skipTest('empty')

    def test_003_post_documentProduct(self):
        self.skipTest('empty')

    def test_004_update_documentProduct(self):
        self.skipTest('empty')

    def test_005_delete_documentProduct(self):
        self.skipTest('empty')

    def test_006_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_007_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_008_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_006_Entity(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_entity(self):
        self.skipTest('empty')

    def test_003_post_entity(self):
        self.skipTest('empty')

    def test_004_update_entity(self):
        self.skipTest('empty')

    def test_005_delete_entity(self):
        self.skipTest('empty')

    def test_006_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_007_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_008_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_007_Price(TestCase):

    def test_001_get_price(self):
        self.skipTest('empty')

    def test_002_post_price(self):
        self.skipTest('empty')

    def test_003_update_price(self):
        self.skipTest('empty')

    def test_004_delete_price(self):
        self.skipTest('empty')

    def test_005_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_006_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_007_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_008_Product(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_product(self):
        self.skipTest('empty')

    def test_003_post_product(self):
        self.skipTest('empty')

    def test_004_update_product(self):
        self.skipTest('empty')

    def test_005_delete_product(self):
        self.skipTest('empty')

    def test_006_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_007_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_008_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_009_Stock(TestCase):

    def test_001_get_stock(self):
        self.skipTest('empty')

    def test_002_dont_post_stock(self):
        self.skipTest('empty')

    def test_003_dont_update_stock(self):
        self.skipTest('empty')

    def test_004_dont_delete_stock(self):
        self.skipTest('empty')

    def test_005_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_006_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_007_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_010_StockMovement(TestCase):

    def test_001_get_stockMovement(self):
        self.skipTest('empty')

    def test_002_dont_post_stockMovement(self):
        self.skipTest('empty')

    def test_003_dont_update_stockMovement(self):
        self.skipTest('empty')

    def test_004_dont_delete_stockMovement(self):
        self.skipTest('empty')
    
    def test_005_dont_show_deleted_items(self):
        self.skipTest('empty')
    
    def test_006_dont_alter_deleted_items(self):
        self.skipTest('empty')

    def test_007_dont_show_deletedAt(self):
        self.skipTest('empty')


class TestCase_010_StockMovement(TestCase):

    def test_001_price1(self):
        self.skipTest('empty')

    def test_002_price2(self):
        self.skipTest('empty')