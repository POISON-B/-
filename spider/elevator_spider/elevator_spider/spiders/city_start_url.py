#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 18-8-3 上午10:22
# @Author  : Shark
# @Site    : 
# @File    : city_start_url.py
# @Software: PyCharm
import scrapy
import csv
import codecs

start_url_dict = dict()


def xian(**kwargs):
    """
    类属性：
        url2 = 'http://weixin.xseii.com.cn/wx96333/qc?regcode={0}'
        url1 = 'http://www.xseii.com.cn/getDtSearchValues'
        regcode = 1300000
        code = COED_ID_1
         payload = {
         'regcode': '1571333'
        }
        以上属性写入EvInfoSpider类属性中
    有回掉函数还需传入回调函数名

    :return: scrapy post请求对象
    """

    return scrapy.FormRequest(url=kwargs['url1'], formdata=kwargs['payload'], callback=kwargs['callback'])


def wuhu(**kwargs):
    """
    类属性：
        url = 'http://dtjy.zjj.wuhu.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=0000{0}'
        num = 0
    :param kwargs:
    :return:
    """

    if len(str(kwargs['num'])) == 1:
        return scrapy.Request(url=kwargs['url'].format(kwargs['num']), callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 2:
        kwargs['num'] += 1
        return scrapy.Request(
            url='http://dtjy.zjj.wuhu.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=0000{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 3:
        kwargs['num'] += 1
        return scrapy.Request(
            url='http://dtjy.zjj.wuhu.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=00{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(self.num)) == 4:
        kwargs['num'] += 1
        return scrapy.Request(
            url='http://dtjy.zjj.wuhu.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=0{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 5:
        kwargs['num'] += 1
        return scrapy.Request(
            url='http://dtjy.zjj.wuhu.gov.cn/qt/OnlineQRCode.aspx?ElevatorId={0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)


def tianjin(**kwargs):
    """
    类属性：
        url = 'http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=00000{0}'
        num = 0
    :param kwargs:
    :return:
    """

    if len(str(kwargs['num'])) == 1:
        return scrapy.Request(url=kwargs['url'].format(kwargs['num']), callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 2:
        return scrapy.Request(
            url='http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=0000{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 3:
        return scrapy.Request(
            url='http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=000{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 4:
        return scrapy.Request(
            url='http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=00{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 5:
        return scrapy.Request(
            url='http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=0{0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)

    elif len(str(kwargs['num'])) == 6:
        return scrapy.Request(
            url='http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId={0}'.format(kwargs['num']),
            callback=kwargs['callback'], dont_filter=True)


def nanjing():
    urls = codecs.open('url.csv', 'r')
    return urls


def chengdu():
    urls = codecs.open('url.csv', 'r')
    return urls


def nanjing2(**kwargs):
        """
        类属性：
            url = 'http://dtpt.scjg.tj.gov.cn/qt/OnlineQRCode.aspx?ElevatorId=00000{0}'
            num = 0
        :param kwargs:
        :return:
        """

        if len(str(kwargs['num'])) == 1:
            return scrapy.Request(url=kwargs['url'].format(kwargs['num']), callback=kwargs['callback'],
                                  dont_filter=True)

        elif len(str(kwargs['num'])) == 2:
            return scrapy.Request(
                url='http://njdt.njtjy.org.cn/lift/getLift/0000{0}'.format(kwargs['num']),
                callback=kwargs['callback'], dont_filter=True)

        elif len(str(kwargs['num'])) == 3:
            return scrapy.Request(
                url='http://njdt.njtjy.org.cn/lift/getLift/000{0}'.format(kwargs['num']),
                callback=kwargs['callback'], dont_filter=True)

        elif len(str(kwargs['num'])) == 4:
            return scrapy.Request(
                url='http://njdt.njtjy.org.cn/lift/getLift/00{0}'.format(kwargs['num']),
                callback=kwargs['callback'], dont_filter=True)

        elif len(str(kwargs['num'])) == 5:
            return scrapy.Request(
                url='http://njdt.njtjy.org.cn/lift/getLift/0{0}'.format(kwargs['num']),
                callback=kwargs['callback'], dont_filter=True)

        elif len(str(kwargs['num'])) == 6:
            return scrapy.Request(
                url='http://njdt.njtjy.org.cn/lift/getLift/{0}'.format(kwargs['num']),
                callback=kwargs['callback'], dont_filter=True)


start_url_dict['西安'] = xian
start_url_dict['芜湖'] = wuhu
start_url_dict['天津'] = tianjin
start_url_dict['南京'] = nanjing
start_url_dict['成都'] = chengdu
start_url_dict['南京2'] = nanjing2


class URLFactory(object):
    def __init__(self, key):
        self.key = key

    def get_obj(self):
        if self.key in start_url_dict.keys():
            return start_url_dict[self.key]


if __name__ == '__main__':
    for i in chengdu():
        print(i)
