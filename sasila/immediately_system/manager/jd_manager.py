#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json
from sasila.immediately_system.crawler.jd.request import JdRequest
from sasila.immediately_system.database.jd_database import *

reload(sys)
sys.setdefaultencoding('utf-8')


class JdResponse(object):
    def __init__(self, code, code_description):
        self.code = code
        self.code_description = code_description


class JdManager(object):
    def __init__(self):
        self.database = JdDatabase()
        self.request = JdRequest()
        self.request.init_pool()

    def login(self, collect_token, account, password):
        session = self.database.create_session()

        message = self.request.login(account, password)
        if message.code == 0:
            session.query(Process).filter(Process.collect_token == collect_token).update({
                Process.cookies: message.cookies
            })

        return json.dumps(JdResponse(code=message.code, code_description=message.code_description).__dict__).decode(
                'unicode-escape')

    def qrlogin(self, collect_token, account):
        session = self.database.create_session()
        process = session.query(Process).filter(Process.collect_token == collect_token).first()
        if process:
            if datetime.datetime.now() > process.expire_time:
                # collect_token 过期
                pass
            else:
                message = self.request.qr_login()
                session.query(Process).filter(Process.collect_token == collect_token).update({
                    Process.account: account,
                    Process.process_cookie: json.dumps(message.qr_cookies).decode('unicode-escape')
                })
                return message.qr_captcha.encode('base64')
        else:
            # 没有申请collect_token
            return 'collect_token 无效'

    def submit_qrlogin(self, collect_token):
        session = self.database.create_session()
        process = session.query(Process).filter(Process.collect_token == collect_token).first()
        if process:
            if datetime.datetime.now() > process.expire_time:
                # collect_token 过期
                pass
            else:
                message = self.request.submit_qrlogin(process.process_cookie)
                # session.query(Process).filter(Process.collect_token == collect_token).update({
                #     Process.account: account,
                #     Process.process_cookie: json.dumps(message.qr_cookies).decode('unicode-escape')
                # })
                return message
        else:
            # 没有申请collect_token
            return 'collect_token 无效'
