#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from sasila.slow_system.downloader.web_driver_pool import get_web_driver_pool
from selenium.webdriver.phantomjs.webdriver import WebDriver
from selenium.webdriver.common.action_chains import ActionChains
import time

reload(sys)
sys.setdefaultencoding('utf8')

pool = get_web_driver_pool(1)

web = pool.get()  # type:WebDriver

web.get(
    "http://store.nike.com/cn/zh_cn/pd/lunarepic-low-flyknit-2-%E7%94%B7%E5%AD%90%E8%B7%91%E6%AD%A5%E9%9E%8B/pid-11232563/pgid-11493486")

element = web.find_element_by_css_selector('div.exp-pdp-size-container a.nsg-form--drop-down--label')
element.click()

time.sleep(1)

web.save_screenshot('test.png')

element = web.find_elements_by_css_selector(
    'li.nsg-form--drop-down--option')[
    3]
ActionChains(web).move_to_element(element).perform()
web.save_screenshot('test.png')

ActionChains(web).click(element).perform()

time.sleep(1)

web.save_screenshot('test.png')

element = web.find_element_by_css_selector('button#buyingtools-add-to-cart-button')
element.click()

time.sleep(1)

web.save_screenshot('test76.png')
