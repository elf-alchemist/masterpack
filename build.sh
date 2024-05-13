#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Simplest build script possible

# Bash strict mode - Early exit, instead of failing later
set -o errtrace
set -o errexit
set -o nounset
set -o pipefail

version='v0.4.0'

cd src/

zip "masterpack-${version}-windows.zip" source/delete_me.txt patches/masterpack_ml25amp.wad base.wad masterpack.exe
mv "masterpack-${version}-windows.zip" ../pkgs/
echo "Windows package built"

zip "masterpack-${version}-linux.zip" source/delete_me.txt patches/masterpack_ml25amp.wad base.wad masterpack.elf
mv "masterpack-${version}-linux.zip" ../pkgs/
echo "Linux package built"

