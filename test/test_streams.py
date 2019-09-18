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
import json

from requests import Response

from test.fixtures import get_test_client as test_client  # NOQA

from splunk_sdk.streams import DataStreamProcessingRESTAPI as Streams

from splunk_sdk.streams import DslCompilationRequest, UplPipeline, \
    PipelineRequest, PipelineResponse, PipelineDeleteResponse, \
    PaginatedResponseOfPipelineResponse, ActivatePipelineRequest, \
    DeactivatePipelineRequest, PipelineReactivateResponse, ValidateRequest, \
    PaginatedResponseOfPipelineJobStatus, GetInputSchemaRequest, \
    PreviewState, PreviewSessionStartRequest, UplType, TemplateRequest, \
    MetricsResponse, PipelinesMergeRequest, TemplatePatchRequest, \
    TemplateResponse, PaginatedResponseOfTemplateResponse, \
    UplRegistry, UplCategory, PreviewStartResponse, PreviewData, \
    PaginatedResponseOfConnectorResponse, PaginatedResponseOfConnectionResponse

from splunk_sdk.base_client import SSCVoidModel


@pytest.mark.usefixtures('test_client')  # NOQA
def test_pipeline_operations(test_client):
    streams = Streams(test_client)
    dsl = 'events = read-splunk-firehose(); write-index(events, "index", "main");'
    pipe_id = None

    try:
        # compile DSL
        upl = streams.compile_dsl(DslCompilationRequest(dsl=dsl))
        assert(upl is not None)
        assert(isinstance(upl, UplPipeline))
        assert(len(upl.edges) > 0)
        assert(len(upl.nodes) > 0)
        assert(len(upl.root_node) == 1)

        # create pipeline
        pipe_req = PipelineRequest(data=upl,
                                   name="pytest" + str(time.time_ns()),
                                   bypass_validation=True,
                                   description='python SDK integration test',
                                   create_user_id=test_client.context.tenant,)

        pipe_resp = streams.create_pipeline(pipe_req)
        assert(pipe_resp is not None)
        assert(isinstance(pipe_resp, PipelineResponse))
        assert(pipe_resp.tenant_id == test_client.context.tenant)
        assert(pipe_resp.id is not None)

        pipe_id = pipe_resp.id

        # validate
        v_resp = streams.validate_pipeline(ValidateRequest(upl=upl))
        assert(v_resp is not None)
        assert(v_resp.success is True)

        # activate pipelines
        activate_data = streams.activate_pipeline(
            id=pipe_resp.id,
            activate_pipeline_request=ActivatePipelineRequest(
                activate_latest_version=True))
        assert(activate_data is not None)

        # get pipeline status
        ps = streams.get_pipelines_status(name=pipe_resp.name)
        assert(ps is not None)
        assert(isinstance(ps, PaginatedResponseOfPipelineJobStatus))

        #
        # Note: this is not part of v2beta1
        #
        # create pipeline preview session start request
        preview = streams.start_preview(
            PreviewSessionStartRequest(upl=upl, records_limit=100,
                                       records_per_pipeline=5,
                                       session_lifetime_ms=10000,
                                       use_new_data=False))
        assert(preview is not None)
        assert(isinstance(preview, PreviewStartResponse))
        assert(preview.preview_id is not None)

        # get a pipeline preview
        get_preview_state = streams.get_preview_session(
            str(preview.preview_id))
        assert (get_preview_state is not None)
        assert (isinstance(get_preview_state, PreviewState))

        # delete preview
        # TODO(dan): sometimes returns 404 often
        #   No longer part of spec
        # if get_preview_state.preview_id is not None:
        #     preview_state = streams.delete_pipeline_preview(
        #         str(get_preview_state.preview_id))
        #     assert(preview_state is not None)
        #     assert(isinstance(preview_state, PreviewState))

        # get pipeline metrics preview
        preview_metrics_resp = \
            streams.get_preview_session_latest_metrics(
                str(get_preview_state.preview_id))

        assert(preview_metrics_resp is not None)
        assert(isinstance(preview_metrics_resp, MetricsResponse))
        assert(preview_metrics_resp.nodes is not None)

        # get pipeline metrics
        metrics_response = streams.get_pipeline_latest_metrics(pipe_id)
        assert(metrics_response is not None)
        assert(isinstance(metrics_response, MetricsResponse))
        assert(metrics_response.nodes is not None)

        #
        # Note: this is not part of v2beta1
        #
        # get all data
        preview_data = streams.get_preview_data(str(get_preview_state.preview_id))
        assert(preview_data is not None)
        assert(isinstance(preview_data, PreviewData))

        # get input schema
        # TODO(dan): we have bugs open for this response = <Response [500]>
        # node_uuid = upl.get('edges')[0].get('target_node')
        # port = upl.get('edges')[0].get('target_port')
        # # src_port = upl.edges[0].source_port
        #
        # upl_type = streams.get_input_schema(GetInputSchemaRequest(
        #     node_uuid=node_uuid, target_port_name=port, upl_json=upl))
        #
        # assert(upl_type is not None)
        # assert(isinstance(upl_type, UplType))
        # assert(upl_type.parameters[0].type == "field")
        # assert(upl_type.parameters[0].field_name == "timestamp")
        # assert(upl_type.parameters[0].parameters[0].type == "long")

        # get output schema
        # TODO(dan): need to see the payload looks like atm, 455
        # if there is a key or set of keys we can use that would help
        # in the handle_response call
        # d = streams.get_output_schema(GetOutputSchemaRequest(
        #     node_uuid=node_uuid, source_port_name=src_port, upl_json=upl))
        # assert(d is not None)
        # assert(isinstance(d, dict))

        # get pipeline
        pr = streams.get_pipeline(pipe_resp.id)
        assert(pr is not None)
        assert(pr.tenant_id == test_client.context.tenant)
        assert(pr.name == pipe_req.name)
        assert(pr.description == pipe_req.description)

        # get pipelines
        pipelines = streams.list_pipelines()
        assert (pipelines is not None)
        assert (isinstance(pipelines, PaginatedResponseOfPipelineResponse))

        for p in pipelines.items:
            assert (isinstance(p, PipelineResponse))

        #
        # Note: this is not part of v2beta1
        #
        # update pipeline
        # TODO(dan): there used to be an update model
        # pipe_req.name = "pytest" + str(time.time_ns())
        # pipe_req.description = "python SDK integration test update"
        #
        # upr = streams.update_pipeline5(pipe_resp.id, pipe_req)
        # assert(upr is not None)
        # assert(upr.name == pipe_req.name)
        # assert(upr.description == pipe_req.description)

        # deactivate pipelines
        if pr.status == "ACTIVATED":
            deactivate_data = streams.deactivate_pipeline(
                id=pipe_resp.id,
                deactivate_pipeline_request=DeactivatePipelineRequest())
            assert(deactivate_data is not None)

        # reactivate pipelines
        prr = streams.reactivate_pipeline(pipe_resp.id)
        assert(prr is not None)
        assert(isinstance(prr, PipelineReactivateResponse))
        assert(prr.pipeline_reactivation_status in
               ("alreadyActivatedWithCurrentVersion", "activated"))

    finally:
        # delete pipeline
        if pipe_id is not None:
            del_resp = streams.delete_pipeline(pipe_id)
            assert(del_resp is not None)
            assert(isinstance(del_resp, PipelineDeleteResponse))


