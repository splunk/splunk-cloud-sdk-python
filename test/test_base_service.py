# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import os
import pytest

from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.base_service import BaseService


@pytest.mark.usefixtures("test_client")  # NOQA
def test_base_service_default(test_client):
    """If the cluster is not set the host will default to the api
     cluster."""
    base_service = BaseService(test_client)

    assert (base_service is not None)

    _host = base_service.base_client.context.host
    assert (_host == os.environ.get('SPLUNK_HOST'))
    assert (_host == os.environ.get('SPLUNK_API_HOST'))
    assert (_host != os.environ.get('SPLUNK_APP_HOST'))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_base_service_api(test_client):
    """If the cluster is set to api the host will default to the api
     cluster."""
    base_service = BaseService(test_client, 'api')

    assert (base_service is not None)

    _host = base_service.base_client.context.host
    assert (_host == os.environ.get('SPLUNK_HOST'))
    assert (_host == os.environ.get('SPLUNK_API_HOST'))
    assert (_host != os.environ.get('SPLUNK_APP_HOST'))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_base_service_app(test_client):
    """If the cluster is set to app the host will default to the app
     cluster."""
    base_service = BaseService(test_client, 'app')

    assert (base_service is not None)

    _host = base_service.base_client.context.host
    assert (_host != os.environ.get('SPLUNK_HOST'))
    assert (_host == os.environ.get('SPLUNK_APP_HOST'))
    assert (_host != os.environ.get('SPLUNK_API_HOST'))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_base_service_app_uppercase(test_client):
    """If the cluster is set to app the host will default to the app
     cluster."""
    base_service = BaseService(test_client, 'App')

    assert (base_service is not None)

    _host = base_service.base_client.context.host
    assert (_host != os.environ.get('SPLUNK_HOST'))
    assert (_host == os.environ.get('SPLUNK_APP_HOST'))
    assert (_host != os.environ.get('SPLUNK_API_HOST'))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_base_service_exception(test_client):
    """If the cluster is set to an invalid host an exception will be
     raised."""

    with pytest.raises(Exception) as e:
        BaseService(test_client, 'bad_data')
    assert (e is not None)
    assert ("The target cluster: bad_data is invalid." in str(e))
