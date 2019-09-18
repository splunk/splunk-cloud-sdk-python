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


from test.fixtures import get_test_client as test_client  # NOQA

from splunk_sdk.base_client import SSCVoidModel
from splunk_sdk.collect import CollectService
from splunk_sdk.collect import Job, JobPatch, JobsPatch, SingleJobResponse, \
    ListJobsResponse, ScalePolicy, StaticScale


def _cleanup(collect):
    """There is a limit of 10 jobs per tenant."""
    jobs = collect.list_jobs()
    assert (jobs is not None)
    assert (isinstance(jobs, ListJobsResponse))

    if len(jobs.data) > 5:
        collect.delete_jobs()


def _create_job():
    return Job(connector_id="aws-cloudwatch-metrics",
               name="sdkpytest_" + str(time.time_ns()),
               schedule="16 * * * *",
               parameters={"namespaces": "AWS/EC2"},
               scale_policy={"static": {"workers": 2}})


@pytest.mark.usefixtures("test_client")  # NOQA
def test_basic_job_operations(test_client):
    collect = CollectService(test_client)
    assert (collect is not None)
    job_id = None
    try:
        # clean up before we start
        _cleanup(collect)

        # create a job
        job = _create_job()
        job_response = collect.create_job(job)

        assert (job_response is not None)
        assert (isinstance(job_response, SingleJobResponse))
        assert (job_response.data is not None)

        job_id = job_response.data.id

        # get job
        job_found = collect.get_job(job_id=job_id)
        assert (job_found is not None)
        assert (isinstance(job_found, SingleJobResponse))
        assert (job_found.data == job_response.data)

        # patch job
        patch = JobPatch(name=job_found.data.name + "_patched")
        job_patched = collect.patch_job(job_id=job_found.data.id,
                                        job_patch=patch)

        assert (job_patched is not None)
        assert (isinstance(job_patched, SingleJobResponse))
        assert (job_found.data.id == job_patched.data.id)
        assert (job_found.data.name != job_patched.data.name)

        # list job
        jobs = collect.list_jobs()
        assert (jobs is not None)
        assert (isinstance(jobs, ListJobsResponse))
        assert (len(jobs.data) > 0)

    finally:
        # delete job
        deleted_job = collect.delete_job(job_id=job_id)
        assert (deleted_job is not None)
        assert (isinstance(deleted_job, SSCVoidModel))


@pytest.mark.usefixtures("test_client")  # NOQA
def test_patch_jobs(test_client):
    collect = CollectService(test_client)
    assert (collect is not None)
    job_id = None
    try:
        # clean up before we start
        _cleanup(collect)

        # create a job
        job = _create_job()
        job_response = collect.create_job(job)

        assert (job_response is not None)
        assert (isinstance(job_response, SingleJobResponse))
        assert (job_response.data is not None)

        job_id = job_response.data.id

        scale_policy = ScalePolicy(static=StaticScale(workers=1))
        jp = JobsPatch(scale_policy=scale_policy)

        new_jobs = collect.patch_jobs(jobs_patch=jp,
                                      connector_id=job.connector_id)

        assert (new_jobs is not None)
        assert (new_jobs.data[0].updated is True)

        new_jobs_id = new_jobs.data[0].id

        # get job
        job_found = collect.get_job(job_id=new_jobs_id)
        assert (job_found is not None)
        assert (job_found.data.name is not None)
        assert (job_found.data.scale_policy['static'] is not None)

    finally:
        # delete job
        if job_id:
            deleted_job = collect.delete_job(job_id=job_id)
            assert (deleted_job is not None)
            assert (isinstance(deleted_job, SSCVoidModel))
