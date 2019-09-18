# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import sys
import logging

from threading import Timer
from splunk_sdk.ingest import IngestAPI, Event, HTTPResponse
from typing import Optional, Callable, List

DEFAULT_BATCH_SIZE = 1040000  # bytes

logger = logging.getLogger(__name__)


class EventBatcher(object):

    def __init__(self, ingest_service: IngestAPI,
                 batch_size: int = DEFAULT_BATCH_SIZE,
                 batch_count: int = 500, timeout: int = 30,
                 batch_dispatch_handler:
                 Callable[[List[Event]], Optional[HTTPResponse]] = None,
                 error_handler: Callable[[Exception], None] = None):
        """Creates an instance of the EventBatcher
        :param ingest_service:
        :param batch_size: size limit of the batch in bytes
        :param batch_count: number of events in the batch
        :param timeout: time in seconds to flush the queue and send events
        :param batch_dispatch_handler: custom handler to deal with responses
        :param error_handler: custom exception handler
        """
        self.ingest_service = ingest_service
        self.batch_size = batch_size
        self.batch_count = batch_count
        self.timeout = timeout

        self.queue = []
        self.timer = Timer(timeout, self.flush)
        self.timer.start()

        if batch_dispatch_handler is None:
            self.batch_dispatch_handler = self._batch_dispatch_handler
        else:
            self.batch_dispatch_handler = batch_dispatch_handler

        if error_handler is None:
            self.error_handler = self._error_handler
        else:
            self.error_handler = error_handler

    def add(self, event: Event) -> None:
        """Adds a new event to the list and sends all of the events if the
        event limits are met.
        :param event:
        """
        self.queue.append(event)
        self._run()

    def _run(self) -> Optional[HTTPResponse]:
        """Processes the events in the queue and sends them to the ingest API
        when the queue limits are met or exceeded.
        Otherwise, the event is queued until the limit is reached.
        A timer runs periodically to ensure that events do not stay queued too
        long.
        :return: HTTPResponse
        """
        max_count_reached = len(self.queue) >= self.batch_count
        byte_size_reached = sys.getsizeof(self.queue) >= self.batch_size

        if max_count_reached or byte_size_reached:
            return self.flush()

    def stop(self) -> Optional[HTTPResponse]:
        """Performs a flush operation if the queue is not empty.
        :return: HTTPResponse
        """
        self._stop_timer()
        if self.queue and len(self.queue) > 0:
            return self.flush()

    def set_timer(self) -> None:
        """Creates a periodic task to send all of the events.
        """
        self.timer = Timer(self.timeout, self.flush)
        self.timer.start()
        if self.queue and len(self.queue) > 0:
            self.flush()

    def reset_timer(self) -> None:
        """Resets the timer and updates the timer ID.
        """
        self._stop_timer()
        self.timer = Timer(self.timeout, self.flush)
        self.timer.start()

    def _stop_timer(self) -> None:
        """Stops the timer.
        """
        self.timer.cancel()

    @staticmethod
    def _batch_dispatch_handler(func, data) -> Optional[HTTPResponse]:
        """Default handling for sending events
        :param data: batched events
        """
        return func(data)

    def _error_handler(self, e) -> None:
        """Default error handler.
        :param e:
        """
        logger.error(e)

    def flush(self) -> Optional[HTTPResponse]:
        """Cleans up the events and timer.
        """
        self.reset_timer()
        data = self.queue
        self.queue = []
        try:
            return self.batch_dispatch_handler(self.ingest_service.post_events,
                                               data)
        except Exception as e:
            self.error_handler(e)
