# Create your tests here.

import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone as djangoTimezone

from backoffice.models.PayReceive import PayReceive
from backoffice.models.PaymentMethod import PaymentMethod
from shop.core.validators.cnpj import ValidateCNPJ
from shop.core.validators.cpf import ValidateCPF
from shop.models.Company import Company
from shop.models.CompanyLog import CompanyLog
from shop.models.Deposit import Deposit
from shop.models.DepositLog import DepositLog
from shop.models.DocumentFolder import DocumentFolder
from shop.models.DocumentFolderLog import DocumentFolderLog
from shop.models.Document import Document
from shop.models.DocumentLog import DocumentLog, pre_save_documentLog
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Entity import Entity
from shop.models.EntityLog import EntityLog
from shop.models.Inventory import Inventory
from shop.models.InventoryLog import InventoryLog
from shop.models.InventoryProduct import InventoryProduct
from shop.models.Price import Price
from shop.models.Product import Product
from shop.models.ProductLog import ProductLog
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement

from backoffice.tests.tests_models import AutoCreate as BackOfficeAutoCreate

class AutoCreate:

    def __init__(self,name):
        self.name = name
    
    def createCompany(self,name=None):
        if name is None:
            name = self.name
        
        company = Company.objects.filter(name=name)
        if company:
            return company[0]
        else:
            company = Company.objects.create(name=name)
            return company

    def createAndDeleteCompany(self,name=None):
        if name is None:
            name = self.name
        company = self.createCompany(name)
        
        company = Company.objects.get(id=company.id)
        company.delete()
        return company        

    def createDeposit(self,name=None):
        if name is None:
            name = self.name
        company = self.createCompany(name)

        deposit = Deposit.objects.filter(name=name)
        if deposit:
            return deposit[0]
        else:
            deposit = Deposit.objects.create(name=name,company=company)
            return deposit
        
    def createEntity(self,name=None,entityType='FOR',identifierType='JU',identifier='15.982.546/0001-62'):
        if name is None:
            name = self.name

        if entityType == 'CLI':
            identifierType = 'FI'
            identifier = '446.846.440-22'

        entity = Entity.objects.filter(name=name)
        if entity:
            return entity[0]
        else:
            entity = Entity.objects.create(name=name
                ,identifier=identifier
                ,identifierType=identifierType
                ,entityType=entityType)
            return entity

    def createProduct(self,name=None):
        if name is None:
            name = self.name
        product = Product.objects.filter(name=name)
        if product:
            return product[0]
        else:
            product = Product.objects.create(name=name)
            return product

    def createDocumentFolder(self,name=None,documentType='IN',financial=False, stock=True):
        if name is None:
            name = self.name
        
        folder = DocumentFolder.objects.filter(name=name)
        if folder:
            return folder[0]
        
        folder = DocumentFolder()
        folder.name = name
        folder.documentType = documentType
        folder.stock = stock
        folder.product = True
        folder.financial = financial
        folder.updateCost = False if documentType == 'OUT' else True
        folder.createPrice = False if documentType == 'OUT' else True
        folder.save()

        return folder

    def createPaymentMethod(self,name=None,isPortion=True,portionAmount=7,dueDate=6,portionRegex='15/30/45/60'):
        if name is None:
            name = self.name

        boAuto = BackOfficeAutoCreate(name=name)
        return boAuto.createPaymentMethod(isPortion=isPortion
                                    ,portionAmount=portionAmount
                                    ,dueDate=dueDate
                                    ,portionRegex=portionRegex)


    def createDocument(self,name=None,documentType='IN',key=None):
        if name is None:
            name = self.name
        deposit = self.createDeposit(name)
        entityType = 'FOR' if documentType == 'IN' else 'CLI'
        entity = self.createEntity(name if key == None else key, entityType=entityType)
        folder = self.createDocumentFolder(name=name if key == None else key,documentType=documentType)
        paymentMethod = self.createPaymentMethod(name=name)

        document = Document.objects.filter(key=name if key == None else key)
        if document:
            return document[0]
        else:
            
            document = Document.objects.create(key=name if key == None else key
                            ,deposit=deposit
                            ,entity=entity
                            ,paymentMethod=paymentMethod
                            ,folder=folder)
            return document
    
    def createDocumentProduct(self,name=None,documentType='IN',amount=1,key=None):
        if name is None:
            name = self.name

        document = self.createDocument(name,documentType=documentType,key=key)
        product = self.createProduct(name)
        
        documentProduct = DocumentProduct.objects.filter(
            document=document
            ,product=product
        )

        if documentProduct:
            return documentProduct[0]

        documentProduct = DocumentProduct.objects.create(document=document
                                                        ,product=product
                                                        ,amount=amount
                                                        ,value=1)
        return documentProduct
    
    def fullDocumentOperation(self,name=None,documentType='IN',amount=1, key=None):
        if name is None:
            name = self.name
        document = self.createDocument(documentType=documentType, key=key)
        documentProduct = self.createDocumentProduct(name,documentType=documentType,amount=amount,key=key)
        document = Document.objects.get(id=documentProduct.document.id)
        document.isOpen = False
        document.save()
        return document

    def createPrice(self, name=None, value=1, priceType='NO', startedAt=None, finishedAt=None):
        if name is None:
            name = self.name

        deposit = self.createDeposit()
        product = self.createProduct()

        price = Price.objects.filter(
            deposit=deposit
            , product=product
            , priceType=priceType
            , startedAt=startedAt
            , finishedAt=finishedAt)

        if price:
            return price[0]
        else:
            price = Price()
            price.deposit = deposit
            price.product = product
            price.value = value
            price.priceType = priceType
            price.startedAt = djangoTimezone.now() if startedAt == None else startedAt
            price.finishedAt = finishedAt
            price.save()
            return price
    
    def createInventory(self,name=None):
        if name is None:
            name = self.name
        
        self.createDocumentFolder(name='INVENTARIO ENTRADA',documentType='IN')
        self.createDocumentFolder(name='INVENTARIO SAIDA',documentType='OUT')
        self.createEntity(name=f'{name}INVIN',entityType='FOR')
        self.createEntity(name=f'{name}INVOUT',entityType='CLI')
        deposit = self.createDeposit(name)

        inventory = Inventory.objects.filter(name=name)
        if inventory:
            return inventory[0]
        
        inventory = Inventory()
        inventory.name = name 
        inventory.deposit = deposit
        inventory.save()

        return inventory
    
    def createInventoryProduct(self,name=None):
        if name == None:
            name = self.name
        
        inventory = self.createInventory(name=name)
        product = self.createProduct(name=name)

        inventoryProduct = InventoryProduct()
        inventoryProduct.inventory = inventory
        inventoryProduct.product = product
        inventoryProduct.value = 1
        inventoryProduct.isOpen = True
        inventoryProduct.save()

        return inventoryProduct