@pytest.mark.usefixtures('test_client')  # NOQA
def test_merge_pipeline(test_client):
    streams = Streams(test_client)
    dsl = 'events = read-splunk-firehose(); write-index(events, "main", "index");'
    pipe_id = None

    try:
        # compile DSL
        upl1 = streams.compile_dsl(DslCompilationRequest(dsl=dsl))
        assert(upl1 is not None)
        assert(isinstance(upl1, UplPipeline))
        assert(len(upl1.edges) > 0)
        assert(len(upl1.nodes) > 0)
        assert(len(upl1.root_node) == 1)

        # compile DSL
        upl5 = streams.compile_dsl(DslCompilationRequest(dsl=dsl))
        assert (upl5 is not None)
        assert (isinstance(upl5, UplPipeline))
        assert (len(upl5.edges) > 0)
        assert (len(upl5.nodes) > 0)
        assert (len(upl5.root_node) == 1)

        # merge pipelines
        upl = streams.merge_pipelines(
            PipelinesMergeRequest(input_tree=upl1, main_tree=upl5,
                                  target_port=upl5.edges[0].target_port,
                                  target_node=upl5.edges[0].target_node))
        assert(upl is not None)
        assert(isinstance(upl, UplPipeline))

        # create a pipeline
        pipe_req = PipelineRequest(data=upl,
                                   name="pytest" + str(time.time_ns()),
                                   bypass_validation=True,
                                   description='python SDK integration test',
                                   create_user_id=test_client.context.tenant, )

        pipe_resp = streams.create_pipeline(pipe_req)
        assert (pipe_resp is not None)
        assert (isinstance(pipe_resp, PipelineResponse))
        assert (pipe_resp.tenant_id == test_client.context.tenant)
        assert (pipe_resp.id is not None)
        pipe_id = pipe_resp.id

    finally:
        # delete pipeline
        if pipe_id is not None:
            del_resp = streams.delete_pipeline(pipe_id)
            assert(del_resp is not None)
            assert(isinstance(del_resp, PipelineDeleteResponse))

