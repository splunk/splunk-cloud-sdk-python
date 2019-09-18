# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import os
import pytest
import logging

from splunk_sdk.ingest import IngestAPI, HTTPResponse
from splunk_sdk.ingest.ingest_event_batcher import EventBatcher, \
    DEFAULT_BATCH_SIZE
from test.test_ml import _parse_csv as parse_csv
from test.fixtures import get_test_client_ml as test_client  # NOQA

BATCH_COUNT = 50
EVENTS = parse_csv(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                "data/ml/iris.csv"))

logger = logging.getLogger(__name__)


def _response_handler(func, data):
    """This is an example callback function that allows for custom error
    handling

    :param func: The ingest.post_events method
    :param data: The batch of events to send
    :return:
    """
    resp = func(data)
    if resp is not None:
        assert (isinstance(resp, HTTPResponse))
        if resp.code != "SUCCESS":
            logger.error("Error encountered in %s" % data)
            pytest.xfail(resp.code)
            # throw new Exception so caller can stop or reset batcher
            raise Exception(resp.code)


def _error_handler(e: Exception):
    logger.error(e)
    pytest.fail()
    # rethrow so caller can stop the batcher
    raise e


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events(test_client):
    ingest = IngestAPI(test_client)
    batcher = EventBatcher(ingest_service=ingest,
                           batch_size=DEFAULT_BATCH_SIZE,
                           batch_count=BATCH_COUNT,
                           batch_dispatch_handler=_response_handler)
    assert (batcher is not None)

    for e in EVENTS:
        try:
            assert(len(batcher.queue) <= BATCH_COUNT)
            batcher.add(e)
        except Exception:
            batcher.stop()

    # kill the timer
    batcher.stop()

    assert (len(batcher.queue) == 0)
