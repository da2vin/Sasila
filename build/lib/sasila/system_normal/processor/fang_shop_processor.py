#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from bs4 import BeautifulSoup as bs
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.text_pipeline import TextPipelineFangShop

from base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request
import time
from sasila.system_normal.utils.decorator import checkResponse
from sasila.system_normal.utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class Fang_Shop_Processor(BaseProcessor):
    spider_id = 'fang_shop_spider'
    spider_name = 'fang_shop_spider'
    allowed_domains = ['fang.com']
    start_requests = [Request(url='http://shop.fang.com', priority=0)]

    @checkResponse
    def process(self, response):
        city_crawl_list = {u'成都', u'南京', u'苏州', u'无锡', u'南昌', u'济南', u'青岛', u'广州', u'东莞'}
        soup = bs('''<a href="http://shop1.fang.com/" style="width:40px;padding:4px 0 4px 8px;">北京</a>
                     <a href="http://shop.sh.fang.com/" style="width:40px;padding:4px 0 4px 8px;">上海</a>
                     <a href="http://shop.gz.fang.com/" style="width:40px;padding:4px 0 4px 8px;">广州</a>
                     <a href="http://shop.sz.fang.com/" style="width:40px;padding:4px 0 4px 8px;">深圳</a>
                     <a href="http://shop.tj.fang.com/" style="width:40px;padding:4px 0 4px 8px;">天津</a>
                     <a href="http://shop.cq.fang.com/" style="width:40px;padding:4px 0 4px 8px;">重庆</a>
                     <a href="http://shop.cd.fang.com/" style="width:40px;padding:4px 0 4px 8px;">成都</a>
                     <a href="http://shop.suzhou.fang.com/" style="width:40px;padding:4px 0 4px 8px;">苏州</a>
                     <a href="http://shop.wuhan.fang.com/" style="width:40px;padding:4px 0 4px 8px;">武汉</a>
                     <a href="http://shop.xian.fang.com/" style="width:40px;padding:4px 0 4px 8px;">西安</a>
                     <a href="http://shop.dg.fang.com/" style="width:40px;padding:4px 0 4px 8px;">东莞</a>
                     <a href="http://shop.km.fang.com/" style="width:40px;padding:4px 0 4px 8px;">昆明</a>
                     <a href="http://shop.hz.fang.com/" style="width:40px;padding:4px 0 4px 8px;">杭州</a>
                     <a href="http://shop.jn.fang.com/" style="width:40px;padding:4px 0 4px 8px;">济南</a>
                     <a href="http://shop.wuxi.fang.com/" style="width:40px;padding:4px 0 4px 8px;">无锡</a>
                     <a href="http://shop.zz.fang.com/" style="width:40px;padding:4px 0 4px 8px;">郑州</a>
                     <a href="http://shop.nc.fang.com/" style="width:40px;padding:4px 0 4px 8px;">南昌</a>
                     <a href="http://shop.qd.fang.com/" style="width:40px;padding:4px 0 4px 8px;">青岛</a>
                     <a href="http://shop.sjz.fang.com/" style="width:40px;padding:4px 0 4px 8px;">石家庄</a>
                     <a href="http://shop.nanjing.fang.com/" style="width:40px;padding:4px 0 4px 8px;">南京</a>
                     <a href="http://shop.dl.fang.com/" style="width:40px;padding:4px 0 4px 8px;">大连</a>''', 'lxml')
        city__list = soup.select('a')
        for city in city__list:
            city_name = city.text
            if city_name in city_crawl_list:
                url = city['href']
                request = Request(url=url, priority=1, callback=self.process_page_1)
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
            request.meta['city'] = response.request.meta['city']
            request.meta['district'] = district_name
            yield request

    @checkResponse
    def process_page_2(self, response):
        soup = bs(response.m_response.content, 'lxml')
        detail_list = soup.select('div.houseList dl')
        for detail in detail_list:
            estate = detail.select('p.mt15 span.spName')[0].text
            detail_str = detail.select('p.mt10')[0].text

            temp_list = detail.select('p.mt10')[0].text.split('/')
            temp_list = [temp.strip() for temp in temp_list]

            if '购物中心/百货' not in detail_str and '层' in detail_str:
                m_type = temp_list[0].replace('类型：', '')
                floor = temp_list[1]
                total_floor = temp_list[2].replace('层', '')
            elif '购物中心/百货' not in detail_str and '层' not in detail_str:
                m_type = temp_list[0].strip().replace('类型：', '')
                floor = '未知'
                total_floor = '未知'
            elif '购物中心/百货' in detail_str and '层' not in detail_str:
                m_type = temp_list[0].replace('类型：', '') + temp_list[1]
                floor = '未知'
                total_floor = '未知'
            elif '购物中心/百货' in detail_str and '层' in detail_str:
                m_type = temp_list[0].replace('类型：', '') + temp_list[1]
                floor = temp_list[2]
                total_floor = temp_list[3].replace('层', '')
            else:
                logger.error('unexpective detail_str: ' + detail_str.strip())

            area = detail.select('div.area')[0].text.replace('㎡', '').replace('建筑面积', '')
            total_price = detail.select('div.moreInfo p.mt5 span.price')[0].text
            crawl_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

            item = dict()
            item['estate'] = estate
            item['floor'] = floor
            item['total_floor'] = total_floor
            item['type'] = m_type
            item['area'] = area
            item['total_price'] = total_price
            item['crawl_date'] = crawl_date

            item['city'] = response.request.meta['city']
            item['district'] = response.request.meta['district']
            item['url'] = response.request.url
            yield item

        next_page = soup.select('a#PageControl1_hlk_next')
        if len(next_page) > 0:
            url = response.nice_join(next_page[0]['href']) + '/'
            request = Request(url=url, priority=2, callback=self.process_page_2)
            request.meta['city'] = response.request.meta['city']
            request.meta['district'] = response.request.meta['district']
            yield request


# if __name__ == '__main__':
#     spider = SpiderCore(Fang_Shop_Processor()).set_pipeline(ConsolePipeline()).set_pipeline(
#             TextPipelineFangShop()).start()
