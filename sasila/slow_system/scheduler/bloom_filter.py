#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis
from hashlib import md5
from sasila.settings import default_settings

reload(sys)
sys.setdefaultencoding('utf-8')


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class BloomFilter(object):
    def __init__(self, host=default_settings.REDIS_HOST, port=default_settings.REDIS_PORT, db=0, block_num=1, key='bloomfilter'):
        """
        :param host: the host of Redis
        :param port: the port of Redis
        :param db: witch db in Redis
        :param block_num: one blockNum for about 90,000,000; if you have more strings for filtering, increase it.
        :param key: the key's name in Redis
        """
        self.server = redis.Redis(host=host, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = block_num
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def is_contains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)
        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)


if __name__ == '__main__':
    bf1 = BloomFilter(key='test1')
    bf2 = BloomFilter(key='test2')
    bf3 = BloomFilter(key='test3')
    bf4 = BloomFilter(key='test4')
    bf1.insert('http://www.baidu.com')
    bf2.insert('http://www.baidu.com')
    bf3.insert('http://www.baidu.com')
    bf4.insert('http://www.baidu.com')

    print bf1.server.keys()
    bf1.clear()
    print bf1.server.keys()
    bf2.clear()
    print bf1.server.keys()
    bf3.clear()
    print bf1.server.keys()
    bf4.clear()
    print bf1.server.keys()
