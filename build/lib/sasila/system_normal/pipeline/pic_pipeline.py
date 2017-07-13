#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import uuid
from sasila.system_normal.pipeline.base_pipeline import ItemPipeline

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class PicPipeline(ItemPipeline):
    def process_item(self, item):
        if item is not None:
            if not os.path.exists("img"):
                os.mkdir("img")
            with open("img/" + str(uuid.uuid1()) + ".jpg", 'wb') as fs:
                fs.write(item)
                print("download success!")
