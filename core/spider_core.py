#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderCore(object):
    def __init__(self):
        self._downloader = None
        self._processor = None
        self._scheduler = None
        self._pipline = None
        self._spider_name = None
        self._spider_id = None

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
