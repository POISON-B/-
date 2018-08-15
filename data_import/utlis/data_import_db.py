#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午11:47
# @Author  : Shark
# @File    : data_import_db.py
# @Software: PyCharm
from utlis.data_initialize import ProjectInfo, LiftInfo
from utlis.db_query import project_judge_create, lift_judge_create


class ProjectTOdb(object):
    project_info = dict

    @property
    def to_db(self, name):
        data = ProjectInfo.project_info_format(name)
        for k, v in data:
            info = project_judge_create(k, v)
            self.project_info[k] = info

    @classmethod
    def lift_to_db(cls, wbid, temid):
        data = LiftInfo.lift_info_format()
        for k, v in data:
            lift_judge_create(k, v, cls.project_info, wbid, temid)


if __name__ == '__main__':
    a =ProjectTOdb()
    a.to_db