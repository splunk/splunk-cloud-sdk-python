# coding: utf-8

# flake8: noqa

# Copyright © 2022 Splunk, Inc.
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

    OpenAPI spec version: v4alpha1.1 
    Generated by: https://openapi-generator.tech
"""


__version__ = "1.0.0"

# import apis into sdk package
from splunk_sdk.streams.v4alpha1.gen_data_stream_processing_rest_api_api import DataStreamProcessingRESTAPI

# import models into sdk package
from splunk_sdk.streams.v4alpha1.gen_models import ActivatePipelineRequest, \
    ArgumentModel, \
    AutopilotActivationDeactivationResponse, \
    ConnectionPatchRequest, \
    ConnectionPutRequest, \
    ConnectionRequest, \
    Source, \
    ConnectionVersionResponse, \
    ConnectionResponse, \
    ConnectionSaveResponse, \
    ConnectorResponse, \
    DeactivatePipelineRequest, \
    Pipeline, \
    PipelineEdge, \
    PipelineNode, \
    PipelineMigrationInfo, \
    DecompileRequest, \
    DecompileResponse, \
    ErrorResponse, \
    UploadFileResponse, \
    FilesMetaDataResponse, \
    FunctionModel, \
    GetInputSchemaRequest, \
    GetOutputSchemaRequest, \
    LookupTableResponse, \
    NodeMetrics, \
    MetricsResponse, \
    PaginatedResponseOfConnectionResponse, \
    PaginatedResponseOfConnectorResponse, \
    PipelineResponseV4, \
    UpdateError, \
    PaginatedResponseOfPipelineResponseV4, \
    TemplateResponse, \
    PaginatedResponseOfTemplateResponse, \
    PipelinePatchRequest, \
    PipelineRequest, \
    PreviewNode, \
    RuleMetrics, \
    PreviewData, \
    PreviewSessionStartRequest, \
    PreviewStartResponse, \
    PreviewState, \
    RegistryModel, \
    SplCompileRequest, \
    TemplatePatchRequest, \
    TemplatePutRequest, \
    TemplateRequest, \
    UplType, \
    ValidateConnectionRequest, \
    ValidateRequest, \
    ValidateResponse
