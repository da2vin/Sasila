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

    def create(self, processor):
        self.processor = processor
        return self

    def set_scheduler(self, scheduler):
        self.scheduler = scheduler
        return self

    def set_downloader(self, downloader):
        self.downloader = downloader
        return self
