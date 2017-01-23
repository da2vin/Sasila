#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from base_processor import BaseProcessor
from core.spider_core import SpiderCore
from downloader.spider_request import Request
from bs4 import BeautifulSoup as bs

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
                    yield Request(url=url)


if __name__ == '__main__':
    spider = SpiderCore(FirstProcessor()).set_start_request(Request(url="http://www.mzitu.com/")).start()
