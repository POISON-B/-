#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import random

from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import *
from sqlalchemy.pool import NullPool
from sqlalchemy.sql import func

from lib.config import ttd_db_uri
from twd_db_manager import *
from flask import jsonify


def connect_db():
    db_connect = create_engine(ttd_db_uri, poolclass=NullPool)
    return db_connect


ttd_engine = connect_db()
ttd_metadata = MetaData(ttd_engine)

Table('alarm_info', ttd_metadata, autoload=True)
Table('ev_records', ttd_metadata, autoload=True)
Table('wo_info', ttd_metadata, autoload=True)
Table('ev_info', ttd_metadata, autoload=True)
Table('projectInfo', ttd_metadata, autoload=True)
# Table('area',ttd_metadata,autoload=True)
Table('employee', ttd_metadata, autoload=True)
Table('ev_remind', ttd_metadata, autoload=True)
Table('companyConf', ttd_metadata, autoload=True)
Table('wo_info_status', ttd_metadata, autoload=True)
Table('em_team', ttd_metadata, autoload=True)
Table('team', ttd_metadata, autoload=True)
Table('user', ttd_metadata, autoload=True)
Table('c_workclock', ttd_metadata, autoload=True)
Table('c_elevator', ttd_metadata, autoload=True)
Table('c_evRepair', ttd_metadata, autoload=True)

Base = automap_base(metadata=ttd_metadata)
Base.prepare()

AlarmInfo = Base.classes.alarm_info
EvRecords = Base.classes.ev_records
WoInfo = Base.classes.wo_info
EvInfo = Base.classes.ev_info
ProjectInfo = Base.classes.projectInfo
Employee = Base.classes.employee
EvRemind = Base.classes.ev_remind
CompanyConf = Base.classes.companyConf
WoInfoStatus = Base.classes.wo_info_status
CElevator = Base.classes.c_elevator
CEvRepair = Base.classes.c_evRepair

EmTeam = Base.classes.em_team
Team = Base.classes.team
User = Base.classes.user
C_workclock = Base.classes.c_workclock


# 生成数据库uuid
def get_uuid_for_db():
    return random.randint(100000000, 130000000)


# 判断uuid是否存在
def judge_uuid(uuid, tables):
    while True:
        pro_obj_check = db.session.query(tables).filter_by(uuid=uuid).first()
        if pro_obj_check:
            uuid = get_uuid_for_db()
            continue
        else:
            break
    return uuid


# 获取前12个月日期列表
def get_month_list():
    now = datetime.datetime.now()
    today_year = now.year
    today_month = now.month
    if today_month == 12:
        year_month_list = []
        for i in range(1, 13):
            month = "%s-%s-1" % (today_year, i)
            year_month_list.append(month)
        return year_month_list
    else:
        # print(today_year,today_month)
        last_year = int(now.year) - 1
        today_year_months = range(1, now.month + 1)
        last_year_months = range(now.month + 1, 13)

        date_list_last = []
        for last_year_month in last_year_months:
            date_list = '%s-%s-1' % (last_year, last_year_month)
            date_list_last.append(date_list)
        # print(date_list_last)

        date_list_today = []
        for today_year_month in today_year_months:
            data_list = '%s-%s-1' % (today_year, today_year_month)
            date_list_today.append(data_list)
        # print(date_list_today)
        year_month_list = date_list_last + date_list_today
        return year_month_list


