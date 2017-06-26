#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.console_pipeline import ConsolePipeline
from sasila.slow_system.pipeline.text_pipeline import TextPipelineCar

from base_processor import BaseProcessor
from sasila.slow_system.downloader.http.spider_request import Request
from xpinyin import Pinyin
import json
import time
from sasila.slow_system.utils.decorator import testResponse
from sasila.slow_system.utils import logger
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


class Car_Processor(BaseProcessor):
    spider_id = 'car_spider'
    spider_name = 'car_spider'
    allowed_domains = ['che168.com']
    start_requests = [Request(url='http://www.che168.com', priority=0)]

    @testResponse
    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')
        province_div_list = soup.select('div.city-list div.cap-city > div.fn-clear')
        for province_div in province_div_list:
            province_name = province_div.select('span.capital a')[0].text
            city_list = province_div.select('div.city a')
            for city in city_list:
                city_name = city.text
                request = Request(
                        url='http://www.che168.com/handler/usedcarlistv5.ashx?action=brandlist&area=%s' % Pinyin().get_pinyin(
                                city_name, splitter=''), priority=1, callback=self.process_page_1)
                request.meta['province'] = province_name
                request.meta['city'] = city_name
                yield request

    @testResponse
    def process_page_1(self, response):
        brand_list = list(json.loads(response.m_response.content.decode('gb2312')))
        for brand in brand_list:
            brand_dict = dict(brand)
            brand_name = brand_dict['name']
            url = response.nice_join(brand_dict['url']) + '/'
            request = Request(url=url, priority=2, callback=self.process_page_2)
            request.meta['province'] = response.request.meta['province']
            request.meta['city'] = response.request.meta['city']
            request.meta['brand'] = brand_name
            yield request

    @testResponse
    def process_page_2(self, response):
        soup = bs(response.m_response.content, 'lxml')
        cars_line_list = soup.select('div#series div.content-area dl.model-list dd a')
        for cars_line in cars_line_list:
            cars_line_name = cars_line.text
            url = 'http://www.che168.com' + cars_line['href']
            request = Request(url=url, priority=3, callback=self.process_page_3)
            request.meta['province'] = response.request.meta['province']
            request.meta['city'] = response.request.meta['city']
            request.meta['brand'] = response.request.meta['brand']
            request.meta['cars_line'] = cars_line_name
            yield request

    @testResponse
    def process_page_3(self, response):
        soup = bs(response.m_response.content, 'lxml')
        car_info_list = soup.select('div#a2 ul#viewlist_ul li a.carinfo')
        for car_info in car_info_list:
            url = 'http://www.che168.com' + car_info['href']
            request = Request(url=url, priority=4, callback=self.process_page_4)
            request.meta['province'] = response.request.meta['province']
            request.meta['city'] = response.request.meta['city']
            request.meta['brand'] = response.request.meta['brand']
            request.meta['cars_line'] = response.request.meta['cars_line']
            yield request
        next_page = soup.find(lambda tag: tag.name == 'a' and '下一页' in tag.text)
        if next_page:
            url = 'http://www.che168.com' + next_page['href']
            request = Request(url=url, priority=3, callback=self.process_page_3)
            request.meta['province'] = response.request.meta['province']
            request.meta['city'] = response.request.meta['city']
            request.meta['brand'] = response.request.meta['brand']
            request.meta['cars_line'] = response.request.meta['cars_line']
            yield request

    @testResponse
    def process_page_4(self, response):
        try:
            soup = bs(response.m_response.content, 'lxml')
            # <html><head><title>Object moved</title></head><body>
            # <h2>Object moved to <a href="/CarDetail/wrong.aspx?errorcode=5&amp;backurl=/&amp;infoid=21415515">here</a>.</h2>
            # </body></html>
            if len(soup.select('div.car-title h2')) != 0:
                car = soup.select('div.car-title h2')[0].text
                detail_list = soup.select('div.details li')
                if len(detail_list) == 0:
                    soup = bs(response.m_response.content, 'html5lib')
                    detail_list = soup.select('div.details li')
                mileage = detail_list[0].select('span')[0].text.replace('万公里', '')
                first_borad_date = detail_list[1].select('span')[0].text
                gear = detail_list[2].select('span')[0].text.split('／')[0]
                displacement = detail_list[2].select('span')[0].text.split('／')[1]
                price = soup.select('div.car-price ins')[0].text.replace('￥', '')
                crawl_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

                item = dict()
                item['car'] = car
                item['mileage'] = mileage
                item['first_borad_date'] = first_borad_date
                item['gear'] = gear
                item['displacement'] = displacement
                item['price'] = price
                item['crawl_date'] = crawl_date

                item['province'] = response.request.meta['province']
                item['city'] = response.request.meta['city']
                item['brand'] = response.request.meta['brand']
                item['cars_line'] = response.request.meta['cars_line']
                yield item
        except Exception:
            logger.error(
                'process error: ' + response.request.url + '\r\n' + response.m_response.content + '\r\n' + traceback.format_exc())


if __name__ == '__main__':
    spider = RequestSpider(Car_Processor()).set_pipeline(ConsolePipeline()).set_pipeline(
            TextPipelineCar()).start()
