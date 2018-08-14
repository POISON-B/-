#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/22 13:27
# @Author  : shark
# @Site    : 
# @File    : Tools_function.py
# @Software: PyCharm

"""
版本：py3
各种功能的函数
"""

import random
import requests
import os
from retry import retry
import sys
import time
import logging
import inspect
import datetime
import time
from sqlalchemy import and_

from config import BAIDU_MAP_AK, CREATE_BY, ADDRESS_JSON, log
from db_Initialization import db_session, projectInfo_domain_query, db_domain_query, \
                db_area_query, db_ev_query, db_ev_conf_query, db_esun_conf_query, db_eh_conf_query, db_es_conf_query, \
                db_Area, db_EvConf, db_EsunConf, db_EhConf, db_EsConf, db_ev_records_query, db_ev_records, db_Ev, \
                db_projectInfo, db_year_time_query, db_Time, db_ev_remind, db_remind_query, db_team, db_team_query

logger = log()


# 随机取AK
def get_AK(ak):
    return random.choice(ak)


# 保存电梯详细信息
def info_save(line, ev_type, ev_uuid):
    if line[4]:
        if ev_type_map[ev_type] == 1:

            now_uuid = gen_uuid_for_db()  # 生成直梯表的uuid
            ev_conf = db_ev_conf_query.filter_by(evId=ev_uuid).first()  # 查询直梯表
            if ev_conf:
                logger.warning('{}的直梯信息存在,更新信息'.format(line[0]))
                ev_conf.actuationForm = 1

                ev_conf.floors = line[11]
                ev_conf.station = line[12]
                ev_conf.door = line[13]
                ev_conf.maxLoad = line[14]
                ev_conf.speed = line[15]
                db_session.commit()

            else:
                now_uuid = judge_uuid(now_uuid, db_ev_conf_query)  # 判度生成的uuid是否存在
                db_evconf = db_EvConf(
                    uuid=now_uuid,
                    evId=ev_uuid,  # 用电梯信息表里的uuid来确认在直梯表里的关联关系
                    actuationForm=1,
                    floors=line[11],
                    station=line[12],
                    door=line[13],
                    maxLoad=line[14],
                    speed=line[15]
                    )
                db_session.add(db_evconf)
                db_session.commit()

        elif ev_type_map[ev_type] == 2:
            now_uuid = gen_uuid_for_db()
            ev_esun_info = db_esun_conf_query.filter_by(evId=ev_uuid).first()
            if ev_esun_info:
                logger.warning('{}的杂物梯信息存在,更新信息'.format(line[0]))

                ev_esun_info.actuationForm = 1
                ev_esun_info.floors = line[11]
                ev_esun_info.station = line[12]
                ev_esun_info.door = line[13]
                ev_esun_info.maxLoad = line[14]
                ev_esun_info.speed = line[15]
                db_session.commit()

            else:
                now_uuid = judge_uuid(now_uuid, db_esun_conf_query)

                db_esunconf = db_EsunConf(
                    uuid=now_uuid,
                    evId=ev_uuid,
                    actuationForm=1,
                    floors=line[11],
                    station=line[12],
                    door=line[13],
                    maxLoad=line[14],
                    speed=line[15]
                )
                db_session.add(db_esunconf)
                db_session.commit()

        elif ev_type_map[ev_type] == 3:
            now_uuid = gen_uuid_for_db()
            ev_eh_info = db_eh_conf_query.filter_by(evId=ev_uuid).first()
            if ev_eh_info:
                logger.warning('{}的液压梯信息存在,更新信息'.format(line[0]))

                ev_eh_info.floors = line[10]
                ev_eh_info.station = line[11]
                ev_eh_info.door = line[12]
                ev_eh_info.maxLoad = line[13]
                ev_eh_info.speedUp = line[14]
                ev_eh_info.speedDown = line[15]
                ev_eh_info.hydraulicCylinder = line[18]
                ev_eh_info.jackingType = line[19]
                db_session.commit()
            else:
                now_uuid = judge_uuid(now_uuid, db_eh_conf_query)

                db_ehconf = db_EhConf(
                    uuid=now_uuid,
                    evId=ev_uuid,
                    floors=line[10],
                    station=line[11],
                    door=line[12],
                    maxLoad=line[13],
                    speedUp=line[14],
                    speedDown=line[15],
                    hydraulicCylinder=line[18],
                    jackingType=line[19]
                )
                db_session.add(db_ehconf)
                db_session.commit()

        elif ev_type_map[ev_type] == 4:
            now_uuid = gen_uuid_for_db()
            ev_es_info = db_es_conf_query.filter_by(evId=ev_uuid).first()
            if ev_es_info:
                logger.warning('{}的扶梯信息存在,更新信息'.format(line[0]))

                ev_es_info.nominalSpeed = line[10]
                ev_es_info.nominalWidth = line[11]
                ev_es_info.inclinationAngle = line[12]
                ev_es_info.transforAbility = line[13]
                ev_es_info.liftingHeight = line[14]
                ev_es_info.length = line[15]
                ev_es_info.power = line[18]
                db_session.commit()

            else:
                now_uuid = judge_uuid(now_uuid, db_es_conf_query)

                db_esconf = db_EsConf(
                    uuid=now_uuid,
                    evId=ev_uuid,
                    nominalSpeed=line[10],
                    nominalWidth=line[11],
                    inclinationAngle=line[12],
                    transforAbility=line[13],
                    liftingHeight=line[14],
                    length=line[15],
                    power=line[18],
                )
                db_session.add(db_esconf)
                db_session.commit()

    else:
        if ev_type_map[ev_type] == 1:

            ev_conf = db_ev_conf_query.filter_by(evId=ev_uuid).first()  # 查询直梯表
            if ev_conf:
                logger.warning('{}信息存在,更新信息'.format(line[0]))
                ev_conf.actuationForm = 1

                ev_conf.floors = line[11]
                ev_conf.station = line[12]
                ev_conf.door = line[13]
                ev_conf.maxLoad = line[14]
                ev_conf.speed = line[15]
                db_session.commit()

            else:
                now_uuid = gen_uuid_for_db()  # 生成直梯表的uuid
                now_uuid = judge_uuid(now_uuid, db_ev_conf_query)  # 判度生成的uuid是否存在

                db_evconf = db_EvConf(
                    uuid=now_uuid,
                    evId=ev_uuid,  # 用电梯信息表里的uuid来确认在直梯表里的关联关系
                    actuationForm=1,
                    floors=line[11],
                    station=line[12],
                    door=line[13],
                    maxLoad=line[14],
                    speed=line[15]
                )

                db_session.add(db_evconf)
                db_session.commit()