class TestCase_001_ModelCompany(TestCase):

    def test_001_create_company(self):
        auto = AutoCreate('test_000001')
        company = auto.createCompany()
        self.assertEqual(company.name,'test_000001')
        
    def test_002_update_company(self):
        auto = AutoCreate('test_000002')
        company = auto.createCompany()

        company = Company.objects.get(name='test_000002')
        company.name = 'company'
        self.assertRaises(ValidationError,company.save)

        company = Company.objects.get(name='test_000002')
        company.name = 'test_000002_001'
        company.save()

        company = Company.objects.get(name='test_000002_001')
        self.assertEqual(company.name,'test_000002_001')
        self.assertLess(company.createdAt,company.updatedAt)
        self.assertIsNot(company.createdAt,company.updatedAt)

    def test_003_delete_company_with_product_stock(self):
        auto = AutoCreate('test_000003')
        document = auto.fullDocumentOperation()

        company = Company.objects.get(name='test_000003')
        self.assertRaises(ValidationError,company.delete)

        company = Company.objects.get(name='test_000003')
        company.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,company.save)

    def test_999_delete_company(self):

        auto = AutoCreate('test_company')
        company = auto.createCompany()

        company = Company.objects.get(id=company.id)
        self.assertIsNone(company.deletedAt)
        company.delete()
        
        company = Company.objects.get(name='test_company')
        self.assertIsNotNone(company.deletedAt)

    def test_004_delete_company_with_product_inventory(self):
        auto = AutoCreate('test_000004')
        company = auto.createCompany()
        inventoryProduct = auto.createInventoryProduct()
        
        self.assertRaises(ValidationError,company.delete)
    
    def test_006_delete_company_with_document_open(self):
        auto = AutoCreate(name='test_000006')
        document = auto.createDocument()

        company = Company.objects.get(name='test_000006')
        company.delete()

        company = Company.objects.get(name='test_000006')
        self.assertIsNone(company.deletedAt)
       
    def test_008_delete_company_with_deposit_is_finance_open(self):
        auto = AutoCreate('test_000008')
        company = auto.createCompany()
        auto.createPaymentMethod(portionAmount=0)
        document = auto.createDocumentFolder(financial=True,stock=False)
        auto.fullDocumentOperation()

        self.assertRaises(ValidationError, company.delete)

    
    def test_009_delete_company_with_deposit_inventory_is_open(self):
        auto = AutoCreate('test_000009')
        company = auto.createCompany()
        auto.createDeposit()
        inventory = auto.createInventory()

        self.assertRaises(ValidationError,company.close)

    def test_010_company_register_in_log_table(self):
        auto = AutoCreate('test_000010')
        company = auto.createCompany()

        log = CompanyLog.objects.filter(company=company)
        self.assertTrue(log)

    def test_011_companyLog_write_correct(self):
        auto = AutoCreate('test_000011')
        company = auto.createCompany()

        company = Company.objects.get(id=company.id)
        company.name = 'test_000011_001'
        company.save()

        company = Company.objects.get(id=company.id)
        company.close()

        log = CompanyLog.objects.filter(company=company)
        self.assertEqual(log[0].table,'COMPANY')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'COMPANY')
        self.assertEqual(log[1].transaction,'UPD')

        self.assertEqual(log[2].table,'COMPANY')
        self.assertEqual(log[2].transaction,'DEL')

    def test_012_company_size_minimun_of_name_is_10(self):
        self.assertRaises(ValidationError,Company.objects.create,name='test_012')
        
        auto = AutoCreate('test_000012')
        company = auto.createCompany()
        self.assertEqual(company.name,'test_000012')

    def test_013_update_fields_with_after_deleted(self):
        auto = AutoCreate(name='test_000013')
        companyAux = auto.createAndDeleteCompany()

        company = Company.objects.get(name='test_000013')
        company.name = 'test_013_update'
        self.assertRaises(Exception,company,createdAt = djangoTimezone.now())
        company.updatedAt = djangoTimezone.now()
        company.deletedAt = djangoTimezone.now()
        self.assertRaises(Exception,company.save)

        company = Company.objects.get(id=company.id)

        self.assertEqual(companyAux.name,company.name)
        self.assertEqual(companyAux.createdAt,company.createdAt)
        self.assertEqual(companyAux.updatedAt,company.updatedAt)
        self.assertEqual(companyAux.deletedAt,company.deletedAt)

    def test_014_return_deleted_company(self):
        auto = AutoCreate(name='test_000014')
        companyAux = auto.createAndDeleteCompany()

        company = Company.objects.get(id=companyAux.id)
        company.name = 'test_000014_001'
        self.assertRaises(ValidationError,company.save)

        company = Company.objects.get(id=companyAux.id)
        company.deletedAt = None
        company.save()

        company = Company.objects.get(id=companyAux.id)
        self.assertIsNone(company.deletedAt)

    def test_015_create_with_deletedAt_not_none(self):
        company = Company(name = 'test_000015', deletedAt = djangoTimezone.now())
        company.save()

        company = Company.objects.get(name='test_000015')
        self.assertIsNone(company.deletedAt)

        Company.objects.create(name = 'test_000015_001', deletedAt = djangoTimezone.now())
        company = Company.objects.get(name='test_000015_001')
        self.assertIsNone(company.deletedAt)

    def test_016_function_close(self):
        auto = AutoCreate('test_000016')
        company = auto.createCompany()

        company.close()
        company = Company.objects.get(id=company.id)
        self.assertIsNotNone(company.deletedAt)
    
    def test_017_function_open(self):
        auto = AutoCreate('test_000017')
        company = auto.createCompany()
        company.close()

        company = Company.objects.get(id=company.id)
        self.assertIsNotNone(company.deletedAt)
        
        company.open()
        company = Company.objects.get(id=company.id)
        self.assertIsNone(company.deletedAt)


class TestCase_002_ModelDeposit(TestCase):

    def test_001_create_deposit(self):
        auto = AutoCreate('test_000001')
        auto.createDeposit()

        deposit = Deposit.objects.get(name='test_000001')
        self.assertEqual(deposit.name,'test_000001')

    def test_002_update_deposit(self):
        auto = AutoCreate('test_000002')
        auto.createDeposit()

        deposit = Deposit.objects.get(name='test_000002')
        deposit.name = 'test_000002_001'
        deposit.save()

        deposit = Deposit.objects.get(name='test_000002_001')
        self.assertEqual(deposit.name,'test_000002_001')

    def test_003_delete_deposit_with_product_stock(self):
        auto = AutoCreate('test_000003')
        auto.fullDocumentOperation()

        deposit = Deposit.objects.get(name='test_000003')
        self.assertRaises(ValidationError,deposit.delete)

        deposit = Deposit.objects.get(name='test_000003')
        deposit.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,deposit.save)

    def test_999_delete_deposit(self):
        auto = AutoCreate('test_000999')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(name='test_000999')
        deposit.delete()

        deposit = Deposit.objects.get(name='test_000999')
        self.assertIsNotNone(deposit.deletedAt)

    def test_004_delete_deposit_with_product_inventory(self):
        auto = AutoCreate('test_000004')
        deposit = auto.createDeposit()
        auto.createInventoryProduct()

        self.assertRaises(ValidationError,deposit.delete)

    
    def test_005_delete_deposit_with_document_open(self):
        auto = AutoCreate('test_000005')
        auto.createDocumentProduct()

        deposit = Deposit.objects.get(name='test_000005')
        self.assertIsNone(deposit.deletedAt)

    def test_006_delete_deposit_with_is_finance_open(self):
        auto = AutoCreate('test_000006')
        auto.createDocumentFolder(stock=False, financial=True)
        auto.fullDocumentOperation()

        deposit = Deposit.objects.get(name='test_000006')
        self.assertRaises(ValidationError,deposit.delete)

    
    def test_007_delete_deposit_with_inventory_is_open(self):
        auto = AutoCreate('test_000004')
        deposit = auto.createDeposit()
        inventory = auto.createInventory()

        self.assertRaises(ValidationError,deposit.close)

    def test_008_deposit_register_in_log_table(self):
        auto = AutoCreate('test_000009')
        deposit = auto.createDeposit()

        log = DepositLog.objects.filter(deposit=deposit)
        self.assertTrue(log)

    def test_009_depositLog_write_correct(self):
        auto = AutoCreate('test_000009')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.name = 'test_000009_001'
        deposit.save()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.close()

        log = DepositLog.objects.filter(deposit=deposit)
        self.assertEqual(log[0].table,'DEPOSIT')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'DEPOSIT')
        self.assertEqual(log[1].transaction,'UPD')

        self.assertEqual(log[2].table,'DEPOSIT')
        self.assertEqual(log[2].transaction,'DEL')

    def test_010_deposit_size_minimun_of_name_is_10(self):
        auto = AutoCreate('test_010')
        self.assertRaises(ValidationError, auto.createDeposit)

    def test_011_create_deposit_with_deleted_company(self):
        auto = AutoCreate('test_000011')
        company = auto.createCompany()

        company = Company.objects.get(id=company.id)
        company.delete()

        deposit = Deposit()
        deposit.company = company
        deposit.name = 'test_000011'
        self.assertRaises(ValidationError,deposit.save)

    def test_012_update_fields_with_after_deleted(self):
        auto = AutoCreate('test_000012')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.delete()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.name='test_000012_001'
        self.assertRaises(ValidationError,deposit.save)
    
    def test_013_create_with_deletedAt_not_none(self):
        auto = AutoCreate('test_000013')
        company = auto.createCompany()

        deposit = Deposit()
        deposit.name = 'test_000013'
        deposit.company = company
        deposit.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError, deposit.save)

    def test_014_return_deleted_deposit(self):
        auto = AutoCreate('test_000014')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.delete()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.deletedAt = None
        deposit.save()

        deposit = Deposit.objects.get(id=deposit.id)
        self.assertIsNone(deposit.deletedAt)

        auto = AutoCreate('test_000014_001')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.deletedAt = djangoTimezone.now()
        deposit.save()

        Deposit.objects.filter(id=deposit.id).update(deletedAt=None)

        deposit = Deposit.objects.get(id=deposit.id)
        self.assertIsNone(deposit.deletedAt)

    def test_016_function_close(self):
        auto = AutoCreate('test_000016')
        deposit = auto.createDeposit()

        deposit.close()
        deposit = Deposit.objects.get(id=deposit.id)
        self.assertIsNotNone(deposit.deletedAt)
    
    def test_017_function_open(self):
        auto = AutoCreate('test_000017')
        deposit = auto.createDeposit()
        deposit.close()

        deposit = Deposit.objects.get(id=deposit.id)
        self.assertIsNotNone(deposit.deletedAt)
        
        deposit.open()
        deposit = Deposit.objects.get(id=deposit.id)
        self.assertIsNone(deposit.deletedAt)


