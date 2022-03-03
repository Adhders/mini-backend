from django.db import models

# Create your models here.



class Template(models.Model):
    name = models.CharField(max_length=20, verbose_name='标题')
    category = models.ForeignKey('industry.Industry',to_field='name',
                                 related_name='all_template', verbose_name='类别')
    tags = models.CharField(max_length=200, verbose_name='标签')
    pages = models.JSONField(verbose_name='样本页面',null=True)
    link = models.CharField(max_length=100, verbose_name='链接')
    class Meta:
        db_table = 'tb_template'
        verbose_name = '模板'
        verbose_name_plural = verbose_name
