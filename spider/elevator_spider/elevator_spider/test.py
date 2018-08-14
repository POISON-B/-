#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-6 上午10:50
# @Author  : Shark
# @Site    : 
# @File    : test.py
# @Software: PyCharm

import requests
import codecs
import time


equipment_code = ['3100', '3110', '3120', '3130', '3140', '3150', '3160', '3170', '3200', '3210', '3220', '3230', '3240'
                  '3250', '3300', '3310', '3320', '3330', '3340', '3400', '3500', '3600']

area_code = ['320100', '320102', '320103', '320104', '320105', '320106', '320107', '320111', '320113', '320114',
             '320114', '320115', '320116', '320124', '320125']

year_code = ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018']

moth_code = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

url = 'http://njdt.njtjy.org.cn/lift/liftInfo/{0}'

for equipment in equipment_code:
    for area in area_code:
        for year in year_code:
            for moth in moth_code:
                try:
                    req = requests.get(url=url.format(equipment + area + year + moth + '0001'))
                    print(req.url, req.status_code)
                    if req.status_code == 200:
                        with open('url1.csv', 'a') as f:
                            f.write(req.url + '\n')
                except requests.exceptions.ConnectionError:
                    print('请求太快')
                    time.sleep(5)
