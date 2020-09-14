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

from time import time

from splunk_sdk.app_registry import CreateAppRequest, UpdateAppRequest, AppRegistry, AppName, NativeAppPOST
from splunk_sdk.base_client import BaseClient
from test.fixtures import get_test_client as test_client  # NOQA


@pytest.mark.usefixtures("test_client")  # NOQA
def test_crud_app(test_client: BaseClient):
    app_name = None
    appregistry = AppRegistry(test_client)
    try:
        # test_client.context.debug = True
        secs = str(round(time()))
        app_name = "p.c" + secs
        app_title = "psdk-" + app_name + "-" + secs
        redirect_urls = ["https://localhost"]

        app = appregistry.create_app(NativeAppPOST(
            kind="native",
            name=app_name,
            title=app_title,
            redirect_urls=redirect_urls,
        ))

        assert(app.name == app_name)

        apps = appregistry.list_apps()
        assert(len(apps) > 0)

        app_ret = appregistry.get_app(app_name)
        assert(app_ret.name == app_name)
        assert(app_ret.kind == "native")

        description = "A New Description"
        redirect_urls = ["https://somewhereelse"]
        app_title = "psdk-2-" + app_name + "-" + secs
        appregistry.update_app(app_name, UpdateAppRequest(
            description=description,
            title=app_title,
            redirect_urls=redirect_urls,
        ))

        app_ret = appregistry.get_app(app_name)
        assert(app_ret.name == app_name)
        assert(app_ret.kind == "native")
        assert(app_ret.title == app_title)
        assert(app_ret.description == description)

    finally:
        appregistry.delete_app(app_name)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_app_rotate_secret(test_client: BaseClient):
    app_name = None
    appregistry = AppRegistry(test_client)
    try:
        secs = str(round(time()))
        app_name = "p.c" + secs
        app_title = "psdk-" + app_name + "-" + secs
        redirect_urls = ["https://localhost"]

        app = appregistry.create_app(NativeAppPOST(
            kind="native",
            name=app_name,
            title=app_title,
            redirect_urls=redirect_urls,
        ))
        secret1 = app.to_dict()["clientSecret"]
        app_response = appregistry.rotate_secret(app_name)
        secret2 = app_response.to_dict()["clientSecret"]

        assert (secret1 != secret2)

    finally:
        appregistry.delete_app(app_name)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_subscriptions(test_client: BaseClient):
    appregistry = AppRegistry(test_client)
    app_name = None
    try:
        secs = str(round(time()))
        app_name = "p.c" + secs
        app_title = "psdk-" + app_name + "-" + secs
        redirect_urls = ["https://localhost"]

        app = appregistry.create_app(NativeAppPOST(
            name=app_name,
            title=app_title,
            redirect_urls=redirect_urls,
        ))

        appregistry.create_subscription(AppName(app.name))
        sub = appregistry.get_subscription(app.name)
        assert(app.name == sub.app_name)
        subs = appregistry.list_subscriptions()
        sub_count = len(subs)
        assert(sub_count > 0)

        subs = [s for s in appregistry.list_subscriptions() if s.app_name == app.name]
        assert(len(subs) == 1)

        subs = appregistry.list_app_subscriptions(app.name)
        assert(len(subs) == 1)

        appregistry.delete_subscription(app.name)

        subs = appregistry.list_app_subscriptions(app.name)
        assert(len(subs) == 0)

        subs = appregistry.list_subscriptions()
        assert(len(subs) == sub_count - 1)

    finally:
        appregistry.delete_app(app_name)
