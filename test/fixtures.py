# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging
import os
import pytest
import sys

from splunk_sdk.auth import ClientAuthManager, PKCEAuthManager, ServicePrincipalAuthManager
from splunk_sdk.common.context import Context
from splunk_sdk.base_client import get_client

from splunk_sdk.base_client import RetryConfig

# create logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


@pytest.fixture(scope='session')
def get_test_client_default_retry():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      tenant=os.environ.get('SPLUNK_TENANT'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')

    retry_config = RetryConfig(retry_requests_enabled=True)

    # integration tests use pkce by default
    service_client = get_client(context, _get_pkce_manager(), retry_config)
    assert (service_client is not None)
    return service_client

@pytest.fixture(scope='session')
def get_test_client_retry_false():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      tenant=os.environ.get('SPLUNK_TENANT'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')

    retry_config = RetryConfig(retry_requests_enabled=False)

    # integration tests use pkce by default
    service_client = get_client(context, _get_pkce_manager(), retry_config)
    assert (service_client is not None)
    return service_client

@pytest.fixture(scope='session')
def get_test_client_custom_retry():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      tenant=os.environ.get('SPLUNK_TENANT'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')

    retry_config = RetryConfig(retry_requests_enabled=True, retry_count=12, retry_interval=1200)

    # integration tests use pkce by default
    service_client = get_client(context, _get_pkce_manager(), retry_config)
    assert (service_client is not None)
    return service_client

@pytest.fixture(scope='session')
def get_test_client():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      tenant=os.environ.get('SPLUNK_TENANT'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')

    # integration tests use pkce by default
    service_client = get_client(context, _get_pkce_manager())
    assert (service_client is not None)
    return service_client

@pytest.fixture(scope='session')
def get_test_client_ml():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      tenant=os.environ.get('SPLUNK_TENANT_ML'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')

    # integration tests use pkce by default
    service_client = get_client(context, _get_pkce_manager())
    assert (service_client is not None)
    return service_client


@pytest.fixture(scope='session')
def get_test_client_provisioner():
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      tenant='system',
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')

    # integration tests use pkce by default
    service_client = get_client(context, _get_pkce_manager())
    assert (service_client is not None)
    return service_client


@pytest.fixture(scope='session')
def get_auth_manager():
    # Note: leaving this so we don't create too many merge conflicts
    auth_manager = _get_pkce_manager()
    assert (auth_manager is not None)
    return auth_manager


@pytest.fixture(scope='session')
def get_client_auth_manager():
    auth_manager = _get_client_manager()
    assert (auth_manager is not None)
    return auth_manager


@pytest.fixture(scope='session')
def get_service_principal_auth_manager():
    auth_manager = _get_principal_manager()
    assert (auth_manager is not None)
    return auth_manager


def _get_pkce_manager():
    return PKCEAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                           client_id=os.environ.get('SPLUNK_APP_CLIENT_ID'),
                           username=os.environ.get('SPLUNK_USERNAME'),
                           password=os.environ.get('SPLUNK_PASSWORD'),
                           redirect_uri=os.environ.get('SPLUNK_REDIRECT_URL'))


def _get_client_manager():
    return ClientAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                             client_id=os.environ.get(
                                 'SPLUNK_APP_CLIENT_CRED_ID'),
                             client_secret=os.environ.get(
                                 'SPLUNK_APP_CLIENT_CRED_SECRET'),
                             scope=os.environ.get('SPLUNK_SCOPE'))


def _get_principal_manager():
    return ServicePrincipalAuthManager(host=os.environ.get('SPLUNK_AUTH_HOST'),
                                       principal_name=os.environ.get('SPLUNK_APP_PRINCIPAL_NAME'),
                                       key=os.environ.get('SPLUNK_APP_PRINCIPAL_PRIVATE_KEY'),
                                       kid=os.environ.get('SPLUNK_APP_PRINCIPAL_KEY_ID'),
                                       algorithm=os.environ.get('SPLUNK_APP_PRINCIPAL_KEY_ALG'))
