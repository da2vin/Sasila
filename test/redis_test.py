#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import redis

reload(sys)
sys.setdefaultencoding('utf-8')

r = redis.Redis()
r.set('name', 'mjw')

print r.get('name')
