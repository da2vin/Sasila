#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class BaseDownLoader(object):
    def __init__(self):
        self.loginer = None

    def download(self, request):
        pass

    def set_loginer(self, loginer):
        self.loginer = loginer
