# Generated by Django 3.2.8 on 2021-11-28 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0018_inventory_inventorylog_inventoryproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='sendMail',
            field=models.BooleanField(default=True),
        ),
    ]
