from django.core.exceptions import ValidationError
from django.test import TestCase

from backoffice.models.PaymentMethod import PaymentMethod
from backoffice.models.PayReceive import PayReceive
# Create your tests here.

class AutoCreate:

    def __init__(self, name):
        self.name = name

    def createPaymentMethod(self, name=None,isPortion=True,portionAmount=7,dueDate=6,portionRegex='15/30/45/60'):
        if name is None:
            name = self.name
        
        paymentMethod = PaymentMethod.objects.filter(name=name)
        if paymentMethod:
            return paymentMethod[0]
        
        paymentMethod = PaymentMethod()
        paymentMethod.name = name
        paymentMethod.isPortion = isPortion
        paymentMethod.portionAmount = portionAmount
        paymentMethod.dueDate = dueDate
        paymentMethod.portionRegex = portionRegex
        paymentMethod.percentagePerDelay = 3
        paymentMethod.percentageDiscount = 8
        paymentMethod.save()

        return paymentMethod

    def createPayReceive(self, document, name=None):
        if name is None:
            name = self.name
        
        payReceive = PayReceive.objects.filter(name=name)
        if payReceive:
            return payReceive[0]


class TestCase_001_ModelPaymentMethod(TestCase):

    def test_001_create(self):
        paymentMethod = PaymentMethod()
        paymentMethod.name = 'test_001_create'
        paymentMethod.isPortion = True
        paymentMethod.portionAmount = 7
        paymentMethod.dueDate = 6
        paymentMethod.portionRegex = '15/30/45/60'
        paymentMethod.percentagePerDelay = 3
        paymentMethod.percentageDiscount = 8
        paymentMethod.save()

        paymentMethod = PaymentMethod.objects.filter(name='test_001_create')
        self.assertTrue(paymentMethod)


    def test_002_update(self):
        paymentMethod = PaymentMethod()
        paymentMethod.name = 'test_002_update'
        paymentMethod.isPortion = True
        paymentMethod.portionAmount = 7
        paymentMethod.dueDate = 6
        paymentMethod.portionRegex = '15/30/45/60'
        paymentMethod.percentagePerDelay = 3
        paymentMethod.percentageDiscount = 8
        paymentMethod.save()

        paymentMethod = PaymentMethod.objects.get(name='test_002_update')
        paymentMethod.name = 'test_002_update_2'
        paymentMethod.save()

        self.assertEqual(paymentMethod.name, 'test_002_update_2')

    def test_999_delete(self):
        paymentMethod = PaymentMethod()
        paymentMethod.name = 'test_999_delete'
        paymentMethod.isPortion = True
        paymentMethod.portionAmount = 7
        paymentMethod.dueDate = 6
        paymentMethod.portionRegex = '15/30/45/60'
        paymentMethod.percentagePerDelay = 3
        paymentMethod.percentageDiscount = 8
        paymentMethod.save()

        paymentMethod = PaymentMethod.objects.get(name='test_999_delete')
        paymentMethod.delete()

        paymentMethod = PaymentMethod.objects.get(name='test_999_delete')
        self.assertIsNotNone(paymentMethod.deletedAt)

    def test_003_inCash_isPortion_equal_False(self):
        paymentMethod = PaymentMethod()
        paymentMethod.name = 'test_003'
        paymentMethod.inCash = True
        paymentMethod.isPortion = True
        paymentMethod.portionAmount = 1
        paymentMethod.dueDate = 0
        paymentMethod.portionRegex = '15/30/45/60'
        paymentMethod.percentagePerDelay = 3
        paymentMethod.percentageDiscount = 8
        self.assertRaises(ValidationError, paymentMethod.save)

    def test_004_inCash_portionAmount_equal_1(self):
        paymentMethod = PaymentMethod()
        paymentMethod.name = 'test_003'
        paymentMethod.inCash = True
        paymentMethod.isPortion = False
        paymentMethod.portionAmount = 1
        paymentMethod.dueDate = 0
        paymentMethod.portionRegex = '15/30/45/60'
        paymentMethod.percentagePerDelay = 3
        paymentMethod.percentageDiscount = 8
        paymentMethod.save()

        for i in range(-50,50):

            paymentMethod = PaymentMethod.objects.get(name='test_003')
            paymentMethod.portionAmount = i
            if i == 1:
                self.assertTrue(paymentMethod.save)
            else:
                self.assertRaises(ValidationError, paymentMethod.save)

    def test_005_inCash_dueDate_is_now(self):
        self.skipTest('empty')

    def test_006_dont_update_if_document_movement(self):
        self.skipTest('empty')

    def test_007_portionAmount_is_gte_1(self):
        self.skipTest('empty')

    def test_008_dueDate_between_1_31(self):
        self.skipTest('empty')

    def test_009_percentagePerDelay_gte_0(self):
        self.skipTest('empty')

    def test_010_percentageDiscount_gte_0(self):
        self.skipTest('empty')

    def test_011_dont_delete_if_PayReceive(self):
        self.skipTest('empty')
    
    def test_012_log_writer(self):
        self.skipTest('empty')


class TestCase_002_ModelPayReceive(TestCase):

    def test_001_create(self):
        self.skipTest('empty')

    def test_002_update(self):
        self.skipTest('empty')

    def test_999_delete(self):
        self.skipTest('empty')

    def test_003_if_document_reopen_delete_movement(self):
        self.skipTest('empty')

    def test_004_dont_repeat_portionNumber_in_same_document(self):
        self.skipTest('empty')

    def test_005_test_valueExtra(self):
        self.skipTest('empty')

    def test_006_test_valueDiscount(self):
        self.skipTest('empty')

    def test_007_method_extra_total_is_working(self):
        self.skipTest('empty')

    def test_008_dont_update_document(self):
        self.skipTest('empty')

    def test_009_dont_update_paymentMethod(self):
        self.skipTest('empty')

    def test_010_dont_update_portionNumber(self):
        self.skipTest('empty')

    def test_011_log_writer(self):
        self.skipTest('empty')


class TesCase_003_ModelPaymentMethod(TestCase):

    def test_001_create(self):
        self.skipTest('empty')

    def test_002_dont_update(self):
        self.skipTest('empty')

    def test_999_delete(self):
        self.skipTest('empty')


class TesCase_003_ModelPayReceive(TestCase):

    def test_001_create(self):
        self.skipTest('empty')

    def test_002_dont_update(self):
        self.skipTest('empty')

    def test_999_delete(self):
        self.skipTest('empty')
