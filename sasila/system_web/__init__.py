#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from flask import Flask
from sasila.system_normal.blueprints.slow_spiders import slow_spider

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

app.register_blueprint(slow_spider, url_prefix='/slow_spider')


@app.route('/')
def index():
    return 'welcome to sasila!'


def start():
    app.run(host='0.0.0.0', threaded=True)
