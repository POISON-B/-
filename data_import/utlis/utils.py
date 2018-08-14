#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午2:54
# @Author  : Shark
# @Site    : 
# @File    : utils.py
# @Software: PyCharm

import requests
import random
from retry import retry

from config import BAIDU_MAP_AK


# 根据项目名称利用百度地图API查询经纬度118926602749922523
@retry(tries=3, delay=3)
def get_Lat_lon(project_name):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = lambda x: random.choice(x)
    ak = ak(BAIDU_MAP_AK)
    params = {'address': project_name, 'ak': ak, 'output': 'json'}
    html = requests.get(url=url, params=params)
    location = html.json()

    if location['status'] == 0:
        # print(location['result']['location'])
        return location['result']['location']
    else:
        print('未找到关于{}的地址'.format(project_name))
        return ''


# 根据经纬度利用百度地图API查询详细地址
@retry(tries=3, delay=3)
def get_address(location):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = lambda x: random.choices(BAIDU_MAP_AK)
    if isinstance(location, dict):
        params = {'location': '{lat},{lng}'.format(lat=location['lat'], lng=location['lng']), 'ak': ak, 'output': 'json', 'pois': 1}
        html = requests.get(url=url, params=params)
        address = html.json()
        formatted_address = address['result']['formatted_address']
        address_info = address['result']['addressComponent']
        address_info['address'] = formatted_address

        return address_info
    else:
        return print("请输入正确格式的经纬度({'lng': 104.0529375076847, 'lat': 30.552951548072645})")


# json地址缓存文件项目加密
def project_md5(project: str):
    import hashlib
    return hashlib.md5(project.encode('utf8')).hexdigest()


# json地址缓存返回
def address_json(filename: str):
    import json
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read(), encoding='utf8')
            return data
    except json.decoder.JSONDecodeError:
        print('载入地址缓存文件失败....重新载入')


# 写入json地址缓存
def insert_json(data, filename):
    import json
    import collections
    data = collections.OrderedDict(sorted(data.items()))
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
