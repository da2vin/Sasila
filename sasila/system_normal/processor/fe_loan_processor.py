#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.system_normal.spider.request_spider import RequestSpider
from sasila.system_normal.pipeline.pic_pipeline import PicPipeline

from base_processor import BaseProcessor, Rule, LinkExtractor
from sasila.system_normal.downloader.http.spider_request import Request
from bs4 import BeautifulSoup as bs

reload(sys)
sys.setdefaultencoding('utf-8')


class FeProcessor(BaseProcessor):
    spider_id = 'fe'
    spider_name = 'fe'
    allowed_domains = ['58.com']
    start_requests = [Request(url='http://www.58.com/daikuan/changecity/')]

    rules = (
        Rule(LinkExtractor(regex_str=r"http://[a-z]*?.58.com/daikuan/"), priority=0),
        Rule(LinkExtractor(regex_str=r"/daikuan/pn\d+/"), priority=1),
        Rule(LinkExtractor(css_str="table.small-tbimg a.t"), priority=3, callback='save'),
    )

    def save(self, response):
        if response.m_response:
            print bs(response.m_response.content, 'lxml').title.string


fe_spider = RequestSpider(FeProcessor()).set_pipeline(PicPipeline())
if __name__ == '__main__':
    fe_spider.start()
