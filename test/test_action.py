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
import time


from test.fixtures import get_test_client as test_client  # NOQA

from splunk_sdk.action import ActionService
from splunk_sdk.action import EmailAction, WebhookAction, TriggerEvent, \
    TriggerEventKind

from splunk_sdk.base_client import BaseClient
from splunk_sdk.common.sscmodel import SSCModel


class Event(SSCModel):

    def __init__(self):
        super().__init__()

    def to_dict(self) -> dict:
        return self.__dict__


def _assert_webhook_action(a1: WebhookAction, a2: WebhookAction):
    assert(a1.name == a2.name)
    assert(a1.title == a2.title)
    assert(a1.webhook_payload == a2.webhook_payload)
    assert(a1.webhook_url == a2.webhook_url)


def _assert_email_action(a1: EmailAction, a2: EmailAction):
    assert(a1.name == a2.name)
    assert(a1.title == a2.title)
    assert(a1.subject == a2.subject)
    assert(a1.body == a2.body)
    assert(a1.body_plain_text == a2.body_plain_text)


def _create_webhook_action():
    return WebhookAction(
        name="sdkpytest_" + str(time.time_ns()),
        title="sdktitle",
        webhook_url="https://webhook.site/4d4dd94e-e14f-4123-8f8a-18df20b34214",
        webhook_payload="A message to post")


def _create_email_action():
    return EmailAction(
        name="sdkpytest_" + str(time.time_ns()),
        title="sdktitle", members=["success@simulator.amazonses.com", ],
        body="<html><h1>The HTML</h1></html>",
        body_plain_text="This is a plain text body.", subject="test subject",
        from_name="sdk@splunk.com")


