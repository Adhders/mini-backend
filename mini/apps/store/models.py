from django.db import models
# Create your models here.
from django.db import models


class Store(models.Model):
    pid = models.ForeignKey('users.User', on_delete=models.CASCADE, to_field='pid',
                            db_column='pid', related_name='all_store', verbose_name='用户')
    appid = models.CharField(max_length=50, null=True, unique=True, verbose_name='微信号')
    mch_id = models.CharField(max_length=15, verbose_name='商户id', unique=True, null=True)
    product_name = models.CharField(max_length=20, verbose_name='产品名')
    version = models.CharField(max_length=20, verbose_name='版本')
    storename = models.CharField(max_length=40, verbose_name='店铺名称')
    trademark = models.CharField(max_length=100, verbose_name='店铺标识')
    address = models.JSONField(max_length=200, verbose_name='店铺地址')
    industry = models.JSONField(max_length=100, verbose_name='行业')
    introduce = models.CharField(max_length=250, null=True, verbose_name='店铺简介')
    mobile = models.CharField(max_length=20, null=True, verbose_name='手机号')
    telephone = models.CharField(max_length=20, null=True, verbose_name='办公电话')
    name = models.CharField(max_length=20, null=True, verbose_name='姓名')
    mail = models.CharField(max_length=30, null=True, verbose_name='邮箱')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_store'
        verbose_name = '店铺'
        ordering = ['-update_time', '-create_time']
        verbose_name_plural = verbose_name


class Detail(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='detail_info', verbose_name='店铺详情')
    detail = models.JSONField(verbose_name='详情')
    pages = models.JSONField(verbose_name='页面')
    tabbar = models.JSONField(verbose_name='导航')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    class Meta:
        db_table = 'tb_detail'
        verbose_name = '详情'
        verbose_name_plural = verbose_name


class Page(models.Model):
    """自定义用户模型类"""
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='page_info', verbose_name='页面详情')
    title = models.CharField(max_length=20, verbose_name='名称', unique=True)
    status = models.CharField(max_length=10, verbose_name='页面状态')
    remarks = models.CharField(null=True, max_length=100, verbose_name='备注')
    marks = models.JSONField(null=True, verbose_name='标签')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="更新时间")

    # 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
    class Meta:
        db_table = 'tb_pages'
        verbose_name = '页面'
        verbose_name_plural = verbose_name
