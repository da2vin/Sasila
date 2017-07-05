# Sasila [![version](https://img.shields.io/badge/version-0.0.1-green.svg)](https://pypi.python.org/pypi/Sasila)

&emsp;&emsp;在爬虫工作中，我接触过较多的爬虫框架，比如[**scrapy**](https://github.com/scrapy/scrapy)、[**webmagic**](https://github.com/code4craft/webmagic)、[**pyspider**](https://github.com/binux/pyspider)，也经常直接通过[**requests**](https://github.com/requests/requests)+[**beautifulsoup**](https://github.com/il-vladislav/BeautifulSoup4)来写一些个性化的小型爬虫脚本。但是在实际爬取过程当中，仍然不能完全满足实际需要。所以我开发了这套**小型的**、**灵活的**、**功能完善的**爬虫框架。

![jichu](https://github.com/DarkSand/Sasila/blob/master/pic/jigou.png)

##**Sasila的主要特色**：

* 框架代码结构简单易用，易于修改。
* 完全模块化的设计，强大的可扩展性。
* 使用方式和结构参考了[**scrapy**](https://github.com/scrapy/scrapy)和[**webmagic**](https://github.com/code4craft/webmagic)。对有接触过这两个框架的朋友非常友好。
* 对数据的解析模块并没有集成，可以自由使用[**beautifulsoup**](https://github.com/il-vladislav/BeautifulSoup4)、[**lxml**](https://github.com/lxml/lxml)、[**pyquery**](https://github.com/gawel/pyquery)、[**html5lib**](https://github.com/html5lib/html5lib-python)等等各种解析器进行数据抽取。
* 集成代理换IP功能。
* 支持多线程。
* 支持分布式。
* 支持增量爬取。
* 支持爬取js动态渲染的页面。
* 提供http接口对爬虫进行管理、监控。
* 提供即时爬虫的集成思路和结构。
