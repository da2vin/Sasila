#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import requests

from downloader.base_downloder import BaseDownLoader
from downloader.spider_response import Response

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    count = 0
    # proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}

    def download(self, request):
        response = Response(requests.get(request.url, verify=False).content, request)
        RequestsDownLoader.count += 1
        print RequestsDownLoader.count
        return response
