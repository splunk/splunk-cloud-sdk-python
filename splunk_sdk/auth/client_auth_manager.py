from splunk_sdk.auth.auth_manager import AuthManager, AuthContext
from splunk_sdk.auth.idp import IdpClient


class ClientAuthManager(AuthManager):

    def __init__(self, host, client_id, client_secret, server,
                 scope=""):

        super().__init__(host, client_id, server)
        self.client_secret = client_secret
        self.scope = scope
        self.app = self._build_app_payload()

    def _build_app_payload(self):
        app = dict()
        app['scope'] = self.scope
        app['client_id'] = self.client_id
        app['client_secret'] = self.client_secret
        app['server'] = self.server
        return app

    def authenticate(self):
        """Return the payload from okta, all tokens, expiry, etc"""
        data = IdpClient(host=self.host).client(self.app)
        return AuthContext(**data)
