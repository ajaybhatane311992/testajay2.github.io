# Generated by Django 3.2.4 on 2021-06-12 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EcomApp1', '0002_ordermodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='address',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='phone',
            field=models.CharField(default='', max_length=20),
        ),
    ]