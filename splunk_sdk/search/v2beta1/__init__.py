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
    SDC Service: Splunk Search service

    Use the Search service in Splunk Cloud Services to dispatch, review, and manage searches and search jobs. You can finalize or cancel jobs, retrieve search results, and request search-related configurations from the Metadata Catalog service in Splunk Cloud Services.

    OpenAPI spec version: v2beta1.1 
    Generated by: https://openapi-generator.tech
"""


__version__ = "1.0.0"

# import apis into sdk package
from splunk_sdk.search.v2beta1.gen_splunk_search_service_api import SplunkSearchService

# import models into sdk package
from splunk_sdk.search.v2beta1.gen_models import Message, \
    QueryParameters, \
    SearchStatus, \
    DeleteSearchJob, \
    SingleFieldSummary, \
    SingleValueMode, \
    FieldsSummary, \
    ListPreviewResultsResponseFields, \
    ListPreviewResultsResponse, \
    ListSearchResultsResponse, \
    SearchJob, \
    SingleTimeBucket, \
    TimeBucketsSummary, \
    UpdateJob
