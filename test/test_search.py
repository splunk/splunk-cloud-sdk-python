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
from test.fixtures import get_test_client as test_client  # NOQA

from splunk_sdk.search import SplunkSearchService as Search
from splunk_sdk.search import SearchJob, UpdateJob, Message, \
    ListSearchResultsResponse

import itertools

from splunk_sdk.search.search_helper import wait_for_job

STANDARD_QUERY = '| from index:main | head 5'

# TODO(shakeel): add test_list_results w/ a search using a module when catalog
#  is ready for that

@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_job(test_client):
    search = Search(test_client)

    search_job = SearchJob(query=STANDARD_QUERY)
    job = search.create_job(search_job=search_job)

    assert (isinstance(job, SearchJob))
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

@pytest.mark.usefixtures("test_client")  # NOQA
def test_update_job(test_client):
    search = Search(test_client)

    # create job
    search_job = SearchJob(query=STANDARD_QUERY)
    job = search.create_job(search_job=search_job)
    assert (isinstance(job, SearchJob))

    # get job
    _job = search.get_job(job.sid)

    if _job.status == 'running':
        # update
        canceled_job = UpdateJob(status='canceled')
        updated_job = search.update_job(job.sid, update_job=canceled_job)
        assert (isinstance(updated_job, SearchJob))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_job(test_client):
    search = Search(test_client)

    search_job = SearchJob(query=STANDARD_QUERY)
    job = search.create_job(search_job=search_job)
    assert (isinstance(job, SearchJob))
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

    job2 = search.get_job(job.sid)
    assert (isinstance(job2, SearchJob))
    assert (job.sid == job2.sid)
    assert (job.query == job2.query)


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_list_results(test_client):
    search = Search(test_client)

    search_job = SearchJob(query=STANDARD_QUERY)
    job = search.create_job(search_job=search_job)
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

    results = search.list_results(job.sid)
    assert (isinstance(results, ListSearchResultsResponse))
    assert (results.next_link is not None)

    job2 = await wait_for_job(search.get_job, job.sid)
    assert (isinstance(job, SearchJob))
    assert (job2.status == 'done')

    results2 = search.list_results(job2.sid)
    assert (isinstance(results2, ListSearchResultsResponse))


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_list_results_with_pagination(test_client):
    search = Search(test_client)

    search_job = SearchJob(query=STANDARD_QUERY)
    job = search.create_job(search_job=search_job)
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

    job2 = await wait_for_job(search.get_job, job.sid)
    assert (isinstance(job, SearchJob))
    assert (job2.status == 'done')
    assert (job2.results_available == 5)

    results = search.list_results(job2.sid, offset=0, count=3)
    assert (isinstance(results, ListSearchResultsResponse))
    assert (len(results.results) == 3)

    results = search.list_results(job2.sid, offset=3, count=5)
    assert (isinstance(results, ListSearchResultsResponse))
    assert (len(results.results) == 2)

    results = search.list_results(job2.sid, offset=10, count=10)
    assert (isinstance(results, ListSearchResultsResponse))
    assert (len(results.results) == 0)


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_wait_for_job(test_client):
    search = Search(test_client)

    search_job = SearchJob(query=STANDARD_QUERY)
    job = search.create_job(search_job=search_job)


    jobs = search.list_jobs()
    assert (len(jobs) > 0)

    for job in jobs:
        assert (isinstance(job, SearchJob))
        assert (job.status is not None)
        assert (job.results_available is not None)
        assert (job.sid is not None)
        assert (job.query is not None)
        assert (job.module is not None)
        assert (job.percent_complete is not None)
