#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from downloader.base_downloder import BaseDownLoader
from selenium import webdriver

reload(sys)
sys.setdefaultencoding('utf-8')


class SeleniumDownLoader(BaseDownLoader):
    def download(self, url):
        web = webdriver.PhantomJS()
        web.get(url)
        return web.execute_script("return document.documentElement.outerHTML")
