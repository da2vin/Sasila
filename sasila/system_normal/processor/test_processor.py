#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.processor.base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request
from sasila.system_normal.utils.decorator import checkResponse
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.pic_pipeline import PicPipeline
from sasila.system_normal.pipeline.pipe_item import pipeItem
from sasila.system_normal.pipeline.test_pipeline import TestPipeline

from bs4 import BeautifulSoup as bs
import hashlib
import time
import random
import sys

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')



class TEST_Processor(BaseProcessor):
    spider_id = 'zhu_spider'
    spider_name = 'zhu_spider'
    allowed_domains = ['zhuwang.cc']
    start_requests = [Request(url='http://www.zhuwang.cc/list-58-1.html', priority=0)]

    @checkResponse
    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')

        page_list = soup.select('div.zxpage a')
        total_page = int(page_list[page_list.__len__()-2].text)
        page = 1
        while page<=total_page:
            yield Request(url='http://www.zhuwang.cc/list-58-%d.html' % page,callback=self.process_page, priority=0,duplicate_remove=False)
            page +=1

    @checkResponse
    def process_page(self, response):
        soup = bs(response.m_response.content, 'lxml')

        zhu_div_list = soup.select('div.zxleft ul li')
        for zhu_div in zhu_div_list:
            detail_url = zhu_div.select('a')[0]['href']
            img_url = zhu_div.select('a img')[0]['src']
            title = zhu_div.select('a img')[0]['alt'].strip()
            shortDes = zhu_div.select('p.zxleft32 a')[0].text

            md5 = hashlib.md5()
            rand_name = str(time.time()) + str(random.random())
            md5.update(rand_name.encode(encoding='utf-8'))
            img_name = md5.hexdigest() + '.jpg'

            request = Request(url=img_url, priority=1, callback=self.process_pic)
            request.meta['img_name'] = img_name
            yield request

            request = Request(url=detail_url, priority=1, callback=self.process_detail)
            request.meta['title'] = title
            request.meta['shortDes'] = shortDes
            request.meta['img_name'] = img_name
            yield request

    @checkResponse
    def process_pic(self, response):
        result = response.m_response.content
        yield pipeItem(['save'],result)

    @checkResponse
    def process_detail(self, response):
        soup = bs(response.m_response.content, 'lxml')

        dd_tail = soup.select('div.zxxwleft p.zxxw2')[0].text.replace('来源： ','').replace('来源：','').split(' ')
        date_time = dd_tail[1].strip() + ' ' + dd_tail[2].strip().replace('|','')
        newsFrom = dd_tail[0].strip()

        result = dict()
        result['date_time'] = date_time
        result['newsFrom'] = newsFrom

        yield pipeItem(['console','test'],result)

if __name__ == '__main__':
    SpiderCore(TEST_Processor()).set_pipeline(ConsolePipeline(),'console')\
        .set_pipeline(PicPipeline(),'save').set_pipeline(TestPipeline(),'test').start()