class TestCase_003_ModelEntity(TestCase):

    def test_001_create_entity(self):
        auto = AutoCreate('test_000001')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        self.assertEqual(entity.name,'test_000001')

    def test_002_update_entity(self):
        auto = AutoCreate('test_000002')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        entity.name = 'test_000002_001'
        entity.save()

        entity = Entity.objects.get(id=entity.id)
        self.assertEqual(entity.name,'test_000002_001')

    def test_999_delete_entity(self):
        auto = AutoCreate('test_000999')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        entity.delete()

        entity = Entity.objects.get(id=entity.id)
        self.assertIsNotNone(entity.deletedAt)

    def test_003_delete_entity_with_document_open(self):
        auto = AutoCreate('test_000003')
        document = auto.createDocument()

        entity = Entity.objects.get(id=document.entity.id)
        self.assertRaises(ValidationError,entity.delete)

    def test_004_delete_entity_with_is_finance_open(self):
        auto = AutoCreate('test_000004')
        entity = auto.createEntity()
        folder = auto.createDocumentFolder(stock=False, financial=True)
        auto.fullDocumentOperation()

        entity = Entity.objects.get(id=entity.id)
        self.assertRaises(ValidationError,entity.delete)
    
    def test_005_entity_register_in_log_table(self):
        auto = AutoCreate('test_000005')
        entity = auto.createEntity()

        log = EntityLog.objects.filter(entity=entity)
        self.assertTrue(log)

    def test_006_entityLog_write_correct(self):
        auto = AutoCreate('test_000006')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        entity.name = 'test_000006_001'
        entity.save()

        entity = Entity.objects.get(id=entity.id)
        entity.close()

        log = EntityLog.objects.filter(entity=entity)
        self.assertEqual(log[0].table,'ENTITY')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'ENTITY')
        self.assertEqual(log[1].transaction,'UPD')

        self.assertEqual(log[2].table,'ENTITY')
        self.assertEqual(log[2].transaction,'DEL')

    def test_007_entity_size_minimun_of_name_is_10(self):
        entity = Entity()
        entity.name = 'test_007'
        self.assertRaises(ValidationError,entity.save)

    def test_008_if_entity_is_JU_validate_CNPJ(self):
        auto = AutoCreate('test_000008')
        company = auto.createCompany()

        entity = Entity()
        entity.name = 'test_000008'
        entity.company = company
        entity.identifierType = 'JU'
        self.assertRaises(ValidationError, entity.save)

        entity = Entity()
        entity.name = 'test_000008'
        entity.company = company
        entity.identifierType = 'JU'
        entity.identifier = '1111'
        self.assertRaises(ValidationError, entity.save)

        entity = Entity()
        entity.name = 'test_000008'
        entity.company = company
        entity.identifierType = 'JU'
        entity.identifier = '72.964.696/0001-87'
        self.assertTrue(entity.save)

    def test_009_if_entity_is_FI_validate_CPF(self):
        auto = AutoCreate('test_000009')
        company = auto.createCompany()

        entity = Entity()
        entity.name = 'test_000009'
        entity.company = company
        entity.identifierType = 'FI'
        self.assertRaises(ValidationError, entity.save)

        entity = Entity()
        entity.name = 'test_000009'
        entity.company = company
        entity.identifierType = 'FI'
        entity.identifier = '1111'
        self.assertRaises(ValidationError, entity.save)

        entity = Entity()
        entity.name = 'test_000009'
        entity.company = company
        entity.identifierType = 'FI'
        entity.identifier = '703.165.570-64'
        self.assertTrue(entity.save)

    def test_010_update_fields_with_after_deleted(self):
        auto = AutoCreate('test_000010')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        entity.delete()

        entity = Entity.objects.get(id=entity.id)
        entity.name = 'test_000010_001'
        self.assertRaises(ValidationError,entity.save)

    def test_011_create_with_deletedAt_not_none(self):
        entity = Entity()
        entity.name = 'test_000011'
        entity.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,entity.save)

    def test_012_return_deleted_entity(self):
        auto = AutoCreate('test_000012')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        entity.delete()

        entity = Entity.objects.get(id=entity.id)
        self.assertIsNotNone(entity.deletedAt)
        entity.deletedAt = None
        entity.save()

        entity = Entity.objects.get(id=entity.id)
        self.assertIsNone(entity.deletedAt)

    def test_013_is_valid_entity_type_in_JU_or_FI(self):
        auto = AutoCreate('test_000013')
        company = auto.createCompany()

        entity = Entity()
        entity.name = 'test_000013'
        entity.company=company
        entity.identifierType = 'AA'
        entity.identifier = '703.165.570-64'

        self.assertRaises(ValidationError,entity.save)

    def test_016_function_close(self):
        auto = AutoCreate('test_000016')
        entity = auto.createEntity()

        entity.close()
        entity = Entity.objects.get(id=entity.id)
        self.assertIsNotNone(entity.deletedAt)
    
    def test_017_function_open(self):
        auto = AutoCreate('test_000017')
        entity = auto.createEntity()
        entity.close()

        entity = Entity.objects.get(id=entity.id)
        self.assertIsNotNone(entity.deletedAt)
        
        entity.open()
        entity = Entity.objects.get(id=entity.id)
        self.assertIsNone(entity.deletedAt)


class TestCase_004_ModelProduct(TestCase):

    def test_001_create_product(self):
        auto = AutoCreate('test_000001')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        self.assertEqual(product.name,'test_000001')

    def test_002_update_product(self):
        auto = AutoCreate('test_000002')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.name = 'test_000002_001'
        product.save()

        product = Product.objects.get(id=product.id)
        self.assertEqual(product.name,'test_000002_001')

    def test_999_delete_product(self):
        auto = AutoCreate('test_000999')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.delete()

        product = Product.objects.get(id=product.id)
        self.assertIsNotNone(product.deletedAt)

    def test_003_delete_with_stock(self):
        auto = AutoCreate('test_000003')
        document = auto.fullDocumentOperation()

        product = Product.objects.get(name='test_000003')
        self.assertRaises(ValidationError,product.delete)

    def test_004_delete_with_document_open(self):
        auto = AutoCreate('test_000004')
        document = auto.createDocumentProduct()

        product = Product.objects.get(name='test_000004')
        self.assertRaises(ValidationError,product.delete)

    def test_005_delete_with_inventory_is_open(self):
        auto = AutoCreate('test_000005')
        product = auto.createProduct()
        auto.createInventoryProduct()

        self.assertRaises(ValidationError,product.delete)

    def test_006_productLog_write_correct(self):
        auto = AutoCreate('test_000010')
        product = auto.createProduct()

        log = ProductLog.objects.filter(product=product)
        self.assertTrue(log)

    def test_007_product_size_minimun_of_name_is_10(self):
        auto = AutoCreate('test_006')
        self.assertRaises(ValidationError,auto.createProduct)
    
    def test_008_product_margin_negative(self):
        product = Product()
        product.name = 'test_000008'
        product.margin = -1
        self.assertRaises(ValidationError,product.save)

    def test_009_update_fields_after_deleted(self):
        auto = AutoCreate('test_000009')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.delete()

        product = Product.objects.get(id=product.id)
        product.name = 'test_000009_001'
        self.assertRaises(ValidationError,product.save)

    def test_010_product_register_in_log_table(self):
        auto = AutoCreate('test_000010')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.name = 'test_000010_001'
        product.save()

        product = Product.objects.get(id=product.id)
        product.close()

        log = ProductLog.objects.filter(product=product)
        self.assertEqual(log[0].table,'PRODUCT')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'PRODUCT')
        self.assertEqual(log[1].transaction,'UPD')

        self.assertEqual(log[2].table,'PRODUCT')
        self.assertEqual(log[2].transaction,'DEL')

    def test_011_create_with_deletedAt_not_none(self):
        product = Product()
        product.name = 'test_000011'
        product.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,product.save)

    def test_012_return_deleted_product(self):
        auto = AutoCreate('test_000012')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.delete()

        product = Product.objects.get(id=product.id)
        self.assertIsNotNone(product.deletedAt)

        product.deletedAt = None
        product.save()

        product = Product.objects.get(id=product.id)
        self.assertIsNone(product.deletedAt)

    def test_016_function_close(self):
        auto = AutoCreate('test_000016')
        product = auto.createProduct()

        product.close()
        product = Product.objects.get(id=product.id)
        self.assertIsNotNone(product.deletedAt)
    
    def test_017_function_open(self):
        auto = AutoCreate('test_000017')
        product = auto.createProduct()
        product.close()

        product = Product.objects.get(id=product.id)
        self.assertIsNotNone(product.deletedAt)
        
        product.open()
        product = Product.objects.get(id=product.id)
        self.assertIsNone(product.deletedAt)


