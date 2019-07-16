# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import re

import pytest
from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.gateway.client import Gateway

ACTION_URI = r"""https://(?P<host>[\w.]+)/system/action/specs/v\d+(?:(?:alpha|beta)\d+(?:\.\d+)?)/openapi.yaml"""


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_specs(test_client):
    # Get the specs from the api gateway
    gateway = Gateway(test_client)
    specs = gateway.list_specs()
    assert(len(specs) > 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_service_names(test_client):
    # Get the service names from the api gateway
    gateway = Gateway(test_client)
    names = gateway.get_service_names()
    assert(len(names) > 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_spec_url(test_client):
    # Get the spec url from the app gateway
    gateway = Gateway(test_client)
    spec = gateway.get_spec_url('action')

    match = re.match(ACTION_URI, spec)
    assert match
    assert(match.group('host') == gateway.base_client.context.api_host)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_spec(test_client):
    # Download the spec from the api gateway
    gateway = Gateway(test_client)
    spec = gateway.get_spec('action')
    print(spec)
    assert(spec is not None)
