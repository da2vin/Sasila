#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.pic_pipeline import PicPipeline

from base_processor import BaseProcessor, Rule, LinkExtractor
from sasila.slow_system.downloader.http.spider_request import Request
import os
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')


class MezituProcessor(BaseProcessor):
    spider_id = 'mzitu'
    spider_name = 'mzitu'
    start_requests = [Request(url='http://www.mzitu.com/xinggan')]

    rules = (
        Rule(LinkExtractor(regex_str=r"http://i.meizitu.net/\d{4}/\d{2}/[0-9a-z]+.jpg"),
             callback="save", priority=3),
        Rule(LinkExtractor(regex_str=r"http://www.mzitu.com/\d+"), priority=1),
        Rule(LinkExtractor(regex_str=r"http://www.mzitu.com/\d+/\d+"), priority=2),
        Rule(LinkExtractor(regex_str=r"http://www.mzitu.com/xinggan/page/\d+"), priority=0),
    )

    def save(self, response):
        if response.m_response:
            if not os.path.exists("img"):
                os.mkdir("img")
            with open("img/" + str(uuid.uuid1()) + ".jpg", 'wb') as fs:
                fs.write(response.m_response.content)
                print("download success!")


if __name__ == '__main__':
    spider = RequestSpider(MezituProcessor()).set_pipeline(PicPipeline()).start()
