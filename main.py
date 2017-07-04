#!/usr/bin/env python
# -*- coding: utf-8 -*-
from car_processor import Car_Processor
from fang_processor import Fang_Processor
from sasila.slow_system.pipeline.console_pipeline import ConsolePipeline
from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.manager import manager
import sasila

spider_car = RequestSpider(Car_Processor()).set_pipeline(ConsolePipeline())
spider_fang = RequestSpider(Fang_Processor()).set_pipeline(ConsolePipeline())
manager.set_spider(spider_car)
manager.set_spider(spider_fang)
sasila.start()