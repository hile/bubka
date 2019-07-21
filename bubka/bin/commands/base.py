
import json

from bubka.session.session import load_api_session
from systematic.shell import ScriptCommand

# Formats we can validate
SUPPORTED_FORMATS = (
    'json',
)


class APICommand(ScriptCommand):
    """
    Common base class for API commands
    """
    def parse_args(self, args):
        if 'indent' in args:
            if not 0 <= args.indent <= 32:
                self.exit(1, 'Invalid indentation')
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
