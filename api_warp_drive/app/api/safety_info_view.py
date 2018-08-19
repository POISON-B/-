#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-18 下午1:04
# @Author  : Shark
# @File    : safety_info_view.py
# @Software: PyCharm
import datetime
from flask import request

from app.modles.base_info_query import *
from app.utils.utils import return_result
from lib.util import *
from lib.request_pre_check import *
from . import api, ARG_FLAG_ORG_ID, pm

# 必须在最后加载
import inspect


@api.route("/getTodayWorkOverview", methods=['GET'])
def get_today_work_overview():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)
    print(result[0])
    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')

    today_date = datetime.date.today()
    get_work_overview_to_db(company_id)
    query_work_overview = WorkOverview.query.filter(and_(WorkOverview.row_datetime >= today_date,
                                                         WorkOverview.org_id == company_id)).first()

    if not query_work_overview:
        result = return_result(company_id=company_id, today_date=today_date, token=token)
        print_exit_func(func_name)
        return jsonify(result)

    date = str(query_work_overview.row_datetime.date())
    repair_num = query_work_overview.ev_num_repair
    mainten_num = query_work_overview.ev_num_maintenance

    result = return_result(company_id=company_id, data=date, repairTask=repair_num, maintenanceTask=mainten_num, token=token)

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getRepairMainStat", methods=['GET'])
def get_repair_main_stat():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)

    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')
    get_month_maintan_repair_to_db(company_id)
    query_repair_main = RepairMainStat.query.filter(RepairMainStat.org_id == company_id). \
        order_by(RepairMainStat.row_datetime).all()

    repair = list()
    mainten = list()

    last_tw_month = get_month_list()
    if not query_repair_main:
        for tm in last_tw_month:
            month = tm.split('-')[1]
            repair.append({"name": month, "value": 0})
            mainten.append({"name": month, "value": 0})
        result = return_result(companyId=company_id, month={"repair": repair, "maintenance": mainten}, token=token)

        print_exit_func(func_name)
        return jsonify(result)

    # print(last_tw_month)
    # for qr in query_repair_main:
    #     # print(qr.row_datetime,qr.ev_num_repair,qr.ev_num_maintenance)
    #     repair.append({"name": qr.row_datetime.strftime('%Y-%m'), "value": qr.ev_num_repair})
    #     mainten.append({"name": qr.row_datetime.strftime('%Y-%m'), "value": qr.ev_num_maintenance})
    month_mainten_repair = dict()
    for qr in query_repair_main:
        month_mainten_repair[qr.row_datetime] = {"repair": qr.ev_num_repair, "mainten": qr.ev_num_maintenance}

    for tm in last_tw_month:
        month = tm.split('-')[1]
        tm_date = datetime.datetime.strptime(tm, '%Y-%m-%d')
        if tm_date in month_mainten_repair:
            repair.append({"name": month, "value": month_mainten_repair[tm_date]['repair']})
            mainten.append({"name": month, "value": month_mainten_repair[tm_date]['mainten']})
        else:
            repair.append({"name": month, "value": 0})
            mainten.append({"name": month, "value": 0})

    result = return_result(companyId=company_id, month={"repair": repair, "maintenance": mainten}, token=token)

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getCompanyOverview", methods=['GET'])
def get_company_overview():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)

    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')
    today_date = datetime.date.today()
    get_company_info_to_db(company_id)
    query_org_overview = OrgOverview.query.filter(and_(OrgOverview.org_id == company_id,
                                                       OrgOverview.row_datetime >= today_date)).first()
    if not query_org_overview:
        result = return_result(companyId=company_id, date=today_date, token=token)

        print_exit_func(func_name)
        return jsonify(result)

    date = str(query_org_overview.row_datetime.date())
    total_elevators = query_org_overview.ev_total
    total_employees = query_org_overview.Employee_total

    result = return_result(companyId=company_id, date=date, totalElevators=total_elevators,
                           totalEmployees=total_employees, token=token)

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getAlarmNum", methods=['GET'])
def get_alarm_num():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)

    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')
    get_month_alarm_to_db(company_id)
    query_alarm_info = AlarmNum.query.filter(AlarmNum.org_id == company_id).order_by(AlarmNum.row_datetime).all()
    alarm_info_list = list()
    last_tw_month = get_month_list()
    if not query_alarm_info:
        for tm in last_tw_month:
            month = tm.split('-')[1]
            alarm_info_list.append({"name": month, "value": 0})

        result = return_result(companyId=company_id, month={"alarmNum": alarm_info_list}, token=token)

        print_exit_func(func_name)
        return jsonify(result)

    # for qa in query_alarm_info:
    #     alarm_info_list.append({"name": qa.row_datetime.strftime('%Y-%m'), "value": qa.alarm_num})
    #     # print(qa.row_datetime)
    last_tw_month = get_month_list()
    month_alarm_dict = dict()
    for qa in query_alarm_info:
        month_alarm_dict[qa.row_datetime] = {"alarm_num": qa.alarm_num}

    for tm in last_tw_month:
        month = tm.split('-')[1]
        tm_date = datetime.datetime.strptime(tm,'%Y-%m-%d')
        if tm_date in month_alarm_dict:
            alarm_info_list.append({"name": month, "value": month_alarm_dict[tm_date]['alarm_num']})

        else:
            alarm_info_list.append({"name": month, "value":0})

    result = return_result(companyId=company_id, month={"alarmNum": alarm_info_list}, token=token)

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getCurrMonthAlarmStatSource", methods=['GET'])
def get_curr_month_alarm_stat_source():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)

    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')
    today_date = datetime.date.today()
    today_month = today_date.strftime("%Y-%m")
    today_month_day = today_date.strftime("%Y-%m-1")

    get_month_src_alarm_to_db(company_id)
    query_alarm_src = AlarmSrcStat.query.filter(and_(AlarmSrcStat.row_datetime >= today_month_day,
                                                     AlarmSrcStat.org_id == company_id)).first()

    if not query_alarm_src:
        result = return_result(companyId=company_id, date=today_month, source={"wechat": 0, "mix": 0, "nano": 0}, token=token)

        print_exit_func(func_name)
        return jsonify(result)

    total_num = query_alarm_src.alarm_total
    wechat_num = query_alarm_src.alarm_wechat
    mix_num = query_alarm_src.alarm_mix
    nano_num = query_alarm_src.alarm_nano

    result = return_result(companyId=company_id, date=today_month, total=total_num,
                           source={"wechat": wechat_num, "mix": mix_num, "nano": nano_num}, token=token)

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getEvArea", methods=['GET'])
def get_ev_area():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)

    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')
    today_date = datetime.date.today()
    get_main_com_ev_area_to_db(company_id, [])
    query_ev_area = EvArea.query.filter(
        and_(EvArea.row_datetime >= today_date, EvArea.org_id == company_id)).all()
    # if query_ev_area is None:
    #     print_exit_func(func_name)
    #     return jsonify({"code": 1, "message": "请求companyId值返回为空"})

    project_info = []
    for ea in query_ev_area:
        project_info.append(
            {"projectName": ea.project_name, "longitude": ea.user_longitude, "latitude": ea.user_latitude,
             "evNum": ea.ev_num})

    results = return_result(companyId=company_id, projectInfo=project_info, token=token)

    print_exit_func(func_name)
    return jsonify(results)



