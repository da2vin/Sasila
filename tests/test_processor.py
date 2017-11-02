#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest2 as unittest
from sasila.system_normal.processor.first_processor import FirstProcessor
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.test_pipeline import TestPipeline


class TestProcessor(unittest.TestCase):
    def test_car_processor(self):
        test_pipeline = TestPipeline()
        SpiderCore(FirstProcessor(), test=True).set_pipeline(ConsolePipeline()).set_pipeline(test_pipeline).start()
        self.assertIn('mzitu',test_pipeline.result['url'])
