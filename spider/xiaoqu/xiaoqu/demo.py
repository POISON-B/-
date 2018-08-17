#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-10 上午11:57
# @Author  : Shark
# @Site    : 
# @File    : demo.py
# @Software: PyCharm

import pymongo

myclient = pymongo.MongoClient("mongodb://172.16.1.200:27017/")
mydb = myclient["chengu1"]
mycol = mydb["ev"]

data = mycol.find_one()
for i in data['info']:
    print(i)
# for x in mycol.find():
#     print(x)

