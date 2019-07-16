from asyncio import sleep


# TODO: when doc-ing, note that poll_interval is seconds, not ms
async def wait_for_job(get_job_func, job_id, poll_interval=0.5):
    done = False
    job = None
    while not done:
        job = get_job_func(job_id)
        done = job.status in ('done', 'failed')
        if not done:
            await sleep(poll_interval)
    return job
