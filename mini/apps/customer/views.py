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
from django.forms.models import model_to_dict
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
        customer = json.loads(request.body)
        url = 'https://api.weixin.qq.com/sns/jscode2session?appid=' + \
              appid + '&secret=' + secret + '&js_code=' + js_code
        # 1.创建新的用户
        try:
            openid = requests.post(url).json()['openid']
            obj = Customer.objects.filter(openid=openid)
            pid = getpid(openid)
            userInfo = {}
            if obj.exists():
                obj.update(pid=pid)
                userInfo = {'phone': obj.first().phone}
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
        return http.JsonResponse({"code": RETCODE.OK, 'token': token})

    def get(self, request, pid):
        # 1.接受参数
        try:
            customer = Customer.objects.filter(pid=pid).first()
            res = dict()
            res['avatarUrl'] = customer.avatarUrl
            res['nickName'] = customer.nickName
            res['gender'] = customer.gender
            res['birthDay'] = customer.birthDay
            res['phone'] = customer.phone
            res['defaultAddress'] = customer.defaultAddress
            pid = getpid(customer.openid)
            customer.pid = pid
            customer.save()
            token = gettoken(pid, res)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'token': token})

    def put(self, request, pid, mode):
        customer = json.loads(request.body)
        try:
            if mode == 'addressList':
                defaultAddress = customer['addressList'][0]
                Customer.objects.filter(pid=pid).update(addressList=customer['addressList'], defaultAddress=defaultAddress)
            elif mode == 'nickName':
                Customer.objects.filter(pid=pid).update(nickName=customer['nickName'])
            elif mode == 'birthDay':
                Customer.objects.filter(pid=pid).update(birthDay=customer['birthDay'])
        except Exception as e:
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


class CustomerAddressView(View):
    def get(self, request, pid):
        try:
            customer = Customer.objects.filter(pid=pid).first()
            res = customer.addressList
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'addressList': res})
