#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
梯梯达表结构引用
"""

from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class CompanyInfo(Base):
    __tablename__ = 'companyinfo'
    uuid = Column(Integer, primary_key=True)
    name = Column(String(255), default=None, comment='公司名称')
    contactPhone = Column(String(255), default=None, comment='公司电话')
    typeid = Column(Integer, default=None, comment='公司类型')
    address = Column(String(255), default=None, comment='公司地址')
    memo = Column(String(255), default=None, comment='')
    shortName = Column(String(255), default=None, comment='公司缩写')
    legalPerson = Column(String(255), default=None, comment='法定代表人')
    registerCode = Column(String(255), default=None, comment='营业执照号')
    province = Column(Integer, default=None, comment='省')
    city = Column(Integer, default=None, comment='市')
    country = Column(Integer, default=None, comment='区')
    del_status = Column(Integer, default=None, comment='删除标识')
    disable = Column(Integer, default=None, comment='状态')
    createAt = Column(DateTime, default=None, comment='记录时间')
