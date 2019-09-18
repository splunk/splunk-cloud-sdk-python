# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import pytest


from test.fixtures import get_test_client as test_client  # NOQA

from splunk_sdk.base_client import BaseClient
from splunk_sdk.splunk_cloud import SplunkCloud


@pytest.mark.usefixtures("test_client")  # NOQA
def test_splunk_cloud_instance(test_client: BaseClient):
    sc = SplunkCloud(test_client.context, test_client.auth_manager)
    assert (sc is not None)
    assert (sc.action is not None)
    assert (sc.app_registry is not None)
    assert (sc.catalog is not None)
    assert (sc.collect is not None)
    assert (sc.forwarders is not None)
    assert (sc.gateway is not None)
    assert (sc.identity is not None)
    assert (sc.ingest is not None)
    assert (sc.kvstore is not None)
    assert (sc.provisioner is not None)
    assert (sc.search is not None)
    assert (sc.streams is not None)
    assert (sc.ml is not None)
