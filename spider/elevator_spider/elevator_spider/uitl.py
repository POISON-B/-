#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-7-18 下午5:05
# @Author  : Shark
# @Site    : 
# @File    : uitl.py
# @Software: PyCharm
from sqlalchemy.orm import *
from sqlalchemy import *
import random
from sqlalchemy.ext.automap import automap_base

from scrapy.conf import settings


def handle_value(value):
    value = value.replace('[', '').replace(']', '').replace("'", '')
    return value


COED_ID_1 = (1300000, 1335667)
# COED_ID_1 = (2010001, 2010111)
COED_ID_2 = (1335667, 1571333)
COED_ID_3 = (1571333, 1806999)


# 随机生成uuid
def gen_uuid_for_db():
    return random.randint(100000000000000000, 130000000000000000)


# 判断uuid是否存在

def judge_uuid(uuid, table):
    while True:
        pro_obj_check = table.filter_by(uuid=uuid).first()
        if pro_obj_check:
            uuid = gen_uuid_for_db()
            continue
        else:
            break
    return uuid


# 连接数据库
def connect_db(text_run=True):
    if text_run:
        # 使用UTF-8编码连接
        db_connect = create_engine('mysql+pymysql://' + settings['DB_USER'] + ':' + settings['DB_PASSWD'] + '@' +
                                   settings['DB_HOST'] + ':' + settings['DB_PORT'] + '/' + settings['DB_NAME'] + '?charset=utf8&autocommit=true')
        return db_connect

    else:
        db_connect = create_engine(
            'mysql+pymysql://' + settings['DB_USER'] + ':' + settings['DB_PASSWD'] + '@' + settings['DB_HOST'] + ':' +
            settings['DB_PORT'] + '/' + settings['DB_NAME'] + '?charset=utf8')
        return db_connect


engine = connect_db()  # 连接数据库
db_session = sessionmaker(bind=engine)  # 创建session工厂
db_session = db_session()  # 调用工厂方法创建工厂对象

# 映射projectInfo表和获得相关操作
db_domain_metadata = MetaData(engine)  # 绑定引擎
Table('elev_info_nanjing_increase_1', db_domain_metadata, autoload=True)


db_domain_base = automap_base(metadata=db_domain_metadata)
db_domain_base.prepare()
db_evIfo = db_domain_base.classes.elev_info_nanjing_increase_1
db_evIfo_query = db_session.query(db_evIfo)

