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
from concurrent.futures import ThreadPoolExecutor as PoolExecutor
from splunk_sdk.base_client import HTTPError
from test.fixtures import get_test_client as test_client  # NOQA
from test.fixtures import get_test_client_default_retry as test_client_default_retry # NOQA
from test.fixtures import get_test_client_custom_retry as test_client_custom_retry # NOQA
from test.fixtures import get_test_client_retry_false as test_client_retry_false # NOQA


from splunk_sdk.search import SplunkSearchService as Search
from splunk_sdk.search import SearchJob

import itertools

STANDARD_QUERY = '| from index:main | head 5'

def execute_search_job(expect_error, search_job, search_client):
    try:
        job = search_client.create_job(search_job=search_job)
        print("NAME")
        print(job.name)
        assert(job is not None)
    except HTTPError as error:
        got_error = True
        if expect_error is True:
            assert(error.code == "too_many_requests")
            assert (error.http_status_code == 429)
        else:
            assert(got_error == expect_error)


@pytest.mark.usefixtures("test_client_default_retry")  # NOQA
def test_create_job_default_retry(test_client_default_retry):
    search_client = Search(test_client_default_retry)
    search_job = SearchJob(query=STANDARD_QUERY)
    with PoolExecutor(max_workers=10) as executor:
        for _ in executor.map(execute_search_job, itertools.repeat(False), itertools.repeat(search_job, 29), itertools.repeat(search_client)):
            pass

@pytest.mark.usefixtures("test_client_custom_retry")  # NOQA
def test_create_job_custom_retry(test_client_custom_retry):
    search_client = Search(test_client_custom_retry)
    search_job = SearchJob(query=STANDARD_QUERY)
    with PoolExecutor(max_workers=10) as executor:
        for _ in executor.map(execute_search_job, itertools.repeat(False), itertools.repeat(search_job, 27), itertools.repeat(search_client)):
            pass

@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_job_no_retry_expect_429(test_client):
    search_client = Search(test_client)
    search_job = SearchJob(query=STANDARD_QUERY)
    with PoolExecutor(max_workers=10) as executor:
        for _ in executor.map(execute_search_job, itertools.repeat(True), itertools.repeat(search_job, 28), itertools.repeat(search_client)):
            pass

@pytest.mark.usefixtures("test_client_retry_false")  # NOQA
def test_create_job_retry_enabled_false(test_client_retry_false):
    search_client = Search(test_client_retry_false)
    search_job = SearchJob(query=STANDARD_QUERY)
    with PoolExecutor(max_workers=10) as executor:
        for _ in executor.map(execute_search_job, itertools.repeat(True), itertools.repeat(search_job, 28), itertools.repeat(search_client)):
            pass
