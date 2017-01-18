#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from bloom_filter import BloomFilter

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseScheduler(object):
    def __init__(self):
        self.filter = BloomFilter()

    def push(self, request):
        pass

    def poll(self):
        pass
