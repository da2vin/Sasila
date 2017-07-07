#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup as bs

with open('html.txt', 'r') as f:
    content = f.read()
    soup = bs(content, 'lxml')
    print soup.select('div.details li')[0].select('span')[0].text
