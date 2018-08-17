# -*- coding: utf-8 -*-
import scrapy
import re

from xiaoqu.items import XiaoquItem


class ChengduSpider(scrapy.Spider):
    name = 'chengdu'
    allowed_domains = ['chengdu.anjuke.com']
    start_urls = ['http://www.scsei.org.cn/?searchtype=sydw&sydw=天鹅湖花园&action=queryreport']
    url = 'https://chengdu.anjuke.com/community/p{0}/'
    p = 1

    def parse(self, response):
        item = XiaoquItem()


        # for i in info:
        #     print(i)
        # print(response.xpath())
        # for i in response.xpath(r'//*[@id="list-content"]/div'):
            # item = XiaoquItem()
            # item['name'] = i.xpath(r'./div[1]/h3/a/text()').extract_first()
            #
            # yield item

        # if self.p < 50:
        #     self.p += 1
        #     yield scrapy.Request(url=self.url.format(self.p), callback=self.parse)
