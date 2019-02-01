DEFAULT_AUTHZ_SERVER = 'aus1vigjbbW3KwZJ72p7'
DEFAULT_SCOPE = 'openid email profile'
DEFAULT_REFRESH_SCOPE = 'openid offline_access email profile'


class AuthManager(object):

    def __init__(self, host, client_id, authz_server):
        self.host = host
        self.client_id = client_id
        self.authz_server = authz_server

    def authenticate(self):
        raise NotImplementedError

    def refresh(self):
        raise NotImplementedError


class AuthContext(object):

    def __init__(self, token_type, access_token, expires_in, scope,
                 id_token=None, refresh_token=None):
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
