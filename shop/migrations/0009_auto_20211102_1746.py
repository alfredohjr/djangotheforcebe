# Generated by Django 3.2.8 on 2021-11-02 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_auto_20211102_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='finishedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='price',
            name='startedAt',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
