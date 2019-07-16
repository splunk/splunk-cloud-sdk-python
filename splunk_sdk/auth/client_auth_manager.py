# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from splunk_sdk.auth.auth_manager import AuthManager, AuthContext
from splunk_sdk.auth.idp import IdpClient


class ClientAuthManager(AuthManager):
    """
    Implements the Client Credentials auth flow. Client Credentials is used when an application is authorized to
    make calls on it's own behalf- in other words, there is not a human user associated with the request. For
    more details look to documentation for the identity service.
    """

    def __init__(self, host, client_id, client_secret, scope=""):

        super().__init__(host, client_id)
        self.client_secret = client_secret
        self.scope = scope
        self.app = self._build_app_payload()

    def _build_app_payload(self):
        app = dict()
        app['scope'] = self.scope
        app['client_id'] = self.client_id
        app['client_secret'] = self.client_secret
        return app

    def authenticate(self):
        """Return the payload from idp, all tokens, expiry, etc"""
        data = IdpClient(host=self.host).client(self.app)
        return AuthContext(**data)
