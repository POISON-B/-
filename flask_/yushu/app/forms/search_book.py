#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-10 下午10:21
# @Author  : Shark
# @File    : search_book.py
# @Software: PyCharm

from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange


class SearchForm(Form):
    """
    搜索参数校验
    """
    q = StringField(validators=[Length(min=1, max=30)],)
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)
