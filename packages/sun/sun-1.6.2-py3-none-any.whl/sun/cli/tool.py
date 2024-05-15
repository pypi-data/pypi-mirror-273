#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import getpass
import subprocess
from sun.configs import Configs
from sun.utils import Utilities, Fetch
from sun.__metadata__ import __version__, data_configs


class Tools(Configs):

    """ SUN Utilities.
    """

    def __init__(self):
        super(Configs, self).__init__()
        self.data_configs: dict = data_configs
        self.utils = Utilities()
        self.fetch = Fetch()

    @staticmethod
    def su() -> None:
        """ Root privileges not required. """
        if getpass.getuser() == 'root':
            raise SystemExit('sun: Error: It should not be run as root')

    @staticmethod
    def usage() -> None:
        """ Usage help menu. """
        args: str = (f'SUN (Slackware Update Notifier) - Version: {__version__}\n'
                     '\nUsage: sun [OPTIONS]\n'
                     '\nOptional arguments:\n'
                     '  help       Display this help and exit.\n'
                     '  start      Start sun daemon.\n'
                     '  stop       Stop sun daemon.\n'
                     '  restart    Restart sun daemon.\n'
                     '  check      Check for software updates.\n'
                     '  status     Sun daemon status.\n'
                     '  info       Os and machine information.\n'
                     '\nStart GTK icon from the terminal: sun start --gtk')
        print(args)

    def check_updates(self) -> tuple:
        """ Returns the count of the packages and the message. """
        message: str = 'No news is good news!'
        packages: list = list(self.fetch.updates())
        count_packages: int = len(packages)
        count_repositories: int = len({repo.split(':')[0] for repo in packages})
        repositories_message: str = str()

        if count_repositories > 1:
            repositories_message: str = f'from {count_repositories} repositories'

        if count_packages > 0:
            message: str = f'{count_packages} software updates are available {repositories_message}\n'

        return message, packages

    def view_updates(self) -> None:
        """ Prints the updates packages to the terminal. """
        message, packages = self.check_updates()
        print(message)
        if len(packages) > 0:
            for package in packages:
                print(package)

    def daemon_status(self) -> bool:
        """ Returns the daemon status. """
        output = subprocess.run(self.sun_daemon_running, shell=True, check=False)
        if output.returncode == 0:
            return True
        return False

    def daemon_process(self, arg: str, message: str) -> str:
        """ Returns the daemon status message. """
        output: int = 1

        command: dict = {
            'start': self.sun_daemon_start,
            'stop': self.sun_daemon_stop,
            'restart': self.sun_daemon_restart
        }

        if self.daemon_status() and arg == 'start':
            message: str = 'SUN is already running'
        elif not self.daemon_status() and arg == 'stop':
            message: str = 'SUN is not running'
        elif not self.daemon_status() and arg == 'restart':
            message: str = 'SUN is not running'
        else:
            output: int = subprocess.call(command[arg], shell=True)

        if output > 0:
            message: str = f'FAILED [{output}]: {message}'

        return message


class Cli:
    """ Command line control menu.
    """

    def __init__(self):
        self.args: list = []
        self.tools = Tools()
        self.utils = Utilities()

    def menu(self) -> None:
        """ Menu call methods.
        """
        self.tools.su()
        self.args: list = sys.argv
        self.args.pop(0)

        process: dict = {
            'start': self.view_start,
            'stop': self.view_stop,
            'restart': self.view_restart,
            'status': self.view_status,
            'check': self.tools.view_updates,
            'info': self.view_info,
            'help': self.tools.usage
        }

        if len(self.args) == 1:
            try:
                process[self.args[0]]()
            except KeyError as e:
                raise SystemExit("try: 'sun help'") from e

        elif len(self.args) == 2 and self.args[0] == 'start' and self.args[1] == '--gtk':
            subprocess.call('sun-gtk &', shell=True)

        else:
            raise SystemExit("try: 'sun help'")

    def view_start(self) -> None:
        """ View starting message.
        """
        print(self.tools.daemon_process(self.args[0], 'Starting SUN daemon:  sun-daemon &'))

    def view_stop(self) -> None:
        """ View stopping message.
        """
        print(self.tools.daemon_process(self.args[0], 'Stopping SUN daemon:  sun-daemon'))

    def view_restart(self) -> None:
        """ View restarting message.
        """
        print(self.tools.daemon_process(self.args[0], 'Restarting SUN daemon:  sun-daemon'))

    def view_status(self) -> None:
        """ View status message.
        """
        print('SUN is running...' if self.tools.daemon_status() else 'SUN is not running')

    def view_info(self) -> None:
        """ View info message.
        """
        print(self.utils.os_info())


def main() -> None:
    """ Call menu object.
    """
    try:
        cli = Cli()
        cli.menu()
    except KeyboardInterrupt as e:
        raise SystemExit(1) from e
