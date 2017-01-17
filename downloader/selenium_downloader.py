#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from downloader.base_downloder import BaseDownLoader
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')


class SeleniumDownLoader(BaseDownLoader):
    def download(self, requests):
        web = webdriver.PhantomJS()
        web.get(requests)
        return web.execute_script("return document.documentElement.outerHTML")
