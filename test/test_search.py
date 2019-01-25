import pytest
import asyncio
from test.fixtures import get_test_client as test_client  # NOQA
from splunk_sdk.search.client import Search
from splunk_sdk.search.results import Job, UpdateJobResponse, SearchResults, \
    ResultsNotReadyResponse

STANDARD_QUERY = '| from index:main | head 5'


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
    assert (updated_job.messages[0]['text'] == 'Search job cancelled.')


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

    # TODO: wait, then check for final results
    job2 = await search.wait_for_job(job.sid)
    assert (isinstance(job, Job))
    assert (job2.status == 'done')

    results2 = search.list_results(job2.sid)
    assert (isinstance(results2, SearchResults))
    print(results2)

@pytest.mark.asyncio
@pytest.mark.usefixtures("test_client")  # NOQA
async def test_wait_for_job(test_client):
    search = Search(test_client)

    job = search.create_job(query=STANDARD_QUERY)
    assert (isinstance(job, Job))

    job2 = await search.wait_for_job(job.sid)
    assert (isinstance(job2, Job))
    assert (job2.status == 'done')


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_jobs(test_client):
    search = Search(test_client)

    jobs = search.list_jobs()
    assert (len(jobs) > 0)

    for job in jobs:
        assert (isinstance(job, Job))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_list_jobs_with_args(test_client):
    search = Search(test_client)

    jobs = search.list_jobs(status='running,done')
    assert (len(jobs) > 0)

    for job in jobs:
        assert (isinstance(job, Job))
