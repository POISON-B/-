#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-2 下午4:25
# @Author  : Shark
# @Site    : 
# @File    : city_pipelines.py
# @Software: PyCharm
import pymongo

from elevator_spider.uitl import db_evIfo, db_session, db_evIfo_query, gen_uuid_for_db, judge_uuid
from scrapy.conf import settings

pipelines_dict = dict()


def xian(*args):
    if args:
        if not db_evIfo_query.filter_by(id=args[0]['code']).first():
            ev_info = db_evIfo(
                id=args[0]['code'],
                brand=args[0]['brand'],
                reg_code=args[0]['regcode'],
                inspection_unit_name=args[0]['test'],
                maintenance_company_name=args[0]['maintenance'],
                customer_name=args[0]['use'],
                project_addr=args[0]['address'],
                customer_addr=args[0]['region']
            )
            db_session.add(ev_info)
            db_session.commit()

            return args[0]

    return None


def wuhu(*args):
    if args:
        if not db_evIfo_query.filter_by(id=args[0]['elevator_number']).first():
            date = args[0]['next_inspect_date'].replace('年', '-').replace('月', '')
            ev_info = db_evIfo(
                id=args[0]['elevator_number'],
                customer_addr=args[0]['address'],
                customer_name=args[0]['customer_name'],
                inspector_name=args[0]['phone'],
                reg_code=args[0]['reg_code'],
                next_inspect_date=date,
                maintenance_company_name=args[0]['maintenance_company_name']
            )

            db_session.add(ev_info)
            db_session.commit()

            return args[0]
    return None


def tianjin(*args):
    if args:
        if not db_evIfo_query.filter_by(id=args[0]['id']).first():
            date = args[0]['next_inspect_date'].replace('年', '-').replace('月', '')
            next_date = args[0]['up_inspect_date'].replace('年', '-').replace('月', '')
            ev_info = db_evIfo(
                id=args[0]['id'],
                reg_code=args[0]['reg_code'],
                customer_name=args[0]['customer_name'],
                inspector_name=args[0]['use_phone'],
                maintenance_company_name = args[0]['maintenance_company_name'],
                building_num = args[0]['help_phone'],
                unit_num = args[0]['complaints_phone'],
                next_inspect_date=date,
                customer_device_id=next_date
            )

            db_session.add(ev_info)
            db_session.commit()

            return args[0]
    return None


def nanjing(*args):
    if args:
        if not db_evIfo_query.filter_by(id=args[0]['id']).first():
            try:
                uuid = gen_uuid_for_db()
                uuid = judge_uuid(uuid, db_evIfo_query)
                ev_info = db_evIfo(
                    uuid=args[0]['id'] if args[0]['id'] else uuid,
                    reg_code=args[0]['reg_code'],
                    customer_name=args[0]['customer_name'],
                    inspector_name=args[0]['phone'],
                    customer_addr=args[0]['project_addr'],
                    next_inspect_date=args[0]['next_inspect_date'],
                    brand=args[0]['brand']
                )

                db_session.add(ev_info)
                db_session.commit()

                return args[0]
            except:
                uuid = gen_uuid_for_db()
                uuid = judge_uuid(uuid, db_evIfo_query)
                ev_info = db_evIfo(
                    id=uuid,
                    reg_code=args[0]['reg_code'],
                    customer_name=args[0]['customer_name'],
                    inspector_name=args[0]['phone'],
                    customer_addr=args[0]['project_addr'],
                    next_inspect_date=args[0]['next_inspect_date'],
                    brand=args[0]['brand']
                )

                db_session.add(ev_info)
                db_session.commit()
    return None


# def najing2(**kwargs):
#     if kwargs:
#         if not db_evIfo_query.filter_by(id=args[0]['id']).first():


def chengdu(*args):
    host = settings['MONGODB_HOST']
    port = settings['MONGODB_PORT']
    dbname = settings['MONGODB_DBNAME']
    sheetname = settings['SHEETNAME']

    client = pymongo.MongoClient(host=host, port=port)

    mydb = client[dbname]
    # 存放数据的表
    mydata = mydb[sheetname]

    data = dict(args[0])

    mydata.insert(data)


def nanjing2(*args):
    host = settings['MONGODB_HOST']
    port = settings['MONGODB_PORT']
    dbname = settings['MONGODB_DBNAME']
    sheetname = settings['SHEETNAME']

    client = pymongo.MongoClient(host=host, port=port)

    mydb = client[dbname]
    # 存放数据的表
    mydata = mydb[sheetname]

    data = dict(args[0])

    mydata.insert(data)


pipelines_dict['西安'] = xian
pipelines_dict['芜湖'] = wuhu
pipelines_dict['天津'] = tianjin
pipelines_dict['南京'] = nanjing
pipelines_dict['南京2'] = nanjing2
pipelines_dict['成都'] = chengdu


class Factory(object):
    def __init__(self, key):
        self.key = key

    def get_obj(self):
        if self.key in pipelines_dict.keys():
            return pipelines_dict[self.key]


if __name__ == '__main__':
    city = Factory('xian')
    city.get_obj()
