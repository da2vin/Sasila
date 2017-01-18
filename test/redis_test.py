#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis

reload(sys)
sys.setdefaultencoding('utf-8')

r = redis.StrictRedis()
r.sadd('aaa', 'mjw1')
r.sadd('aaa', 'mjw2')
r.sadd('aaa', 'mjw3')
r.sadd('aaa', 'mjw4')
r.sadd('aaa', 'mjw5')

print r.lpop("aaa")



