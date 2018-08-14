#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 上午10:38
# @Author  : Shark
# @File    : base.py
# @Software: PyCharm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, SmallInteger, Column

db = SQLAlchemy()


class Base(db.Model):
    __abstract__ = True
    create_time = Column('create_time', Integer)
    status = Column(SmallInteger, default=1)

    def set_attrs(self, attrs_dict):
        for k, v in attrs_dict.items():
            if hasattr(self, k) and k != 'id':
                setattr(self, k, v)



