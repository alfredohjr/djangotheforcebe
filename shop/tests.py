from datetime import timezone
from unittest.case import SkipTest
from django.test import TestCase
from django.utils import timezone as djangoTimezone

# Create your tests here.

from shop.models.Company import Company
from shop.models.Deposit import Deposit
from shop.models.Document import Document
from shop.models.DocumentProduct import DocumentProduct
from shop.models.Entity import Entity
from shop.models.Product import Product
from shop.models.Stock import Stock

class AutoCreate:

    def __init__(self,name):
        self.name = name
    
    def createCompany(self,name=None):
        if name is None:
            name = self.name
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
        deposit = Deposit.objects.create(name=name,company=company)
        return deposit
        
    def createEntity(self,name=None):
        if name is None:
            name = self.name
        entity = Entity.objects.create(name=name
                                        ,identifier=name + '_123456'
                                        ,identifierType='JU'
                                        ,entityType='FOR')
        return entity

    def createDocument(self,name=None,documentType='IN'):
        if name is None:
            name = self.name
        deposit = self.createDeposit(name)
        entity = self.createEntity(name)
        document = Document.objects.create(key=name
                            ,deposit=deposit
                            ,entity=entity
                            ,documentType=documentType)
        return document
    
    def createDocumentProduct(self,name=None):
        if name is None:
            name = self.name
        document = self.createDocument(name)
        documentProduct = DocumentProduct.objects.create(document=document
                                                        ,product=self.product
                                                        ,amount=1
                                                        ,value=1)
        return documentProduct
    
    def fullDocumentOperation(self,name=None):
        if name is None:
            name = self.name
        documentProduct = self.createDocumentProduct(name)
        document = Document.objects.get(id=documentProduct.document.id)
        document.isOpen = False
        document.save()
        return document

class TestCase_BaseModel(TestCase):

    def setUp(self):
        self.company = Company.objects.create(name='test_company')
        self.deposit = Deposit.objects.create(name='test_deposit',company=self.company)
        self.entity = Entity.objects.create(name='test_entity'
                                        ,identifier='123456789'
                                        ,identifierType='FI'
                                        ,entityType='FOR')
        self.product = Product.objects.create(name='test_product',margin=10)

        self.createDocument()

    def createDocument(self,close=True):
        
        self.document = Document.objects.create(key='test_document'
                                        ,deposit=self.deposit
                                        ,entity=self.entity
                                        ,documentType='IN')
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
        company = Company.objects.get(name='test_company')
        self.assertEqual(company.name,'test_company')
        
    def test_002_update_company(self):
        company = Company.objects.get(name='test_company')
        company.name = 'company'
        company.save()
        company = Company.objects.get(name='company')
        self.assertEqual(company.name,'company')
        self.assertLess(company.createdAt,company.updatedAt)
        self.assertIsNot(company.createdAt,company.updatedAt)

    def test_003_delete_company_with_product_stock(self):

        company = Company.objects.get(name='test_company')
        company.delete()
        self.assertIsNone(company.deletedAt)

    def test_999_delete_company(self):

        document = Document.objects.create(key='test_document_out'
                                            ,deposit=self.deposit
                                            ,entity=self.entity
                                            ,documentType='OUT')
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
        auto = AutoCreate(name='test_006')
        document = auto.createDocument()

        company = Company.objects.get(name='test_006')
        company.delete()

        company = Company.objects.get(name='test_006')
        self.assertIsNone(company.deletedAt)
       
    def test_008_delete_company_with_deposit_is_finance_open(self):
        self.skipTest('empty')
    
    def test_009_delete_company_with_deposit_inventory_is_open(self):
        self.skipTest('empty')

    def test_010_company_register_in_log_table(self):
        self.skipTest('empty')

    def test_011_companyLog_write_correct(self):
        self.skipTest('empty')

    def test_012_company_size_minimun_of_name_is_10(self):
        self.skipTest('empty')

    def test_013_update_fields_with_after_deleted(self):
        auto = AutoCreate(name='test_013')
        companyAux = auto.createAndDeleteCompany()

        company = Company.objects.get(name='test_013')
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
        auto = AutoCreate(name='test_014')
        companyAux = auto.createAndDeleteCompany()

        company = Company.objects.get(id=companyAux.id)
        company.deletedAt = None
        company.save()

        company = Company.objects.get(id=companyAux.id)
        self.assertIsNone(company.deletedAt)


