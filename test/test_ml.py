# Copyright © 2019 Splunk, Inc.
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os

import pytest
import time
from requests import Response

from test.fixtures import get_test_client_ml as test_client_ml  # NOQA

from splunk_sdk.common.sscmodel import SSCModel

from splunk_sdk.ml import \
    MachineLearningServiceMLAPI

from splunk_sdk.ml.gen_models import FitTask, Fields, Workflow, InputData, \
    OutputData, SPL, Events, WorkflowBuild, WorkflowRun,\
    WorkflowsGetResponse, WorkflowDeployment, DeploymentSpec

import logging

logger = logging.getLogger()


host_train = "server_power_train_ef5wlcd4njiovmdl"
host_test = "server_power_test_ef5wlcd4njiovmdl"
host_out = "server_power_out_ef5wlcd4njiovmdl"

workflow_name = "PredictServerPowerConsumption"
build_spl = "| from mlapishowcase.mlapishowcase where host=\"%s\"" % host_train
run_spl = "| from mlapishowcase.mlapishowcase where host=\"%s\"" % host_test
module = "mlapishowcase"


def _create_fit_task():
    return FitTask(algorithm="LinearRegression",
                   fields=Fields(features=[
                       "total-unhalted_core_cycles",
                       "total-instructions_retired",
                       "total-last_level_cache_references",
                       "total-memory_bus_transactions",
                       "total-cpu-utilization",
                       "total-disk-accesses",
                       "total-disk-blocks",
                       "total-disk-utilization"
                   ], target="ac_power"),
                   name="linearregression",
                   output_transformer="example_server_power",
                   parameters={"fit_intercept": True, "normalize": False})


def _create_workflow_build():
    return WorkflowBuild(input=InputData(kind='SPL',
                                         source=SPL(module=module,
                                                    query=build_spl,
                                                    extract_all_fields=True,
                                                    query_parameters={
                                                        "earliest": "0",
                                                        "latest": "now"},
                                                    )))


def _create_workflow_run():
    return WorkflowRun(input=InputData(kind='SPL',
                                       source=SPL(module=module,
                                                  query=run_spl,
                                                  extract_all_fields=True,
                                                  query_parameters={
                                                      "earliest": "0",
                                                      "latest": "now"})),
                       output=OutputData(kind='Events',
                                         destination=Events(
                                             attributes={
                                                 "index": "mlapishowcase",
                                                 "module": "mlapishowcase",
                                             },
                                             source="mlapi-showcase",
                                             host=host_out)))


@pytest.mark.usefixtures('test_client_ml')  # NOQA
@pytest.mark.skipif(not os.getenv('SPLUNK_TENANT_ML'), reason="ML tests require a preconfigured tenant")
def test_workflow_operations(test_client_ml):
    ml = MachineLearningServiceMLAPI(test_client_ml)
    assert(ml is not None)
    flow_id = None
    build_id = None
    run_id = None
    wd_id = None
    try:
        # create workflow
        task = _create_fit_task()
        flow = Workflow(tasks=[task], name="PredictServerPowerConsumption")
        _flow = ml.create_workflow(flow)
        assert(_flow is not None)
        assert(isinstance(_flow, Workflow))
        flow_id = _flow.id

        # get workflow
        _flow = ml.get_workflow(flow_id)
        assert (_flow is not None)
        assert (isinstance(_flow, Workflow))

        # get workflows
        flows = ml.list_workflows()
        assert(flows is not None)
        assert(isinstance(flows, list))
        assert(isinstance(flows[0], WorkflowsGetResponse))

        # create workflow build
        build = _create_workflow_build()
        _build = ml.create_workflow_build(flow_id, build)
        assert(_build is not None)
        assert(isinstance(_build, WorkflowBuild))
        build_id = _build.id

        # get workflow build
        _build = ml.get_workflow_build(flow_id, build_id)
        assert(_build is not None)
        assert(isinstance(_build, WorkflowBuild))

        retry = 0
        limit = 10
        while retry <= limit:
            logger.debug("build status:" + _build.status)
            if _build.status != "success":
                _build = ml.get_workflow_build(flow_id, build_id)
                time.sleep(5)
                retry += 1
            else:
                build_id = _build.id
                break

        # create workflow run
        run = _create_workflow_run()
        _run = ml.create_workflow_run(id=flow_id, build_id=build_id,
                                      workflow_run=run)
        assert(_run is not None)
        assert(isinstance(_run, WorkflowRun))
        run_id = _run.id

        # get workflow run
        _run = ml.get_workflow_run(id=flow_id, build_id=build_id,
                                   run_id=run_id)
        assert (_run is not None)
        assert (isinstance(_run, WorkflowRun))

        # create workflow deployment
        ds = DeploymentSpec()
        wd = WorkflowDeployment(spec=ds)
        _wd = ml.create_workflow_deployment(id=flow_id, build_id=build_id,
                                            workflow_deployment=wd)
        wd_id = _wd.id

        assert(_wd is not None)
        assert(isinstance(_wd, WorkflowDeployment))

        # get workflow deployment
        retry = 0
        limit = 10
        while retry <= limit:
            logger.debug("Workflow deployment id: " + _wd.id)
            if _wd.id is None:
                _wd = ml.get_workflow_deployment(id=wd_id, build_id=build_id,
                                                 deployment_id=wd_id)
                assert (_wd is not None)
                assert (isinstance(_wd, WorkflowDeployment))
                time.sleep(5)
                retry += 1
            else:
                wd_id = _wd.id
                break

        # get workflow deployments
        deployments = ml.list_workflow_deployments(id=wd_id, build_id=build_id)
        assert (deployments is not None)
        assert (isinstance(deployments, list))

        for d in deployments:
            assert(isinstance(d, WorkflowDeployment))

    finally:
        # TODO(dan): explore retries later, this is failing atm
        # delete workflow deployment
        response = ml.delete_workflow_deployment(id=flow_id, build_id=build_id,
                                                 deployment_id=wd_id).response
        assert (response is not None)
        assert (response.status_code == 204)

        # delete workflow run
        response = ml.delete_workflow_run(id=flow_id, build_id=build_id,
                                          run_id=run_id).response
        assert (response is not None)
        assert (response.status_code == 204)

        # delete workflow build
        response = ml.delete_workflow_build(flow_id, build_id).response
        assert(response is not None)
        assert(response.status_code == 204)

        # delete workflow
        response = ml.delete_workflow(flow_id).response
        assert(response is not None)
        assert(response.status_code == 204)

