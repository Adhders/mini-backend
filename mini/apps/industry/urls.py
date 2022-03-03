from django.conf.urls import url

from . import views

urlpatterns = [
    # 省市区数据查询
    url(r'^industry/$', views.IndustryView.as_view(), name='industry'),
]
