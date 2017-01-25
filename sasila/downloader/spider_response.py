#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Response(object):
    def __init__(self, content=None, request=None):
        self.content = content
        self.request = request
