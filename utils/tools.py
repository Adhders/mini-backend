#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: tools.py
@time: 2021/8/8 10:46
@desc:
'''
import binascii
from utils import constants
from pyDes import des, ECB,PAD_PKCS5
import math,random

# 需要安装 pip install pyDes
def generatekey(num):
    library = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
    key = ""
    for i in range(num):
        randomPoz = math.floor(random.random() * len(library))
        key += library[randomPoz]
    return key


def des_encrypt(s, secret_key=constants.SECRET_KEY):
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    en = k.encrypt(s, padmode=PAD_PKCS5)
    return binascii.b2a_hex(en).decode()


def des_decrypt(s, secret_key=constants.SECRET_KEY):
    iv = secret_key
    k = des(secret_key, ECB, iv, pad=None, padmode=PAD_PKCS5)
    de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
    return de.decode()


if __name__ == "__main__":

    secret_str = des_encrypt('hello word')
    print(secret_str)
    clear_str = des_decrypt("8380d086094b66fc444b7eb641d28a6d")
    print(clear_str)
