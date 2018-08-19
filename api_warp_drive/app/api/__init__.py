#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-18 下午12:58
# @Author  : Shark
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint

from lib.request_pre_check import check_org_id, ParameterManager

api = Blueprint('api', __name__)
ARG_FLAG_ORG_ID = 1 << 0
ARG_FLAG_USER_ID = 2 << 0
ARG_FLAG_AREA_ID = 3 << 0

pm = ParameterManager()
pm.register_para(ARG_FLAG_ORG_ID, 'companyId', check_org_id)


from app.api import safety_info_view
from app.api import maintenance_view