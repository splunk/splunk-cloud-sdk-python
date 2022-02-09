# coding: utf-8

# Copyright © 2022 Splunk, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# [http://www.apache.org/licenses/LICENSE-2.0]
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

############# This file is auto-generated.  Do not edit! #############

"""
    SDC Service: Action Service

    With the Splunk Cloud Action service, you can receive incoming trigger events and use pre-defined action templates to turn these events into meaningful actions. 

    OpenAPI spec version: v2alpha1.12 
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.action.v2alpha1.gen_models import Action
from splunk_sdk.action.v2alpha1.gen_models import ActionMutable
from splunk_sdk.action.v2alpha1.gen_models import PublicWebhookKey
from splunk_sdk.action.v2alpha1.gen_models import ServiceError


class ActionService(BaseService):
    """
    Action Service
    Version: v2alpha1.12
    With the Splunk Cloud Action service, you can receive incoming trigger events and use pre-defined action templates to turn these events into meaningful actions. 
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def create_action(self, action: Action, query_params: Dict[str, object] = None) -> Action:
        """
        Creates an action template.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/action/v2alpha1/actions").substitute(path_params)
        url = self.base_client.build_url(path)
        data = action.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, Action)

    def delete_action(self, action_name: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes an action template.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "action_name": action_name,
        }

        path = Template("/action/v2alpha1/actions/${action_name}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def get_action(self, action_name: str, query_params: Dict[str, object] = None) -> Action:
        """
        Returns a specific action template.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "action_name": action_name,
        }

        path = Template("/action/v2alpha1/actions/${action_name}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Action)

    def get_public_webhook_keys(self, query_params: Dict[str, object] = None) -> List[PublicWebhookKey]:
        """
        Get the current webhook key(s). If multiple keys were returned, one is active and one is expired.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/system/action/v2alpha1/webhook/keys").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, PublicWebhookKey)

    def list_actions(self, query_params: Dict[str, object] = None) -> List[Action]:
        """
        Returns the list of action templates.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/action/v2alpha1/actions").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Action)

    def update_action(self, action_name: str, action_mutable: ActionMutable, query_params: Dict[str, object] = None) -> Action:
        """
        Modifies an action template.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "action_name": action_name,
        }

        path = Template("/action/v2alpha1/actions/${action_name}").substitute(path_params)
        url = self.base_client.build_url(path)
        data = action_mutable.to_dict()
        response = self.base_client.patch(url, json=data, params=query_params)
        return handle_response(response, Action)


