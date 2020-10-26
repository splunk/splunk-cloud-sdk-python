import os

import pytest

from splunk_sdk import Context
from splunk_sdk.auth import TokenAuthManager
from splunk_sdk.auth.auth_manager import AuthnError, RefreshTokenAuthManager
from splunk_sdk.base_client import BaseClient
from splunk_sdk.identity import Identity as IdentityAndAccessControl
from splunk_sdk.auth import PKCEAuthManager, ClientAuthManager
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA
from test.fixtures import get_service_principal_auth_manager as service_principal_auth_manager  # NOQA


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

@pytest.mark.usefixtures('pkce_auth_manager')  # NOQA
def test_refresh_token_authenticate(pkce_auth_manager):
    auth_context = pkce_auth_manager.authenticate()

    # use existing token from auth_context
    refresh_token_mgr = RefreshTokenAuthManager(client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                                                refresh_token=auth_context.refresh_token,
                                                host=os.environ.get('SPLUNK_AUTH_HOST'))

    new_auth_context = refresh_token_mgr.authenticate()

    assert (new_auth_context.refresh_token is not None)
    assert (new_auth_context.access_token is not None)
    assert (new_auth_context.id_token is not None)
    assert (new_auth_context.token_type is not None)
    assert (new_auth_context.expires_in is not None)
    assert (new_auth_context.scope is not None)

def test_error_refresh_token_authenticate():
    refresh_token_mgr = RefreshTokenAuthManager(client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                                                refresh_token="refresh",
                                                host=os.environ.get('SPLUNK_AUTH_HOST'))

    with pytest.raises(AuthnError):
        refresh_token_mgr.authenticate()

@pytest.mark.usefixtures('client_auth_manager')  # NOQA
def test_client_credentials_authenticate(client_auth_manager):
    auth_context = client_auth_manager.authenticate()
    _assert_client_credentials_auth_context(auth_context)


@pytest.mark.usefixtures('client_auth_manager')  # NOQA
def test_token_authenticate(client_auth_manager):
    auth_context = client_auth_manager.authenticate()
    _assert_client_credentials_auth_context(auth_context)

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

    context = Context(host=os.environ.get("SPLUNK_HOST"), tenant=os.environ.get("SPLUNK_TENANT"))
    base_client = BaseClient(context=context, auth_manager=token_mgr)
    idc = IdentityAndAccessControl(base_client)
    assert (idc.validate_token().name.lower() == os.environ.get("SPLUNK_APP_CLIENT_CRED_ID").lower())


def test_pkce_requests_hook():
    responses = []

    def test_hook(response, **kwargs):
        responses.append(response)

    PKCEAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                    client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                    username=os.environ.get('SPLUNK_USERNAME'),
                    password=os.environ.get('SPLUNK_PASSWORD'),
                    redirect_uri=os.environ.get('SPLUNK_REDIRECT_URL'),
                    requests_hooks=[test_hook]).authenticate()
    assert len(responses) == 4
    auth_url = 'https://%s' % os.environ.get('SPLUNK_AUTH_HOST')
    assert responses[0].request.method == 'GET'
    assert responses[0].request.url == '%s/csrfToken' % auth_url
    assert responses[0].status_code == 200
    assert responses[1].request.method == 'POST'
    assert responses[1].request.url == '%s/authn' % auth_url
    assert responses[1].status_code == 200
    assert responses[2].request.method == 'GET'
    assert responses[2].request.url.startswith('%s/authorize' % auth_url)
    assert responses[2].status_code == 302
    assert responses[3].request.method == 'POST'
    assert responses[3].request.url == '%s/token' % auth_url
    assert responses[3].status_code == 200


def test_pkce_no_list_hooks():
    hook_called = []

    def test_hook(*args, **kwargs):
        hook_called.append(True)

    PKCEAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                    client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                    username=os.environ.get('SPLUNK_USERNAME'),
                    password=os.environ.get('SPLUNK_PASSWORD'),
                    redirect_uri=os.environ.get('SPLUNK_REDIRECT_URL'),
                    requests_hooks=test_hook).authenticate()
    assert hook_called


def test_client_manager_requests_hook():
    hook_called = []

    def test_hook(*args, **kwargs):
        hook_called.append(True)

    ClientAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                      client_id=os.environ.get('SPLUNK_APP_CLIENT_CRED_ID'),
                      client_secret=os.environ.get('SPLUNK_APP_CLIENT_CRED_SECRET'),
                      scope=os.environ.get('SPLUNK_SCOPE'),
                      requests_hooks=[test_hook]).authenticate()
    assert hook_called


def test_pkce_manager_no_list_hooks():
    hook_called = []

    def test_hook(*args, **kwargs):
        hook_called.append(True)

    PKCEAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                    client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                    username=os.environ.get('SPLUNK_USERNAME'),
                    password=os.environ.get('SPLUNK_PASSWORD'),
                    redirect_uri=os.environ.get('SPLUNK_REDIRECT_URL'),
                    requests_hooks=test_hook).authenticate()
    assert hook_called


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


def _assert_client_credentials_auth_context(auth_context, expires_in=43200):
    assert (auth_context is not None)
    assert (auth_context.access_token is not None)
    # assert(auth_context.id_token is None)
    assert (auth_context.expires_in == expires_in)
    assert (auth_context.token_type == 'Bearer')
    assert (auth_context.refresh_token is None)
    assert (auth_context.scope == 'client_credentials')


def _assert_sp_credentials_auth_context(auth_context):
    _assert_client_credentials_auth_context(auth_context, 3600)


@pytest.mark.usefixtures('service_principal_auth_manager')  # NOQA
def test_sp_authenticate(service_principal_auth_manager):
    auth_context = service_principal_auth_manager.authenticate()
    _assert_sp_credentials_auth_context(auth_context)


@pytest.mark.usefixtures('service_principal_auth_manager')  # NOQA
def test_sp_token_authenticate(service_principal_auth_manager):
    auth_context = service_principal_auth_manager.authenticate()
    _assert_sp_credentials_auth_context(auth_context)

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

    context = Context(host=os.environ.get("SPLUNK_HOST"), tenant=os.environ.get("SPLUNK_TENANT"))
    base_client = BaseClient(context=context, auth_manager=token_mgr)
    idc = IdentityAndAccessControl(base_client)
    assert (idc.validate_token().name.lower() == os.environ.get("SPLUNK_APP_PRINCIPAL_NAME").lower())
