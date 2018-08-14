#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-1 下午5:07
# @Author  : Shark
# @Site    : 
# @File    : city_parser.py
# @Software: PyCharm

from abc import ABCMeta, abstractmethod
import re
import json
from scrapy.loader import ItemLoader

from elevator_spider.items import ItemFactory
from elevator_spider.uitl import handle_value

methods_dict = dict()


class CityParser(object, metaclass=ABCMeta):

    @abstractmethod
    def parse(self, response, city_name):
        pass

    def save(self):
        pass


class XianCityParser(CityParser):
    def parse(self, response, city_name):
        item = ItemFactory(city_name).get_methods()
        for i in response.xpath('//table[@class="table"]'):
            if i.xpath('./tbody/tr[1]/td/text()').extract():
                item['code'] = i.xpath('./tbody/tr[1]/td/text()').extract_first()
                item['regcode'] = i.xpath('./tbody/tr[2]/td/text()').extract_first()
                item['region'] = i.xpath('./tbody/tr[3]/td/text()').extract_first()
                item['brand'] = i.xpath('./tbody/tr[4]/td/text()').extract_first()
                item['test'] = i.xpath('./tbody/tr[5]/td/text()').extract_first()
                item['maintenance'] = i.xpath('./tbody/tr[6]/td/text()').extract_first()
                item['use'] = i.xpath('./tbody/tr[7]/td/text()').extract_first()
                item['address'] = i.xpath('./tbody/tr[8]/td/text()').extract_first()

                return item


class WuhuCityParser(CityParser):

    def parse(self, response, city_name):
        item = ItemFactory(city_name).get_methods()
        if response.xpath('//*[@id="lblReportNo"]/text()').extract():
            item['elevator_number'] = response.xpath('//*[@id="lblReportNo"]/text()').extract_first()
            item['address'] = response.xpath('//*[@id="lblElevatorName"]/text()').extract_first()
            item['customer_name'] = response.xpath('//*[@id="lblHouseName"]/text()').extract_first()
            item['phone'] = response.xpath('//*[@id="lblHouseTel"]/text()').extract_first()
            item['reg_code'] = response.xpath('//*[@id="lblRegisterNo"]/text()').extract_first()
            item['next_inspect_date'] = response.xpath('//*[@id="lblNextChecktime"]/text()').extract_first()
            item['maintenance_company_name'] = response.xpath('//*[@id="lblGroupName"]/text()').extract_first()

            return item


class TianJinParser(CityParser):

    def parse(self, response, city_name):
        item = ItemFactory(city_name).get_methods()
        if response.xpath('//*[@id="lblReportNo"]/text()').extract():
            item['id'] = response.xpath('//*[@id="lblReportNo"]/text()').extract_first()
            item['reg_code'] = response.xpath('//*[@id="lblRegisterNo"]/text()').extract_first()
            item['customer_name'] = response.xpath('//*[@id="lblHouseName"]/text()').extract_first()
            item['use_phone'] = response.xpath('//*[@id="lblHouseTel"]/text()').extract_first()
            item['maintenance_company_name'] = response.xpath('//*[@id="lblGroupName"]/text()').extract_first()
            item['help_phone'] = response.xpath('//*[@id="lblGroupTel"]/text()').extract_first()
            item['complaints_phone'] = response.xpath('//*[@id="lblTsTel"]/text()').extract_first()
            item['next_inspect_date'] = response.xpath('//*[@id="lblNextChecktim"]/text()').extract_first()
            item['up_inspect_date'] = response.xpath('//*[@id="lblCheckDate"]/text()').extract_first()

            return item


class NanJingParser(CityParser):
    def parse(self, response, city_name):
        item = ItemFactory(city_name).get_methods()
        item['id'] = response.xpath(r'//*[@id="liftcode"]/text()').extract_first()
        item['maintenance_company_name'] = response.xpath(r'//*[@id="addDiv"]/div[1]/div[2]/div[1]/p/b[1]/text()').extract_first()
        item['reg_code'] = response.xpath(r'//*[@id="regcode"]/text()').extract_first()
        item['phone'] = response.xpath(r'//*[@id="company"]/b/a/text()').extract_first()
        a = response.xpath(r'//*[@id="company"]/text()').extract()
        try:
            if a:
                item['customer_name'] = a[3]
        except:
            item['customer_name'] = None
        item['project_addr'] = response.xpath(r'//*[@id="liftAddress"]/text()').extract_first()
        item['next_inspect_date'] = response.xpath(r'//*[@id="nextinspect"]/text()').extract_first()
        item['brand'] = response.xpath(r'//*[@id="baseBrand"]/text()').extract_first()

        return item


class NanJingParser2(CityParser):
    def parse(self, response, city_name):
        item = ItemFactory(city_name).get_methods()
        data = json.loads(response.text, encoding='utf8')
        print(data['liftcode'])
        item['id'] = data['liftcode']
        item['reg_code'] = data['regcode']
        item['manufacture_product_id'] = data['liftid']
        item['maintenance_company_name'] = data['maintain']['maintainName'] or None
        item['maintenance_company_addr'] = data['maintain']['officeaddr'] or None
        item['project_name'] = data['baseCompany']['companyName'] or None
        item['project_addr'] = data['liftaddress']
        item['inspection_unit_name'] = data['inspect']
        item['next_inspect_date'] = data['nextinspect']
        item['country'] = data['baseArea']['areaName'] if data['baseArea'] else None

        return item


class ChengDuParser(CityParser):
    def parse(self, response, city_name):
        item = ItemFactory(city_name).get_methods()
        info = re.findall(r'<tr style="border-top:dashed 1px #999;" align="center">.*?</tr>', response.body_as_unicode(), re.S)
        if info:
            info = str(info).replace('[', '').replace(']', '').replace(
                '<tr style="border-top:dashed 1px #999;" align="center">', '')
            info = info.replace('<td style="background-color:#fff">', '').replace(r'\r\n', '')
            info = info.replace('<td style="background-color:#fff" align="left"> ', '').replace('</td>', '')
            info = info.replace('<br>', '').replace('</tr>', '').replace('           ', '-').replace('-  ', '')
            info = info.replace('        ', '').replace("'", '').replace('电梯-', '')
            info = info.split(",")
            # for i in info:
            #     print(i)
            item['info'] = info

            return item


methods_dict['西安'] = XianCityParser()
methods_dict['芜湖'] = WuhuCityParser()
methods_dict['天津'] = TianJinParser()
methods_dict['南京'] = NanJingParser()
methods_dict['成都'] = ChengDuParser()
methods_dict['南京2'] = NanJingParser2()


class ParseFactory(object):
    def __init__(self, key):
        self.key = key

    def get_obj(self):
        if self.key in methods_dict.keys():
            return methods_dict[self.key]


if __name__ == '__main__':
    pass
