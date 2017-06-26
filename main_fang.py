#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sasila.slow_system.processor.fang_processor import Fang_Processor
from sasila.slow_system.core.request_spider import RequestSpider
from sasila.slow_system.pipeline.console_pipeline import ConsolePipeline
from sasila.slow_system.pipeline.text_pipeline import TextPipelineFang

if __name__ == '__main__':
    spider = RequestSpider(Fang_Processor()).set_pipeline(ConsolePipeline()).set_pipeline(
            TextPipelineFang()).start()
