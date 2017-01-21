#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import gevent
import gevent.monkey

from downloader.requests_downloader import RequestsDownLoader
from downloader.spider_request import Request
from processor.base_processor import BaseProcessor
from scheduler.url_scheduler import UrlScheduler

gevent.monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderCore(object):
    def __init__(self, spider_id):
        self._downloader = RequestsDownLoader()  # type:RequestsDownLoader
        self._scheduler = UrlScheduler(spider_id)  # type: UrlScheduler
        self._processor = BaseProcessor(self._scheduler)  # type: BaseProcessor
        self._pipline = None
        self._spider_name = None
        self._spider_id = None
        self._spider_type = None
        self._spider_status = None

    def set_spider_name(self, spider_name):
        self._spider_name = spider_name
        return self

    def set_spider_id(self, spider_id):
        self._spider_id = spider_id
        return self

    def create(self, processor):
        self._processor = processor
        return self

    def set_scheduler(self, scheduler):
        self._scheduler = scheduler
        return self

    def set_downloader(self, downloader):
        self._downloader = downloader
        return self

    def set_pipline(self, pipline):
        self._pipline = pipline

    def get_status(self):
        return self._spider_status

    def init_component(self):
        pass

    def crawl(self, request):
        response = self._downloader.download(request)  # type:Response
        self._processor.process(response)

    def start_by_request(self, request):
        self._scheduler.push(request)
        for batch in self.batch_requests():
            if len(batch) > 0:
                gevent.joinall([gevent.spawn(self.crawl, r) for r in batch])
                # while True:
                #     temp_request = self._scheduler.poll()
                #     task = gevent.spawn(self.crawl, temp_request)
                #     task.join()

    def batch_requests(self):
        batch = []
        count = 0
        while True:
            count += 1
            if len(batch) > 99 or count > 99:
                yield batch
                batch = []
                count = 0
            temp_request = self._scheduler.poll()
            if temp_request:
                batch.append(temp_request)

    def start_by_scheduler(self):
        pass


if __name__ == '__main__':
    s = SpiderCore("test")
    s.start_by_request(Request("http://news.163.com/"))
