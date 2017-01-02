#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import Iterator
from sasila.slow_system.downloader.http.spider_request import Request
from sasila.slow_system.downloader.requests_downloader import RequestsDownLoader
from sasila.slow_system.scheduler.queue import PriorityQueue

from sasila.slow_system.utils import logger

reload(sys)
sys.setdefaultencoding('utf-8')


def _priority_compare(r1, r2):
    return r2.priority - r1.priority


class RequestSpider(object):
    def __init__(self, processor=None, downloader=None, scheduler=None):
        self._processor = processor
        self._spider_status = 0
        self._pipelines = []
        self._batch_size = 99
        self._spider_name = processor.spider_name
        self._spider_id = processor.spider_id

        if not downloader:
            self._downloader = RequestsDownLoader()

        if not scheduler:
            self._queue = PriorityQueue(self._spider_id, self._processor)

    def create(self, processor):
        self._processor = processor
        return self

    def set_scheduler(self, scheduler):
        self._queue = scheduler
        return self

    def set_downloader(self, downloader):
        self._downloader = downloader
        return self

    def set_pipeline(self, pipeline):
        self._pipelines.append(pipeline)
        return self

    def get_status(self):
        return self._spider_status

    def init_component(self):
        pass

    def start(self):
        if len(self._processor.start_requests) > 0:
            for start_request in self._processor.start_requests:
                start_request.duplicate_remove = False
                self._queue.push(start_request)
                logger.info("start request:" + str(start_request))
        for batch in self._batch_requests():
            if len(batch) > 0:
                self._crawl(batch)

    def _batch_requests(self):
        batch = []
        count = 0
        while True:
            count += 1
            if len(batch) > self._batch_size or count > self._batch_size:
                batch.sort(_priority_compare)
                yield batch
                batch = []
                count = 0
            temp_request = self._queue.pop()
            if temp_request:
                if not temp_request.callback:
                    temp_request.callback = self._processor.process
                batch.append(temp_request)

    def _crawl(self, batch):
        responses = self._downloader.download(batch)
        for response in responses:
            callback = response.request.callback(response)
            if isinstance(callback, Iterator):
                pipe = self._queue.get_pipe()
                for item in callback:
                    if isinstance(item, Request):
                        # logger.info("push request to queue..." + str(item))
                        self._queue.push_pipe(item, pipe)
                    else:
                        for pipeline in self._pipelines:
                            pipeline.process_item(item)
                pipe.execute()
            else:
                if isinstance(callback, Request):
                    # logger.info("push request to queue..." + str(back))
                    self._queue.push(callback)
                else:
                    for pipeline in self._pipelines:
                        pipeline.process_item(callback)