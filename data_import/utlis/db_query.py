# #!/usr/bin/env python3
# # -*- coding: utf-8 -*-
# # @Time    : 18-8-14 下午3:33
# # @Author  : Shark
# # @Site    :
# # @File    : db_query.py
# # @Software: PyCharm
import Levenshtein
import difflib
from datetime import datetime

from config import CREATE_BY, ERROR_FILE_PATH
from utlis import db_area_query, db_Area, db_brand_query, db_projectInfo, projectInfo_domain_query, db_session, db_Ev, \
    db_ev_conf_query, db_EvConf, db_eh_conf_query, db_EhConf, db_es_conf_query, db_EsConf, db_ev_records_query, \
    db_ev_records, db_year_time_query, db_Time, db_remind_query, db_ev_remind, db_ev_query
from utlis.utils import gen_uuid_for_db, judge_uuid


lift_conf_dict = dict()


def project_address_id_query(data):
    """
    项目地址id查询

    :param data:   项目地址信息
    :return:   地址id
    """

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


def brand_id_query(data):
    """
    电梯品牌查询

    :param data: 电梯品牌信息
    :return:  品牌id
    """
    return db_brand_query.filter_by(name=data['brandId']).first()


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

    return {k: project.uuid}


def create_project(k, value):
    """
    创建项目

    :param value: 项目信息
    :param k: 项目名
    :return: None
    """
    uuid = gen_uuid_for_db()
    uuid = judge_uuid(uuid, projectInfo_domain_query)
    project = db_projectInfo(
        uuid=uuid,
        name=k,
        address=value['project_address'],
        latitude=value['ln_la']['lat'],
        longitude=value['ln_la']['lng'],
        province=value['project_province'],
        city=value['project_city'],
        country=value['project_country'],
        createBy=CREATE_BY,
        createAt=datetime.now().date()
    )

    db_session.add(project)
    db_session.commit()

    return {k: uuid}


def project_judge_create(k, value):
    """
    查询项目，如果有则更新，没有则新增
    :param k: 项目名字
    :param value: 项目具体信息
    :return: 项目uuid
    """
    name = projectInfo_domain_query.filter(db_projectInfo.name.like('%' + k)).all()
    if len(name) == 1:
        updata_project(k, value)
        return None
    if len(name) > 1:
        for info in name:
            number = difflib.SequenceMatcher(None, k, info.name).ratio()
            if number >= 0.7:  # 可能需要添加地址判断
                updata_project(k, value)
    else:
        create_project(k, value)


def update_lift(lift, value):
    """
    电梯信息更新
    :param value:电梯信息
    :return:
    """
    lift.brandId = value['brandId']
    lift.useFor = value['useFor']
    lift.type = value['useFor']
    lift.deviceNumber = value['deviceNumber']
    lift.manufacturer = value['manufacturer']
    lift.productionDate = value['productionDate']
    lift.productionNumber = value['productionNumber']
    lift.modelNumber = value['modelNumber']
    lift.evOrder = value['evOrder']
    lift.createAt = datetime.now().date()
    lift.createBy = CREATE_BY
    lift.status = 0
    lift.userLock = 2

    db_session.commit()

    return lift.uuid


def create_lift(k, value, project):
    """
    创建电梯信息基本
    :param k: 项目名
    :param value: 电梯信息
    :param project: 项目uuid信息
    :return:
    """
    uuid = gen_uuid_for_db()
    uuid = judge_uuid(uuid, db_ev_query)
    lift = db_Ev(
        uuid=uuid,
        projectId=project[k][k],
        brandId=value['brandId'],
        regCode=value['regCode'],
        useFor=value['useFor'],
        type=value['useFor'],
        deviceNumber=value['deviceNumber'],
        manufacturer=value['manufacturer'],
        productionDate=value['productionDate'],
        productionNumber=value['productionNumber'],
        modelNumber=value['modelNumber'],
        evOrder=value['evOrder'],
        createAt=datetime.now().date(),
        createBy=CREATE_BY,
        status=0,
        userLock=2,
    )

    db_session.add(lift)
    db_session.commit()

    return uuid


def create_lift_zhi_conf(evid, value):
    """
    直梯参数信息

    :param evid: 电梯uuid
    :param value:  直梯参数
    :return:
    """
    info = db_ev_conf_query.filter_by(evId=evid).first()
    if info:
        info.floors = value['lift_parameter']['floors'] or None
        info.station = value['lift_parameter']['station'] or None
        info.door = value['lift_parameter']['door'] or None
        info.maxLoad = value['lift_parameter']['maxLoad'] or None
        info.speed = value['lift_parameter']['speed'] or None
    else:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, db_ev_conf_query)
        confi_zhi = db_EvConf(
            uuid=uuid,
            evId=evid,
            actuationForm=value['lift_parameter']['actuationForm'],
            floors=value['lift_parameter']['floors'],
            station=value['lift_parameter']['station'],
            door=value['lift_parameter']['door'],
            maxLoad=value['lift_parameter']['maxLoad'],
            speed=value['lift_parameter']['speed']
        )
        db_session.add(confi_zhi)
    db_session.commit()


