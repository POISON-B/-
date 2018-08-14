#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-7-23 下午5:30
# @Author  : Shark
# @Site    : 
# @File    : data_matching.py
# @Software: PyCharm

import csv

from db_Initialization import *
from config import *
import datetime


def regcode_matching():
    """
    根据绑定了维保单位的电梯，和导入的excle表的注册代码进行匹配验证
    :return:
    """

    wb_name = '东莞市顺捷电梯有限公司'
    ev_info_uuid_list = list()
    ev_info_regcode_list = list()
    csv_recode = list()


    wb_name_uuid = db_domain_query.filter_by(name=wb_name).first()    # 查询维保单位uuid

    # name = projectInfo_domain_query.filter_by(name='金色水岸花园').first()  # 查询项目uuid

    ev_info_uuid = db_ev_records_query.filter_by(companyId=wb_name_uuid.uuid, status=0).all()  # 查询所有在此维保单位中的电梯

    # ev_info_uuid = db_ev_query.filter_by(projectId=name.uuid).all()

    for i in ev_info_uuid:
        ev_info_uuid_list.append(i.evId)  # 生成电梯uuid列表
    #
    for j in ev_info_uuid_list:
        ev_info_regcode = db_ev_query.filter_by(uuid=j).first()
        regcode = str(ev_info_regcode.regCode).strip("b'").strip("'")
        # with open('3.csv', 'a+') as f:
        #     f.write(regcode + '\n')
        ev_info_regcode_list.append(regcode)  # 查询电梯表获得，注册代码
    #
    print(len(ev_info_uuid_list))

    csv_data = csv.reader(open('regcode.csv'))
    for c in csv_data:
        csv_recode.append(c[0])  # 原始csv文件注册代码列表

    # for k in ev_info_regcode_list:
    #     if k not in csv_recode:
    #         with open('1.csv', 'a') as f:
    #             f.write(str(k) + '\n')  # 比对两个注册代码列表 没有在原始csv文件就输出

    for k in csv_recode:
        if k not in ev_info_regcode_list:
            with open('1.csv', 'a') as f:
                f.write(k + '\n')

#     if c[0] not in ev_info_regcode_list:
#         ev_info = db_ev_query.filter_by(regCode=c[0]).first()
#         wb = db_ev_records_query.filter_by(evId=ev_info.uuid, status=0).first()
        # wb.status = 1
        # wb.endTime = datetime.datetime.now().date()
        # remind = db_remind_query.filter_by(evId=ev_info.uuid, remind=0).first()
        # remind.remind = 1
        # db_session.commit()