class TestCase_005_ModelDocument(TestCase):

    def test_001_create_document(self):
        auto = AutoCreate('test_000001')
        document = auto.createDocument()

        document = Document.objects.get(id=document.id)
        self.assertEqual(document.key,'test_000001')

    def test_002_update_document(self):
        auto = AutoCreate('test_000002')
        document = auto.createDocument()

        document = Document.objects.get(id=document.id)
        document.key = 'test_000002_001'
        document.save()

        document = Document.objects.get(id=document.id)
        self.assertEqual(document.key,'test_000002_001')

    def test_999_delete_document(self):
        auto = AutoCreate('test_000999')
        document = auto.createDocument()

        document = Document.objects.get(id=document.id)
        document.delete()

        document = Document.objects.get(id=document.id)
        self.assertIsNotNone(document.deletedAt)

    def test_003_delete_with_document_close(self):
        auto = AutoCreate('test_000003')
        document = auto.fullDocumentOperation()

        document = Document.objects.get(id=document.id)
        document.delete()

        document = Document.objects.get(id=document.id)
        self.assertIsNone(document.deletedAt)

    def test_004_documentLog_write_correct(self):
        auto = AutoCreate('test_000004')
        document = auto.createDocument()

        document = Document.objects.get(id=document.id)
        document.key = 'test_000004_001'
        document.save()

        document = Document.objects.get(id=document.id)
        document.delete()

        log = DocumentLog.objects.filter(document=document)
        self.assertEqual(log[0].table,'DOCUMENT')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'DOCUMENT')
        self.assertEqual(log[1].transaction,'UPD')

        self.assertEqual(log[2].table,'DOCUMENT')
        self.assertEqual(log[2].transaction,'DEL')

    def test_005_create_document_with_company_is_close(self):
        auto = AutoCreate('test_000005')
        company = auto.createCompany()

        company = Company.objects.get(id=company.id)
        company.delete()

        self.assertRaises(ValidationError,auto.createDocument)

    def test_006_create_document_with_deposit_is_close(self):
        auto = AutoCreate('test_000006')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.delete()

        self.assertRaises(ValidationError,auto.createDocument)

    def test_007_create_document_with_entity_is_close(self):
        auto = AutoCreate('test_000007')
        entity = auto.createEntity()

        entity = Entity.objects.get(id=entity.id)
        entity.delete()

        self.assertRaises(ValidationError,auto.createDocument)

    def test_008_close_document_without_product(self):
        auto = AutoCreate('test_000008')
        document = auto.createDocument()

        document = Document.objects.get(id=document.id)
        document.isOpen = False
        self.assertRaises(ValidationError,document.save)

    def test_009_create_document_with_isOpen_false(self):
        auto = AutoCreate('test_000009')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        folder = auto.createDocumentFolder()

        document = Document()
        document.key = 'test_000009'
        document.deposit = deposit
        document.entity = entity
        document.isOpen = False
        document.folder = folder
        self.assertRaises(ValidationError,document.save)

    def test_010_create_document_if_entity_is_CLI_documentType_is_IN(self):
        auto = AutoCreate('test_000010')
        deposit = auto.createDeposit()
        entity = auto.createEntity(entityType='CLI',identifierType='FI',identifier='462.924.380-15')
        folder = auto.createDocumentFolder()
        
        document = Document()
        document.key = 'test_000010'
        document.deposit = deposit
        document.entity = entity
        document.folder = folder
        self.assertRaises(ValidationError,document.save)

    def test_011_create_document_if_entity_is_FOR_documentType_is_OUT(self):
        auto = AutoCreate('test_000011')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        folder = auto.createDocumentFolder(documentType='OUT')
        
        document = Document()
        document.key = 'test_000011'
        document.deposit = deposit
        document.entity = entity
        document.folder = folder
        self.assertRaises(ValidationError,document.save)

    def test_012_check_product_of_documents_isOpen_is_equals(self):
        auto = AutoCreate('test_000012')
        documentProduct = auto.createDocumentProduct()

        self.assertTrue(documentProduct.isOpen)

        document = Document.objects.get(id=documentProduct.document.id)
        document.isOpen = False
        document.save()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertFalse(documentProduct.isOpen)

        document = Document.objects.get(id=documentProduct.document.id)
        document.reOpenDocument(reason='test_000012_000000000000000')
        document.save()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertTrue(documentProduct.isOpen)

    def test_013_close_document_stock_is_correct(self):

        for i in range(0,10):
            auto = AutoCreate('test_' + str(i).zfill(8))
            document = auto.fullDocumentOperation()

            documentProduct = DocumentProduct.objects.filter(document__id=document.id)
            
            for docprod in documentProduct:
                stock = Stock.objects.get(
                            product__id=docprod.product.id
                            , deposit__id=document.deposit.id)
                self.assertEqual(stock.amount,1)

    def test_014_Reopen_document_stock_is_correct(self):
        auto = AutoCreate('test_000014')
        document = auto.fullDocumentOperation()

        documentProduct = DocumentProduct.objects.filter(document__id=document.id)
            
        for docprod in documentProduct:
            stock = Stock.objects.get(
                        product__id=docprod.product.id
                        ,deposit__id=document.deposit.id)
            self.assertEqual(stock.amount,1)
        
        document = Document.objects.get(id=document.id)
        document.reOpenDocument(reason='test_000014_000000000000')
        document.save()

        for docprod in documentProduct:
            stock = Stock.objects.get(
                        product__id=docprod.product.id
                        ,deposit__id=document.deposit.id)
            self.assertEqual(stock.amount,0)

    def test_015_Reopen_document_reason_as_20_or_more_chars(self):
        auto = AutoCreate('test_000015')
        document = auto.fullDocumentOperation()

        document = Document.objects.get(id=document.id)
        self.assertRaises(ValidationError,document.reOpenDocument,reason='test_000015')

    def test_016_update_fields_after_deleted(self):
        auto = AutoCreate('test_000016')
        document = auto.createDocument()

        document = Document.objects.get(id=document.id)
        document.delete()

        document = Document.objects.get(id=document.id)
        document.key = 'test_000016_001'
        self.assertRaises(ValidationError,document.save)

    def test_017_document_register_in_log_table(self):
        auto = AutoCreate('test_000004')
        document = auto.createDocument()

        log = DocumentLog.objects.filter(document=document)
        self.assertTrue(log)

    def test_018_create_with_deletedAt_not_none(self):
        auto = AutoCreate('test_000018')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        folder = auto.createDocumentFolder()

        document = Document()
        document.key = 'test_000018'
        document.deposit = deposit
        document.entity = entity
        document.folder = folder
        document.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,document.save)

    def test_019_return_deleted_document(self):
        auto = AutoCreate('test_000019')
        document = auto.createDocumentProduct()

        document = Document.objects.get(id=document.id)
        document.delete()

        document = Document.objects.get(id=document.id)
        self.assertIsNotNone(document.deletedAt)

        document = Document.objects.get(id=document.id)
        document.deletedAt = None
        document.save()

        document = Document.objects.get(id=document.id)
        self.assertIsNone(document.deletedAt)
    
    def test_020_update_documentProducts_if_document_is_close(self):
        auto = AutoCreate('test_000020')
        document = auto.fullDocumentOperation()

        documentProduct = DocumentProduct.objects.filter(document__id=document.id)
        documentProduct = DocumentProduct.objects.get(id=documentProduct[0].id)
        documentProduct.amount = 10
        self.assertRaises(ValidationError,documentProduct.save)
        
    def test_021_update_document_if_isOpen_False(self):
        auto = AutoCreate('test_000021')

        document = auto.fullDocumentOperation()
        
        document = Document.objects.get(id=document.id)
        document.key = 'test_000021_001'
        self.assertRaises(ValidationError,document.save)

        document = Document.objects.get(id=document.id)
        document.deposit = auto.createDeposit(name='test_000021_001')
        self.assertRaises(ValidationError,document.save)

        document = Document.objects.get(id=document.id)
        document.entity = auto.createEntity(name='test_000021_001')
        self.assertRaises(ValidationError,document.save)

        document = Document.objects.get(id=document.id)
        document.folder = auto.createDocumentFolder(name='test_000021_001')
        self.assertRaises(ValidationError,document.save)

        document = Document.objects.get(id=document.id)
        document.paymentMethod = auto.createPaymentMethod(name='test_000021_001')
        self.assertRaises(ValidationError,document.save)

        document = Document.objects.get(id=document.id)
        document.deliveryValue = 1800
        self.assertRaises(ValidationError,document.save)

    def test_022_dont_change_isOpen_if_inventory_open(self):
        auto = AutoCreate('test_000022')
        documentProduct = auto.createDocumentProduct()

        inventoryProduct = auto.createInventoryProduct()
        inventoryProduct.startedAt = djangoTimezone.now()
        self.assertRaises(ValidationError, inventoryProduct.save)

        document = auto.fullDocumentOperation()
        auto.createInventoryProduct()

        document = Document.objects.get(id=document.id)
        document.isOpen=True
        self.assertRaises(ValidationError,document.save)
        