# 获取公司各项目电梯梯量，经纬度
def get_main_com_ev_area_to_db(arg_com_id: int, arg_area_info: list):
    """
    获取维保公司的电梯分布，包括小区名称、梯量、经度、纬度。可以获取指定区域的小区信息。
    :param arg_com_id: 维保公司编号
    :param arg_area_info: 项目所在区域信息，包括省、市、区三个区域编号。字典不为空时，必须提供省编号，市编号和区编号可选
    :return:
    """
    src_session = Session(ttd_engine)
    ev_ids = list()
    pro_ev_num_dict = dict()
    pro_info_dict = dict()
    today = datetime.date.today()
    # 1. 获取公司名下电梯编号列表
    ev_records = src_session.query(EvRecords).with_entities(EvRecords.evId).filter_by(companyId=arg_com_id,
                                                                                      status=0,
                                                                                      endTime=None)
    for er in ev_records:
        ev_ids.append(er.evId)
    query_ev_info = src_session.query(EvInfo.projectId,
                                      ProjectInfo.name,
                                      ProjectInfo.latitude,
                                      ProjectInfo.longitude). \
        join(ProjectInfo, EvInfo.projectId == ProjectInfo.uuid). \
        filter(EvInfo.uuid.in_(ev_ids)).all()

    for ei in query_ev_info:
        pro_info_dict[ei[0]] = {"projectName": ei[1], "latitude": ei[2], "longitude": ei[3]}
        if ei[0] in pro_ev_num_dict:
            # 如果电梯对应项目编号已经存在于字典中，则电梯数量加一
            pro_ev_num_dict[ei.projectId] += 1
        else:
            # 如果电梯对应项目编号不存在于字典中，则增加一个字典元素并设置值为一
            pro_ev_num_dict[ei.projectId] = 1
    # print(query_ev_info)
    # print(pro_ev_num_dict)
    # print(pro_info_dict)
    src_session.close()

    result = db.session.query(func.max(EvArea.row_datetime)).filter(EvArea.org_id == arg_com_id).one()
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]

    if today == max_row_datetime.date():
        pass
    else:
        for pro_id in pro_info_dict:
            new_uuid = get_uuid_for_db()
            uuid = judge_uuid(new_uuid, EvArea)
            project_name = pro_info_dict[pro_id]["projectName"]
            project_lat = pro_info_dict[pro_id]["latitude"]
            project_long = pro_info_dict[pro_id]["longitude"]
            data = EvArea(
                uuid=uuid,
                org_id=arg_com_id,
                row_datetime=today,
                project_name=project_name,
                user_longitude=project_long,
                user_latitude=project_lat,
                ev_num=pro_ev_num_dict[pro_id]

            )
            db.session.add(data)
        db.session.commit()
    # 根据区域来查询电梯数量
    if not arg_area_info:
        pass
    else:
        province_id = arg_area_info[0]
        city_id = arg_area_info[1]
        country_id = arg_area_info[2]

        pro_ids = list(pro_ev_num_dict.keys())
        project_info_dict = dict()

        if province_id and not city_id and not country_id:
            pro_infos = src_session.query(ProjectInfo).filter(ProjectInfo.province == province_id). \
                filter(ProjectInfo.uuid.in_(pro_ids))
        elif province_id and city_id and not country_id:
            pro_infos = src_session.query(ProjectInfo).filter(ProjectInfo.province == province_id). \
                filter(ProjectInfo.city == city_id). \
                filter(ProjectInfo.uuid.in_(pro_ids))
        elif province_id and city_id and country_id:
            pro_infos = src_session.query(ProjectInfo).filter(ProjectInfo.province == province_id). \
                filter(ProjectInfo.city == city_id). \
                filter(ProjectInfo.country == country_id). \
                filter(ProjectInfo.uuid.in_(pro_ids))
        else:
            pro_infos = src_session.query(ProjectInfo).filter(ProjectInfo.uuid.in_(pro_ids))

        for pi in pro_infos:
            project_info_dict[pi.uuid] = pi

        result_pros = list()

        for pro_id, pro_info in project_info_dict.items():
            result_pro = {
                'projectName': pro_info.name,
                'longitude': pro_info.longitude,
                'latitude': pro_info.latitude,
                'evNum': pro_ev_num_dict[pro_id]
            }

            result_pros.append(result_pro)
        return result_pros


