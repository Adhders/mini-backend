from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models

class User(AbstractBaseUser):
    """自定义用户模型类"""
    mobile = models.CharField(max_length=20, primary_key=True, verbose_name='手机号')
    name = models.CharField(max_length=20, null=True, verbose_name='姓名')
    mail = models.CharField(max_length=30, null=True, verbose_name='邮箱')
    wechat = models.CharField(max_length=50, null=True, unique=True, verbose_name='微信号')
    pid = models.CharField(unique=True, max_length=50, verbose_name="用户id")
    token = models.CharField(null=True, max_length=250, verbose_name='token')
    store = models.ForeignKey('store.Store',null=True, on_delete=models.CASCADE,verbose_name='默认店铺')
    create_time = models.DateTimeField(null=True,auto_now=False, auto_now_add=True, verbose_name="注册时间")
    USERNAME_FIELD = 'mobile'

    # 模型已经迁移建表,并且表中已经有数据之后,再给表/模型新增字段时,必须给默认值或可以为空,不然迁移就报错
    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
