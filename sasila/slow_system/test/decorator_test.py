#!/usr/bin/env python
# -*- coding: utf-8 -*-


import functools


def testResponse(func):
    @functools.wraps(func)
    def wrapper(self, response):
        if response is None:
            print 'response is None'
        elif response.m_response is None:
            print 'response.m_response is None'
        else:
            process = func(self, response)
            for callback in process:
                yield callback
    return wrapper


@testResponse
def test(a, b):
    for i in range(10):
        yield i


for item in test(1, None):
    print item
