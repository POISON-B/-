#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/22 13:36
# @Author  : shark
# @Site    : 
# @File    : db_Initialization.py
# @Software: PyCharm

"""
主函数各个功能实现
"""

from sqlalchemy.orm import *
from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from config import *


# 连接数据库
def connect_db(text_run=True):
    if text_run:
        # 使用UTF-8编码连接
        db_connect = create_engine('mysql+pymysql://' + DB_USER + ':' + DB_PASSWD + '@' + DB_HOST + ':' + DB_PORT
                                   + '/' + DB_NAME + '?charset=utf8')
        return db_connect

    else:
        db_connect = create_engine('mysql+pymysql://' + DB_USER + ':' + DB_PASSWD + '@' + DB_HOST + ':' + DB_PORT
                                   + '/' + DB_NAME + '?charset=utf8')
        return db_connect


engine = connect_db()  # 连接数据库
db_session = sessionmaker(bind=engine)  # 创建session工厂
db_session = db_session()  # 调用工厂方法创建工厂对象

# 映射projectInfo表和获得相关操作
db_domain_metadata = MetaData(engine)  # 绑定引擎
Table('projectInfo', db_domain_metadata, autoload=True)
Table('companyinfo', db_domain_metadata, autoload=True)
Table('area', db_domain_metadata, autoload=True)
Table('brand', db_domain_metadata, autoload=True)
Table('ev_records', db_domain_metadata, autoload=True)
Table('ev_info', db_domain_metadata, autoload=True)
Table('ev_verticalLander_conf', db_domain_metadata, autoload=True)
Table('ev_sundriesLander_conf', db_domain_metadata, autoload=True)
Table('ev_hydraulicPressure_conf', db_domain_metadata, autoload=True)
Table('ev_escalator_conf', db_domain_metadata, autoload=True)
Table('ev_annual_inspection', db_domain_metadata, autoload=True)
Table('ev_remind', db_domain_metadata, autoload=True)
Table('team', db_domain_metadata, autoload=True)

db_domain_base = automap_base(metadata=db_domain_metadata)  # 映射表
db_domain_base.prepare()
db_projectInfo = db_domain_base.classes.projectInfo  # 后跟需要操作的表名
projectInfo_domain_query = db_session.query(db_projectInfo)  # 查询项目

db_Domain = db_domain_base.classes.companyinfo
db_domain_query = db_session.query(db_Domain)   # 查询公司

db_Area = db_domain_base.classes.area               # 查询地址
db_area_query = db_session.query(db_Area)

db_brand = db_domain_base.classes.brand
db_brand_query = db_session.query(db_brand)         # 查询品牌

db_ev_records = db_domain_base.classes.ev_records
db_ev_records_query = db_session.query(db_ev_records)   # 查询维保公司


db_Ev = db_domain_base.classes.ev_info
db_ev_query = db_session.query(db_Ev)       # 查询电梯信息

db_EvConf = db_domain_base.classes.ev_verticalLander_conf   # 查询直梯表信息
db_ev_conf_query = db_session.query(db_EvConf)

db_EsunConf = db_domain_base.classes.ev_sundriesLander_conf
db_esun_conf_query = db_session.query(db_EsunConf)          # 查询杂货电梯表信息

db_EhConf = db_domain_base.classes.ev_hydraulicPressure_conf    # 查询液压电梯表信息
db_eh_conf_query = db_session.query(db_EhConf)

db_EsConf = db_domain_base.classes.ev_escalator_conf
db_es_conf_query = db_session.query(db_EsConf)              # 查询扶梯表信息

db_Time = db_domain_base.classes.ev_annual_inspection
db_year_time_query = db_session.query(db_Time)              # 查询年检详细表信息


db_ev_remind = db_domain_base.classes.ev_remind             # 年检提醒表信息
db_remind_query = db_session.query(db_ev_remind)

db_team = db_domain_base.classes.team                       # 默认班组信息
db_team_query = db_session.query(db_team)


