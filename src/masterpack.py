#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Masterpack for Doom II, a utility for creating the ultimate way to enjoy the Master Levels for Doom II

from os import listdir
from hashlib import sha256

from omg.wad import WAD

logfile = None
LOG_FILE = 'masterpack.log'

BUFFER_SIZE = 16384

DIR_SOURCE = 'source/'

BASE = 'base.wad'
MASTERPACK = 'masterpack.wad'

SOURCE_WADS = [
    # IWADs
    'DOOM.WAD',
    'TNT.WAD',
    # Inferno
    'VIRGIL.WAD',
    'MINOS.WAD',
    'NESSUS.WAD',
    'GERYON.WAD',
    'VESPERAS.WAD',
    # Titan
    'MANOR.WAD',
    'TTRAP.WAD',
    # Cabal
    'BLOODSEA.WAD',
    'BLACKTWR.WAD',
    'MEPHISTO.WAD',
    'TEETH.WAD',
    # Klietech
    'SUBSPACE.WAD',
    'COMBINE.WAD',
    'FISTULA.WAD',
    'SUBTERRA.WAD',
    'CATWALK.WAD',
    'GARRISON.WAD',
    # Lost Levels
    'PARADOX.WAD',
    'ATTACK.WAD',
    'CANYON.WAD',
]

SOURCE_SHA256SUM = {
    # Masterpack
    'base.wad': 'cc1381363256199b5e93031c7d84cc7d27ed1c23db83f8421d46e4ac9ed16181',
    'masterpack.wad': '0dfe970900481a6b474c51e5ceabed53754b3163674dcd9bdcd91f3cdd9df030',
    # IWADS
    'DOOM.WAD': '6fdf361847b46228cfebd9f3af09cd844282ac75f3edbb61ca4cb27103ce2e7f',
    'TNT.WAD': 'c0a9c29d023af2737953663d0e03177d9b7b7b64146c158dcc2a07f9ec18f353',
    # Inferno
    'VIRGIL.WAD': 'c468a1684be8e8055fca52c0c0b3068893481dbaeff0d25f2d72a13b340dff09',
    'MINOS.WAD': 'fc3996e52b527dd4d7e76b023eebaa0c18263c94e21115b06ba64c8cda371ec0',
    'NESSUS.WAD': '05a2e5f7e13acfe21895f6ad2ecd216052d8c5c4bcb65b67745678ca0ae3e0dc',
    'GERYON.WAD': 'ec5c0b1b846764d4b7cc8038e5fac1b1562627d0bcca413a55e918d3141cbfbc',
    'VESPERAS.WAD': '14a515f480455a4bd23c8204d9d236c9ba18c147e8c10a364300832ee804fea3',
    # Titan
    'MANOR.WAD': 'fe0a502310ef1b32597e2e82d6f7f12ad77cb603ac5838056dee86f4bae31e2f',
    'TTRAP.WAD': '90c7d8fc103e7b02b9602d5eb37fa439da1c5880355e4ee9fa53428ef30dcf45',
    # Cabal
    'BLOODSEA.WAD': '1b1acb09f4319db32903dc502d84fc034d21611e375771f4aaac66fafabea39a',
    'BLACKTWR.WAD': 'a0120667412fcf293ea13cdc31c1fa0626d7828f83a195aa09f4170797d07473',
    'MEPHISTO.WAD': '585040c5408bc66583dbe1b8e36d009c81799f7dbebd002af48e4c00088bfbd5',
    'TEETH.WAD': '629e2a6eb1a0234ef0f152384a01130b3d8cd0e44f6c292463dbc2d6ae34d14e',
    # Klietech
    'SUBSPACE.WAD': '2c61963efe338abc38b13fb01f238fd95d6b0e2a627ca78db038b9761ff6e6ac',
    'COMBINE.WAD': 'fef0ac1090ba2f0bce92503625047d726c2d8d1964561bd557234e7ab6202dff',
    'FISTULA.WAD': '864d51febc039b1431c5d75fb051f567433adbddce4bb4d8b6e959fc0b414724',
    'SUBTERRA.WAD': '3dba2abcb85ae3685c259b21bd867d542439c591c12162a36066f1fbab6cbdd8',
    'CATWALK.WAD': 'ce1241e16b2e8bb8bbceea84a281e81f865c52670e4eb3649dc7372870985b77',
    'GARRISON.WAD': '7a7a37d1f31c51ced17167f5283daffef27d79310df0c96b13f4cb1723a2417c',
    # Lost Levels
    'PARADOX.WAD': '4e9f37b8209dc7006637050876d917e9a68b053ef24e17725432781b00969bdf',
    'ATTACK.WAD': '4b9a404a4ee43ed33f7c2e208269b84b58ccfec5823afa1fe50e3dd08e927622',
    'CANYON.WAD': 'a2dd18d174d25a5d31046114bf73d87e9e13e49e9e6b509b2c9942e77d4c9ecf',
}

BASE_PATCHES = [
    # UDTWiD
    'MSKY1',
    # Master Levels
    'MSKY2_1',      # space
    'MSKY2_2',      # nebula
    'MSKY2_3',      # saturn
    'MSKY3',        # stars
    # UDTWiD
    'DRSLEEP',
    # MINES.WAD
    'ASHWALL',
    'WATER',
    'REDWALL1',
    'REDWALL2',
    # anomaly.wad
    'BLACK',
    'FIRELV',
    'ANOMALY1',
    'ANOMALY2',
    'ANOMALY3',
    'ANOMALY4',
    'ANOMALY5',
    'ANOMALY6',
    'ANOMALY7',
    'ANOMALY8',
    # TROUBLE.WAD
    'SAVED',
    'TROUBLE1',
    'TROUBLE2',
    'TROUBLE3',
    'TROUBLE4',
    'TROUBLE5',
    'SW2_3',
    'W15_6',
    'WALL40_1',
    'WALL63_2',
    'WALL76_1',
    'W109_1',
    'W109_2',
    'W110_1',
    'W113_1',
    'W113_2',
    'W113_3',
]

