import pytest

from test.fixtures import get_auth_manager as auth_manager  # NOQA
from splunk_sdk.common.context import Context
from splunk_sdk.base_client import BaseClient


@pytest.mark.usefixtures("auth_manager")  # NOQA
def test_service_client_instance(auth_manager):
    """Get a service client given a token"""
    default_config = Context()
    service_client = BaseClient(context=default_config,
                                auth_manager=auth_manager)
    assert(default_config is not None)
    assert(service_client is not None)
