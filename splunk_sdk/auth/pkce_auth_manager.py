from splunk_sdk.auth.okta import pkce as pkce_flow

KIND = 'pkce'
SCOPE = 'openid offline_access email profile'


class PKCEAuthManager(object):

    def __init__(self, host, client_id, redirect_uri, server, username,
                 password):
        self.host = host

        from splunk_sdk.auth.okta import HOST  # NOQA
        HOST = host  # NOQA

        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.server = server
        self.username = username
        self.password = password

    def _build_app_payload(self):
        app = dict()
        app['kind'] = KIND
        app['scope'] = SCOPE
        app['client_id'] = self.client_id
        app['redirect_uri'] = self.redirect_uri
        app['server'] = self.server
        return app

    def authenticate(self):
        """Return the payload from okta, all tokens, expiry, etc"""
        app = self._build_app_payload()
        data = pkce_flow(app, self.username, self.password)
        return AuthContext(**data)


class AuthContext(object):

    def __init__(self, token_type, access_token, expires_in, scope, id_token,
                 refresh_token):
        self._token_type = token_type
        self._access_token = access_token
        self._expires_in = expires_in
        self._scope = scope
        self._id_token = id_token
        self._refresh_token = refresh_token

    @property
    def token_type(self):
        return self._token_type

    @token_type.setter
    def token_type(self, token_type):
        self._token_type = token_type

    @property
    def access_token(self):
        return self._access_token

    @access_token.setter
    def access_token(self, access_token):
        self._access_token = access_token

    @property
    def expires_in(self):
        return self._expires_in

    @expires_in.setter
    def expires_in(self, expires_in):
        self._expires_in = expires_in

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope):
        self._scope = scope

    @property
    def id_token(self):
        return self._id_token

    @id_token.setter
    def id_token(self, id_token):
        self._id_token = id_token

    @property
    def refresh_token(self):
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token):
        self._refresh_token = refresh_token
