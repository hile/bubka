
import json
import traceback

from bubka.api.exceptions import APIResponseError
from .base import APICommand


GET_COMMAND_DESCRIPTION = """
Get data from REST API
"""

GET_COMMAND_EPILOG = """
Get command returns a list of records or single record from REST API.
"""


class GetCommand(APICommand):
    """
    Get records from REST API
    """
    name = 'get'
    short_description = 'Get records from REST API'
    description = GET_COMMAND_DESCRIPTION
    epilog = GET_COMMAND_EPILOG

    def __register_arguments__(self, parser):
        """
        Register command arguments
        """
        parser.add_argument('--debug', action='store_true', help='Show debug traces')
        parser.add_argument('-i', '--indent', type=int, default=2, help='Indent level')
        parser.add_argument('url', help='URL for API listings')

    def run(self, args):

        try:
            response = self.session.list(args.url, debug=args.debug)
            for record in response:
                self.message(json.dumps(record, indent=args.indent))
        except APIResponseError as e:
            if args.debug:
                self.error(traceback.print_exc())
            self.exit(1, e)
