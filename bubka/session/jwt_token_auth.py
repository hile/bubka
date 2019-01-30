
import json
import os
import requests

from ..api.exceptions import APIResponseError
from .session import APISession
from .environment import JWT_API_TOKEN_VARIABLE


class JWTAuthenticationSession(APISession):
    """
    API Session with django rest framework token authentication
    """

    def __init__(self, obtail_token_url, verify_token_url, refresh_token_url=None, token=None, timeout=10):
        self.token = token if token is not None else os.environ.get(JWT_API_TOKEN_VARIABLE, None)
        self.timeout = timeout

        # URLs for JWT authentication. Refreshing tokens is optional
        self.obtain_token_url = obtail_token_url
        self.verify_token_url = verify_token_url
        self.refresh_token_url = refresh_token_url

        if not self.token:
            raise APIResponseError('Authentication token for JWT authentication not detected')
        self.user = {}

    @property
    def headers(self):
        """
        Authorization headers for JWT
        """
        return {'Authorization': 'JWT {}'.format(self.token), }

    def obtain_token(self, username, password):
        """
        Obtain new JTW session token and store it to self.token
        """

        try:

            res = requests.post(
                self.obtain_token_url,
                data=json.dumps({'username': username, 'password': password}),
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout,
            )

            if res.status_code == 200:
                data = json.loads(str(res.content, 'utf-8'))
                self.token = data['token']
                self.user = data.get('user', None)

            else:
                raise APIResponseError('Error authenticating to API')

        except Exception as e:
            raise APIResponseError('Error obtaining API token: {}'.format(e))

    def verify_token(self):
        """
        Try to verify existing token
        """

        if not self.token:
            raise APIResponseError('Token not loaded')

        try:
            res = requests.post(
                self.verify_token_url,
                data=json.dumps({'token': self.token}),
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout,
            )

            if res.status_code == 200:
                return True
            else:
                return False

        except Exception as e:
            raise APIResponseError('Error verifying API token: {}'.format(e))

    def refresh_token(self):
        """
        Try to refresh existing token
        """

        if not self.token:
            raise APIResponseError('Token not loaded')

        if not self.refresh_token_url:
            raise APIResponseError('Refresh URL for JWT tokens not specified')

        try:
            res = requests.post(
                self.refresh_token_url,
                data=json.dumps({'token': self.token}),
                headers={'Content-Type': 'application/json'},
                timeout=self.timeout,
            )

            if res.status_code == 200:
                data = json.loads(str(res.content, 'utf-8'))
                self.token = data['token']
                self.user = data.get('user', None)

            else:
                raise APIResponseError('Server returns error code {} ({})'.format(
                    res.status_code,
                    res.content
                ))

        except Exception as e:
            raise APIResponseError('Error refreshing API token: {}'.format(e))
