#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest2 as unittest
from sasila.system_normal.processor.test_processor import TEST_Processor
from sasila.system_normal.spider.spider_core import SpiderCore
from sasila.system_normal.pipeline.console_pipeline import ConsolePipeline
from sasila.system_normal.pipeline.pic_pipeline import PicPipeline
from sasila.system_normal.pipeline.test_pipeline import TestPipeline


class TestProcessor(unittest.TestCase):
    def test_car_processor(self):
        test_pipeline = TestPipeline()
        SpiderCore(TEST_Processor(),test=True).set_pipeline(ConsolePipeline(),'console').set_pipeline(PicPipeline(),'save')\
            .set_pipeline(test_pipeline,'test').start()
        self.assertIn('2017',test_pipeline.result['date_time'])
