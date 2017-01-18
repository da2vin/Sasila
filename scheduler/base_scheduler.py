#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from task_db import TaskDb

reload(sys)
sys.setdefaultencoding('utf-8')


class BaseScheduler(object):
    def __init__(self):
        self.task = TaskDb

