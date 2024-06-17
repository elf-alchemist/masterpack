#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>

import os
import platform

windows_cmd = 'pyinstaller src/master.py ' \
    + ' --log-level WARN' \
    + ' --onefile ' \
    + ' --add-data "src/vcdiff.zip;."' \
    + ' --icon masterpack.ico' \
    + ' --noupx'

linux_to_windows_cmd = 'wine' \
    + ' pyinstaller src/master.py' \
    + ' --log-level WARN' \
    + ' --onefile ' \
    + ' --add-data "src/vcdiff.zip;."' \
    + ' --icon masterpack.ico' \
    + ' --noupx'

linux_cmd = 'pyinstaller src/master.py' \
    + ' --log-level WARN' \
    + ' --onefile' \
    + ' --add-data=src/vcdiff.zip:.' \
    + ' --noupx'

def windows_build():
    print('Building for Windows')
    os.system(linux_to_windows_cmd)
    print('Package built')


def linux_build():
    print('Building for Windows...')
    os.system(linux_to_windows_cmd)
    print('Building for Linux...')
    os.system(linux_cmd)
    print('Packages built')


if platform.system() == '':
    print('Could not assertain the operating system. Exiting safely')
    exit(1)
elif platform.system() == 'Windows':
    print('Host is Windows.')
    windows_build()
elif platform.system() == 'Linux':
    print('Host is Linux.')
    linux_build()
