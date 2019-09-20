import pytest

from splunk_sdk.base_client import BaseClient
from splunk_sdk.identity import Identity as IdentityAndAccessControl
from test.fixtures import get_test_client as test_client


@pytest.mark.usefixtures("test_client")  # NOQA
def test_crud_groups(test_client: BaseClient):
    identity = IdentityAndAccessControl(test_client)
    result = identity.validate_token()
    assert(result.response.status_code == 200)
    original_token = test_client.auth_manager.context.access_token
    test_client.auth_manager.context.expires_in = 20
    result = identity.validate_token()
    assert(result.response.status_code == 200)
    assert(original_token != test_client.auth_manager.context.access_token)
    assert(test_client.auth_manager.context.expires_in > 20)
