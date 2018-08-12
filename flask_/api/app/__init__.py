#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午3:44
# @Author  : Shark
# @File    : __init__.py.py
# @Software: PyCharm

from flask import Flask

from app.config import settings


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.settings')
    app.config.from_object('app.config.secure')

    # 注册蓝图
    register_blueprint(app)

    # 注册数据模型
    register_plugin(app)

    return app


def register_blueprint(app):
    from app.api import ceate_blueprint_v1
    app.register_blueprint(ceate_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    db.init_app(app)
    with app.app_context():
        db.create_all()
