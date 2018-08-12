#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午4:44
# @Author  : Shark
# @File    : clinet.py
# @Software: PyCharm
from flask import request

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import ClientTypeError
from app.libs.redprint import RedPrint
from app.validatprs.forms import ClientForm, UserEmailForm

api = RedPrint('client')


@api.route('/register', method=['POST'])
def create_client():
    data = request.json
    form = ClientForm(data=data)
    if form.validate():
        promise = {
            ClientTypeEnum.USER_EMAIL: __register_user_by_email
        }
        promise[form.type.data]()

    else:
        raise ClientTypeError()

    return '添加成功'


def __register_user_by_email():
    form = UserEmailForm(data=request.json)
    if form.validate():
        User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
