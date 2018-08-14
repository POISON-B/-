#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-10 下午9:46
# @Author  : Shark
# @File    : __init__.py
# @Software: PyCharm
from flask import Flask
from flask_login import LoginManager

from app.models.base import db

login_manager = LoginManager()


def create_app():
    """
    创建flask app核心对象
    :return:
    """
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.settings')
    register_blueprint(app)

    db.init_app(app)  # 注册数据库操作
    db.create_all(app=app)  # 创建数据库表
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请登录或注册'
    return app


def register_blueprint(app):
    """
    注册蓝图
    :param app:
    :return:
    """
    from app.web.book import web
    app.register_blueprint(web)

