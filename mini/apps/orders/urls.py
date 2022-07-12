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
    # 获取用户订单信息
    url(r'^getOrders/(?P<pid>.*)$', views.OrdersView.as_view()),

    # 删除订单
    url(r'^deleteOrder/(?P<orderNum>.*)$', views.OrdersView.as_view()),

    # 更新订单信息
    url(r'^updateOrder/(?P<orderNum>.*)/(?P<mode>.*)$', views.OrdersView.as_view()),

    # 添加售后订单
    url(r'^addRefundOrder/(?P<pid>.*)/(?P<appid>.*)/(?P<orderNum>.*)$', views.RefundOrderView.as_view()),

    # 获取售后订单信息
    url(r'^getRefundOrders/(?P<pid>.*)$', views.RefundOrderView.as_view()),

    # 更新售后订单
    url(r'^updateRefundOrders/(?P<refundNum>.*)/(?P<mode>.*)$', views.RefundOrderView.as_view()),

    # 删除售后订单
    url(r'^deleteRefundOrder/(?P<refundNum>.*)$', views.RefundOrderView.as_view()),

]
