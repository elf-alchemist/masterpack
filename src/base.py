#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Masterpack base builder, a utility for creating the base.wad file needed for building masterpack.wad

from os import listdir
from hashlib import sha256
from pprint import pprint

from omg.wad import WAD
from omg.mapedit import MapEditor

logfile = None
LOG_FILE = 'base.log'

BUFFER_SIZE = 16384

DIR_SOURCE = 'base/'

ALPHA = 'alpha.wad'
BASE = 'beta.wad'

SOURCE_WADS = [
    'DANTE25.WAD', 'ACHRON22.WAD', 'UDTWiD.wad',
    'MINES.WAD', 'anomaly.wad', 'FARSIDE.WAD', 'TROUBLE.WAD',
    'CABALL.WAD',
    'cpu.wad', 'device_1.wad', 'dmz.wad', 'cdk_fury.wad', 'e_inside.wad', 'hive.wad',
    'ultimidi.wad', 'midtwid2.wad',
]

SOURCE_SHA256SUM = {
    'alpha.wad': 'a51d69955c4a0141fb353f6732cf4421ea275f641789e10907a0169b34915234',

    'DANTE25.WAD': '8ac0ce535c75027f46a8909ad6fa7c173ba1457a76167a05ac2213d5606cf902',
    'ACHRON22.WAD': '9c285f5b14b5a26a5e46e0c5566a1fbfc94a170a9d0d6c2dee19069b3e4d5423',
    'UDTWiD.wad': '523108f0341da424fc390c2a43cb3a9d418f0137298e85b19d12272da4021ec7',

    'MINES.WAD': '4156ed584a667f3d97cd4e3795e0cafa7194404855d9c88826e6e417da9e5d5d',
    'anomaly.wad': 'e0d3efc52add92974cf989c34ce93dbb35149041a1192a2ea169e24922490dad',
    'FARSIDE.WAD': '55e40715b49c201ea035eef00b5ece40243ca217a56b20c1fb7625c7103ac277',
    'TROUBLE.WAD': '8f89694bdaeb10709acea88423929bf4ea75cfc8f6d406565151076ccbc365f5',

    'CABALL.WAD': '5ed07c63382124793eb8c2881a4d85da15d430d32265c14d8452930ef3f2c2c4',

    'cpu.wad': '9377554a75a18eaa2cd60a8707040efeaa21d136e842b0060d4262972f6b790f',
    'device_1.wad': 'f1493e01d7f3fdcda098ebf4c48560fe098b9c56610650b44bd535e0255d7d54',
    'dmz.wad': '365e62691813d9653d588c65590b889cf0fb16276363c3d5454fbcabbb45eaea',
    'cdk_fury.wad': '1cafc59bd422991c93f9c34830793375c9914cf4ffae88db927867d6871888a8',
    'e_inside.wad': 'f5f97aa3f09c97a99f3721aeda32037e55cf4f936f9a74fa8d4c5bcf57ab3eae',
    'hive.wad': '754479211ffcbf240c08c6cdc6c1912f1c2eee3626682d04fe286a8fb55d1d70',

    'ultimidi.wad': 'cff289109308dceffb0f2e9361196bda1c35edca7665c5ad604d335ad8d756c5',
    'midtwid2.wad': '54806d8606273cda58db29477fb3fc8be8e40c774f587dda217dab1015e1547b',
}

PATCH_TRIPLETS = [
    # patch X, in wad Y, as Z
    ['MSKY1', 'UDTWiD.wad', 'SKY4'],
    ['MSKY2_1', 'MINES.WAD', 'STARS'],
    ['MSKY2_2', 'MINES.WAD', 'STARS1'],
    ['MSKY2_3', 'MINES.WAD', 'STARSAT'],

    ['DRSLEEP', 'UDTWiD.wad', 'DRSLEEP'],
    # ['UN_SKY', 'ACHRON22.WAD', 'SKY1'],
    # ^ unused because MSKY1 is a MUCH better fit for Inferno

    ['ASHWALL', 'MINES.WAD', 'W104_1'],
    ['WATER', 'MINES.WAD', 'TWF'],
    ['REDWALL1', 'MINES.WAD', 'W15_4'],
    ['REDWALL2', 'MINES.WAD', 'W15_5'],
    ['BLACK', 'anomaly.wad', 'BLACK'],
    ['FIRELV', 'anomaly.wad', 'FIRELV'],
    ['ANOMALY1', 'anomaly.wad', 'S_DOOM09'],
    ['ANOMALY2', 'anomaly.wad', 'S_DOOM10'],
    ['ANOMALY3', 'anomaly.wad', 'S_DOOM11'],
    ['ANOMALY4', 'anomaly.wad', 'S_DOOM12'],
    ['ANOMALY5', 'anomaly.wad', 'S_DOOM13'],
    ['ANOMALY6', 'anomaly.wad', 'S_DOOM14'],
    ['ANOMALY7', 'anomaly.wad', 'S_DOOM15'],
    ['ANOMALY8', 'anomaly.wad', 'S_DOOM16'],
    ['SAVED', 'TROUBLE.WAD', 'SAVED'],
    ['TROUBLE1', 'TROUBLE.WAD', 'TROU00'],
    ['TROUBLE2', 'TROUBLE.WAD', 'TROU01'],
    ['TROUBLE3', 'TROUBLE.WAD', 'TROU06'],
    ['TROUBLE4', 'TROUBLE.WAD', 'TROU07'],
    ['TROUBLE5', 'TROUBLE.WAD', 'TROU13'],
]

