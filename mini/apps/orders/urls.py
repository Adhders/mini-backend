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
    # 添加订单
    url(r'^addOrder/(?P<pid>.*)/(?P<store_id>.*)$', views.OrdersView.as_view(), name='goods'),

    # 获取订单信息
    url(r'^getOrders/(?P<pid>.*)$', views.OrdersView.as_view()),

    # 获取订单状态信息
    url(r'^getOrderState/(?P<pid>.*)$', views.OrdersInfoView.as_view()),

    # 删除订单
    url(r'^deleteOrder/(?P<orderNum>.*)$', views.OrdersView.as_view()),


    # 更新订单信息
    url(r'^updateOrder/(?P<orderNum>.*)/(?P<mode>.*)$', views.OrdersView.as_view()),

]
