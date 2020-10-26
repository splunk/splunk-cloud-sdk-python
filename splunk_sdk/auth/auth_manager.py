# coding: utf-8

# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import base64
import hashlib
import json
import jwt
import os
import urllib
import time
import uuid
from datetime import datetime, timezone, timedelta
from abc import ABC, abstractmethod
from typing import Optional

from splunk_sdk.common import REQUESTS_HOOK_NAME_RESPONSE

import requests
from requests import Response

DEFAULT_HOST = "auth.scp.splunk.com"
PATH_AUTHN = "/authn"
PATH_AUTHORIZE = "/authorize"
PATH_TOKEN = "/token"
PATH_CSRFTOKEN = "/csrfToken"

HEADERS_DEFAULT = {
    "Accept": "application/json",
    "Content-Type": "application/json"}
HEADERS_URLENCODED = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"}

DEFAULT_SCOPE = "openid email profile"
DEFAULT_REFRESH_SCOPE = "openid offline_access email profile"


class AuthnError(Exception):
    def __init__(self, message: str, response: Response):
        super().__init__(message)
        self._response = response

    @property
    def _response_body(self) -> Optional[dict]:
        if self._response is not None and self._response.text is not None:
            try:
                return self._response.json()
            except Exception:
                return None

    @property
    def server_error_description(self) -> Optional[str]:
        """ The message explaining the error from the server (if any)"""
        if self._response_body is not None:

            # FIXME(dan):
            #   Work around for issue with IAC returning non-consistent keys
            #   There is a bug filed already
            error_desc = self._response_body.get("error_description", None)
            if error_desc is not None:
                return error_desc

            return self._response_body.get("description")

    @property
    def status(self) -> Optional[str]:
        """ The status field from the payload body if supplied"""
        if self._response_body is not None:
            return self._response_body.get("status")

    @property
    def request_id(self) -> Optional[str]:
        """ The unique request ID if supplied by the service"""
        if self._response is not None:
            return self._response.headers.get("x-request-id")


class AuthContext(object):
    """
    TODO DOCS
    The AuthContext class...
    """

    def __init__(self, token_type, access_token, expires_in, scope,
                 id_token=None, refresh_token=None):
        self._token_type = token_type
        self._access_token = access_token
        self._expires_in = expires_in
        self._scope = scope
        self._id_token = id_token
        self._refresh_token = refresh_token
        self._created_at = datetime.now()

    @property
    def token_type(self) -> str:
        return self._token_type

    @token_type.setter
    def token_type(self, token_type: str):
        self._token_type = token_type

    @property
    def access_token(self) -> str:
        return self._access_token

    @access_token.setter
    def access_token(self, access_token: str):
        self._access_token = access_token

    @property
    def expires_in(self) -> int:
        return self._expires_in

    @expires_in.setter
    def expires_in(self, expires_in: int):
        self._expires_in = expires_in

    @property
    def scope(self) -> str:
        return self._scope

    @scope.setter
    def scope(self, scope: str):
        self._scope = scope

    @property
    def id_token(self) -> str:
        return self._id_token

    @id_token.setter
    def id_token(self, id_token: str):
        self._id_token = id_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    @refresh_token.setter
    def refresh_token(self, refresh_token: str):
        self._refresh_token = refresh_token

    def will_expire_within(self, seconds: int = 30):
        if self.expires_in:  # If we don't have an expire time, presume that it never does.
            return (datetime.now() - self._created_at).total_seconds() > self.expires_in - seconds
        else:
            return False


class AuthManager(ABC):
    """
    The AuthManager class is a base class that manages different authentication flows.
    When creating an authorization manager, create a subclass that corresponds to
    the flow that you need for your app.
    """

    def __init__(self, host, client_id, requests_hooks=None):
        self._host = host
        self._client_id = client_id
        self._context = None
        self._requests_hooks = requests_hooks or []

    def _get(self, url, headers=None, params=None):
        response = requests.get(
            url,
            headers=headers or HEADERS_DEFAULT,
            params=params,
            allow_redirects=False,
            hooks={REQUESTS_HOOK_NAME_RESPONSE: self._requests_hooks})
        return response

    # Note: the requests module interprets the data param in an interesting
    # way, if its a dict, it will be url form encoded, if its a string it
    # will be posted in the body
    def _post(self, url, auth=None, headers=None, data=None, cookies=None):
        response = requests.post(
            url,
            auth=auth,
            headers=headers or HEADERS_DEFAULT,
            data=data,
            cookies=cookies,
            hooks={REQUESTS_HOOK_NAME_RESPONSE: self._requests_hooks})
        return response

    def _url(self, path):
        return "https://%s%s" % (self._host, path)

    @staticmethod
    def _parse_querystring(url):
        """Returns dict containing parsed query string params."""
        if url is None:
            return None
        url = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(url.query)
        params = dict(params)
        return params

    def _post_token(self, auth=None, **data):
        """POST ${basePath}/token, expect 200"""
        path = PATH_TOKEN
        response = self._post(
            self._url(path),
            auth=auth,
            headers=HEADERS_URLENCODED,
            data=data)
        if response.status_code != 200:
            raise AuthnError("Unable to post for token", response)
        return response

    @abstractmethod
    def authenticate(self) -> AuthContext:
        """
        Makes the required calls to authorization endpoints and returns an
        `AuthContext` instance to use for subsequent calls to service endpoints.
        :return: The `AuthContext` instance.
        """
        raise NotImplementedError

    @property
    def context(self):
        if self._context is None:
            self._context = self.authenticate()
        if self._context.will_expire_within(seconds=30):
            self._context = self.authenticate()
        return self._context


