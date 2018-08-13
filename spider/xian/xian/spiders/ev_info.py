# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals

from selenium import webdriver

from xian.city_parser import *
from xian.middlewares import JsPageMiddle

from xian.uitl import handle_value, COED_ID_1


class EvInfoSpider(scrapy.Spider):
    name = 'ev_info'
    allowed_domains = ['weixin.xseii.com.cn']
    # start_urls = ['http://weixin.xseii.com.cn/wx96333/qc?regcode=31106101182012100029']
    url2 = 'http://weixin.xseii.com.cn/wx96333/qc?regcode={0}'
    url1 = 'http://www.xseii.com.cn/getDtSearchValues'
    regcode = 1300000
    code = COED_ID_1
    payload = {
        'regcode': '1571333'
    }

    def __init__(self):
        self.browser = webdriver.Chrome()
        super(EvInfoSpider, self).__init__()
        dispatcher.connect(self.spider_closed, signals.spider_closed)  # scrapy信号量爬虫关闭，关闭浏览器

    def spider_closed(self, spider):
        print("spider closed")
        self.browser.quit()

    def start_requests(self):
        while self.regcode <= self.code[1]:
            self.regcode += 1
            self.payload['regcode'] = str(self.regcode)
            self.log(self.regcode)
            yield scrapy.FormRequest(url=self.url1, formdata=self.payload, callback=self.secondary_request)

    def parse(self, response):
        city = Factory('xian')
        city.get_methods().parse()

    def secondary_request(self, response):
        print(response.body)
        if response.body and json.loads(response.body, encoding='utf8')['msg'] == '成功':
            yield scrapy.Request(url=self.url2.format(json.loads(response.body, encoding='utf8')['data']['regcode']), callback=self.parse)
