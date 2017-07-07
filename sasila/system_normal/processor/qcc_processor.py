#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.system_normal.pipeline.kafa_pipeline import KafkaPipeline
from sasila.system_normal.spider.request_spider import RequestSpider
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.text_pipeline import TextPipeline
from base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request
from bs4 import BeautifulSoup as bs
import time
from sasila.system_normal.utils import logger

import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


class QccProcessor(BaseProcessor):
    spider_id = 'qcc'
    spider_name = 'qcc'
    allowed_domains = ['qichacha.com']

    start_requests = [
        Request(url='http://www.qichacha.com/search?key=%E5%B0%8F%E9%A2%9D%E8%B4%B7%E6%AC%BE')
    ]

    def process(self, response):
        if not response.m_response:
            logger.error(response.request.url)
            yield response.request
        if '<script>window.location.href=' in response.m_response.content:
            logger.error(response.m_response.content + "\n" + response.request.url)
            yield response.request
        soup = bs(response.m_response.content, "lxml")
        province_list = soup.select_one("dl#provinceOld").select("div.pull-left")[1].select("dd a")
        for province in province_list:
            province_name = province.string.strip()
            province_id = province["data-value"].strip()
            request = Request(
                    url="http://www.qichacha.com/search_getCityListHtml?province=" + province_id + "&q_type=1",
                    callback="get_city", priority=0)
            request.meta["province_name"] = province_name
            request.meta["province_id"] = province_id
            yield request

    def get_city(self, response):
        if not response.m_response:
            logger.error(response.request.url)
            yield response.request
        if '<script>window.location.href=' in response.m_response.content:
            logger.error(response.m_response.content + "\n" + response.request.url)
            yield response.request
        if response.m_response.content == "":
            request = Request(
                    url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&province=" +
                        response.request.meta["province_id"] + "&",
                    callback="get_all_page", priority=1)
            request.meta["city_name"] = ""
            request.meta["city_id"] = ""
            request.meta["province_name"] = response.request.meta["province_name"]
            request.meta["province_id"] = response.request.meta["province_id"]
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
                        callback="get_all_page", priority=1)
                request.meta["city_name"] = city_name
                request.meta["city_id"] = city_id
                request.meta["province_name"] = response.request.meta["province_name"]
                request.meta["province_id"] = response.request.meta["province_id"]
                yield request

    def get_all_page(self, response):
        if not response.m_response:
            logger.error(response.request.url)
            yield response.request
        if '<script>window.location.href=' in response.m_response.content:
            logger.error(response.m_response.content + "\n" + response.request.url)
            yield response.request
        else:
            soup = bs(response.m_response.content, "lxml")
            try:
                temp_page = soup.find(lambda tag: tag.name == 'a' and '>' == tag.text).parent.findNextSibling()
                if temp_page:
                    page = temp_page.select_one("a")
                    if page:
                        total_page = int(page.string.strip().replace("...", ""))
                    else:
                        total_page = 1
                else:
                    temp_page = soup.find(lambda tag: tag.name == 'a' and '>' == tag.text).parent.findPreviousSibling()
                    if temp_page:
                        page = temp_page.select_one("a")
                        if page:
                            total_page = int(page.string.strip().replace("...", ""))
                        else:
                            total_page = 1
                    else:
                        total_page = 1
            except:
                total_page = 1

            now_page = 1
            while now_page <= total_page:
                if response.request.meta["city_id"] == "":
                    request = Request(
                            url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&province=" +
                                response.request.meta["province_id"] + "&p=" + str(now_page) + "&",
                            callback="get_content", priority=2)
                    request.meta["city_name"] = response.request.meta["city_name"]
                    request.meta["city_id"] = response.request.meta["city_id"]
                    request.meta["province_name"] = response.request.meta["province_name"]
                    request.meta["province_id"] = response.request.meta["province_id"]
                    yield request
                else:
                    request = Request(
                            url="http://www.qichacha.com/search_index?key=%25E5%25B0%258F%25E9%25A2%259D%25E8%25B4%25B7%25E6%25AC%25BE&ajaxflag=1&p=" + str(
                                    now_page) + "&province=" +
                                response.request.meta["province_id"] + "&city=" + response.request.meta[
                                    "city_id"] + "&",
                            callback="get_content", priority=2)
                    request.meta["city_name"] = response.request.meta["city_name"]
                    request.meta["city_id"] = response.request.meta["city_id"]
                    request.meta["province_name"] = response.request.meta["province_name"]
                    request.meta["province_id"] = response.request.meta["province_id"]
                    yield request
                now_page += 1

    def get_content(self, response):
        if not response.m_response:
            logger.error(response.request.url)
            yield response.request
        if '<script>window.location.href=' in response.m_response.content:
            logger.error(response.m_response.content + "\n" + response.request.url)
            yield response.request
        soup = bs(response.m_response.content, "lxml")
        content_list = soup.select("table.m_srchList tbody tr")
        for content in content_list:
            try:
                result_item = dict()
                result_item["province"] = response.request.meta["province_name"]
                result_item["city"] = response.request.meta["city_name"]
                result_item["company_name"] = content.select("td")[1].text.split('\n')[0].strip()
                result_item["company_man"] = content.select("td")[1].text.split('\n')[1].strip().replace("企业法人：", "")
                result_item["company_telephone"] = content.select("td")[1].text.split('\n')[2].strip().replace("联系方式：",
                                                                                                               "")
                result_item["company_address"] = content.select("td")[1].text.split('\n')[3].strip()
                if "地址：" in result_item["company_address"]:
                    result_item["company_address"] = result_item["company_address"].replace("地址：", "")
                else:
                    result_item["company_address"] = ""
                result_item["company_registered_capital"] = content.select("td")[2].text.strip()
                result_item["company_registered_time"] = content.select("td")[3].text.strip()
                result_item["company_status"] = content.select("td")[4].text.strip()
                result_item["source"] = "企查查"
                result_item["update_time"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                yield result_item
            except Exception:
                print traceback.format_exc()


qcc_spider = RequestSpider(QccProcessor(), time_sleep=1).set_pipeline(KafkaPipeline()).set_pipeline(
        TextPipeline()).set_pipeline(ConsolePipeline())
if __name__ == '__main__':
    qcc_spider.start()
