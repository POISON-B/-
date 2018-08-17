#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-2 下午4:25
# @Author  : Shark
# @Site    : 
# @File    : city_pipelines.py
# @Software: PyCharm

from xian.uitl import db_evIfo, db_session, db_evIfo_query

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
        print('ssss')
        if not db_evIfo_query.filter_by(id=args[0]['elevator_number']).first():
            data = args[0]['next_inspect_date'].replace('年', '-').replace('月', '')
            ev_info = db_evIfo(
                id=args[0]['elevator_number'],
                customer_addr=args[0]['address'],
                customer_name=args[0]['customer_name'],
                inspector_name=args[0]['phone'],
                reg_code=args[0]['reg_code'],
                next_inspect_date=data,
                maintenance_company_name=args[0]['maintenance_company_name']
            )

            db_session.add(ev_info)
            db_session.commit()

            return args[0]
    return None


pipelines_dict['xian'] = xian
pipelines_dict['wuhu'] = wuhu


class Factory(object):
    def __init__(self, key):
        self.key = key

    def get_obj(self):
        if self.key in pipelines_dict.keys():
            return pipelines_dict[self.key]


if __name__ == '__main__':
    city = Factory('xian')
    city.get_obj()