class TestCase_006_ModelDocumentProduct(TestCase):

    def test_001_create_documentProduct(self):
        auto = AutoCreate('test_000001')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertEqual(documentProduct.product.name,'test_000001')

    def test_002_update_documentProduct(self):
        auto = AutoCreate('test_000002')
        documentProduct = auto.createDocumentProduct()
        
        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertEqual(documentProduct.amount,1)
        documentProduct.amount = 10
        documentProduct.save()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertEqual(documentProduct.amount,10)

    def test_999_delete_documentProduct(self):
        auto = AutoCreate('test_000999')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNone(documentProduct.deletedAt)

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.delete()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNotNone(documentProduct.deletedAt)

    def test_003_delete_with_document_close(self):
        auto = AutoCreate('test_000003')
        documentProduct = auto.fullDocumentOperation()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertRaises(ValidationError,documentProduct.delete)

    def test_004_documentLog_write_correct(self):
        auto = AutoCreate('test_000004')
        auto.createDocumentProduct()
        document = auto.createDocument()
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.value = 30
        documentProduct.save()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.close()

        log = DocumentLog.objects.filter(document=document)
        self.assertEqual(log[0].table,'DOCUMENT')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'DOCUMENTPRODUCT')
        self.assertEqual(log[1].transaction,'CRE')

        self.assertEqual(log[2].table,'DOCUMENTPRODUCT')
        self.assertEqual(log[2].transaction,'UPD')

        self.assertEqual(log[3].table,'DOCUMENTPRODUCT')
        self.assertEqual(log[3].transaction,'DEL')

    def test_005_value_is_negative(self):
        auto = AutoCreate('test_000005')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.value = -1
        self.assertRaises(ValidationError,documentProduct.save)

    def test_006_amount_is_negative(self):
        auto = AutoCreate('test_000005')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.amount = -1
        self.assertRaises(ValidationError,documentProduct.save)

    def test_007_create_documentProduct_with_delete_is_not_none(self):
        auto = AutoCreate('test_000007')
        product = auto.createProduct()
        document = auto.createDocument()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.amount = 10
        documentProduct.value = 10
        documentProduct.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,documentProduct.save)

    def test_008_create_documentProduct_with_isOpen_false(self):
        auto = AutoCreate('test_000008')
        product = auto.createProduct()
        document = auto.createDocument()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.amount = 10
        documentProduct.value = 10
        documentProduct.isOpen = False
        self.assertRaises(ValidationError,documentProduct.save)

    def test_009_create_documentProduct_with_document_isOpen_false(self):
        auto = AutoCreate('test_000009')
        product = auto.createProduct()
        document = auto.createDocument()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.amount = 10
        documentProduct.value = 10
        documentProduct.save()

        document = Document.objects.get(id=document.id)
        document.isOpen = False
        document.save()

        product2 = Product.objects.create(name='test_000009_001')
        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product2
        documentProduct.amount = 10
        documentProduct.value = 10

        self.assertRaises(ValidationError,documentProduct.save)       

    def test_010_close_documentProduct_IN_stock_is_correct(self):
        auto = AutoCreate('test_000010')
        document = auto.fullDocumentOperation()
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stock = Stock.objects.filter(product=product, deposit=deposit)
        self.assertEqual(stock[0].amount,1)

    def test_011_close_documentProduct_IN_stock_movement_is_correct(self):
        auto = AutoCreate('test_000011')
        document = auto.fullDocumentOperation()
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stockMovement = StockMovement.objects.filter(product=product, deposit=deposit)
        self.assertEqual(document.folder.documentType,'IN')
        self.assertEqual(stockMovement[0].amount,1)
        self.assertEqual(stockMovement[0].movementType,'IN')

    def test_012_close_documentProduct_OUT_stock_is_correct(self):
        auto = AutoCreate('test_000012')
        document = auto.fullDocumentOperation(documentType='OUT')
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stock = Stock.objects.filter(product=product, deposit=deposit)
        self.assertEqual(stock[0].amount,-1)

    def test_013_close_documentProduct_OUT_stock_movement_is_correct(self):
        auto = AutoCreate('test_000013')
        document = auto.fullDocumentOperation(documentType='OUT')
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stockMovement = StockMovement.objects.filter(product=product, deposit=deposit)
        self.assertEqual(len(stockMovement),1)
        self.assertEqual(document.folder.documentType,'OUT')
        self.assertEqual(stockMovement[0].amount,1)
        self.assertEqual(stockMovement[0].movementType,'OUT')

    def test_014_close_documentProduct_price_is_suggested_correct(self):
        auto = AutoCreate('test_000014')
        document = auto.fullDocumentOperation()
        documentProduct = auto.createDocumentProduct()
        product = auto.createProduct()
        deposit = auto.createDeposit()

        price = Price.objects.filter(deposit=deposit,product=product)
        self.assertIsNotNone(price)
        self.assertEqual(price[0].deposit,deposit)
        self.assertEqual(price[0].product,product)
        self.assertEqual(price[0].value,documentProduct.value)
        self.assertEqual(price[0].priceType,'NO')
        self.assertIsNotNone(price[0].startedAt)
        self.assertIsNone(price[0].finishedAt)
        self.assertEqual(price[0].isValid,False)
        self.assertIsNone(price[0].deletedAt)

    def test_015_update_fields_with_after_deleted(self):
        auto = AutoCreate('test_000015')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.delete()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.amount = 10
        self.assertRaises(ValidationError,documentProduct.save)

    def test_016_documentProduct_register_in_log_table(self):
        auto = AutoCreate('test_000016')
        auto.createDocumentProduct()
        document = auto.createDocument()
        documentProduct = auto.createDocumentProduct()

        log = DocumentLog.objects.filter(document=document)
        self.assertEqual(len(log),2)

    def test_017_value_is_zero(self):
        auto = AutoCreate('test_000005')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.value = 0
        self.assertRaises(ValidationError,documentProduct.save)

    def test_018_amount_is_zero(self):
        auto = AutoCreate('test_000005')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.amount = -1
        self.assertRaises(ValidationError,documentProduct.save)

    def test_019_return_deleted_documentProduct(self):
        auto = AutoCreate('test_000018')
        documentProduct = auto.createDocumentProduct()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.delete()
        
        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNotNone(documentProduct.deletedAt)

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        documentProduct.deletedAt = None
        documentProduct.save()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNone(documentProduct.deletedAt)

    def test_016_function_close(self):
        auto = AutoCreate('test_000016')
        documentProduct = auto.createDocumentProduct()

        documentProduct.close()
        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNotNone(documentProduct.deletedAt)
    
    def test_017_function_open(self):
        auto = AutoCreate('test_000017')
        documentProduct = auto.createDocumentProduct()
        documentProduct.close()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNotNone(documentProduct.deletedAt)
        
        documentProduct.open()
        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertIsNone(documentProduct.deletedAt)

    def test_018_dont_change_isOpen_if_inventory_open(self):
        """
        create fullDocument
        create inventory
        create inventoryProduct
        update inventory isOpen to True
        call document.reOpenDocument with reason test_0000000000000000000 and check if assertRaises
        """
        auto = AutoCreate('test_000018')
        document = auto.fullDocumentOperation()
        inventory = auto.createInventory()
        auto.createInventoryProduct()
        inventory.isOpen = True
        inventory.save()

        self.assertRaises(ValidationError,document.reOpenDocument,reason='test_0000000000000000000')


class TestCase_007_ModelPrice(TestCase):
    
    def test_001_create_price(self):
        auto = AutoCreate('test_000001')
        price = auto.createPrice()

        price = Price.objects.get(id=price.id)
        self.assertIsNotNone(price)

    def test_002_update_price(self):
        auto = AutoCreate('test_000002')
        price = auto.createPrice()

        price = Price.objects.get(id=price.id)
        price.value = 100
        price.save()

        price = Price.objects.get(id=price.id)
        self.assertEqual(price.value,100)

    def test_999_delete_price(self):
        auto = AutoCreate('test_000999')
        price = auto.createPrice()

        price = Price.objects.get(id=price.id)
        price.delete()

        price = Price.objects.get(id=price.id)
        self.assertIsNotNone(price.deletedAt)

    def test_003_create_price_with_closed_company(self):
        auto = AutoCreate('test_000003')
        company = auto.createCompany()
        deposit = auto.createDeposit()
        product = auto.createProduct()

        company = Company.objects.get(id=company.id)
        company.delete()

        self.assertRaises(ValidationError, auto.createPrice)

    def test_004_create_price_with_closed_deposit(self):
        auto = AutoCreate('test_000004')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.delete()

        self.assertRaises(ValidationError, auto.createPrice)

    def test_005_create_price_with_negative_values(self):
        auto = AutoCreate('test_000005')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = -1
        self.assertRaises(ValidationError,price.save)

    def test_006_if_priceType_is_NO_finishedAt_is_none(self):
        auto = AutoCreate('test_000006')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = 1
        price.priceType = 'NO'
        price.finishedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,price.save)

    def test_007_if_priceType_is_OF_startedAt_and_finishedAt_is_not_none(self):
        auto = AutoCreate('test_000007')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = 1
        price.priceType = 'OF'
        price.startedAt = None
        self.assertRaises(ValidationError,price.save)

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = 1
        price.priceType = 'OF'
        price.startedAt = djangoTimezone.now()
        price.finishedAt = None
        self.assertRaises(ValidationError,price.save)        

    def test_009_create_if_startedAt_yesterday(self):
        auto = AutoCreate('test_000009')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = 1
        price.priceType = 'OF'
        price.startedAt = djangoTimezone.now() - datetime.timedelta(days=1)
        price.finishedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,price.save)
    
    def test_010_create_if_finishedAt_yesterday(self):
        auto = AutoCreate('test_000010')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = 1
        price.priceType = 'OF'
        price.startedAt = djangoTimezone.now()
        price.finishedAt = djangoTimezone.now() - datetime.timedelta(days=1)
        self.assertRaises(ValidationError,price.save)

    def test_011_update_fields_with_after_deleted(self):
        auto = AutoCreate('test_000011')
        price = auto.createPrice()

        price = Price.objects.get(id=price.id)
        price.delete()

        price = Price.objects.get(id=price.id)
        price.value = 100
        self.assertRaises(ValidationError, price.save)

    def test_012_price_register_in_log_table(self):
        auto = AutoCreate('test_000012')
        price = auto.createPrice()
        product = auto.createProduct()

        price = Price.objects.get(id=price.id)
        price.value = 30
        price.save()

        price = Price.objects.get(id=price.id)
        price.close()

        log = ProductLog.objects.filter(product=product)
        self.assertEqual(log[0].table,'PRODUCT')
        self.assertEqual(log[0].transaction,'CRE')

        self.assertEqual(log[1].table,'PRICE')
        self.assertEqual(log[1].transaction,'CRE')

        self.assertEqual(log[2].table,'PRICE')
        self.assertEqual(log[2].transaction,'UPD')

        self.assertEqual(log[3].table,'PRICE')
        self.assertEqual(log[3].transaction,'DEL')
    
    def test_014_create_with_deletedAt_not_none(self):
        auto = AutoCreate('test_000014')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.priceType = 'NO'
        price.value = 100
        price.startedAt = djangoTimezone.now()
        price.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError, price.save)
    
    def test_015_create_price_with_product_deleted(self):
        auto = AutoCreate('test_000015')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.delete()

        self.assertRaises(ValidationError, auto.createPrice)

    def test_016_return_deleted_price(self):
        auto = AutoCreate('test_000016')
        price = auto.createPrice()

        price = Price.objects.get(id=price.id)
        price.delete()

        price = Price.objects.get(id=price.id)
        self.assertIsNotNone(price.deletedAt)

        price = Price.objects.get(id=price.id)
        price.deletedAt = None
        price.save()

        price = Price.objects.get(id=price.id)
        self.assertIsNone(price.deletedAt)

    def test_016_function_close(self):
        auto = AutoCreate('test_000016')
        price = auto.createPrice()

        price.close()
        price = Price.objects.get(id=price.id)
        self.assertIsNotNone(price.deletedAt)
    
    def test_017_function_open(self):
        auto = AutoCreate('test_000017')
        price = auto.createPrice()
        price.close()

        price = Price.objects.get(id=price.id)
        self.assertIsNotNone(price.deletedAt)
        
        price.open()
        price = Price.objects.get(id=price.id)
        self.assertIsNone(price.deletedAt)

    def test_018_dont_alter_if_isActive_true(self):
        """
        if price is active, dont alter the value
        """

        auto = AutoCreate('test_000018')
        price = auto.createPrice()
        price.isValid = True
        price.value = 100
        price.save()

        price = Price.objects.get(id=price.id)
        price.value = 200
        self.assertRaises(ValidationError, price.save)

