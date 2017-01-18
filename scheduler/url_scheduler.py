#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
import pickle
from bloom_filter import BloomFilter

reload(sys)
sys.setdefaultencoding('utf-8')


class UrlScheduler(object):
    def __init__(self, task_id):
        self.task_id = task_id
        self._filter = BloomFilter(key=self.task_id)
        self._server = redis.StrictRedis()

    def push(self, request, dont_filter=True):
        request_pickle = pickle.dumps(request)
        if dont_filter:
            self._server.lpush(self.task_id, request_pickle)
        else:
            if not self._filter.is_contains(request_pickle):
                self._server.lpush(self.task_id, request_pickle)
                self._filter.insert(request_pickle)

    def pushf(self, request, dont_filter=True):
        request_pickle = pickle.dumps(request)
        if dont_filter:
            self._server.rpush(self.task_id, request_pickle)
        else:
            if not self._filter.is_contains(request_pickle):
                self._server.rpush(self.task_id, request_pickle)
                self._filter.insert(request_pickle)

    def poll(self):
        requests_pickle = self._server.brpop(self.task_id)[1]
        return pickle.loads(requests_pickle)

    def despose(self):
        self._server.delete(self.task_id)

    def count(self):
        return self._server.llen(self.task_id)


if __name__ == '__main__':
    pass
