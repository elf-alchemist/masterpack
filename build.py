#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>

import os
import platform
import shutil
import zipfile


version = 'v0.5.0'

windows = 'masterpack-' + version + '-windows.zip'
linux = 'masterpack-' + version + '-linux.zip'
addons = 'masterpack-addons-alpha.zip'

pkg_windows = 'pkgs/' + windows
pkg_linux = 'pkgs/' + linux
pkg_addons = 'pkgs/' + addons


windows_cmd = 'pyinstaller src/master.py ' \
    + ' --log-level WARN' \
    + ' --paths venv/lib64/python3.11/site-packages/' \
    + ' --onefile ' \
    + ' --add-data "src/vcdiff.zip;."' \
    + ' --icon masterpack.ico' \
    + ' --noupx'

linux_to_windows_cmd = 'wine' \
    + ' pyinstaller src/master.py' \
    + ' --log-level WARN' \
    + ' --paths venv/lib64/python3.11/site-packages/' \
    + ' --onefile ' \
    + ' --add-data "src/vcdiff.zip;."' \
    + ' --icon masterpack.ico' \
    + ' --noupx'

linux_cmd = 'pyinstaller src/master.py' \
    + ' --log-level WARN' \
    + ' --paths venv/lib64/python3.11/site-packages/' \
    + ' --onefile' \
    + ' --add-data=src/vcdiff.zip:.' \
    + ' --noupx'


def create_zip_package(name: str, files: list[tuple[str, str | None]]) -> None:
    file_path = os.path.join('pkgs/', name)
    if os.path.isfile(file_path):
        return None
    with zipfile.ZipFile(name, 'w') as zipf:
        for src_file, arc_name in files:
            zipf.write(src_file, arc_name)


def windows_build():
    print('Building for Windows')
    os.system(linux_to_windows_cmd)
    create_zip_package(
        windows,
        files=[
            ('source/delete_me.txt', None),
            ('dist/master.exe', 'masterpack.exe'),
        ],
    )
    shutil.move(windows, pkg_windows)
    print('Bundling addons...')
    create_zip_package(
        addons,
        files=[
            ('addons/masterpack-ml25amp.wad', 'masterpack-ml25amp.wad'),
            ('addons/masterpack-freedoom-tc.wad', 'masterpack-freedoom-tc-alpha.wad'),
            ('addons/masterpack-psx-tc.wad', 'masterpack-psx-tc-alpha.wad'),
        ]
    )
    shutil.move(addons, pkg_addons)
    print('Package built')


def linux_build():
    print('Building for Windows...')
    os.system(linux_to_windows_cmd)
    create_zip_package(
        windows,
        files=[
            ('source/delete_me.txt', None),
            ('dist/master.exe', 'masterpack.exe'),
        ],
    )
    shutil.move(windows, pkg_windows)
    print('Building for Linux...')
    os.system(linux_cmd)
    create_zip_package(
        linux,
        files=[
            ('source/delete_me.txt', None),
            ('dist/master', 'masterpack.elf'),
        ],
    )
    shutil.move(linux, pkg_linux)
    print('Bundling addons...')
    create_zip_package(
        addons,
        files=[
            ('addons/masterpack-ml25amp.wad', 'masterpack-ml25amp.wad'),
            ('addons/masterpack-freedoom-tc.wad', 'masterpack-freedoom-tc-alpha.wad'),
            ('addons/masterpack-psx-tc.wad', 'masterpack-psx-tc-alpha.wad'),
        ]
    )
    shutil.move(addons, pkg_addons)
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
