#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from lxml import etree

reload(sys)
sys.setdefaultencoding('utf-8')

text = '''
<div>
    <ul>
         <li class="item-0"><a href="link1.html">first item</a></li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-inactive"><a href="link3.html">third item</a></li>
         <li class="item-1"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a>
     </ul>
 </div>
'''
html = etree.HTML(text)
result = html.xpath('//li[contains(@class,\'item-1\')]/preceding::*')[0]
print etree.tostring(result)
