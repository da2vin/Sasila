#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderCore(object):
    def __init__(self):
        self.downloader = None

    def set_downloader(self, downloader):
        self.downloader = downloader
        return self