class TestCase_002_ModelDeposit(TestCase):

    def test_001_create_deposit(self):
        self.skipTest('empty')

    def test_002_update_deposit(self):
        self.skipTest('empty')

    def test_003_delete_deposit_with_product_stock(self):
        self.skipTest('empty')

    def test_999_delete_deposit(self):
        self.skipTest('empty')

    def test_004_delete_deposit_with_product_inventory(self):
        self.skipTest('empty')
    
    def test_005_delete_deposit_with_document_open(self):
        self.skipTest('empty')

    def test_006_delete_deposit_with_is_finance_open(self):
        self.skipTest('empty')
    
    def test_007_delete_deposit_with_inventory_is_open(self):
        self.skipTest('empty')

    def test_008_deposit_register_in_log_table(self):
        self.skipTest('empty')

    def test_009_depositLog_write_correct(self):
        self.skipTest('empty')

    def test_010_deposit_size_minimun_of_name_is_10(self):
        self.skipTest('empty')

    def test_011_create_deposit_with_deleted_company(self):
        self.skipTest('empty')

    def test_012_update_fields_with_after_deleted(self):
        self.skipTest('empty')


class TestCase_003_ModelEntity(TestCase):

    def test_001_create_entity(self):
        self.skipTest('empty')

    def test_002_update_entity(self):
        self.skipTest('empty')

    def test_999_delete_entity(self):
        self.skipTest('empty')

    def test_003_delete_entity_with_document_open(self):
        self.skipTest('empty')

    def test_004_delete_entity_with_is_finance_open(self):
        self.skipTest('empty')
    
    def test_005_entity_register_in_log_table(self):
        self.skipTest('empty')

    def test_006_entityLog_write_correct(self):
        self.skipTest('empty')

    def test_007_entity_size_minimun_of_name_is_10(self):
        self.skipTest('empty')

    def test_008_if_entity_is_CLI_document_is_OUT(self):
        self.skipTest('empty')

    def test_009_if_entity_is_FOR_document_is_IN(self):
        self.skipTest('empty')

    def test_010_if_entity_is_JU_validate_CNPJ(self):
        self.skipTest('empty')

    def test_011_if_entity_is_FI_validate_CPF(self):
        self.skipTest('empty')

    def test_012_entity_size_minimun_of_name_is_10(self):
        self.skipTest('empty')

    def test_013_update_fields_with_after_deleted(self):
        self.skipTest('empty')


class TestCase_004_ModelProduct(TestCase):

    def test_001_create_product(self):
        self.skipTest('empty')

    def test_002_update_product(self):
        self.skipTest('empty')

    def test_999_delete_product(self):
        self.skipTest('empty')

    def test_003_delete_with_stock(self):
        self.skipTest('empty')

    def test_004_delete_with_document_open(self):
        self.skipTest('empty')

    def test_005_delete_with_inventory_is_open(self):
        self.skipTest('empty')

    def test_006_productLog_write_correct(self):
        self.skipTest('empty')

    def test_007_product_size_minimun_of_name_is_10(self):
        self.skipTest('empty')
    
    def test_008_product_margin_negative(self):
        self.skipTest('empty')

    def test_009_update_fields_with_after_deleted(self):
        self.skipTest('empty')

    def test_010_product_register_in_log_table(self):
        self.skipTest('empty')


class TestCase_005_ModelDocument(TestCase):

    def test_001_create_document(self):
        self.skipTest('empty')

    def test_002_update_document(self):
        self.skipTest('empty')

    def test_999_delete_document(self):
        self.skipTest('empty')

    def test_003_delete_with_document_close(self):
        self.skipTest('empty')

    def test_004_documentLog_write_correct(self):
        self.skipTest('empty')

    def test_005_create_document_with_company_is_close(self):
        self.skipTest('empty')

    def test_006_create_document_with_deposit_is_close(self):
        self.skipTest('empty')

    def test_007_create_document_with_entity_is_close(self):
        self.skipTest('empty')

    def test_008_close_document_without_product(self):
        self.skipTest('empty')

    def test_009_create_document_with_isOpen_false(self):
        self.skipTest('empty')

    def test_010_create_document_if_entity_is_CLI_documentType_is_IN(self):
        self.skipTest('empty')

    def test_011_create_document_if_entity_is_FOR_documentType_is_OUT(self):
        self.skipTest('empty')

    def test_012_check_product_of_documents_isOpen_is_equals(self):
        self.skipTest('empty')

    def test_013_close_document_stock_is_correct(self):
        self.skipTest('empty')

    def test_014_Reopen_document_stock_is_correct(self):
        self.skipTest('empty')

    def test_015_Reopen_document_reason_as_20_or_more_chars(self):
        self.skipTest('empty')

    def test_016_update_fields_with_after_deleted(self):
        self.skipTest('empty')

    def test_010_document_register_in_log_table(self):
        self.skipTest('empty')


