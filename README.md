# Sasila [![version](https://img.shields.io/badge/version-0.0.6-green.svg)](https://pypi.python.org/pypi/Sasila) [![Build Status]][Travis CI] [![Coverage Status]][Coverage]

&emsp;&emsp;现在有很多爬虫框架，比如[**scrapy**](https://github.com/scrapy/scrapy)、[**webmagic**](https://github.com/code4craft/webmagic)、[**pyspider**](https://github.com/binux/pyspider)都可以在爬虫工作中使用，也可以直接通过[**requests**](https://github.com/requests/requests)+[**beautifulsoup**](https://github.com/il-vladislav/BeautifulSoup4)来写一些个性化的小型爬虫脚本。但是在实际爬取过程当中，爬虫框架各自有优势和缺陷。比如scrapy，它的功能强大，但过于强大的功能也许反而让新手无所适从，并且它采用twisted异步框架开发，对新手来说源码难以理解，项目难于调试。所以我模仿这些爬虫框架的优势，以尽量简单的原则，搭配gevent(实际上是grequests)开发了这套轻量级爬虫框架。

![jiagou](https://github.com/DarkSand/Sasila/blob/master/pic/jigou.png)

* downloader是下载器。
* processor是解析器。
* scheduler是调度器。
* pipeline是数据处理器。
* 将下载器，解析器，调度器，数据处理器注入核心core成为spider对象。
* 通过manager管理spider对象。
* manager透过webapi提供外部访问/控制接口。

## **主要特点**

* 框架代码结构简单易用，易于修改。新手、老鸟皆可把控。
* 采用gevent实现并发操作，与scrapy的twisted相比，代码更容易理解。
* 完全模块化的设计，强大的可扩展性。
* 使用方式和结构参考了[**scrapy**](https://github.com/scrapy/scrapy)和[**webmagic**](https://github.com/code4craft/webmagic)。对有接触过这两个框架的朋友非常友好。
* 不采用命令行来启动爬虫，方便调试。
* 对数据的解析模块并没有集成，可以自由使用[**beautifulsoup**](https://github.com/il-vladislav/BeautifulSoup4)、[**lxml**](https://github.com/lxml/lxml)、[**pyquery**](https://github.com/gawel/pyquery)、[**html5lib**](https://github.com/html5lib/html5lib-python)等等各种解析器进行数据抽取。
* 集成代理换IP功能。
* 支持高并发抓取数据。
* 支持分布式。
* 支持增量爬取。
* 支持爬取js动态渲染的页面(加载SeleniumDownLoader即可)。
* 提供webapi对爬虫进行管理、监控。
* 提供即时爬虫的集成思路和结构。

## **安装**
```
pip install sasila
```
## **准备**
* 请准备好您的redis服务器进行调度。
* 并在settings.py文件中 写入您的redis服务器地址
```python
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
```
## **构建processor(解析器)**
```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as bs
from sasila.system_normal.processor.base_processor import BaseProcessor
from sasila.system_normal.downloader.http.spider_request import Request
from sasila.system_normal.spider.spider_core import SpiderCore

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
**写法与scrapy几乎一样**

* 所有的解析器都继承自 *BaseProcessor* ，默认入口解析函数为def process(self, response)。
* 为该解析器设置spider_id和spider_name,以及限定域名。
* 初始爬取请求为 *start_requests*，构建Request对象，该对象支持GET、POST方法，支持优先级，设置回调函数等等所有构建request对象的一切属性。默认回调函数为 *process*。
* 可以使用@checkResponse装饰器对返回的 *response* 进行校验并记录异常日志。你也可以定义自己的装饰器。
* 解析函数因为使用 *yield* 关键字，所以是一个生成器。当 *yield* 返回 *Request* 对象，则会将 *Request* 对象推入调度器等待调度继续进行爬取。若 *yield* 不是返回 *Request* 对象则会进入 *pipeline* ， *pipeline* 将对数据进行清洗入库等操作。

**与scrapy相似，sasila同样提供*LinkExtractor的*方式来提取链接，以下是用*LinkExtractor*的方式构造*processor*下载妹子图的示例**

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sasila.system_normal.processor.base_processor import BaseProcessor, Rule, LinkExtractor
from sasila.system_normal.downloader.http.spider_request import Request
import os
import uuid

class MezituProcessor(BaseProcessor):
    spider_id = 'mzitu'
    spider_name = 'mzitu'
    allowed_domains = ['mzitu.com', 'meizitu.net']
    start_requests = [Request(url='http://www.mzitu.com/xinggan/')]

    rules = (
        Rule(LinkExtractor(regex_str=r"http://i.meizitu.net/\d{4}/\d{2}/[0-9a-z]+.jpg"),callback="save", priority=3),
        Rule(LinkExtractor(regex_str=r"http://www.mzitu.com/\d+"), priority=1),
        Rule(LinkExtractor(regex_str=r"http://www.mzitu.com/\d+/\d+"), priority=2),
        Rule(LinkExtractor(regex_str=r"http://www.mzitu.com/xinggan/page/\d+"), priority=0),
    )

    def save(self, response):
        if response.m_response:
            if not os.path.exists("img"):
                os.mkdir("img")
            with open("img/" + str(uuid.uuid1()) + ".jpg", 'wb') as fs:
                fs.write(response.m_response.content)
                print("download success!")
```

**LinkExtractor的构造方式为**

```python
LinkExtractor(regex_str=None, css_str=None, process_value=None)
```

* 提供正则表达式提取方式：*regex_str*
* 提供css选择器提取方式：*css_str*
* 也可以自定义*process_value*来提取链接，其中*process_value*是一个生成器
* 若使用此方式构造*processor*，请不要定义默认入口函数def process(self, response)


## **构建pipeline**
该pipeline获取数据后将数据转为json格式，并输出到屏幕
```python
from sasila.system_normal.pipeline.base_pipeline import ItemPipeline

class ConsolePipeline(ItemPipeline):
    def process_item(self, item):
        print json.dumps(item).decode("unicode-escape")
```
## **构建spider(爬虫对象）**
* 通过注入 *processor* 生成spider对象
```python
from sasila.system_normal.spider.spider_core import SpiderCore

spider = SpiderCore(Mzi_Processor())
```
* RequestSpider对象包含批下载数量 *batch_size*，下载间隔 *time_sleep*，使用代理 *use_proxy* 等一切必要的属性
```python
SpiderCore(processor=None, downloader=None, use_proxy=False,scheduler=None,batch_size=None,time_sleep=None)
```
* 本项目集成使用代理IP的功能，只要在构建RequestSpider时将  *use_proxy* 设置为 *True*,并在脚本同级目录下放置proxy.txt文件即可。你也可以在settings.py文件中写入代理IP文件路径。
```python
PROXY_PATH_REQUEST = 'proxy/path'
```
* proxy.txt文件中请写入代理IP，格式为：IP,端口号。若该代理IP有账号密码，在末尾追加账号密码即可。
```text
127.0.0.1,8080
127.0.0.2,8080,user,pwd
127.0.0.3,8080,user,pwd
```
* RequestSpider已经默认设置好了 *downloader* 和 *scheduler*，如果不满意，可以自己进行定制。
* 可以为spider设置 *downloader* 和 *pipeline* 甚至 *scheduler*
```python
 spider = spider.set_pipeline(ConsolePipeline())
```
* 可以通过该方式启动爬虫
```python
spider.start()
```
* 也可以将spider注入*manager*进行管理
```python
from sasila.system_normal.manager import manager
from sasila import system_web

manager.set_spider(spider)

web.start()
```

访问 http://127.0.0.1:5000/slow_spider/start?spider_id=mzi_spider 来启动爬虫。

访问 http://127.0.0.1:5000/slow_spider/stop?spider_id=mzi_spider 来停止爬虫。

访问 http://127.0.0.1:5000/slow_spider/detail?spider_id=mzi_spider 来查看爬虫详细信息。

## **针对需要登录才能爬取的处理办法**
* 可以为downloader加载登录器(loginer),在使用downloader的时候使用loginer进行登录获取cookies,再进行爬取
* 也可以自己定义一个cookie池，批量进行登录并将登录成功的cookies放进cookie池中随时进行取用。项目中暂时没有这些功能。欢迎pull request~

## **架构**
![jichu](https://github.com/DarkSand/Sasila/blob/master/pic/jichu.png)

* 任务由 scheduler 发起调度，downloader 抓取网页内容， processor 执行预先编写的py脚本，输出结果或产生新的提链任务（发往 scheduler），形成闭环。
* 每个脚本被认为是一个spider，spiderid确定一个任务。
* downloader
1. method, header, cookie, proxy,timeout 等等抓取调度控制。
2. 可以通过适配类似 phantomjs 的webkit引擎支持渲染。
* processor
1. 灵活运用pyquery，beautifulsoup等解析页面。
2. 在脚本中完全控制调度抓取的各项参数。
3. 可以向后链传递信息。
4. 异常捕获。
* scheduler
1. 任务优先级。
2. 对任务进行监控。
3. 对任务进行去重等操作。
4. 支持增量。
* webApi
1. 对爬虫进行增删改查等操作。
* 非及时爬虫流程图

![feijishi](https://github.com/DarkSand/Sasila/blob/master/pic/feijishi.png)

## **即时爬虫**
即时爬虫是可以通过api调用，传入需要爬取的页面或者需求，即时爬取数据并返回结果。现阶段开发并不完善。仅提供思路参考。示例核心代码在 *sasila.system_instant* 中。

* 即时爬虫-获取数据流程图

![huoqushuju](https://github.com/DarkSand/Sasila/blob/master/pic/jishi-huoqushuju.png)

* 即时爬虫-授权流程图

![shouquan](https://github.com/DarkSand/Sasila/blob/master/pic/jishi-shouquan.png)

## **为啥叫Sasila？**

![spider](https://github.com/DarkSand/Sasila/blob/master/pic/spider.jpg)

作为一个wower,你可以猜到吗ヾ(￣▽￣)

## **联系方式**

如果对使用有疑问，或者有想法，欢迎加入讨论群:602909155交流~


[Build Status]:         https://img.shields.io/travis/DarkSand/Sasila.svg?branch=master&style=flat
[Travis CI]:            https://travis-ci.org/DarkSand/Sasila
[Coverage Status]:      https://img.shields.io/coveralls/DarkSand/Sasila.svg?branch=master&style=flat
[Coverage]:             https://coveralls.io/github/DarkSand/Sasila


