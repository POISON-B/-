# !/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-9 下午10:32
# @Author  : Shark
# @File    : httper.py
# @Software: PyCharm

import requests


class Http(object):
    @staticmethod
    def get(url, return_json=False):
        r = requests.get(url)

        if r.status_code != 200:
            return {} if return_json else ''
        return r.json() if return_json else r.text
