import pytest
from splunk_sdk.auth.okta import OktaClient, DEFAULT_HOST
from splunk_sdk.auth.auth_manager import AuthContext
from test.auth.test_auth_manager import _assert_client_auth_context, \
    _assert_pkce_auth_context
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA


def test_default_okta_client():
    client = OktaClient()
    assert (client.scheme == "https")
    assert (client.host == DEFAULT_HOST)
    assert (client.verbose is False)


def test_verbose_okta_client():
    client = OktaClient(verbose=True)
    assert (client.scheme == "https")
    assert (client.host == DEFAULT_HOST)
    assert (client.verbose is True)


def test_http_okta_client():
    client = OktaClient(scheme="http")
    assert (client.scheme == "http")
    assert (client.host == DEFAULT_HOST)
    assert (client.verbose is False)


def test_host_okta_client():
    client = OktaClient(host="splunk-ciam.okta.com")
    assert (client.scheme == "https")
    assert (client.host == "splunk-ciam.okta.com")
    assert (client.verbose is False)


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_pkce(pkce_auth_manager):
    data = OktaClient().pkce(pkce_auth_manager.app, pkce_auth_manager.username,
                             pkce_auth_manager.password)
    assert (data is not None)
    ctx = AuthContext(**data)
    _assert_pkce_auth_context(ctx)


@pytest.mark.usefixtures("client_auth_manager")  # NOQA
def test_client(client_auth_manager):
    data = OktaClient().client(client_auth_manager.app)
    assert (data is not None)
    ctx = AuthContext(**data)
    _assert_client_auth_context(ctx)


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_pkce_refresh(pkce_auth_manager):
    okta_client = OktaClient()

    data = okta_client.pkce(pkce_auth_manager.app, pkce_auth_manager.username,
                            pkce_auth_manager.password)
    assert (data is not None)
    ctx = AuthContext(**data)
    _assert_pkce_auth_context(ctx)

    refreshed_data = okta_client.refresh(pkce_auth_manager.app,
                                         ctx.refresh_token)
    assert (refreshed_data is not None)
    refreshed_ctx = AuthContext(**refreshed_data)
    _assert_pkce_auth_context(refreshed_ctx)
