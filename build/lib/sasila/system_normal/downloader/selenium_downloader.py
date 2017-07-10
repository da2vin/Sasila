#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila.settings import default_settings
from sasila.system_normal.downloader.base_downloder import BaseDownLoader
from sasila.system_normal.downloader.http.spider_response import Response
from sasila.system_normal.downloader.web_driver_pool import get_web_driver_pool
from sasila.system_normal.utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class SeleniumDownLoader(BaseDownLoader):
    def __init__(self):
        logger.info("init web driver pool...")
        self.web_driver_pool = get_web_driver_pool(default_settings.DRIVER_POOL_SIZE)
        logger.info("init web driver pool success")

    def download(self, request):
        web = self.web_driver_pool.get()  # type:WebDriver
        web.get(request.url)
        response = Response(content=web.execute_script("return document.documentElement.outerHTML"), request=request)
        self.web_driver_pool.put(web)
        logger.info("selenium download success:" + request.url)
        return response
