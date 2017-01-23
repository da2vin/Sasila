#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseProcessor(object):
    def __init__(self, scheduler):
        self._spider_name = None
        self._spider_id = None
        self._spider_type = None

    def process(self, request):
        pass


