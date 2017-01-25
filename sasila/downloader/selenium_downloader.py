#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from sasila.downloader.base_downloder import BaseDownLoader
from sasila.downloader.web_driver_pool import get_web_driver_pool
from sasila import setting

reload(sys)
sys.setdefaultencoding('utf-8')


class SeleniumDownLoader(BaseDownLoader):
    def __init__(self):
        self.web_driver_pool = get_web_driver_pool(setting.DRIVER_POOL_SIZE)

    def download(self, requests):
        web = self.web_driver_pool.get()
        web.get(requests)
        return web.execute_script("return document.documentElement.outerHTML")
