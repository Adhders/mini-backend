# Generated by Django 3.1.1 on 2022-06-05 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='baseData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pv', models.IntegerField(verbose_name='浏览量')),
                ('uv', models.IntegerField(verbose_name='访问量')),
            ],
            options={
                'verbose_name': '数据概况',
                'verbose_name_plural': '数据概况',
                'db_table': 'tb_baseData',
            },
        ),
    ]
