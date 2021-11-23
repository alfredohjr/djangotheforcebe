# Create your tests here.

import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone as djangoTimezone

from shop.core.validators.cnpj import ValidateCNPJ
from shop.core.validators.cpf import ValidateCPF
from shop.models.Company import Company
from shop.models.CompanyLog import CompanyLog
from shop.models.Deposit import Deposit
from shop.models.DepositLog import DepositLog
from shop.models.Document import Document
from shop.models.DocumentLog import DocumentLog
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Entity import Entity
from shop.models.EntityLog import EntityLog
from shop.models.Price import Price
from shop.models.Product import Product
from shop.models.ProductLog import ProductLog
from shop.models.Stock import Stock
from shop.models.StockMovement import StockMovement

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

    def createDocument(self,name=None,documentType='IN'):
        if name is None:
            name = self.name
        deposit = self.createDeposit(name)
        entityType = 'FOR' if documentType == 'IN' else 'CLI'
        entity = self.createEntity(name, entityType=entityType)

        document = Document.objects.filter(key=name)
        if document:
            return document[0]
        else:    
            document = Document.objects.create(key=name
                            ,deposit=deposit
                            ,entity=entity
                            ,documentType=documentType)
            return document
    
    def createDocumentProduct(self,name=None,documentType='IN'):
        if name is None:
            name = self.name

        document = self.createDocument(name,documentType=documentType)
        product = self.createProduct(name)
        
        documentProduct = DocumentProduct.objects.filter(
            document=document
            ,product=product
        )

        if documentProduct:
            return documentProduct[0]

        documentProduct = DocumentProduct.objects.create(document=document
                                                        ,product=product
                                                        ,amount=1
                                                        ,value=1)
        return documentProduct
    
    def fullDocumentOperation(self,name=None,documentType='IN'):
        if name is None:
            name = self.name
        document = self.createDocument(documentType=documentType)
        documentProduct = self.createDocumentProduct(name,documentType=documentType)
        document = Document.objects.get(id=documentProduct.document.id)
        document.isOpen = False
        document.save()
        return document

    def createPrice(self, name=None):
        if name is None:
            name = self.name

        deposit = self.createDeposit()
        product = self.createProduct()

        price = Price.objects.filter(deposit=deposit, product=product)
        if price:
            return price[0]
        else:
            price = Price()
            price.deposit = deposit
            price.product = product
            price.value = 10
            price.priceType = 'NO'
            price.startedAt = djangoTimezone.now()
            price.save()
            return price


class TestCase_BaseModel(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='test_company')
        self.deposit = Deposit.objects.create(name='test_deposit',company=self.company)
        self.entity = Entity.objects.create(name='test_entity'
                                        ,identifier='494.678.920-06'
                                        ,identifierType='FI'
                                        ,entityType='CLI')
        self.product = Product.objects.create(name='test_product',margin=10)

        self.createDocument()

    def createDocument(self,close=True):
        
        self.document = Document.objects.create(key='test_document'
                                        ,deposit=self.deposit
                                        ,entity=self.entity
                                        ,documentType='OUT')
        self.documentProduct = DocumentProduct.objects.create(document=self.document
                                                    ,product=self.product
                                                    ,amount=1
                                                    ,value=1)

        if close:
            document = Document.objects.get(key='test_document')
            document.isOpen = False
            document.save()

    def _001_create_model(self):
        self.skipTest('empty')
        
    def _002_update_model(self):
        self.skipTest('empty')

    def _999_delete_company(self):
        self.skipTest('empty')

    def _012_update_fields_with_after_deleted(self):
        self.skipTest('empty')


