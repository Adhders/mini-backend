from django.db import models


# Create your models here.

class Shipment(models.Model):
    orderNum = models.ForeignKey('orders.Order', to_field='orderNum', on_delete=models.CASCADE, verbose_name='订单号')
    tracking_number = models.CharField(max_length=20, verbose_name='快递单号', unique=True, null=True)
    mailing_method = models.CharField(max_length=10, verbose_name="邮寄方式", default="免邮")
    message = models.JSONField(verbose_name="快递信息", null=True)
    delivery_time = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="发货时间")
    receiving_time = models.DateTimeField(null=False, verbose_name="收货时间")

    class Meta:
        db_table = 'tb_shipment'
        verbose_name = 'tb_shipment'
        verbose_name_plural = verbose_name

