#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import requests
from requests.adapters import HTTPAdapter

from sasila.downloader.base_downloder import BaseDownLoader
from sasila.downloader.http.spider_response import Response
from sasila.utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    # proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}

    def __init__(self, loginer=None):
        self.loginer = loginer
        self._cookies = None

        self._headers = dict()
        self._headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        self._headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        self._headers["Accept-Encoding"] = "gzip, deflate, sdch"
        self._headers["Accept-Language"] = "zh-CN,zh;q=0.8"
        self._request_retry = HTTPAdapter(max_retries=3)

    def init_loginer(self, account, password):
        self._cookies = self.loginer.logint(account, password)

    def download(self, request):
        session = requests.session()
        session.mount('https://', self._request_retry)
        session.mount('http://', self._request_retry)
        response = None

        if not request.headers:
            request.headers = self._headers
            session.headers = self._headers

        if request.method.upper() == "GET":
            response = session.get(
                    url=request.url,
                    headers=request.headers,
                    cookies=self._cookies,
                    verify=False,
                    allow_redirects=request.allow_redirects,
                    timeout=request.timeout
            )
        elif request.method.upper() == "POST":
            response = session.post(
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
