# Generated by Django 3.2.8 on 2021-10-31 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_document_isopen'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentproduct',
            name='isOpen',
            field=models.BooleanField(default=True),
        ),
    ]
