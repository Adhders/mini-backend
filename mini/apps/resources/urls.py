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
    # 上传图片
    url(r'^uploadImage/(?P<pid>.*)/(?P<store_id>.*)$', views.ImageView.as_view(), name='image'),
    url(r'^uploadVideo/(?P<pid>.*)/(?P<store_id>.*)$', views.VideoView.as_view(), name='video'),
    url(r'^uploadAuthor/(?P<pid>.*)/(?P<store_id>.*)$', views.AuthorView.as_view(), name='author'),
    url(r'^uploadArticle/(?P<pid>.*)/(?P<store_id>.*)$', views.ArticleView.as_view(), name='article'),

    # 获取图片
    url(r'^queryImage/(?P<pid>.*)/(?P<store_id>.*)$', views.ImageView.as_view()),
    # 获取视频
    url(r'^queryVideo/(?P<pid>.*)/(?P<store_id>.*)$', views.VideoView.as_view()),
    # 获取作者
    url(r'^queryAuthor/(?P<pid>.*)/(?P<store_id>.*)$', views.AuthorView.as_view()),
    # 获取文章
    url(r'^queryArticle/(?P<pid>.*)/(?P<store_id>.*)$', views.ArticleView.as_view()),

    # 删除图像
    url(r'^deleteImage/(?P<pid>.*)/(?P<store_id>.*)/(?P<bucket_name>.*)$', views.ImageView.as_view()),
    # 删除视频
    url(r'^deleteVideo/(?P<pid>.*)/(?P<store_id>.*)/(?P<bucket_name>.*)$', views.VideoView.as_view()),
    # 删除作者
    url(r'^deleteAuthor/(?P<pid>.*)/(?P<store_id>.*)/(?P<authorId>.*)$', views.AuthorView.as_view()),
    # 删除文章
    url(r'^deleteArticle/(?P<pid>.*)/(?P<store_id>.*)$', views.ArticleView.as_view()),

    # 更新图像
    url(r'^updateImage/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.ImageView.as_view()),
    # 更新视频
    url(r'^updateVideo/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.VideoView.as_view()),
    # 更新文章
    url(r'^updateArticle/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.ArticleView.as_view()),
    # 更新作者
    url(r'^updateAuthor/(?P<pid>.*)/(?P<store_id>.*)/(?P<mode>.*)$', views.AuthorView.as_view()),

    # 获取图片分组
    url(r'^queryImageGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.ImageGroupView.as_view()),
    # 获取视频分组
    url(r'^queryVideoGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.VideoGroupView.as_view()),
    # 获取文章分组
    url(r'^queryArticleGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.ArticleGroupView.as_view()),
    url(r'^queryAuthor/(?P<pid>.*)/(?P<store_id>.*)$', views.AuthorView.as_view()),

    # 更新图片分组
    url(r'^updateImageGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.ImageGroupView.as_view()),
    # 更新视频分组
    url(r'^updateVideoGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.VideoGroupView.as_view()),
    # 更新文章分组
    url(r'^updateArticleGroup/(?P<pid>.*)/(?P<store_id>.*)$', views.ArticleGroupView.as_view()),

    # 获取上传token
    url(r'^upload/token/(?P<bucket_name>.*)$', views.GetToken.as_view()),
]
