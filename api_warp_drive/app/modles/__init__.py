#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-17 下午11:33
# @Author  : Shark
# @File    : __init__.py.py
# @Software: PyCharm

from sqlalchemy import *
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.pool import NullPool

from twd_db_manager import *
from flask import jsonify
from config_load import *


def connect_db():
    db_connect = create_engine(ttd_db_uri, poolclass=NullPool)
    return db_connect


ttd_engine = connect_db()
ttd_metadata = MetaData(ttd_engine)

Table('alarm_info', ttd_metadata, autoload=True)
Table('ev_records', ttd_metadata, autoload=True)
Table('wo_info', ttd_metadata, autoload=True)
Table('ev_info', ttd_metadata, autoload=True)
Table('projectInfo', ttd_metadata, autoload=True)
# Table('area',ttd_metadata,autoload=True)
Table('employee', ttd_metadata, autoload=True)
Table('ev_remind', ttd_metadata, autoload=True)
Table('companyConf', ttd_metadata, autoload=True)
Table('wo_info_status', ttd_metadata, autoload=True)
Table('em_team', ttd_metadata, autoload=True)
Table('team', ttd_metadata, autoload=True)
Table('user', ttd_metadata, autoload=True)
Table('c_workclock', ttd_metadata, autoload=True)
Table('c_elevator', ttd_metadata, autoload=True)
Table('c_evRepair', ttd_metadata, autoload=True)

Base = automap_base(metadata=ttd_metadata)
Base.prepare()

AlarmInfo = Base.classes.alarm_info
EvRecords = Base.classes.ev_records
WoInfo = Base.classes.wo_info
EvInfo = Base.classes.ev_info
ProjectInfo = Base.classes.projectInfo
Employee = Base.classes.employee
EvRemind = Base.classes.ev_remind
CompanyConf = Base.classes.companyConf
WoInfoStatus = Base.classes.wo_info_status
CElevator = Base.classes.c_elevator
CEvRepair = Base.classes.c_evRepair

EmTeam = Base.classes.em_team
Team = Base.classes.team
User = Base.classes.user
C_workclock = Base.classes.c_workclock
