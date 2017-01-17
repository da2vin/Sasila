#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from manager.spider_manager import SpiderManager

app = Flask(__name__)
manager = SpiderManager()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/all')
def get_all_spider(self):
    pass


@app.route('/find')
def find_spider(self, spider_id):
    pass


@app.route('/start')
def start_spider(self, spider_id):
    pass


@app.route('/restart')
def restart_spider(self, spider_id):
    pass


@app.route('/stop')
def stop_spider(self, spider_id):
    pass


@app.route('/pause')
def pause_spider(self, spider_id):
    pass


@app.route('/detail')
def get_spider_detail(self, spider_id):
    pass


@app.route('/init')
def init_system(self):
    pass


if __name__ == '__main__':
    app.run()
