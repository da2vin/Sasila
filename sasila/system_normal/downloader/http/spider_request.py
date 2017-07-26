#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class Request(object):
    def __init__(self, url=None, data=None, json=None, headers=None, method="GET", cookies=None, meta=None,
                 callback=None,
                 errback=None, priority=0, allow_redirects=True, timeout=5, duplicate_remove=True):
        self.url = url
        self.data = data
        self.json = json
        self.headers = headers
        self.method = method
        self.allow_redirects = allow_redirects
        self.meta = {}
        self.cookies = cookies
        self.callback = callback
        self.priority = priority
        self.duplicate_remove = duplicate_remove
        self.timeout = timeout
        self.errback = errback

    def __str__(self):
        return "<Request [%s] [%s]>" % (self.method, self.url)

    __repr__ = __str__
