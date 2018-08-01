#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-1 下午5:07
# @Author  : Shark
# @Site    : 
# @File    : city_parser.py
# @Software: PyCharm

from abc import ABCMeta, abstractmethod

from xian.items import XianItem


class CityParser(object, metaclass=ABCMeta):

    @abstractmethod
    def parse(self, response):
        pass

    def save(self):
        pass


class XianCityParser(CityParser):
    def parse(self, response):
        item = XianItem()
        for i in response.xpath('//table[@class="table"]'):
            if i.xpath('./tbody/tr[1]/td/text()').extract():
                item['code'] = i.xpath('./tbody/tr[1]/td/text()').extract()[0]
                item['regcode'] = i.xpath('./tbody/tr[2]/td/text()').extract()[0]
                item['region'] = i.xpath('./tbody/tr[3]/td/text()').extract()[0]
                item['brand'] = handle_value(str(i.xpath('./tbody/tr[4]/td/text()').extract()))
                item['test'] = handle_value(str(i.xpath('./tbody/tr[5]/td/text()').extract()))
                item['maintenance'] = i.xpath('./tbody/tr[6]/td/text()').extract()[0]
                item['use'] = i.xpath('./tbody/tr[7]/td/text()').extract()[0]
                item['address'] = i.xpath('./tbody/tr[8]/td/text()').extract()[0]

                yield item


if __name__ == '__main__':
    pass