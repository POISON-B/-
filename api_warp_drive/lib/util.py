#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import random

from lib.config import ttd_db_uri
from twd_db_manager import *
from flask import jsonify


# 生成数据库uuid
def get_uuid_for_db():
    return random.randint(100000000, 130000000)


# 判断uuid是否存在
def judge_uuid(uuid, tables):
    while True:
        pro_obj_check = db.session.query(tables).filter_by(uuid=uuid).first()
        if pro_obj_check:
            uuid = get_uuid_for_db()
            continue
        else:
            break
    return uuid


def make_api_respone(code: int, msg: str):
    return {'code': code, 'message': msg}


def print_enter_func(func_name: str):
    logger.debug("Enter function: %s" % func_name)


def print_exit_func(func_name: str):
    logger.debug("Exit function: %s" % func_name)
