# Generated by Django 3.1.1 on 2022-03-08 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0026_auto_20220308_1143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodsreview',
            name='imgs',
            field=models.JSONField(default=list, verbose_name='评论图片'),
        ),
    ]