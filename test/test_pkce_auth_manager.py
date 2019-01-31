# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import pytest
from test.fixtures import get_auth_manager as auth_manager  # NOQA


@pytest.mark.usefixtures('auth_manager')  # NOQA
def test_authenticate(auth_manager):
    auth_context = auth_manager.authenticate()
    assert(auth_context is not None)
