#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import time
import requests
from bs4 import BeautifulSoup as bs
from sasila.slow_system.downloader.web_driver_pool import get_web_driver_pool
from sasila.slow_system.utils.cookie import formart_selenium_cookies
from sasila.slow_system.utils import logger
from sasila.slow_system.utils import jd_code

reload(sys)
sys.setdefaultencoding('utf-8')


def abstract(text, start, end):
    if text is None or text == '':
        return ''
    res = ''
    if start is not None and start != '':
        if start not in text:
            return res
        else:
            text = text[text.index(start) + len(start):]
    if end is not None and end != '':
        if end not in text:
            return res
        else:
            res = text[0:text.index(end)]
    else:
        res = text
    return res


class JdMessage(object):
    def __init__(self):
        self.code = ""
        self.code_description = ""
        self.cookies = ""
        self.qr_captcha = ""


class JdRequest(object):
    def __init__(self):
        self.web_driver_pool = None  # type:  Queue

    def init_pool(self):
        logger.info('init web driver pool...')
        self.web_driver_pool = get_web_driver_pool(1)
        logger.info('init web driver pool success...')

    def login(self, account, password):
        message = JdMessage()

        web = self.web_driver_pool.get()  # type: webdriver.PhantomJS
        web.delete_all_cookies()

        web.get("https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fhome.jd.com%2F")
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
        time.sleep(3)

        if '我的京东' in bs(web.execute_script("return document.documentElement.outerHTML"), 'lxml').title.string:
            message.code = jd_code.SUCCESS
            message.code_description = "登录成功"
            message.cookies = formart_selenium_cookies(web.get_cookies())
        else:
            # 需要手机验证码等等状况
            pass

        self.web_driver_pool.put(web)
        return message

    def qr_login(self):
        message = JdMessage()
        headers = dict()
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        headers["Accept"] = "*/*"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Accept-Language"] = "zh-CN,en,*"
        headers["Referer"] = "https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fhome.jd.com%2F"
        session = requests.Session()
        response = session.get("https://qr.m.jd.com/show?appid=133&size=147&t=" + str(time.time()))

        message.code = jd_code.SUCCESS
        message.qr_captcha = response.content.encode("base64")
        message.cookies = json.dumps(session.cookies.get_dict()).decode("unicode-escape")
        return message

    def submit_qrlogin(self, cookies):
        message = JdMessage()

        headers = dict()
        headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        headers["Accept"] = "*/*"
        headers["Accept-Encoding"] = "gzip, deflate"
        headers["Accept-Language"] = "zh-CN,en,*"
        headers["Referer"] = "https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fhome.jd.com%2F"
        session = requests.Session()

        response = session.get("https://qr.m.jd.com/check?callback=jQuery6172296&appid=133&_=1486609849337",
                               cookies=json.loads(cookies),
                               headers=headers)

        ticket = abstract(response.content, '\"ticket\" : \"', '\"')

        headers['X-Requested-With'] = 'XMLHttpRequest'
        response = session.get("https://passport.jd.com/uc/qrCodeTicketValidation?t=" + ticket, headers=headers)

        message.code = jd_code.SUCCESS
        message.code_description = "登录成功"
        message.cookies = json.dumps(session.cookies.get_dict()).decode("unicode-escape")

        return message
