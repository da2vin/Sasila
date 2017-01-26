#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Response(object):
    def __init__(self, content=None
                 , request=None
                 , status_code=None
                 , headers=None
                 , raw=None
                 , url=None
                 , encoding=None
                 , history=None
                 , reason=None
                 , cookies=None
                 , text=None
                 , json=None
                 , links=None):
        self.text = text
        self.content = content
        self.request = request
        self.status_code = status_code
        self.headers = headers
        self.raw = raw
        self.url = url
        self.encoding = encoding
        self.history = history
        self.reason = reason
        self.cookies = cookies
        self.json = json
        self.links = links

    def __str__(self):
        return "<Response [%s] [%s]>" % (self.status_code,self.url)

    __repr__ = __str__
