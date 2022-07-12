import json
import os
import uuid
import qrcode
import datetime
import requests
from django import http
from django.conf import settings
from django.views import View
from django_redis import get_redis_connection
from users.models import User
from orders.models import Order, RefundOrder
from customer.models import Customer
from goods.models import Goods
from utils import constants
from django.forms.models import model_to_dict
from utils.response_code import RETCODE
from django.shortcuts import HttpResponse, render
from .models import Store, Detail, StoreSetting


class StoreView(View):
    """创建店铺"""

    def post(self, request, pid):
        # 1.接受参数
        store = json.loads(request.body)
        # 1.创建新的图片对象
        try:
            user = User.objects.get(pid=pid)
            new_store = Store(
                pid=user,
                storename=store['storename'],
                trademark=store['trademark'],
                product_name=store['product_name'],
                version=store['version'],
                address=store['address'],
                telephone=store['telephone'],
                mobile=user.mobile if store['mobile'] == '' else store['mobile'],
                mail=user.mail if store['mail'] == '' else store['mail'],
                name=user.name if store['name'] == '' else store['name'],
                industry=store['industry'],
                introduce=store['introduce']
            )
            new_store.save()
            user.store = new_store
            user.save()
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'store_id': new_store.id})

    def put(self, request, pid, store_id):
        # 1.接受参数
        store = json.loads(request.body)
        # 1.创建新的图片对象
        try:
            user = User.objects.get(pid=pid)
            Store.objects.filter(id=store_id).update(
                storename=store['storename'],
                trademark=store['trademark'],
                address=store['address'],
                telephone=store['telephone'],
                mobile=user.mobile if store['mobile'] == '' else store['mobile'],
                mail=user.mail if store['mail'] == '' else store['mail'],
                name=user.name if store['name'] == '' else store['name'],
                industry=store['industry'],
                introduce=store['introduce']
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid):
        try:
            user = User.objects.get(pid=pid)
            stores = user.all_store.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, "store_list": list(stores)})

    def delete(self, request, pid, store_id):
        try:
            Store.objects.filter(id=store_id).delete()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK})


class DefaultStore(View):
    def get(self, request, pid):
        try:
            user = User.objects.filter(pid=pid).first()
            if not user:
                return http.JsonResponse({"code": RETCODE.INVALIDUSERERR, "msg": "用户不存在"})
            store = user.store
            if not store:
                return http.JsonResponse({"code": RETCODE.STOREERR, "msg": "店铺不存在"})
        except Exception as e:
            return http.JsonResponse({"code": RETCODE.STOREERR})
        return http.JsonResponse({"code": RETCODE.OK, "default_store": model_to_dict(store)})

    def put(self, request, pid):
        # 1.接受参数
        store = json.loads(request.body)
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(id=store['id'])
            User.objects.filter(pid=pid).update(store=store)
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class SettingView(View):
    def put(self, request, pid, store_id, mode):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            data = json.loads(request.body)
            if mode == 'payment':
               store.store_setting.update(paymentSetting=data['paymentSetting'])
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id, mode):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            appid = store.appid
            res = {}
            store_setting = store.store_setting
            if store_setting.exists():
                setting = store_setting.first()
                if mode == 'payment':
                    res['paymentSetting'] = setting.paymentSetting
            else:
                StoreSetting.objects.create(
                    store=store
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, 'appid': appid, "setting": res})

class UploadFile(View):
    """上传证书"""
    def post(self, request, appid):
        try:
            cert = request.FILES['file']
            filename = cert.name
            savePath = './static/path_to_key/' + appid
            if not os.path.exists(savePath):
                os.mkdir(savePath)
            path = os.path.join(savePath, filename)
            with open(path, 'wb+') as destination:
                for chunk in cert.chunks():
                    destination.write(chunk)
                destination.close()
            return http.JsonResponse({"code": RETCODE.OK, 'filePath': path})
        except Exception as e:
            return http.HttpResponseForbidden()

# Create your views here.
class PageView(View):
    """添加页面"""
    def post(self, request, store_id):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        try:
            con = get_redis_connection('preview')
            store = Store.objects.get(id=store_id)
            appid = store.appid
            con.setex("data_%s" % appid, constants.PREVIEW_DATA_EXPIRES, request.body)
            url = 'http://192.168.1.40:8000/saas/preview/#/?appid=%s' % appid
            print('url', url)
            img = qrcode.make(url)
            uid = str(uuid.uuid1())
            suid = ''.join(uid.split('-'))
            file_url = os.path.join(settings.BASE_DIR, '../static/images/%s.png' % suid)
            img_url = 'http://localhost:8000/static/images/%s.png' % suid
            with open(file_url, 'wb') as f:
                img.save(f)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, "url": img_url})

    def get(self, request, appid):
        try:
            con = get_redis_connection('preview')
            data = con.get("data_%s" % appid).decode()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, 'pageInfo': json.loads(data)})

