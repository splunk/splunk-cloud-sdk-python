from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService

from splunk_sdk.ingest.results import PostIngestResponse
import json

INGEST = "/ingest/v1beta2/"


class Ingest(BaseService):

    def __init__(self, base_client, cluster='api'):
        super().__init__(base_client, cluster=cluster)

    def post_events(self, event_data):
        url = self.base_client.build_url(
            INGEST + "events"
        )

        response = self.base_client.post(url, data=json.dumps(event_data))
        return handle_response(response, PostIngestResponse)

    def post_metrics(self, metric_data):
        url = self.base_client.build_url(
            INGEST + "metrics"
        )
        response = self.base_client.post(url, data=json.dumps(metric_data))
        return handle_response(response, PostIngestResponse)
