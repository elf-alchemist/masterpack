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

FILE="masterpack.zip"

if [[ -e "${FILE}" ]]; then rm "${FILE}"; fi

zip "${FILE}" omg/* source/delete_me.txt base.wad masterpack.py
