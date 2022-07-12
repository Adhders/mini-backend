from functools import reduce

from django.test import TestCase

# Create your tests here.


a = {'id': 1, 'num': 24, 'group': '全部图像',
     'children': [
        {'id': 0, 'num': 20, 'group': '默认分组'},
        {'id': 1251675959, 'num': 1, 'group': 'abc',
            'children': [{'id': 213611896, 'num': 1, 'group': 'test', 'children': []}]}]}
def sum(s):
    print(s)
    if 'children' in s:
        for item in s['children']:
            s['num'] = s['num'] + sum(item)
    return s['num']

sum(a)
print(a)
#
# b = [{'id': 1, 'num': 6, 'group': '全部视频', 'children': [{'id': 0, 'num': 7, 'group': '默认分组'}]}]
#
# def elements(s, arr=None):
#     if arr is None:
#         arr = []
#     a = []
#
#
#
# def extract(arr, props, num):
#     for o in arr:
#         if o['group'] == props:
#             o['num'] = num
#             break
#         if 'children' in o:
#             extract(o['children'], props, num)
#
#
# res = extract(b, '默认分组', 6)
# print('res', res, b)
#
# s = []
# total = reduce(lambda x, y: sum(x) + sum(y), s, 0)
# print('total', total)
