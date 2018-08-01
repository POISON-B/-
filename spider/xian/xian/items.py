# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


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