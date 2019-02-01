from splunk_sdk.auth.auth_manager import AuthManager, AuthContext, \
    DEFAULT_AUTHZ_SERVER, DEFAULT_REFRESH_SCOPE
from splunk_sdk.auth.idp import IdpClient


class PKCEAuthManager(AuthManager):

    def __init__(self, host, client_id, redirect_uri, username,
                 password, authz_server=DEFAULT_AUTHZ_SERVER):
        super().__init__(host, client_id, authz_server)
        self.redirect_uri = redirect_uri
        self.username = username
        self.password = password
        self.app = self._build_app_payload()

    def _build_app_payload(self):
        app = dict()
        app['scope'] = DEFAULT_REFRESH_SCOPE
        app['client_id'] = self.client_id
        app['redirect_uri'] = self.redirect_uri
        app['server'] = self.authz_server
        return app

    def authenticate(self):
        """Return the payload from okta, all tokens, expiry, etc"""
        data = IdpClient(host=self.host).pkce(self.app, self.username,
                                              self.password)
        return AuthContext(**data)
