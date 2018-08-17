#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from abc import ABCMeta, abstractmethod


class TSDConfigBase(object, metaclass=ABCMeta):
    filename = str()
    options = dict()
    set_methods = dict()

    def __init__(self, options: dict):
        self.options = options

    def get_options(self):
        return self.options

    @abstractmethod
    def cfg_filename(self):
        """
        配置文件路径

        :return:
        """
        pass

    @abstractmethod
    def bind_set_method(self):
        """
        绑定参数名称和set方法，以便后续使用回调

        :return:
        """
        pass


class TSDConfigParser:
    def __init__(self, arg_stc_cfg: TSDConfigBase):
        self.stc_cfg = arg_stc_cfg
        self.stc_cfg.bind_set_method()
        self.load()

    def load(self):
        from configparser import ConfigParser

        try:
            if not os.path.exists(self.stc_cfg.cfg_filename()):
                print("[Error] 配置文件 %s 不存在" % self.stc_cfg.cfg_filename())
                exit(1)

            cfg = ConfigParser()
            cfg.read(self.stc_cfg.cfg_filename())

            for option, o_type in self.stc_cfg.get_options().items():
                if type(o_type) is str:
                    v = cfg.get('main', option)
                elif type(o_type) is int:
                    v = cfg.getint('main', option)
                elif type(o_type) is bool:
                    v = cfg.getboolean('main', option)
                elif type(o_type) is float:
                    v = cfg.getfloat('main', option)
                else:  # 默认按照布尔值处理
                    v = cfg.getboolean('main', option)

                self.stc_cfg.set_methods[option](v)
        except Exception as e:
            print("[Error] 配置文件读取错误：%s" % str(e))
            exit(1)


class CommonConfig(TSDConfigBase):
    from pathlib import PurePath

    filename = str(PurePath(__file__).parent.parent / 'configs' / 'common.ini')
    # 参数列表及其参数类型
    options = {
        "listen": "",
        "port": 0,
        "debug": False,
        "ttd_mysql_host": "",
        "ttd_mysql_port": 0,
        "ttd_mysql_user": "",
        "ttd_mysql_pwd": "",
        "ttd_mysql_db": "",
        "liftdatav_mysql_host": "",
        "liftdatav_mysql_port": 0,
        "liftdatav_mysql_user": "",
        "liftdatav_mysql_pwd": "",
        "liftdatav_mysql_db": ""
    }

    def __init__(self):
        super().__init__(self.options)
        self.set_methods = dict()

        self.listen = self.options["listen"]
        self.port = self.options["port"]
        self.debug = self.options["debug"]
        self.ttd_mysql_host = self.options["ttd_mysql_host"]
        self.ttd_mysql_port = self.options["ttd_mysql_port"]
        self.ttd_mysql_user = self.options["ttd_mysql_user"]
        self.ttd_mysql_pwd = self.options["ttd_mysql_pwd"]
        self.ttd_mysql_db = self.options["ttd_mysql_db"]
        self.liftdatav_mysql_host = self.options["liftdatav_mysql_host"]
        self.liftdatav_mysql_port = self.options["liftdatav_mysql_port"]
        self.liftdatav_mysql_user = self.options["liftdatav_mysql_user"]
        self.liftdatav_mysql_pwd = self.options["liftdatav_mysql_pwd"]
        self.liftdatav_mysql_db = self.options["liftdatav_mysql_db"]

    def bind_set_method(self):
        self.set_methods = {
            "listen": self.set_listen,
            "port": self.set_port,
            "debug": self.set_debug,
            "ttd_mysql_host": self.set_ttd_mysql_host,
            "ttd_mysql_port": self.set_ttd_mysql_port,
            "ttd_mysql_user": self.set_ttd_mysql_user,
            "ttd_mysql_pwd": self.set_ttd_mysql_pwd,
            "ttd_mysql_db": self.set_ttd_mysql_db,
            "liftdatav_mysql_host": self.set_liftdatav_mysql_host,
            "liftdatav_mysql_port": self.set_liftdatav_mysql_port,
            "liftdatav_mysql_user": self.set_liftdatav_mysql_user,
            "liftdatav_mysql_pwd": self.set_liftdatav_mysql_pwd,
            "liftdatav_mysql_db": self.set_liftdatav_mysql_db
        }

    def cfg_filename(self):
        return self.filename

    def set_listen(self, v: str):
        self.listen = v

    def get_listen(self):
        return self.listen

    def set_port(self, v: str):
        self.port = v

    def get_port(self):
        return self.port

    def set_debug(self, v: str):
        self.debug = v

    def get_debug(self):
        return self.debug

    def set_ttd_mysql_host(self, v: str):
        self.ttd_mysql_host = v

    def get_ttd_mysql_host(self):
        return self.ttd_mysql_host

    def set_ttd_mysql_port(self, v: str):
        self.ttd_mysql_port = v

    def get_ttd_mysql_port(self):
        return self.ttd_mysql_port

    def set_ttd_mysql_user(self, v: str):
        self.ttd_mysql_user = v

    def get_ttd_mysql_user(self):
        return self.ttd_mysql_user

    def set_ttd_mysql_pwd(self, v: str):
        self.ttd_mysql_pwd = v

    def get_ttd_mysql_pwd(self):
        return self.ttd_mysql_pwd

    def set_ttd_mysql_db(self, v: str):
        self.ttd_mysql_db = v

    def get_ttd_mysql_db(self):
        return self.ttd_mysql_db

    def set_liftdatav_mysql_host(self, v: str):
        self.liftdatav_mysql_host = v

    def get_liftdatav_mysql_host(self):
        return self.liftdatav_mysql_host

    def set_liftdatav_mysql_port(self, v: str):
        self.liftdatav_mysql_port = v

    def get_liftdatav_mysql_port(self):
        return self.liftdatav_mysql_port

    def set_liftdatav_mysql_user(self, v: str):
        self.liftdatav_mysql_user = v

    def get_liftdatav_mysql_user(self):
        return self.liftdatav_mysql_user

    def set_liftdatav_mysql_pwd(self, v: str):
        self.liftdatav_mysql_pwd = v

    def get_liftdatav_mysql_pwd(self):
        return self.liftdatav_mysql_pwd

    def set_liftdatav_mysql_db(self, v: str):
        self.liftdatav_mysql_db = v

    def get_liftdatav_mysql_db(self):
        return self.liftdatav_mysql_db


common_cfg = CommonConfig()
common_cfg_parser = TSDConfigParser(common_cfg)

ttd_db_uri = \
    'mysql+pymysql://' + common_cfg.get_ttd_mysql_user() + ':' + common_cfg.get_ttd_mysql_pwd() + '@' \
    + common_cfg.get_ttd_mysql_host() + ':' + str(common_cfg.get_ttd_mysql_port()) + '/' \
    + common_cfg.get_ttd_mysql_db() + '?charset=utf8'

liftdatav_db_uri = \
    'mysql+pymysql://' + common_cfg.get_liftdatav_mysql_user() + ':' + common_cfg.get_liftdatav_mysql_pwd() + '@' \
    + common_cfg.get_liftdatav_mysql_host() + ':' + str(common_cfg.get_liftdatav_mysql_port()) + '/' \
    + common_cfg.get_liftdatav_mysql_db() + '?charset=utf8'
