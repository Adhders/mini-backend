#!/usr/bin/env python
# encoding: utf-8
'''
@author: junbo
@file: __init__.py
@time: 1/14/2021 1:56 PM
@desc:
'''

import  pymysql

pymysql.version_info = (1, 4, 13, "final", 0)
pymysql.install_as_MySQLdb()