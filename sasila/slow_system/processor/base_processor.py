#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
from bs4 import BeautifulSoup as bs
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
    def __init__(self, regex_str=None, css_str=None, process_value=None):
        if not regex_str:
            self.regex = re.compile(regex_str)
        else:
            self.regex = None
        self.css_str = css_str
        self.process_value = process_value

    def extract_links(self, response):
        if self.process_value:
            return [response.nice_join(link) for link in self.process_value(response.m_response.content)]
        elif self.regex:
            return [response.nice_join(link) for link in self.regex.findall(response.m_response.content)]
        elif self.css_str:
            soup = bs(response.m_response.content)
            tags = soup.select(self.css_str)
            return [response.nice_join(tag.attrs["href"]) for tag in tags]


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