class TestCase_008_ModelStock(TestCase):

    def test_001_create_stock_only_document(self):
        auto = AutoCreate('test_000001')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        stock = Stock()
        stock.deposit = deposit
        stock.product = product
        stock.amount = 1
        stock.value = 1
        self.assertRaises(ValidationError,stock.save)

    def test_002_update_stock_only_document(self):
        auto = AutoCreate('test_000002')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        auto.fullDocumentOperation()

        stock = Stock.objects.get(product=product, deposit=deposit)
        stock.amount = 10
        self.assertRaises(ValidationError,stock.save)

    def test_999_delete_stock_with_amount_gt_zero(self):
        auto = AutoCreate('test_000999')
        document = auto.fullDocumentOperation()
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stock = Stock.objects.get(product=product, deposit=deposit)
        self.assertRaises(ValidationError,stock.delete)

        stock = Stock.objects.get(product=product, deposit=deposit)
        stock.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,stock.save)

    def test_003_update_value_only_document_IN(self):
        auto = AutoCreate('test_000003')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        auto.fullDocumentOperation(documentType='OUT')

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.value,0)

    def test_005_inventory_IN(self):
        """
        create fullDocument
        create inventory
        create inventoryProduct with 100 in amount
        isOpen is False in inventory
        check if stock amount is 100 if not, raise ValidationError
        """
        auto = AutoCreate('test_000005')
        auto.fullDocumentOperation()
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,1)

        inventory = auto.createInventory()

        inventoryProduct = InventoryProduct()
        inventoryProduct.inventory = inventory
        inventoryProduct.product = product
        inventoryProduct.value = 100
        inventoryProduct.save()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.isOpen = False
        inventory.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,100)

    def test_006_inventory_OUT(self):
        """
        create fullDocument with amount 100
        create inventory
        create inventoryProduct with 10 in value
        isOpen is False in inventory
        check if stock amount is 10 if not, raise ValidationError
        """
        auto = AutoCreate('test_000006')
        auto.fullDocumentOperation(amount=100)
        product = auto.createProduct()
        deposit = auto.createDeposit()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,100)

        inventory = auto.createInventory()

        inventoryProduct = InventoryProduct()
        inventoryProduct.inventory = inventory
        inventoryProduct.product = product
        inventoryProduct.value = 10
        inventoryProduct.save()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.isOpen = False
        inventory.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,10)
        
    def test_007_create_stock_with_company_close(self):
        auto = AutoCreate('test_000007')
        document = auto.createDocumentProduct()

        document = Document.objects.get(id=document.id)
        document.isOpen = False
        document.save()

        company = auto.createCompany()

        company = Company.objects.get(id=company.id)
        self.assertRaises(ValidationError,company.delete)

    def test_008_create_stock_with_deposit_close(self):
        auto = AutoCreate('test_000008')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.deletedAt = djangoTimezone.now()
        deposit.save()

        self.assertRaises(ValidationError,auto.fullDocumentOperation)

    def test_009_create_stock_with_product_close(self):
        auto = AutoCreate('test_000009')
        product = auto.createProduct()

        product = Product.objects.get(id=product.id)
        product.deletedAt = djangoTimezone.now()
        product.save()

        self.assertRaises(ValidationError, auto.fullDocumentOperation)

    def test_010_create_with_value_negative(self):
        auto = AutoCreate('test_000010')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        stock = Stock()
        stock.deposit = deposit
        stock.product = product
        stock.amount = 0
        stock.value = -1
        self.assertRaises(ValidationError, stock.save)

    def test_011_update_with_value_negative(self):
        auto = AutoCreate('test_000011')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        document = auto.fullDocumentOperation()

        stock = Stock.objects.get(deposit__id=deposit.id, product__id=product.id)
        stock.value = -1
        self.assertRaises(ValidationError, stock.save)

    def test_012_update_fields_with_after_deleted(self):
        auto = AutoCreate('test_000012')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        folder = auto.createDocumentFolder(name='test_000012_001',documentType='OUT')
        entity = auto.createEntity(name='test_000012_001',entityType='CLI')
        document = auto.fullDocumentOperation()

        payment = auto.createPaymentMethod()

        document = Document()
        document.deposit = deposit
        document.entity = entity
        document.folder = folder
        document.paymentMethod = payment
        document.save()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.value = 1
        documentProduct.amount = 1
        documentProduct.save()

        document = Document.objects.get(id=document.id)
        document.isOpen = False
        document.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        stock.delete()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertIsNotNone(stock.deletedAt)

    def test_014_create_with_deletedAt_not_none(self):
        auto = AutoCreate('test_000014')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        
        stock = Stock()
        stock.deposit = deposit
        stock.product = product
        stock.value = 1
        stock.amount = 0
        stock.deletedAt = djangoTimezone.now()
        self.assertRaises(ValidationError,stock.save)

    def test_015_return_deleted_stock(self):
        auto = AutoCreate('test_000015')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        folder = auto.createDocumentFolder(name='test_000015_001',documentType='OUT')
        entity = auto.createEntity(name='test_000015_001', entityType='CLI')
        auto.fullDocumentOperation()

        payment = auto.createPaymentMethod()

        document = Document()
        document.deposit = deposit
        document.entity = entity
        document.folder = folder
        document.paymentMethod = payment
        document.save()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.value = 1
        documentProduct.amount = 1
        documentProduct.save()

        document = Document.objects.get(id=document.id)
        document.isOpen = False
        document.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        stock.delete()

        stock = Stock.objects.get(deposit=deposit, product=product)
        stock.deletedAt = None
        stock.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertIsNone(stock.deletedAt)


class TestCase_009_ModelStockMovement(TestCase):
    
    def test_001_dont_update_register(self):
        auto = AutoCreate('test_000001')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        auto.fullDocumentOperation()

        stockMovement = StockMovement.objects.get(deposit=deposit,product=product)
        stockMovement.amount = 100
        self.assertRaises(ValidationError, stockMovement.save)

    def test_002_create_or_update_stockMovement_only_stock(self):
        auto = AutoCreate('test_000002')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        stockMovement = StockMovement()
        stockMovement.deposit = deposit
        stockMovement.product = product
        stockMovement.value = 1
        stockMovement.amount = 1
        self.assertRaises(ValidationError,stockMovement.save)

        auto.fullDocumentOperation()
        stockMovement = StockMovement.objects.get(deposit=deposit, product=product)
        stockMovement.amount = 100
        self.assertRaises(ValidationError,stockMovement.save)


