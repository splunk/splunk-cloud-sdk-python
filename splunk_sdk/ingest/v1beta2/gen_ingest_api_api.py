# coding: utf-8

# Copyright © 2020 Splunk, Inc.
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
    SDC Service: Ingest API

    Use the Ingest service in Splunk Cloud Services to send event and metrics data, or upload a static file, to Splunk Cloud Services.

    OpenAPI spec version: v1beta2.16 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.ingest.v1beta2.gen_models import Error
from splunk_sdk.ingest.v1beta2.gen_models import Event
from splunk_sdk.ingest.v1beta2.gen_models import HECResponse
from splunk_sdk.ingest.v1beta2.gen_models import HECTokenAccessResponse
from splunk_sdk.ingest.v1beta2.gen_models import HECTokenCreateRequest
from splunk_sdk.ingest.v1beta2.gen_models import HECTokenCreateResponse
from splunk_sdk.ingest.v1beta2.gen_models import HECTokenUpdateRequest
from splunk_sdk.ingest.v1beta2.gen_models import HTTPResponse
from splunk_sdk.ingest.v1beta2.gen_models import List
from splunk_sdk.ingest.v1beta2.gen_models import MetricEvent
from splunk_sdk.ingest.v1beta2.gen_models import UploadSuccessResponse


class IngestAPI(BaseService):
    """
    Ingest API
    Version: v1beta2.16
    Use the Ingest service in Splunk Cloud Services to send event and metrics data, or upload a static file, to Splunk Cloud Services.
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def delete_all_collector_tokens(self, query_params: Dict[str, object] = None) -> object:
        """
        Delete All dsphec tokens for a given tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/ingest/v1beta2/collector/tokens").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, object)

    def delete_collector_token(self, token_name: str, query_params: Dict[str, object] = None) -> object:
        """
        Delete dsphec token by name.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "tokenName": token_name,
        }

        path = Template("/ingest/v1beta2/collector/tokens/${tokenName}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, object)

    def get_collector_token(self, token_name: str, query_params: Dict[str, object] = None) -> HECTokenAccessResponse:
        """
        Get the metadata of a dsphec token by name.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "tokenName": token_name,
        }

        path = Template("/ingest/v1beta2/collector/tokens/${tokenName}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, HECTokenAccessResponse)

    def list_collector_tokens(self, limit: int = None, offset: int = None, query_params: Dict[str, object] = None) -> List[HECTokenAccessResponse]:
        """
        List dsphec tokens for a tenant.
        """
        if query_params is None:
            query_params = {}
        if limit is not None:
            query_params['limit'] = limit
        if offset is not None:
            query_params['offset'] = offset

        path_params = {
        }

        path = Template("/ingest/v1beta2/collector/tokens").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, HECTokenAccessResponse)

    def post_collector_raw(self, host: str = None, index: str = None, source: str = None, sourcetype: str = None, time: str = None, body: str = None, query_params: Dict[str, object] = None) -> HECResponse:
        """
        Sends collector raw events.
        """
        if query_params is None:
            query_params = {}
        if host is not None:
            query_params['host'] = host
        if index is not None:
            query_params['index'] = index
        if source is not None:
            query_params['source'] = source
        if sourcetype is not None:
            query_params['sourcetype'] = sourcetype
        if time is not None:
            query_params['time'] = time

        path_params = {
        }

        path = Template("/ingest/v1beta2/collector/raw").substitute(path_params)
        url = self.base_client.build_url(path)
        data = body
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, HECResponse)

    def post_collector_raw_v1(self, host: str = None, index: str = None, source: str = None, sourcetype: str = None, time: str = None, body: str = None, query_params: Dict[str, object] = None) -> HECResponse:
        """
        Sends collector raw events.
        """
        if query_params is None:
            query_params = {}
        if host is not None:
            query_params['host'] = host
        if index is not None:
            query_params['index'] = index
        if source is not None:
            query_params['source'] = source
        if sourcetype is not None:
            query_params['sourcetype'] = sourcetype
        if time is not None:
            query_params['time'] = time

        path_params = {
        }

        path = Template("/ingest/v1beta2/collector/raw/1.0").substitute(path_params)
        url = self.base_client.build_url(path)
        data = body
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, HECResponse)

    def post_collector_tokens(self, hec_token_create_request: HECTokenCreateRequest, query_params: Dict[str, object] = None) -> HECTokenCreateResponse:
        """
        Creates dsphec tokens.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/ingest/v1beta2/collector/tokens").substitute(path_params)
        url = self.base_client.build_url(path)
        data = hec_token_create_request.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, HECTokenCreateResponse)

    def post_events(self, event: List[Event] = None, query_params: Dict[str, object] = None) -> HTTPResponse:
        """
        Sends events.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/ingest/v1beta2/events").substitute(path_params)
        url = self.base_client.build_url(path)
        data = [e.to_dict() for e in event]
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, HTTPResponse)

    def post_metrics(self, metric_event: List[MetricEvent] = None, query_params: Dict[str, object] = None) -> HTTPResponse:
        """
        Sends metric events.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/ingest/v1beta2/metrics").substitute(path_params)
        url = self.base_client.build_url(path)
        data = [e.to_dict() for e in metric_event]
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, HTTPResponse)

    def put_collector_token(self, token_name: str, hec_token_update_request: HECTokenUpdateRequest, query_params: Dict[str, object] = None) -> HECTokenAccessResponse:
        """
        Update the metadata of a dsphec token by name.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "tokenName": token_name,
        }

        path = Template("/ingest/v1beta2/collector/tokens/${tokenName}").substitute(path_params)
        url = self.base_client.build_url(path)
        data = hec_token_update_request.to_dict()
        response = self.base_client.put(url, json=data, params=query_params)
        return handle_response(response, HECTokenAccessResponse)


