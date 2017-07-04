#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.console_pipeline import ConsolePipeline

from base_processor import BaseProcessor
from sasila.slow_system.downloader.http.spider_request import Request

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
                if response.is_url(url):
                    yield Request(url=url, callback=self.procces2)

    def procces2(self, response):
        if response.m_response:
            soup = bs(response.m_response.content, 'lxml')
            yield soup.title
            a_list = soup.select("a")
            for a in a_list:
                if "href" in a.attrs:
                    url = response.nice_join(a["href"])
                    if response.is_url(url):
                        yield Request(url=url, callback=self.procces2)
        else:
            print response.request.url


if __name__ == '__main__':
    spider = RequestSpider(FirstProcessor()).set_pipeline(ConsolePipeline()).start()
