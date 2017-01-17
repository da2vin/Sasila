#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import scrapy

reload(sys)
sys.setdefaultencoding('utf-8')


class Request(object):
    def __init__(self):
        scrapy.Request()
        self.url = None
        self.headers = None
        self.method = None
        self.meta = None
        self.cookies = None
