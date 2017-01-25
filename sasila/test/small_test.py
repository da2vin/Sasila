#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re

reload(sys)
sys.setdefaultencoding('utf-8')


def test(cls):
    def _test():
        clsName = re.findall('(\w+)', repr(cls))[-1]
        print 'Call %s.__init().' % clsName
        return cls()

    return _test


@test
class sy(object):
    value = 32


def extract_by_css(css_expression):
    def _extract_by_css(processor):
        def __extract_by_css():
            return 1
        return css_expression
    return _extract_by_css


class Processor(object):
    @extract_by_css('123')
    @property
    def title(self):
        return self


p = Processor()
print p.title
