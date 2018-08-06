"""Send "taskflows" requests to girder."""

import json

from girder_client import HttpError


class TaskflowsUtils:
    """Utility functions for sending taskflows requests to girder."""

    TASKFLOWS_CREATE_PATH = '/taskflows'
    TASKFLOWS_GET_PATH = '/taskflows/{id}'
    TASKFLOWS_START_PATH = '/taskflows/{id}/start'
    TASKFLOWS_TERMINATE_PATH = '/taskflows/{id}/terminate'
    TASKFLOWS_DELETE_PATH = '/taskflows/{id}'

    def __init__(self, gc):
        """Initialize with an authenticated GirderClient object."""
        self.gc = gc

    def createTaskflow(self, body):
        """Create a taskflow with a given body."""
        return self.gc.post(TaskflowsUtils.TASKFLOWS_CREATE_PATH,
                            data=json.dumps(body))

    def getTaskflow(self, taskflowId):
        """Get a taskflow from its id."""
        path = TaskflowsUtils.TASKFLOWS_GET_PATH.replace('{id}', taskflowId)
        return self.gc.get(path)

    def startTaskflow(self, taskflowId):
        """Start a taskflow from its id."""
        path = TaskflowsUtils.TASKFLOWS_START_PATH.replace('{id}', taskflowId)
        return self.gc.put(path)

    def terminateTaskflow(self, taskflowId):
        """Terminate a taskflow from its id."""
        path = TaskflowsUtils.TASKFLOWS_TERMINATE_PATH.replace(
            '{id}', taskflowId)
        return self.gc.put(path)

    def deleteTaskflow(self, taskflowId):
        """Delete a taskflow from its id."""
        path = TaskflowsUtils.TASKFLOWS_DELETE_PATH.replace('{id}', taskflowId)

        # For some reason, the girder client will throw an exception here.
        # Catch it. If the error is 202, we are fine.
        try:
            resp = self.gc.delete(path)
        except HttpError as e:
            if e.status != 202:
                raise
            resp = e.responseText

        return resp

    def log(self, taskflowId):
        """Get the log of a taskflow from its id."""
        resp = self.getTaskflow(taskflowId)
        return resp.get("log")

    def status(self, taskflowId):
        """Get the status of a taskflow from its id."""
        resp = self.getTaskflow(taskflowId)
        return resp.get("status")
