#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: urls.py
@time: 2021/12/23 18:04
@desc:
'''

from django.conf.urls import url

from . import views

urlpatterns = [
    # # 添加用户
    url(r'^customerLogin/(?P<appid>.*)/(?P<secret>.*)/(?P<js_code>.*)$', views.CustomerView.as_view(), name='customer'),

    #获取用户信息
    url(r'^queryUserInfo/(?P<pid>.*)$', views.CustomerView.as_view()),

    # 获取用户联系方式
    url(r'^getPhoneNumber/(?P<appid>.*)/(?P<secret>.*)/(?P<pid>.*)$', views.CustomerPhoneNumberView.as_view()),

    # 更新用户信息
    url(r'^updateCustomer/(?P<pid>.*)/(?P<mode>.*)$', views.CustomerView.as_view()),

    # 获取用户地址
    url(r'^getAddressList/(?P<pid>.*)$', views.CustomerAddressView.as_view()),
]
