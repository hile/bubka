
import traceback

from bubka.api.exceptions import APIResponseError
from .base import APICommand, SUPPORTED_FORMATS

UPDATE_COMMAND_DESCRIPTION = """
Update data with REST API
"""

UPDATE_COMMAND_EPILOG = """

"""


class UpdateCommand(APICommand):
    """
    Update data with REST API
    """
    name = 'update'
    short_description = 'Update a record to REST API'
    description = UPDATE_COMMAND_DESCRIPTION
    epilog = UPDATE_COMMAND_EPILOG

    def __register_arguments__(self, parser):
        """
        Register command arguments
        """
        parser.add_argument('--debug', action='store_true', help='Show debug traces')
        parser.add_argument('-f', '--format', choices=SUPPORTED_FORMATS, default='json', help='Validate data')
        parser.add_argument('-d', '--data', help='Data to send')
        parser.add_argument('-i', '--file', help='Data from file')
        parser.add_argument('url', help='URL for API')

    def run(self, args):
        data = None
        if args.file:
            try:
                with open(args.file, 'r') as fd:
                    data = fd.read()
            except Exception as e:
                self.exit(1, 'Error reading JSON data from {}: {}'.format(args.file, e))
        elif args.data:
            try:
                data = args.data
            except Exception as e:
                self.exit(1, 'Error parsing JSON data: {}'.format(args.file, e))

        if data is None:
            self.exit(1, 'Data to send not provided')

        data = self.validate_data(data, format=args.format)

        try:
            jsonformat = args.format == 'json'
            self.session.update(args.url, data, json=jsonformat, debug=args.debug)
        except APIResponseError as e:
            if args.debug:
                self.error(traceback.print_exc())
            self.exit(1, e)
