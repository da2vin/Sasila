#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

text = '''
    <bookstore>

    <book category="COOKING">
      <title lang="en">Everyday Italian</title>
      <author>Giada De Laurentiis</author>
      <year>2005</year>
      <price>30.00</price>
    </book>

    <book category="CHILDREN">
      <title lang="en">Harry Potter</title>
      <author>J K. Rowling</author>
      <year>2005</year>
      <price>29.99</price>
    </book>

    <book category="WEB">
      <title lang="en">XQuery Kick Start</title>
      <author>James McGovern</author>
      <author>Per Bothner</author>
      <author>Kurt Cagle</author>
      <author>James Linn</author>
      <author>Vaidyanathan Nagarajan</author>
      <year>2003</year>
      <price>49.99</price>
    </book>

    <book category="WEB">
      <title lang="en">Learning XML</title>
      <author>Erik T. Ray</author>
      <year>2003</year>
      <price>39.95</price>
    </book>

    </bookstore>
'''
html = etree.HTML(text)
result = html.xpath('//bookstore/book[@category=\'WEB\' and contains(./author/text(),\'Ray\')]/title')
for r in result:
    print etree.tostring(r)
