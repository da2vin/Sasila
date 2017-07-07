#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.system_normal.spider.request_spider import RequestSpider

from base_processor import BaseProcessor, Rule, LinkExtractor
from sasila.system_normal.downloader.http.spider_request import Request
from bs4 import BeautifulSoup as bs

reload(sys)
sys.setdefaultencoding('utf-8')


class CityLocationProcessor(BaseProcessor):
    spider_id = 'city'
    spider_name = 'city'
    allowed_domains = ['supfree.net']
    start_requests = [Request(url='http://jingwei.supfree.net/')]

    rules = (
        Rule(LinkExtractor(regex_str=r"kongzi\.asp\?id=\d+"), priority=0),
        Rule(LinkExtractor(regex_str=r"mengzi\.asp\?id=\d+"), priority=1, only_first=True, callback='save'),
    )

    def save(self, response):
        if response.m_response:
            soup = bs(response.m_response.content, 'lxml')
            name = soup.select("div.cdiv p")[0].string.strip().split(' ')
            if len(name) > 2:
                province = name[0]
                city = name[1]
                area = name[2]
            elif len(name) > 1:
                province = name[0]
                city = name[0]
                area = name[1]
            else:
                province = name[0]
                city = name[0]
                area = name[0]
            lo = soup.select("div.cdiv p")[1].select("span")[0].string.strip()
            la = soup.select("div.cdiv p")[1].select("span")[1].string.strip()
            data = province + ',' + city + ',' + area + ',' + lo + ',' + la
            print data
            with open('city.txt', 'a+') as fs:
                data = province + ',' + city + ',' + area + ',' + lo + ',' + la
                fs.write(data + '\n')
                print data


fe_spider = RequestSpider(CityLocationProcessor())
if __name__ == '__main__':
    fe_spider.start()
