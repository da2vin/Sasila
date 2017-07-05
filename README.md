# Sasila [![version](https://img.shields.io/badge/version-0.0.1-green.svg)](https://pypi.python.org/pypi/Sasila)

&emsp;&emsp;在爬虫工作中，我接触过较多的爬虫框架，比如[**scrapy**](https://github.com/scrapy/scrapy)、[**webmagic**](https://github.com/code4craft/webmagic)、[**pyspider**](https://github.com/binux/pyspider)，也经常直接通过[**requests**](https://github.com/requests/requests)+[**beautifulsoup**](https://github.com/il-vladislav/BeautifulSoup4)来写一些个性化的小型爬虫脚本。但是在实际爬取过程当中，仍然不能完全满足实际需要。所以我开发了这套**小型的**、**灵活的**、**功能完善的**爬虫框架。

![jiagou](https://github.com/DarkSand/Sasila/blob/master/pic/jigou.png)

## **主要特点**

* 框架代码结构简单易用，易于修改。
* 采用gevent实现并发操作，与scrapy的twisted相比，代码更容易理解。
* 完全模块化的设计，强大的可扩展性。
* 使用方式和结构参考了[**scrapy**](https://github.com/scrapy/scrapy)和[**webmagic**](https://github.com/code4craft/webmagic)。对有接触过这两个框架的朋友非常友好。
* 对数据的解析模块并没有集成，可以自由使用[**beautifulsoup**](https://github.com/il-vladislav/BeautifulSoup4)、[**lxml**](https://github.com/lxml/lxml)、[**pyquery**](https://github.com/gawel/pyquery)、[**html5lib**](https://github.com/html5lib/html5lib-python)等等各种解析器进行数据抽取。
* 集成代理换IP功能。
* 支持多线程。
* 支持分布式。
* 支持增量爬取。
* 支持爬取js动态渲染的页面。
* 提供webapi对爬虫进行管理、监控。
* 提供即时爬虫的集成思路和结构。

## **安装**
```
pip install sasila
```

## **构建processor(解析器)**
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from base_processor import BaseProcessor
from sasila.slow_system.downloader.http.spider_request import Request
from sasila.slow_system.core.request_spider import RequestSpider

class Mzi_Processor(BaseProcessor):
    spider_id = 'mzi_spider'
    spider_name = 'mzi_spider'
    allowed_domains = ['mzitu.com']
    start_requests = [Request(url='http://www.mzitu.com/', priority=0)]

    @checkResponse
    def process(self, response):
        soup = bs(response.m_response.content, 'lxml')
        print soup.title.string
        href_list = soup.select('a')
        for href in href_list:
            yield Request(url=response.nice_join(href['href']))
```
写法与scrapy几乎一样

* 所有的解析器都继承自BaseProcessor，默认入口解析函数为def process(self, response)。
* 为该解析器设置spider_id和spider_name,以及限定域名。
* 初始爬取请求为start_requests，构建Request对象，该对象支持GET、POST方法，支持优先级，设置回调函数等等所有构建request对象的一切属性。默认回调函数为*process*。
* 解析函数因为使用yield关键字，所以是一个生成器。当yield返回Request对象，则会将Request对象推入调度器等待调度继续进行爬取。若yield不是返回Request对象则会进入*pipeline*，*pipeline*将对数据进行清洗入库等操作。

## **构建pipeline**
```python
from sasila.slow_system.pipeline.base_pipeline import ItemPipeline

class ConsolePipeline(ItemPipeline):
    def process_item(self, item):
        print json.dumps(item).decode("unicode-escape")
```
## **构建spider(爬虫对象）**
* 通过注入*processor*生成spider对象
```python
from sasila.slow_system.core.request_spider import RequestSpider

spider = RequestSpider(Mzi_Processor())
```
* RequestSpider对象包含批下载数量*batch_size*，下载间隔*time_sleep*，使用代理*use_proxy*等一切必要的属性
```python
RequestSpider(processor=None, downloader=None, use_proxy=False,scheduler=None,batch_size=None,time_sleep=None)
```
* RequestSpider已经默认设置好了*downloader*和*scheduler*，如果不满意，可以自己进行定制。
* 可以为spider设置*downloader*和*pipeline*甚至*scheduler*
```python
 spider = spider.set_pipeline(ConsolePipeline())
```
* 可以通过该方式启动爬虫
```python
spider.start()
```
* 也可以将spider注入*manager*进行管理
```python
from sasila.slow_system.manager import manager

manager.set_spider(spider)

sasila.start()
```

>访问 http://127.0.0.1:5000/slow_spider/start?spider_id=mzi_spider 来启动爬虫。
>访问 http://127.0.0.1:5000/slow_spider/stop?spider_id=mzi_spider 来停止爬虫。
>访问 http://127.0.0.1:5000/slow_spider/detail?spider_id=mzi_spider 来查看爬虫详细信息。

## **架构**
![jichu](https://github.com/DarkSand/Sasila/blob/master/pic/jichu.png)

* 任务由 scheduler 发起调度，fetcher 抓取网页内容， processor 执行预先编写的py脚本，输出结果或产生新的提链任务（发往 scheduler），形成闭环。
* 每个脚本被认为是一个spider，spiderid确定一个任务。
* downloader
1. method, header, cookie, proxy,timeout 等等抓取调度控制。
2. 可以通过适配类似 phantomjs 的webkit引擎支持渲染。
3. 流量控制