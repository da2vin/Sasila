#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from posixpath import normpath
from urlparse import urljoin
from urlparse import urlparse
from urlparse import urlunparse

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseProcessor(object):
    def _nice_join(self, base, url):
        url1 = urljoin(base, url)
        arr = urlparse(url1)
        path = normpath(arr[2])
        return urlunparse((arr.scheme, arr.netloc, path, arr.params, arr.query, arr.fragment))

    def _is_url(self, url):
        if re.match(r'^https?:/{2}\w.+$', url):
            return True
        else:
            return False

    spider_id = None
    spider_name = None
    start_requests = []

    def process(self, response):
        raise NotImplementedError
