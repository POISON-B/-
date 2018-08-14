#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午3:33
# @Author  : Shark
# @Site    : 
# @File    : db_query.py
# @Software: PyCharm

from .db_initialize import *


# 项目地址id查询
def project_address_id_query(data):

        if 'project_province' in data and data['project_province']:
            v3_area_obj = db_area_query.filter(db_Area.areaName.like(data['project_province'] + "%")).first()
            if v3_area_obj:
                data['project_province'] = v3_area_obj.uuid

        if 'project_city' in data and data['project_city']:
            # 兼容直辖市，会同时查出省和市
            v3_area_obj = db_area_query.filter(
                db_Area.areaName.like(data['project_city'] + "%")).order_by(db_Area.uuid.desc()).first()

            if v3_area_obj:
                data['project_city'] = v3_area_obj.uuid

        if 'project_country' in data and data['project_country']:
            v3_area_obj = db_area_query.filter(db_Area.areaName.like(data['project_country'] + "%")).first()

            if v3_area_obj:
                data['project_country'] = v3_area_obj.uuid

        return data