MAP_TRIPLETS = [

    ['MAP01', 'DANTE25.WAD', 'MAP02'],
    ['MAP02', 'ACHRON22.WAD', 'MAP03'],
    ['MAP09', 'UDTWiD.wad', 'E4M8'],

    ['MAP10', 'MINES.WAD', 'MAP01'],
    ['MAP11', 'anomaly.wad', 'MAP01'],
    ['MAP12', 'FARSIDE.WAD', 'MAP01'],
    ['MAP15', 'TROUBLE.WAD', 'MAP01'],

    ['MAP16', 'CABALL.WAD', 'MAP24'],
    ['MAP17', 'CABALL.WAD', 'MAP25'],
    ['MAP18', 'CABALL.WAD', 'MAP26'],
    ['MAP20', 'CABALL.WAD', 'MAP27'],
    ['MAP21', 'CABALL.WAD', 'MAP28'],
    ['MAP24', 'CABALL.WAD', 'MAP30'],
    ['MAP26', 'CABALL.WAD', 'MAP29'],

    ['MAP28', 'cpu.wad', 'MAP01'],
    ['MAP31', 'device_1.wad', 'MAP01'],
    ['MAP34', 'dmz.wad', 'MAP01'],
    ['MAP36', 'cdk_fury.wad', 'MAP01'],
    ['MAP38', 'e_inside.wad', 'MAP01'],
    ['MAP39', 'hive.wad', 'MAP01'],

    ['MAP42', 'TWM01.WAD', 'MAP03'],
    ['MAP46', 'kickdm2.wad', 'MAP01'],
]

BASE_MAPS = [
    'MAP01', 'MAP02', 'MAP09',
    'MAP10', 'MAP11', 'MAP12', 'MAP15',
    'MAP16', 'MAP17', 'MAP18', 'MAP20', 'MAP21', 'MAP24', 'MAP26',
    'MAP28', 'MAP31', 'MAP34', 'MAP36', 'MAP38', 'MAP39',
    'MAP42', 'MAP46',
]

ULTIMIDI = [
    'D_INTRO', 'D_INTROA', 'D_INTER', 'D_VICTOR', 'D_BUNNY',
    'D_E1M1', 'D_E1M2', 'D_E1M3', 'D_E1M4', 'D_E1M5', 'D_E1M6', 'D_E1M7', 'D_E1M8', 'D_E1M9',
    'D_E2M1', 'D_E2M2', 'D_E2M3', 'D_E2M4', 'D_E2M5', 'D_E2M6', 'D_E2M7', 'D_E2M8', 'D_E2M9',
    'D_E3M1', 'D_E3M2', 'D_E3M3', 'D_E3M4', 'D_E3M5', 'D_E3M6', 'D_E3M7', 'D_E3M8', 'D_E3M9',
    'D_E4M1', 'D_E4M2', 'D_E4M3', 'D_E4M4', 'D_E4M5', 'D_E4M6', 'D_E4M7', 'D_E4M8', 'D_E4M9',
]

