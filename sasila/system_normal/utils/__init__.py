#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import logging
import os

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

if not os.path.exists("log"):
    os.mkdir("log")
logger = logging.getLogger("SASILA")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("log/SASILA.log")
fh.setLevel(logging.ERROR)
# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# 将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)
