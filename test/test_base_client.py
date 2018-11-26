from sdk.common.context import Context
from sdk.base_client import BaseClient


def test_service_client_instance():
    """Get a service client given a token"""
    default_config = Context()
    service_client = BaseClient(context=default_config, token="FAKE_TOKEN")
    assert(default_config is not None)
    assert(service_client is not None)
