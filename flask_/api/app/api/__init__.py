#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午3:47
# @Author  : Shark
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Blueprint

from app.api.v1 import book, clinet


def ceate_blueprint_v1():
    """
    注册蓝图并挂载红图
    :return:
    """
    bp_v1 = Blueprint('v1', __name__)
    book.api.register(bp_v1)
    clinet.api.register(bp_v1)

    return bp_v1
