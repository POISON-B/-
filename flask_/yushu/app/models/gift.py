#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-12 上午10:40
# @Author  : Shark
# @File    : gift.py
# @Software: PyCharm
from sqlalchemy import ForeignKey, Integer, String, Column, Boolean
from sqlalchemy.orm import relationship

from app.models.base import Base


class Gift(Base):
    __tablename__ = 'gift'

    id = Column(Integer, primary_key=True)
    uid = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User')
    isbn = Column(String(13))
    launched = Column(Boolean, default=False)
