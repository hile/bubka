
import os

from ..api.exceptions import APIResponseError
from .session import APISession
from .environment import REST_AUTH_TOKEN_NAME, REST_AUTH_TOKEN_VARIABLE


class AuthorizationHeaderSession(APISession):
    """
    REST API Session with generic Authorization header authentication
    """
    session_type = 'token'
    token_name = os.environ.get(REST_AUTH_TOKEN_NAME, None)
    token_var = REST_AUTH_TOKEN_VARIABLE

    def __init__(self, token=None, timeout=10):
        self.token = token if token is not None else os.environ.get(self.token_var, None)
        self.timeout = timeout

        if not self.token:
            raise APIResponseError('Authentication token for TokenAuthSession not detected')

    @property
    def headers(self):
        if self.token_name:
            return {'Authorization': '{} {}'.format(self.token_name, self.token)}
        else:
            return {'Authorization': '{}'.format(self.token)}
