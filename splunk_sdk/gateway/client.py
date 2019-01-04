from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService

from splunk_sdk.gateway.results import Spec

GATEWAY_SPECS = '/urls.json'


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
