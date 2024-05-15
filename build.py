#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Simplest build script possible

from os import system
from shutil import move
from zipfile import ZipFile


version = 'v0.4.4'

windows = 'masterpack-' + version + '-windows.zip'
linux = 'masterpack-' + version + '-linux.zip'

pkg_windows = 'pkgs/' + windows
pkg_linux = 'pkgs/' + linux

windows_cmd = 'wine' \
    + ' pyinstaller src/masterpack.py' \
    + ' --log-level WARN' \
    + ' --paths venv/lib64/python3.11/site-packages/' \
    + ' --onefile ' \
    + ' --add-data "src/data.zip;."' \
    + ' --icon masterpack.ico' \
    + ' --noupx'

linux_cmd = 'pyinstaller src/masterpack.py' \
    + ' --log-level WARN' \
    + ' --paths venv/lib64/python3.11/site-packages/' \
    + ' --onefile' \
    + ' --add-data=src/data.zip:.' \
    + ' --noupx'

def create_zip_package(name: str, files: list[tuple[str, str | None]]) -> None:
    with ZipFile(name, 'w') as zipf:
        for src_file, arc_name in files:
            zipf.write(src_file, arc_name)


print('Building for Windows...')
system(windows_cmd)
create_zip_package(
    windows,
    files=[
        ('source/delete_me.txt', None),
        ('patches/masterpack-ml25amp.wad', None),
        ('src/data.zip', 'data.zip'),
        ('dist/masterpack.exe', 'masterpack.exe'),
    ],
)
move(windows, pkg_windows)


print('Building for Linux...')
system(linux_cmd)
create_zip_package(
    linux,
    files=[
        ('source/delete_me.txt', None),
        ('patches/masterpack-ml25amp.wad', None),
        ('src/data.zip', 'data.zip'),
        ('dist/masterpack', 'masterpack.elf'),
    ],
)
move(linux, pkg_linux)

print('Packages built')
