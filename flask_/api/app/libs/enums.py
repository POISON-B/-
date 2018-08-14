#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午4:48
# @Author  : Shark
# @File    : enums.py
# @Software: PyCharm

from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200

    # 微信公众号
    USER_WX = 201

