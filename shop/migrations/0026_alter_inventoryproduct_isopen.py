# Generated by Django 3.2.8 on 2021-12-05 21:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0025_alter_inventoryproduct_valuebefore'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryproduct',
            name='isOpen',
            field=models.BooleanField(default=True),
        ),
    ]