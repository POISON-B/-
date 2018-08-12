#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-9 下午10:14
# @Author  : Shark
# @File    : apps.py
# @Software: PyCharm
from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run()
