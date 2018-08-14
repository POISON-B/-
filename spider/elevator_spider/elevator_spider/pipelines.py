# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

from elevator_spider.city_pipelines import Factory
from scrapy.conf import settings

logger = logging.getLogger(__name__)


class ElevatorSpiderPipeline(object):

    def process_item(self, item, spider):
        city = Factory(settings['CITY_NAME'])
        obj = city.get_obj()
        obj(item)
        return item