class TestCase_001_ModelCompany(TestCase_BaseModel):

    def setUp(self):
        super().setUp()

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

        entity = Entity.objects.create(name='test_entity'
                                        ,identifier='15.987.787/0001-02'
                                        ,identifierType='JU'
                                        ,entityType='FOR')
        document = Document.objects.create(key='test_document_out'
                                            ,deposit=self.deposit
                                            ,entity=entity
                                            ,documentType='IN')
        DocumentProduct.objects.create(document=document
                                        ,product=self.product
                                        ,amount=1
                                        ,value=1)

        document = Document.objects.get(key='test_document_out')
        document.isOpen = False
        document.save()

        company = Company.objects.get(name='test_company')
        self.assertIsNone(company.deletedAt)
        company.delete()
        
        company = Company.objects.get(name='test_company')
        self.assertIsNotNone(company.deletedAt)

    def test_004_delete_company_with_product_inventory(self):
        self.skipTest('empty')
    
    def test_006_delete_company_with_document_open(self):
        auto = AutoCreate(name='test_000006')
        document = auto.createDocument()

        company = Company.objects.get(name='test_000006')
        company.delete()

        company = Company.objects.get(name='test_000006')
        self.assertIsNone(company.deletedAt)
       
    def test_008_delete_company_with_deposit_is_finance_open(self):
        self.skipTest('empty')
    
    def test_009_delete_company_with_deposit_inventory_is_open(self):
        self.skipTest('empty')

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
        self.skipTest('empty')
    
    def test_005_delete_deposit_with_document_open(self):
        auto = AutoCreate('test_000005')
        auto.createDocumentProduct()

        deposit = Deposit.objects.get(name='test_000005')
        self.assertIsNone(deposit.deletedAt)

    def test_006_delete_deposit_with_is_finance_open(self):
        self.skipTest('empty')
    
    def test_007_delete_deposit_with_inventory_is_open(self):
        self.skipTest('empty')

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
        self.skipTest('empty')
    
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
        self.skipTest('empty')

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

        document = Document()
        document.key = 'test_000009'
        document.deposit = deposit
        document.entity = entity
        document.isOpen = False
        self.assertRaises(ValidationError,document.save)

    def test_010_create_document_if_entity_is_CLI_documentType_is_IN(self):
        auto = AutoCreate('test_000010')
        deposit = auto.createDeposit()
        entity = auto.createEntity(entityType='CLI',identifierType='FI',identifier='462.924.380-15')
        
        document = Document()
        document.key = 'test_000010'
        document.deposit = deposit
        document.entity = entity
        document.documentType = 'IN'
        self.assertRaises(ValidationError,document.save)

    def test_011_create_document_if_entity_is_FOR_documentType_is_OUT(self):
        auto = AutoCreate('test_000011')
        deposit = auto.createDeposit()
        entity = auto.createEntity()
        
        document = Document()
        document.key = 'test_000011'
        document.deposit = deposit
        document.entity = entity
        document.documentType = 'OUT'
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
        document.isOpen = True
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
        document.isOpen = True
        document.save()

        for docprod in documentProduct:
            stock = Stock.objects.get(
                        product__id=docprod.product.id
                        ,deposit__id=document.deposit.id)
            self.assertEqual(stock.amount,0)

    def test_015_Reopen_document_reason_as_20_or_more_chars(self):
        self.skipTest('empty')

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

        document = Document()
        document.key = 'test_000018'
        document.deposit = deposit
        document.entity = entity
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
        self.assertEqual(document.documentType,'IN')
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
        self.assertEqual(document.documentType,'OUT')
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
    
    def test_013_hierarchy_of_prices(self):
        self.skipTest('empty')

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
        self.skipTest('empty')

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
        self.skipTest('empty')

    def test_006_inventory_OUT(self):
        self.skipTest('empty')

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
        entity = auto.createEntity(name='test_000012_001',entityType='CLI')
        document = auto.fullDocumentOperation()

        document = Document()
        document.deposit = deposit
        document.entity = entity
        document.documentType = 'OUT'
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
        entity = auto.createEntity(name='test_000015_001', entityType='CLI')
        auto.fullDocumentOperation()

        document = Document()
        document.deposit = deposit
        document.entity = entity
        document.documentType = 'OUT'
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