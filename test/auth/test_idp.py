import os
import pytest
from splunk_sdk.auth.idp import IdpClient
from splunk_sdk.auth.auth_manager import AuthContext
from test.auth.test_auth_manager import \
    _assert_client_credentials_auth_context, _assert_pkce_auth_context
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA


def test_default_idp_client():
    client = IdpClient()
    assert (client.scheme == "https")
    assert (client.host == "auth.scp.splunk.com")


def test_http_idp_client():
    client = IdpClient(scheme="http")
    assert (client.scheme == "http")
    assert (client.host == "auth.scp.splunk.com")


def test_host_idp_client():
    client = IdpClient(host=os.environ.get('SPLUNK_AUTH_HOST'))
    assert (client.scheme == "https")
    assert (client.host == os.environ.get('SPLUNK_AUTH_HOST'))


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_pkce(pkce_auth_manager):
    data = IdpClient(host=pkce_auth_manager.host).pkce(
        pkce_auth_manager.app, pkce_auth_manager.username,
        pkce_auth_manager.password)
    assert (data is not None)
    ctx = AuthContext(**data)
    _assert_pkce_auth_context(ctx)


@pytest.mark.usefixtures("client_auth_manager")  # NOQA
def test_client(client_auth_manager):
    data = IdpClient(host=client_auth_manager.host).client(
        client_auth_manager.app)
    assert (data is not None)
    ctx = AuthContext(**data)
    _assert_client_credentials_auth_context(ctx)


# TODO(dan): waiting on IAC implementation
@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_pkce_refresh(pkce_auth_manager):
    idp_client = IdpClient(host=pkce_auth_manager.host)

    data = idp_client.pkce(pkce_auth_manager.app,
                           pkce_auth_manager.username,
                           pkce_auth_manager.password)
    assert (data is not None)
    ctx = AuthContext(**data)
    _assert_pkce_auth_context(ctx)

    refreshed_data = idp_client.refresh(pkce_auth_manager.app,
                                        ctx.refresh_token)
    assert (refreshed_data is not None)
    refreshed_ctx = AuthContext(**refreshed_data)
    _assert_pkce_auth_context(refreshed_ctx)
