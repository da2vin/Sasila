#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import grequests
import requests
from requests.adapters import HTTPAdapter
from sasila.slow_system.downloader.base_downloder import BaseDownLoader
from sasila.slow_system.downloader.http.spider_response import Response

from sasila.slow_system.utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')


class RequestsDownLoader(BaseDownLoader):
    # proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}

    def __init__(self, loginer=None):
        self.loginer = loginer
        self._cookies = None

        self._headers = dict()
        self._headers[
            "User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36"
        self._headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        self._headers["Accept-Encoding"] = "gzip, deflate, sdch"
        self._headers["Accept-Language"] = "zh-CN,zh;q=0.8"
        self._request_retry = HTTPAdapter(max_retries=3)

    def init_loginer(self, account, password):
        self._cookies = self.loginer.logint(account, password)

    def download(self, batch):
        batch_requests = []

        for request in batch:
            session = requests.session()
            session.mount('https://', self._request_retry)
            session.mount('http://', self._request_retry)

            if not request.headers:
                request.headers = self._headers
                session.headers = self._headers

            if request.method.upper() == "GET":
                batch_requests.append(grequests.get(
                        session=session,
                        url=request.url,
                        headers=request.headers,
                        cookies=self._cookies,
                        verify=False,
                        allow_redirects=request.allow_redirects,
                        timeout=request.timeout
                ))
            elif request.method.upper() == "POST":
                batch_requests.append(grequests.post(
                        session=session,
                        url=request.url,
                        data=request.data,
                        json=request.json,
                        headers=request.headers,
                        cookies=self._cookies,
                        verify=False,
                        allow_redirects=request.allow_redirects,
                        timeout=request.timeout
                ))
            else:
                pass

        rets = grequests.map(batch_requests, exception_handler=exception_handler)

        true_responses = []
        index = 0
        for ret in rets:
            true_response = Response(
                    m_response=ret,
                    request=batch[index],
            )
            true_responses.append(true_response)
            logger.info(true_response)
            index += 1

        return true_responses


def exception_handler(request, exception):
    logger.error("%s %s" % (request.url, exception))

if __name__ == "__main__":
    proxies = {"http": "http://127.0.0.1:8888", "https": "http://127.0.0.1:8888",}
    requests.post(url="http://www.jd.com", data={"123": "fdsgs"})
