from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService

from splunk_sdk.ingest.results import Event

import json

INGEST = "/ingest/v1beta2/"


class Ingest(BaseService):

    def __init__(self, base_client, cluster='api'):
        super().__init__(base_client, cluster=cluster)

    def post_events(self, arr):
        url = self.base_client.build_url(
            INGEST + "events"
        )
        print('url' + url)
        jsondata = json.dumps(arr)
        print(jsondata)
        response = self.base_client.post(url, json=jsondata)
        return handle_response(response, Event)
