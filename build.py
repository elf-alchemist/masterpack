#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Simplest build script possible

from os import remove
from shutil import move
from zipfile import ZipFile

version = "v0.4.1"
windows_pkg = f"masterpack-{version}-windows.zip"
linux_pkg = f"masterpack-{version}-linux.zip"
pkgs = "pkgs/"


def create_zip_package(name: str, files: list[tuple[str, str | None]]) -> None:
    with ZipFile(name, "w") as zipf:
        for src_file, arc_name in files:
            zipf.write(src_file, arc_name)


create_zip_package(
    windows_pkg,
    files=[
        ("source/delete_me.txt", None),
        ("patches/masterpack_ml25amp.wad", None),
        ("src/base.wad", "base.wad"),
        ("src/data.zip", "data.zip"),
        ("dist/masterpack.exe", "masterpack.exe"),
    ],
)
move(windows_pkg, pkgs + windows_pkg)
print("Windows package built")
