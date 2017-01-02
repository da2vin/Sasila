#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from sasila.slow_system import settings
import Queue

reload(sys)
sys.setdefaultencoding('utf-8')

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 10
dcap["phantomjs.page.settings.loadImages"] = True
dcap["phantomjs.page.settings.userAgent"] = settings.USER_AGENT


def _get_base_ali_driver():
    if settings.PHANTOMJS_SERVICE:
        web = webdriver.PhantomJS(service_args=settings.PHANTOMJS_SERVICE, executable_path=settings.PHANTOMJS_PATH
                                  , desired_capabilities=dcap)
    else:
        web = webdriver.PhantomJS(executable_path=settings.PHANTOMJS_PATH
                                  , desired_capabilities=dcap)
    return web


def get_web_driver_pool(num):
    driver_queue = Queue.Queue()
    i = 0
    while i < num:
        web = _get_base_ali_driver()
        driver_queue.put(web)
        i += 1
    return driver_queue
