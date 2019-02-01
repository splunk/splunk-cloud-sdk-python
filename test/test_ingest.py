# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import pytest
from splunk_sdk.ingest.client import Ingest
from splunk_sdk.ingest.results import PostIngestResponse

from splunk_sdk.base_client import HTTPError

from test.fixtures import get_test_client as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events(test_client):
    ingest = Ingest(test_client)
    event_data = {'body': 'event1',
                  'host': 'host1',
                  'source': 'sourcename',
                  'sourcetype': 'sourcetype',
                  'timestamp': 1533671808138,
                  'nanos': 0,
                  'attributes': {'data': 'data1'}
                  }
    event_list = [event_data, event_data]
    event_response = ingest.post_events(event_list)

    assert (isinstance(event_response, PostIngestResponse))
    assert (event_response.message == 'Success')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_metrics(test_client):
    ingest = Ingest(test_client)
    metrics = {'Name': "CPU", 'Value': 5.5,
               'Dimensions': {'data': 'data1'}, 'Unit': 'data3'}
    metrics_list = [metrics]
    metrics_data = {'body': metrics_list,
                    'host': 'host1',
                    'source': 'source1',
                    'sourcetype': 'sourcetype',
                    'timestamp': 1533671808138,
                    'nanos': 0,
                    'attributes': {'DefaultType': 'data1',
                                   'DefaultDimensions': {'dimension':
                                                         'dimensionValue'}}
                    }
    metrics_data_list = [metrics_data]
    metrics_response = ingest.post_metrics(metrics_data_list)

    assert (isinstance(metrics_response, PostIngestResponse))
    assert (metrics_response.message == 'Success')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events_body_empty(test_client):
    ingest = Ingest(test_client)
    event_data = {}
    event_list = [event_data]
    error_str = 'Event body cannot be empty'
    try:
        ingest.post_events(event_list)
    except HTTPError as error:
        assert (error.details['failedEvents'][0]['message'] == error_str)
        assert (error.httpStatusCode == 400)
        assert (error.code == 'INVALID_DATA')
        assert (error.message == 'Invalid data format')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events_bad_request(test_client):
    ingest = Ingest(test_client)
    event_list = []
    error_str = 'Empty array was provided as input'
    try:
        ingest.post_events(event_list)
    except HTTPError as error:
        assert (error.httpStatusCode == 400)
        assert (error.code == 'INVALID_DATA')
        assert (error.message == 'Invalid data format')
        assert (error.details == error_str)
