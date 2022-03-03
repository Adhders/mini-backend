# Generated by Django 3.1.1 on 2022-02-01 12:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0010_auto_20211223_1848'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.IntegerField(default=5, verbose_name='星数')),
                ('likes', models.JSONField(null=True, verbose_name='收藏')),
                ('address', models.JSONField(null=True, verbose_name='收货地址')),
                ('name', models.CharField(max_length=50, verbose_name='用户名')),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='手机')),
                ('avatar', models.CharField(max_length=100, verbose_name='用户头像')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_customers', to='store.store', verbose_name='用户')),
            ],
            options={
                'verbose_name': 'tb_customer',
                'verbose_name_plural': 'tb_customer',
                'db_table': 'tb_customer',
            },
        ),
    ]
