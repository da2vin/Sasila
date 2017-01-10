#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

from downloader.base_downloder import BaseDownLoader
import requests

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    def download(self, url):
        return requests.get(url).content
