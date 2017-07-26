#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.text_pipeline import TextPipelineBendibao

from sasila.system_normal.processor.base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request
from sasila.system_normal.utils.decorator import checkResponse

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

start_requests_temp = []

with open(name='city.txt', mode='r') as fs:
    lines = fs.readlines()
    for line in lines:
        request_temp = Request(url=line.strip().split(',')[0] + 'wangdian/', priority=0)
        request_temp.meta["city_name"] = line.strip().split(',')[1]
        start_requests_temp.append(request_temp)


class Bendibao_Processor(BaseProcessor):
    spider_id = 'bendibao_spider'
    spider_name = 'bendibao_spider'
    allowed_domains = ['bendibao.com']
    start_requests = start_requests_temp

    @checkResponse
    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')
        category1 = soup.select('div.navlink')
        for category in category1:
            category1_name = category.select('div.title h2')[0].text
            category_2 = category.select('ul.topic li a')
            for category_2_one in category_2:
                url = response.nice_join(category_2_one['href']) + '/'
                category_2_name = category_2_one.text
                request = Request(url=url, priority=1, callback=self.process_page_1)
                request.meta['city_name'] = response.request.meta['city_name']
                request.meta['category1_name'] = category1_name
                request.meta['category2_name'] = category_2_name
                yield request

    @checkResponse
    def process_page_1(self, response):
        if '下暂无网点信息' not in response.m_response.content:
            soup = bs(response.m_response.content, 'lxml')
            results = soup.select('ul.catalist li')
            for result in results:
                result_name = result.select("div.infoschema h3 a")[0].text
                result_mobile = result.find(lambda tag: tag.name == 'p' and '电话：' in tag.text).text
                m_result = dict()
                m_result['result_name'] = result_name
                m_result['result_mobile'] = result_mobile.replace('电话：', '')
                m_result['city_name'] = response.request.meta['city_name']
                m_result['category1_name'] = response.request.meta['category1_name']
                m_result['category2_name'] = response.request.meta['city_name']
                yield m_result
            next_page = soup.find(lambda tag: tag.name == 'a' and '下一页' in tag.text)
            if next_page:
                url_splits = response.request.url.split('/')
                url_splits[-1] = next_page['href']
                url = '/'.join(url_splits)
                request = Request(url=url, priority=1, callback=self.process_page_1)
                request.meta['city_name'] = response.request.meta['city_name']
                request.meta['category1_name'] = response.request.meta['category1_name']
                request.meta['category2_name'] = response.request.meta['category2_name']
                yield request


if __name__ == '__main__':
    SpiderCore(Bendibao_Processor(), time_sleep=0.5).set_pipeline(TextPipelineBendibao()).set_pipeline(
            ConsolePipeline()).start()
