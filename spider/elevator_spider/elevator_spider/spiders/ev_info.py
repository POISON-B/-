# -*- coding: utf-8 -*-
import json
import scrapy
import requests

from elevator_spider.spiders.city_start_url import URLFactory
from elevator_spider.city_parser import ParseFactory
from scrapy.conf import settings


class EvInfoSpider(scrapy.Spider):
    name = 'ev_info'
    allowed_domains = ['']
    # start_urls = ['http://njdt.njtjy.org.cn/lift/getLift/000001']
    url = 'http://njdt.njtjy.org.cn/lift/getLift/00000{}'
    num = 1

    def start_requests(self):
        city = URLFactory(settings['CITY_NAME'])
        request = city.get_obj()
        while self.num < 100001:
            yield request(url=self.url, num=self.num, callback=self.parse)
            self.num += 1

    def parse(self, response):
        city = ParseFactory(settings['CITY_NAME'])
        item = city.get_obj().parse(response, settings['CITY_NAME'])
        yield item
