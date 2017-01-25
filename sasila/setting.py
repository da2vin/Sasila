#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
# PHANTOMJS_PATH = '/root/phantomjs/phantomjs'
PHANTOMJS_PATH = 'C:/Python27/phantomjs.exe'
# PHANTOMJS_SERVICE = [
#     '--proxy=localhost:8888',
#     '--proxy-type=http',
#     # '--proxy-auth=username:password'
# ]
PHANTOMJS_SERVICE = None
DRIVER_POOL_SIZE = 1
