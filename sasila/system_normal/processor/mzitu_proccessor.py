#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.system_normal.spider.request_spider import RequestSpider
from sasila.system_normal.pipeline.pic_pipeline import PicPipeline

from base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request

reload(sys)
sys.setdefaultencoding('utf-8')


class MezituProcessor(BaseProcessor):
    spider_id = 'mzitu'
    spider_name = 'mzitu'
    allowed_domains = ['mzitu.com', 'meizitu.net']
    start_requests = [Request(url='http://www.mzitu.com/xinggan')]

    def process(self, response):
        if response.m_response:
            soup = bs(response.m_response.content, "lxml")
            total_page = int(soup.select_one("a.next.page-numbers").find_previous_sibling().text)
            for page in range(1, total_page + 1):
                yield Request(url="http://www.mzitu.com/xinggan/page/" + str(page), callback=self.get_page_content)

    def get_page_content(self, response):
        if response.m_response:
            soup = bs(response.m_response.content, 'lxml')
            li_list = soup.select("div.postlist ul#pins li")
            for li in li_list:
                yield Request(url=li.select_one("a").attrs["href"], callback=self.get_pic, priority=1)

    def get_pic(self, response):
        if response.m_response:
            li_soup = bs(response.m_response.content, "lxml")
            if li_soup.find(lambda tag: tag.name == 'a' and '下一页»' in tag.text) is not None:
                total_page = int(li_soup.find(lambda tag: tag.name == 'a' and '下一页»' in tag.text) \
                                 .find_previous_sibling().text)
                for page in range(1, total_page + 1):
                    yield Request(url=response.request.url + "/" + str(page), callback=self.download_pic, priority=2)

    def download_pic(self, response):
        if response.m_response:
            href = bs(response.m_response.content, "lxml").select_one("div.main-image img").attrs["src"]
            yield Request(url=href, callback=self.download, priority=3)

    def download(self, response):
        if response.m_response:
            if response.m_response.status_code == 200:
                yield response.m_response.content


# mzitu_spider = RequestSpider(MezituProcessor()).set_pipeline(PicPipeline())
#
# if __name__ == '__main__':
#     spider = RequestSpider(MezituProcessor()).set_pipeline(PicPipeline()).start()
