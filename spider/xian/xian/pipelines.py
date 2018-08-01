# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from xian.uitl import db_evIfo, db_session, db_evIfo_query

logger = logging.getLogger(__name__)


class XianPipeline(object):

    def process_item(self, item, spider):
        if not db_evIfo_query.filter_by(id=item['code']).first():
            ev_info = db_evIfo(
                id=item['code'],
                brand=item['brand'],
                reg_code=item['regcode'],
                inspection_unit_name=item['test'],
                maintenance_company_name=item['maintenance'],
                customer_name=item['use'],
                project_addr=item['address'],
                customer_addr=item['region']
            )
            db_session.add(ev_info)
            db_session.commit()

            return item

