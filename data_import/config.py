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
FILE_NAME = '电梯导入模板文件.csv'
FILE_PATH = '/'.join((PATH, FILE_NAME))

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
