# coding: utf-8

# Copyright © 2019 Splunk, Inc.
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
    SDC Service: App Registry

    With the Splunk Cloud App Registry service, you can create, update, and manage apps built with Splunk Developer Cloud.

    OpenAPI spec version: v1beta2.0 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.app_registry.gen_models import AppName
from splunk_sdk.app_registry.gen_models import AppResourceKind
from splunk_sdk.app_registry.gen_models import AppResponseCreateUpdate
from splunk_sdk.app_registry.gen_models import AppResponseGetList
from splunk_sdk.app_registry.gen_models import CreateAppRequest
from splunk_sdk.app_registry.gen_models import Error
from splunk_sdk.app_registry.gen_models import Key
from splunk_sdk.app_registry.gen_models import Subscription
from splunk_sdk.app_registry.gen_models import UpdateAppRequest


class AppRegistry(BaseService):
    """
    App Registry
    Version: v1beta2.0
    With the Splunk Cloud App Registry service, you can create, update, and manage apps built with Splunk Developer Cloud.
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def create_app(self, create_app_request: CreateAppRequest, query_params: Dict[str, object] = None) -> AppResponseCreateUpdate:
        """
        Creates an app.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/app-registry/v1beta2/apps").substitute(path_params)
        url = self.base_client.build_url(path)
        data = create_app_request.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, AppResponseCreateUpdate)

    def create_subscription(self, app_name: AppName, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Creates a subscription.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/app-registry/v1beta2/subscriptions").substitute(path_params)
        url = self.base_client.build_url(path)
        data = app_name.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, )

    def delete_app(self, app_name: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes an app.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/apps/${appName}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_subscription(self, app_name: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a subscription.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/subscriptions/${appName}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def get_app(self, app_name: str, query_params: Dict[str, object] = None) -> AppResponseGetList:
        """
        Returns the metadata of an app.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/apps/${appName}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, AppResponseGetList)

    def get_keys(self, query_params: Dict[str, object] = None) -> List[Key]:
        """
        Returns a list of the public keys used for verifying signed webhook requests.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/system/app-registry/v1beta2/keys").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Key)

    def get_subscription(self, app_name: str, query_params: Dict[str, object] = None) -> Subscription:
        """
        Returns or validates a subscription.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/subscriptions/${appName}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Subscription)

    def list_app_subscriptions(self, app_name: str, query_params: Dict[str, object] = None) -> List[Subscription]:
        """
        Returns the collection of subscriptions to an app.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/apps/${appName}/subscriptions").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Subscription)

    def list_apps(self, query_params: Dict[str, object] = None) -> List[AppResponseGetList]:
        """
        Returns a list of apps.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/app-registry/v1beta2/apps").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, AppResponseGetList)

    def list_subscriptions(self, kind: AppResourceKind = None, query_params: Dict[str, object] = None) -> List[Subscription]:
        """
        Returns the tenant subscriptions.
        """
        if query_params is None:
            query_params = {}
        if kind is not None:
            query_params['kind'] = kind

        path_params = {
        }

        path = Template("/app-registry/v1beta2/subscriptions").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Subscription)

    def rotate_secret(self, app_name: str, query_params: Dict[str, object] = None) -> AppResponseCreateUpdate:
        """
        Rotates the client secret for an app.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/apps/${appName}/rotate-secret").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.post(url, params=query_params)
        return handle_response(response, AppResponseCreateUpdate)

    def update_app(self, app_name: str, update_app_request: UpdateAppRequest, query_params: Dict[str, object] = None) -> AppResponseCreateUpdate:
        """
        Updates an app.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "appName": app_name,
        }

        path = Template("/app-registry/v1beta2/apps/${appName}").substitute(path_params)
        url = self.base_client.build_url(path)
        data = update_app_request.to_dict()
        response = self.base_client.put(url, json=data, params=query_params)
        return handle_response(response, AppResponseCreateUpdate)


