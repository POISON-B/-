#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-7-31 下午2:35
# @Author  : Shark
# @Site    : 
# @File    : regcode_check.py
# @Software: PyCharm
import csv

from db_Initialization import *

webao_name = '重庆其士电梯有限公司'

db_records = list()

weibao_info = db_domain_query.filter_by(name=webao_name).first()

ev_records_info = db_ev_records_query.filter_by(companyId=weibao_info.uuid, status=0).all()

for ev in ev_records_info:
    ev_info = db_ev_query.filter_by(uuid=ev.evId).first()
    db_records.append(ev_info.regCode)

local_data = csv.reader(open('regcode.csv'))

for reg in local_data:
    if bytes(reg[0], encoding='utf8') not in db_records:
        with open('1.csv', 'a') as f:
            f.write(reg[0] + '\n')
        print(reg)


