# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# OAuth 2.0 authentication flows
#
#   Authorization code with PKCE (pkce) -- known/trusted app
#      client_id + code challenge + redirect_uri + username + password =>
#          access, id_token, refresh_token[*]
#
#   Client credentials (client) -- private service
#      client_id + client_secret + custom scope =>
#          access
#
#   * refresh_token is available if the offline_access scope is requested.
#
# Note: code, pkce flow is normally browser based and involve
# redirection. The implementation below make use of an extension to the
# standard OIDC flows that allows client code to first authenticate with user
# credentials against the "primary" endpoint (/authn) and retrieve a one
# time session token, which when used with these flows, will result in the
# requested grants being returned directly in the redirect url.


import base64
import hashlib
import json
import os
import time
import urllib.parse
import urllib
import logging
import requests

DEFAULT_HOST = "auth.scp.splunk.com"
PATH_AUTHN = "/authn"
PATH_AUTHORIZE = "/authorize"
PATH_TOKEN = "/token"

HEADERS_DEFAULT = {
    "Accept": "application/json",
    "Content-Type": "application/json"}
HEADERS_URLENCODED = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"}

logger = logging.getLogger(__name__)


class AuthnError(Exception):
    pass


class IdpClient(object):
    """
    This class is an http client for authorization. It is an implementation specific for the SDK, and should not
    be used directly by clients of the SDK. For standalone authentication, use AuthManager and it's subclasses.
    """

    def __init__(self, scheme='https', host=DEFAULT_HOST):
        self.scheme = scheme
        self.host = host

    def _get(self, url, headers=None, params=None):
        response = requests.get(
            url,
            headers=headers or HEADERS_DEFAULT,
            params=params,
            allow_redirects=False)
        return response

    # Note: the requests module interprets the data param in an interesting
    # way, if its a dict, it will be url form encoded, if its a string it
    # will be posted in the body
    def _post(self, url, auth=None, headers=None, data=None):
        response = requests.post(
            url,
            auth=auth,
            headers=headers or HEADERS_DEFAULT,
            data=data)
        return response

    def _url(self, path):
        return "%s://%s%s" % (self.scheme, self.host, path)

    def _get_authorize(self, params):
        """GET ${basePath}/authorize, expect 302 (redirect)"""
        path = PATH_AUTHORIZE
        response = self._get(self._url(path), params=params)
        if response.status_code != 302:
            response.raise_for_status()
        return response

    def _post_token(self, data, auth=None):
        """POST ${basePath}/token, expect 200"""
        path = PATH_TOKEN
        response = self._post(
            self._url(path),
            auth=auth,
            headers=HEADERS_URLENCODED,
            data=data)
        if response.status_code != 200:
            response.raise_for_status()
        return response

    @staticmethod
    def _parse_qs(url):
        """Returns dict containing parsed query string params."""
        if url is None:
            return None
        url = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(url.query)
        params = dict(params)
        return params

    @staticmethod
    def _parse_frag(url):
        """Returns dict containing parsed url fragment params."""
        if url is None:
            return None
        url = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qsl(url.fragment)
        params = dict(params)
        return params

    def _get_session_token(self, username, password):
        """Returns a one-time session token by authenticating using the
         (extended) "primary" endpoint (/authn)."""
        result = self._primary(username, password)
        if result is None:
            return None
        return result.get("sessionToken", None)

    def client(self, app):
        """Authenticate using the "client credentials" flow."""
        client_id = app.get("client_id", None)
        if client_id is None:
            raise ValueError("missing client_id")
        client_secret = app.get("client_secret", None)
        if client_secret is None:
            raise ValueError("missing client_secret")
        scope = app.get("scope", None)
        if scope is None:
            raise ValueError("missing scope")

        data = {"grant_type": "client_credentials", "scope": scope}
        auth = (client_id, client_secret)
        response = self._post_token(data, auth=auth)
        return response.json()

    # Note: see https://tools.ietf.org/html/rfc7636#section-4.1
    # code_verifier = a high-entropy cryptographic random STRING using the
    # unreserved characters [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
    # from Section 2.3 of [RFC3986], with a minimum length of 43 characters
    # and a maximum length of 128 characters.
    SAFE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-._~"

    @staticmethod
    def _create_code_verifier(n):
        """Returns a code verifier of length 'n', where 43 <= n <= 128."""
        assert n >= 43 and n <= 128
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

    def pkce(self, app, username, password, state=None):
        """Authenticate with the (extended) "authorization code with pkce"
         flow."""
        client_id = app.get("client_id", None)
        if client_id is None:
            raise ValueError("missing client_id")
        redirect_uri = app.get("redirect_uri", None)
        if redirect_uri is None:
            raise ValueError("missing redirect_uri")
        scope = app.get("scope", "openid")

        # retrieve one time session token
        session_token = self._get_session_token(username, password)
        if session_token is None:
            return None

        cv = self._create_code_verifier(50)
        cc = self._create_code_challenge(cv)

        # request authorization code
        params = {
            "client_id": client_id,
            "code_challenge": cc.decode("utf-8"),
            "code_challenge_method": "S256",
            "nonce": "none",
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "session_token": session_token,
            "state": state or str(time.time())}
        response = self._get_authorize(params)

        # retrieve the authorization code from the redirect url query string
        location = response.headers.get("location", None)
        if location is None:
            return None
        params = self._parse_qs(location)
        value = params.get("code", None)
        assert value and len(value) == 1
        value = value[0]

        # exchange authorization code for token(s)
        data = {
            "client_id": client_id,
            "code": value,
            "code_verifier": cv,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri}
        response = self._post_token(data)
        return response.json()

    def _primary(self, username, password):
        """Authenticate using the (extended) "primary" method."""
        data = {"username": username, "password": password}
        path = PATH_AUTHN
        response = self._post(self._url(path), data=json.dumps(data))
        if response.status_code != 200:
            response.raise_for_status()
        result = response.json()
        status = result.get("status", None)
        if status is None:
            raise AuthnError("no response status from /authn")
        if status != "SUCCESS":  # eg: LOCKED_OUT
            raise AuthnError("authentication failed: %s" % status)
        return result

    def refresh(self, app, refresh_token):
        """Authenticate using the OAuth refresh_token grant type."""
        client_id = app.get("client_id", None)
        if client_id is None:
            raise ValueError("missing client_id")
        scope = app.get("scope", "openid")
        data = {
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": scope}
        response = self._post_token(data)
        return response.json()
