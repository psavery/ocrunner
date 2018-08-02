"""Send "clusters" requests to girder."""

from girder_client import HttpError

import sys

class ClustersUtils:
    """Utility functions for sending clusters requests to girder."""

    CLUSTERS_LIST_PATH = '/clusters'

    def __init__(self, gc):
        """Initialize with an authenticated GirderClient object."""
        self.gc = gc

    def clusters(self):
        """Get all clusters and their statuses."""
        params = {'limit': '0'}
        return self.gc.get(ClustersUtils.CLUSTERS_LIST_PATH, parameters=params)
