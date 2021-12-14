from enum import auto
from django.core import exceptions
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.module_loading import autodiscover_modules
from rest_framework.test import APIClient
from rest_framework.exceptions import MethodNotAllowed
from shop.models.Deposit import Deposit
from shop.models.Inventory import Inventory

from shop.models.Stock import Stock
from shop.models.Price import Price

from shop.tests.tests_models import AutoCreate as ShopAutoCreate

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
        autoShop = ShopAutoCreate(name='test_000003_001')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.startedAt = timezone.now()
        price.priceType = 'NO'
        price.value = 10
        price.isValid = False
        price.save()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()

        auto = AutoCreate()
        response = auto.get('/shop/api/shop/')
        for data in response.data:
            if data['id'] == stock.id:
                self.assertEqual(data['price1'], None)
                break

    def test_004_price2_dont_show_isValid_false(self):
        autoShop = ShopAutoCreate(name='test_000004')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.startedAt = timezone.now()
        price.finishedAt = timezone.now() + timezone.timedelta(days=1)
        price.priceType = 'OF'
        price.value = 10
        price.isValid = False
        price.save()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()

        auto = AutoCreate()
        response = auto.get('/shop/api/shop/')
        for data in response.data:
            if data['id'] == stock.id:
                self.assertEqual(data['price2'], None)
                break

    def test_005_dont_show_if_stock_lte_zero(self):
        autoShop = ShopAutoCreate(name='test_000005')
        autoShop.fullDocumentOperation()

        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()

        inventory = autoShop.createInventory()
        autoShop.createInventoryProduct(value=0)
        inventory.startedAt = timezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/shop/', id=stock.id)
        self.assertEqual(response.status_code, 404)
    
    def test_006_dont_show_price1_is_None(self):
        autoShop = ShopAutoCreate(name='test_000006')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        self.assertTrue(stock)

        auto = AutoCreate()
        response = auto.get('/shop/api/shop/', id=stock.id)
        self.assertEqual(response.status_code, 404)

    def test_007_dont_update_shop(self):
        autoShop = ShopAutoCreate(name='test_000007')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        self.assertTrue(stock)

        price = autoShop.createPrice()

        auto = AutoCreate()
        try:
            auto.put('/shop/api/shop/', id=stock.id, data={'amount': stock.amount + 1})
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_008_dont_delete_shop(self):
        autoShop = ShopAutoCreate(name='test_000008')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        self.assertTrue(stock)

        price = autoShop.createPrice()

        auto = AutoCreate()
        try:
            auto.delete('/shop/api/shop/', id=stock.id)
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_009_dont_insert_shop(self):
        autoShop = ShopAutoCreate(name='test_000009')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        self.assertTrue(stock)

        price = autoShop.createPrice()

        auto = AutoCreate()
        try:
            auto.post('/shop/api/shop/', data={'amount': stock.amount + 1})
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_010_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000010')
        autoShop.fullDocumentOperation()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        stock = Stock.objects.filter(product=product, deposit=deposit).first()
        self.assertTrue(stock)

        inventory = autoShop.createInventory()
        autoShop.createInventoryProduct(value=0)
        inventory.startedAt = timezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        stock.deletedAt = timezone.now()
        stock.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/shop/', id=stock.id)
        self.assertEqual(response.status_code, 404)


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
        autoShop = ShopAutoCreate(name='test_000006')
        company = autoShop.createCompany()
        company.deletedAt = timezone.now()
        company.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/company/', id=company.id)
        self.assertEqual(response.status_code, 404)
    
    def test_007_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000007')
        company = autoShop.createCompany()
        company.deletedAt = timezone.now()
        company.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/company/', id=company.id, data={'name': 'test_000007_001'})
        self.assertEqual(response.status_code, 404)

    def test_008_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000008')
        company = autoShop.createCompany()

        auto = AutoCreate()
        response = auto.get('/shop/api/company/', id=company.id)
        self.assertFalse('deletedAt' in response.data)
    
    def test_009_create_company(self):
        auto = AutoCreate()
        response = auto.post('/shop/api/company/', {'name': 'test_000009'})
        self.assertEqual(response.status_code, 201)

