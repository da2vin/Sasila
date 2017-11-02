#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class pipeItem(object):
    def __init__(self, pipenames=[], result=None):
        self.pipenames = pipenames
        self.result = result
