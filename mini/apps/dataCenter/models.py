from django.db import models


# Create your models here.

class baseData(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='general_data',
                              verbose_name='店铺')
    pv = models.IntegerField(verbose_name='浏览量')
    uv = models.IntegerField(verbose_name='访问量')

    class Meta:
        db_table = 'tb_baseData'
        verbose_name = '数据概况'
        verbose_name_plural = verbose_name
