from django.db import models


# Create your models here.
class Order(models.Model):
    orderNum = models.CharField(max_length=20, verbose_name='订单编号', unique=True)
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_orders', verbose_name='店铺订单')
    customer = models.ForeignKey('customer.Customer', to_field='openid', on_delete=models.CASCADE, verbose_name='顾客')
    status = models.CharField(max_length=10, verbose_name='订单状态')
    note = models.CharField(max_length=250, verbose_name='留言', null=True)
    description = models.CharField(max_length=125, verbose_name='描述', null=True)
    totalCost = models.FloatField(verbose_name='总价', default=0.00)
    netCost = models.FloatField(verbose_name="实付", default=0.00)
    discount = models.FloatField(verbose_name="优惠", default=0.00)
    shipping_fee = models.FloatField(verbose_name='邮费', default=0.00)
    paymentInfo = models.JSONField(verbose_name="支付信息", null=True)
    reviewState = models.JSONField(verbose_name="评论状态", null=True)
    goodsList = models.JSONField(verbose_name="商品列表", null=True)
    address = models.JSONField(verbose_name="邮寄地址", null=True)
    payment_time = models.DateTimeField(auto_now=False, null=True, verbose_name="支付时间")
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'tb_order'
        ordering = ['-create_time']
        verbose_name = 'tb_order'
        verbose_name_plural = verbose_name


class RefundOrder(models.Model):
    store = models.ForeignKey('store.Store', on_delete=models.CASCADE, related_name='all_refundOrders', verbose_name='店铺订单', null=True)
    customer = models.ForeignKey('customer.Customer', to_field='openid', on_delete=models.CASCADE, verbose_name='顾客', null=True)
    order = models.ForeignKey('orders.Order', to_field='orderNum', on_delete=models.CASCADE, verbose_name='订单号')
    refundNum = models.CharField(max_length=20, verbose_name='退款编号', unique=True)
    refundType = models.CharField(max_length=20, verbose_name='退款类型')
    refund_fee = models.FloatField(verbose_name='退款金额', default=0)
    imgs = models.JSONField(verbose_name="附件", null=True)
    # 退款成功  #申请已撤销  #处理中
    status = models.CharField(max_length=10, verbose_name='退款状态', default='处理中')
    reason = models.CharField(max_length=100, verbose_name='退款原因', default='')
    description = models.CharField(max_length=200, verbose_name='退款详述', default='')
    create_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="创建时间", null=True)

    class Meta:
        db_table = 'tb_refund_order'
        ordering = ['-create_time']
        verbose_name = 'tb_refund_order'
        verbose_name_plural = verbose_name
