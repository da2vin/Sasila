#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
from sasila.slow_system.utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')

try:
    l1 = list()
    a = l1[0]
    print a

except Exception:
    logger.error(traceback.format_exc())
