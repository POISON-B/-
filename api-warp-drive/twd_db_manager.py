#! /usr/bin/env python3
# -*- coding: utf-8 -*-

"""
曲速引擎 API 服务数据库管理工具
"""

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from lib.common import *

db = SQLAlchemy(application)
migrate = Migrate(application, db)

manager = Manager(application)
manager.add_command('db', MigrateCommand)


class OrgOverview(db.Model):
    """
    机构概况
    """

    __tablename__ = 'org_overview'
    uuid = db.Column(db.BIGINT, primary_key=True)
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    ev_total = db.Column(db.Integer, default=None)  # 电梯总数
    Employee_total = db.Column(db.Integer, default=None)  # 员工总数


class WorkOverview(db.Model):
    """
    记录每天工作情况
    """

    __tablename__ = 'work_overview'
    uuid = db.Column(db.BIGINT, primary_key=True)
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    ev_num_repair = db.Column(db.Integer, default=None)  # 已修理电梯数
    ev_num_maintenance = db.Column(db.Integer, default=None)  # 已保养电梯数


class OrgRelationship(db.Model):
    """
    机构关系表
    """

    __tablename__ = 'org_relationship'
    uuid = db.Column(db.BIGINT, primary_key=True)
    org_id_a = db.Column(db.BIGINT, default=None)  # 机构编号A，一般是政府
    org_id_b = db.Column(db.BIGINT, default=None)  # 机构编号B，一般是维保或物业单位


class AlarmNum(db.Model):
    """
    报警次数
    """

    __tablename__ = 'alarm_num'
    uuid = db.Column(db.BigInteger, primary_key=True)
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    alarm_num = db.Column(db.Integer, default=None)  # 报警次数


class AlarmSrcStat(db.Model):
    """
    报警来源统计
    """

    __tablename__ = 'alarm_src_stat'
    uuid = db.Column(db.BIGINT, primary_key=True)
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    alarm_total = db.Column(db.Integer, default=None)  # 报警总数
    alarm_wechat = db.Column(db.Integer, default=None)  # 微信报警次数
    alarm_mix = db.Column(db.Integer, default=None)  # Mix 报警次数
    alarm_nano = db.Column(db.Integer, default=None)  # Nano 报警次数


class RepairMainStat(db.Model):
    """
    记录月度工作情况
    """

    __tablename__ = 'repair_main_stat'
    uuid = db.Column(db.BIGINT, primary_key=True)
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    ev_num_repair = db.Column(db.Integer, default=None)  # 维修电梯数
    ev_num_maintenance = db.Column(db.Integer, default=None)  # 保养电梯数


class EvArea(db.Model):
    """
    电梯分布
    """

    __tablename__ = 'ev_area'
    uuid = db.Column(db.BIGINT, primary_key=True)
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    project_name = db.Column(db.String(255), default=None)  # 小区名称
    area_name = db.Column(db.String(255), default=None)  # 区域名称
    area_id = db.Column(db.Integer, default=None)  # 区域id
    ev_num = db.Column(db.Integer, default=None)  # 电梯数
    user_longitude = db.Column(db.Float, default=None)  # 经度
    user_latitude = db.Column(db.Float, default=None)  # 纬度


class WorkInfo(db.Model):
    """
    任务信息
    """

    __tablename__ = 'work_info'
    uuid = db.Column(db.BIGINT, primary_key=True)
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    ev_order = db.Column(db.String(255), default=None)  # 梯号
    team = db.Column(db.String(255), default=None)  # 班组
    type = db.Column(db.String(255), default=None)  # 工单类型
    project_name = db.Column(db.String(255), default=None)  # 项目名
    employee = db.Column(db.String(255), default=None)  # 工单创建人
    start_time = db.Column(db.DateTime, default=None)  # 工单开始时间
    end_time = db.Column(db.DateTime, default=None)  # 工单结束时间
    status = db.Column(db.String(255), default=None)  # 工单状态
    exception = db.Column(db.String(255), default=None)  # 异常


class AnnualInfo(db.Model):
    """
    年检信息
    """

    __tablename__ = 'annual_info'
    uuid = db.Column(db.BIGINT, primary_key=True)
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    project_name = db.Column(db.String(255), default=None)  # 项目名
    ev_order = db.Column(db.String(255), default=None)  # 梯号
    wt_code = db.Column(db.Integer, default=None)  # 维特号
    lastAnnualDate = db.Column(db.DateTime, default=None)  # 最后一次年检时间
    annualstatus = db.Column(db.String(255), default=None)  # 年检状态


class TaskOverview(db.Model):
    """
    任务概要
    """

    __tablename__ = 'task_overview'
    uuid = db.Column(db.BIGINT, primary_key=True)
    row_datetime = db.Column(db.DateTime, default=None)  # 记录时间
    org_id = db.Column(db.BIGINT, default=None)  # 机构编号
    task_num = db.Column(db.Integer, default=None)  # 应保养电梯数
    complete_task = db.Column(db.Integer, default=None)  # 保养完成电梯数
    incomplete_task = db.Column(db.Integer, default=None)  # 正在保养电梯数
    fault_task = db.Column(db.Integer, default=None)  # 故障完成数


class ProjectInfo(db.Model):
    """
    项目信息表
    """

    __tablename__ = 'projectInfo'
    uuid = db.Column(db.BIGINT, primary_key=True)
    name = db.Column(db.String(255), default=None)
    memo = db.Column(db.String(255), default=None)
    createAt = db.Column(db.DateTime, default=None)
    createBy = db.Column(db.String(255), default=None)
    address = db.Column(db.String(255), default=None)
    latitude = db.Column(db.Float, default=None)
    longitude = db.Column(db.Float, default=None)
    province = db.Column(db.BigInteger, default=None)
    city = db.Column(db.BigInteger, default=None)
    country = db.Column(db.BigInteger, default=None)
    propCompanyId = db.Column(db.BigInteger, default=None)


class EvInfo(db.Model):
    """
    电梯信息表
    """

    __tablename__ = 'ev_info'
    uuid = db.Column(db.BIGINT, primary_key=True)
    projectId = db.Column(db.BigInteger, default=None)
    wtCode = db.Column(db.String(255), default=None)
    regCode = db.Column(db.String(255), default=None)
    brandId = db.Column(db.BigInteger, default=None)
    useFor = db.Column(db.BigInteger, default=None)
    type = db.Column(db.BigInteger, default=None)
    deviceNumber = db.Column(db.String(255), default=None)
    manufacturer = db.Column(db.String(255), default=None)
    productionDate = db.Column(db.DateTime, default=None)
    productionNumber = db.Column(db.String(255), default=None)
    modelNumber = db.Column(db.String(255), default=None)
    evOrder = db.Column(db.String(255), default=None)
    createAt = db.Column(db.DateTime, default=None)
    createBy = db.Column(db.String(255), default=None)
    status = db.Column(db.BigInteger, default=None)
    userLock = db.Column(db.BigInteger, default=None)


class EvRecords(db.Model):
    """
    电梯领用表
    """

    __tablename__ = 'ev_records'
    uuid = db.Column(db.BIGINT, primary_key=True)
    fileNumber = db.Column(db.String(255), default=None)
    companyId = db.Column(db.BigInteger, default=None)
    evId = db.Column(db.BigInteger, default=None)
    startTime = db.Column(db.DateTime, default=None)
    status = db.Column(db.BigInteger, default=None)
    endTime = db.Column(db.DateTime, default=None)
    userName = db.Column(db.String(255), default=None)
    lastAnnualDate = db.Column(db.DateTime, default=None)


if __name__ == '__main__':
    manager.run()
