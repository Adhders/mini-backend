# Generated by Django 3.1.1 on 2022-02-13 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0010_auto_20220212_0857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.JSONField(default=[], null=True, verbose_name='收货地址'),
        ),
    ]
