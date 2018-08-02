"""User utility functions for communicating with girder."""


class UserUtils:
    """Utility functions for performing user operations on girder."""

    ME_PATH = '/user/me'
    GET_PATH = '/user/{id}'

    def __init__(self, gc):
        """Initialize with an authenticated GirderClient object."""
        self.gc = gc

    def getCurrentUserId(self):
        """Get the current user's id number."""
        resp = self.gc.get(UserUtils.ME_PATH)
        if resp and '_id' in resp:
            return resp['_id']
        else:
            print('Warning: current user ID not found!')
            return None

    def getUserLogin(self, userId):
        """Get a user's login name from their id."""
        params = {'id': userId}
        resp = self.gc.get(UserUtils.GET_PATH, parameters=params)
        if resp and 'login' in resp:
            return resp['login']
        else:
            print('Warning: user login name not found!')
            return None
