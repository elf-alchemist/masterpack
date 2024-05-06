#!/usr/bin/env python3

from os import listdir, mkdir, path
from hashlib import sha256

from omg.wad import WAD

VERSION = '0.2-proto'

logfile = None
LOG_FILE = 'masterpack.log'

BUFFER_SIZE = 16384

DIR_SOURCE = 'source/'
DIR_BASE = 'base/'
DIR_DEST = 'dest/'

IWADS = [
    'DOOM.WAD',
    'DOOM2.WAD',
    'TNT.WAD',
]

IWADS_SHA256SUM = {
    'DOOM.WAD': '6fdf361847b46228cfebd9f3af09cd844282ac75f3edbb61ca4cb27103ce2e7f',
    'DOOM2.WAD': '10d67824b11025ddd9198e8cfc87ca335ee6e2d3e63af4180fa9b8a471893255',
    'TNT.WAD': 'c0a9c29d023af2737953663d0e03177d9b7b7b64146c158dcc2a07f9ec18f353',
}

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

ML_WADS = [
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

ML_WADS_SHA256SUM = {
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

ML_MASTERPACK = [
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

MASTERPACK_WADS = [
    'master.wad',     # empty base
    'master_p1.wad',  # special lumps, graphics and midi
    'master_p2.wad',  # pacthes
    'master_p3.wad',  # maps
]

MASTERPACK_SHA256SUM = {
    'master.wad': 'eb90ad49c63db42e7bc87eb290d80c24752dc47026f709c5cd0c8acb9de8d0fe',
    'master_p1.wad': 'cfa9f5877ccdfe6998c8fc6e764325babf4500f8a86fb7b75036b12397edec3e',
    'master_p2.wad': 'cabfa36f20a6506db9f7bf21854c5317a01698b71a7068819f46735a10202ec2',
    'master_p3.wad': '863faaef816d46822eefc9993fbadf815ec34847ccf3912380a8d775eb6e7de9',
}

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
# Check ML WAD data
#

def get_ml_wad_pre_hash(wad_name: str) -> str | None:
    if wad_name not in ML_WADS:
        return None

    return ML_WADS_SHA256SUM[wad_name]


def get_ml_wad_hash(wad_name: str) -> str | None:
    sha256hash = sha256()

    if wad_name not in ML_WADS:
        return None

    file_handler = open(DIR_SOURCE + wad_name, 'rb')

    while True:
        data = file_handler.read(BUFFER_SIZE)
        if not data:
            break
        sha256hash.update(data)

    return sha256hash.hexdigest()


def validate_ml_wad_by_hash(wad_name: str) -> str | None:
    if wad_name not in ML_WADS:
        return None
    if get_ml_wad_hash(wad_name) != get_ml_wad_pre_hash(wad_name):
        return None
    if get_ml_wad_hash(wad_name) == get_ml_wad_pre_hash(wad_name):
        return wad_name


def get_found_ml_wads() -> bool:
    found_wads: list[str] = []
    missing_wads: list[str] = []

    for wad in ML_WADS:
        if get_wad_filename(wad):
            if validate_ml_wad_by_hash(wad) == None:
                log(f'  {wad.upper()} failed SHA256 checksum!')
                missing_wads.append(wad)

            wad_name = wad.upper().split(f".")[0]
            log(f'  {wad_name} found!')
            found_wads.append(wad)

        else:
            log(f'  {wad.upper()} is missing.')
            missing_wads.append(wad)

    if sorted(found_wads) != sorted(ML_WADS):
        return False

    return True

#
# Check IWAD data
#


def get_iwad_pre_hash(iwad_name: str) -> str | None:
    if iwad_name not in IWADS:
        return None

    return IWADS_SHA256SUM[iwad_name]


def get_iwad_hash(iwad_name: str) -> str | None:
    sha256hash = sha256()

    if iwad_name not in IWADS:
        return None

    file_handler = open(DIR_SOURCE + iwad_name, 'rb')

    while True:
        data = file_handler.read(BUFFER_SIZE)
        if not data:
            break
        sha256hash.update(data)

    return sha256hash.hexdigest()


def validate_iwad_by_hash(iwad_name: str) -> str | None:
    if iwad_name not in IWADS:
        return None
    if get_iwad_hash(iwad_name) != get_iwad_pre_hash(iwad_name):
        return None
    if get_iwad_hash(iwad_name) == get_iwad_pre_hash(iwad_name):
        return iwad_name


#
# Check base PWAD data
#

#
# Actual lump-to-wad extraction
#


def extract_p1_lumps():
    log('  Base fiels extraction begins.')
    master1_wad = WAD(DIR_BASE + 'master_p1.wad')
    doom_wad = WAD(DIR_SOURCE + 'DOOM.WAD')
    doom2_wad = WAD(DIR_SOURCE + 'DOOM2.WAD')

    master1_wad.graphics['INTERPIC'] = doom_wad.graphics['INTERPIC']
    master1_wad.graphics['BOSSBACK'] = doom2_wad.graphics['INTERPIC']

    log('    First extraction done.')
    return master1_wad


def extract_p2_lumps():
    log('  Patch extraction begins.')

    master2_wad = WAD(DIR_BASE + 'master_p2.wad')
    doom_wad = WAD(DIR_SOURCE + 'DOOM.WAD')

    for doom_patch in DOOM_PATCHES:
        master2_wad.patches[doom_patch] = doom_wad.patches[doom_patch]

    log('    Second part of extraction done.')
    return master2_wad


def extract_p3_lumps():
    log('  Extracting maps.')
    master3_wad = WAD(DIR_BASE + 'master_p3.wad')

    for map in ML_MASTERPACK:
        master3_wad.maps[map[0]] = WAD(DIR_SOURCE + map[1]).maps[map[2]]

    log('    Final extraction complete. Moving on...')
    return master3_wad


def masterpack_build() -> None:
    master_wad = WAD(DIR_BASE + 'master.wad')

    master_p1_wad = extract_p1_lumps()
    master_wad.data += master_p1_wad.data
    master_wad.music += master_p1_wad.music
    master_wad.txdefs += master_p1_wad.txdefs
    master_wad.graphics += master_p1_wad.graphics

    master_p2_wad = extract_p2_lumps()
    master_wad.patches += master_p2_wad.patches

    master_p3_wad = extract_p3_lumps()
    for map in MASTERPACK_MAPS:
        master_wad.maps[map] = master_p3_wad.maps[map]

    if not path.exists(DIR_DEST):
        mkdir(DIR_DEST)
    master_wad.to_file(DIR_DEST + 'master.wad')
    return None


def main() -> None:
    log('Welcome to Master Levels Masterpack build script.')
    log('Checking ML source wads...')

    if get_found_ml_wads() == None:
        log('Did not find all Master Levels! Check missing files and failed checksums!')
        log('Build failed. Exiting...')
        exit(1)
    log('Found all Master Levels WADs!')

    log('Starting to build WAD!')
    masterpack_build()
    log('Finished build.')

    log('Done. Exiting...')
    exit(0)


if __name__ == '__main__':
    main()
