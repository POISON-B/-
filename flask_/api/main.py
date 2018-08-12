#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午3:44
# @Author  : Shark
# @File    : main.py
# @Software: PyCharm

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
