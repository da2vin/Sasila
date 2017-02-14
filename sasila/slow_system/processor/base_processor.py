#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from sasila.slow_system.downloader.http.spider_request import Request

reload(sys)
sys.setdefaultencoding('utf-8')


def identity(x):
    return x


class Rule(object):
    def __init__(self, link_extractor, callback=None, process_request=identity, priority=0):
        self.link_extractor = link_extractor
        self.callback = callback
        self.process_request = process_request
        self.priority = priority


class LinkExtractor(object):
    def __init__(self, regex_str=None):
        self.regex = re.compile(regex_str)

    def extract_links(self, response):
        return [response.nice_join(link) for link in self.regex.findall(response.m_response.content)]


class BaseProcessor(object):
    spider_id = None
    spider_name = None
    start_requests = []
    rules = ()
    allowed_domains = []

    def process(self, response):
        if hasattr(self, 'rules'):
            rules = getattr(self, 'rules', None)
        else:
            rules = ()
        for rule in rules:
            links = rule.link_extractor.extract_links(response)
            for link in links:
                request = Request(url=link, callback=rule.callback, priority=rule.priority)
                request = rule.process_request(request)
                yield request
