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
        response = None
        if request.method.upper() == "GET":
            response = requests.get(
                    url=request.url,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout
            )
        elif request.method.upper() == "POST":
            response = requests.post(
                    url=request.url,
                    data=request.data,
                    json=request.json,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout
            )
        else:
            pass

        response = Response(
                text=response.text,
                content=response.content,
                request=request,
                status_code=response.status_code,
                headers=response.headers,
                raw=response.raw,
                url=response.url,
                encoding=response.encoding,
                history=response.history,
                reason=response.reason,
                cookies=response.cookies,
                json=response.json,
                links=response.links
        )

        logger.info(response)
        return response


if __name__ == "__main__":
    proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}
    requests.post(url="http://www.jd.com", data={"123": "fdsgs"})
