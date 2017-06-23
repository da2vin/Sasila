#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sasila.slow_system.pipeline.base_pipeline import ItemPipeline
import codecs

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
            with codecs.open("result.csv", 'a', 'gb2312') as f:
                f.write(
                        item["province"] + ',' +
                        item["city"] + ',' +
                        item["brand"] + ',' +
                        item["cars_line"] + ',' +
                        item["car"] + ',' +
                        item["mileage"] + ',' +
                        item["first_borad_date"] + ',' +
                        item["gear"] + ',' +
                        item["displacement"] + ',' +
                        item["price"] + ',' +
                        item["crawl_date"] + "\n"
                )
        except:
            with codecs.open("result.csv", 'a', 'utf8') as f:
                f.write(
                        item["province"] + ',' +
                        item["city"] + ',' +
                        item["brand"] + ',' +
                        item["cars_line"] + ',' +
                        item["car"] + ',' +
                        item["mileage"] + ',' +
                        item["first_borad_date"] + ',' +
                        item["gear"] + ',' +
                        item["displacement"] + ',' +
                        item["price"] + ',' +
                        item["crawl_date"] + "\n"
                )
