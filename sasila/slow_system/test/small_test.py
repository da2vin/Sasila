#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from hashlib import md5

reload(sys)
sys.setdefaultencoding('utf-8')

str_input = "aaaaaaaaaaa"
m5 = md5()
m5.update(str_input)
str_input = m5.hexdigest()
key = "test"
blockNum = 1235
name = key + str(int(str_input[0:2], 16) % blockNum)

print name
