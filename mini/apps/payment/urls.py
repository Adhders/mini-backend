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
    #native 支付
    url(r'^pay$', views.NativePay.as_view()),

    #小程序支付
    url(r'^pay_miniprog/(?P<appid>.*)/(?P<pid>.*)$', views.MiniProgPay.as_view()),

    url(r'^queryOrder_miniprog/(?P<orderNum>.*)$', views.MiniProgPay.as_view()),

    url(r'^refund_miniProg/(?P<orderNum>.*)$', views.MiniProgRefound.as_view()),

    url(r'^closeOrder_miniProg/(?P<orderNum>.*)$', views.MiniProgClose.as_view())
]
