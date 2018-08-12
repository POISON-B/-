#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午3:47
# @Author  : Shark
# @File    : book.py
# @Software: PyCharm

from app.libs.redprint import RedPrint

api = RedPrint('book')


@api.route('/get')
def get_book():
    return 'haha'
