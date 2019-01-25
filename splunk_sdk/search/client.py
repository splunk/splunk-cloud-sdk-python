import json
from asyncio import sleep

from splunk_sdk.base_client import handle_response
from splunk_sdk.base_service import BaseService
from splunk_sdk.search.results import Job, UpdateJobResponse, SearchResults, \
    ResultsNotReadyResponse, DispatchState

SEARCH = "/search/v1beta1/"


class Search(BaseService):

    def __init__(self, base_client, cluster='api'):
        super().__init__(base_client, cluster=cluster)

    def list_jobs(self, **kwargs):
        url = self.base_client.build_url(
            SEARCH + "jobs"
        )
        response = self.base_client.get(url, **kwargs)
        return handle_response(response, Job)

    def create_job(self, **kwargs):
        url = self.base_client.build_url(
            SEARCH + "jobs"
        )
        response = self.base_client.post(url, data=json.dumps(kwargs))
        return handle_response(response, Job)

    def get_job(self, job_id):
        url = self.base_client.build_url(
            "{}jobs/{}".format(SEARCH, job_id)
        )
        response = self.base_client.get(url)
        return handle_response(response, Job)

    def update_job(self, job_id, **kwargs):
        url = self.base_client.build_url(
            "{}jobs/{}/".format(SEARCH, job_id)
        )
        response = self.base_client.patch(url, data=json.dumps(kwargs))
        return handle_response(response, UpdateJobResponse)

    # TODO: when doc-ing, note that poll_interval is seconds, not ms
    async def wait_for_job(self, job_id, poll_interval=0.5):

        done = False
        job = None
        while not done:
            job = self.get_job(job_id)
            done = \
                job.status == DispatchState.DONE.value or \
                job.status == DispatchState.FAILED.value
            if not done:
                await sleep(poll_interval)

        return job

    def list_results(self, job_id, **kwargs):
        url = self.base_client.build_url(
            "{}jobs/{}/results".format(SEARCH, job_id)
        )
        response = self.base_client.get(url, **kwargs)
        body = handle_response(response, object)
        if 'results' in body:
            return SearchResults(**body)
        else:
            return ResultsNotReadyResponse(**body)
