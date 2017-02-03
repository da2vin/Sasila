#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from sasila import setting
from sasila.downloader.base_downloder import BaseDownLoader
from sasila.downloader.http.spider_response import Response
from sasila.downloader.web_driver_pool import get_web_driver_pool
from sasila.util import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class SeleniumDownLoader(BaseDownLoader):
    def __init__(self):
        logger.info("init web driver pool...")
        self.web_driver_pool = get_web_driver_pool(setting.DRIVER_POOL_SIZE)
        logger.info("init web driver pool success")
        Logger.info("happh nen year~")

    def download(self, request):
        web = self.web_driver_pool.get()  # type:WebDriver
        web.get(request.url)
        response = Response(content=web.execute_script("return document.documentElement.outerHTML"), request=request)
        self.web_driver_pool.put(web)
        logger.info("selenium download success:" + request.url)
        return response
