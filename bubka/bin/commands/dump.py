
import json
import traceback

from .base import APICommand


DUMP_COMMAND_DESCRIPTION = """
Dump JSON data from files
"""

DUMP_COMMAND_EPILOG = """
Dump JSON formatted data from files with pretty printing
"""


class DumpCommand(APICommand):
    """
    Dump data from file
    """
    name = 'dump'
    short_description = 'Dump JSON files'
    description = DUMP_COMMAND_DESCRIPTION
    epilog = DUMP_COMMAND_EPILOG

    def __register_arguments__(self, parser):
        """
        Register command arguments
        """
        parser.add_argument('--debug', action='store_true', help='Show debug traces')
        parser.add_argument('-i', '--indent', type=int, default=2, help='Indent level')
        parser.add_argument('files', nargs='*', help='Files to show')

    def run(self, args):

        for filename in args.files:
            try:
                with open(filename, 'r') as fd:
                    self.message(json.dumps(json.loads(fd.read()), indent=args.indent))
            except Exception as e:
                if args.debug:
                    self.error(traceback.print_exc())
                self.exit(1, e)
