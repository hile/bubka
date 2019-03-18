
import os

from ..api.exceptions import APIResponseError
from .session import APISession
from .environment import DRF_AUTH_TOKEN_VARIABLE


class TokenAuthSession(APISession):
    """
    API Session with django rest framework token authentication
    """
    session_type = 'token'

    def __init__(self, token=None, timeout=10):
        self.token = token if token is not None else os.environ.get(DRF_AUTH_TOKEN_VARIABLE, None)
        self.timeout = timeout

        if not self.token:
            raise APIResponseError('Authentication token for TokenAuthSession not detected')

    @property
    def headers(self):
        return {'Authorization': 'Token {}'.format(self.token)}
