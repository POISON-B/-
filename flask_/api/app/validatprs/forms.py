#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午4:47
# @Author  : Shark
# @File    : forms.py
# @Software: PyCharm

from wtforms import Form, StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, ValidationError

from app.libs.enums import ClientTypeEnum


class ClientForm(Form):
    account = StringField(validators=[DataRequired(), length(min=1, max=32)])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)

        except ValueError as e:
            raise e
        self.type.data = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[Email(message='标准邮箱地址')])
    secret = StringField(validators=[DataRequired(), Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')])
    nickname = StringField(validators=[DataRequired(), length(min=1, max=22)])

    def validata_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()
