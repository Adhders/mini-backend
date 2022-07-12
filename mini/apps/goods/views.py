import os

# Create your views here.
import re
import json
import time
from .uploader import Uploader
from django import http
from django.views import View
from django.utils import timezone
from django.shortcuts import HttpResponse, render
from .models import Goods, SPU, GoodsGroup, GoodsTag, GoodsProperty, GoodsReview
from store.models import Store
from customer.models import Customer
from orders.models import Order
from utils.response_code import RETCODE


# Create your views here.
def get_sku_spu(store, spu, sku):
    try:
        # 生成sku
        sku = sku if sku else 'P0000' + str(int(time.time()))
        spu_list = SPU.objects.filter(spu=spu)
        if spu_list.exists():
            spu = spu_list[0]
        else:
            spu = SPU.objects.create(store=store, spu=spu)
    except Exception as e:
        print(e)
    return spu, sku


class GoodsView(View):
    def post(self, request, pid, store_id):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        goods = json.loads(request.body)
        # 1.创建新的商品对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            # 获取spu, sku
            spu, sku = get_sku_spu(store, goods['spu'], goods['sku'])
            newGoods = Goods.objects.create(
                store=store,
                spu=spu,
                sku=sku,
                title=goods['title'],
                slogan=goods['slogan'],
                goodsType=goods['goodsType'],
                sellModelType=goods['sellModelType'],
                price=goods['price'],
                costPrice=goods['costPrice'],
                salesNum=goods['salesNum'],
                sortNum=goods['sortNum'],
                originalPrice=goods['originalPrice'],
                stock=goods['stock'],
                detail=goods['detail'],
                sellUnit=goods['sellUnit'],
                videoUrl=goods['videoUrl'],
                videoImage=goods['videoImage'],
                playTime=goods['playTime'],
                goodsImageUrls=goods['goodsImageUrls'],
                defaultImageUrl=goods['defaultImageUrl'],
                goodsLimitVo=goods['goodsLimitVo'],
                selectedTag=goods['selectedTag'],
                selectedClassifyList=goods['selectedClassifyList'],
                selectedGoodsAttrList=goods['selectedGoodsAttrList'],
                selectedGoodsPropList=goods['selectedGoodsPropList'],
                selectedGoodsRightsList=goods['selectedGoodsRightsList'],
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, "id": newGoods.id, 'putAwayDate': newGoods.putAwayDate})

    def get(self, request, pid, store_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            goodsList = store.all_goods.all()
            res = []
            for goods in goodsList:
                obj = goods.to_dict()
                obj['spu'] = goods.spu.spu
                obj['spu_id'] = goods.spu.id
                res.append(obj)
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsList': res})

    def delete(self, request, pid, store_id):
        goods_id = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.all_goods.filter(id__in=goods_id).delete()
        except:
            http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})

    def put(self, request, pid, store_id, mode):
        goods = json.loads(request.body)
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            if mode == 'rank':
                store.all_goods.filter(id__in=goods['id']).update(sortNum=goods['sortNum'])
            elif mode == 'group':
                for good in goods:
                    store.all_goods.filter(id=good['id']).update(
                        selectedClassifyList=good['selectedClassifyList'])
            elif mode == 'status':
                store.all_goods.filter(id__in=goods['id']).update(isPutAway=goods['isPutAway'],
                                                                  update_time=timezone.now())
            elif mode == 'price':
                store.all_goods.filter(id=goods['id']).update(
                    price=goods['price'],
                    costPrice=goods['costPrice'],
                    salesNum=goods['salesNum'],
                    sortNum=goods['sortNum'],
                    originalPrice=goods['originalPrice'],
                    stock=goods['stock'],
                )
            else:
                # 更新spu, sku
                spu, sku = get_sku_spu(store, goods['spu'], goods['sku'])
                store.all_goods.filter(id=goods['id']).update(
                    spu=spu,
                    sku=sku,
                    title=goods['title'],
                    slogan=goods['slogan'],
                    goodsType=goods['goodsType'],
                    sellModelType=goods['sellModelType'],
                    price=goods['price'],
                    costPrice=goods['costPrice'],
                    salesNum=goods['salesNum'],
                    sortNum=goods['sortNum'],
                    originalPrice=goods['originalPrice'],
                    stock=goods['stock'],
                    sellUnit=goods['sellUnit'],
                    videoUrl=goods['videoUrl'],
                    playTime=goods['playTime'],
                    videoImage=goods['videoImage'],
                    goodsImageUrls=goods['goodsImageUrls'],
                    defaultImageUrl=goods['defaultImageUrl'],
                    goodsLimitVo=goods['goodsLimitVo'],
                    selectedTag=goods['selectedTag'],
                    detail=goods['detail'],
                    selectedClassifyList=goods['selectedClassifyList'],
                    selectedGoodsAttrList=goods['selectedGoodsAttrList'],
                    selectedGoodsPropList=goods['selectedGoodsPropList'],
                    selectedGoodsRightsList=goods['selectedGoodsRightsList'],
                    update_time=timezone.now()
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


# 用户购买商品后，更新商品库存
class updateGoodsStock(View):
    def put(self, request):
        data = json.loads(request.body)
        try:
            goods = Goods.objects.get(id=data['id'])
            realStock = goods.stock - data['buyNum']
            goods.stock = realStock if realStock > 0 else 0
            goods.save()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class GoodsDetailView(View):
    def get(self, request, spu_id):
        # 1.接受参数
        try:
            spu = SPU.objects.get(id=spu_id)
            goodsList = spu.all_skus.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsList': list(goodsList)})


class GoodsGroupView(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            goodsList = store.all_goods.values()
            group = store.goods_group
            if group.exists():
                res = group.first().group
                countSet = {}
                for goods in goodsList:
                    for groupName in goods['selectedClassifyList']:
                        if groupName in countSet:
                            countSet[groupName] += 1
                        else:
                            countSet[groupName] = 1
                for groupList in res:
                    for group in groupList['children']:
                        if group['name'] in countSet:
                            group['num'] = countSet[group['name']]
            else:
                res = [{
                    "id": 0,
                    "group": "system",
                    "activeNames": ['1'],
                    "name": "系统分组",
                    "status": False,
                    "children": [],
                }]
                GoodsGroup.objects.create(
                    store=store,
                    group=res,
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsGroup': res})

    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.goods_group.update(group=json.loads(request.body))
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class GoodsTagView(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            goodsList = store.all_goods.values()
            goodsTag = store.goods_tag
            if goodsTag.exists():
                res = goodsTag.first().tags
                countSet = {}
                for goods in goodsList:
                    for tag in goods['selectedTag']:
                        selectedTagName = tag['name']
                        if selectedTagName in countSet:
                            countSet[selectedTagName] += 1
                        else:
                            countSet[selectedTagName] = 1
                for tag in res:
                    if tag['name'] in countSet:
                        tag['num'] = countSet[tag['name']]
            else:
                res = []
                GoodsTag.objects.create(
                    store=store,
                    tags=res,
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsTag': res})

    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.goods_tag.update(tags=json.loads(request.body))
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class GoodsPropertyView(View):
    def get(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            goodsProperty = store.goods_property

            if goodsProperty.exists():
                res = goodsProperty.first().property
            else:
                res = []
                GoodsProperty.objects.create(
                    store=store,
                    property=res,
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'goodsProperty': res})

    def post(self, request, pid, store_id):
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            store.goods_property.update(property=json.loads(request.body))
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})


class GoodsReviewView(View):
    def post(self, request, spu_id, pid, orderNum, index):
        """
        :param request:
        :return:
        """
        # 1.接受参数
        goodsReview = json.loads(request.body)
        # 1.创建新的商品对象
        try:
            customer = Customer.objects.get(pid=pid)
            order = Order.objects.filter(orderNum=orderNum).first()
            obj = SPU.objects.filter(id=spu_id)
            spu = obj.first() if obj.exists() else None
            review = GoodsReview.objects.create(
                spu=spu,
                customer=customer,
                order=order,
                star=goodsReview['star'],
                name=goodsReview['name'],
                msg=goodsReview['msg'],
                specs=goodsReview['specs'],
                avatar=goodsReview['avatar'],
                imgs=goodsReview['imgs'],
                anonymous=goodsReview['anonymous'],
            )
            goodsReview['reviewState'][int(index)]['id'] = review.id
            order.reviewState = goodsReview['reviewState']
            res = filter(lambda x: x['count'] == 0, order.reviewState)
            if len(list(res)) == 0:
                order.status = '交易成功'
            order.save()
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK, 'reviewState': goodsReview['reviewState']})

    def get(self, request, spu_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            spu = SPU.objects.get(id=spu_id)
            res = spu.all_reviews.values()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'reviewList': list(res)})

    def put(self, request, id, mode):
        reviews = json.loads(request.body)
        try:
            if mode == 'likes':
                GoodsReview.objects.filter(id=id).update(likes=reviews['likes'])
            elif mode == 'reply':
                GoodsReview.objects.filter(id=id).update(likes=reviews['likes'], children=reviews['children'])
            elif mode == 'additional':
                goodsReview = GoodsReview.objects.filter(id=id).first()
                order = goodsReview.order
                order.reviewState = reviews['reviewState']
                goodsReview.additional = {'msg': reviews['msg'], 'imgs': reviews['imgs'],
                                          'date': str(timezone.now())}
                order.save()
                goodsReview.save()
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class GoodsDetailUploadView(View):
    def get(self, request):
        result = {}
        action = request.GET["action"]
        # 解析JSON格式的配置文件
        with open('static/config.json') as fp:
            try:
                # 删除 `/**/` 之间的注释
                CONFIG = json.load(fp)
            except:
                CONFIG = {}
        if action == 'config':
            # 初始化时，返回配置文件给客户端
            result = CONFIG

        elif action in ('uploadimage', 'uploadfile', 'uploadvideo'):
            # 图片、文件、视频上传
            if action == 'uploadimage':
                fieldName = CONFIG.get('imageFieldName')
                config = {
                    "pathFormat": CONFIG['imagePathFormat'],
                    "maxSize": CONFIG['imageMaxSize'],
                    "allowFiles": CONFIG['imageAllowFiles']
                }
            elif action == 'uploadvideo':
                fieldName = CONFIG.get('videoFieldName')
                config = {
                    "pathFormat": CONFIG['videoPathFormat'],
                    "maxSize": CONFIG['videoMaxSize'],
                    "allowFiles": CONFIG['videoAllowFiles']
                }
            else:
                fieldName = CONFIG.get('fileFieldName')
                config = {
                    "pathFormat": CONFIG['filePathFormat'],
                    "maxSize": CONFIG['fileMaxSize'],
                    "allowFiles": CONFIG['fileAllowFiles']
                }

            if fieldName in request.FILES:
                field = request.FILES[fieldName]
                uploader = Uploader(field, config, './')
                result = uploader.getFileInfo()
            else:
                result['state'] = '上传接口出错'

        elif action in ('uploadscrawl'):
            # 涂鸦上传
            fieldName = CONFIG.get('scrawlFieldName')
            config = {
                "pathFormat": CONFIG.get('scrawlPathFormat'),
                "maxSize": CONFIG.get('scrawlMaxSize'),
                "allowFiles": CONFIG.get('scrawlAllowFiles'),
                "oriName": "scrawl.png"
            }
            if fieldName in request.form:
                field = request.form[fieldName]
                uploader = Uploader(field, config, './', 'base64')
                result = uploader.getFileInfo()
            else:
                result['state'] = '上传接口出错'

        elif action in ('catchimage'):
            config = {
                "pathFormat": CONFIG['catcherPathFormat'],
                "maxSize": CONFIG['catcherMaxSize'],
                "allowFiles": CONFIG['catcherAllowFiles'],
                "oriName": "remote.png"
            }
            fieldName = CONFIG['catcherFieldName']
            source = []
            if fieldName in request.form:
                # 这里比较奇怪，远程抓图提交的表单名称不是这个
                source = []
            elif '%s[]' % fieldName in request.form:
                # 而是这个
                source = request.form.getlist('%s[]' % fieldName)

            _list = []
            for imgurl in source:
                uploader = Uploader(imgurl, config, './', 'remote')
                info = uploader.getFileInfo()
                _list.append({
                    'state': info['state'],
                    'url': info['url'],
                    'original': info['original'],
                    'source': imgurl,
                })

            result['state'] = 'SUCCESS' if len(_list) > 0 else 'ERROR'
            result['list'] = _list

        else:
            result['state'] = '请求地址出错'

        if 'callback' in request.GET:
            callback = request.GET.get('callback')
            if re.match(r'^[\w_]+$', callback):
                obj = HttpResponse('%s(%s)' % (callback, json.dumps(result)))
                obj['Access-Control-Allow-Origin'] = '*'
                return obj
            return http.JsonResponse({'state': 'callback参数不合法'})
        return http.JsonResponse(result)


class GoodsDetailVideoView(View):
    def get(self, request):
        return render(request, "video.html")


class GoodsReviewDefaultView(View):
    @classmethod
    def post(cls, request, specs, spu_id, order, customer):
        """
        :param request:
        :return:
        """
        try:
            spu = SPU.objects.get(id=spu_id)
            review = GoodsReview.objects.create(
                spu=spu,
                customer=customer,
                order=order,
                specs=specs,
                name=customer.nickName,
                msg='顾客未及时做出评价，系统默认好评',
                avatar=customer.avatarUrl,
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return review.id
