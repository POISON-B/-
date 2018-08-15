#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-15 下午11:37
# @Author  : Shark
# @File    : main.py
# @Software: PyCharm
from utlis import db_domain_query, db_team_query
from utlis.data_import_db import ProjectTOdb


def run(name, wbid, temid):
    ProjectTOdb().to_db(name)
    ProjectTOdb().lift_to_db(wbid, temid)


if __name__ == '__main__':
    weibao_name = ''
    wbid = db_domain_query.filter_by(name=weibao_name).first()
    temid = db_team_query.filter_by(companyId=wbid.uuid, teamName='默认班组').first()

    if wbid and temid:
        run(weibao_name, wbid.uuid, temid.uuid)
