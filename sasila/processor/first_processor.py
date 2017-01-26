#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.core.request_spider import RequestSpider
from sasila.pipeline.console_pipeline import ConsolePipeline
from sasila.downloader.selenium_downloader import SeleniumDownLoader

from base_processor import BaseProcessor
from sasila.downloader.spider_request import Request

reload(sys)
sys.setdefaultencoding('utf-8')


class FirstProcessor(BaseProcessor):
    spider_id = 'test'
    spider_name = 'test'

    def process(self, response):
        soup = bs(response.content, 'lxml')
        a_list = soup.select("a")
        for a in a_list:
            if "href" in a.attrs:
                url = self._nice_join(response.request.url, a["href"])
                if self._is_url(url):
                    yield Request(url=url, callback=self.procces2)

    def procces2(self, response):
        soup = bs(response.content, 'lxml')
        yield soup.title
        a_list = soup.select("a")
        for a in a_list:
            if "href" in a.attrs:
                url = self._nice_join(response.request.url, a["href"])
                if self._is_url(url):
                    yield Request(url=url, callback=self.procces2)


if __name__ == '__main__':
    spider = RequestSpider(FirstProcessor()).set_pipeline(ConsolePipeline()).set_start_request(Request(url="http://www.mzitu.com/")).start()
