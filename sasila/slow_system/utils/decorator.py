#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from sasila.slow_system.utils import logger


def testResponse(func):
    @functools.wraps(func)
    def wrapper(self, response):
        if response.m_response is None:
            yield response.request
            logger.error('response.m_response is None and url : ' + response.request.url + ' and request has been push to queue again!')
        else:
            process = func(self, response)
            if process is not None:
                for callback in process:
                    yield callback

    return wrapper
