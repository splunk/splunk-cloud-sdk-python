from sdk.base_client import handle_response
from sdk.base_service import BaseService

from sdk.gateway.results import Spec

GATEWAY_SPECS = '/urls.json'

# API cluster
API_ACTION_SERVICE = "Action Service"
API_SEARCH_SERVICE = "Splunk Search Service"
API_CATALOG_SERVICE = "Metadata Catalog"
API_IDENTITY_SERVICE = "Identity and Access Control"
API_KVSTORE_SERVICE = "KV Store API"
API_METERING_SERVICE = "Metering Service API"
API_STREAM_SERVICE = "Data Stream Processing REST API"

# TODO(dan): This is duplicated due to a test route
API_INGEST_SERVICE = "Ingest API"
API_COLLECT_SERVICE = "Collect Service"
API_FORWARDER_SERVICE = "Splunk Forwarder Service"

# APP cluster
APP_KEYSTONE_CONFIG_SERVICE = "Keystone's Configuration Management API"
APP_KEYSTONE_SYMBOLICATOR_SERVICE = "Keystone's symbolicator API"
APP_KEYSTONE_ADMIN_SERVICE = "Keystone's admin API"
APP_ML_SERVICE = "SSC Machine Learning Service"
APP_ML_DATA_SERVICE = "Data service for SSC Machine Learning Service"
APP_REGISTRY_SERVICE = "App Registry"
APP_CONTENT_STORE_SERVICE = "Content Store"


class Gateway(BaseService):

    def __init__(self, base_client, cluster='api'):
        super().__init__(base_client, cluster=cluster)

    def list_specs(self):
        """Returns raw response."""
        url = self.base_client.build_url(GATEWAY_SPECS)
        response = self.base_client.get(url)
        return handle_response(response, Spec, key='urls')

    def get_spec(self, name, link='yaml'):
        """Return the spec file for a particular service"""
        specs = self.list_specs()
        for s in specs:
            if name == s.name:
                return self.base_client.build_url(s.links[link])

    def download_spec(self, name, link='yaml'):
        """Download the spec file"""
        # TODO(dan): need to set accept header
        return self.base_client.get(self.get_spec(name, link=link))
