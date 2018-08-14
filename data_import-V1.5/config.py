#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-6-14 上午9:44
# @Author  : Shark
# @Site    : 
# @File    : config.py.py
# @Software: PyCharm

import logging

DB_HOST = '172.16.1.210'
DB_PORT = '3306'
DB_NAME = 'ttd'
DB_USER = 'ttd'
DB_PASSWD = 'ROOT@mwteck123'

# DB_HOST = '172.16.1.208'
# DB_PORT = '3306'
# DB_NAME = 'ttd_20180808005604'
# DB_USER = 'root'
# DB_PASSWD = 'root'

# DB_HOST2 = '172.16.1.208'
# DB_PORT2 = '3306'
# DB_NAME2 = 'ttd_20180722005601'
# DB_USER2 = 'root'
# DB_PASSWD2 = 'root'

ADDRESS_JSON = 'var_s/address.json'

TEST_RUN = False
CREATE_BY = 'znh'
SAVE_ID = 50

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