def create_lift_yei_conf(evid, value) :
    """
    液压梯参数信息

    :param evid: 电梯uuid
    :param value: 液压梯参数
    :return:
    """
    info = db_eh_conf_query.filter_by(evId=evid).first()
    if info:
        info.floors = value['lift_parameter']['floors'] or None
        info.station = value['lift_parameter']['station'] or None
        info.door = value['lift_parameter']['door'] or None
        info.maxLoad = value['lift_parameter']['maxLoad'] or None
        info.speedUp = value['lift_parameter']['speed'] or None
        info.speedDown = value['lift_parameter']['speedDown'] or None
        info.hydraulicCylinder = value['lift_parameter']['hydraulicCylinder'] or None
        info.jackingType = value['lift_parameter']['jackingType'] or None
    else:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, db_ev_conf_query)
        confi_yei = db_EhConf(
            uuid=uuid,
            evId=evid,
            actuationForm=value['lift_parameter']['actuationForm'],
            floors=value['lift_parameter']['floors'],
            station=value['lift_parameter']['station'],
            door=value['lift_parameter']['door'],
            maxLoad=value['lift_parameter']['maxLoad'],
            speedUp=value['lift_parameter']['speed'],
            speedDown=value['lift_parameter']['speedDown'],
            hydraulicCylinder = value['lift_parameter']['hydraulicCylinder'],
            jackingType = value['lift_parameter']['jackingType'],
        )
        db_session.add(confi_yei)
    db_session.commit()


def create_lift_fu_conf(evid, value):
    """
    扶梯参数信息

    :param evid: 电梯uuid
    :param value: 扶梯参数
    :return:
    """
    info = db_es_conf_query.filter_by(evId=evid).first()
    if info:
        info.nominalSpeed = value['lift_parameter']['nominalSpeed'] or None
        info.nominalWidth = value['lift_parameter']['nominalWidth'] or None
        info.inclinationAngle = value['lift_parameter']['inclinationAngle'] or None
        info.transforAbility = value['lift_parameter']['transforAbility'] or None
        info.liftingHeight = value['lift_parameter']['liftingHeight'] or None
        info.length = value['lift_parameter']['length'] or None
        info.power = value['lift_parameter']['power'] or None
    else:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, db_ev_conf_query)
        confi_fu = db_EsConf(
            uuid=uuid,
            evId=evid,
            nominalSpeed=value['lift_parameter']['nominalSpeed'],
            nominalWidth=value['lift_parameter']['nominalWidth'],
            inclinationAngle=value['lift_parameter']['inclinationAngle'],
            transforAbility=value['lift_parameter']['transforAbility'],
            liftingHeight=value['lift_parameter']['liftingHeight'],
            length=value['lift_parameter']['length'],
            power=value['lift_parameter']['power'],
        )
        db_session.add(confi_fu)
    db_session.commit()


lift_conf_dict[1] = create_lift_zhi_conf
lift_conf_dict[3] = create_lift_yei_conf
lift_conf_dict[4] = create_lift_fu_conf


def create_wb(evid, value, wbid):
    """
    添加维保单位

    :param evid: 电梯uuid
    :param value: 电梯信息
    :param wbid: 维保单位uuid
    :return:
    """
    info = db_ev_records_query.fiert_by(evId=evid, companyId=wbid, status=0).first()
    if not info:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, db_ev_records_query)
        we_bao = db_ev_records(
            uuid=uuid,
            fileNumber=CREATE_BY,
            companyId=wbid,
            evId=evid,
            startTime=datetime.now().date(),
            status=0,
            lastAnnualDate=value['lastAnnualDate']
        )

        db_session.add(we_bao)
        db_session.commit()


def create_yertime(evid, value, wbid):
    """
    电梯年检时间查询 添加 更新

    :param evid: 电梯uuid
    :param value: 电梯信息
    :param wbid: 维保单位uuid
    :return:
    """
    year_time = db_year_time_query.filter_by(evId=evid, companyId=wbid).first()
    if year_time:
        year_time.evId = evid,
        year_time.fileId = CREATE_BY,
        year_time.companyId = wbid,
        year_time.date = value['lastAnnualDate']

    else:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, db_ev_records_query)
        time = db_Time(
            uuid=uuid,
            evId=evid,
            fileId=CREATE_BY,
            companyId=wbid,
            date=value['lastAnnualDate']
        )
        db_session.add(time)
    db_session.commit()


def create_time_remind(evid, temid):
    """
    保养提醒

    :param evid: 电梯uuid
    :param temid: 默认班组uuid
    :return:
    """
    remind_info = db_remind_query.filter_by(evId=evid, teamid=temid).first()
    if remind_info:
        remind_info.evId = evid
        remind_info.teamid = temid
        remind_info.remind = 0

    else:
        uuid = gen_uuid_for_db()
        uuid = judge_uuid(uuid, db_remind_query)
        ev_remind = db_ev_remind(
            uuid=uuid,
            evId=evid,
            teamid=temid,
            remind=0
        )
        db_session.add(ev_remind)
        db_session.commit()


def lift_judge_create(k, value, project, wbid, temid):
    """
    查询电梯，如果有更新，没有新增
    :param k: 项目名和电梯注册码
    :param value: 电梯信息
    :param project: 项目的uuid信息
    :return:
    """
    k = k.split('+')[0]
    if value['regCode']:
        evid = create_lift(k, value, project)
        lift_conf_dict[value['useFor']](evid, value)
        create_wb(evid, value, wbid)
        create_yertime(evid, value, wbid)
        create_time_remind(evid, temid)

    else:
        lift = db_ev_query.filter_by(regCode=value['regCode']).all()
        if lift > 1:
            print('注册码存在冲突，查看文件')
            with open(ERROR_FILE_PATH, 'a') as f:
                f.write(str(value) + '\n')

        elif lift.projectId == project[k][k]:
            evid = update_lift(lift, value)
            lift_conf_dict[value['useFor']](evid, value)
            create_wb(evid, value, wbid)
            create_yertime(evid, value, wbid)
            create_time_remind(evid, temid)

        else:
            evid = create_lift(k, value, project)
            lift_conf_dict[value['useFor']](evid, value)
            create_wb(evid, value, wbid)
            create_yertime(evid, value, wbid)
            create_time_remind(evid, temid)