# 获取每月报警次数
def get_month_alarm_to_db(arg_com_id: int):
    src_session = Session(ttd_engine)
    result = db.session.query(func.max(AlarmNum.row_datetime)).filter(AlarmNum.org_id == arg_com_id).first()
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]

    evid_list = list()
    query_ev_records = src_session.query(EvRecords).filter(and_(EvRecords.companyId == arg_com_id,
                                                                EvRecords.status == 0,
                                                                EvRecords.endTime == None)).all()
    for re in query_ev_records:
        evid_list.append(re.evId)

    query_alarm_info = src_session.query(AlarmInfo).filter(and_(AlarmInfo.createAt >= max_row_datetime,
                                                                AlarmInfo.evId.in_(evid_list))).all()

    print(len(query_alarm_info))
    month_dict = dict()
    for i in query_alarm_info:
        month = i.createAt.strftime('%Y-%m-01')
        if month in month_dict:
            month_dict[month] += 1
        else:
            month_dict[month] = 1
    # print(month_dict)
    src_session.close()
    # api_tsd_logger.info("month_dict-%s" % month_dict)

    for j in month_dict.keys():
        if datetime.datetime.strptime(j, "%Y-%m-%d") == max_row_datetime:
            query_alarm_num = AlarmNum.query.filter(and_(AlarmNum.org_id == arg_com_id,
                                                         AlarmNum.row_datetime == max_row_datetime)).first()
            query_alarm_num.alarm_num = month_dict[j]
        else:
            new_uuid = get_uuid_for_db()
            uuid = judge_uuid(new_uuid, AlarmNum)
            data = AlarmNum(
                uuid=uuid,
                org_id=arg_com_id,
                row_datetime=j,
                alarm_num=month_dict[j],

            )
            db.session.add(data)
    db.session.commit()


# 获取公司每月报警来源的次数
def get_month_src_alarm_to_db(arg_com_id: int):
    src_session = Session(ttd_engine)

    result = db.session.query(func.max(AlarmSrcStat.row_datetime)).filter(AlarmSrcStat.org_id == arg_com_id).first()
    # print(result[0])
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]

    today_date = datetime.date.today()
    today_month = today_date.strftime("%Y-%m-1")
    # print(today_month)

    company_evid_list = []
    query_ev_records = src_session.query(EvRecords).filter(and_(EvRecords.companyId == arg_com_id,
                                                                EvRecords.status == 0,
                                                                EvRecords.endTime == None)).all()
    for ev in query_ev_records:
        company_evid_list.append(ev.evId)

    query_alarm_info = src_session.query(AlarmInfo).filter(and_(AlarmInfo.createAt >= today_month,
                                                                AlarmInfo.evId.in_(company_evid_list)
                                                                ,AlarmInfo.alarmType.in_([2,4,5]))).all()
    print(query_alarm_info)
    alarm_type_dict = {}
    for al in query_alarm_info:
        alarm_type = al.alarmType
        # print(alarm_type)
        if alarm_type in alarm_type_dict:
            alarm_type_dict[alarm_type] += 1
        else:
            alarm_type_dict[alarm_type] = 1

    src_session.close()
    print(alarm_type_dict)
    wechat_num = 0
    nano_num = 0
    mix_num = 0
    for j in alarm_type_dict.keys():
        if j == 2:
            wechat_num = alarm_type_dict[j]
        elif j == 4:
            nano_num = alarm_type_dict[j]
        elif j == 5:
            mix_num = alarm_type_dict[j]
    total_num = wechat_num + nano_num + mix_num
    print(total_num)
    # if today_date == max_row_datetime.date():
    #     pass
    # else:
    #     new_uuid = get_uuid_for_db()
    #     uuid = judge_uuid(new_uuid, AlarmSrcStat)
    #     data = AlarmSrcStat(
    #         uuid=uuid,
    #         org_id=arg_com_id,
    #         row_datetime=today_date,
    #         alarm_total=total_num,
    #         alarm_wechat=wechat_num,
    #         alarm_mix=mix_num,
    #         alarm_nano=nano_num,
    #     )
    #     db.session.add(data)
    # db.session.commit()



    today_datetime = datetime.datetime.strptime(today_month, '%Y-%m-%d')
    if today_datetime == max_row_datetime:
        query_alarm_src = \
            AlarmSrcStat.query.filter(and_(AlarmSrcStat.org_id == arg_com_id,
                                           AlarmSrcStat.row_datetime == max_row_datetime)).first()
        query_alarm_src.alarm_total = total_num
        query_alarm_src.alarm_wechat = wechat_num
        query_alarm_src.alarm_mix = mix_num
        query_alarm_src.alarm_nano = nano_num
    else:
        new_uuid = get_uuid_for_db()
        uuid = judge_uuid(new_uuid, AlarmSrcStat)
        data = AlarmSrcStat(
            uuid=uuid,
            org_id=arg_com_id,
            row_datetime=today_datetime,
            alarm_total=total_num,
            alarm_wechat=wechat_num,
            alarm_mix=mix_num,
            alarm_nano=nano_num,
        )
        db.session.add(data)
    db.session.commit()


