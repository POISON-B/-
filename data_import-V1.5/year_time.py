#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-7-9 下午5:44
# @Author  : Shark
# @Site    : 
# @File    : year_time.py
# @Software: PyCharm

import csv

from db_Initialization import *


def reade_info(file_name):
    csv_data = csv.reader(open(file_name))
    for line in csv_data:
        line[1] = bytes(line[1], encoding="utf8")
        ev_uuid = db_ev_query.filter_by(projectId=line[0], regCode=line[1]).first()
        if ev_uuid:
            ev_records_info = db_ev_records_query.filter(and_(db_ev_records.companyId.isnot(None), db_ev_records.evId == ev_uuid.uuid, db_ev_records.status == 0)).first()
            print(ev_records_info.lastAnnualDate)
            if ev_records_info and line[2]:
                print('更改项目{0}的电梯,维保公司表的年检时间'.format(line[1]))
                ev_records_info.lastAnnualDate = line[2]
                db_session.commit()
                year_time_info = db_year_time_query.filter_by(evId=ev_uuid.uuid, companyId=ev_records_info.companyId).first()
                if year_time_info and line[2]:
                    print('更改项目{0}的电梯,年检提醒表的年检时间'.format(line[1]))
                    print(year_time_info.date)
                    year_time_info.date = line[2]
                    db_session.commit()


if __name__ == '__main__':
    reade_info('广东华富年检时间修改.csv')
