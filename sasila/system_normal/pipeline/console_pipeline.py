#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sasila.system_normal.pipeline.base_pipeline import ItemPipeline
import json

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class ConsolePipeline(ItemPipeline):
    def process_item(self, item):
        if sys.version_info < (3, 0):
            print(json.dumps(item).decode("unicode-escape"))
        else:
            print(json.dumps(item).encode('utf8').decode("unicode-escape"))
