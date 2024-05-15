#!/usr/bin/python3
# -*- coding: utf-8 -*-

import time
import notify2

from sun.cli.tool import Tools
from sun.configs import Configs
from sun.utils import Fetch
from sun.__metadata__ import __prgnam__, data_configs


class Notify(Configs):
    """ Main notify Class.
    """

    def __init__(self):
        super(Configs, self).__init__()
        self.tool = Tools()
        self.fetch = Fetch()

        self.notify = None
        self.icon = None
        self.message: str = str()
        self.count_packages: int = 0
        self.title: str = f"{'':>10}Software Updates"
        self.icon: str = f'{data_configs["icon_path"]}/{__prgnam__}.png'

        notify2.uninit()
        notify2.init('sun')

    def set_notification_message(self) -> None:
        """ Set dbus notification message.
        """
        self.count_packages: int = len(list(self.fetch.updates()))
        self.message: str = f"{'':>3}{self.count_packages} Software updates are available\n"
        self.notify = notify2.Notification(self.title, self.message, self.icon)
        self.notify.set_timeout(60000 * self.standby)

    def daemon(self) -> None:
        """ SUN daemon.
        """
        while True:
            self.set_notification_message()
            if self.count_packages > 0:
                self.notify.show()

            time.sleep(60 * self.interval)


def main() -> None:
    """ Starts the daemon.

    Raises:
        SystemExit: Exit code 1.
    """
    try:
        notify = Notify()
        notify.daemon()
    except KeyboardInterrupt as e:
        raise SystemExit(1) from e
