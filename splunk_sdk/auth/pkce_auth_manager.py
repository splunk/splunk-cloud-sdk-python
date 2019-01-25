# from splunk_sdk.auth.okta import pkce as pkce_flow

from splunk_sdk.auth.auth_manager import AuthManager, AuthContext, \
    DEFAULT_REFRESH_SCOPE
from splunk_sdk.auth.okta import OktaClient


class PKCEAuthManager(AuthManager):

    def __init__(self, host, client_id, redirect_uri, server, username,
                 password):
        super().__init__(host, client_id, server)
        self.redirect_uri = redirect_uri
        self.username = username
        self.password = password
        self.app = self._build_app_payload()

    def _build_app_payload(self):
        app = dict()
        app['scope'] = DEFAULT_REFRESH_SCOPE
        app['client_id'] = self.client_id
        app['redirect_uri'] = self.redirect_uri
        app['server'] = self.server
        return app

    def authenticate(self):
        """Return the payload from okta, all tokens, expiry, etc"""
        data = OktaClient(host=self.host).pkce(self.app, self.username,
                                               self.password)
        return AuthContext(**data)
