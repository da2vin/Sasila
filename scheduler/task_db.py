#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
import pickle
from bloom_filter import BloomFilter

reload(sys)
sys.setdefaultencoding('utf-8')


class TaskDb(object):
    def __init__(self, task_id):
        self.task_id = task_id
        self._filter = BloomFilter(key=self.task_id)
        self._server = redis.StrictRedis()

    def push(self, request):
        request_pickle = pickle.dumps(request)
        if not self._filter.is_contains(request_pickle):
            self._server.lpush(self.task_id, request_pickle)

    def poll(self):
        requests_pickle = self._server.blpop(self.task_id)[1]
        return pickle.loads(requests_pickle)


if __name__ == '__main__':
    pass
