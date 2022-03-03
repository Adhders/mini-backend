import json
import os
import uuid
import qrcode
from django import http
from django.conf import settings
from django.views import View
from django_redis import get_redis_connection
from users.models import User
from utils import constants
from django.forms.models import model_to_dict
from utils.response_code import RETCODE
from .models import Store, Detail


class StoreView(View):
    """创建店铺"""

    def post(self, request, pid):
        # 1.接受参数
        store = json.loads(request.body)
        # 1.创建新的图片对象
        try:
            user = User.objects.get(pid=pid)
            new_store = Store(
                pid=user,
                storename=store['storename'],
                trademark=store['trademark'],
                product_name=store['product_name'],
                version=store['version'],
                address=store['address'],
                telephone=store['telephone'],
                mobile=user.mobile if store['mobile'] == '' else store['mobile'],
                mail=user.mail if store['mail'] == '' else store['mail'],
                name=user.name if store['name'] == '' else store['name'],
                wechat=user.wechat if store['wechat'] == '' else store['wechat'],
                industry=store['industry'],
                introduce=store['introduce']
            )
            new_store.save()
            user.store = new_store
            user.save()
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'store_id': new_store.id})

    def put(self, request, pid, store_id):
        # 1.接受参数
        store = json.loads(request.body)
        # 1.创建新的图片对象
        try:
            user = User.objects.get(pid=pid)
            Store.objects.filter(id=store_id).update(
                storename=store['storename'],
                trademark=store['trademark'],
                address=store['address'],
                telephone=store['telephone'],
                mobile=user.mobile if store['mobile'] == '' else store['mobile'],
                mail=user.mail if store['mail'] == '' else store['mail'],
                name=user.name if store['name'] == '' else store['name'],
                wechat=user.wechat if store['wechat'] == '' else store['wechat'],
                industry=store['industry'],
                introduce=store['introduce']
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid):
        try:
            user = User.objects.get(pid=pid)
            stores = user.all_store.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, "store_list": list(stores)})

    def delete(self, request, pid, store_id):
        try:
            Store.objects.filter(id=store_id).delete()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK})


class DefaultStore(View):
    def get(self, request, pid):
        try:
            user = User.objects.filter(pid=pid).first()
            if not user:
                return http.JsonResponse({"code": RETCODE.INVALIDUSERERR, "msg": "用户不存在"})
            store = user.store
            if not store:
                return http.JsonResponse({"code": RETCODE.STOREERR,"msg": "店铺不存在"})
        except Exception as e:
            print(e)
            return http.JsonResponse({"code": RETCODE.STOREERR})
        return http.JsonResponse({"code": RETCODE.OK, "default_store": model_to_dict(store)})

    def put(self, request, pid):
        # 1.接受参数
        store = json.loads(request.body)
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(id=store['id'])
            User.objects.filter(pid=pid).update(store=store)
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


# Create your views here.
class PageView(View):
    """添加页面"""

    def post(self, request, pid):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        try:
            con = get_redis_connection('preview')
            con.setex("data_%s" % pid, constants.PREVIEW_DATA_EXPIRES, request.body)
            url = 'http://localhost:8080/saas/preview?userId=%s' % pid
            img = qrcode.make(url)
            uid = str(uuid.uuid1())
            suid = ''.join(uid.split('-'))
            file_url = os.path.join(settings.BASE_DIR, 'static/images/%s.png' % suid)
            img_url = 'http://localhost:8000/static/images/%s.png' % suid
            with open(file_url, 'wb') as f:
                img.save(f)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, "url": img_url})

    def get(self, request, pid):
        try:
            con = get_redis_connection('preview')
            data = con.get("data_%s" % pid).decode()

        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, 'pageInfo': json.loads(data)})


class DetailView(View):
    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            data = json.loads(request.body.decode())
            # print('data',data)
            store.detail_info.update(
                detail=data['detail'],
                pages=data['pages'],
                tabbar=data['tabbar']
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
        
            detail = store.detail_info
            if detail.exists():
                res = detail.first().detail
                pages = detail.first().pages
                tabbar = detail.first().tabbar
            else:
                res = [{
                    "index": 0,
                    "title": "默认分组",
                    "children": [
                        {
                            'pageIndex': 0,
                            'itemGroupIndex': 0,
                            'style': {
                                'isEmbedding': False,
                                'isBack': True,
                                'iconClass': '',
                                'searchBoxStyle': 0,
                                'iconColor': '#fa392d',
                                'colorStyle': 0,
                                'color': '#000000',
                                'backgroundColor': '#FFFFFF'},
                            'title': "首页",
                            'arrList': []
                        }]
                }]
                pages = ['首页']
                tabbar = {'style': {'activeColor': '#fa392d', 'inactiveColor': '#b2b1af'}, 'iconList': []}
                Detail.objects.create(
                    store=store,
                    detail=res,
                    pages=pages,
                    tabbar=tabbar
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({"code": RETCODE.OK, 'detail': res, 'pages': pages, 'tabbar': tabbar})
