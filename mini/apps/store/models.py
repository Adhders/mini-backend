from django.db import models
# Create your models here.
from django.db import models
import json

class Store(models.Model):
    pid = models.ForeignKey('users.User', on_delete=models.CASCADE, to_field='pid',
                            db_column='pid', related_name='all_store', verbose_name='用户')
    appid = models.CharField(max_length=50, null=True, unique=True, verbose_name='微信号')
    mch_id = models.CharField(max_length=15, verbose_name='商户id', unique=True, null=True)
    product_name = models.CharField(max_length=20, verbose_name='产品名')
    version = models.CharField(max_length=20, verbose_name='版本')
    storename = models.CharField(max_length=40, verbose_name='店铺名称')
    trademark = models.CharField(max_length=100, verbose_name='店铺标识')
    address = models.JSONField(verbose_name='店铺地址', default=list)
    industry = models.JSONField(verbose_name='行业', default=list)
    introduce = models.CharField(max_length=250, null=True, verbose_name='店铺简介')
    mobile = models.CharField(max_length=20, null=True, verbose_name='手机号')
    telephone = models.CharField(max_length=20, null=True, verbose_name='办公电话')
    name = models.CharField(max_length=20, null=True, verbose_name='联系人姓名')
    mail = models.CharField(max_length=30, null=True, verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")
    def toJSON(self):
        return json.dumps(dict([(attr, getattr(self, attr)) for attr in [f.name for f in self._meta.fields]]))

    class Meta:
        db_table = 'tb_store'
        verbose_name = '店铺'
        ordering = ['-update_time', '-create_time']
        verbose_name_plural = verbose_name


class StoreSetting(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='store_setting', verbose_name='店铺设置')
    paymentSetting = models.JSONField(verbose_name='行业', null=True)

    class Meta:
        db_table = 'tb_setting'
        verbose_name = '店铺设置'
        verbose_name_plural = verbose_name



class Detail(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='detail_info', verbose_name='店铺详情')
    detail = models.JSONField(verbose_name='详情', default=list)
    tabbar = models.JSONField(verbose_name='导航', null=True)
    labels = models.JSONField(verbose_name='标签', default=list)
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_detail'
        verbose_name = '详情'
        verbose_name_plural = verbose_name

