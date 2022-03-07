from django.shortcuts import render
from django.utils import timezone
# Create your views here.
import json
import time
from django import http
from django.views import View
from django.forms.models import model_to_dict
from .models import Goods, SPU, GoodsGroup, GoodsTag, GoodsProperty, GoodsReview
from store.models import Store
from customer.models import Customer
from orders.models import Order
from utils.response_code import RETCODE


# Create your views here.
def get_sku_spu(store, spu, sku):
    spu_list = store.all_spus.filter(spu=spu)
    count = spu_list.count()
    spu = SPU.objects.create(store=store, spu=spu) if count == 0 else spu_list[0]
    # 生成sku
    sku = sku if sku else 'P0000' + str(int(time.time()))
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
            Goods.objects.create(
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
                originalPrice=goods['originalPrice'],
                stock=goods['stock'],
                sellUnit=goods['sellUnit'],
                videoUrl=goods['videoUrl'],
                videoImage=goods['videoImage'],
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
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, pid, store_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            store = Store.objects.get(pid=pid, id=store_id)
            goodsList = store.all_goods.all()
            res = []
            for goods in goodsList:
                obj = model_to_dict(goods)
                obj['spu'] = goods.spu.spu
                res.append(obj)

        except Exception as e:
            print(e)
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
                    originalPrice=goods['originalPrice'],
                    stock=goods['stock'],
                    sellUnit=goods['sellUnit'],
                    videoUrl=goods['videoUrl'],
                    videoImage=goods['videoImage'],
                    goodsImageUrls=goods['goodsImageUrls'],
                    defaultImageUrl=goods['defaultImageUrl'],
                    goodsLimitVo=goods['goodsLimitVo'],
                    selectedTag=goods['selectedTag'],
                    selectedClassifyList=goods['selectedClassifyList'],
                    selectedGoodsAttrList=goods['selectedGoodsAttrList'],
                    selectedGoodsPropList=goods['selectedGoodsPropList'],
                    selectedGoodsRightsList=goods['selectedGoodsRightsList'],
                    update_time=timezone.now()
                )
        except Exception as e:
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


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
                    selectedTagName = goods['selectedTag']['name']
                    if selectedTagName:
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
            print(e)
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
        print(goodsReview)
        # 1.创建新的商品对象
        try:
            customer = Customer.objects.get(pid=pid)
            spu = SPU.objects.get(id=spu_id)
            review = GoodsReview.objects.create(
                spu=spu,
                customer=customer,
                star=goodsReview['star'],
                name=goodsReview['name'],
                msg=goodsReview['msg'],
                specs=goodsReview['specs'],
                avatar=goodsReview['avatar'],
                imgs=goodsReview['imgs'],
                anonymous=goodsReview['anonymous'],
            )
            goodsReview['reviewState'][int(index)]['id'] = review.id
            order = Order.objects.filter(orderNum=orderNum).first()
            order.reviewState = goodsReview['reviewState']
            res = filter(lambda x: x.count <= 1, order.reviewState)
            if len(list(res)) == 0:
                order.status = '交易完成'
            order.save()
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        # 4.响应
        return http.JsonResponse({"code": RETCODE.OK})

    def get(self, request, spu_id):
        # 1.接受参数
        # 1.创建新的图片对象
        try:
            spu = SPU.objects.get(id=spu_id)
            res = spu.all_reviews.values()
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK, 'reviewList': list(res)})

    def put(self, request, id, mode):
        reviews = json.loads(request.body)
        try:
            if mode == 'likes':
                GoodsReview.objects.filter(id=id).update(likes=reviews['likes'])
            elif mode == 'reply':
                GoodsReview.objects.filter(id=id).update(children=reviews['children'], reviews=reviews['reviews'])
            elif mode == 'additional':
                goodsReview = GoodsReview.objects.filter(id=id).first()
                order = goodsReview.order
                order.reviewState = reviews['reviewState']
                goodsReview.additional = {'msg': reviews['msg'], 'imgs': reviews['imgs']}
                order.save()
                goodsReview.save()
        except Exception as e:
            print(e)
            return http.HttpResponseForbidden()
        return http.JsonResponse({'code': RETCODE.OK})


class GoodsReviewDefaultView(View):
    @classmethod
    def post(cls, request, specs, spu_id, customer):
        """
        :param request:
        :return:
        """
        try:
            spu = SPU.objects.get(id=spu_id)
            review = GoodsReview.objects.create(
                spu=spu,
                customer=customer,
                specs=specs,
                name=customer.nickName,
                msg='顾客未及时做出评价，系统默认好评',
                avatar=customer.avatarUrl,
            )
        except Exception as e:
            return http.HttpResponseForbidden()
        # 4.响应
        return review.id


