#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderCore(object):
    def __init__(self):
        self.downloader = None
        self.processor = None
        self.scheduler = None
        self.pipline = None
        self.spider_name = None
        self.spider_id = None

    def set_spider_name(self, spider_name):
        self.spider_name = spider_name

    def set_spider_id(self, spider_id):
        self.spider_id = spider_id

    def create(self, processor):
        self.processor = processor
        return self

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler
        return self

    def set_downloader(self, downloader):
        self.downloader = downloader
        return self

    def set_pipline(self, pipline):
        self.pipline = pipline
