#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest2 as unittest
from sasila.system_normal.processor.car_processor import Car_Processor
from sasila.system_normal.spider.request_spider import RequestSpider
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.test_pipeline import TestPipeline


class TestProcessor(unittest.TestCase):
    def test_car_processor(self):
        test_pipeline = TestPipeline()
        RequestSpider(Car_Processor(), test=True).set_pipeline(ConsolePipeline()).set_pipeline(test_pipeline).start()
        self.assertEqual(test_pipeline.result['province'], '上海', '爬取结果，省份为上海')
