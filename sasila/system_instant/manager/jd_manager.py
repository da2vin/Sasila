#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from sasila.system_normal.utils import jd_code
import json
from sasila.system_instant.crawler.jd.request import JdRequest
from sasila.system_instant.database.jd_database import *

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


class JdResponse(object):
    def __init__(self, code, code_description, qr_captcha=None):
        self.code = code
        self.code_description = code_description
        self.qr_captcha = qr_captcha


class JdManager(object):
    def __init__(self):
        self.database = JdDatabase()
        self.request = JdRequest()
        self.request.init_pool()

    def login(self, collect_token, account, password):
        message = self.request.login(account, password)
        if message.code == jd_code.SUCCESS:
            self.database.update_cookie(collect_token, message.cookies)
        return json.dumps(JdResponse(code=message.code, code_description=message.code_description).__dict__).decode(
                'unicode-escape')

    def qrlogin(self, collect_token):
        message = self.request.qr_login()
        if message.code == jd_code.SUCCESS:
            self.database.update_cookie(collect_token, message.cookies)
        return json.dumps(JdResponse(code=message.code, code_description=message.code_description,
                                     qr_captcha=message.qr_captcha).__dict__).decode(
                'unicode-escape')

    def submit_qrlogin(self, collect_token):
        cookies = self.database.query_cookie(collect_token)
        message = self.request.submit_qrlogin(cookies)
        if message.code == jd_code.SUCCESS:
            self.database.update_cookie(collect_token, message.cookies)
        return json.dumps(JdResponse(code=message.code, code_description=message.code_description).__dict__).decode(
                'unicode-escape')
