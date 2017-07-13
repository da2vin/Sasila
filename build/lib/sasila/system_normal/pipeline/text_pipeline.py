#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sasila.system_normal.pipeline.base_pipeline import ItemPipeline
from sasila.system_normal.utils import logger
import traceback
import codecs

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TextPipeline(ItemPipeline):
    def process_item(self, item):
        with open("result.txt", 'a') as f:
            f.write(
                    item["province"] + ',' +
                    item["city"] + ',' +
                    item["company_name"] + ',' +
                    item["company_man"] + ',' +
                    item["company_telephone"] + ',' +
                    item["company_address"] + ',' +
                    item["company_registered_capital"] + ',' +
                    item["company_registered_time"] + ',' +
                    item["company_status"] + ',' +
                    item["source"] + ',' +
                    item["update_time"] + "\n"
            )


class TextPipelineCar(ItemPipeline):
    def process_item(self, item):
        try:
            with codecs.open("result.csv", 'a', 'gbk') as f:
                f.write(
                        item["province"] + ',' +
                        item["city"] + ',' +
                        item["brand"].replace(u'\u30fb', '·') + ',' +
                        item["cars_line"].replace(u'\u30fb', '·') + ',' +
                        item["car"].replace(u'\u30fb', '·') + ',' +
                        item["mileage"] + ',' +
                        item["first_borad_date"] + ',' +
                        item["gear"] + ',' +
                        item["displacement"] + ',' +
                        item["price"] + ',' +
                        item["crawl_date"] + "\n"
                )
        except:
            logger.error(traceback.format_exc())


class TextPipelineFang(ItemPipeline):
    def process_item(self, item):
        try:
            with codecs.open("fang.csv", 'a', 'gbk') as f:
                f.write(
                        item["province"] + ',' +
                        item["city"] + ',' +
                        item["district"] + ',' +
                        item["avg_price"] + ',' +
                        item["estate"].replace(',', '，') + ',' +
                        item["area"] + ',' +
                        item["layout"] + ',' +
                        item["total_price"] + ',' +
                        item["crawl_date"] + ',' +
                        item["url"] + "\n"
                )
        except:
            logger.error(traceback.format_exc())


class TextPipelineFangShop(ItemPipeline):
    def process_item(self, item):
        try:
            with codecs.open("fang_shop.csv", 'a', 'gbk') as f:
                f.write(
                        item["city"] + ',' +
                        item["district"] + ',' +
                        item["estate"].replace(',', '，') + ',' +
                        item["floor"] + ',' +
                        item["total_floor"] + ',' +
                        item["type"] + ',' +
                        item["area"] + ',' +
                        item["total_price"] + ',' +
                        item["crawl_date"] + ',' +
                        item["url"] + "\n"
                )
        except:
            logger.error(traceback.format_exc())
