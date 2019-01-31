# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import pytest
from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.gateway.client import Gateway

ACTION_URI = "https://{host}/system/action/openapi.yaml"


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_specs(test_client):
    # Get the specs from the api gateway
    gateway = Gateway(test_client, cluster='api')
    specs = gateway.list_specs()
    assert(len(specs) > 0)

    # Get the specs from the app gateway
    gateway = Gateway(test_client, cluster='app')
    specs = gateway.list_specs()
    assert(len(specs) > 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_service_names(test_client):
    # Get the service names from the api gateway
    gateway = Gateway(test_client, cluster='api')
    names = gateway.get_service_names()
    assert(len(names) > 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_spec_url(test_client):
    # Get the spec url from the app gateway
    gateway = Gateway(test_client, cluster='api')
    spec = gateway.get_spec_url('Action Service')
    expected_uri = ACTION_URI.format(host=gateway.base_client.context.api_host)
    assert(expected_uri == spec)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_spec(test_client):
    # Download the spec from the app gateway
    gateway = Gateway(test_client, cluster='api')
    spec = gateway.get_spec('Action Service')
    assert(spec is not None)
