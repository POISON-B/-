#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-17 下午10:48
# @Author  : Shark
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask


def create_app():
    """
    注册flask核心对象
    :return:
    """
    app = Flask(__name__)
    register_blueprint(app)

    return app


def register_blueprint(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    from app.api.safety_info_view import api
    app.register_blueprint(api)
