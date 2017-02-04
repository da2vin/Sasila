#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

import gevent
import gevent.monkey
from collections import Iterator
from sasila.downloader.http.spider_request import Request
from sasila.downloader.requests_downloader import RequestsDownLoader
from sasila.scheduler.queue import PriorityQueue
from sasila.utils import logger

# gevent.monkey.patch_all()
reload(sys)
sys.setdefaultencoding('utf-8')


def _priority_compare(r1, r2):
    return r2.priority - r1.priority


class RequestSpider(object):
    def __init__(self, processor=None, downloader=None, scheduler=None):
        self._processor = processor
        self._spider_status = 0
        self._pipelines = []
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

    def _priority_compare(r1, r2):
        return r1.priority - r2.priority

    def start(self):
        if len(self._processor.start_requests) > 0:
            for start_request in self._processor.start_requests:
                start_request.duplicate_remove = False
                self._queue.push(start_request)
                logger.info("start request:" + str(start_request))
        for batch in self._batch_requests():
            if len(batch) > 0:
                tasks = [gevent.spawn(self._crawl, r) for r in batch]
                gevent.joinall(tasks)

    def _batch_requests(self):
        batch = []
        count = 0
        while True:
            count += 1
            if len(batch) > 9 or count > 9:
                batch.sort(_priority_compare)
                yield batch
                batch = []
                count = 0
            temp_request = self._queue.pop()
            if temp_request:
                batch.append(temp_request)

    def _crawl(self, request):
        if not request.callback:
            request.callback = self._processor.process
        response = self._downloader.download(request)
        callback = request.callback(response)
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
