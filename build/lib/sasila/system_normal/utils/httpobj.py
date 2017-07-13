#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import weakref
# from six.moves.urllib.parse import urlparse
if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    from urlparse import urlparse
else:
    from urllib.parse import urlparse

_urlparse_cache = weakref.WeakKeyDictionary()


def urlparse_cached(request_or_response):
    if request_or_response not in _urlparse_cache:
        _urlparse_cache[request_or_response] = urlparse(request_or_response.url)
    return _urlparse_cache[request_or_response]
