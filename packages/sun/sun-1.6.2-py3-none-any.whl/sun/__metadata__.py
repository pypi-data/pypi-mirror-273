#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
import platform
import subprocess
from pathlib import Path


__prgnam__: str = 'sun'
__author__: str = 'dslackw'
__copyright__: str = '2015-2024'
__version__: str = '1.6.2'
__license__: str = 'GNU General Public License v3 (GPLv3)'
__email__: str = 'dslackw@gmail.com'
__website__: str = 'https://gitlab.com/dslackw/sun'


data_configs: dict = {
    'bin_path': Path('/usr/bin/'),
    'pkg_path': Path('/var/log/packages'),
    'icon_path': Path('/usr/share/pixmaps'),
    'desktop_path': Path('/usr/share/applications'),
    'xdg_autostart': Path('/etc/xdg/autostart'),
    'sun_conf_path': Path('/etc/', __prgnam__),
    'arch': platform.machine(),
    'kernel': os.uname()[2],
    'cpu': platform.processor(),
    'mem': subprocess.getoutput('free -h').split(),
    'disk': shutil.disk_usage('/'),
    'uptime': subprocess.getoutput('uptime -p')
}
