# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService

from splunk_sdk.gateway.results import Spec

GATEWAY_SPECS = '/urls.json'


class Gateway(BaseService):
    """The Gateway class TODO DOCS."""

    def __init__(self, base_client):
        super().__init__(base_client)

    def list_specs(self):
        """Returns a raw response."""
        url = self.base_client.build_url(GATEWAY_SPECS, omit_tenant=True)
        response = self.base_client.get(url)
        return handle_response(response, Spec, key='urls')

    def get_service_names(self):
        """Returns all Splunk Cloud service names."""
        return [spec.name for spec in self.list_specs()]

    def get_spec_url(self, name, link='yaml3'):
        """Return the API specification URL for a given service name."""
        specs = self.list_specs()
        for s in specs:
            if name == s.name:
                return self.base_client.build_url(s.links[link],
                                                  omit_tenant=True)

    def get_spec(self, name, link='yaml3'):
        """Downloads the API specification file for a given service name."""
        # TODO(dan): need to set accept header
        return self.base_client.get(self.get_spec_url(name, link=link))