class ClientAuthManager(AuthManager):
    """
    Implements the Client Credentials auth flow. Client Credentials is used when an application is authorized to
    make calls on it's own behalf- in other words, there is not a human user associated with the request. For
    more details look to documentation for the identity service.
    """

    # TODO: Host can be an optional value since it has a default
    def __init__(self, host, client_id, client_secret, scope="", requests_hooks=None):
        super().__init__(host, client_id, requests_hooks=requests_hooks)
        self._client_secret = client_secret
        self._scope = scope

    def authenticate(self):
        """Authenticate using the "client credentials" flow."""
        if self._client_id is None:
            raise ValueError("missing client_id")
        if self._client_secret is None:
            raise ValueError("missing client_secret")
        if self._scope is None:
            raise ValueError("missing scope")

        data = {"grant_type": "client_credentials", "scope": self._scope}
        auth = (self._client_id, self._client_secret)
        response = self._post_token(auth, **data)
        if response.status_code != 200:
            raise AuthnError("Unable to authenticate. Check credentials.", response)
        return AuthContext(**response.json())


class PKCEAuthManager(AuthManager):
    """
    This subclass of AuthManager handles the PKCE auth flow.  PKCE should be used when an app is acting on behalf
    of a human user. Both the user and the app are authenticating themselves to the system- the user through username
    and password, the app through the client_id and redirect_uri. For more details, see identity service documentation.
    """

    def __init__(self, host, client_id, redirect_uri, username, password, scope=DEFAULT_REFRESH_SCOPE, requests_hooks=None):
        super().__init__(host, client_id, requests_hooks=requests_hooks)
        self._redirect_uri = redirect_uri
        self._username = username
        self._password = password
        self._state = None
        self._scope = scope

    # Note: see https://tools.ietf.org/html/rfc7636#section-4.1
    # code_verifier = a high-entropy cryptographic random STRING using the
    # unreserved characters [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
    # from Section 2.3 of [RFC3986], with a minimum length of 43 characters
    # and a maximum length of 128 characters.
    _SAFE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-._~"

    @staticmethod
    def _create_code_verifier(n):
        """Returns a code verifier of length 'n', where 43 <= n <= 128."""
        assert 43 <= n <= 128, "Code verifier length must be between the values of 43 and 128 inclusive"
        result = bytearray(os.urandom(n))
        result = base64.urlsafe_b64encode(result)
        result = result.rstrip('='.encode('utf-8'))  # strip b64 padding
        return result

    # Note: see https://tools.ietf.org/html/rfc7636#section-4.2
    # code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))
    @staticmethod
    def _create_code_challenge(cv):
        """Returns a code challenge based on the given code verifier."""
        result = hashlib.sha256(cv).digest()
        result = base64.urlsafe_b64encode(result)
        result = result.rstrip('='.encode('utf-8'))  # strip b64 padding
        return result

    def _get_session_token(self, username, password):
        """Returns a one-time session token by authenticating using the
         (extended) "primary" endpoint (/authn)."""
        csrfToken, cookies = self._get_csrf_token()
        if csrfToken is None:
            return None
        result = self._authenticate_user(username, password, csrfToken, cookies)
        if result is None:
            return None
        return result.get("sessionToken", None)

    def _get_csrf_token(self):
        """Returns a CSRF token to be passed into /authn"""
        response = self._get(self._url(PATH_CSRFTOKEN))
        if response.status_code != 200:
            raise AuthnError("Authentication failed.", response)
        csrfTokenCookie = self._get_cookie(response.cookies, "csrf")
        if csrfTokenCookie is None:
            raise AuthnError("no CSRF token from /csrfToken", response)
        return csrfTokenCookie.value, response.cookies

    def _get_cookie(self, cookies, name):
        """Returns the specified cookie"""
        for cookie in cookies:
            if cookie.name == name:
                return cookie
        return None

    def _authenticate_user(self, username, password, csrfToken, cookies):
        """Authenticate using the (extended) "primary" method."""
        data = {"username": username, "password": password, "csrfToken": csrfToken}
        response = self._post(self._url(PATH_AUTHN), data=json.dumps(data), cookies=cookies)
        if response.status_code != 200:
            raise AuthnError("Authentication failed.", response)
        result = response.json()
        status = result.get("status", None)
        if status is None:
            raise AuthnError("no response status from /authn", response)
        if status != "SUCCESS":  # eg: LOCKED_OUT
            raise AuthnError("authentication failed: %s" % status, response)
        return result

    def _get_authorization_code(self, **params):
        """GET ${basePath}/authorize, expect 302 (redirect)"""
        path = PATH_AUTHORIZE
        response = self._get(self._url(path), params=params)
        if response.status_code != 302:
            raise AuthnError("Unable to obtain authorization code. Check client_id, redirect_uri, and scope", response)
        location = response.headers.get("location", None)
        if location is None:
            raise AuthnError("Unable to obtain authorization code. Check client_id, redirect_uri, and scope", response)
        params = self._parse_querystring(location)
        value = params.get("code", None)
        if value is None:
            raise AuthnError("Unable to obtain authorization code. Check client_id, redirect_uri, and scope", response)

        assert value and len(value) == 1
        return value[0]

    def validate(self):
        if self._client_id is None:
            raise ValueError("missing client_id")
        if self._redirect_uri is None:
            raise ValueError("missing redirect_uri")

    def authenticate(self):
        """Authenticate with the (extended) "authorization code with pkce"
         flow."""

        self.validate()

        # retrieve one time session token
        session_token = self._get_session_token(self._username, self._password)

        cv = self._create_code_verifier(50)
        cc = self._create_code_challenge(cv)

        # request authorization code
        auth_code = self._get_authorization_code(
            client_id=self._client_id,
            code_challenge=cc.decode("utf-8"),
            code_challenge_method="S256",
            nonce="none",
            redirect_uri=self._redirect_uri,
            response_type="code",
            scope=self._scope,
            session_token=session_token,
            state=self._state or str(time.time())
        )

        # exchange authorization code for token(s)
        response = self._post_token(
            client_id=self._client_id,
            code=auth_code,
            code_verifier=cv,
            grant_type="authorization_code",
            redirect_uri=self._redirect_uri
        )
        if response.status_code != 200:
            raise AuthnError("Unable to exchange authorization code for a token", response)
        return AuthContext(**response.json())


