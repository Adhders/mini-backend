from django.views import View
from django.http import JsonResponse, HttpResponseForbidden
from django.core.cache import cache

from utils.response_code import RETCODE
from .models import Industry


class IndustryView(View):
    """行业数据查询"""

    def get(self, request):
        """
        提供行业数据
        :param request: 请求对象
        :return: 响应
        """
        # 获取查询参数industry_id
        industry_id = request.GET.get('industry_id')

        # 如果前段没有传入industry_id,代表要查询所有行业
        if industry_id is None:
            # 读取行业缓存数据
            category_list = cache.get('category_list')
            # 先尝试从缓存中读取数据
            if category_list is None:
                # 查询所有行业的模型，得到所有行业的查询集
                category_qs = Industry.objects.filter(parent=None)
                # 遍历所有行业的模型，将里面的每一个模型对象转换成字典对象，再包装到列表中
                category_list = []  # 用来装每一个行业的字典对象
                for category_model in category_qs:
                    category_list.append(
                        {
                            'id': category_model.id,
                            'name': category_model.name
                        }
                    )
                # 从mysql中查询出来行业数据之后立即设置缓存，缓存时间3600秒
                cache.set('category_list', category_list, 3600)
            # 响应行业数据
            return JsonResponse({
                'code': RETCODE.OK,
                'errmsg': 'OK',
                'category_list': category_list
            })
        else:
            # 先尝试取缓存数据
            sub_data = cache.get('sub_industry_' + industry_id)
            if sub_data is None:
                # 如果前端有传入industry_id,代表查询指定行业下面的所有分类
                subs_qs = Industry.objects.filter(parent_id=industry_id)
                try:
                    # 查询当前指定的上级行政区
                    parent_model = Industry.objects.get(id=industry_id)
                except Industry.DoesNotExist:
                    return HttpResponseForbidden('industry_id不存在')

                sub_list = []  # 用来装所有下级行政区字典数据
                for sub_model in subs_qs:
                    sub_list.append({
                        'id': sub_model.id,
                        'name': sub_model.name
                    })

                # 构造完整数据
                sub_data = {
                    'id': parent_model.id,
                    'name': parent_model.name,
                    'subs': sub_list  # 下级所有行政区数据
                }
                # 设置缓存
                cache.set('sub_industry_'+industry_id, sub_data, 3600)
            # 响应市或区数据
            return JsonResponse({
                'code': RETCODE.OK,
                'errmsg': 'OK',
                'sub_data': sub_data
            })


