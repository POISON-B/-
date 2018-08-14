#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-7-24 下午2:36
# @Author  : Shark
# @Site    : 
# @File    : ev_info_modify.py
# @Software: PyCharm
# from db_Initialization import db_ev_records_query, db_domain_query, db_ev_query, db_session
# from sqlalchemy.orm import *
# from sqlalchemy import *
# from sqlalchemy.ext.automap import automap_base
#
# from config import *
#
#
# def connect_db(text_run=True):
#     if text_run:
#         # 使用UTF-8编码连接
#         db_connect = create_engine('mysql+pymysql://' + DB_USER2 + ':' + DB_PASSWD2 + '@' + DB_HOST2 + ':' + DB_PORT2
#                                    + '/' + DB_NAME2 + '?charset=utf8')
#         return db_connect
#
#
# engine2 = connect_db()  # 连接数据库
# db_session2 = sessionmaker(bind=engine2)  # 创建session工厂
# db_session2 = db_session2()  # 调用工厂方法创建工厂对象
# db_domain_metadata2 = MetaData(engine2)
# Table('ev_info', db_domain_metadata2, autoload=True)
# db_domain_base2 = automap_base(metadata=db_domain_metadata2)  # 映射表
# db_domain_base2.prepare()
# db_Ev2 = db_domain_base2.classes.ev_info
# db_ev_query2 = db_session2.query(db_Ev2)
#
# wb_name = '广东华富电梯有限公司'
#
# wb_name_uuid = db_domain_query.filter_by(name=wb_name).first()
#
# ev_info_uuid = db_ev_records_query.filter_by(companyId=wb_name_uuid.uuid, status=0).all()
#
# ev_info_uuid_list = list()
#
# for i in ev_info_uuid:
#     ev_info1 = db_ev_query.filter_by(uuid=i.evId).first()
#     ev_info2 = db_ev_query2.filter_by(uuid=i.evId).first()
#     if ev_info2 or ev_info1:
#         ev_info1.deviceNumber = ev_info1.evOrder
#         ev_info1.manufacturer = ev_info2.manufacturer
#         ev_info1.productionDate = ev_info2.productionDate
#         ev_info1.productionNumber = ev_info2.productionNumber
#         db_session.commit()
#





