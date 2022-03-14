# Generated by Django 3.1.1 on 2022-03-11 19:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0015_remove_customer_defaultaddress'),
        ('store', '0011_auto_20220206_1909'),
        ('orders', '0013_auto_20220311_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='refundorder',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='all_refundOrders', to='store.store', verbose_name='店铺订单'),
        ),
        migrations.AlterField(
            model_name='refundorder',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='customer.customer', to_field='openid', verbose_name='顾客'),
        ),
    ]
