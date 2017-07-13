#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sasila.system_normal.manager.spider_manager import SpiderManager
import sys

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

manager = SpiderManager()
