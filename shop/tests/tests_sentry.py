from django.test import TestCase
from shop.tests.tests_models import AutoCreate

class TestCase_001_sentry(TestCase):

    def test_001_sentry_only_production(self):
        self.skipTest('empty')

    def test_002_ignore_ValidationError(self):
        self.skipTest('empty')