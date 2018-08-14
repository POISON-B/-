#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午2:04
# @Author  : Shark
# @Site    : 
# @File    : config.py
# @Software: PyCharm
from os import path

import logging

DB_HOST = '172.16.1.210'
DB_PORT = '3306'
DB_NAME = 'ttd'
DB_USER = 'ttd'
DB_PASSWD = 'ROOT@mwteck123'


ADDRESS_JSON = 'var/address.json'


CREATE_BY = 'znh'
SAVE_ID = 50
PATH = path.dirname(__file__)
FILE_NAME = '项目上传模板.csv'
FILE_PATH = '/'.join((PATH, FILE_NAME))
print(FILE_PATH)
JSON_PATH = '/'.join((PATH, ADDRESS_JSON))

BAIDU_MAP_AK = (
    'O7hgHKGFW4DGh0n8TxaOxOdoiFLnrZGI',  # 公司API KEY
    'W7KW0i88jYz1x0OxX5hZ9VEcHD8sxkcC',  # 吕强API KEY
    'yQBIj4sdILLqW5iLZEvNdPMUseFB3ozG',  # 徐恒API KEY
    'he4grC14QgGg1u4GzSVB6xbUmDIGIe8b',  # myfifi_2 API KEY
    'pF2sGa7vwXzj3NiOrayli0aytoUDn9fg',  # myfifi_3 API KEY
    'xsF1V1EKn14M71yH0MYPk9sfmbER1KcG',  # myfifi_4 API KEY
    '0B8yZIqc4GvE3UCOzUVzHtLCm3sSqlwk',  # myfifi_55 API KEY
    'YNw3saMUSu6jUM7l3jvOL5mhhLukcqcZ'
)

# 电梯类型，1:直梯, 2：杂物梯, 3:液压梯, 4:扶梯

EV_TYPE_MAP = {
    '乘客电梯': 1,
    '特种电梯': 1,
    '载货电梯': 1,
    '医用电梯': 1,
    '车辆电梯': 1,
    '观光电梯': 1,
    '餐梯': 1,
    '自动扶梯与自动人行道': 4,
    '曳引与强制驱动电梯': 1,
    '曳引驱动乘客电梯': 1,
    '液压驱动电梯': 3,
    '强制驱动载货电梯': 1,
    '曳引驱动载货电梯': 1,
    '其它类型电梯': 1,
    '杂物电梯': 2,
    '液压乘客电梯': 3,
    '防爆电梯': 1,
    '自动扶梯': 4,
    '自动人行道': 4,
    '液压载货电梯': 3,
    '其它': 1,
    '病床电梯': 1,
    '': 1
}

# 电梯类型
EV_TYPE = {
        '直梯': 1,
        '杂物梯': 2,
        '液压梯': 3,
        '扶梯': 4
}

# 电梯驱动方式
DRIVE_TYPE = {
    '曳引驱动': 1,
}


def log():
    # 创建logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # 创建handler 命令行
    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(logging.DEBUG)

    # 文件
    fileHandler = logging.FileHandler('var_s/log.txt')
    fileHandler.setLevel(logging.NOTSET)

    # 格式化输出样式
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    consoleHandler.setFormatter(formatter)
    fileHandler.setFormatter(formatter)

    # 添加到logger中
    logger.addHandler(consoleHandler)
    logger.addHandler(fileHandler)

    return logger
