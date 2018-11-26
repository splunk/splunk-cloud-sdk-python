from sdk.base_client import handle_response
from sdk.base_service import BaseService
from sdk.kvstore.results import Health

VERSION = "v1beta1"
KVSTORE_HEALTH = "/{tenant}/kvstore/{version}/ping"


class KVStore(BaseService):

    def __init__(self, base_client, cluster='api'):
        super().__init__(base_client, cluster=cluster)

    def get_health_status(self):
        url = self.base_client.build_url(
            KVSTORE_HEALTH, tenant=self.base_client.get_tenant(),
            version=VERSION)
        response = self.base_client.get(url)
        return handle_response(response, Health)
