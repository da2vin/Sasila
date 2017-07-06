#!/usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
# from sasila.slow_system.pipeline.base_pipeline import ItemPipeline
# import json
# from sasila.slow_system.utils.kafka_utils import send_message
#
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
#
# class KafkaPipeline(ItemPipeline):
#     def process_item(self, item):
#         send_message("dataCollectionTopic", bytes("CompanyConsummer__" + json.dumps(item).decode("unicode-escape")))
