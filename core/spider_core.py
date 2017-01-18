#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from scheduler.url_scheduler import UrlScheduler
import gevent
import gevent.monkey

# gevent.monkey.patch_all()

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderCore(object):
    def __init__(self, spider_id):
        self._downloader = None
        self._processor = None
        self._scheduler = UrlScheduler(spider_id)  # type: UrlScheduler
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
        pass

    def start_by_request(self, request):
        self._scheduler.push(request)
        while True:
            temp_request = self._scheduler.poll()
            task = gevent.spawn(self.crawl, temp_request)
            task.join()

    def start_by_scheduler(self):
        pass
