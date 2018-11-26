import pytest
from test.fixtures import get_test_client as test_client  # NOQA
from sdk.kvstore.client import KVStore


@pytest.mark.usefixtures('test_client')  # NOQA
def test_get_health_status(test_client):
    kvs = KVStore(test_client)
    health = kvs.get_health_status()
    assert(health.status == 'healthy')
