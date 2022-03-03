#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: urls.py
@time: 2021/7/26 11:45
@desc:
'''

from django.conf.urls import url

from . import views

urlpatterns = [
    # 预览
    url(r'^pagePreview/(?P<pid>.*)$', views.PageView.as_view(), name='preview'),
    url(r'^getValue/(?P<pid>.*)$',views.PageView.as_view()),

    # 店铺页面详情
    url(r'^getDetail/(?P<pid>.*)/(?P<store_id>.*)$',views.DetailView.as_view()),
    url(r'^updateDetail/(?P<pid>.*)/(?P<store_id>.*)$',views.DetailView.as_view()),

    # 店铺
    url(r'^createStore/(?P<pid>.*)$', views.StoreView.as_view()),
    url(r'^updateStore/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreView.as_view()),
    url(r'^deleteStore/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreView.as_view()),
    url(r'^getStore/(?P<pid>.*)$', views.StoreView.as_view()),

    #默认店铺
    url(r'^defaultStore/(?P<pid>.*)$', views.DefaultStore.as_view()),
    #页面信息
    url(r'^getPage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$',views.PageView.as_view()),
    url(r'^createPage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$',views.PageView.as_view()),
    url(r'^updatePage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$',views.PageView.as_view()),
    url(r'^deletePage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$',views.PageView.as_view()),
    ]
