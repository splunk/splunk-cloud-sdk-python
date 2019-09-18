# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest

from splunk_sdk.base_client import HTTPError
from splunk_sdk.ingest import IngestAPI, Event, HTTPResponse, Metric, \
    MetricAttribute, MetricEvent
from test.fixtures import get_test_client as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events(test_client):
    ingest = IngestAPI(test_client)

    event_data = Event(body='event1', host='host1', source='source1', sourcetype='sourcetype1',
                       attributes={'data': 'data1'}, timestamp=1533671808138)
    event_list = [event_data]
    event_response = ingest.post_events(event_list)

    assert (isinstance(event_response, HTTPResponse))
    assert (event_response.code == 'SUCCESS')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_metrics(test_client):
    ingest = IngestAPI(test_client)

    metrics = Metric('CPU', value=5.5, dimensions={'data': 'data1'}, unit='units')
    metrics_list = [metrics]
    met_attr = MetricAttribute(default_type='data1', default_dimensions={'dimension': 'dValue'}, default_unit='data2')
    metrics_data = MetricEvent(metrics_list, host='host1', source='source1',
                               sourcetype='sourcetype1', timestamp=1533671808138,
                               attributes=met_attr)
    metrics_data_list = [metrics_data]
    metrics_response = ingest.post_metrics(metrics_data_list)

    assert (isinstance(metrics_response, HTTPResponse))
    assert (metrics_response.code == 'SUCCESS')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events_bad_request(test_client):
    ingest = IngestAPI(test_client)
    event_list = []
    error_str = 'Empty array was provided as input'
    try:
        ingest.post_events(event_list)
    except HTTPError as error:
        assert (error.http_status_code == 400)
        assert (error.code == 'INVALID_DATA')
        assert (error.details == error_str)
