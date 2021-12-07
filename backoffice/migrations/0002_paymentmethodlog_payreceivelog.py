# Generated by Django 3.2.8 on 2021-12-07 00:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backoffice', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayReceiveLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=50)),
                ('transaction', models.CharField(max_length=3)),
                ('message', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
                ('payReceive', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.payreceive')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethodLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('table', models.CharField(max_length=50)),
                ('transaction', models.CharField(max_length=3)),
                ('message', models.TextField()),
                ('createdAt', models.DateTimeField(auto_now_add=True)),
                ('updatedAt', models.DateTimeField(auto_now=True)),
                ('deletedAt', models.DateTimeField(blank=True, null=True)),
                ('paymentMethod', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backoffice.paymentmethod')),
            ],
        ),
    ]
