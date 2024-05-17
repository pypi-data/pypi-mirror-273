import typing

from everai.commands.command import ClientCommand, command_error
from everai.commands.app import app_detect, add_app_name_to_parser
from argparse import _SubParsersAction
from everai.app import App
from everai.app.app_manager import AppManager
from everai.runner.run import find_target


class CheckCommand(ClientCommand):
    def __init__(self, args):
        self.args = args

    @staticmethod
    def setup(parser: _SubParsersAction):
        check_parser = parser.add_parser("check", help="Check app is correct in app directory")

        check_parser.set_defaults(func=CheckCommand)

    @command_error
    def run(self):
        find_target(print_exception=True)

