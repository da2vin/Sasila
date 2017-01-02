#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Blueprint
from sasila.slow_system.manager.spider_manager import SpiderManager
import json

reload(sys)
sys.setdefaultencoding('utf-8')

slow_spider = Blueprint('slow_spider', __name__)

manager = SpiderManager()


@slow_spider.route('/all')
def get_all_spider():
    return json.dumps(manager.get_all_spider())


@slow_spider.route('/find')
def find_spider(spider_id):
    return json.dumps(manager.find_spider(spider_id))


@slow_spider.route('/start')
def start_spider(spider_id):
    return json.dumps(manager.start_spider(spider_id))


@slow_spider.route('/restart')
def restart_spider(spider_id):
    return json.dumps(manager.restart_spider(spider_id))


@slow_spider.route('/stop')
def stop_spider(spider_id):
    return json.dumps(manager.stop_spider(spider_id))


@slow_spider.route('/pause')
def pause_spider(spider_id):
    return json.dumps(manager.pause_spider(spider_id))


@slow_spider.route('/detail')
def get_spider_detail(spider_id):
    return json.dumps(manager.get_spider_detail(spider_id))


@slow_spider.route('/init')
def init_system():
    return json.dumps(manager.init_system())
