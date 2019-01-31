# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

# Okta OAuth 2.0 authentication flows
#
#   Authorization code (code) -- not recommended, prefer pkce
#      client_id + client_secret + redirect_uri + username + password =>
#          access, id_token, refresh_token[*]
#
#   Authorization code with PKCE (pkce) -- known/trusted app
#      client_id + code challenge + redirect_uri + username + password =>
#          access, id_token, refresh_token[*]
#
#   Client credentials (client) -- private service
#      client_id + client_secret + custom scope =>
#          access
#
#   Implicit flow (implicit) -- unknown/untrusted app
#      client_id + redirect_uri + username + password =>
#          access, id_token
#
#   Resource owner password (ropw) -- not recomended, prefer pkce
#      client_id + client_secret + username + password =>
#          access, id_token, refresh_token[*]
#
#   * reffresh_token is available if enabled in app config on Okta and if
#     the offline_access scope is requested.
#
# Note: code, pkce and implicit flows are normally browser based and involve
# redirection. The implementation below make use of an Okta extension to the
# standard OIDC flows that allows client code to first authenticate with user
# credentials against the Okta "primary" endpoint (/authn) and retrieve a one
# time session token, which when used with these flows, will result in the
# requested grants being returned directly in the redirect url.
#
# todo: test flows with mfa

import base64
import hashlib
import json
import os
import sys
import time
import urllib.parse
import urllib
import requests

HOST = "splunk-ciam.okta.com:443"
PATH_AUTHN = "/api/v1/authn"
PATH_AUTHORIZE = "/oauth2/%s/v1/authorize"
PATH_KEYS = "/oauth2/%s/v1/keys"
PATH_TOKEN = "/oauth2/%s/v1/token"

HEADERS_DEFAULT = {
    "Accept": "application/json",
    "Content-Type": "application/json"}
HEADERS_URLENCODED = {
    "Accept": "application/json",
    "Content-Type": "application/x-www-form-urlencoded"}

VERBOSE = False


class AuthnError(Exception):
    pass


def _printj(value):
    try:
        json.dump(value, sys.stdout, indent=4, sort_keys=True)
    except TypeError as e:
        print(e)

    print()  # CR


def _printv(response):
    print("%d %s" % (response.status_code, response.reason))
    for k in sorted(response.headers.keys()):
        v = response.headers[k]
        print("%s: %s" % (k, v))
    try:
        _printj(response.json())
    except Exception:
        print(response.text)
    print()


def _get(url, headers=None, params=None):
    if VERBOSE:
        print("GET %s" % url)
        if params:
            _printj(params)
        if headers:
            _printj(headers)
        print("---")
    response = requests.get(
        url,
        headers=headers or HEADERS_DEFAULT,
        params=params,
        allow_redirects=False)
    if VERBOSE:
        _printv(response)
    return response


# note: the requests module interprets the data param in an interesting way,
# if its a dict, it will be url form encoded, if its a string it will be
# posted in the body
def _post(url, auth=None, headers=None, data=None):
    if VERBOSE:
        print("POST %s" % url)
        if headers:
            _printj(headers)
        if data:
            _printj(data)
        print("---")
    response = requests.post(
        url,
        auth=auth,
        headers=headers or HEADERS_DEFAULT,
        data=data)
    if VERBOSE:
        _printv(response)
    return response


def _url(path):
    return "https://%s%s" % (HOST, path)


# GET ${basePath}/authorize, expect 302 (redirect)
def _get_authorize(params, server=None):
    server = server or "default"
    path = PATH_AUTHORIZE % server
    response = _get(_url(path), params=params)
    if response.status_code != 302:
        response.raise_for_status()
    return response


# POST ${basePath}/token, expect 200
def _post_token(data, auth=None, server=None):
    server = server or "default"
    path = PATH_TOKEN % server
    response = _post(
        _url(path),
        auth=auth,
        headers=HEADERS_URLENCODED,
        data=data)
    if response.status_code != 200:
        response.raise_for_status()
    return response


# Returns dict containing parsed query string params.
def _parse_qs(url):
    if url is None:
        return None
    url = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qs(url.query)
    params = dict(params)
    return params


