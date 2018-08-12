#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午6:03
# @Author  : Shark
# @File    : error.py
# @Software: PyCharm
from werkzeug.exceptions import HTTPException
from flask import request, json


class APIException(HTTPException):
    code = 500
    msg = '未知错误'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None, headers=None):
        if code:
            self.code = code

        if error_code:
            self.error_code = error_code

        if msg:
            self.msg = msg
        super(APIException, slef).__init(msg, None)

    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_on_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_on_param():
        full_path = str(requrst.full_path)
        main_path = full_path.split('?')

        return main_path[0]