#  保存电梯基本信息
def ev_info_save(line, new_uuid, project_id):
    if not line[4]:
        ev_data = db_Ev(
                    uuid=new_uuid,
                    projectId=project_id.uuid,
                    wtCode=None,
                    regCode=None,
                    brandId=line[2],
                    useFor=usefor[line[3]],
                    type=ev_type_map[line[3]],
                    deviceNumber='',
                    manufacturer=line[6],
                    productionDate=line[7],
                    productionNumber=line[8],
                    modelNumber=line[9],
                    evOrder=line[1],
                    createAt=datetime.datetime.now().date(),
                    createBy=CREATE_BY,
                    status=1,
                    userLock=0,
                )
        db_session.add(ev_data)
        db_session.commit()

    else:
        ev_data = db_Ev(
            uuid=new_uuid,
            projectId=project_id.uuid,
            wtCode=None,
            regCode=line[4],
            brandId=line[2],
            useFor=usefor[line[3]] if usefor[line[3]] else 1,
            type=ev_type_map[line[3]],
            deviceNumber='',
            manufacturer=line[6],
            productionDate=line[7],
            productionNumber=line[8],
            modelNumber=line[9],
            evOrder=line[1],
            createAt=datetime.datetime.now().date(),
            createBy=CREATE_BY,
            status=1,
            userLock=0,
        )
        db_session.add(ev_data)


