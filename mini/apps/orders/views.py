from django.shortcuts import render
from django.views import View
# Create your views here.
import json
import time
import datetime
from django import http
from django.utils import timezone
from django.views import View
from store.models import Store
from customer.models import Customer
from .models import Order, RefundOrder
from goods.views import GoodsReviewDefaultView
# from django.core import serializers
from utils.response_code import RETCODE


class OrdersView(View):
    @classmethod
    def post(cls, request, appid, pid):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        orders = json.loads(request.body)
        # 1.创建新的商品对象
        try:
            store = Store.objects.get(appid=appid)
            customer = Customer.objects.get(pid=pid)
            orderNum = str(10000 + store.id) + str(int(time.time() * 100000))
            description = orders['goodsList'][0]['title']
            Order.objects.create(
                store=store,
                customer=customer,
                description=description,
                orderNum=str(orderNum),
                status=orders['status'],
                note=orders['note'],
                netCost=orders['netCost'],
                discount=orders['discount'],
                address=orders['address'],
                totalCost=orders['totalCost'],
                reviewState=[{'count': 0}] * len(orders['goodsList']),  # 评论状态:pp0代表尚未评论，1代表评论了一次,还可以追加一次
                shipping_fee=orders['shipping_fee'],
                goodsList=orders['goodsList'],
            )
        except Exception as e:
            return {"code": RETCODE.ORDERERR}
        # 4.响应
        return {"code": RETCODE.OK, "openid": customer.openid, 'orderNum': orderNum, 'description': description}

    def get(self, request, pid, mode):
        # 1.接受参数
        try:
            customer = Customer.objects.get(pid=pid)
            if mode: #获取可退款的订单
                now = datetime.datetime.now()
                start = now - datetime.timedelta(days=5)
                res = Order.objects.filter(customer=customer, payment_time__gt=start).values(
                    'status', 'orderNum', 'goodsList', 'netCost')
                print(res)
            else:
                res = Order.objects.filter(customer=customer).values(
                    'status', 'orderNum', 'goodsList', 'totalCost', 'address', 'discount', 'netCost', 'note',
                    'shipping_fee', 'reviewState', 'paymentInfo', 'create_time', 'payment_time')
            # orderList = serializers.serialize("json",res)
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'orderList': list(res)})

    def delete(self, request, orderNum):
        Order.objects.filter(orderNum=orderNum).delete()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, orderNum, mode):
        order = json.loads(request.body)
        if mode == 'status':
            Order.objects.filter(orderNum=orderNum).update(status=order['status'])
        elif mode == 'payment':
            Order.objects.filter(orderNum=orderNum).update(status=order['status'], payment_time=timezone.now())
        elif mode == 'paymentInfo':
            Order.objects.filter(orderNum=orderNum).update(paymentInfo=order['paymentInfo'])
        return http.JsonResponse({'code': RETCODE.OK})


class OrdersInfoView(View):
    @classmethod
    def get(self, request, customer):
        # 1.接受参数
        orderState = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        try:
            orderList = Order.objects.filter(customer=customer)
            num = RefundOrder.objects.filter(customer=customer, status='处理中').count()
            orderState[5] = num
            for order in orderList:
                if order.status == "待支付":
                    t1 = order.create_time
                    t2 = datetime.datetime.now()
                    diff = (t2 - t1).days
                    if diff != 0:
                        order.status = '交易关闭'
                        order.save()
                    orderState[1] += 1
                elif order.status == "待发货":
                    orderState[2] += 1
                elif order.status == "待收货":
                    orderState[3] += 1
                elif order.status == "待评价":
                    t1 = order.payment_time
                    t2 = datetime.datetime.now()
                    diff = (t2 - t1).days
                    # 超过两周未评价，自动评论
                    if diff > 14:
                        reviewState = order.reviewState
                        for (index, goods) in enumerate(order.goodsList):
                            specs = '，'.join(map(lambda x: x['value'], goods['propertyList']))
                            if reviewState[index]['count'] == 0:
                                review_id = GoodsReviewDefaultView.post(request, specs, goods['id'], order, customer)
                                reviewState[index] = {'count': 1, 'id': review_id}
                        order.reviewState = reviewState
                        order.status = '交易成功'
                        order.save()
                    else:
                        orderState[4] += 1
        except Exception as e:
            return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        return orderState


class RefundOrderView(View):
    def post(self, request, appid, pid, orderNum):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        # 1.创建新的退货服务单
        refundOrder = json.loads(request.body)
        try:
            store = Store.objects.get(appid=appid)
            customer = Customer.objects.get(pid=pid)
            order = Order.objects.get(orderNum=orderNum)
            refundNum = str(10000 + store.id) + str(int(time.time() * 100000))
            RefundOrder.objects.create(
                store=store,
                order=order,
                customer=customer,
                refundNum=refundNum,
                refundType=refundOrder['refundType'],
                refund_fee=refundOrder['refund_fee'],
            )
        except Exception as e:
            print('e', e)
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            customer = Customer.objects.get(pid=pid)
            refundList = RefundOrder.objects.filter(customer=customer)
            res = []
            for refundOrder in refundList:
                item = {'refundNum': refundOrder.refundNum, 'refund_fee': refundOrder.refund_fee,
                        'status': refundOrder.status, 'create_time': refundOrder.create_time,
                        'goodsList': refundOrder.order.goodsList, 'netCost': refundOrder.order.netCost}
                res.append(item)
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'refundList': res})


