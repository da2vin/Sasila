#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseProcessor(object):
    spider_id = None
    spider_name = None
    start_requests = []

    def process(self, response):
        raise NotImplementedError
