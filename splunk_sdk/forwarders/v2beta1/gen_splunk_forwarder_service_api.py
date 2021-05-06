# coding: utf-8

# Copyright © 2021 Splunk, Inc.
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
    SDC Service: Splunk Forwarder Service

    Send data from a Splunk forwarder to the Splunk Forwarder service in Splunk Cloud Services.

    OpenAPI spec version: v2beta1.4 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.forwarders.v2beta1.gen_models import Certificate
from splunk_sdk.forwarders.v2beta1.gen_models import CertificateInfo
from splunk_sdk.forwarders.v2beta1.gen_models import Error


class SplunkForwarderService(BaseService):
    """
    Splunk Forwarder Service
    Version: v2beta1.4
    Send data from a Splunk forwarder to the Splunk Forwarder service in Splunk Cloud Services.
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def add_certificate(self, certificate: Certificate = None, query_params: Dict[str, object] = None) -> CertificateInfo:
        """
        Adds a certificate to a vacant slot on a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/forwarders/v2beta1/certificates").substitute(path_params)
        url = self.base_client.build_url(path)
        data = certificate.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, CertificateInfo)

    def delete_certificate(self, slot: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a certificate on a particular slot on a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "slot": slot,
        }

        path = Template("/forwarders/v2beta1/certificates/${slot}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_certificates(self, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes all certificates on a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/forwarders/v2beta1/certificates").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def list_certificates(self, query_params: Dict[str, object] = None) -> List[CertificateInfo]:
        """
        Returns a list of all certificates for a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/forwarders/v2beta1/certificates").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, CertificateInfo)


