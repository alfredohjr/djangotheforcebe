# Generated by Django 3.2.8 on 2021-12-04 01:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0023_rename_entity_inventorylog_inventory'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inventory',
            unique_together={('name', 'deposit', 'createdAt')},
        ),
    ]
