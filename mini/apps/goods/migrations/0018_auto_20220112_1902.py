# Generated by Django 3.1.1 on 2022-01-12 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0017_review_anonymous'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='videoImage',
            field=models.CharField(max_length=100, null=True, verbose_name='视频链接'),
        ),
        migrations.AddField(
            model_name='review',
            name='videoUrl',
            field=models.CharField(max_length=100, null=True, verbose_name='视频封面'),
        ),
        migrations.DeleteModel(
            name='GoodsReview',
        ),
    ]
