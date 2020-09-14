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

from splunk_sdk.streams import SplCompileRequest, Pipeline, RegistryModel, \
    PipelineRequest, PipelineResponse, \
    PaginatedResponseOfPipelineResponse, ActivatePipelineRequest, \
    DeactivatePipelineRequest, ReactivatePipelineRequest, PipelineReactivateResponse, ValidateRequest, \
    PaginatedResponseOfPipelineJobStatus, GetInputSchemaRequest, GetOutputSchemaRequest, FunctionModel, \
    PreviewState, PreviewSessionStartRequest, UplType, TemplateRequest, \
    MetricsResponse, TemplatePatchRequest, \
    TemplateResponse, PaginatedResponseOfTemplateResponse, PipelinePatchRequest, \
    PreviewStartResponse, PreviewData, \
    PaginatedResponseOfConnectorResponse, PaginatedResponseOfConnectionResponse

from splunk_sdk.base_client import SSCVoidModel


@pytest.mark.usefixtures('test_client')  # NOQA
def test_pipeline_operations(test_client):
    streams = Streams(test_client)
    spl = '| from read_splunk_firehose() | into write_index("", "main");'
    pipe_id = None

    try:
        # compile SPL
        pipeline = streams.compile(SplCompileRequest(spl=spl))
        assert (pipeline is not None)
        assert (isinstance(pipeline, Pipeline))
        assert (len(pipeline.edges) > 0)
        assert (len(pipeline.nodes) > 0)
        assert (len(pipeline.attributes) == 0)

        # create pipeline
        pipe_req = PipelineRequest(data=pipeline,
                                   name="pytest" + str(time.time_ns()),
                                   bypass_validation=True,
                                   description='python SDK integration test',
                                   create_user_id=test_client.context.tenant)

        pipe_resp = streams.create_pipeline(pipe_req)
        assert (pipe_resp is not None)
        assert (isinstance(pipe_resp, PipelineResponse))
        assert (pipe_resp.tenant_id == test_client.context.tenant)
        assert (pipe_resp.id is not None)
        assert (pipe_resp.data is not None)
        assert (pipe_resp.name is not None)
        assert (pipe_resp.description == 'python SDK integration test')

        pipe_id = pipe_resp.id

        # validate
        v_resp = streams.validate_pipeline(ValidateRequest(upl=pipeline))
        assert (v_resp is not None)
        assert (v_resp.success is True)

        # activate pipelines
        activate_data = streams.activate_pipeline(
            id=pipe_resp.id,
            activate_pipeline_request=ActivatePipelineRequest(
                activate_latest_version=True))
        assert (activate_data is not None)

        # get pipeline status
        ps = streams.get_pipelines_status(name=pipe_resp.name)
        assert (ps is not None)
        assert (isinstance(ps, PaginatedResponseOfPipelineJobStatus))

        # create pipeline preview session start request
        preview = streams.start_preview(
            PreviewSessionStartRequest(upl=pipeline, records_limit=100,
                                       records_per_pipeline=5,
                                       session_lifetime_ms=10000,
                                       use_new_data=False))
        assert (preview is not None)
        assert (isinstance(preview, PreviewStartResponse))
        assert (preview.preview_id is not None)

        # get a pipeline preview
        get_preview_state = streams.get_preview_session(
            str(preview.preview_id))
        assert (get_preview_state is not None)
        assert (isinstance(get_preview_state, PreviewState))

        # get pipeline metrics preview
        preview_metrics_resp = \
            streams.get_preview_session_latest_metrics(
                preview_session_id=str(get_preview_state.preview_id))
        assert (preview_metrics_resp is not None)
        assert (isinstance(preview_metrics_resp, MetricsResponse))
        assert (preview_metrics_resp.nodes is not None)

        # get pipeline metrics
        metrics_response = streams.get_pipeline_latest_metrics(id=pipe_id)
        assert (metrics_response is not None)
        assert (isinstance(metrics_response, MetricsResponse))
        assert (metrics_response.nodes is not None)

        #
        # Note: this is not part of v2beta1
        #
        # get all data
        preview_data = streams.get_preview_data(preview_session_id=str(get_preview_state.preview_id))
        assert (preview_data is not None)
        assert (isinstance(preview_data, PreviewData))
        assert (preview_data.preview_id is not None)
        assert (preview_data.records_per_pipeline is not None)
        assert (preview_data.current_number_of_records is not None)

        # get input schema
        node_uuid = pipeline.edges[0].target_node
        port = pipeline.edges[0].target_port
        # src_port = pipeline.edges[0].source_port

        pipeline_type = streams.get_input_schema(GetInputSchemaRequest(
            node_uuid=node_uuid, target_port_name=port, upl_json=pipeline))

        assert (pipeline_type is not None)
        assert (isinstance(pipeline_type, UplType))
        assert (pipeline_type.parameters[0].type == "field")
        assert (pipeline_type.parameters[0].field_name == "timestamp")
        assert (pipeline_type.parameters[0].parameters[0].type == "long")

        # get output schema
        # TODO(dan): need to see the payload looks like atm, 455
        # if there is a key or set of keys we can use that would help
        # in the handle_response call
        # d = streams.get_output_schema(GetOutputSchemaRequest(
        #     node_uuid=node_uuid, source_port_name=src_port, upl_json=pipeline))
        # assert(d is not None)
        # assert(isinstance(d, dict))

        # get pipeline
        pr = streams.get_pipeline(pipe_resp.id)
        assert (pr is not None)
        assert (pr.tenant_id == test_client.context.tenant)
        assert (pr.name == pipe_req.name)
        assert (pr.description == pipe_req.description)

        # get pipelines
        pipelines = streams.list_pipelines()
        assert (pipelines is not None)
        assert (isinstance(pipelines, PaginatedResponseOfPipelineResponse))

        for p in pipelines.items:
            assert (isinstance(p, PipelineResponse))

        #
        # Note: this is not part of v2beta1
        #
        # update/patch pipeline
        updated_pipeline_name = "pytest" + str(time.time_ns())
        updated_pipeline_description = "python SDK integration test update"

        updated_pipeline = streams.patch_pipeline(id=pipe_resp.id, pipeline_patch_request=PipelinePatchRequest(
            name=updated_pipeline_name, description=updated_pipeline_description))
        assert (updated_pipeline is not None)
        assert (updated_pipeline.name is not None)
        assert (updated_pipeline.description == updated_pipeline_description)

        # deactivate pipelines
        if pr.status == "ACTIVATED":
            deactivate_data = streams.deactivate_pipeline(
                id=pipe_resp.id,
                deactivate_pipeline_request=DeactivatePipelineRequest())
            assert (deactivate_data is not None)

        # reactivate pipelines
        prr = streams.reactivate_pipeline(pipe_resp.id, reactivate_pipeline_request=ReactivatePipelineRequest())
        assert (prr is not None)
        assert (isinstance(prr, PipelineReactivateResponse))
        assert (prr.pipeline_reactivation_status in
                ("alreadyActivatedWithCurrentVersion", "activated"))

    finally:
        # delete pipeline
        if pipe_id is not None:
            del_resp = streams.delete_pipeline(pipe_id)
            assert (del_resp is not None)
            print("Delete Response", del_resp)