MIDTWID = [
    'D_DM2TTL', 'D_DM2INT', 'D_READ_M',
    'D_RUNNIN', 'D_STALKS', 'D_COUNTD', 'D_BETWEE', 'D_DOOM',   'D_THE_DA', 'D_SHAWN',  'D_DDTBLU',
    'D_IN_CIT', 'D_DEAD',   'D_STLKS2', 'D_THEDA2', 'D_DOOM2',  'D_DDTBL2', 'D_RUNNI2', 'D_DEAD2',
    'D_STLKS3', 'D_ROMERO', 'D_SHAWN2', 'D_MESSAG', 'D_COUNT2', 'D_DDTBL3', 'D_AMPIE',  'D_THEDA3',
    'D_ADRIAN', 'D_MESSG2', 'D_ROMER2', 'D_TENSE',  'D_SHAWN3', 'D_OPENIN', 'D_EVIL',   'D_ULTIMA',
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


def massive_simple_sidedef_switch(map: MapEditor, initial_tx: str, desired_tx: str) -> None:
    for sidedef in map.sidedefs:
        if sidedef.tx_up == initial_tx:
            sidedef.tx_up = desired_tx
        if sidedef.tx_mid == initial_tx:
            sidedef.tx_mid = desired_tx
        if sidedef.tx_low == initial_tx:
            sidedef.tx_low = desired_tx


def base_build() -> None:
    base = WAD()
    alpha = WAD('alpha.wad')

    midi1 = WAD(DIR_SOURCE + 'ultimidi.wad')
    midi2 = WAD(DIR_SOURCE + 'midtwid2.wad')

    log('  Extracting patches...')
    for triple in PATCH_TRIPLETS:
        wad = WAD(DIR_SOURCE + triple[1])
        patch = wad.patches[triple[2]]
        alpha.patches[triple[0]] = patch

    log('  Extracting maps...')
    for triple in MAP_TRIPLETS:
        wad = WAD(DIR_SOURCE + triple[1])
        map = wad.maps[triple[2]]
        alpha.maps[triple[0]] = map

    log('    Fixing MAP09...')
    map09 = MapEditor(alpha.maps['MAP09'])
    massive_simple_sidedef_switch(map09, 'SKY4', 'MSKY1')
    alpha.maps['MAP09'] = map09.to_lumps()

    log('    Fixing MAP10...')
    map10 = MapEditor(alpha.maps['MAP10'])
    massive_simple_sidedef_switch(map10, 'DBRAIN1', 'WATER')
    massive_simple_sidedef_switch(map10, 'SW1COMP', 'TT1COMP')
    massive_simple_sidedef_switch(map10, 'SW2COMP', 'TT2COMP')
    massive_simple_sidedef_switch(map10, 'SW1STON1', 'TT1STON1')
    massive_simple_sidedef_switch(map10, 'SW2STON1', 'TT2STON1')
    alpha.maps['MAP10'] = map10.to_lumps()

    log('    Fixing MAP11...')
    map11 = MapEditor(alpha.maps['MAP11'])
    massive_simple_sidedef_switch(map11, 'SW1STON2', 'TT1STON2')
    massive_simple_sidedef_switch(map11, 'SW2STON2', 'TT2STON2')
    alpha.maps['MAP11'] = map11.to_lumps()

    log('    Fixing MAP12...')
    map12 = MapEditor(alpha.maps['MAP12'])
    massive_simple_sidedef_switch(map12, 'SW1BRIK', 'TT1BRIK')
    massive_simple_sidedef_switch(map12, 'SW2BRIK', 'TT2BRIK')
    massive_simple_sidedef_switch(map12, 'SW1STON3', 'TT1STON3')
    massive_simple_sidedef_switch(map12, 'SW2STON3', 'TT2STON3')
    massive_simple_sidedef_switch(map12, 'SW1STON4', 'TT1STON4')
    massive_simple_sidedef_switch(map12, 'SW2STON4', 'TT2STON4')
    alpha.maps['MAP12'] = map12.to_lumps()

    log('    Fixing MAP15...')
    map15 = MapEditor(alpha.maps['MAP15'])
    massive_simple_sidedef_switch(map15, 'SW1VINE', 'TT1VINE')
    massive_simple_sidedef_switch(map15, 'SW2VINE', 'TT2VINE')
    massive_simple_sidedef_switch(map15, 'SW1PIPE', 'TT1PIPE')
    massive_simple_sidedef_switch(map15, 'SW2PIPE', 'TT2PIPE')
    massive_simple_sidedef_switch(map15, 'SW1STON5', 'TT1STON5')
    massive_simple_sidedef_switch(map15, 'SW2STON5', 'TT2STON5')
    massive_simple_sidedef_switch(map15, 'SW1STON6', 'TT1STON6')
    massive_simple_sidedef_switch(map15, 'SW2STON6', 'TT2STON6')
    massive_simple_sidedef_switch(map15, 'SW1STON7', 'TT1STON7')
    massive_simple_sidedef_switch(map15, 'SW2STON7', 'TT2STON7')
    massive_simple_sidedef_switch(map15, 'PIC00', 'PORTAL1')
    massive_simple_sidedef_switch(map15, 'PIC01', 'PORTAL2')
    massive_simple_sidedef_switch(map15, 'PIC06', 'PORTAL3')
    massive_simple_sidedef_switch(map15, 'PIC07', 'PORTAL4')
    massive_simple_sidedef_switch(map15, 'PIC13', 'PORTAL5')
    alpha.maps['MAP15'] = map15.to_lumps()

    log('  Transferring lumps...')
    base.data += alpha.data
    base.txdefs += alpha.txdefs
    base.patches += alpha.patches
    base.sprites += alpha.sprites
    base.graphics += alpha.graphics

    for midi in ULTIMIDI:
        base.music[midi] = midi1.music[midi]

    for midi in MIDTWID:
        base.music[midi] = midi2.music[midi]

    for map in BASE_MAPS:
        base.maps[map] = alpha.maps[map]

    log('  Creating base.wad...')
    base.to_file(BASE)


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

    log('Build successful.')
    exit(0)


if __name__ == '__main__':
    main()
