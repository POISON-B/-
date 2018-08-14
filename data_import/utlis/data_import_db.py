#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-14 下午11:47
# @Author  : Shark
# @File    : data_import_db.py
# @Software: PyCharm
from utlis.data_initialize import ProjectInfo


class ProjectTOdb(object):

    @property
    def to_db(self):
        data = ProjectInfo.project_info_format()
        for k, v in data:
            project_judge_creat(k, v)


if __name__ == '__main__':
    a =ProjectTOdb()
    a.to_db