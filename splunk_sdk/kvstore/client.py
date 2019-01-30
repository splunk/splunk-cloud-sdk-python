from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.kvstore.results import Health

KVSTORE_HEALTH = "/kvstore/v1beta1/ping"


class KVStore(BaseService):

    def __init__(self, base_client, cluster='api'):
        super().__init__(base_client, cluster=cluster)

    def get_health_status(self):
        url = self.base_client.build_url(
            KVSTORE_HEALTH)
        response = self.base_client.get(url)
        return handle_response(response, Health)
