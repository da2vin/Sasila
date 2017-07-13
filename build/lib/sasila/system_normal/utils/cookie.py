#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import json

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def formart_selenium_cookies(cookies):
    cookie_dict = dict()
    for c in cookies:
        cookie_dict[c['name']] = c['value']
    return json.dumps(cookie_dict).decode('unicode-escape')


def selenium_add_cookies(cookies, web):
    cookie_list = [{'name': c[0], 'value': c[1], 'path': '/', 'domain': '.jd.com', 'expiry': 4070880000} for c in
                   dict(json.loads(cookies)).items()]
    for c in cookie_list:
        web.add_cookie(c)
