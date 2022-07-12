
from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # url(r'^search/', include('haystack.urls')),  # 搜索模块
    url(r'^', include(('users.urls', 'users'), namespace='users')),  # 用户模块
    url(r'^', include(('resources.urls', 'resources'), namespace='resources')),  # 资源模块
    url(r'^', include(('store.urls', 'store'), namespace='store')),  # 店铺模块
    # url(r'^', include(('contents.urls','contents'), namespace='contents')),  # 首页模块
    # url(r'^', include(('oauth.urls','oauth'), namespace='oauth')),  # QQ模块
    url(r'^', include(('customer.urls', 'customer'), namespace='customer')),
    url(r'^', include(('orders.urls', 'orders'), namespace='orders')),
    url(r'^', include(('dataCenter.urls', 'dataCenter'), namespace='dataCenter')),
    url(r'^', include(('goods.urls', 'goods'), namespace='goods')),  # 商品模块
    url(r'^', include(('message.urls', 'message'), namespace='message')),
    # url(r'^', include(('carts.urls','carts'), namespace='carts')),  # 购物车模块
    url(r'^', include(('payment.urls', 'payment'), namespace='payment')),  # 支付模块

]
