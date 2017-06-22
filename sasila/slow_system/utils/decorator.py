#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
from sasila.slow_system.utils import logger


def testResponse(func):
    @functools.wraps(func)
    def wrapper(self, response):
        if response.m_response is None:
            logger.error('response.m_response is None and url : ' + response.request.url)
        else:
            process = func(self, response)
            for callback in process:
                yield callback

    return wrapper
