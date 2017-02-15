#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.pic_pipeline import PicPipeline

from base_processor import BaseProcessor, Rule, LinkExtractor
from sasila.slow_system.downloader.http.spider_request import Request
from bs4 import BeautifulSoup as bs

reload(sys)
sys.setdefaultencoding('utf-8')


class FeProcessor(BaseProcessor):
    spider_id = 'mzitu'
    spider_name = 'mzitu'
    start_requests = [Request(url='http://www.58.com/daikuan/changecity/')]

    rules = (
        Rule(LinkExtractor(regex_str=r"http://[a-z]*?.58.com/daikuan/"), priority=0),
        Rule(LinkExtractor(regex_str=r"/daikuan/pn\d+/"), priority=1),
        Rule(LinkExtractor(css_str="table.small-tbimg a.t"), priority=3, callback='save'),
    )

    def save(self, response):
        if response.m_response:
            print bs(response.m_response.content, 'lxml').title.string


if __name__ == '__main__':
    spider = RequestSpider(FeProcessor()).set_pipeline(PicPipeline()).start()
