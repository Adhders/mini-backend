from django.shortcuts import render
# Create your views here.
import json
import time
import datetime
from django import http
from django.utils import timezone
from django.views import View
from store.models import Store
# from django.db.models import Q
from customer.models import Customer
from orders.models import Order, RefundOrder
from goods.views import GoodsReviewDefaultView
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
            total = orders['totalCost']*100
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
        return {"code": RETCODE.OK, "openid": customer.openid, 'total': total, 'orderNum': orderNum, 'description': description}

    def get(self, request, pid):
        # 1.接受参数
        try:
            res = []
            customer = Customer.objects.get(pid=pid)
            orderList = Order.objects.filter(isDeleted=False, customer=customer).all()
            for order in orderList:
                order_dict = order.to_dict()
                refundList = order.refundorder_set.values()
                if len(refundList) > 0:
                    order_dict['status'] = refundList[0]['status']
                order_dict['refundList'] = list(refundList)
                res.append(order_dict)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'orderList': list(res)})

    def delete(self, request, orderNum):
        try:
            Order.objects.filter(orderNum=orderNum).update(isDeleted=True)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, orderNum, mode):
        order = json.loads(request.body)
        try:
            if mode == 'status':
                Order.objects.filter(orderNum=orderNum).update(status=order['status'])
            elif mode == 'payment':

                Order.objects.filter(orderNum=orderNum).update(status=order['status'], payment_time=timezone.now())
            elif mode == 'paymentInfo':
                Order.objects.filter(orderNum=orderNum).update(paymentInfo=order['paymentInfo'])
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class OrdersInfoView(View):
    @classmethod
    def get(self, request, customer):
        # 1.接受参数
        #  1: "待支付", 2: '待发货', 3: '待收货' 4: '待评价' 5: '退款'
        orderState = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        try:
            orderList = Order.objects.filter(isDeleted=False, customer=customer)
            orderState[5] = RefundOrder.objects.filter(isDeleted=False, customer=customer, status='处理中').count()
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
                    try:
                        #只有未发起售后的订单可以进行评价
                        if len(order.refundorder_set.values()) == 0:
                            t1 = order.payment_time
                            t2 = datetime.datetime.now()
                            diff = (t2 - t1).days
                            # 超过两周未评价，自动评论
                            if diff > 14:
                                reviewState = order.reviewState
                                for (index, goods) in enumerate(order.goodsList):
                                    specs = '，'.join(map(lambda x: x['value'], goods['propertyList']))
                                    if reviewState[index]['count'] == 0:
                                        review_id = GoodsReviewDefaultView.post(request, specs, goods['id'], order,
                                                                                customer)
                                        reviewState[index] = {'count': 1, 'id': review_id}
                                order.reviewState = reviewState
                                order.status = '交易成功'
                                order.save()
                            else:
                                orderState[4] += 1
                    except Exception as e:
                        print(e)
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
            refundOrder = RefundOrder.objects.create(
                order=order,
                customer=customer,
                store=store,
                refundNum=refundNum,
                refundType=refundOrder['refundType'],
                refund_fee=refundOrder['refund_fee'],
                reason=refundOrder['reason'],
                detail=refundOrder['detail'],
                imgs=refundOrder['imgs']
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, "refundOrder": refundOrder.to_dict()})

    def get(self, request, pid):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            customer = Customer.objects.get(pid=pid)
            refundList = RefundOrder.objects.filter(isDeleted=False, customer=customer).all()
            res = []
            for refund in refundList:
                refund_dict = refund.to_dict(exclude=['id', 'isDeleted'])
                order = refund.order
                order_dict = order.to_dict(exclude=['id', 'status', 'paymentInfo', 'reviewState'])
                order_dict['refundList'] = list(
                    order.refundorder_set.filter(isDeleted=False).values('refundNum', 'refund_fee',
                                                                         'status'))  # 为了移动端判断是否可以再次申请售后
                refund_dict.update(order_dict)
                res.append(refund_dict)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'refundList': res})

    def put(self, request, refundNum, mode):
        data = json.loads(request.body)
        try:
            if mode == 'edit':
                RefundOrder.objects.filter(refundNum=refundNum).update(
                    refundType=data['refundType'],
                    refund_fee=data['refund_fee'],
                    reason=data['reason'],
                    detail=data['detail'],
                    imgs=data['imgs']
                )
            if mode == 'status':
                RefundOrder.objects.filter(refundNum=refundNum).update(status=data['status'])
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def delete(self, request, refundNum):
        try:
            RefundOrder.objects.filter(refundNum=refundNum).update(isDeleted=True)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})
