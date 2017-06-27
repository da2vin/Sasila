#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def test():
    with open(name='test.txt', mode='r') as f:
        content = f.read()
    start = time.time()
    soup = bs(content, 'lxml')
    if len(soup.select('div.car-title h2')) != 0:
        car = soup.select('div.car-title h2')[0].text
        detail_list = soup.select('div.details li')
        if len(detail_list) == 0:
            soup = bs(content, 'html5lib')
            detail_list = soup.select('div.details li')
        mileage = detail_list[0].select('span')[0].text.replace('万公里', '')
        first_borad_date = detail_list[1].select('span')[0].text
        gear = detail_list[2].select('span')[0].text.split('／')[0]
        displacement = detail_list[2].select('span')[0].text.split('／')[1]
        price = soup.select('div.car-price ins')[0].text.replace('￥', '')
        crawl_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    print time.time() - start


test()
