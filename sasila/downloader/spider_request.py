#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Request(object):
    def __init__(self, url=None, headers=None, method=None, cookies=None, meta={}, callback=None, priority=0,
                 duplicate_remove=True):
        self.url = url
        self.headers = headers
        self.method = method
        self.meta = meta
        self.cookies = cookies
        self.callback = callback
        self.priority = priority
        self.duplicate_remove = duplicate_remove