def _create_trigger_event(name, tenant):
    payload = {'host': "myhost",
               'index': "main",
               'source': "mysource",
               'sourcetype': "mysourcetype",
               'time': 0,
               'fields': {"f1": "myfield", "f2": "anotherfield"},
               }

    return TriggerEvent(
        kind=TriggerEventKind.TRIGGER, payload=payload, tenant=tenant,
        trigger_name=name)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_delete_webhook_action(test_client: BaseClient):
    action = ActionService(test_client)
    webhook = None
    try:
        webhook = _create_webhook_action()
        _webhook = action.create_action(webhook)
        _assert_webhook_action(webhook, _webhook)

    finally:
        # delete action
        resp = action.delete_action(action_name=webhook.name)
        assert(resp.response.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_delete_email_action(test_client: BaseClient):
    action = ActionService(test_client)
    try:
        email = _create_email_action()
        _email = action.create_action(email)
        _assert_email_action(email, _email)

    finally:
        # delete action
        resp = action.delete_action(action_name=email.name)
        assert(resp.response.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_action(test_client: BaseClient):
    action = ActionService(test_client)
    try:
        webhook = _create_webhook_action()

        # ignore result
        action.create_action(webhook)

        # get webhook action
        _webhook = action.get_action(webhook.name)
        _assert_webhook_action(webhook, _webhook)

    finally:
        # delete action
        resp = action.delete_action(action_name=webhook.name)
        assert(resp.response.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_actions(test_client: BaseClient):
    action = ActionService(test_client)
    action_list = []
    try:
        actions = {}
        for i in range(0, 2):
            wh = _create_webhook_action()
            action.create_action(wh)
            actions[wh.name] = wh

            e = _create_email_action()
            action.create_action(e)
            actions[e.name] = e

        action_list = action.list_actions()
        assert(action_list is not None)
        assert(len(action_list) >= 2)
        for created in action_list:
            found = actions.get(created.name)

            # there could be some extra actions in the list
            if found:
                if found.kind == 'webhook':
                    _assert_webhook_action(created, found)

                elif found.kind == 'email':
                    _assert_email_action(created, found)

    finally:
        # delete action
        for a in action_list:
            if a.name.startswith("sdkpytest_"):
                payload = action.delete_action(action_name=a.name)
                assert(payload.response.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_trigger_event(test_client: BaseClient):
    action = ActionService(test_client)

    try:
        # create a webhook action first
        webhook = _create_webhook_action()
        _webhook = action.create_action(webhook)
        _assert_webhook_action(webhook, _webhook)

        # create a trigger event
        event = _create_trigger_event(name="trigger_" + webhook.name,
                                      tenant=action.base_client.context.tenant)

        # trigger the webhook action
        resp = action.trigger_action(action_name=webhook.name, trigger_event=event).response
        assert(resp.status_code == 201)
        assert(action.base_client.context.tenant in resp.headers['location'])
        assert('/action/v1beta2/actions/' in resp.headers['location'])

    finally:
        # delete action
        resp = action.delete_action(action_name=webhook.name).response
        assert(resp.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_action_status(test_client: BaseClient):
    action = ActionService(test_client)

    try:
        # create a webhook action first
        webhook = _create_webhook_action()
        _webhook = action.create_action(webhook)
        _assert_webhook_action(webhook, _webhook)

        # create a trigger event
        event = _create_trigger_event(name="trigger_" + webhook.name,
                                      tenant=action.base_client.context.tenant)
        # trigger the webhook action
        resp = action.trigger_action(action_name=webhook.name,
                                     trigger_event=event).response
        assert (resp.status_code == 201)
        assert (action.base_client.context.tenant in resp.headers['location'])
        assert ('/action/v1beta2/actions/' in resp.headers['location'])

        location = resp.headers['location']
        url, status_id = location.split("/status/", 1)
        assert(url is not None)
        assert(status_id is not None)

        # get action status
        action_result = action.get_action_status(action_name=webhook.name,
                                                 status_id=status_id)
        assert(action_result is not None)
        assert(action_result.status_id is not None)
        assert(action_result.state in ['QUEUED', 'RUNNING', 'DONE', 'FAILED'])

    finally:
        # delete action
        resp = action.delete_action(action_name=webhook.name).response
        assert(resp.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_email_action_status_details(test_client: BaseClient):
    action = ActionService(test_client)

    try:
        # create a email action first
        email = _create_email_action()
        _email = action.create_action(email)
        _assert_email_action(email, _email)

        # create a trigger event
        event = _create_trigger_event(name="trigger_" + email.name,
                                      tenant=action.base_client.context.tenant)

        # trigger the email action
        resp = action.trigger_action(action_name=email.name,
                                     trigger_event=event).response
        assert (resp.status_code == 201)
        assert (action.base_client.context.tenant in resp.headers['location'])
        assert ('/action/v1beta2/actions/' in resp.headers['location'])

        location = resp.headers['location']
        url, status_id = location.split("/status/", 1)
        assert (url is not None)
        assert (status_id is not None)

        # get action status details
        action_result_email_detail = action.get_action_status_details(
            action_name=email.name, status_id=status_id)

        # this could be a list of results
        for email_status in action_result_email_detail:
            assert(email_status.email_address is not None)

    finally:
        # delete action
        resp = action.delete_action(action_name=email.name).response
        assert(resp.status_code == 204)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_public_webhook_keys(test_client: BaseClient):
    action = ActionService(test_client)
    keys = action.get_public_webhook_keys()
    assert(keys is not None)
    assert(len(keys) > 0)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_update_action(test_client: BaseClient):
    action = ActionService(test_client)
    try:
        # create a email action first
        email = _create_email_action()
        _email = action.create_action(email)
        _assert_email_action(email, _email)

        email.subject = 'The new subject'
        email.title = 'The new title'

        updated_model = action.update_action(email.name, action_mutable=email)
        assert(email.subject == updated_model.subject)
        assert(email.title == updated_model.title)

    finally:
        # delete action
        resp = action.delete_action(action_name=email.name).response
        assert (resp.status_code == 204)