# Returns dict containing parsed url fragment params.
def _parse_frag(url):
    if url is None:
        return None
    url = urllib.parse.urlparse(url)
    params = urllib.parse.parse_qsl(url.fragment)
    params = dict(params)
    return params


# Returns a one-time session token by authenticating using the Okta "primary"
# endpoint (/authn).
def _get_session_token(username, password):
    result = primary(username, password)
    if result is None:
        return None
    return result.get("sessionToken", None)


# Reutrns the public key(s) currently associated with the given client_id.
# They keys are returned as a map from 'kid' (key id) to the key object.
#
# Note: To save the network round trip, your app should cache the jwks_uri
# response locally. The standard HTTP caching headers are used and should be
# respected (per Okta).
def get_keys(client_id, server=None):
    server = server or "default"
    params = {"client_id": client_id}
    path = PATH_KEYS % server
    response = _get(_url(path), params=params)
    if response.status_code != 200:
        response.raise_for_status()
    body = response.json()
    result = {}
    for key in body.get("keys", []):
        kid = key.get("kid", None)
        if kid is None:
            continue  # ignore
        result[kid] = key
    return result


# Authenticate using the "client credentials" flow.
def client(app):
    client_id = app.get("client_id", None)
    if client_id is None:
        raise ValueError("missing client_id")
    client_secret = app.get("client_secret", None)
    if client_secret is None:
        raise ValueError("missing client_secret")
    scope = app.get("scope", None)
    if scope is None:
        raise ValueError("missing scope")
    server = app.get("server", "default")

    data = {"grant_type": "client_credentials", "scope": scope}
    auth = (client_id, client_secret)
    response = _post_token(data, auth=auth, server=server)
    return response.json()


# Authenticate using the "authorization code" flow.
def code(app, username, password, state=None):
    client_id = app.get("client_id", None)
    if client_id is None:
        raise ValueError("missing client_id")
    client_secret = app.get("client_secret", None)
    if client_secret is None:
        raise ValueError("missing client_secret")
    redirect_uri = app.get("redirect_uri", None)
    if redirect_uri is None:
        raise ValueError("missing redirect_uri")
    scope = app.get("scope", "openid")
    server = app.get("server", "default")

    # retrieve one time session token
    session_token = _get_session_token(username, password)
    if session_token is None:
        return None

    # request authorization code
    params = {
        "client_id": client_id,
        "nonce": "none",
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "sessionToken": session_token,
        "state": state or str(time.time())}
    response = _get_authorize(params, server=server)

    # retrieve the authorization code from the redirect url query string
    location = response.headers.get("Location", None)
    params = _parse_qs(location)
    value = params.get("code", None)
    assert value and len(value) == 1
    value = value[0]

    # exchange authorizataion code for token(s)
    data = {
        "code": value,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri}
    auth = (client_id, client_secret)
    response = _post_token(data, auth=auth, server=server)
    return response.json()


# Authenticate using the (extended) "implicit" flow.
def implicit(app, username, password, state=None):
    client_id = app.get("client_id", None)
    if client_id is None:
        raise ValueError("missing client_id")
    redirect_uri = app.get("redirect_uri", None)
    if redirect_uri is None:
        raise ValueError("missing redirect_uri")
    scope = app.get("scope", "openid")
    server = app.get("server", "default")

    # retrieve one time session token
    session_token = _get_session_token(username, password)
    if session_token is None:
        return None

    # this endpoint generally initiates a browser-based authentication flow,
    # but when using a session token, the requested grants and  metadata are
    # returned directly in the URL of the response Location header.
    # request authorization code
    params = {
        "client_id": client_id,
        "nonce": "none",
        "redirect_uri": redirect_uri,
        "response_type": "token id_token",
        "scope": scope,
        "sessionToken": session_token,
        "state": state or str(time.time())}
    response = _get_authorize(params, server=server)

    # retrieve token(s) from the redirect url fragment
    location = response.headers.get("Location", None)
    return _parse_frag(location)