class Preview(View):
    def get(self, request):
        return render(request, "index.html")

class DetailView(View):

    def put(self, request, pid, store_id, mode):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            data = json.loads(request.body)
            if mode == 'detail':
                store.detail_info.update(
                    detail=data['detail'],
                    tabbar=data['tabbar'],
                )
            elif mode == 'pages':
                store.detail_info.update(
                    detail=data['detail']
                )
            else:
                store.detail_info.update(
                    labels=data['labels']
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            detail = store.detail_info
            if detail.exists():
                storeDetail = detail.first()
                res = storeDetail.detail
                tabBar = storeDetail.tabbar
                labels = storeDetail.labels
            else:
                res = [{
                    'id': 1,
                    "title": "默认分组",
                    "children": [
                        {
                            'id': 0,
                            'style': {
                                'isEmbedding': False,
                                'isBack': True,
                                'iconClass': '',
                                'searchBoxStyle': 0,
                                'iconColor': '#fa392d',
                                'colorStyle': 0,
                                'color': '#000000',
                                'backgroundColor': '#FFFFFF'},
                            'title': "首页",
                            'arrList': [],
                            'labels': ["全部标签"],
                            'status': '未发布',
                        }]
                }]
                tabBar = {'color': '#666666', 'selectedColor': '#EB0909', 'backgroundColor': '#fff', 'list': []}
                labels = []
                Detail.objects.create(
                    store=store,
                    detail=res,
                    tabbar=tabBar,
                    labels=labels
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, 'detail': res, 'tabBar': tabBar, 'labels': labels})


class StoreDetailView(View):
    def get(self, request, appid):
        try:
            store = Store.objects.get(appid=appid)
            detail = store.detail_info
            pages = []
            tabBar = []
            if detail.exists():
                storeDetail = detail.first()
                detail = storeDetail.detail
                for page in detail:
                    pages.extend(page['children'])
                pages = list(filter(lambda x: x["status"] == "已发布", pages))
                tabBar = storeDetail.tabbar
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, 'pages': pages, 'tabBar': tabBar})


class StoreInfoView(View):
    def get(self, request, appid):

        state = {'pendingPay': 0, 'pendingDelivery': 0, 'refundOrder': 0, 'onSales': 0, 'putAway': 0, 'orderNum': 0,
                 'receipt': 0}
        try:
            store = Store.objects.get(appid=appid)
            storeInfo = {'appid': store.appid, 'mchId': store.mch_id, 'storename': store.storename,
                         'address': store.address, 'introduce': store.introduce, 'trademark': store.trademark}
            orderList = Order.objects.filter(store=store)
            for order in orderList:
                t1 = order.create_time
                t2 = datetime.datetime.now()
                diff = (t2 - t1).days
                if diff <= 1:
                    state['orderNum'] += 1
                    state['receipt'] += order.netCost
                if order.status == "代付款":
                    state['pendingPay'] += 1
                if order.status == "代发货":
                    state["pendingDelivery"] += 1
            state['refundOrder'] = RefundOrder.objects.filter(store=store, status="处理中").count()
            state['onSales'] = Goods.objects.filter(store=store, isPutAway=1).count()
            state['putAway'] = Goods.objects.filter(store=store, isPutAway=0).count()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'state': state, 'storeInfo': storeInfo})


class StoreStaticData(View):
    def get(self, request, pid, store_id):
        state = {'pendingPay': 0, 'pendingDelivery': 0, 'refundOrder': 0, 'sellout': 0}
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            orderList = Order.objects.filter(store=store)
            for order in orderList:
                if order.status == "代付款":
                    state['pendingPay'] += 1
                if order.status == "代发货":
                    state["pendingDelivery"] += 1
            state['refundOrder'] = RefundOrder.objects.filter(store=store, status="处理中").count()
            state['sellout'] = Goods.objects.filter(store=store, stock=0).count()
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'state': state})


class StoreStaticInfoView(View):
    def post(self, request, appid, secret):
        try:
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
            response = requests.get(url).json()
            access_token = response['access_token']
            url = 'https://api.weixin.qq.com/datacube/getweanalysisappiddailyvisittrend?access_token=' + access_token
            data = request.body
            res = requests.post(url, data).json()
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, "data": res})


class StoreOrderView(View):
    def get(self, request, appid):
        try:
            store = Store.objects.get(appid=appid)
            orderList = Order.objects.filter(store=store)
            res = []
            for order in orderList:
                item = {'id': order.id, 'status': order.status, 'orderNum': order.orderNum,
                        'goodsList': order.goodsList, 'totalCost': order.totalCost, 'discount': order.totalCost,
                        'netCost': order.netCost, 'note': order.note, 'shipping_fee': order.shipping_fee,
                        'create_time': order.create_time, 'payment_time': order.payment_time,
                        'address': order.address, 'nickName': order.customer.nickName,
                        'avatarUrl': order.customer.avatarUrl}
                res.append(item)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'orderList': res})