class TestCase_003_Deposit(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_deposit(self):
        autoShop = ShopAutoCreate(name='test_000001')
        deposit = autoShop.createDeposit()

        auto = AutoCreate()
        response = auto.get('/shop/api/deposit/', deposit.id)
        self.assertEqual(response.status_code, 200)

    def test_003_post_deposit(self):
        autoShop = ShopAutoCreate(name='test_000003')
        company = autoShop.createCompany()
        
        auto = AutoCreate()
        response = auto.post('/shop/api/deposit/', {'company':company.id,'name': 'test_000003_001'})
        self.assertEqual(response.status_code, 201)

    def test_004_update_deposit(self):
        autoShop = ShopAutoCreate(name='test_000004')
        company = autoShop.createCompany()
        deposit = autoShop.createDeposit()

        auto = AutoCreate()
        auto.put('/shop/api/deposit/', deposit.id, {'name': 'test_000004_001', 'company': company.id})

        response = auto.get('/shop/api/deposit/', deposit.id)
        self.assertEqual(response.data['name'], 'test_000004_001')

    def test_005_delete_deposit(self):
        autoShop = ShopAutoCreate(name='test_000005')
        deposit = autoShop.createDeposit()

        auto = AutoCreate()
        response = auto.delete('/shop/api/deposit/', id=deposit.id)
        self.assertEqual(response.status_code, 204)

    def test_006_dont_show_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000006')
        deposit = autoShop.createDeposit()
        deposit.deletedAt = timezone.now()
        deposit.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/deposit/', id=deposit.id)
        self.assertEqual(response.status_code, 404)
    
    def test_007_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000007')
        deposit = autoShop.createDeposit()
        deposit.deletedAt = timezone.now()
        deposit.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/deposit/', id=deposit.id, data={'name': 'test_000007_001'})
        self.assertEqual(response.status_code, 404)

    def test_008_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000008')
        deposit = autoShop.createDeposit()

        auto = AutoCreate()
        response = auto.get('/shop/api/deposit/', id=deposit.id)
        self.assertFalse('deletedAt' in response.data)


class TestCase_004_Document(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_document(self):
        autoShop = ShopAutoCreate(name='test_000001')
        document = autoShop.createDocument()

        auto = AutoCreate()
        response = auto.get('/shop/api/document/', document.id)
        self.assertEqual(response.status_code, 200)

    def test_003_post_document(self):
        autoShop = ShopAutoCreate(name='test_000003')
        deposit = autoShop.createDeposit()
        entity = autoShop.createEntity()
        folder = autoShop.createDocumentFolder()
        paymentMethod = autoShop.createPaymentMethod()
                
        auto = AutoCreate()
        response = auto.post('/shop/api/document/'
                        , {'deposit':deposit.id
                            ,'key': 'test_000003_001'
                            ,'folder': folder.id
                            ,'paymentMethod': paymentMethod.id
                            ,'entity':entity.id
                            ,'name': 'test_000003_001'})
        self.assertEqual(response.status_code, 201)

    def test_004_update_document(self):
        autoShop = ShopAutoCreate(name='test_000004')
        deposit = autoShop.createDeposit()
        entity = autoShop.createEntity()
        folder = autoShop.createDocumentFolder()
        paymentMethod = autoShop.createPaymentMethod()
        document = autoShop.createDocument()

        auto = AutoCreate()
        auto.put('/shop/api/document/', document.id, {'key': 'test_000004_001', 'deposit': deposit.id, 'entity': entity.id, 'folder': folder.id, 'paymentMethod': paymentMethod.id})

        response = auto.get('/shop/api/document/', document.id)
        self.assertEqual(response.data['key'], 'test_000004_001')

    def test_005_delete_document(self):
        autoShop = ShopAutoCreate(name='test_000005')
        document = autoShop.createDocument()

        auto = AutoCreate()
        response = auto.delete('/shop/api/document/', id=document.id)
        self.assertEqual(response.status_code, 204)

    def test_006_close_document(self):
        self.skipTest('empty')

    def test_007_reopen_document(self):
        self.skipTest('empty')

    def test_008_dont_show_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000008')
        document = autoShop.createDocument()
        document.deletedAt = timezone.now()
        document.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/document/', id=document.id)
        self.assertEqual(response.status_code, 404)
    
    def test_009_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000009')
        document = autoShop.createDocument()
        document.deletedAt = timezone.now()
        document.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/document/', id=document.id, data={'key': 'test_000009_001'})
        self.assertEqual(response.status_code, 404)

    def test_010_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000010')
        document = autoShop.createDocument()

        auto = AutoCreate()
        response = auto.get('/shop/api/document/', id=document.id)
        self.assertFalse('deletedAt' in response.data)


class TestCase_005_DocumentProduct(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_documentProduct(self):
        autoShop = ShopAutoCreate(name='test_000001')
        documentProduct = autoShop.createDocumentProduct()

        auto = AutoCreate()
        response = auto.get('/shop/api/documentproduct/', documentProduct.id)
        self.assertEqual(response.status_code, 200)

    def test_003_post_documentProduct(self):
        autoShop = ShopAutoCreate(name='test_000003')
        document = autoShop.createDocument()
        product = autoShop.createProduct()
        auto = AutoCreate()
        response = auto.post('/shop/api/documentproduct/'
                        , {'document':document.id
                            ,'product': product.id
                            ,'amount':1
                            ,'value':10})
        self.assertEqual(response.status_code, 201)

    def test_004_update_documentProduct(self):
        autoShop = ShopAutoCreate(name='test_000004')
        document = autoShop.createDocument()
        product = autoShop.createProduct()
        documentProduct = autoShop.createDocumentProduct()

        auto = AutoCreate()
        auto.put('/shop/api/documentproduct/', documentProduct.id, {'document': document.id, 'product': product.id, 'amount': 20, 'value': 10})

        response = auto.get('/shop/api/documentproduct/', documentProduct.id)
        self.assertEqual(response.data['amount'], 20)

    def test_005_delete_documentProduct(self):
        autoShop = ShopAutoCreate(name='test_000005')
        documentProduct = autoShop.createDocumentProduct()

        auto = AutoCreate()
        response = auto.delete('/shop/api/documentproduct/', id=documentProduct.id)
        self.assertEqual(response.status_code, 204)

    def test_006_dont_show_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000006')
        documentProduct = autoShop.createDocumentProduct()
        documentProduct.deletedAt = timezone.now()
        documentProduct.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/documentproduct/', id=documentProduct.id)
        self.assertEqual(response.status_code, 404)
    
    def test_007_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000007')
        documentProduct = autoShop.createDocumentProduct()
        documentProduct.deletedAt = timezone.now()
        documentProduct.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/documentproduct/', id=documentProduct.id, data={'amount': 20})
        self.assertEqual(response.status_code, 404)

    def test_008_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000008')
        documentProduct = autoShop.createDocumentProduct()

        auto = AutoCreate()
        response = auto.get('/shop/api/documentproduct/', id=documentProduct.id)
        self.assertFalse('deletedAt' in response.data)


class TestCase_006_Entity(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_entity(self):
        autoShop = ShopAutoCreate(name='test_000002')
        entity = autoShop.createEntity()

        auto = AutoCreate()
        response = auto.get('/shop/api/entity/', entity.id)
        self.assertEqual(response.status_code, 200)

    def test_003_post_entity(self):
        autoShop = ShopAutoCreate(name='test_000003')
        auto = AutoCreate()
        response = auto.post('/shop/api/entity/'
                        , {'name': 'test_000003_001'
                        , 'identifier': '78413325000355'
                        , 'identifierType': 'JU'
                        , 'entityType': 'FOR'
                        })
        self.assertEqual(response.status_code, 201)

    def test_004_update_entity(self):
        autoShop = ShopAutoCreate(name='test_000004')
        entity = autoShop.createEntity()

        auto = AutoCreate()
        auto.put('/shop/api/entity/', entity.id, {
                        'name': 'test_000004_001'                        
                        , 'identifier': '78413325000355'
                        , 'identifierType': 'JU'
                        , 'entityType': 'FOR'})

        response = auto.get('/shop/api/entity/', entity.id)
        self.assertEqual(response.data['name'], 'test_000004_001')

    def test_005_delete_entity(self):
        autoShop = ShopAutoCreate(name='test_000005')
        entity = autoShop.createEntity()

        auto = AutoCreate()
        response = auto.delete('/shop/api/entity/', id=entity.id)
        self.assertEqual(response.status_code, 204)

    def test_006_dont_show_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000006')
        entity = autoShop.createEntity()
        entity.deletedAt = timezone.now()
        entity.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/entity/', id=entity.id)
        self.assertEqual(response.status_code, 404)
    
    def test_007_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000007')
        entity = autoShop.createEntity()
        entity.deletedAt = timezone.now()
        entity.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/entity/', id=entity.id, data={'name': 'test_000007_001'})
        self.assertEqual(response.status_code, 404)

    def test_008_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000008')
        entity = autoShop.createEntity()

        auto = AutoCreate()
        response = auto.get('/shop/api/entity/', id=entity.id)
        self.assertFalse('deletedAt' in response.data)


class TestCase_007_Price(TestCase):

    def test_001_get_price(self):
        autoShop = ShopAutoCreate(name='test_000001')
        price = autoShop.createPrice()

        auto = AutoCreate()
        response = auto.get('/shop/api/price/', price.id)
        self.assertEqual(response.status_code, 200)

    def test_002_post_price(self):
        autoShop = ShopAutoCreate(name='test_000002')
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        auto = AutoCreate()
        response = auto.post('/shop/api/price/'
                        , {'value':10
                        ,'product': product.id
                        ,'deposit': deposit.id
                        ,'priceType':'NO'
                        ,'startedAt': timezone.now()
                        })
        self.assertEqual(response.status_code, 201)

    def test_003_update_price(self):
        autoShop = ShopAutoCreate(name='test_000003')
        price = autoShop.createPrice()
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()

        auto = AutoCreate()
        auto.put('/shop/api/price/', price.id, {
                        'value':2000
                        ,'priceType':'NO'
                        ,'startedAt': timezone.now()
                        ,'product': product.id
                        ,'deposit': deposit.id
                        })

        response = auto.get('/shop/api/price/', price.id)
        self.assertEqual(response.data['value'], 2000)

    def test_004_delete_price(self):
        autoShop = ShopAutoCreate(name='test_000004')
        price = autoShop.createPrice()

        auto = AutoCreate()
        response = auto.delete('/shop/api/price/', id=price.id)
        self.assertEqual(response.status_code, 204)

    def test_005_dont_show_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000005')
        price = autoShop.createPrice()
        price.deletedAt = timezone.now()
        price.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/price/', id=price.id)
        self.assertEqual(response.status_code, 404)
    
    def test_006_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000006')
        price = autoShop.createPrice()
        price.deletedAt = timezone.now()
        price.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/price/', id=price.id, data={'value':2000})
        self.assertEqual(response.status_code, 404)

    def test_007_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000007')
        price = autoShop.createPrice()

        auto = AutoCreate()
        response = auto.get('/shop/api/price/', id=price.id)
        self.assertFalse('deletedAt' in response.data)


class TestCase_008_Product(TestCase):

    def test_001_is_valid_image_link(self):
        self.skipTest('empty')

    def test_002_get_product(self):
        autoShop = ShopAutoCreate(name='test_000002')
        product = autoShop.createProduct()

        auto = AutoCreate()
        response = auto.get('/shop/api/product/', product.id)
        self.assertEqual(response.status_code, 200)

    def test_003_post_product(self):

        auto = AutoCreate()
        response = auto.post('/shop/api/product/'
                        , {'name': 'test_000003_001'})
        self.assertEqual(response.status_code, 201)

    def test_004_update_product(self):
        autoShop = ShopAutoCreate(name='test_000004')
        product = autoShop.createProduct()

        auto = AutoCreate()
        response = auto.put('/shop/api/product/', product.id, {
                        'name': 'test_000004_001'})
        self.assertEqual(response.status_code, 200)

    def test_005_delete_product(self):
        autoShop = ShopAutoCreate(name='test_000005')
        product = autoShop.createProduct()

        auto = AutoCreate()
        response = auto.delete('/shop/api/product/', id=product.id)
        self.assertEqual(response.status_code, 204)

    def test_006_dont_show_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000006')
        product = autoShop.createProduct()
        product.deletedAt = timezone.now()
        product.save()

        auto = AutoCreate()
        response = auto.get('/shop/api/product/', id=product.id)
        self.assertEqual(response.status_code, 404)
    
    def test_007_dont_alter_deleted_items(self):
        autoShop = ShopAutoCreate(name='test_000007')
        product = autoShop.createProduct()
        product.deletedAt = timezone.now()
        product.save()

        auto = AutoCreate()
        response = auto.put('/shop/api/product/', id=product.id, data={'name': 'test_000007_001'})
        self.assertEqual(response.status_code, 404)

    def test_008_dont_show_deletedAt(self):
        autoShop = ShopAutoCreate(name='test_000008')
        product = autoShop.createProduct()

        auto = AutoCreate()
        response = auto.get('/shop/api/product/', id=product.id)
        self.assertFalse('deletedAt' in response.data)


class TestCase_009_Stock(TestCase):

    def test_001_get_stock(self):
        autoShop = ShopAutoCreate(name='test_000001')
        deposit = autoShop.createDeposit()
        product = autoShop.createProduct()
        autoShop.fullDocumentOperation()

        stock = Stock.objects.get(deposit=deposit, product=product)

        auto = AutoCreate()
        response = auto.get('/shop/api/stock/', stock.id)
        self.assertEqual(response.status_code, 200)

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
