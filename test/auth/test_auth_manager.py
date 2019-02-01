import pytest
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA


@pytest.mark.usefixtures('pkce_auth_manager')  # NOQA
def test_pkce_authenticate(pkce_auth_manager):
    auth_context = pkce_auth_manager.authenticate()
    _assert_pkce_auth_context(auth_context)


@pytest.mark.usefixtures('client_auth_manager')  # NOQA
def test_client_authenticate(client_auth_manager):
    auth_context = client_auth_manager.authenticate()
    _assert_client_auth_context(auth_context)


def _assert_pkce_auth_context(auth_context):
    assert (auth_context is not None)
    assert (auth_context.access_token is not None)
    assert (auth_context.id_token is not None)
    assert (auth_context.expires_in == 43200)
    assert (auth_context.token_type == 'Bearer')
    assert (auth_context.refresh_token is not None)

    # Note: scope comes back from okta in a non-deterministic order
    assert ('offline_access' in auth_context.scope)
    assert ('openid' in auth_context.scope)
    assert ('profile' in auth_context.scope)
    assert ('email' in auth_context.scope)


def _assert_client_auth_context(auth_context):
    assert (auth_context is not None)
    assert (auth_context.access_token is not None)
    assert (auth_context.id_token is None)
    assert (auth_context.expires_in == 43200)
    assert (auth_context.token_type == 'Bearer')
    assert (auth_context.refresh_token is None)
    assert (auth_context.scope == 'client_credentials')
