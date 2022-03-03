#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: test.py
@time: 1/19/2021 8:43 PM
@desc:
'''

from fdfs_client.client import Fdfs_client, get_tracker_conf

# 2. 创建FastDFS客户端实例

tracker_path = get_tracker_conf('fastfdfs_client.conf')
client = Fdfs_client(tracker_path)

# 3. 调用FastDFS客户端上传文件方法
ret = client.upload_by_filename(r'../static/images/silver.jpg')
print(ret)

