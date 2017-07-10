#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sasila.system_normal.pipeline.base_pipeline import ItemPipeline
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class ConsolePipeline(ItemPipeline):
    def process_item(self, item):
        print json.dumps(item).decode("unicode-escape")
