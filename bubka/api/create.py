
import requests
import traceback

from .. import status
from .exceptions import APIResponseError


class CreateResponse:
    """
    Create a record with POST
    """

    def __init__(self, url, data, headers=dict, json=True, debug=False):
        self.headers = headers
        self.debug = debug
        self.__status_code__ = None
        self.__error_response__ = None

        if json:
            headers['Content-Type'] = 'application/json'

        try:
            res = requests.post(url, data, headers=self.headers)
            self.__status_code__ = res.status_code
            content = str(res.content, 'utf-8')
            if self.__status_code__ == status.HTTP_201_CREATED:
                print(content)
            else:
                raise APIResponseError('request returns code {}: {}'.format(
                    self.__status_code__,
                    content,
                ))
        except Exception as e:
            if self.debug:
                print(traceback.print_exc())
            raise APIResponseError('Error creating record: {}'.format(e))