#
# Note: this is not part of v2beta1
#
@pytest.mark.usefixtures('test_client')  # NOQA
def test_template_operations(test_client):
    streams = Streams(test_client)
    spl = '| from read_splunk_firehose() | into write_index("", "main");'
    template_id = None

    try:
        # compile SPL
        pipeline = streams.compile(SplCompileRequest(spl=spl))
        assert (pipeline is not None)
        assert (isinstance(pipeline, Pipeline))
        assert (len(pipeline.edges) > 0)
        assert (len(pipeline.nodes) > 0)
        assert (len(pipeline.attributes) == 0)

        # create a template
        template_req = TemplateRequest(
            data=pipeline, description="python SDK integration test",
            name="pytest" + str(time.time_ns()))

        template_resp = streams.create_template(template_req)
        assert (template_resp is not None)
        assert (isinstance(template_resp, TemplateResponse))
        assert (template_resp.template_id is not None)
        assert (template_resp.name is not None)
        assert (template_resp.description == 'python SDK integration test')

        template_id = template_resp.template_id

        # get template
        _template_resp = streams.get_template(template_id=template_id)
        assert (_template_resp is not None)
        assert (_template_resp.template_id == template_id)
        assert (_template_resp.description == template_resp.description)
        assert (_template_resp.name == template_resp.name)

        # get all templates
        pgt = streams.list_templates()
        assert (pgt is not None)
        assert (isinstance(pgt, PaginatedResponseOfTemplateResponse))

        # update template
        update_req = TemplatePatchRequest(
            data=template_req.data,
            description="python SDK template update test",
            name=template_req.name)

        update_resp = streams.update_template(template_id=template_id, template_patch_request=update_req)
        assert (update_resp is not None)
        assert (isinstance(update_resp, TemplateResponse))
        assert (update_resp.description == "python SDK template update test")
        assert (update_resp.name == template_req.name)

    finally:
        # delete template
        if template_id is not None:
            del_resp = streams.delete_template(template_id)
            assert (del_resp is not None)
            assert (isinstance(del_resp, SSCVoidModel))


@pytest.mark.usefixtures('test_client')  # NOQA
def test_get_upl_registry(test_client):
    streams = Streams(test_client)
    reg_model = streams.get_registry()
    assert (reg_model is not None)
    assert (isinstance(reg_model, RegistryModel))

    for c in reg_model.categories:
        assert (c is not None)
        assert (isinstance(c, str))

    for n, f in enumerate(reg_model.functions):
        assert (f is not None)
        assert (isinstance(f, FunctionModel))
        assert (f.attributes is not None)
        assert (f.arguments is not None)
        assert (f.outputs is not None)


@pytest.mark.usefixtures('test_client')  # NOQA
def test_connection_operations(test_client):
    # NOTE(dan): create and delete will be tested outside int-tests
    streams = Streams(test_client)

    # get connectors
    connectors = streams.list_connectors()
    assert (connectors is not None)
    assert (isinstance(connectors, PaginatedResponseOfConnectorResponse))
    assert (connectors.items is not None)

    for c in connectors.items:
        assert (c is not None)
        assert (c.name is not None)
        assert (c.id is not None)
        assert (c.description is not None)
        assert (len(c.functions) > 0)

        # get connections
        connections = streams.list_connections(c.id)
        assert (connections is not None)
        assert (isinstance(connections, PaginatedResponseOfConnectionResponse))

        for conn in connections.items:
            assert (conn.connector_name is not None)
            assert (conn.connector_id is not None)