# 获取公司每月维修保养次数
def get_month_maintan_repair_to_db(arg_com_id: int):
    src_session = Session(ttd_engine)
    result = db.session.query(func.max(RepairMainStat.row_datetime)).filter(RepairMainStat.org_id == arg_com_id).one()
    if result[0] is None:
        max_row_datetime = "1970-01-01"
    else:
        max_row_datetime = result[0]
    workorder_stat_dict = {}
    query_wo_info = src_session.query(WoInfo).filter(and_(WoInfo.date >= max_row_datetime,
                                                          WoInfo.companyId == arg_com_id,
                                                          WoInfo.type.in_([1, 2]))).all()

    for wo in query_wo_info:
        print(wo.date)
        month = wo.date.strftime('%Y-%m-01')
        print(month)
        if month in workorder_stat_dict:
            month_wo_stat = workorder_stat_dict[month]
            if wo.type in month_wo_stat:
                month_wo_stat[wo.type] += 1
            else:
                month_wo_stat[wo.type] = 1
        else:
            workorder_stat_dict[month] = {}
            workorder_stat_dict[month][wo.type] = 1

    print(workorder_stat_dict)
    src_session.close()

    for ws_datetime, ws_value in workorder_stat_dict.items():
        ev_num_maintenance = ws_value[1] if 1 in ws_value else 0
        ev_num_repair = ws_value[2] if 2 in ws_value else 0
        trans_date = datetime.datetime.strptime(ws_datetime, "%Y-%m-%d")
        if trans_date == max_row_datetime:
            query_repair_main = RepairMainStat.query.filter(and_(RepairMainStat.row_datetime == max_row_datetime,
                                                                 RepairMainStat.org_id == arg_com_id)).first()
            print(query_repair_main.org_id)
            query_repair_main.ev_num_repair = ev_num_repair
            query_repair_main.ev_num_maintenance = ev_num_maintenance

        else:
            new_uuid = get_uuid_for_db()
            uuid = judge_uuid(new_uuid, RepairMainStat)
            data = RepairMainStat(
                uuid=uuid,
                org_id=arg_com_id,
                row_datetime=ws_datetime,
                ev_num_repair=ev_num_repair,
                ev_num_maintenance=ev_num_maintenance,
            )

            db.session.add(data)
    db.session.commit()


