# Generated by Django 3.2.8 on 2021-11-23 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0004_auto_20211123_2334'),
    ]

    operations = [
        migrations.AddField(
            model_name='log',
            name='method',
            field=models.CharField(default='NA', max_length=20),
        ),
    ]