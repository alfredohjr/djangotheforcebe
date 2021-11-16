# Generated by Django 3.2.8 on 2021-11-16 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_auto_20211115_2247'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=50)),
                ('transaction', models.CharField(max_length=3)),
                ('message', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
                ('document', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.document')),
            ],
        ),
    ]