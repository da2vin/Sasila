#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseProcessor(object):
    def __init__(self, scheduler):
        pass

    def process(self, request):
        pass


