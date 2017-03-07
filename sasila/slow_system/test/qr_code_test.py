#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import requests

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


dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.resourceTimeout"] = 10
dcap["phantomjs.page.settings.loadImages"] = True
dcap[
    "phantomjs.page.settings.userAgent"] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
web = webdriver.PhantomJS(executable_path='C:/Python27/phantomjs.exe'
                          , desired_capabilities=dcap)
#
# web.get("https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fhome.jd.com%2F")
# time.sleep(10)
# cookies = web.get_cookies()
# cookie_dict = dict()
# for c in cookies:
#     cookie_dict[c['name']] = c['value']
# web.save_screenshot('qrcode.png')

headers = dict()
headers[
    "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
headers["Accept"] = "*/*"
headers["Accept-Encoding"] = "gzip, deflate"
headers["Accept-Language"] = "zh-CN,en,*"
headers["Referer"] = "https://passport.jd.com/new/login.aspx?ReturnUrl=http%3A%2F%2Fhome.jd.com%2F"
session = requests.Session()

response = session.get("https://qr.m.jd.com/show?appid=133&size=147&t=1486614526653")
with open("qrcode.png", 'wb') as fs:
    fs.write(response.content)

response = session.get("https://qr.m.jd.com/check?callback=jQuery6172296&appid=133&_=1486609849337",
                       headers=headers)

ticket = abstract(response.content, '\"ticket\" : \"', '\"')
print ticket

headers['X-Requested-With'] = 'XMLHttpRequest'
response = session.get("https://passport.jd.com/uc/qrCodeTicketValidation?t=" + ticket, headers=headers)

cookie_dict = session.cookies.get_dict()

cookie_list = [{'name': c[0], 'value': c[1], 'path': '/', 'domain': '.jd.com'} for c in cookie_dict.items()]

for c in cookie_list:
    web.add_cookie(c)

web.get('https://home.jd.com')

web.save_screenshot('test8.png')
print response.headers
print response.content