# 添加维保公司
def ceate_maintenance(line, weibao_name, ev_uuid):
    record_uuid = gen_uuid_for_db()
    record_uuid = judge_uuid(record_uuid, db_ev_records_query)
    companyid = db_domain_query.filter_by(name=weibao_name).first()  # 查询维保单位的uuid
    team_info = db_team_query.filter_by(companyId=companyid.uuid, teamName='默认班组').first()
    if not team_info:
        logger.error('此维保公司未分配默认班组，数据导入终止....')
        exit(1)
    if companyid and team_info:
        if not line[4]:
            ev_records = db_ev_records(
                uuid=record_uuid,
                fileNumber=CREATE_BY,
                companyId=companyid.uuid,
                evId=ev_uuid,
                startTime=datetime.datetime.now().date(),
                status=0,
                lastAnnualDate=line[16]
            )
            db_session.add(ev_records)
            db_session.commit()
        else:

            project_info = projectInfo_domain_query.filter(and_(db_projectInfo.name == line[0][:20],
                                                                db_projectInfo.address == line[17])).first()
            ev_info = db_ev_query.filter(and_(db_Ev.regCode == line[4], db_Ev.projectId == project_info.uuid)).first()  # 根据注册代码查询电梯信息表
            if not ev_info:
                with open('维保单位未绑定.csv', 'a') as f:
                    f.write(str(line + '\n'))
                logger.warning('数据库中可能存在相同的项目名并且注册代码一样的数据，{0}手动录入'.format(line[0]))
            else:
                evid = db_ev_records_query.filter_by(evId=ev_uuid, status=0).first()
                if evid:
                    logger.warning('{0}已经绑定过维保公司请确认'.format(line[0]))
                    evid.status = 0
                    db_session.commit()
                else:
                    ev_records = db_ev_records(
                        uuid=record_uuid,
                        fileNumber=CREATE_BY,
                        companyId=companyid.uuid,
                        evId=ev_uuid,
                        startTime=datetime.datetime.now().date(),
                        status=0,
                        lastAnnualDate=line[16]
                    )
                    db_session.add(ev_records)
                    db_session.commit()
        # 添加年检时间

        year_time = db_year_time_query.filter_by(evId=ev_uuid, companyId=companyid.uuid).first()
        if year_time:
            logger.warning('项目{0}，注册代码为{1}的电梯年检时间已经存在，更新'.format(line[0], line[4]))
            year_time.date = line[16]
            db_session.commit()
            time_uuid = gen_uuid_for_db()
            time_uuid = judge_uuid(time_uuid, db_ev_records_query)
            time_data = db_Time(
                uuid=time_uuid,
                evId=ev_uuid,
                fileId=None,
                companyId=companyid.uuid,
                date=line[16]
            )
            db_session.add(time_data)
            db_session.commit()
        else:
            logger.info('项目{0}, 注册代码为{1}的电梯年检时间不存在，新增'.format(line[0], line[4]))
            time_uuid = gen_uuid_for_db()
            time_uuid = judge_uuid(time_uuid, db_ev_records_query)
            time_data = db_Time(
                uuid=time_uuid,
                evId=ev_uuid,
                fileId=None,
                companyId=companyid.uuid,
                date=line[16]
            )
            db_session.add(time_data)
            db_session.commit()
        db_session.commit()

        # 添加年检提醒
        ev_remind_info = db_remind_query.filter_by(evId=ev_uuid, teamid=team_info.uuid).first()
        if not ev_remind_info:
            remind_uuid = gen_uuid_for_db()
            remind_uuid = judge_uuid(remind_uuid, db_remind_query)
            ev_remind = db_ev_remind(
                uuid=remind_uuid,
                evId=ev_uuid,
                teamid=team_info.uuid,
                remind=0
            )
            db_session.add(ev_remind)
            db_session.commit()
        else:
            logger.warning('年检提醒已经存在')


    else:
        logger.error('{0}维保公司不存在，请确认'.format(weibao_name))
        exit(1)


# 更新项目信息

def update_project(project, line):
    project.name = line[0][:20]
    project.createAt = datetime.datetime.now().date()
    project.createBy = CREATE_BY
    project.address = line[4]
    project.latitude = line[5]['latitude']
    project.longitude = line[5]['longitude']
    project.province = line[1]
    project.country = line[3]

    db_session.commit()


# 根据项目名称利用百度地图API查询经纬度118926602749922523
@retry(tries=3, delay=3)
def get_Lat_lon(project_name):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = get_AK(BAIDU_MAP_AK)
    params = {'address': project_name, 'ak': ak, 'output': 'json'}
    html = requests.get(url=url, params=params)
    location = html.json()

    if location['status'] == 0:
        # print(location['result']['location'])
        return location['result']['location']
    else:
        print('未找到关于{}的地址'.format(project_name))
        return ''


# 根据经纬度利用百度地图API查询详细地址
@retry(tries=3, delay=3)
def get_address(location):
    url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = get_AK(BAIDU_MAP_AK)
    if isinstance(location, dict):
        params = {'location': '{lat},{lng}'.format(lat=location['lat'], lng=location['lng']), 'ak': ak, 'output': 'json', 'pois': 1}
        html = requests.get(url=url, params=params)
        address = html.json()
        formatted_address = address['result']['formatted_address']
        address_info = address['result']['addressComponent']
        address_info['address'] = formatted_address

        return address_info
    else:
        return print("请输入正确格式的经纬度({'lng': 104.0529375076847, 'lat': 30.552951548072645})")


# 随机生成uuid
def gen_uuid_for_db():
    return random.randint(100000000000000000, 130000000000000000)


# 判断uuid是否存在

def judge_uuid(uuid, table):
    while True:
        pro_obj_check = table.filter_by(uuid=uuid).first()
        if pro_obj_check:
            uuid = gen_uuid_for_db()
            continue
        else:
            break
    return uuid


