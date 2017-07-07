#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import weakref
# from six.moves.urllib.parse import urlparse
from urlparse import urlparse

reload(sys)
sys.setdefaultencoding('utf-8')

_urlparse_cache = weakref.WeakKeyDictionary()


def urlparse_cached(request_or_response):
    if request_or_response not in _urlparse_cache:
        _urlparse_cache[request_or_response] = urlparse(request_or_response.url)
    return _urlparse_cache[request_or_response]
