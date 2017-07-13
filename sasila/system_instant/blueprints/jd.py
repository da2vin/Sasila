#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json
from flask import Blueprint
from flask import request
from sasila.system_instant.manager.jd_manager import JdManager

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

im_jd = Blueprint('im_jd', __name__)

jd_manager = JdManager()


@im_jd.route('/login')
def login():
    return jd_manager.login(request.args['collect_token'], request.args['account'], request.args['password'])


@im_jd.route('/qrlogin')
def qr_login():
    message = jd_manager.qrlogin(request.args['collect_token'])
    # result = '<image src=\"data:image/png;base64,' + json.loads(message, strict=False)["qr_captcha"] + '\"><br>' + message
    # return result
    return message


@im_jd.route('/submit_qrlogin')
def submit_qrlogin():
    return jd_manager.submit_qrlogin(request.args['collect_token'])
