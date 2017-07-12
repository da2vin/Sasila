#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
# import os
#
# sys.path.append(os.path.dirname(os.getcwd()))
from car_processor import Car_Processor
from fang_processor import Fang_Processor
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.manager import manager
from sasila import system_web

spider_car = SpiderCore(Car_Processor()).set_pipeline(ConsolePipeline())
spider_fang = SpiderCore(Fang_Processor()).set_pipeline(ConsolePipeline())
manager.set_spider(spider_car)
manager.set_spider(spider_fang)
system_web.start()
