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
    url(r'^pagePreview/(?P<store_id>.*)$', views.PageView.as_view(), name='preview'),
    url(r'^getValue/(?P<appid>.*)$', views.PageView.as_view()),
    url(r'^saas/preview/$', views.Preview.as_view()),

    # 店铺设置
    url(r'^updateStoreSetting/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.SettingView.as_view()),
    url(r'^getStoreSetting/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.SettingView.as_view()),
    url(r'^uploadCert/(?P<appid>.*)$', views.UploadFile.as_view()),
    # 店铺页面详情
    url(r'^getDetail/(?P<pid>.*)/(?P<store_id>.*)$', views.DetailView.as_view()),
    url(r'^updateDetail/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.DetailView.as_view()),

    # PC端店铺数据
    url(r'^getStore/(?P<pid>.*)$', views.StoreView.as_view()),
    url(r'^createStore/(?P<pid>.*)$', views.StoreView.as_view()),
    url(r'^updateStore/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreView.as_view()),
    url(r'^deleteStore/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreView.as_view()),
    url(r'^deleteStore/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreView.as_view()),
    url(r'^getStoreStaticData/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreStaticData.as_view()),
    url(r'^getStoreAllCustomer/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreAllCustomer.as_view()),
    url(r'^getStoreAllReviews/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreAllGoodsReview.as_view()),
    url(r'^getStoreAllOrder/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreAllOrder.as_view()),
    url(r'^getStoreAllRefundOrder/(?P<pid>.*)/(?P<store_id>.*)$', views.StoreAllRefundOrder.as_view()),


    # 移动端店铺数据
    url(r'^getStoreDetail/(?P<appid>.*)$', views.StoreDetailView.as_view()),
    url(r'^getStoreInfo/(?P<appid>.*)$', views.StoreInfoView.as_view()),
    url(r'^getStoreOrder/(?P<appid>.*)$', views.StoreOrderView.as_view()),
    url(r'^getStoreRefundOrder/(?P<appid>.*)$', views.StoreRefundOrderView.as_view()),
    url(r'^getStoreCustomer/(?P<appid>.*)$', views.StoreCustomerView.as_view()),
    url(r'^getCustomerDetail/(?P<openid>.*)$', views.StoreCustomerDetail.as_view()),
    url(r'^getCustomerOrder/(?P<openid>.*)$', views.StoreCustomerOrderView.as_view()),
    url(r'^getCustomerRefundOrder/(?P<openid>.*)$', views.StoreCustomerRefundOrderView.as_view()),
    url(r'^getStoreGoods/(?P<appid>.*)$', views.StoreGoodsView.as_view()),
    url(r'^getStoreGoodsGroup/(?P<appid>.*)$', views.StoreGoodsGroupView.as_view()),
    url(r'^getStoreStatic/(?P<appid>.*)/(?P<secret>.*)$', views.StoreStaticInfoView.as_view()),

    # 默认店铺
    url(r'^defaultStore/(?P<pid>.*)$', views.DefaultStore.as_view()),
    # 页面信息
    url(r'^getPage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$', views.PageView.as_view()),
    url(r'^createPage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$', views.PageView.as_view()),
    url(r'^updatePage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$', views.PageView.as_view()),
    url(r'^deletePage/(?P<pid>.*)/(?P<store_id>.*)/(?P<pageName>.*)$', views.PageView.as_view()),
]
