#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import requests
from sasila.downloader.spider_response import Response
from sasila.downloader.base_downloder import BaseDownLoader
from sasila.util import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    # proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}

    def __init__(self, loginer=None):
        self.loginer = loginer
        self._cookies = None

    def init_loginer(self, account, password):
        self._cookies = self.loginer.logint(account, password)

    def download(self, request):
        response = Response(requests.get(request.url, verify=False, timeout=5, cookies=self._cookies).content, request)
        logger.info('request download success:' + request.url)
        return response
