# Generated by Django 3.1.1 on 2022-01-09 11:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_auto_20211223_1848'),
        ('goods', '0010_review_spu'),
    ]

    operations = [
        # migrations.RemoveField(
        #     model_name='spu',
        #     name='skuList',
        # ),

        migrations.AddField(
            model_name='goods',
            name='sku',
            field=models.CharField(default=0, max_length=20, verbose_name='商品sku'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='goods',
            name='spu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='all_skus', to='store.store', verbose_name='店铺'),
        ),
    ]