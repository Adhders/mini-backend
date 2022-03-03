#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: UserMiddleware.py
@time: 2021/10/24 21:34
@desc:
'''
import jwt
import re
from jwt import exceptions
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse


class LoginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # print('path', request.META['PATH_INFO'])
        request_path = request.META['PATH_INFO']
        token = request.META.get("HTTP_AUTHORIZATION")
        # print('token', token)
        key = 'SECRET_KEY_mini'
        if token:
            try:
                jwt.decode(token, key, algorithms=['HS256'])
            except (exceptions.ExpiredSignatureError, jwt.DecodeError) as e:
                # 参考https://www.zhangshengrong.com/p/9MNloW5naJ/
                obj = HttpResponse('Unauthorized', status=401)
                obj['Access-Control-Allow-Origin'] = '*'
                return obj
        # elif not re.match('^/user_|^/customer|^/getGoods', request_path):
        #     obj = HttpResponse('Unauthorized', status=401)
        #     obj['Access-Control-Allow-Origin'] = '*'
        #     return obj


