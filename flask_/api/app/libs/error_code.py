#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午5:53
# @Author  : Shark
# @File    : error_code.py
# @Software: PyCharm
from werkzeug.exceptions import HTTPException

from app.libs.error import APIException


class ClientTypeError(APIException):
    code = 400
    msg = '参数错误'
    error_code = 1006