# 获取公司今日维修保养次数
def get_work_overview_to_db(arg_com_id: int):
    src_session = Session(ttd_engine)
    today = datetime.date.today()
    result = db.session.query(func.max(WorkOverview.row_datetime)).filter(WorkOverview.org_id == arg_com_id).one()
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]
    # 从原始数据库读取数据
    company_evid_list = []
    query_ev_records = src_session.query(EvRecords).filter(and_(EvRecords.companyId == arg_com_id,
                                                                EvRecords.status == 0,
                                                                EvRecords.endTime == None)).all()
    for ev in query_ev_records:
        company_evid_list.append(ev.evId)
    # mainten_repair_dict = {}
    # query_wo_info = src_session.query(WoInfo).outerjoin(C_workclock,and_(WoInfo.uuid == C_workclock.woId))\
    #                            .filter(and_(WoInfo.date >= today, WoInfo.companyId == arg_com_id,
    #                                         C_workclock.startTime is not None, C_workclock.endTime is not None,
    #                                         WoInfo.type.in_([1,2]))).all()
    #获取当日保养电梯数
    query_wo_info_main = src_session.query(CElevator.evId).join(WoInfo,and_(WoInfo.uuid == CElevator.woId))\
        .filter(WoInfo.date>=today,WoInfo.type == 1, CElevator.evId.in_(company_evid_list)).group_by(CElevator.evId).all()
    evListMain=list()
    for elev in query_wo_info_main:
        evListMain.append(elev.evId)
    ev_mian=len(evListMain)
    # print('ev_mian= ',ev_mian)
    #获取当日维修电梯数
    query_wo_info_repair = src_session.query(CElevator.evId).join(WoInfo,and_(WoInfo.uuid == CElevator.woId))\
        .filter(WoInfo.date>=today,WoInfo.type == 2, CElevator.evId.in_(company_evid_list)).group_by(CElevator.evId).all()
    evListRepair=list()
    for elev in query_wo_info_repair:
        evListRepair.append(elev.evId)
    ev_repair=len(evListRepair)
    # print('ev_repair= ',ev_repair)
    if today == max_row_datetime.date():
        query_work_overview = WorkOverview.query.filter(and_(WorkOverview.org_id == arg_com_id,
                                                             WorkOverview.row_datetime == max_row_datetime)).first()
        query_work_overview.ev_num_repair = ev_repair
        query_work_overview.ev_num_maintenance = ev_mian
    else:
        new_uuid = get_uuid_for_db()
        uuid = judge_uuid(new_uuid, WorkOverview)
        data = WorkOverview(
            uuid=uuid,
            row_datetime=datetime.date.today(),
            org_id=arg_com_id,
            ev_num_repair=ev_repair,
            ev_num_maintenance=ev_mian
        )
        db.session.add(data)
    db.session.commit()

    # print(query_wo_info)
    # for wo in query_wo_info_main:
    #     if wo.type in mainten_repair_dict:
    #         mainten_repair_dict[wo.type] += 1
    #     else:
    #         mainten_repair_dict[wo.type] = 1
    # print(mainten_repair_dict)
    #
    # src_session.close()
    #
    # ev_num_repair = mainten_repair_dict[2] if 2 in mainten_repair_dict else 0
    # ev_num_maintenance = mainten_repair_dict[1] if 1 in mainten_repair_dict else 0
    #
    # if today == max_row_datetime.date():
    #     query_work_overview = WorkOverview.query.filter(and_(WorkOverview.org_id == arg_com_id,
    #                                                          WorkOverview.row_datetime == max_row_datetime)).first()
    #     query_work_overview.ev_num_repair = ev_num_repair
    #     query_work_overview.ev_num_maintenance = ev_num_maintenance
    # else:
    #     new_uuid = get_uuid_for_db()
    #     uuid = judge_uuid(new_uuid, WorkOverview)
    #     data = WorkOverview(
    #         uuid=uuid,
    #         row_datetime=datetime.date.today(),
    #         org_id=arg_com_id,
    #         ev_num_repair=ev_num_repair,
    #         ev_num_maintenance=ev_num_maintenance
    #     )
    #     db.session.add(data)
    # db.session.commit()


