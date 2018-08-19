#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import logging.config

from flask import Flask
from flask_cors import CORS

from lib.config import liftdatav_db_uri

# 为支持 uWSGI 默认加载点，Flask 应用名称不能修改
application = Flask('api_warp_drive')
application.config['SQLALCHEMY_DATABASE_URI'] = liftdatav_db_uri
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
application.config['SQLALCHEMY_POOL_SIZE'] = 100

# 支持 JSON 显示中文
application.config['JSON_AS_ASCII'] = False
# 前端夸域
CORS(application)

logging.config.fileConfig('configs/log.ini')
logger = logging.getLogger('awd')