DOOM_PATCHES = [
    'SW2_3',
    'W15_6',
    'WALL40_1',
    'WALL63_2',
    'WALL76_1',
    'W109_1',
    'W109_2',
    'W110_1',
    'W113_1',
    'W113_2',
    'W113_3',
]

# map X, from wad Y, at slot Z
MAP_TRIPLETS = [
    # Inferno
    ['MAP03', 'VIRGIL.WAD', 'MAP03'],
    ['MAP04', 'MINOS.WAD', 'MAP05'],
    ['MAP05', 'NESSUS.WAD', 'MAP07'],
    ['MAP06', 'GERYON.WAD', 'MAP08'],
    ['MAP07', 'VESPERAS.WAD', 'MAP09'],
    ['MAP08', 'DOOM.WAD', 'E4M7'],
    # Titan
    ['MAP13', 'MANOR.WAD', 'MAP01'],
    ['MAP14', 'TTRAP.WAD', 'MAP01'],
    # Cabal
    ['MAP19', 'BLOODSEA.WAD', 'MAP07'],
    ['MAP22', 'BLACKTWR.WAD', 'MAP25'],
    ['MAP23', 'MEPHISTO.WAD', 'MAP07'],
    ['MAP25', 'TEETH.WAD', 'MAP31'],
    ['MAP27', 'TEETH.WAD', 'MAP32'],
    # Klietech
    ['MAP29', 'SUBSPACE.WAD', 'MAP01'],
    ['MAP30', 'COMBINE.WAD', 'MAP01'],
    ['MAP32', 'FISTULA.WAD', 'MAP01'],
    ['MAP33', 'SUBTERRA.WAD', 'MAP01'],
    ['MAP35', 'CATWALK.WAD', 'MAP01'],
    ['MAP37', 'GARRISON.WAD', 'MAP01'],
    # Lost Levels
    ['MAP40', 'TNT.WAD', 'MAP01'],
    ['MAP41', 'TNT.WAD', 'MAP17'],
    ['MAP43', 'PARADOX.WAD', 'MAP01'],
    ['MAP44', 'ATTACK.WAD', 'MAP01'],
    ['MAP45', 'CANYON.WAD', 'MAP01'],
]

MASTERPACK_MAPS = [
    # Inferno
    'MAP01',
    'MAP02',
    'MAP03',
    'MAP04',
    'MAP05',
    'MAP06',
    'MAP07',
    'MAP08',
    'MAP09',
    # Titan
    'MAP10',
    'MAP11',
    'MAP12',
    'MAP13',
    'MAP14',
    'MAP15',
    # Cabal
    'MAP16',
    'MAP17',
    'MAP18',
    'MAP19',
    'MAP20',
    'MAP21',
    'MAP22',
    'MAP23',
    'MAP24',
    'MAP25',
    'MAP26',
    'MAP27',
    # Klietech
    'MAP28',
    'MAP29',
    'MAP30',
    'MAP31',
    'MAP32',
    'MAP33',
    'MAP34',
    'MAP35',
    'MAP36',
    'MAP37',
    'MAP38',
    'MAP39',
    # Lost Levels
    'MAP40',
    'MAP41',
    'MAP42',
    'MAP43',
    'MAP44',
    'MAP45',
    'MAP46',
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

def masterpack_build() -> None:
    master = WAD()
    base = WAD(BASE)

    doom = WAD(DIR_SOURCE + 'DOOM.WAD')

    if get_wad_hash(BASE) != get_wad_pre_hash(BASE):
        log('  Error: base.wad failed the checksum, if you are seeing this, something terrible happened. Download and try again.')
        log('Build failed.')
        exit(2)

    log('  Extracting patches...')
    # gotta extract the Klietech sky manually
    # since it is not between P_* markers
    combine = WAD(DIR_SOURCE + 'COMBINE.WAD')
    sky = combine.data['RSKY1']
    base.patches['MSKY3'] = sky

    for doom_patch in DOOM_PATCHES:
        base.patches[doom_patch] = doom.patches[doom_patch]

    log('  Extracting maps...')
    for triple in MAP_TRIPLETS:
        base.maps[triple[0]] = WAD(DIR_SOURCE + triple[1]).maps[triple[2]]

    log('  Organizing lumps...')
    master.data += base.data
    master.music += base.music
    master.txdefs += base.txdefs
    master.graphics += base.graphics

    for patch in BASE_PATCHES:
        master.patches[patch] = base.patches[patch]

    for map in MASTERPACK_MAPS:
        master.maps[map] = base.maps[map]

    log('  Creating masterpack.wad...')
    master.to_file(MASTERPACK)

    if get_wad_hash(MASTERPACK) != get_wad_pre_hash(MASTERPACK):
        log('  Warn: masterpack.wad failed the checksum, you can probably keep playing, but there are 0 guarantees.')


def main() -> None:
    log('Checking wads.')
    found_wads: list[str] = []
    check_wads(found_wads)

    if sorted(found_wads) != sorted(SOURCE_WADS):
        log('Error: Did not find all Master Levels. Check masterpack.log for more details.')
        log('Build failed. Exiting...')
        exit(1)
    log(' Found all Master Levels WADs!')

    log('Starting to build WAD.')
    masterpack_build()

    log('Build successful.')
    exit(0)


if __name__ == '__main__':
    main()
