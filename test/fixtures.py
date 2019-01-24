import os
import pytest

from splunk_sdk.auth.client_auth_manager import ClientAuthManager
from splunk_sdk.auth.pkce_auth_manager import PKCEAuthManager
from splunk_sdk.common.context import Context
from splunk_sdk.base_client import get_client


@pytest.fixture(scope="session")
def get_test_client():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_API_HOST'),
                      app_host=os.environ.get('SPLUNK_APP_HOST'),
                      tenant=os.environ.get('SPLUNK_TENANT'))
    service_client = get_client(context, _get_pkce_manager())
    assert(service_client is not None)
    return service_client


@pytest.fixture(scope="session")
def get_auth_manager(authflow='pkce'):

    if authflow == "pkce":
        auth_manager = _get_pkce_manager()
    else:
        auth_manager = _get_client_manager()

    assert(auth_manager is not None)
    return auth_manager


def _get_pkce_manager():
    return PKCEAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                           client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                           server=os.environ.get('SPLUNK_APP_SERVER'),
                           username=os.environ.get('SPLUNK_USERNAME'),
                           password=os.environ.get('SPLUNK_PASSWORD'),
                           redirect_uri='http://localhost')


def _get_client_manager():
    return ClientAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                             client_id=os.environ.get('SPLUNK_APP_CLIENT_CRED_ID'),
                             client_secret=os.environ.get('SPLUNK_APP_CLIENT_CRED_SECRET'),
                             server=os.environ.get('SPLUNK_APP_SERVER')
                             )
