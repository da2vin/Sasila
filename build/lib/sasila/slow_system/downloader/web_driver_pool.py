#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import sys

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from sasila.settings import default_settings

reload(sys)
sys.setdefaultencoding('utf-8')

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 10
dcap["phantomjs.page.settings.loadImages"] = True
dcap["phantomjs.page.settings.userAgent"] = default_settings.USER_AGENT


def _get_base_ali_driver():
    if default_settings.PHANTOMJS_SERVICE:
        web = webdriver.PhantomJS(service_args=default_settings.PHANTOMJS_SERVICE, executable_path=default_settings.PHANTOMJS_PATH
                                  , desired_capabilities=dcap)
    else:
        web = webdriver.PhantomJS(executable_path=default_settings.PHANTOMJS_PATH
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
