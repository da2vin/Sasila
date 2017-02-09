#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from manager.spider_manager import SpiderManager
import json
import uuid
import redis
from sasila.manager.jd_manager import JdManager

app = Flask(__name__)
manager = SpiderManager()


class Token:
    def __init__(self):
        self.code = None
        self.msg = None
        self.accessTocken = None


jd_manager = JdManager()


@app.route('/im/jd/getcollecttoken')
def get_collect_token():
    return jd_manager.init_process(request.args['company_account'], request.args['name'],
                                   request.args['identity_card_number'], request.args['cell_phone_number'], 0)


@app.route('/im/jd/qr_login')
def qr_login():
    pic_str = jd_manager.process_qrlogin(request.args['collect_token'], request.args['account'])
    result = '<image src=\"data:image/png;base64,' + pic_str + '\">'
    return result


@app.route('/im/jd/submit_qrlogin')
def submit_qrlogin():
    return json.dumps(dict(jd_manager.submit_qrlogin(request.args['collect_token'])))


@app.route('/')
def hello_world():
    return 'Hello World1!'


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


# 业务相关流程，获取accessToken
@app.route('/getAccessTocken', methods=['POST'])
def getAccessTocken():
    accountId = request.form['accountId']

    # 进行相应的数据库查询，包括账号状态，账号的预存金额是否足够等信息
    accessTocken = str(uuid.uuid4())
    # 将accessTocken放入redis
    accessRedis = redis.StrictRedis()
    accessRedis.sadd(accessTocken, '')

    tocken = Token()
    tocken.code = '0000'
    tocken.msg = '成功'
    tocken.accessTocken = accessTocken

    tocken_dict = tocken.__dict__
    responseMsg = json.dumps(tocken_dict)
    return responseMsg.decode('unicode-escape')


# 获取用户名和密码
@app.route('/getUserInfo', methods=['POST'])
def getUserInfo():
    pass


if __name__ == '__main__':
    app.run()
