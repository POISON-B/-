# -*- coding: utf-8 -*-
import scrapy
from xian.items import XianItem

from xian.uitl import handle_value, COED_ID_1


class EvInfoSpider(scrapy.Spider):
    name = 'ev_info'
    allowed_domains = ['weixin.xseii.com.cn']
    start_urls = ['http://weixin.xseii.com.cn/wx96333/qc?regcode=31106101182012100029']
    url = 'http://weixin.xseii.com.cn/wx96333/qc?regcode=3110610118201'

    def parse(self, response):
        item = XianItem()
        for i in response.xpath('//table[@class="table"]'):
            if i.xpath('./tbody/tr[1]/td/text()').extract():
                item['code'] = i.xpath('./tbody/tr[1]/td/text()').extract()[0]
                item['regcode'] = i.xpath('./tbody/tr[2]/td/text()').extract()[0]
                # item['region'] = i.xpath('./tbody/tr[3]/td/text()').extract()[0]
                item['brand'] = handle_value(str(i.xpath('./tbody/tr[4]/td/text()').extract()))
                item['test'] = handle_value(str(i.xpath('./tbody/tr[5]/td/text()').extract()))
                item['maintenance'] = i.xpath('./tbody/tr[6]/td/text()').extract()[0]
                item['use'] = i.xpath('./tbody/tr[7]/td/text()').extract()[0]
                item['address'] = i.xpath('./tbody/tr[8]/td/text()').extract()[0]

                yield item

        for code in range(COED_ID_1[0], COED_ID_1[1]):
            yield scrapy.Request(self.url + str(code), callback=self.parse)

