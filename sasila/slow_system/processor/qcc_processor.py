#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.pic_pipeline import PicPipeline

from base_processor import BaseProcessor, Rule, LinkExtractor
from sasila.slow_system.downloader.http.spider_request import Request
from bs4 import BeautifulSoup as bs

reload(sys)
sys.setdefaultencoding('utf-8')


class QccProcessor(BaseProcessor):
    spider_id = 'qcc'
    spider_name = 'qcc'
    allowed_domains = ['qichacha.com']

    start_requests = [
        Request(url='http://www.qichacha.com/search?key=%E5%B0%8F%E9%A2%9D%E8%B4%B7%E6%AC%BE')]

    def process(self, response):
        soup = bs(response.m_response.content, "lxml")
        province_list = soup.select_one("dl#provinceOld").select("div.pull-left")[1].select("dd a")
        for province in province_list:
            province_name = province.string.strip()
            province_id = province["data-value"].strip()
            request = Request(
                    url="http://www.qichacha.com/search_getCityListHtml?province=" + province_id + "&q_type=1",
                    callback="get_city", priority=5)
            request.meta["province_name"] = province_name
            request.meta["province_id"] = province_id
            yield request

    def get_city(self, response):
        if response.m_response.content == "":
            request = Request(
                    url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&province=" +
                        response.request.meta["province_id"] + "&",
                    callback="get_all_page", priority=4)
            request.meta["city_name"] = ""
            request.meta["city_id"] = ""
            request.meta["province_name"] = response.request.meta["province_name"]
            request.meta["province_id"] = response.request.meta["province_id"]
            request.meta["only_province_sign"] = "0"
            yield request
        else:
            soup = bs(response.m_response.content, "lxml")
            city_list = soup.select("a")
            for city in city_list:
                city_name = city.string.strip()
                city_id = city["data-value"].strip()
                request = Request(
                        url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&province=" +
                            response.request.meta["province_id"] + "&city=" + city_id + "&",
                        callback="get_all_page", priority=4)
                request.meta["city_name"] = city_name
                request.meta["city_id"] = city_id
                request.meta["province_name"] = response.request.meta["province_name"]
                request.meta["province_id"] = response.request.meta["province_id"]
                yield request

    def get_all_page(self, response):
        soup = bs(response.m_response.content, "lxml")
        try:
            page = soup.find(lambda tag: tag.name == 'a' and '>' == tag.text).parent.findNextSibling().select_one("a")
            if page:
                total_page = int(page.string.strip().replace("...", ""))
            else:
                page = soup.find(
                    lambda tag: tag.name == 'a' and '>' == tag.text).parent.findPreviousSibling().select_one("a")
                if page:
                    total_page = int(page.string.strip().replace("...", ""))
                else:
                    total_page = 1
        except:
            total_page = 1

        now_page = 1
        while now_page <= total_page:
            if "only_province_sign" in response.request.meta.keys():
                request = Request(
                        url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&province=" +
                            response.request.meta["province_id"] + "&p=" + str(now_page) + "&",
                        callback="get_content", priority=3)
                request.meta["city_name"] = response.request.meta["city_name"]
                request.meta["city_id"] = response.request.meta["city_id"]
                request.meta["province_name"] = response.request.meta["province_name"]
                request.meta["province_id"] = response.request.meta["province_id"]
                yield request
            else:
                request = Request(
                        url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&&p=" + str(
                                now_page) + "&province=" +
                            response.request.meta["province_id"] + "&city=" + response.request.meta["city_id"] + "&",
                        callback="get_content", priority=3)
                request.meta["city_name"] = response.request.meta["city_name"]
                request.meta["city_id"] = response.request.meta["city_id"]
                request.meta["province_name"] = response.request.meta["province_name"]
                request.meta["province_id"] = response.request.meta["province_id"]
                yield request
            now_page += 1

    def get_content(self, response):
        pass
        # soup = bs(response.m_response.content, "lxml")
        # content_list = soup.select("table.m_srchList tbody tr")
        # for content in content_list:
        #     print content.select_one("a").text.strip()


qcc_spider = RequestSpider(QccProcessor()).set_pipeline(PicPipeline())
if __name__ == '__main__':
    qcc_spider.start()
