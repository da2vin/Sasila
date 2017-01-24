#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from pipeline.base_pipeline import BasePipeline

reload(sys)
sys.setdefaultencoding('utf-8')


class ConsolePipeline(BasePipeline):
    def process_item(self, item):
        print item
