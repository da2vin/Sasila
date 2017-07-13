#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

BASE_DIR = os.getcwd()

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'

PHANTOMJS_PATH = 'C:/Python27/phantomjs.exe'

# PHANTOMJS_SERVICE = [
#     '--proxy=localhost:8888',
#     '--proxy-type=http',
#     # '--proxy-auth=username:password'
# ]

PHANTOMJS_SERVICE = None

DRIVER_POOL_SIZE = 5

PROXY_PATH_REQUEST = os.path.join(BASE_DIR, 'proxy.txt')

REDIS_HOST = 'localhost'

REDIS_PORT = 6379

