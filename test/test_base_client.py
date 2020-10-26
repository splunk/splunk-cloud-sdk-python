# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import pytest

from test.auth.test_auth_manager import \
    _assert_client_credentials_auth_context, _assert_pkce_auth_context, _assert_sp_credentials_auth_context  # NOQA
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA
from test.fixtures import get_service_principal_auth_manager as service_principal_auth_manager  # NOQA
from splunk_sdk.common.context import Context
from splunk_sdk.base_client import BaseClient
from splunk_sdk.identity import Identity as IdentityAndAccessControl


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_base_client_instance_with_pkce_auth(pkce_auth_manager):
    """Get a base client with a context and a pkce auth manager."""
    default_config = Context()
    base_client = BaseClient(context=default_config,
                             auth_manager=pkce_auth_manager)
    assert (default_config is not None)
    assert (base_client is not None)
    _assert_pkce_auth_context(base_client.auth_manager.context)


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_base_client_hooks_with_pkce_auth(pkce_auth_manager):
    responses = []

    def test_hook(response, **kwargs):
        responses.append(response)

    pkce_auth_manager.authenticate()
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')
    base_client = BaseClient(context=context,
                             auth_manager=pkce_auth_manager,
                             requests_hooks=[test_hook])
    IdentityAndAccessControl(base_client).validate_token()
    assert len(responses) == 1
    assert responses[0].status_code == 200


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_base_client_empty_hooks_with_pkce_auth(pkce_auth_manager):
    pkce_auth_manager.authenticate()
    context = Context(host=os.environ.get('SPLUNK_HOST'),
                      api_host=os.environ.get('SPLUNK_HOST'),
                      debug=os.environ.get(
                          'SPLUNK_DEBUG', 'false').lower().strip() == 'true')
    base_client = BaseClient(context=context,
                             auth_manager=pkce_auth_manager,
                             requests_hooks=[])
    IdentityAndAccessControl(base_client).validate_token()
    assert True


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_base_client_no_list_hooks_with_pkce_auth(pkce_auth_manager):
    def test_hook(*args, **kwargs):
        pass

    with pytest.raises(TypeError):
        BaseClient(context=Context(), auth_manager=pkce_auth_manager, requests_hooks=test_hook)


@pytest.mark.usefixtures("client_auth_manager")  # NOQA
def test_base_client_instance_with_client_auth(client_auth_manager):
    """Get a base client with a context and a client auth manager."""
    default_config = Context()
    base_client = BaseClient(context=default_config,
                             auth_manager=client_auth_manager)
    assert (default_config is not None)
    assert (base_client is not None)
    _assert_client_credentials_auth_context(base_client.auth_manager.context)


@pytest.mark.usefixtures("service_principal_auth_manager")  # NOQA
def test_base_client_instance_with_sp_auth(service_principal_auth_manager):
    """Get a base client with a context and a client auth manager."""
    default_config = Context()
    base_client = BaseClient(context=default_config,
                             auth_manager=service_principal_auth_manager)
    assert (default_config is not None)
    assert (base_client is not None)
    _assert_sp_credentials_auth_context(base_client.auth_manager.context)
