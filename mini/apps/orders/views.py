from django.shortcuts import render
from django.views import View
# Create your views here.
import json
import time
from django import http
from django.views import View
from store.models import Store
from customer.models import Customer
from .models import Order
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
                shipping_fee=orders['shipping_fee'],
                goodsList=orders['goodsList'],
            )
        except Exception as e:
            return {"code": RETCODE.ORDERERR}
        # 4.响应
        return {"code": RETCODE.OK, "openid": customer.openid, 'orderNum': orderNum, 'description': description}

    def get(self, request, pid):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            customer = Customer.objects.get(pid=pid)
            res = Order.objects.filter(customer=customer).values(
                'status', 'orderNum', 'goodsList', 'totalCost', 'address', 'discount', 'netCost', 'note',
                'shipping_fee', 'paymentInfo')
            # orderList = serializers.serialize("json",res)
            # print('res', orderList)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'orderList': list(res)})

    def delete(self, request, orderNum):
        Order.objects.filter(orderNum=orderNum).delete()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, orderNum, mode):
        order = json.loads(request.body)
        if mode == 'status':
            Order.objects.filter(orderNum=orderNum).update(status=order['status'])
        if mode == 'paymentInfo':
            Order.objects.filter(orderNum=orderNum).update(paymentInfo=order['paymentInfo'])
        return http.JsonResponse({'code': RETCODE.OK})


class OrdersInfoView(View):
    def get(self, request, pid):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            customer = Customer.objects.get(pid=pid)
            orderList = Order.objects.filter(customer=customer)
            orderState = {1: 0, 2: 0, 3: 0, 4: 0}
            for order in orderList:
                if order.status == "待支付":
                    orderState[1] += 1
                elif order.status == "待发货":
                    orderState[2] += 1
                elif order.status == "待收货":
                    orderState[3] += 1
                elif order.status == "待评价":
                    orderState[4] += 1
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'orderState': orderState})

# class RefundView(View):
#     def post(self, request, orderNum):
#         """
#         :param request:
#         :return:
#         """
#         # 1.接受参数
#         # 1.创建新的商品对象
#         try:
#             order = Order.objects.get(orderNum=orderNum)
#             refundNum = 10000 + order.store.id + int(time.time() * 1000)
#             RefundOrder.objects.create(
#                 store=order.store,
#                 customer=order.customer,
#                 orderNum=order.orderNum,
#                 refundNum=str(refundNum),
#                 status=order.status,
#                 goodsList=order.goodsList,
#             )
#         except Exception as e:
#             return http.HttpResponseForbidden()
#         # 4.响应
#         return http.JsonResponse({"code": RETCODE.OK})
#
#     def get(self, request, openid):
#         # 1.接受参数
#         # 1.创建新的图片对象
#         try:
#             customer = Customer.objects.get(openid=openid)
#             res = customer.RefundOrder_set.values()
#         except Exception as e:
#             return http.HttpResponseForbidden()
#         return http.JsonResponse({'code': RETCODE.OK, 'refundList': list(res)})