class TestCase_006_ModelDocumentProduct(TestCase):

    def test_001_create_documentProduct(self):
        self.skipTest('empty')

    def test_002_update_documentProduct(self):
        self.skipTest('empty')

    def test_999_delete_documentProduct(self):
        self.skipTest('empty')

    def test_003_delete_with_document_close(self):
        self.skipTest('empty')

    def test_004_documentLog_write_correct(self):
        self.skipTest('empty')

    def test_005_value_is_negative(self):
        self.skipTest('empty')

    def test_006_amount_is_negative(self):
        self.skipTest('empty')

    def test_007_create_documentProduct_with_isOpen_false(self):
        self.skipTest('empty')

    def test_008_create_documentProduct_with_document_isOpen_false(self):
        self.skipTest('empty')

    def test_009_close_documentProduct_IN_stock_is_correct(self):
        self.skipTest('empty')

    def test_010_close_documentProduct_IN_stock_movement_is_correct(self):
        self.skipTest('empty')

    def test_009_close_documentProduct_OUT_stock_is_correct(self):
        self.skipTest('empty')

    def test_010_close_documentProduct_OUT_stock_movement_is_correct(self):
        self.skipTest('empty')

    def test_009_close_documentProduct_price_is_suggested_correct(self):
        self.skipTest('empty')

    def test_010_update_fields_with_after_deleted(self):
        self.skipTest('empty')

    def test_010_documentProduct_register_in_log_table(self):
        self.skipTest('empty')

    def test_011_value_is_zero(self):
        self.skipTest('empty')

    def test_011_amount_is_zero(self):
        self.skipTest('empty')


class TestCase_007_ModelPrice(TestCase_BaseModel):
    
    def setUp(self):
        return super().setUp()

    def test_001_create_price(self):
        self.skipTest('empty')

    def test_002_update_price(self):
        self.skipTest('empty')

    def test_999_delete_price(self):
        self.skipTest('empty')

    def test_003_create_price_with_closed_company(self):
        self.skipTest('empty')

    def test_004_create_price_with_closed_deposit(self):
        self.skipTest('empty')

    def test_005_create_price_with_negative_values(self):
        self.skipTest('empty')

    def test_006_if_priceType_is_NO_finishedAt_is_none(self):
        self.skipTest('empty')

    def test_007_if_priceType_is_OF_startedAt_and_finishedAt_is_not_none(self):
        self.skipTest('empty')

    def test_008_define_price_before_stock_gt_zero(self):
        self.skipTest('empty')

    def test_009_create_with_startedAt_yesterday(self):
        self.skipTest('empty')
    
    def test_010_create_with_finishedAt_yesterday(self):
        self.skipTest('empty')

    def test_011_update_fields_with_after_deleted(self):
        self.skipTest('empty')

    def test_010_price_register_in_log_table(self):
        self.skipTest('empty')
    
    def test_011_hierarchy_of_prices(self):
        self.skipTest('empty')


class TestCase_008_ModelStock(TestCase):
    
    def setUp(self):
        return super().setUp()

    def test_001_create_stock_only_document(self):
        self.skipTest('empty')

    def test_002_update_stock_only_document(self):
        self.skipTest('empty')

    def test_999_delete_stock_with_amount_gt_zero(self):
        self.skipTest('empty')

    def test_003_update_value_only_document_IN(self):
        self.skipTest('empty')

    def test_004_update_amount_only_document(self):
        self.skipTest('empty')

    def test_005_inventory_IN(self):
        self.skipTest('empty')

    def test_006_inventory_OUT(self):
        self.skipTest('empty')

    def test_007_create_stock_with_company_close(self):
        self.skipTest('empty')

    def test_008_create_stock_with_deposit_close(self):
        self.skipTest('empty')

    def test_009_create_stock_with_product_close(self):
        self.skipTest('empty')

    def test_010_create_with_value_negative(self):
        self.skipTest('empty')

    def test_011_update_with_value_negative(self):
        self.skipTest('empty')

    def test_012_update_fields_with_after_deleted(self):
        self.skipTest('empty')

    def test_010_product_register_in_log_table(self):
        self.skipTest('empty')


class TestCase_009_ModelStockMovement(TestCase):
    
    def test_001_dont_update_register(self):
        self.skipTest('empty')


class TestCase_010_ModelCompanyLog(TestCase):
    
    def test_001_dont_update_log_register(self):
        self.skipTest('empty')


class TestCase_011_ModelDepositLog(TestCase):

    def test_001_dont_update_log_register(self):
        self.skipTest('empty')


class TestCase_012_ModelDocumentLog(TestCase):

    def test_001_dont_update_log_register(self):
        self.skipTest('empty')


class TestCase_013_ModelEntityLog(TestCase):

    def test_001_dont_update_log_register(self):
        self.skipTest('empty')


class TestCase_014_ModelProductLog(TestCase):

    def test_001_dont_update_log_register(self):
        self.skipTest('empty')
