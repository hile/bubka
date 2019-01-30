
import requests
import traceback

from .. import status
from .exceptions import APIResponseError


class DeleteResponse:
    """
    DELETE a record with DELETE request
    """

    def __init__(self, url, headers=dict, debug=False):
        self.headers = headers
        self.debug = debug
        self.__status_code__ = None
        self.__error_response__ = None

        try:
            res = requests.delete(url, headers=self.headers)
            self.__status_code__ = res.status_code
            content = str(res.content, 'utf-8')
            if self.__status_code__ == status.HTTP_204_NO_CONTENT:
                if content:
                    print(content)
            else:
                raise APIResponseError('request returns code {}: {}'.format(
                    self.__status_code__,
                    content,
                ))
        except Exception as e:
            if self.debug:
                print(traceback.print_exc())
            raise APIResponseError('Error deleting record: {}'.format(e))