# Returns a code verifier of length 'n', where 43 <= n <= 128.
# see: https://tools.ietf.org/html/rfc7636#section-4.1
# code_verifier = a high-entropy cryptographic random STRING using the
# unreserved characters [A-Z] / [a-z] / [0-9] / "-" / "." / "_" / "~"
# from Section 2.3 of [RFC3986], with a minimum length of 43 characters
# and a maximum length of 128 characters.
SAFE = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-._~"


def _create_code_verifier(n):
    assert n >= 43 and n <= 128
    # nsafe = len(SAFE)
    result = bytearray(os.urandom(n))
    # for i, b in enumerate(result):
    #     b = b % nsafe
    #     result[i] = SAFE[b]
    result = base64.urlsafe_b64encode(result)
    result = result.rstrip('='.encode('utf-8'))  # strip b64 padding
    return result


# Returns a code challenge based on the given code verifier.
# see: https://tools.ietf.org/html/rfc7636#section-4.2
# code_challenge = BASE64URL-ENCODE(SHA256(ASCII(code_verifier)))
def _create_code_challenge(cv):
    result = hashlib.sha256(cv).digest()
    result = base64.urlsafe_b64encode(result)
    result = result.rstrip('='.encode('utf-8'))  # strip b64 padding
    return result


# Authenticate with the (extended) "authorization code with pkce" flow.
def pkce(app, username, password, state=None):
    client_id = app.get("client_id", None)
    if client_id is None:
        raise ValueError("missing client_id")
    redirect_uri = app.get("redirect_uri", None)
    if redirect_uri is None:
        raise ValueError("missing redirect_uri")
    scope = app.get("scope", "openid")
    server = app.get("server", "default")

    # retrieve one time session token
    session_token = _get_session_token(username, password)
    if session_token is None:
        return None

    cv = _create_code_verifier(50)
    cc = _create_code_challenge(cv)

    # request authorization code
    params = {
        "client_id": client_id,
        "code_challenge": cc.decode("utf-8"),
        "code_challenge_method": "S256",
        "nonce": "none",
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "sessionToken": session_token,
        "state": state or str(time.time())}
    response = _get_authorize(params, server=server)

    # retrieve the authorization code from the redirect url query string
    location = response.headers.get("Location", None)
    if location is None:
        return None
    params = _parse_qs(location)
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
    response = _post_token(data, server=server)
    return response.json()


# Authenticate using the Okta "primary" method.
def primary(username, password):
    data = {"username": username, "password": password}
    response = _post(_url(PATH_AUTHN), data=json.dumps(data))
    if response.status_code != 200:
        response.raise_for_status()
    result = response.json()
    status = result.get("status", None)
    if status is None:
        raise AuthnError("no response status from /authn")
    if status != "SUCCESS":  # eg: LOCKED_OUT
        raise AuthnError("authenticaiton failed: %s" % status)
    return result


def refresh(app, refresh_token):
    client_id = app.get("client_id", None)
    if client_id is None:
        raise ValueError("missing client_id")
    scope = app.get("scope", "openid")
    server = app.get("server", "default")
    data = {
        "client_id": client_id,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": scope}
    response = _post_token(data, server=server)
    return response.json()


# Authenticate using the "resource owner password" flow.
def ropw(app, username, password):
    client_id = app.get("client_id", None)
    if client_id is None:
        raise ValueError("missing client_id")
    scope = app.get("scope", "openid")
    server = app.get("server", "aus1rarj6tQPJfJlz2p7")
    data = {
        "client_id": client_id,
        "grant_type": "password",
        "scope": scope,
        "username": username,
        "password": password}
    response = _post_token(data, server=server)
    return response.json()


def oauth(app, username=None, password=None):
    kind = app.get("kind", None)
    if kind is None:
        raise ValueError("no kind")
    if kind == "client":
        return client(app)
    if kind == "code":
        return code(app, username, password)
    if kind == "implicit":
        return implicit(app, username, password)
    if kind == "pkce":
        return pkce(app, username, password)
    if kind == "ropw":
        return ropw(app, username, password)
    raise ValueError("invalid kind: '%s'" % kind)
