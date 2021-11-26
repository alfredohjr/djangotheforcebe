from django.test import TestCase

# Create your tests here.

class TestCase_001_Group(TestCase):
    
    def test_001_create(self):
        self.skipTest('empty')

    def test_002_update(self):
        self.skipTest('empty')

    def test_003_delete(self):
        self.skipTest('empty')

    def test_004_open(self):
        self.skipTest('empty')

    def test_005_close(self):
        self.skipTest('empty')

    def test_006_dont_update_deleted(self):
        self.skipTest('empty')

    def test_007_dont_delete_if_crontab_active(self):
        self.skipTest('empty')

    def test_007_dont_delete_if_script_active(self):
        self.skipTest('empty')


class TestCase_002_Script(TestCase):
    
    def test_001_create(self):
        self.skipTest('empty')

    def test_002_update(self):
        self.skipTest('empty')

    def test_003_delete(self):
        self.skipTest('empty')

    def test_004_open(self):
        self.skipTest('empty')

    def test_005_close(self):
        self.skipTest('empty')

    def test_006_dont_update_deleted(self):
        self.skipTest('empty')

    def test_007_dont_delete_if_crontab_active(self):
        self.skipTest('empty')


class TestCase_003_Crontab(TestCase):
    
    def test_001_create(self):
        self.skipTest('empty')

    def test_002_update(self):
        self.skipTest('empty')

    def test_003_delete(self):
        self.skipTest('empty')

    def test_004_open(self):
        self.skipTest('empty')

    def test_005_close(self):
        self.skipTest('empty')

    def test_006_dont_update_deleted(self):
        self.skipTest('empty')
    
    def test_007_dont_insert_if_script_deleted(self):
        self.skipTest('empty')

    def test_007_dont_update_if_script_deleted(self):
        self.skipTest('empty')

    def test_007_dont_insert_if_group_deleted(self):
        self.skipTest('empty')

    def test_007_dont_update_if_group_deleted(self):
        self.skipTest('empty')


class TestCase_004_ExecutionLog(TestCase):
    
    def test_001_create(self):
        self.skipTest('empty')

    def test_002_dont_update(self):
        self.skipTest('empty')

    def test_003_dont_delete(self):
        self.skipTest('empty')

    def test_004_open(self):
        self.skipTest('empty')

    def test_005_close(self):
        self.skipTest('empty')

    def test_006_dont_update_deleted(self):
        self.skipTest('empty')


class TestCase_005_ExecutionManual(TestCase):
    
    def test_001_create(self):
        self.skipTest('empty')

    def test_002_dont_update(self):
        self.skipTest('empty')

    def test_003_dont_delete(self):
        self.skipTest('empty')

    def test_004_open(self):
        self.skipTest('empty')

    def test_005_close(self):
        self.skipTest('empty')

    def test_006_dont_update_deleted(self):
        self.skipTest('empty')
    
    def test_007_dont_run_if_script_deleted(self):
        self.skipTest('empty')

    def test_008_dont_run_if_user_is_deleted(self):
        self.skipTest('empty')

    def test_008_dont_run_if_user_is_zero(self):
        self.skipTest('empty')

