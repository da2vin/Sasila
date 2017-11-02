#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline

from sasila.system_normal.processor.base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class FirstProcessor(BaseProcessor):
    spider_id = 'test'
    spider_name = 'test'
    allowed_domains = ['mzitu.com']
    start_requests = [Request(url="http://www.mzitu.com/")]

    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')
        a_list = soup.select("a")
        for a in a_list:
            if "href" in a.attrs:
                url = response.nice_join(a["href"])
                yield {'url': url}

# if __name__ == '__main__':
#     spider = SpiderCore(FirstProcessor()).set_pipeline(ConsolePipeline()).start()
