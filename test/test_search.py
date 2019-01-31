# Copyright © 2019 Splunk Inc.
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.

import pytest
from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.search.client import Search
from splunk_sdk.search.results import Job, UpdateJobResponse, SearchResults, \
    ResultsNotReadyResponse, MessageTypes, SearchJobMessage

STANDARD_QUERY = '| from index:main | head 5'

# TODO: add test_list_results w/ a search using a module when catalog
#  is ready for that


@pytest.mark.usefixtures("test_client")  # NOQA
def test_create_job(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_update_job(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))

    updated_job = search.update_job(job.sid, status='canceled')
    assert (isinstance(updated_job, UpdateJobResponse))
    assert (isinstance(updated_job.messages, list))
    assert (len(updated_job.messages) == 1)
    # Should have 1 message for job being canceled
    msg = SearchJobMessage(**updated_job.messages[0])
    assert (isinstance(msg, SearchJobMessage))
    assert (msg.type == MessageTypes.INFO.value)
    assert (msg.text == 'Search job cancelled.')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_get_job(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

    job2 = search.get_job(job.sid)
    assert (isinstance(job2, Job))
    assert (job.sid == job2.sid)
    assert (job.query == job2.query)


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_list_results(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

    results = search.list_results(job.sid)
    assert (isinstance(results, ResultsNotReadyResponse))
    assert (results.nextLink is not None)
    assert (results.wait is not None)

    job2 = await search.wait_for_job(job.sid)
    assert (isinstance(job, Job))
    assert (job2.status == 'done')

    results2 = search.list_results(job2.sid)
    assert (isinstance(results2, SearchResults))
    assert (len(results2.results) == 5)
    assert (results2.fields is not None)


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_list_results_with_pagination(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))
    assert (job.query == STANDARD_QUERY)
    assert (job.sid is not None)
    assert (job.status is not None)

    job2 = await search.wait_for_job(job.sid)
    assert (isinstance(job, Job))
    assert (job2.status == 'done')
    assert (job2.resultsAvailable == 5)

    results = search.list_results(job2.sid, offset=0, count=3)
    assert (isinstance(results, SearchResults))
    assert (len(results.results) == 3)

    results = search.list_results(job2.sid, offset=3, count=5)
    assert (isinstance(results, SearchResults))
    assert (len(results.results) == 2)

    results = search.list_results(job2.sid, offset=10, count=10)
    assert (isinstance(results, SearchResults))
    assert (len(results.results) == 0)


@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_wait_for_job(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))

    job2 = await search.wait_for_job(job.sid)
    assert (isinstance(job2, Job))
    assert (job2.status == 'done')
    assert (job2.resultsAvailable == 5)
    assert (job2.sid is not None)
    assert (job2.query is not None)
    assert (job2.module is not None)
    assert (job2.percentComplete is not None)


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_jobs(test_client):
    search = Search(test_client)

    jobs = search.list_jobs()
    assert (len(jobs) > 0)
    assert (isinstance(jobs, list))

    for job in jobs:
        assert (isinstance(job, Job))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_jobs_with_args(test_client):
    search = Search(test_client)

    jobs = search.list_jobs(status='running,done')
    assert (len(jobs) > 0)

    for job in jobs:
        assert (isinstance(job, Job))
        assert (job.status is not None)
        assert (job.resultsAvailable is not None)
        assert (job.sid is not None)
        assert (job.query is not None)
        assert (job.module is not None)
        assert (job.percentComplete is not None)
