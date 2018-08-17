#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-2 上午10:17
# @Author  : Shark
# @Site    : 
# @File    : city_item.py
# @Software: PyCharm

import scrapy

item_key = dict()


class XianItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    code = scrapy.Field()
    regcode = scrapy.Field()
    region = scrapy.Field()
    brand = scrapy.Field()
    test = scrapy.Field()
    maintenance = scrapy.Field()
    use = scrapy.Field()
    address = scrapy.Field()


class WuhuItem(scrapy.Item):
    elevator_number = scrapy.Field()
    address = scrapy.Field()
    customer_name = scrapy.Field()
    phone = scrapy.Field()
    reg_code = scrapy.Field()
    next_inspect_date = scrapy.Field()
    maintenance_company_name = scrapy.Field()


item_key['xian'] = XianItem()
item_key['wuhu'] = WuhuItem()


class ItemFactory(object):
    def __init__(self, key):
        self.key = key

    def get_methods(self):

        if self.key in item_key.keys():
            return item_key[self.key]