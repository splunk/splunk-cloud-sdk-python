import pytest
from splunk_sdk.auth import TokenAuthManager
from splunk_sdk.auth.auth_manager import AuthnError
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA


@pytest.mark.usefixtures('pkce_auth_manager')  # NOQA
def test_pkce_authenticate(pkce_auth_manager):
    auth_context = pkce_auth_manager.authenticate()
    _assert_pkce_auth_context(auth_context)


@pytest.mark.usefixtures('pkce_auth_manager')  # NOQA
def test_auth_error_properties(pkce_auth_manager):
    save_passwd = pkce_auth_manager._password
    pkce_auth_manager._password = 'WRONG'
    try:
        pkce_auth_manager.authenticate()
    except AuthnError as err:
        assert (err.status != "")
        assert (err.status is not None)
        assert (err.server_error_description != "")
        assert (err.server_error_description is not None)
        assert (err.request_id != "")
        assert (err.request_id is not None)
    finally:
        pkce_auth_manager._password = save_passwd


@pytest.mark.usefixtures('client_auth_manager')  # NOQA
def test_client_credentials_authenticate(client_auth_manager):
    auth_context = client_auth_manager.authenticate()
    _assert_client_credentials_auth_context(auth_context)


@pytest.mark.usefixtures('client_auth_manager')  # NOQA
def test_token_authenticate(pkce_auth_manager):
    auth_context = pkce_auth_manager.authenticate()
    _assert_pkce_auth_context(auth_context)

    # use existing token from auth_context
    token_mgr = TokenAuthManager(access_token=auth_context.access_token,
                                 token_type=auth_context.token_type,
                                 expires_in=auth_context.expires_in,
                                 scope=auth_context.scope,
                                 id_token=auth_context.id_token,
                                 refresh_token=auth_context.refresh_token)

    new_auth_context = token_mgr.authenticate()
    assert (auth_context.access_token == new_auth_context.access_token)
    assert (auth_context.token_type == new_auth_context.token_type)
    assert (auth_context.expires_in == new_auth_context.expires_in)
    assert (auth_context.scope == new_auth_context.scope)
    assert (auth_context.id_token == new_auth_context.id_token)
    assert (auth_context.refresh_token == new_auth_context.refresh_token)


def _assert_pkce_auth_context(auth_context):
    assert (auth_context is not None)
    assert (auth_context.access_token is not None)
    assert (auth_context.id_token is not None)
    assert (auth_context.expires_in == 43200)
    assert (auth_context.token_type == 'Bearer')
    assert (auth_context.refresh_token is not None)

    # Note: scope comes back from idp in a non-deterministic order
    assert ('offline_access' in auth_context.scope)
    assert ('openid' in auth_context.scope)
    assert ('profile' in auth_context.scope)
    assert ('email' in auth_context.scope)


def _assert_client_credentials_auth_context(auth_context):
    assert (auth_context is not None)
    assert (auth_context.access_token is not None)
    # assert(auth_context.id_token is None)
    assert (auth_context.expires_in == 43200)
    assert (auth_context.token_type == 'Bearer')
    assert (auth_context.refresh_token is None)
    assert (auth_context.scope == 'client_credentials')
