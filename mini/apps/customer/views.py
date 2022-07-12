from django.shortcuts import render

# Create your views here.
import json
import os
import jwt
import requests
from django import http
from hashlib import blake2b
from django.views import View
from store.models import Store
from .models import Customer
from orders.views import OrdersInfoView
from utils.response_code import RETCODE
from datetime import datetime, timedelta, timezone


def getpid(openid):
    salt = os.urandom(blake2b.SALT_SIZE)
    h1 = blake2b(salt=salt, digest_size=20)
    h1.update(openid.encode())
    pid = h1.hexdigest()
    return pid


def gettoken(pid, userInfo):
    payload = {
        'exp': datetime.now(tz=timezone.utc) + timedelta(days=3),  # 令牌过期时间
        'pid': pid,
        'userInfo': userInfo
    }
    key = 'SECRET_KEY_mini'
    token = jwt.encode(payload, key, algorithm='HS256')
    return token


class CustomerView(View):
    def post(self, request, appid, secret, js_code):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + \
              appid + '&secret=' + secret + '&js_code=' + js_code
        # 1.创建新的用户
        try:
            openid = requests.post(url).json()['openid']
            customer = Customer.objects.filter(openid=openid)
            pid = getpid(openid)
            userInfo = {'phone': '', 'defaultAddress': ''}
            reviewLikes = []
            orderState = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
            if customer.exists():
                userInfo['phone'] = customer.first().phone
                userInfo['defaultAddress'] = customer.first().defaultAddress
                reviewLikes = customer.first().reviewLikes
                orderState = OrdersInfoView.get(request, customer.first())
                customer.update(pid=pid)
            else:
                store = Store.objects.get(appid=appid)
                Customer.objects.create(
                    store=store,
                    openid=openid,
                    pid=pid,
                    gender=customer['gender'],
                    nickName=customer['nickName'],
                    avatarUrl=customer['avatarUrl']
                )
            token = gettoken(pid, userInfo)
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'token': token, 'orderState': orderState, 'reviewLikes': reviewLikes})

    def get(self, request, pid):
        # 1.接受参数
        try:
            customer = Customer.objects.filter(pid=pid).first()
            orderState = OrdersInfoView.get(request, customer)
            res = dict()
            res['avatarUrl'] = customer.avatarUrl
            res['defaultAddress'] = customer.defaultAddress
            res['nickName'] = customer.nickName
            res['gender'] = customer.gender
            res['birthDay'] = customer.birthDay
            res['phone'] = customer.phone
            reviewLikes = customer.reviewLikes
            pid = getpid(customer.openid)
            customer.pid = pid
            customer.save()
            token = gettoken(pid, res)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'token': token,
                                  'orderState': orderState, 'reviewLikes': reviewLikes})

    def put(self, request, pid, mode):
        data = json.loads(request.body)
        try:
            if mode == 'addressList':
                defaultList = list(filter(lambda x: x.get('default'), data['addressList']))
                defaultAddress = defaultList[0] if len(defaultList) != 0 else data['addressList'][0] if len(
                    data['addressList']) != 0 else ''
                Customer.objects.filter(pid=pid).update(addressList=data['addressList'], defaultAddress=defaultAddress)
            elif mode == 'nickName':
                Customer.objects.filter(pid=pid).update(nickName=data['nickName'])
            elif mode == 'birthDay':
                Customer.objects.filter(pid=pid).update(birthDay=data['birthDay'])
            elif mode == 'likes':
                Customer.objects.filter(pid=pid).update(likes=data['likes'])
            elif mode == 'reviewLikes':
                customer = Customer.objects.filter(pid=pid).first()
                customer.reviewLikes.append(data['reviewLikes'])
                customer.save()
            elif mode == 'addCart':
                customer = Customer.objects.get(pid=pid)
                # customer.cart.append(data['newGoods'])
                newGoods = data['newGoods']
                IDs = list(map(lambda x: x['id'], customer.cart))
                if newGoods['id'] in IDs:
                    index = IDs.index(newGoods['id'])
                    customer.cart[index]['buyNum'] += newGoods['buyNum']
                else:
                    customer.cart.append(newGoods)
                customer.save()
            elif mode == 'updateCart':
                Customer.objects.filter(pid=pid).update(cart=data['cart'])
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class CustomerPhoneNumberView(View):
    def post(self, request, appid, secret, pid):
        try:
            url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=' + appid + '&secret=' + secret
            response = requests.get(url).json()
            access_token = response['access_token']
            url = 'https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token=' + access_token
            data = request.body
            res = requests.post(url, data).json()
            phone = res['phone_info']['phoneNumber']
            Customer.objects.filter(pid=pid).update(phone=phone)
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'phone': phone})


# 用户地址
class CustomerAddressView(View):
    def get(self, request, pid):
        try:
            customer = Customer.objects.filter(pid=pid).first()
            res = customer.addressList
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'addressList': res})


# 用户购物车
class CustomerCartView(View):
    def get(self, request, appid, pid):
        try:
            customer = Customer.objects.filter(pid=pid).first()
            store = Store.objects.get(appid=appid)
            goodsList = store.all_goods.values()
            cart = customer.cart
            for element in cart:
                for goods in goodsList:
                    if element['id'] == goods['id']:
                        element['invalid'] = goods['stock'] == 0
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'cart': cart})