# 获取公司电梯和员工总数
def get_company_info_to_db(arg_com_id: int):
    src_session = Session(ttd_engine)

    today_date = datetime.date.today()
    result = db.session.query(func.max(OrgOverview.row_datetime)).filter(OrgOverview.org_id == arg_com_id).one()
    # print(result[0])
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]
    ev_num = []
    em_num = []
    rows_ev_num = src_session.query(EvRecords).filter_by(companyId=arg_com_id, status=0, endTime=None).all()
    rows_em_num = src_session.query(User).filter_by(companyId=arg_com_id).all()
    for i in rows_ev_num:
        ev_id = i.uuid
        ev_num.append(ev_id)
    for j in rows_em_num:
        em_id = j.uuid
        em_num.append(em_id)
    elev_num = len(ev_num)
    emp_num = len(em_num)

    src_session.close()
    if max_row_datetime.date() == today_date:
        query_org_overview = OrgOverview.query.filter(and_(OrgOverview.row_datetime == max_row_datetime,
                                                           OrgOverview.org_id == arg_com_id)).first()
        query_org_overview.ev_total = elev_num
        query_org_overview.Employee_total = emp_num
    else:
        new_uuid = get_uuid_for_db()
        uuid = judge_uuid(new_uuid, OrgOverview)
        data = OrgOverview(
            uuid=uuid,
            row_datetime=datetime.date.today(),
            org_id=arg_com_id,
            ev_total=elev_num,
            Employee_total=emp_num
        )
        db.session.add(data)
    db.session.commit()


# 获取公司电梯年检时间
def get_ev_annual_info_to_db(arg_com_id: int):
    src_session = Session(ttd_engine)
    result = db.session.query(func.max(AnnualInfo.row_datetime)).filter(AnnualInfo.org_id == arg_com_id).one()
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]

    # 查询电梯id和年检信息
    ev_annual_dict = dict()
    ev_id_list = list()
    query_ev_id = src_session.query(EvRecords).filter(EvRecords.companyId == arg_com_id,
                                                      EvRecords.status == 0,
                                                      EvRecords.endTime == None).all()
    for ev in query_ev_id:
        ev_id_list.append(ev.evId)
        ev_annual_dict[ev.evId] = {"annual": ev.lastAnnualDate}
    # print(ev_annual_dict)

    # 查询到项目id，电梯维特号，电梯梯号
    ev_info_dict = dict()
    pro_id_list = list()
    query_ev_info = src_session.query(EvInfo).filter(EvInfo.uuid.in_(ev_annual_dict)).all()

    for ei in query_ev_info:
        pro_id_list.append(ei.projectId)
        ev_info_dict[ei.uuid] = {"wtCode": ei.wtCode, "evOrder": ei.evOrder, "projectId": ei.projectId}
    # print(ev_info_dict)
    # print(len(ev_info_dict))
    # print(len(ev_annual_dict))

    pro_info_dict = dict()
    query_project_info = src_session.query(ProjectInfo).filter(ProjectInfo.uuid.in_(pro_id_list)).all()
    for pr in query_project_info:
        pro_info_dict[pr.uuid] = pr.name

    # print(pro_info_dict)
    # print(len(pro_info_dict))
    src_session.close()

    today_date = datetime.date.today()
    if today_date == max_row_datetime.date():
        pass
    else:
        for i in ev_annual_dict:
            last_annual = ev_annual_dict[i]["annual"]
            ev_order = ev_info_dict[i]["evOrder"]
            wt_code = ev_info_dict[i]["wtCode"]
            project_name = pro_info_dict[ev_info_dict[i]["projectId"]]
            if last_annual is not None:
                year = last_annual.year
                month = last_annual.month
                day = last_annual.day
                next_year = "%s-%s-%s" % ((year + 1), month, day)
                next_year_time = datetime.datetime.strptime(next_year, '%Y-%m-%d')
                expire_day = (next_year_time.date() - today_date).days

                if today_date >= next_year_time.date():
                    annual_status = "已超期"
                elif 0 < expire_day <= 31:
                    annual_status = "即将超期"
                else:
                    annual_status = "未超期"
                new_uuid = get_uuid_for_db()
                uuid = judge_uuid(new_uuid, AnnualInfo)
                data = AnnualInfo(
                    uuid=uuid,
                    row_datetime=today_date,
                    org_id=arg_com_id,
                    project_name=project_name,
                    ev_order=ev_order,
                    wt_code=wt_code,
                    lastAnnualDate=last_annual,
                    annualstatus=annual_status,

                )
                db.session.add(data)
        db.session.commit()