class TestCase_016_ModelInventory(TestCase):

    def test_001_create(self):
        auto = AutoCreate('test_000001')
        inventory = auto.createInventory()

        inventory = Inventory.objects.get(id=inventory.id)
        self.assertTrue(inventory)

    def test_002_update(self):
        auto = AutoCreate('test_000001')
        inventory = auto.createInventory()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.name = 'test_000001_001'
        inventory.save()

        inventory = Inventory.objects.get(id=inventory.id)
        self.assertEqual(inventory.name,'test_000001_001')

    def test_999_delete(self):
        auto = AutoCreate('test_000999')
        inventory = auto.createInventory()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.delete()

        inventory = Inventory.objects.get(id=inventory.id)
        self.assertIsNotNone(inventory.deletedAt)

    def test_003_dont_create_with_company_close(self):
        auto = AutoCreate('test_000003')
        company = auto.createCompany()
        
        company = Company.objects.get(id=company.id)
        company.close()

        self.assertRaises(ValidationError,auto.createInventory)

    def test_004_dont_create_with_deposit_close(self):
        auto = AutoCreate('test_000004')
        deposit = auto.createDeposit()

        deposit = Deposit.objects.get(id=deposit.id)
        deposit.close()

        self.assertRaises(ValidationError,auto.createInventory)

    def test_006_dont_start_with_document_open(self):
        auto = AutoCreate('test_000006')
        documentProduct = auto.createDocumentProduct()

        inventoryProduct = auto.createInventoryProduct()
        inventory = auto.createInventory()
        inventory.startedAt = djangoTimezone.now()
        self.assertRaises(ValidationError, inventory.save)

    def test_007_dont_alter_deposit_after_started(self):
        auto = AutoCreate('test_000007')
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        deposit2 = auto.createDeposit('test_000007_002')
        inventory = Inventory.objects.get(id=inventory.id)
        inventory.deposit = deposit2
        self.assertRaises(ValidationError, inventory.save)

    def test_008_write_log(self):
        auto = AutoCreate('test_000008')

        inventory = auto.createInventory()
        log = InventoryLog.objects.filter(inventory__id=inventory.id)
        self.assertEqual(log[0].transaction,'cre')

        inventory = Inventory.objects.get(id=inventory.id)
        inventory.name = 'test_000008_001'
        inventory.save()

        log = InventoryLog.objects.filter(inventory__id=inventory.id)
        self.assertEqual(log[1].transaction,'upd')
        
        inventory = Inventory.objects.get(id=inventory.id)
        inventory.delete()

        log = InventoryLog.objects.filter(inventory__id=inventory.id)
        self.assertEqual(log[2].transaction,'del')

    def test_010_dont_delete_after_inventory_isOpen_false(self):
        auto = AutoCreate('test_000010')
        inventoryProduct = auto.createInventoryProduct()

        inventory = Inventory.objects.get(id=inventoryProduct.inventory.id)
        inventory.startedAt = djangoTimezone.now()        
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        inventory = Inventory.objects.get(id=inventory.id)        
        self.assertRaises(ValidationError,inventory.delete)

    def test_011_change_isOpen_to_false_stock_is_correct(self):
        auto = AutoCreate('test_000011')
        auto.createInventoryProduct()
        inventory = auto.createInventory()

        inventory.startedAt = djangoTimezone.now()        
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        product = auto.createProduct()
        deposit = auto.createDeposit()

        stock = Stock.objects.filter(deposit=deposit, product=product)
        self.assertEqual(stock[0].amount,1)

    def test_012_change_isOpen_to_false_document_is_correct(self):
        auto = AutoCreate('test_000012')
        auto.fullDocumentOperation(amount=100)
        deposit = auto.createDeposit()
        product = auto.createProduct()
        
        inventory = auto.createInventory()
        auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()
        
        inventory.isOpen = False
        inventory.save()

        document = Document.objects.filter(key__contains='[INV]')
        self.assertFalse(document[0].isOpen)

    def test_013_dont_reopen_inventory(self):
        auto = AutoCreate('test_000013')
        auto.createInventoryProduct()
        inventory = auto.createInventory()

        inventory.startedAt = djangoTimezone.now()        
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        inventory = Inventory.objects.get(id=inventory.id)
        self.assertFalse(inventory.isOpen)

        inventory.isOpen = True
        self.assertRaises(ValidationError,inventory.save)

    def test_014_started_register_valueBefore_inventoryProduct(self):
        auto = AutoCreate('test_000014')
        auto.fullDocumentOperation(amount=120)

        inventoryProduct = auto.createInventoryProduct()
        self.assertEqual(inventoryProduct.valueBefore,0)
        inventory = auto.createInventory()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventoryProduct = InventoryProduct.objects.get(id=inventoryProduct.id)
        self.assertEqual(inventoryProduct.valueBefore,120)

    def test_015_started_register_startedAt_in_inventoryProduct(self):
        auto = AutoCreate('test_000015')
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()

        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventoryProduct = InventoryProduct.objects.get(id=inventoryProduct.id)
        self.assertIsNotNone(inventoryProduct.startedAt)

    def test_016_dont_close_inventory_if_not_started(self):
        auto = AutoCreate('test_000015')
        inventory = auto.createInventory()
        auto.createInventoryProduct()

        inventory.isOpen = False
        self.assertRaises(ValidationError, inventory.save)
    
    def test_017_dont_create_and_start_same_time(self):
        """
        create inventory and start it at the same time
        """
        
        auto = AutoCreate('test_000017')
        inventory = Inventory()
        inventory.name = 'test_000017'
        inventory.deposit = auto.createDeposit()
        inventory.isOpen = True
        inventory.startedAt = djangoTimezone.now()
        self.assertRaises(ValidationError, inventory.save)
        

class TestCase_017_ModelInventoryProduct(TestCase):

    def test_001_create(self):
        auto = AutoCreate('test_000001')
        inventoryProduct = auto.createInventoryProduct()

        self.assertTrue(inventoryProduct)

    def test_999_delete(self):
        auto = AutoCreate('test_000999')
        inventoryProduct = auto.createInventoryProduct()

        inventoryProduct.delete()
        inventoryProduct = InventoryProduct.objects.get(id=inventoryProduct.id)
        self.assertIsNotNone(inventoryProduct.deletedAt)

    def test_003_dont_create_with_company_close(self):
        auto = AutoCreate('test_000003')
        company = auto.createCompany()
        company.delete()
        
        self.assertRaises(ValidationError,auto.createInventoryProduct)

    def test_004_dont_create_with_deposit_close(self):
        auto = AutoCreate('test_000004')
        deposit = auto.createDeposit()
        deposit.delete()
        
        self.assertRaises(ValidationError,auto.createInventoryProduct)

    def test_008_write_log(self):
        auto = AutoCreate('test_000008')
        inventoryProduct = auto.createInventoryProduct()

        inventoryProduct.value = 10
        inventoryProduct.save()

        inventoryProduct.delete()
        
        log = InventoryLog.objects.filter(inventory=inventoryProduct.inventory,table='INVENTORYPRODUCT')
        self.assertEqual(log[0].transaction,'cre')
        self.assertEqual(log[1].transaction,'upd')
        self.assertEqual(log[2].transaction,'del')

    def test_010_dont_delete_after_inventory_isOpen_false(self):
        auto = AutoCreate('test_000010')
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()

        inventory.startedAt = djangoTimezone.now()        
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        self.assertRaises(ValidationError, inventoryProduct.delete)

    def test_011_change_isOpen_false_stock_is_correct(self):
        auto = AutoCreate('test_000011')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        auto.fullDocumentOperation(amount=15)
        auto.fullDocumentOperation(documentType='OUT',amount=100, key='test_000011_002')

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,-85)

        inventory = auto.createInventory()
        auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,1)

        auto = AutoCreate('test_000011_003')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        auto.fullDocumentOperation(documentType='IN',amount=100)
        
        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,100)
        
        inventory = auto.createInventory()
        auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        stock = Stock.objects.get(deposit=deposit, product=product)
        self.assertEqual(stock.amount,1)

    def test_012_change_isOpen_false_documentProduct_is_correct(self):
        auto = AutoCreate('test_000012')
        deposit = auto.createDeposit()
        product = auto.createProduct()
       
        inventory = auto.createInventory()
        auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        document = Document.objects.filter(deposit=deposit)
        documentProduct = DocumentProduct.objects.filter(document__in=document, product=product)
        self.assertEqual(document[0].folder.name,'INVENTARIO ENTRADA')
        self.assertEqual(documentProduct[0].amount,1)

    def test_013_change_isOpen_false_document_is_correct(self):
        auto = AutoCreate('test_000013')
        deposit = auto.createDeposit()
        product = auto.createProduct()
        auto.fullDocumentOperation(amount=1000)
       
        inventory = auto.createInventory()
        auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        document = Document.objects.filter(deposit=deposit)
        self.assertEqual(document[1].folder.name,'INVENTARIO SAIDA')
        self.assertFalse(document[1].isOpen)

    def test_014_dont_reopen_inventoryProduct(self):
        auto = AutoCreate('test_000014')
        deposit = auto.createDeposit()
        product = auto.createProduct()
       
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventory.isOpen = False
        inventory.save()

        inventoryProduct = InventoryProduct.objects.get(id=inventoryProduct.id)
        inventoryProduct.isOpen = True
        self.assertRaises(ValidationError,inventoryProduct.save)

    def test_015_dont_alter_valueBefore_after_inventory_started(self):
        auto = AutoCreate('test_000014')
        deposit = auto.createDeposit()
        product = auto.createProduct()
       
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventoryProduct.valueBefore = 10000
        self.assertRaises(ValidationError, inventoryProduct.save)

    def test_017_dont_alter_isOpen_different_inventory(self):
        """
        create inventory
        create inventoryProduct
        isOpen is True in inventory
        change inventoryProduct isOpen to False, and test raise
        """
        auto = AutoCreate('test_000017')
        deposit = auto.createDeposit()
        product = auto.createProduct()
       
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()
        inventory.isOpen = True
        inventory.save()

        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventoryProduct.isOpen = False
        self.assertRaises(ValidationError, inventoryProduct.save)
        
    def test_018_dont_update_after_startedAt(self):
        """
        create inventory
        create inventory product
        start inventory
        update inventory product startedAt and test raise
        """
        auto = AutoCreate('test_000018')
        deposit = auto.createDeposit()
        product = auto.createProduct()
       
        inventory = auto.createInventory()
        inventoryProduct = auto.createInventoryProduct()
        inventory.startedAt = djangoTimezone.now()
        inventory.save()

        inventoryProduct.startedAt = djangoTimezone.now()
        self.assertRaises(ValidationError, inventoryProduct.save)


