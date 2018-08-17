#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
校验 HTTP 请求参数函数集合
"""

from lib.parameter_manager import *
from lib.util import make_api_respone


def request_pre_check(arg_dict: dict, para_manager: ParameterManager):
    para_dict = para_manager.get_enable_paras()

    for k, v in para_dict.items():
        arg_name = v[0]
        callback_func = v[1]

        if arg_name not in arg_dict:
            return False, make_api_respone(1, ('缺少请求参数：%s' % arg_name))

        arg_value = arg_dict[arg_name]

        if not callback_func:
            return False, make_api_respone(1, ('回调函数错误：%s' % callback_func))

        if not callback_func(arg_value):
            return False, make_api_respone(1, ('参数校验失败：%s => %s' % (arg_name, arg_value)))

    return True, make_api_respone(0, '')


def check_org_id(org_id):
    """
    验证机构编号
    :param org_id:
    :return: bool
    """

    return org_id and len(org_id) >= 3
