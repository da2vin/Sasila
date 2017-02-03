#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from manager.spider_manager import SpiderManager
import json

app = Flask(__name__)
manager = SpiderManager()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/all')
def get_all_spider():
    return json.dumps(manager.get_all_spider())


@app.route('/find')
def find_spider(spider_id):
    return json.dumps(manager.find_spider(spider_id))


@app.route('/start')
def start_spider(spider_id):
    return json.dumps(manager.start_spider(spider_id))


@app.route('/restart')
def restart_spider(spider_id):
    return json.dumps(manager.restart_spider(spider_id))


@app.route('/stop')
def stop_spider(spider_id):
    return json.dumps(manager.stop_spider(spider_id))


@app.route('/pause')
def pause_spider(spider_id):
    return json.dumps(manager.pause_spider(spider_id))


@app.route('/detail')
def get_spider_detail(spider_id):
    return json.dumps(manager.get_spider_detail(spider_id))


@app.route('/init')
def init_system():
    return json.dumps(manager.init_system())


if __name__ == '__main__':
    app.run()
