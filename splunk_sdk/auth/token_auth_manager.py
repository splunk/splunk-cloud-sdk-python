from splunk_sdk.auth.auth_manager import AuthContext


class TokenAuthManager(object):
    """
    TokenAuthManager is used for when you have a token that is obtained from a source other than the SDK. When the
    token expires, there is no way to refresh it.
    """

    def __init__(self, access_token, token_type='Bearer', expires_in=None,
                 scope=None, id_token=None, refresh_token=None):
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.id_token = id_token
        self.refresh_token = refresh_token

    def authenticate(self):
        return AuthContext(token_type=self.token_type,
                           access_token=self.access_token,
                           expires_in=self.expires_in, scope=self.scope,
                           id_token=self.id_token,
                           refresh_token=self.refresh_token)
