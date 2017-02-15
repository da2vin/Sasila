#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
from sasila.slow_system.processor.mzitu_proccessor import mzitu_spider
from multiprocessing.process import Process
import threading

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderManager(object):
    def __init__(self):
        self.spider_list = dict()
        self.spider_list[mzitu_spider._spider_id] = mzitu_spider

    def init_system(self):
        pass

    def get_all_spider(self):
        return json.dumps(self.spider_list.keys())

    def find_spider(self, spider_id):
        pass

    def start_spider(self, spider_id):
        # Process(target=self.spider_list[spider_id].start).start()
        threading.Thread(target=self.spider_list[spider_id].start).start()

    def restart_spider(self, spider_id):
        pass

    def stop_spider(self, spider_id):
        self.spider_list[spider_id].stop()

    def pause_spider(self, spider_id):
        self.spider_list[spider_id].pause()

    def continue_spider(self, spider_id):
        self.spider_list[spider_id].conti()

    def get_spider_detail(self, spider_id):
        return str(self.spider_list[spider_id]._process_count)
