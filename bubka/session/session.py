
import os

from ..api.exceptions import APIResponseError
from ..api.create import CreateResponse
from ..api.delete import DeleteResponse
from ..api.response import PaginatedListResponse
from ..api.update import UpdateResponse

from .environment import DRF_AUTH_TOKEN_VARIABLE, JWT_API_TOKEN_VARIABLE


class APISession(object):
    """
    Base class for REST API sessions

    This is also class for anonymous (not authenticated) API sessions
    """
    session_type = 'anonymous'

    @property
    def headers(self):
        """
        Headers to append for session.

        By default empty dictionary, extended by child class
        """
        return {}

    def list(self, url, debug=False):
        """
        Get iterator for resource listings for specified URL
        """
        return PaginatedListResponse(url, headers=self.headers, debug=debug)

    def create(self, url, data, json=False, debug=True):
        """
        Create a record with REST API
        """
        return CreateResponse(url, data, headers=self.headers, json=json, debug=debug)

    def delete(self, url, debug=True):
        """
        Dlete a record with REST API
        """
        return DeleteResponse(url, headers=self.headers, debug=debug)

    def update(self, url, data, json=False, debug=True):
        """
        Update a record with REST API
        """
        return UpdateResponse(url, data, headers=self.headers, json=json, debug=debug)


def load_api_session():
    """
    Try to detect and load session based on environment variables available

    Preferred order of sessions:
    - Static token authentication
    - JWT token authentication
    - Anonymous authentication
    """

    if os.environ.get(DRF_AUTH_TOKEN_VARIABLE, None):
        from .django_token_auth import TokenAuthSession
        session = TokenAuthSession()

    elif os.environ.get(JWT_API_TOKEN_VARIABLE, None):
        from .jwt_token_auth import JWTAuthenticationSession
        session = JWTAuthenticationSession()
        if not session.verify_token():
            raise APIResponseError('JWT session token has expired')
    else:
        session = APISession()

    return session