# json地址缓存文件项目加密
def project_md5(project: str):
    import hashlib
    return hashlib.md5(project.encode('utf8')).hexdigest()


# json地址缓存返回
def address_dict_json(filename: str):
    import json
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.loads(f.read(), encoding='utf8')
            return data
    except json.decoder.JSONDecodeError:
        print('载入地址缓存文件失败....重新载入')


# 写入json地址缓存
def insert_json(data, filename):
    import json
    import collections
    data = collections.OrderedDict(sorted(data.items()))
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


# 清洗值
def clean_value(value):
    import re
    if value:
        value = str(value)
        value = value[:20]
        value = value.split('（')[0]
        reg = re.compile(r'(?=[\x21-\x7e]+)[^A-Za-z0-9]')
        value = re.sub(reg, '', value)

        return value.strip()
    else:
        print('输入值为空')
        return None


def value_clean(value):
    if not value:
        value = None

        return value
    else:
        return value


# 格式化时间
def clean_time(value):
    import re
    if value:
        value = str(value)
        value = value.split('（')[0]
        reg = re.compile(r'(?=[\x21-\x7e]+)[^A-Za-z0-9]')
        value = re.sub(reg, '-', value).split(' ')[0]

        return value


# 判断字符串是否以中文开头
def check_start_with_chinese(s: str):
    if s:
        return u'\u4e00' <= s[0] <= u'\u9fff'

    return False


# 是否包含中文
def is_contain_chinese(s: str):
    if not s:
        return False

    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True

    return False


# 去除值里面的中文
def remove_spec_char(s: str):
    import re
    regexp = re.compile(r'[^\x00-\x7f]')
    value = re.sub(regexp, '', s)

    return value


# 查询数据库地址id号
def get_area_from_db(province, city, district):
    arg_dict = {
        'province': province,
        'city': city,
        'district': district
    }
    province_id = 0
    city_id = 0
    district_id = 0

    if 'province' in arg_dict and arg_dict['province']:
        v3_area_obj = db_area_query.filter(db_Area.areaName.like(arg_dict['province'] + "%")).first()
        if v3_area_obj:
            province_id = v3_area_obj.uuid

    if 'city' in arg_dict and arg_dict['city']:
        # 兼容直辖市，会同时查出省和市
        v3_area_obj = db_area_query.filter(
            db_Area.areaName.like(arg_dict['city'] + "%")).order_by(db_Area.uuid.desc()).first()

        if v3_area_obj:
            city_id = v3_area_obj.uuid

    if 'district' in arg_dict and arg_dict['district']:
        v3_area_obj = db_area_query.filter(db_Area.areaName.like(arg_dict['district'] + "%")).first()

        if v3_area_obj:
            district_id = v3_area_obj.uuid

    return {
        'province_id': province_id,
        'city_id': city_id,
        'district_id': district_id
    }


# 电梯类型，1:直梯, 2：杂物梯, 3:液压梯, 4:扶梯

ev_type_map = {
    '乘客电梯': 1,
    '特种电梯': 1,
    '载货电梯': 1,
    '医用电梯': 1,
    '车辆电梯': 1,
    '观光电梯': 1,
    '餐梯': 1,
    '自动扶梯与自动人行道': 4,
    '曳引与强制驱动电梯': 1,
    '曳引驱动乘客电梯': 1,
    '液压驱动电梯': 3,
    '强制驱动载货电梯': 1,
    '曳引驱动载货电梯': 1,
    '其它类型电梯': 1,
    '杂物电梯': 2,
    '液压乘客电梯': 3,
    '防爆电梯': 1,
    '自动扶梯': 4,
    '自动人行道': 4,
    '液压载货电梯': 3,
    '其它': 1,
    '病床电梯': 1,
    '': 1
}

# 电梯类型
ev_type = {
        '直梯': 1,
        '杂物梯': 2,
        '液压梯': 3,
        '扶梯': 4
}

usefor = {
    '乘客电梯': 1,
    '住宅电梯': 2,
    '观光电梯': 3,
    '载货电梯': 4,
    '医用电梯': 5,
    '车辆电梯': 6,
    '消防电梯': 7,
    '餐梯': 8,
    '别墅梯': 9,
    '杂物电梯': 10,
    '液压电梯': 11,
    '特种电梯': 12,
    '自动扶梯': 13,
    '自动行人道': 14,
    '其它': 15,
    '病床电梯': 16,
    '': 1
}


if __name__ == '__main__':
    # location = get_Lat_lon('深圳市麻布新村第二工业区')
    # print(location)
    # addrees = get_address(location)
    # print(addrees)
    # address_dict_json(ADDRESS_JSON)
    logger = log()
    logger.info('info信息')
    logger.warning('发挥')