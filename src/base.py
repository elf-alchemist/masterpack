#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Masterpack base builder, a utility for creating the base.wad file needed for building masterpack.wad

from os import listdir
from hashlib import sha256

from omg.wad import WAD

VERSION = '0.3-proto'

logfile = None
LOG_FILE = 'base.log'

BUFFER_SIZE = 16384

DIR_SOURCE = 'base/'

ALPHA = 'alpha.wad'
BASE = 'beta.wad'

SOURCE_WADS = [
    # Titan
    'MINES.WAD',
    'anomaly.wad',
    'FARSIDE.WAD',
    'TROUBLE.WAD',
]

SOURCE_SHA256SUM = {
    # Alpha
    'alpha.wad': '732c51c4a16dcbd3fa59ba9b28217ffee431b311813be21f4cb1a66dbcd431ef',
    # Titan
    'MINES.WAD': 'af38046cd3523f43837d9d19fbb9e2fac7d6b5799822f33e0963cd5ca14d0d0b',
    'anomaly.wad': 'cc843c3604ae854acc7b2724704498a22fbb000a0a2dda05215e666bae7424eb',
    'FARSIDE.WAD': '5d2e937c470c5143e4f69069e372515e483ddc5c1b30742b03fc3dfb63bbd2a3',
    'TROUBLE.WAD': '2af8071d14718687cec3d03518b9bccbb1e14dc7a17f71321d2979ddd6df7e23',
}

MAP_TRIPLETS = [
    ['MAP10', 'MINES.WAD', 'MAP01'],
    ['MAP11', 'anomaly.wad', 'MAP01'],
    ['MAP12', 'FARSIDE.WAD', 'MAP01'],
    ['MAP15', 'TROUBLE.WAD', 'MAP01'],
]

BASE_MAPS = [
    # Titan
    'MAP10',
    'MAP11',
    'MAP12',
    'MAP15',
]


#
# Utils
#

def log(line: str) -> None:
    global logfile

    if not logfile:
        logfile = open(LOG_FILE, 'w')

    print(line)
    logfile.write(line + '\n')


def get_wad_filename(wad_name: str) -> str | None:
    for filename in listdir(DIR_SOURCE):
        if wad_name.lower() == filename.lower():
            return DIR_SOURCE + filename

    return None


#
# Check WAD data
#

def get_wad_pre_hash(wad_name: str) -> str | None:
    if wad_name not in SOURCE_SHA256SUM:
        return None

    return SOURCE_SHA256SUM[wad_name]


def get_wad_hash(wad_path: str) -> str | None:
    sha256hash = sha256()

    file_handler = open(wad_path, 'rb')

    while True:
        data = file_handler.read(BUFFER_SIZE)
        if not data:
            break
        sha256hash.update(data)

    return sha256hash.hexdigest()


def check_wads(found_wads: list[str]):
    for wad in SOURCE_WADS:
        if get_wad_filename(wad) == None:
            log(f'  {wad.upper()} is missing.')

        if get_wad_hash(DIR_SOURCE + wad) != get_wad_pre_hash(wad):
            log(f'  {wad.upper()} checksum does not match. Continuing with caution. If you see no other errors or warnings, ignore this one.')

        found_wads.append(wad)


#
# Actual lump-to-wad extraction
#

def base_build() -> None:
    base = WAD()

    if get_wad_hash(ALPHA) != get_wad_pre_hash(ALPHA):
        log('  Error: alpha.wad failed the checksum, something terrible happened. Try again.')
        log('Build failed.')
        exit(2)

    log('  Extracting maps...')
    for triple in MAP_TRIPLETS:
        base.maps[triple[0]] = WAD(DIR_SOURCE + triple[1]).maps[triple[2]]

    log('  Creating base.wad...')
    base.to_file(BASE)

    if get_wad_hash(BASE) != get_wad_pre_hash(BASE):
        log('  Warn: base.wad failed the checksum, you can _maybe_ build masterpack.wad.')


def base_fix() -> None:
    log('None')


def main() -> None:
    log('Checking wads.')
    found_wads: list[str] = []
    check_wads(found_wads)

    if sorted(found_wads) != sorted(SOURCE_WADS):
        log('Error: Did not find all base wads. Check base.log for more details.')
        log('Build failed. Exiting...')
        exit(1)
    log(' Found all base WADs!')

    log('Starting to build WAD.')
    base_build()

    log('Fixing maps.')
    base_fix()

    log('Build successful.')
    exit(0)


if __name__ == '__main__':
    main()
