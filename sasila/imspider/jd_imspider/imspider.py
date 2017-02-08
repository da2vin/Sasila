#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import requests
from sasila.downloader.web_driver_pool import get_web_driver_pool
from Queue import Queue
from selenium import webdriver
from sasila.utils import logger
import pickle
import time

reload(sys)
sys.setdefaultencoding('utf-8')


class JdImSpider(object):
    def __init__(self):
        self.web_driver_pool = None  # type:  Queue

    def init_pool(self):
        logger.info('init web driver pool...')
        self.web_driver_pool = get_web_driver_pool(1)
        logger.info('init web driver pool success...')

    def login(self, account, password, cookie):
        web = self.web_driver_pool.get()  # type: webdriver.PhantomJS
        web.delete_all_cookies()
        if self._validate_login(cookie, web):
            web.get("https://passport.jd.com/new/login.aspx")
            element = web.find_element_by_css_selector("div.login-tab.login-tab-r").find_element_by_css_selector("a")
            element.click()
            element = web.find_element_by_id("loginname")
            element.clear()
            element.send_keys(account)
            element = web.find_element_by_id("nloginpwd")
            element.clear()
            element.send_keys(password)
            element = web.find_element_by_css_selector("a#loginsubmit")
            element.click()
            time.sleep(5)

            cookie = web.get_cookies()
        self.web_driver_pool.put(web)
        return pickle.dumps(cookie)

    def _validate_login(self, cookie, web):
        if not cookie:
            return True
        cookies = pickle.loads(cookie)
        for c in cookies:
            web.add_cookie({k: c[k] for k in ('name', 'value', 'domain', 'path', 'expiry') if k in c})
        web.get("https://home.jd.com/")
        web.save_screenshot("test.png")
        return True
