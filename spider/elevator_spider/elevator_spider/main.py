#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-6 上午10:48
# @Author  : Shark
# @Site    : 
# @File    : main.py
# @Software: PyCharm

from scrapy.cmdline import execute

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "ev_info"])
