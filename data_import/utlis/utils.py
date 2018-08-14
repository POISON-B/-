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


@retry(tries=3, delay=3)
def get_Lat_lon(project_name):
    """
    根据项目名称利用百度地图API查询经纬度

    :param project_name: 项目名称
    :return: 经纬度字典 {"lng": xx, "lat": xx}
    """
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


@retry(tries=3, delay=3)
def get_address(location):
    """
    根据经纬度利用百度地图API查询详细地址

    :param location: 经纬度信息 {"lng": xx, "lat": xx}
    :return: 详细地址信息字典
    """
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


def project_md5(project: str):
    """
    json地址缓存文件项目加密

    :param project: 需加密的字符串
    :return:  MD5值
    """
    import hashlib
    return hashlib.md5(project.encode('utf8')).hexdigest()


def address_json(filename: str):
    """
    json地址缓存载入

    :param filename: json文件地址
    :return: 缓存地址字典
    """
    import json
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read(), encoding='utf8')
            return data
    except json.decoder.JSONDecodeError:
        print('载入地址缓存文件失败....重新载入')


def insert_json(data, filename):
    """
    写入json地址缓存
    :param data: 需要写入的地址信息
    :param filename: json文件地址
    :return: None
    """
    import json
    import collections
    data = collections.OrderedDict(sorted(data.items()))
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def clean_time(value):
    """
    格式化时间

    :param value: 时间字符串
    :return:  标准格式的时间字符串（xx-xx-xx）
    """
    import re
    if value:
        value = str(value)
        value = value.split('（')[0]
        reg = re.compile(r'(?=[\x21-\x7e]+)[^A-Za-z0-9]')
        value = re.sub(reg, '-', value).split(' ')[0]

        return value


def gen_uuid_for_db():
    """
    随机生成uuid
    :return: uuid
    """
    return random.randint(100000000000000000, 130000000000000000)


def judge_uuid(uuid, table):
    """
    判断uuid是否存在

    :param uuid: 生成的uuid
    :param table: 查询表
    :return: uuid
    """
    while True:
        pro_obj_check = table.filter_by(uuid=uuid).first()
        if pro_obj_check:
            uuid = gen_uuid_for_db()
            continue
        else:
            break
    return uuid