#
# Note: this is not part of v2beta1
#
@pytest.mark.usefixtures('test_client')  # NOQA
def test_template_operations(test_client):
    streams = Streams(test_client)
    dsl = 'events = read-splunk-firehose(); write-index(events, "index", "main");'
    template_id = None

    try:
        # compile dsl
        upl = streams.compile_dsl(DslCompilationRequest(dsl=dsl))
        assert (upl is not None)
        assert (isinstance(upl, UplPipeline))
        assert (len(upl.edges) > 0)
        assert (len(upl.nodes) > 0)
        assert (len(upl.root_node) == 1)

        # create a template
        template_req = TemplateRequest(
            data=upl, description="python SDK integration test",
            name="pytest" + str(time.time_ns()))

        template_resp = streams.create_template(template_req)
        assert(template_resp is not None)
        assert(isinstance(template_resp, TemplateResponse))
        template_id = template_resp.template_id
        assert(template_id is not None)

        # get template
        _template_resp = streams.get_template(template_id=template_id)
        assert(_template_resp is not None)
        assert(_template_resp.template_id == template_resp.template_id)
        assert(_template_resp.description == template_resp.description)
        assert(_template_resp.name == template_resp.name)

        # get all templates
        pgt = streams.list_templates()
        assert(pgt is not None)
        assert(isinstance(pgt, PaginatedResponseOfTemplateResponse))

        # update template
        update_req = TemplatePatchRequest(
            data=template_req.data,
            description="python SDK template update test",
            name=template_req.name)

        update_resp = streams.update_template(template_id, update_req)
        assert(update_resp is not None)
        assert(isinstance(update_resp, TemplateResponse))
        assert(update_resp.description == "python SDK template update test")
        assert(update_resp.name == template_req.name)

    finally:
        # delete template
        if template_id is not None:
            del_resp = streams.delete_template(template_id)
            assert (del_resp is not None)
            assert (isinstance(del_resp, SSCVoidModel))


@pytest.mark.usefixtures('test_client')  # NOQA
def test_get_upl_registry(test_client):
    streams = Streams(test_client)
    upl_reg = streams.get_registry()
    assert(upl_reg is not None)
    assert(isinstance(upl_reg, UplRegistry))

    for c in upl_reg.categories:
        assert(c is not None)
        assert(isinstance(c, UplCategory))
        assert(c.name is not None)
        assert(c.id is not None)

    for n, f in enumerate(upl_reg.functions):
        assert(f is not None)
        if f.id == 'receive-from-ingest-rest-api':
            group_id = f.attributes['application']['groupId']
            assert(group_id is not None)

            group = streams.get_group(group_id)
            assert(group is not None)
            assert(group.name is not None)
            assert(group.create_date is not None)
            assert(group.output_type is not None)


@pytest.mark.usefixtures('test_client')  # NOQA
def test_connection_operations(test_client):
    # NOTE(dan): create and delete will be tested outside int-tests
    streams = Streams(test_client)

    # get connectors
    connectors = streams.list_connectors()
    assert(connectors is not None)
    assert(isinstance(connectors, PaginatedResponseOfConnectorResponse))
    assert(connectors.items is not None)

    for c in connectors.items:
        assert(c is not None)
        assert(c.name is not None)
        assert(c.id is not None)

        # get connections
        connections = streams.list_connections(c.id)
        assert(connections is not None)
        assert(isinstance(connections, PaginatedResponseOfConnectionResponse))

        for conn in connections.items:
            assert(conn.connector_name is not None)
            assert(conn.connector_id is not None)
