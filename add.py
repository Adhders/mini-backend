#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: test.py
@time: 2021/7/24 16:44
@desc:
'''

# -*- coding: utf-8 -*-
import requests
from qiniu import Auth, put_file, etag,BucketManager,build_batch_rename,build_batch_delete
import qiniu.config

#需要填写你的 Access Key 和 Secret Key
access_key = 'qzwEr-xaXDxPHOxXAhPs6ofGA4HzCp8UQ1Jslvuo'
secret_key = 'w3UaRyqtpD9pdtAkv-ruIlrxnGPr0JXdfjsch9UW'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'chuangbiying'

#上传后保存的文件名
key = '123.jpg'

#生成上传 Token，可以指定过期时间等
token = q.upload_token(bucket_name)
bucket = BucketManager(q)
#要上传文件的本地路径
localfile = r'C:\Users\86136\Desktop\screen.png'

def add():
    ret, info = put_file(token, key, localfile, version='v2')
    print(info)
    assert ret['key'] == key
    assert ret['hash'] == etag(localfile)

def get():
    # 初始化BucketManager
    # 你要测试的空间， 并且这个key在你空间中存在
    # 获取文件的状态信息
    ret, info = bucket.stat(bucket_name, key)
    print(info)
    assert 'hash' in ret
def rename():
    ops = build_batch_rename(bucket_name, {key: 'target_key1'}, force='true')
    ret, info = bucket.batch(ops)
    print(info)

def delete():
    keys = ['target_key1', 'about1.jpg']
    ops = build_batch_delete(bucket_name, keys)
    ret, info = bucket.batch(ops)
    print(info)


if __name__=='__main__':
    import hashlib

    yan = '123'  # 定义加盐字符串
    pwd = '20c3d606046011ecadfafaf45faf8a54'

    md5_pwd = hashlib.md5()
    md5_pwd.update((pwd + yan).encode('UTF-8'))  # 加盐
    pwd = md5_pwd.hexdigest()
    print(pwd)
    # pwd = hashlib.new('md5',(pwd+yan).encode('UTF-8')).hexdigest()   #也可以这样简写哦。。一句话搞定。
