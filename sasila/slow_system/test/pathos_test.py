#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from multiprocessing.process import Process
from multiprocessing import Manager
from sasila.slow_system.processor.mzitu_proccessor import mzitu_spider

reload(sys)
sys.setdefaultencoding('utf-8')


def test1():
    manager = Manager()
    localResultDict = manager.dict()
    Process(target=mzitu_spider.start).start()
    print localResultDict.keys()


if __name__ == "__main__":
    test1()
