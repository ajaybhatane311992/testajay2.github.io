# Generated by Django 3.2.4 on 2021-06-19 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp1', '0004_ordermodel_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='address',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='Name',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='description',
            field=models.CharField(max_length=200),
        ),
    ]
