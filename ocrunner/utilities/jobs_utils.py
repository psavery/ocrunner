"""Send "jobs" requests to girder."""


class JobsUtils:
    """Utility functions for sending jobs requests to girder."""

    JOBS_LIST_PATH = '/jobs'

    def __init__(self, gc):
        """Initialize with an authenticated GirderClient object."""
        self.gc = gc

    def listJobs(self):
        """For a given user, get all jobs and their statuses."""
        params = {'limit': '0'}
        return self.gc.get(JobsUtils.JOBS_LIST_PATH, parameters=params)
