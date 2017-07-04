#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.console_pipeline import ConsolePipeline
from sasila.slow_system.pipeline.text_pipeline import TextPipelineFang

from sasila.slow_system.processor.base_processor import BaseProcessor
from sasila.slow_system.downloader.http.spider_request import Request
import time
from sasila.slow_system.utils.decorator import checkResponse

reload(sys)
sys.setdefaultencoding('utf-8')


class Fang_Processor(BaseProcessor):
    spider_id = 'fang_spider'
    spider_name = 'fang_spider'
    allowed_domains = ['fang.com']
    start_requests = [Request(url='http://esf.gz.fang.com/newsecond/esfcities.aspx', priority=0)]

    @checkResponse
    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')
        province_list = {u'四川', u'江苏', u'江西', u'山东', u'广东', u'山西'}
        province_div_list = soup.select('div#c02 ul li')
        for province_div in province_div_list:
            province_name = province_div.select('strong')[0].text
            if province_name != '其他':
                if province_name in province_list:
                    city_list = province_div.select('a')
                    for city in city_list:
                        city_name = city.text
                        url = city['href']
                        request = Request(url=url, priority=1, callback=self.process_page_1)
                        request.meta['province'] = province_name
                        request.meta['city'] = city_name
                        yield request

    @checkResponse
    def process_page_1(self, response):
        soup = bs(response.m_response.content, 'lxml')
        district_list = soup.select('div.qxName a')
        district_list.pop(0)
        for district in district_list:
            district_name = district.text
            url = response.request.url + district['href']
            request = Request(url=url, priority=2, callback=self.process_page_2)
            request.meta['province'] = response.request.meta['province']
            request.meta['city'] = response.request.meta['city']
            request.meta['district'] = district_name
            yield request

    @checkResponse
    def process_page_2(self, response):
        soup = bs(response.m_response.content, 'lxml')
        avg_price_list = soup.select('div.newcardR dl')
        if len(avg_price_list) > 0:
            avg_price = avg_price_list[1].select('dd b')[0].text
        else:
            avg_price = '未知'
        detail_list = soup.select('div.houseList dl')
        for detail in detail_list:
            if len(detail.select('p.mt10 a span')) != 0:
                estate = detail.select('p.mt10 a span')[0].text
                area = detail.select('div.area p')[0].text.replace('㎡', '')
                layout = detail.select('p.mt12')[0].text.split('|')[0].strip()
                total_price = detail.select('div.moreInfo p.mt5 span.price')[0].text
                crawl_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
                item = dict()
                item['avg_price'] = avg_price
                item['estate'] = estate
                item['area'] = area
                item['layout'] = layout
                item['total_price'] = total_price
                item['crawl_date'] = crawl_date

                item['province'] = response.request.meta['province']
                item['city'] = response.request.meta['city']
                item['district'] = response.request.meta['district']
                item['url'] = response.request.url
                yield item

        next_page = soup.select('a#PageControl1_hlk_next')
        if len(next_page) > 0:
            url = response.nice_join(next_page[0]['href'])
            request = Request(url=url, priority=2, callback=self.process_page_2)
            request.meta['province'] = response.request.meta['province']
            request.meta['city'] = response.request.meta['city']
            request.meta['district'] = response.request.meta['district']
            yield request


if __name__ == '__main__':
    spider = RequestSpider(Fang_Processor()).set_pipeline(ConsolePipeline()).set_pipeline(TextPipelineFang()).start()