class TestCase_018_ModelDocumentFolder(TestCase):

    def test_001_create(self):
        auto = AutoCreate('test_000018')
        documentFolder = auto.createDocumentFolder()

        documentFolder = DocumentFolder.objects.get(id=documentFolder.id)
        self.assertTrue(documentFolder)

    def test_002_dont_update_flags(self):
        auto = AutoCreate('test_000002')
        folder = auto.createDocumentFolder()
        
        folder.stock = True
        folder.save()

        auto.fullDocumentOperation()

        folder.stock = False
        self.assertRaises(ValidationError, folder.save)

    def test_999_delete(self):
        auto = AutoCreate('test_000999')
        folder = auto.createDocumentFolder()

        folder.delete()
        folder  = DocumentFolder.objects.get(id=folder.id)
        self.assertIsNotNone(folder.deletedAt)
    
    def test_003_dont_delete_document_open(self):
        auto = AutoCreate('test_000004')
        folder = auto.createDocumentFolder()
        document = auto.createDocumentProduct()

        self.assertRaises(ValidationError, folder.delete)

    def test_004_if_stock_is_true_product_is_true(self):
        folder = DocumentFolder()
        folder.name = 'test_000005'
        folder.stock = True
        folder.product = False
        self.assertRaises(ValidationError, folder.save)

    def test_005_product_is_true_accept_documentProduct(self):
        auto = AutoCreate('test_000005')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        product = auto.createProduct()

        folder = DocumentFolder()
        folder.name = 'test_000005'
        folder.product = True
        folder.documentType = 'IN'
        folder.save()

        payment = auto.createPaymentMethod()

        document = Document()
        document.key = 'test_000005'
        document.folder = folder
        document.deposit = deposit
        document.entity = entity
        document.paymentMethod = payment
        document.save()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.value = 1
        documentProduct.amount = 1
        documentProduct.save()

        documentProduct = DocumentProduct.objects.get(id=documentProduct.id)
        self.assertTrue(documentProduct)

    def test_006_product_is_false_dont_accept_documentProduct(self):
        auto = AutoCreate('test_000006')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        product = auto.createProduct()

        folder = DocumentFolder()
        folder.name = 'test_000006'
        folder.product = False
        folder.documentType = 'IN'
        folder.save()

        payment = auto.createPaymentMethod()

        document = Document()
        document.key = 'test_000006'
        document.folder = folder
        document.deposit = deposit
        document.entity = entity
        document.paymentMethod = payment
        document.save()

        documentProduct = DocumentProduct()
        documentProduct.document = document
        documentProduct.product = product
        documentProduct.value = 1
        documentProduct.amount = 1
        self.assertRaises(ValidationError, documentProduct.save)

        document.close()

    def test_007_financial_send(self):
        """
        create documentfolder with financial is True
        create fulldocument
        test if document exists in PayReceive table
        """
        auto = AutoCreate('test_000007')
        auto.createDeposit()
        auto.createEntity()
        auto.createProduct()

        auto.createDocumentFolder(financial=True, stock=True)
        auto.createPaymentMethod()

        document = auto.fullDocumentOperation()

        self.assertTrue(PayReceive.objects.filter(document=document).exists())

    def test_008_order_out_default_send_email_true(self):
        auto = AutoCreate('test_000008')
        deposit = auto.createDeposit()
        entity = auto.createEntity(entityType='CLI')

        folder = DocumentFolder()
        folder.name = 'test_000008'
        folder.order = True
        folder.documentType = 'OUT'
        folder.save()

        payment = auto.createPaymentMethod()

        document = Document()
        document.key = 'test_000008'
        document.folder = folder
        document.deposit = deposit
        document.entity = entity
        document.sendMail = False
        document.paymentMethod = payment
        document.save()

        document = Document.objects.get(id=document.id)
        self.assertTrue(document.sendMail)

    def test_009_updateCost_if_product_is_true(self):
        """
        create documentFolder with product is True
        call fullDocumentOperation
        test if product cost is changed
        """
        auto = AutoCreate('test_000009')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        product = auto.createProduct()

        folder = DocumentFolder()
        folder.name = 'test_000009'
        folder.product = True
        folder.stock = True
        folder.documentType = 'IN'
        folder.save()

        auto.createPaymentMethod()

        auto.fullDocumentOperation()
        auto.createDocumentProduct()

        stock = Stock.objects.get(product=product, deposit=deposit)
        self.assertEqual(stock.value, 1)

    def test_010_createPrice_if_product_is_true(self):

        folder = DocumentFolder()
        folder.name = 'test_000010'
        folder.product = False
        folder.createPrice = True
        folder.documentType = 'IN'
        self.assertRaises(ValidationError,folder.save)

    def test_012_write_documentFolderLog(self):
        auto = AutoCreate('test_000012')
        folder = auto.createDocumentFolder()

        log = DocumentFolderLog.objects.filter(documentFolder=folder)
        self.assertEqual(log.count(), 1)
        


class TestCase_010_ModelCompanyLog(TestCase):
    
    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        company = auto.createCompany()

        log = CompanyLog.objects.get(company=company)
        log.message = 'update log'
        self.assertRaises(ValidationError, log.save)


class TestCase_011_ModelDepositLog(TestCase):

    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        deposit = auto.createDeposit()

        log = DepositLog.objects.get(deposit=deposit)
        log.message = 'update log'
        self.assertRaises(ValidationError, log.save)


class TestCase_012_ModelDocumentLog(TestCase):

    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        document = auto.createDocument()

        log = DocumentLog.objects.get(document=document)
        log.message = 'update log'
        self.assertRaises(ValidationError, log.save)


class TestCase_013_ModelEntityLog(TestCase):

    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        entity = auto.createEntity()

        log = EntityLog.objects.get(entity=entity)
        log.message = 'update log'
        self.assertRaises(ValidationError, log.save)


class TestCase_014_ModelProductLog(TestCase):

    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        product = auto.createProduct()

        log = ProductLog.objects.get(product=product)
        log.message = 'update log'
        self.assertRaises(ValidationError, log.save)


class TestCase_015_ModelInventoryLog(TestCase):

    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        inventory = auto.createInventory()

        log = InventoryLog()
        log.inventory = inventory
        log.table = 'TEST'
        log.transaction = 'CRE'
        log.message = 'create log'
        log.save()

        log = InventoryLog.objects.get(id=log.id)
        log.message = 'update log'
        self.assertRaises(ValidationError, log.save)

class TestCase_015_ModelDocumentFolderLog(TestCase):

    def test_001_dont_update_log_register(self):
        auto = AutoCreate('test_000001')
        folder = auto.createDocumentFolder()

        log = DocumentFolderLog.objects.get(documentFolder=folder)
        log.documentFolder = folder
        log.table = 'TEST'
        log.transaction = 'CRE'
        log.message = 'create log'
        self.assertRaises(ValidationError, log.save)


class TestCase_001_ValidatorsCPF(TestCase):

    def test_001_check_with_valid_chars(self):
        cpf = ValidateCPF('055.188.450-90')
        self.assertTrue(cpf.run())
    
    def test_002_check_with_valid_numbers(self):
        cpf = ValidateCPF(5518845090)
        self.assertTrue(cpf.run())

    def test_003_check_with_invalid_chars(self):
        cpf = ValidateCPF('123.456.789-12')
        self.assertFalse(cpf.run())
    
    def test_004_check_with_invalid_numbers(self):
        cpf = ValidateCPF(12345678912)
        self.assertFalse(cpf.run())

    def test_005_check_with_cpf_is_repeat_sequence(self):
        cpf = ValidateCPF(11111111111)
        self.assertFalse(cpf.run())

    def test_006_validate_len_of_string_is_11(self):
        cpf = ValidateCPF(1111)
        self.assertEqual(len(cpf.cpf),11)
    

class TestCase_001_ValidatorsCNPJ(TestCase):

    def test_001_check_with_valid_chars(self):
        cnpj = ValidateCNPJ('15.982.546/0001-62')
        self.assertTrue(cnpj.run())
    
    def test_002_check_with_valid_numbers(self):
        cnpj = ValidateCNPJ(15982546000162)
        self.assertTrue(cnpj.run())

    def test_003_check_with_invalid_chars(self):
        cnpj = ValidateCNPJ('12.345.678/9123-45')
        self.assertFalse(cnpj.run())
    
    def test_004_check_with_invalid_numbers(self):
        cnpj = ValidateCNPJ(12345678912345)
        self.assertFalse(cnpj.run())

    def test_005_validate_len_of_string_is_13(self):
        cnpj = ValidateCNPJ(1111)
        self.assertEqual(len(cnpj.cnpj),13)