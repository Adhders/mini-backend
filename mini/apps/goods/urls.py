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
    # 上传商品
    url(r'^uploadGoods/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsView.as_view(), name='goods'),
    url(r'^uploadGoodsGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsGroupView.as_view()),
    url(r'^uploadGoodsTag/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsTagView.as_view()),
    url(r'^uploadGoodsProperty/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsPropertyView.as_view()),

    # 获取商品
    url(r'^queryGoods/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsView.as_view()),
    url(r'^queryGoodsGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsGroupView.as_view()),
    url(r'^queryGoodsTag/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsTagView.as_view()),
    url(r'^queryGoodsProperty/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsPropertyView.as_view()),

    # 删除商品
    url(r'^deleteGoods/(?P<pid>.*)/(?P<store_id>.*)$', views.GoodsView.as_view()),

    # 更新商品
    url(r'^updateGoods/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.GoodsView.as_view()),

    # 获取评论
    url(r'getGoodsReview/(?P<spu_id>.*)$', views.GoodsReviewView.as_view()),
    # 添加评论
    url(r'^addGoodsReview/(?P<spu_id>.*)$', views.GoodsReviewView.as_view()),

    # 更新评论
    url(r'^updateGoodsReview/(?P<id>.*)/(?P<mode>.*)$', views.GoodsReviewView.as_view()),

]
