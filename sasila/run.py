#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from manager.spider_manager import SpiderManager
import json
import uuid
import redis


app = Flask(__name__)
manager = SpiderManager()


class Tocken:
    def __init__(self):
        self.code = None
        self.msg = None
        self.accessTocken = None

@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/all')
def get_all_spider(self):
    return json.dumps(manager.get_all_spider())


@app.route('/find')
def find_spider(self, spider_id):
    return json.dumps(manager.find_spider(spider_id))


@app.route('/start')
def start_spider(self, spider_id):
    return json.dumps(manager.start_spider(spider_id))


@app.route('/restart')
def restart_spider(self, spider_id):
    return json.dumps(manager.restart_spider(spider_id))


@app.route('/stop')
def stop_spider(self, spider_id):
    return json.dumps(manager.stop_spider(spider_id))


@app.route('/pause')
def pause_spider(self, spider_id):
    return json.dumps(manager.pause_spider(spider_id))


@app.route('/detail')
def get_spider_detail(self, spider_id):
    return json.dumps(manager.get_spider_detail(spider_id))


@app.route('/init')
def init_system(self):
    return json.dumps(manager.init_system())


# 业务相关流程，获取accessToken
@app.route('/getAccessTocken',methods=['POST'])
def getAccessTocken():
    accountId = request.form['accountId']

    #进行相应的数据库查询，包括账号状态，账号的预存金额是否足够等信息
    accessTocken = str(uuid.uuid4())
    #将accessTocken放入redis
    accessRedis = redis.StrictRedis()
    accessRedis.sadd(accessTocken, '')

    tocken = Tocken()
    tocken.code=1321
    tocken.accessTocken = accessTocken
    #tocken_dict = json.dumps(tocken)

    tocken_dict = tocken.__dict__
    responseMsg = json.dumps(tocken_dict)
    return responseMsg.decode('unicode-escape')

# 获取用户名和密码
@app.route('/getUserInfo',methods=['POST'])
def getUserInfo():


if __name__ == '__main__':
    app.run()
