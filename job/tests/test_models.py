from django.test import TestCase
from django.core.exceptions import ValidationError

# Create your tests here.

from job.models import Group, Script, Crontab, ExecutionLog

class AutoCreate:

    def __init__(self,name):
        self.name = name

    def createGroup(self,name=None):
        if name is None:
            name = self.name

        group = Group.objects.filter(name=name)
        if group:
            return group[0]

        group = Group()
        group.name = name
        group.active = True
        group.save()

        return group
    
    def createScript(self,name=None):
        if name is None:
            name = self.name
        
        script = Script.objects.filter(name=name)
        if script:
            return script[0]
        
        script = Script()
        script.name = name
        script.description = f'desc: {name}'
        script.script = name
        script.group = self.createGroup(name=name)
        script.active = True
        script.save()
        
        return script
    
    def createCrontab(self,name=None):
        if name == None:
            name = self.name
        
        crontab = Crontab.objects.filter(name=name)
        if crontab:
            return crontab[0]

        crontab = Crontab()
        crontab.name = name
        crontab.script = self.createScript()
        crontab.description = f'desc: {name}'
        crontab.active = True
        crontab.minute = '*'
        crontab.hour = '*'
        crontab.dayOfWeek = '*'
        crontab.dayOfMonth = '*'
        crontab.month = '*'
        crontab.save()

        return crontab


class TestCase_001_Group(TestCase):
    
    def test_001_create(self):
        auto = AutoCreate('test_000001')
        group = auto.createGroup()

        group = Group.objects.get(id=group.id)
        self.assertTrue(group)

    def test_002_update(self):
        auto = AutoCreate('test_000002')
        group = auto.createGroup()

        group = Group.objects.get(id=group.id)
        group.name = 'test_000002_001'
        group.save()

        group = Group.objects.get(id=group.id)
        self.assertEqual(group.name,'test_000002_001')

    def test_003_delete(self):
        auto = AutoCreate('test_000003')
        group = auto.createGroup()

        group = Group.objects.get(id=group.id)
        group.delete()

        group = Group.objects.get(id=group.id)
        self.assertIsNotNone(group.deletedAt)

    def test_004_open(self):
        auto = AutoCreate('test_000004')
        group = auto.createGroup()

        group = Group.objects.get(id=group.id)
        group.delete()

        group = Group.objects.get(id=group.id)
        group.open()

        group = Group.objects.get(id=group.id)
        self.assertIsNone(group.deletedAt)

    def test_005_close(self):
        auto = AutoCreate('test_000005')
        group = auto.createGroup()

        group = Group.objects.get(id=group.id)
        group.close()

        group = Group.objects.get(id=group.id)
        self.assertIsNotNone(group.deletedAt)

    def test_006_dont_update_deleted(self):
        auto = AutoCreate('test_000006')
        group = auto.createGroup()

        group = Group.objects.get(id=group.id)
        group.close()

        group = Group.objects.get(id=group.id)
        group.name = 'test_000006_001'
        self.assertRaises(ValidationError,group.save)

    def test_007_dont_delete_if_crontab_active(self):
        auto = AutoCreate('test_000007')
        group = auto.createGroup()
        auto.createCrontab()

        group = Group.objects.get(id=group.id)
        self.assertRaises(ValidationError,group.delete)


    def test_008_dont_delete_if_script_active(self):
        auto = AutoCreate('test_000007')
        group = auto.createGroup()
        auto.createScript()

        group = Group.objects.get(id=group.id)
        self.assertRaises(ValidationError,group.delete)


class TestCase_002_Script(TestCase):
    
    def test_001_create(self):
        auto = AutoCreate('test_000001')
        script = auto.createScript()

        script = Script.objects.get(id=script.id)
        self.assertTrue(script)

    def test_002_update(self):
        auto = AutoCreate('test_000002')
        script = auto.createScript()

        script = Script.objects.get(id=script.id)
        script.name = 'test_000002_001'
        script.save()

        script = Script.objects.get(id=script.id)
        self.assertEquals(script.name,'test_000002_001')

    def test_003_delete(self):
        auto = AutoCreate('test_000003')
        script = auto.createScript()

        script = Script.objects.get(id=script.id)
        script.delete()

        script = Script.objects.get(id=script.id)
        self.assertIsNotNone(script.deletedAt)

    def test_004_open(self):
        auto = AutoCreate('test_000004')
        script = auto.createScript()

        script = Script.objects.get(id=script.id)
        script.delete()

        script = Script.objects.get(id=script.id)
        script.open()

        script = Script.objects.get(id=script.id)
        self.assertIsNone(script.deletedAt)

    def test_005_close(self):
        auto = AutoCreate('test_000005')
        script = auto.createScript()

        script = Script.objects.get(id=script.id)
        script.close()

        script = Script.objects.get(id=script.id)
        self.assertIsNotNone(script.deletedAt)

    def test_006_dont_update_deleted(self):
        auto = AutoCreate('test_000006')
        script = auto.createScript()

        script = Script.objects.get(id=script.id)
        script.close()

        script = Script.objects.get(id=script.id)
        script.name = 'test_000006_001'
        self.assertRaises(ValidationError,script.save)

    def test_007_dont_delete_if_crontab_active(self):
        auto = AutoCreate('test_000006')
        script = auto.createScript()
        crontab = auto.createCrontab()

        self.assertRaises(ValidationError,script.close)


class TestCase_003_Crontab(TestCase):
    
    def test_001_create(self):
        auto = AutoCreate('test_000001')
        crontab = auto.createCrontab()

        crontab = Crontab.objects.get(id=crontab.id)
        self.assertTrue(crontab)

    def test_002_update(self):
        auto = AutoCreate('test_000002')
        crontab = auto.createCrontab()

        crontab = Crontab.objects.get(id=crontab.id)
        crontab.name = 'test_000002_001'
        crontab.save()

        crontab = Crontab.objects.get(id=crontab.id)
        self.assertEquals(crontab.name,'test_000002_001')

    def test_003_delete(self):
        auto = AutoCreate('test_000002')
        crontab = auto.createCrontab()

        crontab = Crontab.objects.get(id=crontab.id)
        crontab.delete()

        crontab = Crontab.objects.get(id=crontab.id)
        self.assertIsNotNone(crontab.deletedAt)

    def test_004_open(self):
        auto = AutoCreate('test_000002')
        crontab = auto.createCrontab()

        crontab = Crontab.objects.get(id=crontab.id)
        crontab.delete()
        self.assertIsNotNone(crontab.deletedAt)

        crontab = Crontab.objects.get(id=crontab.id)
        crontab.open()

        crontab = Crontab.objects.get(id=crontab.id)
        self.assertIsNone(crontab.deletedAt)

    def test_005_close(self):
        auto = AutoCreate('test_000002')
        crontab = auto.createCrontab()

        crontab = Crontab.objects.get(id=crontab.id)
        crontab.delete()
        self.assertIsNotNone(crontab.deletedAt)

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

