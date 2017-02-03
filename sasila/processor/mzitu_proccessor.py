#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs

from base_processor import BaseProcessor
from sasila.core.request_spider import RequestSpider
from sasila.downloader.http.spider_request import Request
from sasila.pipeline.pic_pipeline import PicPipeline

reload(sys)
sys.setdefaultencoding('utf-8')


class MezituProcessor(BaseProcessor):
    spider_id = 'mzitu'
    spider_name = 'mzitu'
    start_requests = [Request(url='http://www.mzitu.com/xinggan')]

    def process(self, response):
        soup = bs(response.content, "lxml")
        total_page = int(soup.select_one("a.next.page-numbers").find_previous_sibling().text)
        for page in range(1, total_page + 1):
            yield Request(url="http://www.mzitu.com/xinggan/page/" + str(page), callback=self.get_page_content)

    def get_page_content(self, response):
        soup = bs(response.content, 'lxml')
        li_list = soup.select("div.postlist ul#pins li")
        for li in li_list:
            yield Request(url=li.select_one("a").attrs["href"], callback=self.get_pic, priority=1)

    def get_pic(self, response):
        li_soup = bs(response.content, "lxml")
        if li_soup.find(lambda tag: tag.name == 'a' and '下一页»' in tag.text) is not None:
            total_page = int(li_soup.find(lambda tag: tag.name == 'a' and '下一页»' in tag.text) \
                             .find_previous_sibling().text)
            for page in range(1, total_page + 1):
                yield Request(url=response.request.url + "/" + str(page), callback=self.download_pic, priority=2)

    def download_pic(self, response):
        href = bs(response.content, "lxml").select_one("div.main-image img").attrs["src"]
        yield Request(url=href, callback=self.download, priority=99)

    def download(self, response):
        if response.status_code == 200:
            yield response.content


if __name__ == '__main__':
    spider = RequestSpider(MezituProcessor()).set_pipeline(PicPipeline()).start()
