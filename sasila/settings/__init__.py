#!/usr/bin/env python
# -*- coding: utf-8 -*-
import imp
import os

import default_settings

setting_path = os.path.join(os.getcwd(), 'settings.py')
new_settings = imp.load_source('settings', setting_path)

new_settings_dict = dict()
for key in dir(new_settings):
    if key.isupper():
        new_settings_dict[key] = getattr(new_settings, key)

for key, value in new_settings_dict.iteritems():
    setattr(default_settings, key, value)
