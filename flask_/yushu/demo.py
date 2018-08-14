#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-8 下午11:24
# @Author  : Shark
# @File    : demo.py
# @Software: PyCharm

from flask import Flask

app = Flask(__name__)
app.config.from_object('settings')


# @app.route('/')
def hello():
    return 'hell'


app.add_url_rule('/', view_func=hello)  # 第二种路由注册方式


if __name__ == '__main__':
    app.run()
