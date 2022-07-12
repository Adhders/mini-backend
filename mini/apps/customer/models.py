from django.db import models


# Create your models here.cc
class Customer(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_customers', verbose_name='用户')
    openid = models.CharField(max_length=50, unique=True, null=True)
    pid = models.CharField(max_length=50, verbose_name='用户编号', unique=True)
    likes = models.JSONField(verbose_name='收藏', null=True)
    reviewLikes = models.JSONField(verbose_name='评论点赞', default=list)
    addressList = models.JSONField(verbose_name='收货地址', default=list)
    defaultAddress = models.JSONField(verbose_name='默认地址', null=True)
    cart = models.JSONField(verbose_name='购物车', default=list)
    gender = models.CharField(max_length=5, verbose_name='性别', null=True)
    city = models.CharField(max_length=20, verbose_name='城市', null=True)
    country = models.CharField(max_length=20, verbose_name='国家', null=True)
    province = models.CharField(max_length=20, verbose_name='省份', null=True)
    nickName = models.CharField(max_length=20, verbose_name='昵称', null=True)
    phone = models.CharField(max_length=20, verbose_name='手机', null=True)
    birthDay = models.CharField(max_length=15, verbose_name='出生年月', null=True, default='未设置')
    avatarUrl = models.CharField(max_length=255, verbose_name='用户头像')
    channel = models.CharField(max_length=10, verbose_name='渠道', default='微信')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'tb_customer'
        verbose_name = 'tb_customer'
        verbose_name_plural = verbose_name
