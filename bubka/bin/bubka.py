
from systematic.shell import Script

from .commands.create import CreateCommand
from .commands.delete import DeleteCommand
from .commands.dump import DumpCommand
from .commands.get import GetCommand
from .commands.patch import PatchCommand
from .commands.update import UpdateCommand


def main():
    script = Script()

    script.add_subcommand(GetCommand())
    script.add_subcommand(DumpCommand())
    script.add_subcommand(CreateCommand())
    script.add_subcommand(DeleteCommand())
    script.add_subcommand(PatchCommand())
    script.add_subcommand(UpdateCommand())

    script.parse_args()


if __name__ == '__main__':
    main()
