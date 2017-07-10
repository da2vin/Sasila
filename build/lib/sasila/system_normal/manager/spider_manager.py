#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
import threading

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderManager(object):
    def __init__(self):
        self.spider_list = dict()

    def set_spider(self, spider):
        self.spider_list[spider._spider_id] = spider

    def del_spider(self, spider_id):
        if spider_id in self.spider_list.keys():
            self.spider_list[spider_id].stop()
            del self.spider_list[spider_id]

    def init_system(self):
        pass

    def get_all_spider(self):
        return json.dumps(self.spider_list.keys())

    def find_spider(self, spider_id):
        pass

    def start_spider(self, spider_id):
        if self.spider_list[spider_id]._spider_status == "stopped":
            thread = threading.Thread(target=self.spider_list[spider_id].start)
            thread.setDaemon(True)
            thread.start()

    def restart_spider(self, spider_id):
        thread = threading.Thread(target=self.spider_list[spider_id].restart)
        thread.setDaemon(True)
        thread.start()

    def stop_spider(self, spider_id):
        self.spider_list[spider_id].stop()

    def get_spider_detail(self, spider_id):
        return str(self.spider_list[spider_id]._process_count)
