from django.core.exceptions import ValidationError
from django.test import TestCase
from shop.models.Deposit import Deposit

from shop.models.Document import Document
from shop.models.Price import Price
from shop.models.Product import Product

from shop.tests.tests_models import AutoCreate

class test_001_bugs(TestCase):

    def test_001_alter_field_sendMail_in_document_after_closed(self):
        auto = AutoCreate('test_000001')
        document = auto.fullDocumentOperation(documentType='OUT')

        self.assertFalse(document.isOpen)
        self.assertTrue(document.sendMail)

        document = Document.objects.get(id=document.id)
        document.sendMail = False
        document.save()

        document = Document.objects.get(id=document.id)

    def test_002_dont_create_price_with_startedAt_None(self):
        auto = AutoCreate('test_000002')
        deposit = auto.createDeposit()
        product = auto.createProduct()

        price = Price()
        price.deposit = deposit
        price.product = product
        price.value = 100
        price.startedAt = None
        self.assertRaises(ValidationError, price.save)