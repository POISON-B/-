#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-10 下午9:52
# @Author  : Shark
# @File    : __init__.py
# @Software: PyCharm
from flask import Blueprint

web = Blueprint('web', __name__)


from app.web import book
from app.web import auth
from app.web import drift
from app.web import gift
from app.web import main
from app.web import wish
