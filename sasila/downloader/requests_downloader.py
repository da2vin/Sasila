#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import requests
from sasila.downloader.spider_response import Response
from sasila.downloader.base_downloder import BaseDownLoader

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    count = 0

    # proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}

    def download(self, request):
        response = Response(requests.get(request.url, verify=False, timeout=5).content, request)
        RequestsDownLoader.count += 1
        print RequestsDownLoader.count, request.url
        return response
