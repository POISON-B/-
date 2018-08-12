#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 下午12:01
# @Author  : Shark
# @File    : wish.py
# @Software: PyCharm

from sqlalchemy import ForeignKey, Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class Wish(Base):
    __tablename__ = 'wish'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)
