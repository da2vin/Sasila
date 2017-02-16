#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
# from immediately_system.blueprints.jd import im_jd
from slow_system.blueprints.slow_spiders import slow_spider

app = Flask(__name__)
# app.register_blueprint(im_jd, url_prefix='/im/jd')
app.register_blueprint(slow_spider, url_prefix='/slow_spider')


@app.route('/')
def hello_world():
    return 'Hello World1!'


if __name__ == '__main__':
    app.run()
