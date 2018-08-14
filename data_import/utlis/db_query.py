# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # @Time    : 18-8-14 下午3:33
# # @Author  : Shark
# # @Site    :
# # @File    : db_query.py
# # @Software: PyCharm
import Levenshtein
import difflib


# from .db_initialize import *
#
#
# def project_address_id_query(data):
#     """
#     项目地址id查询
#
#     :param data:   项目地址信息
#     :return:   地址id
#     """
#
#     if 'project_province' in data and data['project_province']:
#         v3_area_obj = db_area_query.filter(db_Area.areaName.like(data['project_province'] + "%")).first()
#         if v3_area_obj:
#             data['project_province'] = v3_area_obj.uuid
#
#     if 'project_city' in data and data['project_city']:
#         # 兼容直辖市，会同时查出省和市
#         v3_area_obj = db_area_query.filter(
#             db_Area.areaName.like(data['project_city'] + "%")).order_by(db_Area.uuid.desc()).first()
#
#         if v3_area_obj:
#             data['project_city'] = v3_area_obj.uuid
#
#     if 'project_country' in data and data['project_country']:
#         v3_area_obj = db_area_query.filter(db_Area.areaName.like(data['project_country'] + "%")).first()
#
#         if v3_area_obj:
#             data['project_country'] = v3_area_obj.uuid
#
#     return data
#
#
# def brand_id_query(data):
#     """
#     电梯品牌查询
#
#     :param data: 电梯品牌信息
#     :return:  品牌id
#     """
#     return db_brand_query.filter_by(name=data['brandId']).first()
from datetime import datetime

from config import CREATE_BY
from utlis.utils import gen_uuid_for_db, judge_uuid


def updata_project(project, k, value):
    """
    更新项目
    :param value:项目信息
    :param project: 需要跟新的项目
    :param k: 项目名
    :return:
    """
    project.name = k
    project.createAt = datetime.now()
    # project.createBy = CREATE_BY
    project.address = value['project_address']
    project.latitude = value['ln_la']['lat']
    project.longitude = value['ln_la']['lng']
    project.province = value['project_province']
    project.city = value['project_city']
    project.country = value['project_country']

    db_session.commit()


def project_judge_creat(k, value):
    name = projectInfo_domain_query.filter(db_projectInfo.name.like('%' + k)).all()
    if len(name) == 1:
        updata_project()
        return None
    if len(name) > 1:
        for info in name:
            number = difflib.SequenceMatcher(None, k, info.name.).ratio()
            if number >= 0.7:
                updata_project()
    else:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, projectInfo_domain_query)
        project = db_projectInfo(
            uuid = uuid,
            address = value['project_address'],
            latitude = value['ln_la']['lat'],
            longitude = value['ln_la']['lng'],
            province = value['project_province'],
            city = value['project_city'],
            country = value['project_country']
        )

        db_session.add(project)
        db_session.commit()
