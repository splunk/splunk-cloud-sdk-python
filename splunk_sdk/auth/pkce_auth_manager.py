# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from splunk_sdk.auth.auth_manager import AuthManager, AuthContext, \
    DEFAULT_REFRESH_SCOPE
from splunk_sdk.auth.idp import IdpClient


class PKCEAuthManager(AuthManager):
    """
    This subclass of AuthManager handles the PKCE auth flow.  PKCE should be used when an app is acting on behalf
    of a human user. Both the user and the app are authenticating themselves to the system- the user through username
    and password, the app through the client_id and redirect_uri. For more details, see identity service documentation.
    """

    def __init__(self, host, client_id, redirect_uri, username, password):
        super().__init__(host, client_id)
        self.redirect_uri = redirect_uri
        self.username = username
        self.password = password
        self.app = self._build_app_payload()

    def _build_app_payload(self):
        app = dict()
        app['scope'] = DEFAULT_REFRESH_SCOPE
        app['client_id'] = self.client_id
        app['redirect_uri'] = self.redirect_uri
        return app

    def authenticate(self):
        """Return the payload from IDP, all tokens, expiry, etc"""
        data = IdpClient(host=self.host).pkce(self.app, self.username,
                                              self.password)
        return AuthContext(**data)
