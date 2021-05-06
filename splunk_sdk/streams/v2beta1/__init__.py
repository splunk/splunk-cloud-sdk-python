# coding: utf-8

# flake8: noqa

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
    SDC Service: Data Stream Processing REST API

    Use the Streams service to perform create, read, update, and delete (CRUD) operations on your data pipeline. The Streams service also has metrics and preview session endpoints and gives you full control over your data pipeline.

    OpenAPI spec version: v2beta1.4 
    Generated by: https://openapi-generator.tech
"""


__version__ = "1.0.0"

# import apis into sdk package
from splunk_sdk.streams.v2beta1.gen_data_stream_processing_rest_api_api import DataStreamProcessingRESTAPI

# import models into sdk package
from splunk_sdk.streams.v2beta1.gen_models import ActivatePipelineRequest, \
    ConnectionPatchRequest, \
    ConnectionPutRequest, \
    ConnectionRequest, \
    Source, \
    ConnectionVersionResponse, \
    ConnectionResponse, \
    ConnectionSaveResponse, \
    ConnectorResponse, \
    DeactivatePipelineRequest, \
    DslCompilationRequest, \
    UplPipeline, \
    UplEdge, \
    UplNode, \
    PipelineMigrationInfo, \
    GetInputSchemaRequest, \
    GetOutputSchemaRequest, \
    GroupArgumentsNode, \
    GroupExpandRequest, \
    GroupFunctionArgsNode, \
    GroupFunctionArgsMappingNode, \
    GroupFunctionArguments, \
    GroupFunctionMappings, \
    GroupPatchRequest, \
    GroupPutRequest, \
    GroupRequest, \
    GroupResponse, \
    NodeMetrics, \
    MetricsResponse, \
    PaginatedResponseOfConnectionResponse, \
    PaginatedResponseOfConnectorResponse, \
    PipelineJobStatus, \
    PaginatedResponseOfPipelineJobStatus, \
    PipelineResponse, \
    PaginatedResponseOfPipelineResponse, \
    TemplateResponse, \
    PaginatedResponseOfTemplateResponse, \
    PipelineDeleteResponse, \
    PipelinePatchRequest, \
    PipelineReactivateResponse, \
    PipelineRequest, \
    PipelinesMergeRequest, \
    PreviewNode, \
    PreviewData, \
    PreviewSessionStartRequest, \
    PreviewStartResponse, \
    PreviewState, \
    ReactivatePipelineRequest, \
    Response, \
    SplCompileRequest, \
    TemplatePatchRequest, \
    TemplatePutRequest, \
    TemplateRequest, \
    UplArgument, \
    UplCategory, \
    UplFunction, \
    UplType, \
    UplRegistry, \
    ValidateRequest, \
    ValidateResponse
