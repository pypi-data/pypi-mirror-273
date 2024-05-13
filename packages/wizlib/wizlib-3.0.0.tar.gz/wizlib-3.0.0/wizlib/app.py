import sys
from dataclasses import dataclass
import os
from pathlib import Path

from wizlib.class_family import ClassFamily
from wizlib.command import WizHelpCommand
from wizlib.super_wrapper import SuperWrapper
from wizlib.parser import WizParser
from wizlib.ui import UI


RED = '\033[91m'
RESET = '\033[0m'


class AppCancellation(BaseException):
    pass


class WizApp:
    """Root of all WizLib-based CLI applications. Subclass it. Can be
    instantiated and then run multiple commands."""

    base_command = None
    name = ''

    # Set some default types so linting works
    ui: UI

    @classmethod
    def main(cls):  # pragma: nocover
        """Call this from a __main__ entrypoint"""
        cls.start(*sys.argv[1:], debug=os.getenv('DEBUG'))

    @classmethod
    def start(cls, *args, debug=False):
        """Call this from a Python entrypoint"""
        try:
            parser = WizParser(prog=cls.name)
            for handler in cls.base_command.handlers:
                handler.add_args(parser)
            ns, more = parser.parse_known_args(args)
            app = cls.initialize(**vars(ns))
            more = more if more else [cls.base_command.default]
            app.run(*more)
        except AppCancellation as cancellation:
            if str(cancellation):
                print(str(cancellation), file=sys.stderr)
        except BaseException as error:
            if debug:
                raise error
            else:
                name = type(error).__name__
                print(f"\n{RED}{name}{': ' if str(error) else ''}" +
                      f"{error}{RESET}", file=sys.stderr)
                sys.exit(1)

    @classmethod
    def initialize(cls, **vals):
        """Converts argparse values (strings) into actual handlers and
        instantiates the app"""
        handlers = {}
        for handler in cls.base_command.handlers:
            val = vals[handler.name] if (
                handler.name in vals) else handler.default
            handlers[handler.name] = handler.setup(val)
        return cls(**handlers)

    def __init__(self, **handlers):
        for name, handler in handlers.items():
            handler.app = self
            setattr(self, name, handler)
        self.parser = WizParser()
        subparsers = self.parser.add_subparsers(dest='command')
        for command in self.base_command.family_members('name'):
            key = command.get_member_attr('key')
            aliases = [key] if key else []
            subparser = subparsers.add_parser(command.name, aliases=aliases)
            command.add_args(subparser)

    def run(self, *args):
        vals = vars(self.parser.parse_args(args))
        if 'help' in vals:
            return WizHelpCommand(**vals)
        command_name = vals.pop('command')
        command_class = self.base_command.family_member(
            'name', command_name)
        if not command_class:
            raise Exception(f"Unknown command {command_name}")
        command = command_class(self, **vals)
        result = command.execute()
        if result:
            print(result, end='')
            if sys.stdout.isatty():  # pragma: nocover
                print()
        if command.status:
            print(command.status, file=sys.stderr)
