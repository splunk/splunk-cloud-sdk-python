import pytest
from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.ingest.client import Ingest
from splunk_sdk.ingest.results import Event


@pytest.mark.usefixtures("test_client")  # NOQA
def test_post_events(test_client):
    ingest = Ingest(test_client)
    eventdata = {'host': 'host1',
                 'body': 'event1',
                 'source': 'source1',
                 'sourcetype': 'sourcetype1',
                 'timestamp': '1533671808138',
                 'nanos': 0,
                 'attributes': None}
    arr = [eventdata, eventdata]
    event = ingest.post_events(arr)
    print("status", event)
