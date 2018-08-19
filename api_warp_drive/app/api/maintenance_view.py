#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-18 下午2:44
# @Author  : Shark
# @File    : maintenance_view.py
# @Software: PyCharm
import datetime

from flask import request, jsonify
from sqlalchemy import and_

from app.api import api, ARG_FLAG_ORG_ID, pm
from app.modles.base_info_query import *

import inspect

from lib.request_pre_check import request_pre_check
from lib.util import print_enter_func, print_exit_func


@api.route("/getAnnualInfo", methods=['GET'])
def get_annual_info():
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
    get_ev_annual_info_to_db(company_id)
    query_annual_info = AnnualInfo.query.filter(and_(AnnualInfo.row_datetime >= today_date,
                                                     AnnualInfo.org_id == company_id)).all()
    # if query_annual_info is None:
    #     print_exit_func(func_name)
    #     return jsonify({"code": 1, "message": "请求companyId值返回为空"})

    annual_info_list = list()
    for qa in query_annual_info:
        annual_info_list.append({"projectName": qa.project_name, "evOrder": qa.ev_order, "wtCode": qa.wt_code,
                                 "lastAnnualDate": str(qa.lastAnnualDate.date()), "status": qa.annualstatus})

    result = {
        "code": 0,
        "message": "",
        "obj": {
            "companyId": company_id,
            "elevator": annual_info_list

        },
        "tokenStr": token
    }

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getTodayMaintenanceOverview", methods=['GET'])
def get_today_maintenance_overview():
    func_name = inspect.stack()[0][3]
    print_enter_func(func_name)

    pm.set_para(ARG_FLAG_ORG_ID)
    result = request_pre_check(request.args, pm)

    if not result[0]:
        print_exit_func(func_name)
        return jsonify(result[1])

    company_id = request.args.get('companyId')
    token = request.headers.get('tokenStr')
    get_task_overview_to_db(company_id)
    today_date = datetime.date.today()
    query_task_overview = TaskOverview.query.filter(and_(TaskOverview.row_datetime >= today_date,
                                                         TaskOverview.org_id == company_id)).first()
    if not query_task_overview:
        result = {
            "code": 0,
            "message": "",
            "obj": {
                "companyId": company_id,
                "date": str(today_date),
                "overview": {
                    "taskNum": 0,
                    "completeTask": 0,
                    "incompleteTask": 0,
                    "faultTask": 0
                }
            },
            "tokenStr": token
        }
        print_exit_func(func_name)
        return jsonify(result)

    task_num = query_task_overview.task_num
    complete_num = query_task_overview.complete_task
    incomplete_num = query_task_overview.incomplete_task
    repair_complete = query_task_overview.fault_task

    result = {
        "code": 0,
        "message": "",
        "obj": {
            "companyId": company_id,
            "date": str(today_date),
            "overview": {
                "taskNum": task_num,
                "completeTask": complete_num,
                "incompleteTask": incomplete_num,
                "faultTask": repair_complete
            }
        },
        "tokenStr": token
    }

    print_exit_func(func_name)
    return jsonify(result)


@api.route("/getTodayWorkOrder", methods=['GET'])
def get_today_work_order_info():
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
    query_del_items = WorkInfo.query.filter(WorkInfo.org_id == company_id,
                                            WorkInfo.row_datetime == today_date).all()
    for item in query_del_items:
        # print(item.row_datetime)
        db.session.delete(item)
    db.session.commit()

    get_work_order_info(company_id)
    #################################################
    query_work_order_info = WorkInfo.query.order_by(WorkInfo.start_time).filter(and_(WorkInfo.row_datetime >= today_date,
                                                       WorkInfo.org_id == company_id)).all()
    work_order_list = list()
    # if not query_work_order_info:
    #     print_exit_func(func_name)
    #     return jsonify({"code": 1, "message": "请求companyId值返回为空"})

    for qw in query_work_order_info:
        start_time = str(qw.start_time.strftime('%m-%d %H:%M'))
        end_time = str(qw.end_time.strftime('%m-%d %H:%M')) if qw.end_time else ""
        work_order_list.append({"type": qw.type, "projectName": qw.project_name, "employee": qw.employee,
                                "team": qw.team, "startTime": start_time, "endTime": end_time,
                                "status": qw.status, "evOder": qw.ev_order, "exception": ""})
    # print(work_order_list)
    result = {
        "code": 0,
        "message": "",
        "obj": {
            "companyId": company_id,
            "date": str(today_date),
            "workOrderList": work_order_list
        },
        "tokenStr": token
    }

    print_exit_func(func_name)
    return jsonify(result)
