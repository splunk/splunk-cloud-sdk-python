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
    SDC Service: Machine Learning Service (ML API)

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    OpenAPI spec version: v2beta1.1 (recommended default)
    Generated by: https://openapi-generator.tech
"""


from requests import Response
from string import Template
from typing import List, Dict

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.common.sscmodel import SSCModel, SSCVoidModel

from splunk_sdk.ml.gen_models import Error
from splunk_sdk.ml.gen_models import Workflow
from splunk_sdk.ml.gen_models import WorkflowBuild
from splunk_sdk.ml.gen_models import WorkflowBuildError
from splunk_sdk.ml.gen_models import WorkflowBuildLog
from splunk_sdk.ml.gen_models import WorkflowDeployment
from splunk_sdk.ml.gen_models import WorkflowDeploymentError
from splunk_sdk.ml.gen_models import WorkflowDeploymentLog
from splunk_sdk.ml.gen_models import WorkflowInference
from splunk_sdk.ml.gen_models import WorkflowRun
from splunk_sdk.ml.gen_models import WorkflowRunError
from splunk_sdk.ml.gen_models import WorkflowRunLog
from splunk_sdk.ml.gen_models import WorkflowsGetResponse


class MachineLearningServiceMLAPI(BaseService):
    """
    Machine Learning Service (ML API)
    Version: v2beta1.1
    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
    """

    def __init__(self, base_client):
        super().__init__(base_client)

    def create_workflow(self, workflow: Workflow, query_params: Dict[str, object] = None) -> Workflow:
        """
        Creates a workflow configuration.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/ml/v2beta1/workflows").substitute(path_params)
        url = self.base_client.build_url(path)
        data = workflow.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, Workflow)

    def create_workflow_build(self, id: str, workflow_build: WorkflowBuild, query_params: Dict[str, object] = None) -> WorkflowBuild:
        """
        Creates a workflow build.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds").substitute(path_params)
        url = self.base_client.build_url(path)
        data = workflow_build.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, WorkflowBuild)

    def create_workflow_deployment(self, id: str, build_id: str, workflow_deployment: WorkflowDeployment, query_params: Dict[str, object] = None) -> WorkflowDeployment:
        """
        Creates a workflow deployment.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments").substitute(path_params)
        url = self.base_client.build_url(path)
        data = workflow_deployment.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, WorkflowDeployment)

    def create_workflow_inference(self, id: str, build_id: str, deployment_id: str, workflow_inference: WorkflowInference, query_params: Dict[str, object] = None) -> WorkflowInference:
        """
        Creates a workflow inference request.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "deploymentId": deployment_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments/${deploymentId}/inference").substitute(path_params)
        url = self.base_client.build_url(path)
        data = workflow_inference.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, WorkflowInference)

    def create_workflow_run(self, id: str, build_id: str, workflow_run: WorkflowRun, query_params: Dict[str, object] = None) -> WorkflowRun:
        """
        Creates a workflow run.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/runs").substitute(path_params)
        url = self.base_client.build_url(path)
        data = workflow_run.to_dict()
        response = self.base_client.post(url, json=data, params=query_params)
        return handle_response(response, WorkflowRun)

    def delete_workflow(self, id: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a workflow configuration.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
        }

        path = Template("/ml/v2beta1/workflows/${id}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_workflow_build(self, id: str, build_id: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a workflow build.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_workflow_deployment(self, id: str, build_id: str, deployment_id: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a workflow deployment.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "deploymentId": deployment_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments/${deploymentId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def delete_workflow_run(self, id: str, build_id: str, run_id: str, query_params: Dict[str, object] = None) -> SSCVoidModel:
        """
        Removes a workflow run.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "runId": run_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/runs/${runId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.delete(url, params=query_params)
        return handle_response(response, )

    def get_workflow(self, id: str, query_params: Dict[str, object] = None) -> Workflow:
        """
        Returns a workflow configuration.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
        }

        path = Template("/ml/v2beta1/workflows/${id}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, Workflow)

    def get_workflow_build(self, id: str, build_id: str, query_params: Dict[str, object] = None) -> WorkflowBuild:
        """
        Returns the status of a workflow build.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowBuild)

    def get_workflow_build_error(self, id: str, build_id: str, query_params: Dict[str, object] = None) -> WorkflowBuildError:
        """
        Returns a list of workflow errors.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/errors").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowBuildError)

    def get_workflow_build_log(self, id: str, build_id: str, query_params: Dict[str, object] = None) -> WorkflowBuildLog:
        """
        Returns the logs from a workflow build.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/logs").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowBuildLog)

    def get_workflow_deployment(self, id: str, build_id: str, deployment_id: str, query_params: Dict[str, object] = None) -> WorkflowDeployment:
        """
        Returns the status of a workflow deployment.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "deploymentId": deployment_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments/${deploymentId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowDeployment)

    def get_workflow_deployment_error(self, id: str, build_id: str, deployment_id: str, query_params: Dict[str, object] = None) -> WorkflowDeploymentError:
        """
        Returns a list of workflow deployment errors.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "deploymentId": deployment_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments/${deploymentId}/errors").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowDeploymentError)

    def get_workflow_deployment_log(self, id: str, build_id: str, deployment_id: str, query_params: Dict[str, object] = None) -> WorkflowDeploymentLog:
        """
        Returns the logs from a workflow deployment.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "deploymentId": deployment_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments/${deploymentId}/logs").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowDeploymentLog)

    def get_workflow_run(self, id: str, build_id: str, run_id: str, query_params: Dict[str, object] = None) -> WorkflowRun:
        """
        Returns the status of a workflow run.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "runId": run_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/runs/${runId}").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowRun)

    def get_workflow_run_error(self, id: str, build_id: str, run_id: str, query_params: Dict[str, object] = None) -> WorkflowRunError:
        """
        Returns the errors for a workflow run.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "runId": run_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/runs/${runId}/errors").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowRunError)

    def get_workflow_run_log(self, id: str, build_id: str, run_id: str, query_params: Dict[str, object] = None) -> WorkflowRunLog:
        """
        Returns the logs for a workflow run.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
            "runId": run_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/runs/${runId}/logs").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowRunLog)

    def list_workflow_builds(self, id: str, query_params: Dict[str, object] = None) -> List[WorkflowBuild]:
        """
        Returns a list of workflow builds.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowBuild)

    def list_workflow_deployments(self, id: str, build_id: str, query_params: Dict[str, object] = None) -> List[WorkflowDeployment]:
        """
        Returns a list of workflow deployments.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/deployments").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowDeployment)

    def list_workflow_runs(self, id: str, build_id: str, query_params: Dict[str, object] = None) -> List[WorkflowRun]:
        """
        Returns a list of workflow runs.
        """
        if query_params is None:
            query_params = {}

        path_params = {
            "id": id,
            "buildId": build_id,
        }

        path = Template("/ml/v2beta1/workflows/${id}/builds/${buildId}/runs").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowRun)

    def list_workflows(self, query_params: Dict[str, object] = None) -> List[WorkflowsGetResponse]:
        """
        Returns a list of workflow configurations.
        """
        if query_params is None:
            query_params = {}

        path_params = {
        }

        path = Template("/ml/v2beta1/workflows").substitute(path_params)
        url = self.base_client.build_url(path)
        response = self.base_client.get(url, params=query_params)
        return handle_response(response, WorkflowsGetResponse)