class TokenAuthManager(AuthManager):
    """
    TokenAuthManager is used for when you have a token that is obtained from a source other than the SDK. When the
    token expires, there is no way to refresh it.
    """

    def __init__(self, access_token, token_type='Bearer', expires_in=None,
                 scope=None, id_token=None, refresh_token=None, requests_hooks=None):
        super().__init__(None, None, requests_hooks=requests_hooks)
        self.access_token = access_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.scope = scope
        self.id_token = id_token
        self.refresh_token = refresh_token
        self._context = AuthContext(token_type=self.token_type,
                                    access_token=self.access_token,
                                    expires_in=self.expires_in, scope=self.scope,
                                    id_token=self.id_token,
                                    refresh_token=self.refresh_token)

    def authenticate(self) -> AuthContext:
        return self._context


class RefreshTokenAuthManager(AuthManager):
    def __init__(self, client_id, refresh_token, host, scope="openid", requests_hooks=None):
        super().__init__(host, client_id, requests_hooks=requests_hooks)
        self._refresh_token = refresh_token
        self._scope = scope

    def authenticate(self):
        """Authenticate using the OAuth refresh_token grant type."""
        client_id = self._client_id
        if client_id is None:
            raise ValueError("missing client_id")
        data = {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": self._refresh_token,
            "scope": self._scope
        }

        response = self._post_token(**data)
        return AuthContext(**response.json())


class ServicePrincipalAuthManager(AuthManager):
    def __init__(self, host, principal_name, key, kid, algorithm="ES256", **kwargs):
        """
        Creates an AuthManager that uses Service Principals to authenticate.

        principal_name is the principal_name of the authenticating service principal
        key is the PEM formatted private key registered with the service principal
        kid is the key_id of `key`
        algorithm is the algorithm that generated `key`
        """
        super().__init__(host=host, client_id=None, **kwargs)
        self._principal_name = principal_name
        self._key = key
        self._kid = kid
        self._algorithm = algorithm

    def authenticate(self):
        """Authenticate using the "client assertion" flow."""
        if not self._principal_name:
            raise ValueError("missing principal_name")
        if not self._key:
            raise ValueError("missing key")
        if not self._kid:
            raise ValueError("missing kid")
        if not self._algorithm:
            raise ValueError("missing algorithm")

        # Client assertion expires in 10 minutes
        ten_minutes_from_now = datetime.now(timezone.utc) + timedelta(minutes=10)
        jwt_payload = {"sub": self._principal_name, "iss": self._principal_name, "jti": str(uuid.uuid4()),
                       "exp": int(ten_minutes_from_now.timestamp()), "aud": [self._url(PATH_TOKEN)]}

        client_assertion = jwt.encode(payload=jwt_payload, key=self._key, algorithm=self._algorithm,
                                      headers={"kid": self._kid})

        data = {"grant_type": "client_credentials", "client_assertion": client_assertion.decode("utf-8"),
                "client_assertion_type": "urn:ietf:params:oauth:client-assertion-type:jwt-bearer"}

        response = self._post_token(**data)
        if response.status_code != 200:
            raise AuthnError("Unable to authenticate. Check credentials.", response)
        return AuthContext(**response.json())
