#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import six
from sasila.system_normal.downloader.http.spider_request import Request
from sasila.system_normal.utils.python import to_unicode, to_native_str

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def request_to_dict(request, processor=None):
    """Convert Request object to a dict.

    If a spider is given, it will try to find out the name of the spider method
    used in the callback and store that as the callback.
    """
    cb = request.callback
    if callable(cb):
        cb = _find_method(processor, cb)
    eb = request.errback
    if callable(eb):
        eb = _find_method(processor, eb)
    d = {
        'url': to_unicode(request.url),  # urls should be safe (safe_string_url)
        'callback': cb,
        'errback': eb,
        'data': request.data,
        'json': request.json,
        'allow_redirects': request.allow_redirects,
        'duplicate_remove': request.duplicate_remove,
        'timeout': request.timeout,
        'method': request.method,
        'headers': request.headers,
        'cookies': request.cookies,
        'meta': request.meta,
        'priority': request.priority,
    }
    return d


def request_from_dict(d, processor=None):
    """Create Request object from a dict.

    If a spider is given, it will try to resolve the callbacks looking at the
    spider for methods with the same name.
    """
    cb = d['callback']
    if cb and processor:
        cb = _get_method(processor, cb)
    eb = d['errback']
    if eb and processor:
        eb = _get_method(processor, eb)
    return Request(
            url=to_native_str(d['url']),
            data=d['data'],
            json=d['json'],
            allow_redirects=d['allow_redirects'],
            duplicate_remove=d['duplicate_remove'],
            timeout=d['timeout'],
            callback=cb,
            errback=eb,
            method=d['method'],
            headers=d['headers'],
            cookies=d['cookies'],
            meta=d['meta'],
            priority=d['priority'], )


def _find_method(obj, func):
    if obj:
        try:
            func_self = six.get_method_self(func)
        except AttributeError:  # func has no __self__
            pass
        else:
            if func_self is obj:
                return six.get_method_function(func).__name__
    raise ValueError("Function %s is not a method of: %s" % (func, obj))


def _get_method(obj, name):
    name = str(name)
    try:
        return getattr(obj, name)
    except AttributeError:
        raise ValueError("Method %r not found in: %s" % (name, obj))
