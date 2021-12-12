from django.test import TestCase
from shop.models.Document import Document
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
        self.skipTest('empty')