import pytest
from test.fixtures import get_client_auth_manager as auth_manager  # NOQA


@pytest.mark.usefixtures('auth_manager')  # NOQA
def test_authenticate(auth_manager):
    auth_context = auth_manager.authenticate()
    assert(auth_context is not None)
