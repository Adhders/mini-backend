from django.db import models

# Create your models here.

class Industry(models.Model):
    name = models.CharField(max_length=20, verbose_name='分类',unique=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='subs',
                               null=True, blank=True,
                               verbose_name='行业')
    class Meta:
        db_table = 'tb_industry'
        verbose_name = '行业'
        verbose_name_plural = verbose_name
