from django.db import models

# Create your models here.
from django.db.models import ManyToManyField, DateTimeField


class Order(models.Model):
    orderNum = models.CharField(max_length=50, verbose_name='订单编号', unique=True)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_orders', verbose_name='店铺订单')
    customer = models.ForeignKey('customer.Customer', to_field='openid', on_delete=models.CASCADE, verbose_name='顾客')
    status = models.CharField(max_length=10, verbose_name='订单状态')
    note = models.CharField(max_length=250, verbose_name='留言', null=True)
    description = models.CharField(max_length=125, verbose_name='描述', null=True)
    totalCost = models.FloatField(verbose_name='总价', default=0.00)
    netCost = models.FloatField(verbose_name="实付", default=0.00)
    discount = models.FloatField(verbose_name="优惠", default=0.00)
    isDeleted = models.BooleanField(verbose_name='是否已删除', default=False)
    shipping_fee = models.FloatField(verbose_name='邮费', default=0.00)
    paymentInfo = models.JSONField(verbose_name="支付信息", null=True)
    reviewState = models.JSONField(verbose_name="评论状态", null=True)
    goodsList = models.JSONField(verbose_name="商品列表", null=True)
    address = models.JSONField(verbose_name="邮寄地址", null=True)
    payment_time = models.DateTimeField(auto_now=False, null=True, verbose_name="支付时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None
            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            data[f.name] = value
        return data

    class Meta:
        db_table = 'tb_order'
        ordering = ['-create_time']
        verbose_name = 'tb_order'
        verbose_name_plural = verbose_name


class RefundOrder(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_refundOrders',
                              verbose_name='店铺订单', null=True)
    customer = models.ForeignKey('customer.Customer', to_field='openid', on_delete=models.CASCADE, verbose_name='顾客',
                                 null=True)
    order = models.ForeignKey('orders.Order', to_field='orderNum', on_delete=models.CASCADE, verbose_name='订单号')
    refundNum = models.CharField(max_length=50, verbose_name='退款编号', unique=True)
    refundType = models.CharField(max_length=20, verbose_name='退款类型')
    refund_fee = models.FloatField(verbose_name='退款金额', default=0)
    isDeleted = models.BooleanField(verbose_name='是否已删除', default=False)
    imgs = models.JSONField(verbose_name="附件", default=list)
    # 退款成功  #申请已撤销  #处理中
    status = models.CharField(max_length=10, verbose_name='退款状态', default='处理中')
    reason = models.CharField(max_length=100, verbose_name='退款原因', default='')
    detail = models.CharField(max_length=200, verbose_name='退款详述', default='')
    application_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间", null=True)
    refund_time = models.DateTimeField(auto_now=False, verbose_name="退款时间", null=True)

    def to_dict(self, fields=None, exclude=None):
        data = {}
        for f in self._meta.concrete_fields + self._meta.many_to_many:
            value = f.value_from_object(self)
            if fields and f.name not in fields:
                continue
            if exclude and f.name in exclude:
                continue
            if isinstance(f, ManyToManyField):
                value = [i.id for i in value] if self.pk else None
            if isinstance(f, DateTimeField):
                value = value.strftime('%Y-%m-%d %H:%M:%S') if value else None
            data[f.name] = value
        return data

    class Meta:
        db_table = 'tb_refund_order'
        ordering = ['-application_time']
        verbose_name = 'tb_refund_order'
        verbose_name_plural = verbose_name
