
import json
import requests
import traceback

from .exceptions import APIResponseError


class PaginatedListResponse:
    """
    Iterable JSON API listing response with pagination

    By default django rest framework compatible. Override methods to fetch data
    from other types of responses.
    """

    def __init__(self, url, headers=dict, debug=False):
        self.headers = headers
        self.debug = debug

        self.__page_url__ = url
        self.__status_code__ = None
        self.__error_response__ = None
        self.__total_records__ = None
        self.__records__ = []

    def __len__(self):
        """
        Return total records in response

        If no data has been fetched, get first page to get total count
        """

        # Get first page to get count
        if not self.__records__ and self.__page_url__:
            self.__get_page__()

        return self.__total_records__

    def __get_page__(self):
        """
        Get next page for data

        Raises StopIteration if no more pages are available
        """

        if self.__page_url__ is None:
            raise StopIteration

        self.__records__ = []
        try:
            if self.debug:
                print('DEBUG get {}'.format(self.__page_url__))
            res = requests.get(self.__page_url__, headers=self.headers)
            self.__status_code__ = res.status_code
            if res.status_code == 200:
                data = json.loads(res.content)
                self.__records__ = self.get_records(data)
                self.__page_url__ = self.get_next_page_url(data)
                self.__total_records__ = self.get_total_records_count(data)
            else:
                self.__error_response__ = str(res.content, 'utf-8') if res.content else ''
                raise APIResponseError(
                    'Error getting {}: returns status code {}{}'.format(
                        self.__page_url__,
                        res.status_code,
                        ' ({})'.format(self.__error_response__) if self.__error_response__ else ''
                    )
                )
        except Exception as e:
            if self.debug:
                print(traceback.print_exc())
            raise APIResponseError('Error loading data: {}'.format(e))

    def __iter__(self):
        return self

    def __next__(self):
        """
        Get next record from iterator.

        Loads next page as side effect if available, until all pages are loaded
        """

        if self.__records__:
            # Got records to return, pop one and return it
            return self.__records__.pop(0)

        elif self.__page_url__:
            # Got a page URL to load, load page and pop first record from loaded response
            self.__get_page__()
            if self.__records__:
                return self.__records__.pop(0)
            else:
                raise StopIteration
        else:
            raise StopIteration

    def get_records(self, data):
        """
        Get records from data

        By default look up 'records' attribute (django rest framework compatible)
        """
        if isinstance(data, dict):
            if 'results' in data:
                return data.get('results', [])
            else:
                return [data]
        elif isinstance(data, list):
            return data
        else:
            raise ValueError('Unexpected data type: {}'.type(data))

    def get_next_page_url(self, data):
        """
        Get next page's URL from data

        By default look up 'next' field (django rest framework compatible)
        """
        if isinstance(data, dict):
            return data.get('next', None)
        return None

    def get_total_records_count(self, data):
        """
        Get count of total records

        By default look up 'count' field (django rest framework compatible)
        """
        if isinstance(data, dict):
            return data.get('count', None)
        elif isinstance(data, list):
            return len(data)
        else:
            return None
