#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
from bloom_filter import BloomFilter
import dill

reload(sys)
sys.setdefaultencoding('utf-8')


class UrlScheduler(object):
    def __init__(self, task_id):
        self.task_id = task_id
        self._filter = BloomFilter(key=self.task_id)
        self._server = redis.StrictRedis()

    def push(self, request, duplicate_remove=True):
        request_pickle = dill.dumps(request)
        if not duplicate_remove:
            self._server.lpush(self.task_id, request_pickle)
        else:
            if not self._filter.is_contains(request_pickle):
                self._server.lpush(self.task_id, request_pickle)
                self._filter.insert(request_pickle)

    def pushf(self, request, duplicate_remove=True):
        request_pickle = dill.dumps(request)
        if not duplicate_remove:
            self._server.rpush(self.task_id, request_pickle)
        else:
            if not self._filter.is_contains(request_pickle):
                self._server.rpush(self.task_id, request_pickle)
                self._filter.insert(request_pickle)

    def poll(self):
        requests_pickle = self._server.rpop(self.task_id)
        # while not requests_pickle:
        #     requests_pickle = self._server.rpop(self.task_id)
        if requests_pickle:
            return dill.loads(requests_pickle)
        else:
            return None

    def despose(self):
        self._server.delete(self.task_id)

    def count(self):
        return self._server.llen(self.task_id)


if __name__ == '__main__':
    pass
