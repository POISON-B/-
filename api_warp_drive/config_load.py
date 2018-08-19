#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-17 下午11:35
# @Author  : Shark
# @File    : config_load.py
# @Software: PyCharm

from happy_utils.happy_config import HappyConfigParser, HappyConfigBase


class ConfigParser(HappyConfigBase):

    def __init__(self):
        self._section = 'main'
        self.listen = '127.0.0.1'
        self.port = '8080'
        self.debug = 'False'

        self.ttd_mysql_host = '172.16.1.210'
        self.ttd_mysql_port = '1027'
        self.ttd_mysql_user = 'ttd'
        self.ttd_mysql_pwd = 'mFnzGYwHlepMzDR8wJxG'
        self.ttd_mysql_db = 'ttd'

        self.liftdatav_mysql_host = '172.16.1.208'
        self.liftdatav_mysql_port = '3306'
        self.liftdatav_mysql_user = 'root'
        self.liftdatav_mysql_pwd = 'root'
        self.liftdatav_mysql_db = 'twd'


config = ConfigParser()
HappyConfigParser.load('configs/common.ini', config)
config_dict = config.__dict__

ttd_db_uri = \
    'mysql+pymysql://' + config_dict['ttd_mysql_user'] + ':' + config_dict['ttd_mysql_pwd'] + '@' \
    + config_dict['ttd_mysql_host'] + ':' + str(config_dict['ttd_mysql_port']) + '/' \
    + config_dict['ttd_mysql_db'] + '?charset=utf8'

liftdatav_db_uri = \
    'mysql+pymysql://' + config_dict['liftdatav_mysql_user'] + ':' + config_dict['liftdatav_mysql_pwd'] + '@' \
    + config_dict['liftdatav_mysql_host'] + ':' + str(config_dict['liftdatav_mysql_port']) + '/' \
    + config_dict['liftdatav_mysql_db'] + '?charset=utf8'
print(ttd_db_uri)

if __name__ == '__main__':
    pass