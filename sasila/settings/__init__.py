#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imp
import sys
import os

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

import sasila.settings.default_settings

setting_path = os.path.join(os.getcwd(), 'settings.py')

# 如果运行目录存在settings.py文件，则对默认设置进行覆写
if os.path.exists(setting_path):
    new_settings = imp.load_source('settings', setting_path)

    new_settings_dict = dict()
    for key in dir(new_settings):
        if key.isupper():
            new_settings_dict[key] = getattr(new_settings, key)
    if sys.version_info < (3, 0):
        for key, value in new_settings_dict.iteritems():
            setattr(default_settings, key, value)
    else:
        for key, value in new_settings_dict.items():
            setattr(default_settings, key, value)