# 获取公司今日任务总览
def get_task_overview_to_db(arg_com_id: int):
    result = db.session.query(func.max(TaskOverview.row_datetime)).filter(TaskOverview.org_id == arg_com_id).one()
    if result[0] is None:
        max_row_datetime = datetime.datetime.strptime('1970-01-01', '%Y-%m-%d')
    else:
        max_row_datetime = result[0]

    src_session = Session(ttd_engine)

    ev_id_list = list()
    query_ev_id = src_session.query(EvRecords).filter(EvRecords.companyId == arg_com_id,
                                                      EvRecords.status == 0).all()
    for ev in query_ev_id:
        ev_id_list.append(ev.evId)

    ev_last_date_dict = dict()
    query_ev_remind = src_session.query(EvRemind).filter(EvRemind.evId.in_(ev_id_list)).all()
    for er in query_ev_remind:
        ev_last_date_dict[er.evId] = er.lastDate
    # print(ev_last_date_dict)

    query_company_conf = src_session.query(CompanyConf).filter(CompanyConf.companyId == arg_com_id).first()
    today = datetime.date.today()
    today_mainten_num = 0
    if not query_company_conf:
        return

    # 保养周期
    MAIN_DAY = 15
    mainten_period = query_company_conf.mtcRemind if query_company_conf.mtcRemind else MAIN_DAY

    for i in ev_last_date_dict:
        if ev_last_date_dict[i] is None:
            continue
        elif (today - ev_last_date_dict[i]).days == mainten_period:
            today_mainten_num += 1

    query_wo_info_status = src_session.query(WoInfoStatus).filter(and_(WoInfoStatus.updateAt >= today,
                                                                       WoInfoStatus.evId.in_(ev_id_list),
                                                                       WoInfoStatus.woType.in_([1,2])
                                                            )).all()
    print(len(query_wo_info_status))
    mainten_complete_set = set()
    mainten_ing_set = set()
    repair_complete_set = set()
    for qw in query_wo_info_status:
        wo_type = qw.woType
        end_date = qw.endDate
        ev_id = qw.evId
        if wo_type == 1 and end_date :
            mainten_complete_set.add(ev_id)
        elif wo_type == 1 and not end_date:
            mainten_ing_set.add(ev_id)
        elif wo_type == 2 and end_date:
            repair_complete_set.add(ev_id)
        else:
            pass

    repair_complete_num = len(repair_complete_set)
    mainten_complete_num = len(mainten_complete_set)
    mainten_ing_num = len(mainten_ing_set)


    # for wo in query_wo_info_status:
    #     wo_type = wo.woType
    #     end_date = wo.endDate
    #
    #     if wo_type == 2:
    #         repair_complete_num += 1 if end_date else 0
    #     elif wo_type == 1:
    #         if end_date:
    #             mainten_complete_num += 1
    #         else:
    #             mainten_ing_num += 1
    #     else:
    #         pass

    src_session.close()

    if today == max_row_datetime.date():
        query_task = TaskOverview.query.filter(and_(TaskOverview.org_id == arg_com_id,
                                                    TaskOverview.row_datetime == max_row_datetime)).first()
        query_task.task_num = today_mainten_num
        query_task.complete_task = mainten_complete_num
        query_task.incomplete_task = mainten_ing_num
        query_task.fault_task = repair_complete_num
        # pass
    else:
        new_uuid = get_uuid_for_db()
        uuid = judge_uuid(new_uuid, TaskOverview)
        data = TaskOverview(
            uuid=uuid,
            row_datetime=today,
            org_id=arg_com_id,
            task_num=today_mainten_num,
            complete_task=mainten_complete_num,
            incomplete_task=mainten_ing_num,
            fault_task=repair_complete_num

        )
        db.session.add(data)
    db.session.commit()


