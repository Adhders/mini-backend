# Generated by Django 3.1.1 on 2022-02-21 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_auto_20220221_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='description',
            field=models.CharField(max_length=125, null=True, verbose_name='描述'),
        ),
    ]
