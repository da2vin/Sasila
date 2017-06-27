#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from sasila.slow_system.utils import logger
import traceback
import time
import time


def testResponse(func):
    @functools.wraps(func)
    def wrapper(self, response):
        if response.m_response is None:
            yield response.request
            logger.error(
                    'response.m_response is None and url : ' + response.request.url + ' and request has been push to queue again!')
        else:
            process = func(self, response)
            if process is not None:
                try:
                    for callback in process:
                        yield callback
                except Exception:
                    logger.error(
                            'process error: ' + response.request.url + '\r\n' + response.m_response.content + '\r\n' + traceback.format_exc())

    return wrapper


def timeit(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.clock()
        ret = func(*args, **kwargs)
        logger.info(func.__name__ + ' run time: ' + '{:.9f}'.format(time.clock() - start))
        return ret

    return wrapper
