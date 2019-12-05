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

import os
import pytest
import time
import csv
import json
import logging

from test.fixtures import get_test_client_ml as test_client_ml  # NOQA
from splunk_sdk.ingest import IngestAPI, Event
from splunk_sdk.ml import MachineLearning, FitTask, Fields, \
    Workflow, InputData, OutputData, RawData, OutputDataDestination, \
    WorkflowBuild, WorkflowRun, WorkflowsGetResponse, WorkflowDeployment, \
    DeploymentSpec


logger = logging.getLogger()

ML_DATA_FILE = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                            "data/ml/iris.csv")

Base64_DATA = "LHNlcGFsX2xlbmd0aCxzZXBhbF93aWR0aCxwZXRhbF9sZW5ndGgscGV0YWxfd2lkdGgsc3BlY2llcw0KMCw1LjEsMy41LDEuNCwwLjIsSXJpcyBTZXRvc2ENCjUwLDcuMCwzLjIsNC43LDEuNCxJcmlzIFZlcnNpY29sb3INCjEwMCw2LjMsMy4zLDYuMCwyLjUsSXJpcyBWaXJnaW5pY2ENCg=="

SOURCE = 'pythonsdk-tests'
SOURCETYPE = 'json'


def _parse_csv(file):
    events = []
    with open(file) as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        for row in reader:
            #  v needs to be tested for a float or string
            data = {}
            for k, v in zip(headers, row):
                try:
                    v = float(v)
                except ValueError:
                    pass
                data[k] = v
            payload = json.dumps(data)
            events.append(Event(body=payload, sourcetype=SOURCETYPE,
                                source=SOURCE, attributes={'index': 'main'}))
    return events


def _create_fit_tasks():
    f1 = FitTask(name="PCA",
                 algorithm="PCA",
                 fields=Fields(features=[
                     "petal_length",
                     "petal_width",
                     "sepal_length",
                     "sepal_width"],
                     target="",
                     created=[
                         "PC_1",
                         "PC_2",
                         "PC_3"]
                 ),
                 output_transformer="PCA_model",
                 parameters={"k": 3})

    f2 = FitTask(name="RandomForestClassifier",
                 algorithm="RandomForestClassifier",
                 fields=Fields(features=[
                      "PC_1",
                      "PC_2",
                      "PC_3"],
                     target="species",
                     created=["predicted(species)"]),
                 output_transformer="RFC_model",
                 parameters={"n_estimators": 25,
                             "max_depth": 10,
                             "min_samples_split": 5,
                             "max_features": "auto",
                             "criterion": "gini"})
    return [f1, f2]


def _create_workflow_build():
    return WorkflowBuild(name="test_workflowBuild",
                         input=InputData(kind='RawData',
                                         source=RawData(data=Base64_DATA)))


def _create_workflow_run():
    return WorkflowRun(name="test_workflowRun",
                       input=InputData(kind='RawData',
                                       source=RawData(data=Base64_DATA)),
                       output=OutputData(kind='S3',
                                         destination=OutputDataDestination(
                                             key="iris.csv")))


@pytest.mark.usefixtures('test_client_ml')  # NOQA
def test_ingest_ml(test_client_ml):
    ingest = IngestAPI(test_client_ml)
    events = _parse_csv(ML_DATA_FILE)

    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    events_packets = chunks(events, 1000)

    for packet in events_packets:
        # this line changes
        ingest.post_events(packet)
        time.sleep(1)


@pytest.mark.usefixtures('test_client_ml')  # NOQA
@pytest.mark.skipif(not os.getenv('SPLUNK_TENANT_ML'), reason="ML tests require a preconfigured tenant")
def test_workflow_operations(test_client_ml):
    ml = MachineLearning(test_client_ml)
    assert(ml is not None)
    flow_id = None
    build_id = None
    run_id = None
    wd_id = None
    try:
        # create workflow
        tasks = _create_fit_tasks()
        flow = Workflow(tasks=tasks, name="test_workflow")
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
                time.sleep(20)
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