# 获取工单详情
def get_work_order_info(arg_com_id: int):
    # 获取公司电梯信息
    src_session = Session(ttd_engine)
    ev_annual_dict = dict()
    ev_id_list = list()
    query_ev_id = src_session.query(EvRecords).filter(EvRecords.companyId == arg_com_id,
                                                      EvRecords.status == 0,
                                                      EvRecords.endTime == None).all()
    for ev in query_ev_id:
        ev_id_list.append(ev.evId)
        ev_annual_dict[ev.evId] = {"annual": ev.lastAnnualDate}

    # 获取工单状态信息
    today_date = datetime.date.today()
    # query_wo_info = src_session.query(WoInfoStatus.evId, WoInfoStatus.woType, WoInfoStatus.startDate,
    #                                   WoInfoStatus.endDate, EvInfo.evOrder, Team.teamName,
    #                                   ProjectInfo.name.label('projectName'), User.name.label('userName')) \
    #     .join(User, and_(WoInfoStatus.userId == User.uuid)) \
    #     .join(EvInfo, and_(WoInfoStatus.evId == EvInfo.uuid)) \
    #     .join(ProjectInfo, and_(EvInfo.projectId == ProjectInfo.uuid)) \
    #     .join(Employee, and_(WoInfoStatus.userId == Employee.userId)) \
    #     .join(EmTeam, and_(Employee.uuid == EmTeam.emId)) \
    #     .join(Team, and_(EmTeam.teamId == Team.uuid)) \
    #     .filter(and_(WoInfoStatus.updateAt >= today_date,
    #                  WoInfoStatus.evId.in_(ev_id_list))).all()

    query_wo_info = src_session.query(WoInfoStatus.evId, WoInfoStatus.woType, WoInfoStatus.startDate,
                                      WoInfoStatus.endDate, EvInfo.evOrder, Team.teamName,
                                      ProjectInfo.name.label('projectName'), User.name.label('userName')) \
        .join(User, and_(WoInfoStatus.userId == User.uuid)) \
        .join(EvInfo, and_(WoInfoStatus.evId == EvInfo.uuid)) \
        .join(ProjectInfo, and_(EvInfo.projectId == ProjectInfo.uuid)) \
        .join(EvRemind,and_(WoInfoStatus.evId == EvRemind.evId))\
        .join(Team, and_(EvRemind.teamid == Team.uuid))\
        .filter(and_(WoInfoStatus.updateAt >= today_date,
                     WoInfoStatus.evId.in_(ev_id_list),
                     WoInfoStatus.woType.in_([1,2]))).all()

    src_session.close()
    # print(query_wo_info)
    if not query_wo_info:

        return
    wo_info_list = list()
    for wo_ids in query_wo_info:
        wo_info_list.append([wo_ids.evId,{"woType": wo_ids.woType,
                                     "startDate": wo_ids.startDate,
                                     "endDate": wo_ids.endDate,
                                     "evOrder": wo_ids.evOrder,
                                     "teamName": wo_ids.teamName,
                                     "projectName": wo_ids.projectName,
                                     "userName": wo_ids.userName}])
    # print(wo_info_list)
    if not wo_info_list:

        return
    for wo in wo_info_list:
        # print(wo[0],wo[1])
        username = wo[1]["userName"]
        team_name = wo[1]["teamName"]
        project_name = wo[1]["projectName"]
        ev_order = wo[1]["evOrder"]
        start_time = wo[1]["startDate"]
        end_time = wo[1]["endDate"]
        wo_type = wo[1]["woType"]
        wo_type_name = "保养" if wo_type == 1 else "维修"
        state = '已完成' if start_time is not None and end_time is not None else '进行中'
        new_uuid = get_uuid_for_db()
        uuid = judge_uuid(new_uuid, WorkInfo)
        data = WorkInfo(
            uuid=uuid,
            row_datetime=today_date,
            org_id=arg_com_id,
            ev_order=ev_order,
            team=team_name,
            type=wo_type_name,
            project_name=project_name,
            employee=username,
            start_time=start_time,
            end_time=end_time,
            status=state,
            exception=''
        )
        db.session.add(data)
    db.session.commit()


def make_api_respone(code: int, msg: str):
    return {'code': code, 'message': msg}


def print_enter_func(func_name: str):
    logger.debug("Enter function: %s" % func_name)


def print_exit_func(func_name: str):
    logger.debug("Exit function: %s" % func_name)