class StoreAllOrder(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            orderList = store.all_orders.all()
            res = []
            for order in orderList:
                item = {'id': order.id, 'status': order.status, 'orderNum': order.orderNum,
                        'goodsList': order.goodsList,
                        'totalCost': order.totalCost, 'discount': order.totalCost, 'netCost': order.netCost,
                        'note': order.note, 'shipping_fee': order.shipping_fee, 'create_time': order.create_time,
                        'payment_time': order.payment_time, 'address': order.address, 'openid': order.customer.openid,
                        'nickName': order.customer.nickName, 'avatarUrl': order.customer.avatarUrl}
                res.append(item)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'orderList': res})


class StoreCustomerView(View):
    def get(self, request, appid):
        try:
            store = Store.objects.get(appid=appid)
            res = store.all_customers.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'customerList': list(res)})


def orderInfo(obj, customer):
    for index, order in enumerate(Order.objects.filter(customer=customer)):
        if index == 0:
            obj['lastTime'] = order.create_time
        obj['orderNum'] += 1
        obj['overall'] += order.netCost
    obj['refundNum'] = RefundOrder.objects.filter(customer=customer).count()


class StoreCustomerDetail(View):
    def get(self, request, openid):
        try:
            res = {'orderNum': 0, 'refundNum': 0, 'overall': 0, 'lastTime': ''}
            customer = Customer.objects.get(openid=openid)
            orderInfo(res, customer)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'customerDetail': res})


class StoreAllCustomer(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            customerList = store.all_customers.all()
            res = []
            for customer in customerList:
                item = {
                    'id': customer.id,
                    'gender': customer.gender,
                    'phone': customer.phone,
                    'nickName': customer.nickName,
                    'avatarUrl': customer.avatarUrl,
                    'create_time': customer.create_time,
                    'birthDay': customer.create_time,
                    'channel': customer.channel,
                    'orderNum': 0, 'refundNum': 0, 'overall': 0, 'lastTime': '',
                }
                orderInfo(item, customer)
                res.append(item)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'customerList': res})


class StoreAllGoodsReview(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            spuList = store.all_spus.all()
            reviewList = []
            for spu in spuList:
                reviews = spu.all_reviews.values()
                reviewList.extend(list(reviews))
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'reviewList': reviewList})


class StoreCustomerOrderView(View):
    def get(self, request, openid):
        try:
            customer = Customer.objects.get(openid=openid)
            res = Order.objects.filter(customer=customer).values(
                'status', 'orderNum', 'goodsList', 'totalCost', 'address', 'discount', 'netCost', 'note',
                'shipping_fee', 'create_time', 'payment_time')
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'ordersList': list(res)})


class StoreCustomerRefundOrderView(View):
    def get(self, request, openid):
        try:
            customer = Customer.objects.get(openid=openid)
            refundList = RefundOrder.objects.filter(customer=customer)
            res = []
            for refund in refundList:
                refund_dict = refund.to_dict(exclude=['id', 'isDeleted'])
                order = refund.order
                order_dict = order.to_dict(exclude=['id', 'status', 'paymentInfo', 'reviewState'])
                refund_dict.update(order_dict)
                res.append(refund_dict)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'refundList': list(res)})


class StoreGoodsView(View):
    def get(self, request, appid):
        try:
            store = Store.objects.get(appid=appid)
            res = store.all_goods.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsList': list(res)})


class StoreGoodsGroupView(View):
    def get(self, request, appid):
        try:
            store = Store.objects.get(appid=appid)
            group = store.goods_group
            if group.exists():
                res = group.first().group
            else:
                res = [{
                    "group": "system",
                    "name": "系统分组",
                    "children": [],
                }]
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsGroup': res})


class StoreRefundOrderView(View):
    def get(self, request, appid):
        try:
            store = Store.objects.get(appid=appid)
            refundList = store.all_refundOrders.all()
            res = []
            for refund in refundList:
                refund_dict = refund.to_dict()
                order = refund.order
                order_dict = order.to_dict(exclude=['id', 'status', 'paymentInfo', 'reviewState'])
                refund_dict.update(order_dict)
                customer = refund.customer
                refund_dict.update({'nickName': customer.nickName, 'avatarUrl': customer.avatarUrl})
                res.append(refund_dict)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'refundList': list(res)})


class StoreAllRefundOrder(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            refundList = store.all_refundOrders.all()
            res = []
            for refund in refundList:
                refund_dict = refund.to_dict()
                order = refund.order
                order_dict = order.to_dict(exclude=['id', 'status', 'paymentInfo', 'reviewState'])
                refund_dict.update(order_dict)
                customer = refund.customer
                refund_dict.update({'nickName': customer.nickName, 'avatarUrl': customer.avatarUrl})
                res.append(refund_dict)
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'refundList': list(res)})
