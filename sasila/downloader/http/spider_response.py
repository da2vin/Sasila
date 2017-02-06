#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Response(object):
    def __init__(self, m_response=None, request=None):
        self.request = request
        self.m_response = m_response

    def __str__(self):
        return "<Response [%s] [%s] [%.2f KB]>" % (self.m_response.status_code, self.m_response.url, (float(len(self.m_response.content)) / 1000))

    __repr__ = __str__
