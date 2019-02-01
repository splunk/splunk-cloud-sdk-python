import pytest
from splunk_sdk.ingest.client import Ingest
from splunk_sdk.ingest.results import PostIngestResponse
from splunk_sdk.ingest.results import EventData
from splunk_sdk.ingest.results import Attributes
from splunk_sdk.ingest.results import Metric
from splunk_sdk.ingest.results import MetricEvent
from splunk_sdk.ingest.results import MetricAttribute


from splunk_sdk.base_client import HTTPError

from test.fixtures import get_test_client as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events(test_client):
    ingest = Ingest(test_client)

    event_data = EventData('event1', 'host1', 'source1', 'sourcetype1',
                           Attributes({'data': 'data1'}), None, 1533671808138)
    event_list = [event_data]
    event_response = ingest.post_events(event_list)

    assert (isinstance(event_response, PostIngestResponse))
    assert (event_response.message == 'Success')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_metrics(test_client):
    ingest = Ingest(test_client)

    metrics = Metric('CPU', 5.5, {'data': 'data1'}, 'units')
    metrics_list = [metrics]
    met_attr = MetricAttribute('data1', {'dimension': 'dValue'}, 'data2')
    metrics_data = MetricEvent(metrics_list, 'host1', 'source1',
                               'sourcetype1', 1533671808138, None,
                               met_attr, None)
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
