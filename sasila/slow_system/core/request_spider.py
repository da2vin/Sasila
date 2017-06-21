#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from collections import Iterator
from sasila.slow_system.downloader.http.spider_request import Request
from sasila.slow_system.downloader.requests_downloader import RequestsDownLoader
from sasila.slow_system.scheduler.queue import PriorityQueue
from sasila.slow_system.utils import logger
from sasila.slow_system.utils.httpobj import urlparse_cached
import re
import time
import traceback

reload(sys)
sys.setdefaultencoding('utf-8')


def _priority_compare(r1, r2):
    return r2.priority - r1.priority


class RequestSpider(object):
    def __init__(self, processor=None, downloader=None, scheduler=None, batch_size=None, time_sleep=None):
        self._processor = processor
        self._host_regex = self._get_host_regex()
        self._spider_status = 'stopped'
        self._pipelines = []
        self._time_sleep = time_sleep
        if time_sleep:
            self._batch_size = 0
        else:
            if batch_size:
                self._batch_size = batch_size - 1
            else:
                self._batch_size = 99
        self._spider_name = processor.spider_name
        self._spider_id = processor.spider_id
        self._process_count = 0

        if not downloader:
            self._downloader = RequestsDownLoader()

        if not scheduler:
            self._queue = PriorityQueue(self._processor)
        else:
            self._queue = scheduler

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

    def stop(self):
        if self._spider_status == 'stopped':
            logger.info("STOP %s SUCCESS" % self._spider_id)
            return
        elif self._spider_status == 'stopping':
            while self._spider_status == 'stopping':
                pass
        elif self._spider_status == 'start':
            self._spider_status = 'stopping'
            while self._spider_status == 'stopping':
                pass

    def start(self):
        try:
            logger.info("START %s SUCCESS" % self._spider_id)
            self._spider_status = 'start'
            self._queue = PriorityQueue(self._processor)
            if len(self._processor.start_requests) > 0:
                for start_request in self._processor.start_requests:
                    if self._should_follow(start_request):
                        start_request.duplicate_remove = False
                        self._queue.push(start_request)
                        logger.info("start request:" + str(start_request))
            for batch in self._batch_requests():
                if len(batch) > 0:
                    self._crawl(batch)
                if self._spider_status == 'stopping':
                    break
            self._spider_status = 'stopped'
            logger.info("STOP %s SUCCESS" % self._spider_id)
        except Exception:
            logger.info("%s -- Exception -- Stopped -- %s" % (self._spider_id, traceback.format_exc()))
            self._spider_status = 'stopped'

    def restart(self):
        self._queue = PriorityQueue(self._processor)
        self._queue.clear()
        self.start()

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
        if self._time_sleep:
            time.sleep(self._time_sleep)
        for response in responses:
            callback = response.request.callback(response)
            if callback is not None:
                if isinstance(callback, Iterator):
                    pipe = self._queue.get_pipe()
                    for item in callback:
                        if isinstance(item, Request):
                            # logger.info("push request to queue..." + str(item))
                            if self._should_follow(item):
                                self._queue.push_pipe(item, pipe)
                        else:
                            self._process_count += 1
                            for pipeline in self._pipelines:
                                pipeline.process_item(item)
                    pipe.execute()
                else:
                    if isinstance(callback, Request):
                        # logger.info("push request to queue..." + str(back))
                        if self._should_follow(callback):
                            self._queue.push(callback)
                    else:
                        self._process_count += 1
                        for pipeline in self._pipelines:
                            pipeline.process_item(callback)

    def _should_follow(self, request):
        regex = self._host_regex
        # hostname can be None for wrong urls (like javascript links)
        host = urlparse_cached(request).hostname or ''
        return bool(regex.search(host))

    def _get_host_regex(self):
        """Override this method to implement a different offsite policy"""
        allowed_domains = getattr(self._processor, 'allowed_domains', None)
        if not allowed_domains:
            return re.compile('')  # allow all by default
        regex = r'^(.*\.)?(%s)$' % '|'.join(re.escape(d) for d in allowed_domains if d is not None)
        return re.compile(regex)
