"""Send "taskflows" requests to girder."""

import json


class TaskflowsUtils:
    """Utility functions for sending taskflows requests to girder."""

    TASKFLOWS_CREATE_PATH='/taskflows'
    TASKFLOWS_GET_PATH='/taskflows/{id}'
    TASKFLOWS_START_PATH='/taskflows/{id}/start'
    TASKFLOWS_TERMINATE_PATH='/taskflows/{id}/terminate'
    TASKFLOWS_DELETE_PATH='/taskflows/{id}'

    def __init__(self, gc):
        """Initialize with an authenticated GirderClient object."""
        self.gc = gc

    def createTaskflow(self, body):
        """Create a taskflow with a given body."""
        return self.gc.post(TaskflowsUtils.TASKFLOWS_CREATE_PATH,
                            data=json.dumps(body))

    def getTaskflow(self, taskflowId):
        """Get a taskflow from its id."""
        params = {'id': taskflowId}
        return self.gc.get(TaskflowsUtils.TASKFLOWS_GET_PATH, parameters=params)

    def startTaskflow(self, taskflowId):
        """Start a taskflow from its id."""
        params = {'id': taskflowId}
        return self.gc.put(TaskflowsUtils.TASKFLOWS_START_PATH, parameters=params)

    def terminateTaskflow(self, taskflowId):
        """Terminate a taskflow from its id."""
        params = {'id': taskflowId}
        return self.gc.put(TaskflowsUtils.TASKFLOWS_TERMINATE_PATH, parameters=params)

    def deleteTaskflow(self, taskflowId):
        """Delete a taskflow from its id."""
        params = {'id': taskflowId}
        return self.gc.delete(TaskflowsUtils.TASKFLOWS_DELETE_PATH, parameters=params)

    def log(self, taskflowId):
        """Get the log of a taskflow from its id."""
        resp = self.getTaskflow(taskflowId)
        return resp.value("log")
