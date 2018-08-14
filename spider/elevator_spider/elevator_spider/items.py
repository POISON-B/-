# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import os

item_key = dict()


class XianItem(scrapy.Item):
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


class TianJin(scrapy.Item):
    id = scrapy.Field()
    reg_code = scrapy.Field()
    customer_name = scrapy.Field()
    use_phone = scrapy.Field()
    maintenance_company_name = scrapy.Field()
    help_phone = scrapy.Field()
    complaints_phone = scrapy.Field()
    next_inspect_date = scrapy.Field()
    up_inspect_date = scrapy.Field()


class NanJing(scrapy.Item):
    id = scrapy.Field()
    reg_code = scrapy.Field()
    manufacture_product_id = scrapy.Field()
    maintenance_company_name = scrapy.Field()
    maintenance_company_addr = scrapy.Field()
    project_name = scrapy.Field()
    phone = scrapy.Field()
    customer_name = scrapy.Field()
    project_addr = scrapy.Field()
    inspection_unit_name = scrapy.Field()
    next_inspect_date = scrapy.Field()
    brand = scrapy.Field()
    country = scrapy.Field()


class ChengDu(scrapy.Item):
    info = scrapy.Field()
    # add = scrapy.Field()
    # reg_code = scrapy.Field()
    # evOrder = scrapy.Field()
    # next_time = scrapy.Field()


item_key['西安'] = XianItem()
item_key['芜湖'] = WuhuItem()
item_key['天津'] = TianJin()
item_key['南京2'] = NanJing()
item_key['成都'] = ChengDu()


class ItemFactory(object):
    def __init__(self, key):
        self.key = key

    def get_methods(self):

        if self.key in item_key.keys():
            return item_key[self.key]


if __name__ == '__main__':
    print(os.path.dirname(os.path.abspath(__file__)))