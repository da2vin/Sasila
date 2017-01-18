#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
import pickle
from bloom_filter import BloomFilter

reload(sys)
sys.setdefaultencoding('utf-8')


class TaskDb(object):
    def __init__(self):
        self.task_id = None
        self.filter = BloomFilter(key=self.task_id)
        self.server = redis.StrictRedis()

    def push(self, request):
        request_pickle = pickle.dumps(request)
        if not self.filter.is_contains(request_pickle):
            self.server.lpush(self.task_id, request_pickle)

    def poll(self):
        requests_pickle = self.server.blpop(self.task_id)
        return pickle.load(requests_pickle)[1]
