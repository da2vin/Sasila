#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseDownLoader(object):
    def __init__(self):
        self.loginer = None

    def download(self, request):
        pass

    def set_loginer(self, loginer):
        self.loginer = loginer
