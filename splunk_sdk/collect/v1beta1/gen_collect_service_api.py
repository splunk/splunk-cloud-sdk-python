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
    SDC Service: Collect Service

    With the Collect service in Splunk Cloud Services, you can manage how data collection jobs ingest event and metric data.

    OpenAPI spec version: v1beta1.7 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.collect.v1beta1.gen_models import DeleteJobsResponse
from splunk_sdk.collect.v1beta1.gen_models import Error
from splunk_sdk.collect.v1beta1.gen_models import Job
from splunk_sdk.collect.v1beta1.gen_models import JobPatch
from splunk_sdk.collect.v1beta1.gen_models import JobsPatch
from splunk_sdk.collect.v1beta1.gen_models import ListJobsResponse
from splunk_sdk.collect.v1beta1.gen_models import PatchJobsResponse
from splunk_sdk.collect.v1beta1.gen_models import SingleJobResponse


class CollectService(BaseService):
    """
    Collect Service
    Version: v1beta1.7
    With the Collect service in Splunk Cloud Services, you can manage how data collection jobs ingest event and metric data.
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def create_job(self, job: Job, query_params: Dict[str, object] = None) -> SingleJobResponse:
        """
        Creates a job
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/collect/v1beta1/jobs").substitute(path_params)
        url = self.base_client.build_url(path)
        data = job.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, SingleJobResponse)

    def delete_job(self, job_id: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a job based on the job ID.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "jobId": job_id,
        }

        path = Template("/collect/v1beta1/jobs/${jobId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_jobs(self, query_params: Dict[str, object] = None) -> DeleteJobsResponse:
        """
        Removes all jobs on a tenant.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/collect/v1beta1/jobs").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, DeleteJobsResponse)

    def get_job(self, job_id: str, query_params: Dict[str, object] = None) -> SingleJobResponse:
        """
        Returns a job based on the job ID.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "jobId": job_id,
        }

        path = Template("/collect/v1beta1/jobs/${jobId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, SingleJobResponse)

    def list_jobs(self, connector_id: str = None, query_params: Dict[str, object] = None) -> ListJobsResponse:
        """
        Returns a list of all jobs that belong to a tenant.
        """
        if query_params is None:
            query_params = {}
        if connector_id is not None:
            query_params['connectorID'] = connector_id

        path_params = {
        }

        path = Template("/collect/v1beta1/jobs").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, ListJobsResponse)

    def patch_job(self, job_id: str, job_patch: JobPatch, query_params: Dict[str, object] = None) -> SingleJobResponse:
        """
        Modifies a job based on the job ID.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "jobId": job_id,
        }

        path = Template("/collect/v1beta1/jobs/${jobId}").substitute(path_params)
        url = self.base_client.build_url(path)
        data = job_patch.to_dict()
        response = self.base_client.patch(url, json=data, params=query_params)
        return handle_response(response, SingleJobResponse)

    def patch_jobs(self, jobs_patch: JobsPatch, connector_id: str = None, job_i_ds: List[str] = None, query_params: Dict[str, object] = None) -> PatchJobsResponse:
        """
        Finds all jobs that match the query and modifies the with the changes specified in the request.
        """
        if query_params is None:
            query_params = {}
        if connector_id is not None:
            query_params['connectorID'] = connector_id
        if job_i_ds is not None:
            query_params['jobIDs'] = job_i_ds

        path_params = {
        }

        path = Template("/collect/v1beta1/jobs").substitute(path_params)
        url = self.base_client.build_url(path)
        data = jobs_patch.to_dict()
        response = self.base_client.patch(url, json=data, params=query_params)
        return handle_response(response, PatchJobsResponse)


