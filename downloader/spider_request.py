#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import scrapy

reload(sys)
sys.setdefaultencoding('utf-8')


class Request(object):
    def __init__(self, url=None, headers=None, method=None, cookies=None, meta=None):
        self.url = url
        self.headers = headers
        self.method = method
        self.meta = meta
        self.cookies = cookies
