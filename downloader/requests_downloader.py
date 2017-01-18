#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from downloader.base_downloder import BaseDownLoader
import requests
from core.spider_response import Response

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    count = 0

    def download(self, request):
        RequestsDownLoader.count += 1
        print RequestsDownLoader.count
        return Response(requests.get(request.url, verify=False).content, request)
