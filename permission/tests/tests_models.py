from django.test import TestCase

# Create your tests here.

class TestCase_001_Permission(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')


class TestCase_002_UserPermission(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')
    
    def test_008_dont_insert_if_permission_is_closed(self):
        self.skipTest('empty')


class TestCase_003_Group(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')


class TestCase_004_GroupPermission(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')

    def test_008_dont_insert_if_group_deleted(self):
        self.skipTest('empty')

    def test_009_dont_insert_if_permission_deleted(self):
        self.skipTest('empty')


class TestCase_005_userGroup(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')

    def test_008_dont_insert_if_user_deleted(self):
        self.skipTest('empty')

    def test_009_dont_insert_if_user_closed(self):
        self.skipTest('empty')

    def test_010_dont_insert_if_user_blocked(self):
        self.skipTest('empty')


class TestCase_006_Log(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')


class TestCase_007_PermissionLog(TestCase):
    
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

    def test_007_dont_delete_if_user_active(self):
        self.skipTest('empty')