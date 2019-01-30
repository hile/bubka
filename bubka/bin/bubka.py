
import json
import traceback

from bubka.session.session import load_api_session
from bubka.api.exceptions import APIResponseError
from systematic.shell import Script, ScriptCommand


LIST_COMMAND_DESCRIPTION = """
List records from REST API
"""

LIST_COMMAND_EPILOG = """
List command returns a list of records from REST API
"""

CREATE_COMMAND_DESCRIPTION = """
Create a record with REST API
"""

CREATE_COMMAND_EPILOG = """

"""


DELETE_COMMAND_DESCRIPTION = """
Delete data with REST API
"""

DELETE_COMMAND_EPILOG = """

"""


UPDATE_COMMAND_DESCRIPTION = """
Update data with REST API
"""

UPDATE_COMMAND_EPILOG = """

"""

# Formats we can validate
SUPPORTED_FORMATS = (
    'json',
)


class APICommand(ScriptCommand):
    """
    Common base class for API commands
    """
    def parse_args(self, args):
        self.session = load_api_session()
        return args

    def validate_data(self, data, format):
        """
        Validate data format
        """

        if format == 'json':
            try:
                json.loads(data)
            except Exception as e:
                self.exit(1, 'Error loading JSON data: {}'.format(e))

        return data


class ListCommand(APICommand):
    """
    List records from REST API
    """
    name = 'list'
    short_description = 'List records from REST API'
    description = LIST_COMMAND_DESCRIPTION
    epilog = LIST_COMMAND_EPILOG

    def __register_arguments__(self, parser):
        """
        Register command arguments
        """
        parser.add_argument('--debug', action='store_true', help='Show debug traces')
        parser.add_argument('url', help='URL for API listings')

    def run(self, args):

        try:
            response = self.session.list(args.url, debug=args.debug)
            for record in response:
                self.message(json.dumps(record, indent=2))
        except APIResponseError as e:
            if args.debug:
                self.error(traceback.print_exc())
            self.exit(1, e)


class CreateCommand(APICommand):
    """
    Post data to REST API
    """
    name = 'create'
    short_description = 'Create a record with REST API'
    description = CREATE_COMMAND_DESCRIPTION
    epilog = CREATE_COMMAND_EPILOG

    def __register_arguments__(self, parser):
        """
        Register command arguments
        """
        parser.add_argument('--debug', action='store_true', help='Show debug traces')
        parser.add_argument('-f', '--format', choices=SUPPORTED_FORMATS, default='json', help='Validate data')
        parser.add_argument('-d', '--data', help='Data to send')
        parser.add_argument('-i', '--file', help='Data from file')
        parser.add_argument('url', help='URL for API listings')

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
            self.session.create(args.url, data, json=args.format=='json', debug=args.debug)
        except APIResponseError as e:
            if args.debug:
                self.error(traceback.print_exc())
            self.exit(1, e)


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
        parser.add_argument('url', help='URL for API listings')

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
            self.session.update(args.url, data, json=args.format=='json', debug=args.debug)
        except APIResponseError as e:
            if args.debug:
                self.error(traceback.print_exc())
            self.exit(1, e)


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
s

def main():
    script = Script()

    script.add_subcommand(ListCommand())
    script.add_subcommand(CreateCommand())
    script.add_subcommand(DeleteCommand())
    script.add_subcommand(UpdateCommand())

    script.parse_args()


if __name__ == '__main__':
    main()
