# Generated by Django 3.1.1 on 2022-02-01 21:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderNum', models.CharField(max_length=20, unique=True, verbose_name='订单编号')),
                ('status', models.CharField(max_length=10, verbose_name='订单状态')),
                ('goodsList', models.JSONField(null=True, verbose_name='商品列表')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name': 'tb_order',
                'verbose_name_plural': 'tb_order',
                'db_table': 'tb_order',
            },
        )
    ]
