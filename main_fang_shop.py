#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sasila.slow_system.processor.fang_shop_processor import Fang_Shop_Processor
from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.console_pipeline import ConsolePipeline
from sasila.slow_system.pipeline.text_pipeline import TextPipelineFangShop

if __name__ == '__main__':
    spider = RequestSpider(Fang_Shop_Processor()).set_pipeline(ConsolePipeline()).set_pipeline(
            TextPipelineFangShop()).start()
