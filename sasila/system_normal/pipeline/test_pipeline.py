#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sasila.system_normal.pipeline.base_pipeline import ItemPipeline

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class TestPipeline(ItemPipeline):
    def __init__(self):
        self.result = {}

    def process_item(self, item):
        self.result = item
