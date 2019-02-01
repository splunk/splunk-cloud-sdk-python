# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import pytest

from test.auth.test_auth_manager import _assert_client_auth_context, \
    _assert_pkce_auth_context
from test.fixtures import get_auth_manager as pkce_auth_manager  # NOQA
from test.fixtures import get_client_auth_manager as client_auth_manager  # NOQA
from splunk_sdk.common.context import Context
from splunk_sdk.base_client import BaseClient


@pytest.mark.usefixtures("pkce_auth_manager")  # NOQA
def test_base_client_instance_with_pkce_auth(pkce_auth_manager):
    """Get a base client with a context and a pkce auth manager."""
    default_config = Context()
    base_client = BaseClient(context=default_config,
                             auth_manager=pkce_auth_manager)
    assert (default_config is not None)
    assert (base_client is not None)
    _assert_pkce_auth_context(base_client.auth_context)


@pytest.mark.usefixtures("client_auth_manager")  # NOQA
def test_base_client_intance_with_client_auth(client_auth_manager):
    """Get a base client with a context and a client auth manager."""
    default_config = Context()
    base_client = BaseClient(context=default_config,
                             auth_manager=client_auth_manager)
    assert (default_config is not None)
    assert (base_client is not None)
    _assert_client_auth_context(base_client.auth_context)
