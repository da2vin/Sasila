#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from core.spider_core import SpiderCore
from processor.base_processor import BaseProcessor

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseSpider(BaseProcessor):
    def __init__(self):
        pass

    def crawl(self):
        pass
