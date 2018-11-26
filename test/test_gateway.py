import pytest
from test.fixtures import get_test_client as test_client  # NOQA
from sdk.gateway.client import Gateway
from sdk.gateway.client import API_ACTION_SERVICE

ACTION_URI = "https://api.playground.splunkbeta.com/system/action/openapi.yaml"

@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_specs(test_client):
    # Get the specs from the api gateway
    gateway = Gateway(test_client, cluster='api')
    specs = gateway.list_specs()
    assert(len(specs) > 0)

    # Get the specs from the app gateway
    gateway = Gateway(test_client, cluster='app')
    specs = gateway.list_specs()
    assert(len(specs) > 0)

@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_spec(test_client):
    # Get the specs from the app gateway
    gateway = Gateway(test_client, cluster='api')
    spec = gateway.get_spec(API_ACTION_SERVICE)
    assert(ACTION_URI == spec)
