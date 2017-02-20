#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


def formart_selenium_cookies(cookies):
    cookie_dict = dict()
    for c in cookies:
        cookie_dict[c['name']] = c['value']
    return json.dumps(cookie_dict).decode('unicode-escape')


def formart_requests_cookies(cookies):
    cookie_list = [{'name': c[0], 'value': c[1], 'path': '/', 'domain': '.jd.com'} for c in
                   dict(json.loads(cookies)).items()]
    return cookie_list
