#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
import cPickle
from bloom_filter import BloomFilter
from sasila.slow_system.utils.reqser import request_to_dict, request_from_dict

reload(sys)
sys.setdefaultencoding('utf-8')


class Base(object):
    """Per-spider base queue class"""

    def __init__(self, task_id, processor):
        self.task_id = task_id
        self.processor = processor
        self._filter = BloomFilter(key=self.task_id)
        self._server = redis.StrictRedis()

    def __len__(self):
        """Return the length of the queue"""
        raise NotImplementedError

    def push(self, request):
        """Push a request"""
        raise NotImplementedError

    def pop(self):
        """Pop a request"""
        raise NotImplementedError

    def clear(self):
        """Clear queue/stack"""
        self.server.delete(self.key)


class PriorityQueue(Base):
    def get_pipe(self):
        return self._server.pipeline()

    def push_pipe(self, request, pipe):
        score = -request.priority
        data = cPickle.dumps(request_to_dict(request, self.processor), protocol=-1)
        if not request.duplicate_remove:
            pipe.execute_command('ZADD', self.task_id, score, data)
        else:
            if not self._filter.is_contains(data):
                pipe.execute_command('ZADD', self.task_id, score, data)
                self._filter.insert(data)

    def push(self, request):
        score = -request.priority
        data = cPickle.dumps(request_to_dict(request, self.processor), protocol=-1)
        if not request.duplicate_remove:
            self._server.execute_command('ZADD', self.task_id, score, data)
        else:
            if not self._filter.is_contains(data):
                self._server.execute_command('ZADD', self.task_id, score, data)
                self._filter.insert(data)

    def pop(self):
        pipe = self._server.pipeline()
        pipe.multi()
        pipe.zrange(self.task_id, 0, 0).zremrangebyrank(self.task_id, 0, 0)
        results, count = pipe.execute()
        if results:
            return request_from_dict(cPickle.loads(results[0]), self.processor)
        else:
            return None

    def clear(self):
        self._server.delete(self.task_id)

    def __len__(self):
        return self._server.zcard(self.task_id)


if __name__ == '__main__':
    queue = PriorityQueue("test")
    print queue
