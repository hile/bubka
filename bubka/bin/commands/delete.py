
import traceback

from bubka.api.exceptions import APIResponseError
from .base import APICommand

DELETE_COMMAND_DESCRIPTION = """
Delete data with REST API
"""

DELETE_COMMAND_EPILOG = """

"""


class DeleteCommand(APICommand):
    """
    Delete with REST API
    """
    name = 'delete'
    short_description = 'Delete record to REST API'
    description = DELETE_COMMAND_DESCRIPTION
    epilog = DELETE_COMMAND_EPILOG

    def __register_arguments__(self, parser):
        """
        Register command arguments
        """
        parser.add_argument('--debug', action='store_true', help='Show debug traces')
        parser.add_argument('url', help='URL for record to delete')

    def run(self, args):
        try:
            self.session.delete(args.url, debug=args.debug)
        except APIResponseError as e:
            if args.debug:
                self.error(traceback.print_exc())
            self.exit(1, e)
