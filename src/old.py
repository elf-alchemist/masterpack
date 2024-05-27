#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>

import sys
from os import listdir, path
from shutil import copy
from tempfile import mkdtemp
from hashlib import sha256
from zipfile import ZipFile

from omg.lump import Lump
from omg.wad import WAD
from omg.mapedit import MapEditor

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS #type:ignore
else:
    base_path = path.abspath('.')

DATA_ZIP = path.join(base_path, 'data.zip')

logfile = None
LOG_FILE = 'build.log'

BUFFER_SIZE = 16384

DIR_SOURCE = 'source/'

BASE = 'base.wad'

PATCH_TRIPLETS = [
    ['MSKY1', 'UDTWiD.wad', 'SKY4'],
    ['MSKY2_1', 'MINES.WAD', 'STARS'],
    ['MSKY2_2', 'MINES.WAD', 'STARS1'],
    ['MSKY2_3', 'MINES.WAD', 'STARSAT'],

    ['DRSLEEP', 'UDTWiD.wad', 'DRSLEEP'],
    # ['', 'ACHRON22.WAD', 'SKY1'], <-- unused because MSKY1 is a MUCH better fit for Inferno

    ['ASHWALL', 'MINES.WAD', 'W104_1'],
    ['WATER', 'MINES.WAD', 'TWF'],
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

    ['SW2_3', 'DOOM.WAD', 'SW2_3'],
    ['W15_4', 'DOOM.WAD', 'W15_4'],
    ['W15_5', 'DOOM.WAD', 'W15_5'],
    ['W15_6', 'DOOM.WAD', 'W15_6'],
    ['WALL40_1', 'DOOM.WAD', 'WALL40_1'],
    ['WALL63_2', 'DOOM.WAD', 'WALL63_2'],
    ['WALL76_1', 'DOOM.WAD', 'WALL76_1'],
    ['W109_1', 'DOOM.WAD', 'W109_1'],
    ['W109_2', 'DOOM.WAD', 'W109_2'],
    ['W110_1', 'DOOM.WAD', 'W110_1'],
    ['W113_1', 'DOOM.WAD', 'W113_1'],
    ['W113_2', 'DOOM.WAD', 'W113_2'],
    ['W113_3', 'DOOM.WAD', 'W113_3'],
]

ALL_PATCHES = [
    'MSKY1',

    'MSKY2_1',
    'MSKY2_2',
    'MSKY2_3',
    'MSKY3',

    'DRSLEEP',

    'ASHWALL',
    'WATER',

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

    'SAVED',
    'TROUBLE1',
    'TROUBLE2',
    'TROUBLE3',
    'TROUBLE4',
    'TROUBLE5',

    'SW2_3',
    'W15_4',
    'W15_5',
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

SIDEDEF_SWITCH_TRIPLETS = [
    ['MAP09', 'SKY4', 'MSKY1'],

    ['MAP10', 'DBRAIN1', 'WATER'],
    ['MAP10', 'SW1COMP', 'TT1COMP'],
    ['MAP10', 'SW1STON1', 'TT1STON1'],
    ['MAP10', 'SW1STON2', 'TT1STON2'],

    ['MAP11', 'SW1STON2', 'TT1STON5'],

    ['MAP12', 'SW1BRIK', 'TT1BRIK'],
    ['MAP12', 'SW1STON1', 'TT1STON3'],
    ['MAP12', 'SW1STON2', 'TT1STON4'],

    ['MAP15', 'SW1VINE', 'TT1VINE'],
    ['MAP15', 'SW1PIPE', 'TT1PIPE'],
    ['MAP15', 'SW1STON1', 'TT1STON5'],
    ['MAP15', 'SW1STON2', 'TT1STON6'],
    ['MAP15', 'SW1STON6', 'TT1STON7'],

    ['MAP15', 'PIC00', 'PORTAL1'],
    ['MAP15', 'PIC01', 'PORTAL2'],
    ['MAP15', 'PIC06', 'PORTAL3'],
    ['MAP15', 'PIC07', 'PORTAL4'],
    ['MAP15', 'PIC13', 'PORTAL5'],
]

ALL_MAP_TRIPLETS = [
    ['MAP01', 'DANTE25.WAD', 'MAP02'],
    ['MAP02', 'ACHRON22.WAD', 'MAP03'],
    ['MAP03', 'VIRGIL.WAD', 'MAP03'],
    ['MAP04', 'MINOS.WAD', 'MAP05'],
    ['MAP05', 'NESSUS.WAD', 'MAP07'],
    ['MAP06', 'GERYON.WAD', 'MAP08'],
    ['MAP07', 'VESPERAS.WAD', 'MAP09'],
    ['MAP08', 'DOOM.WAD', 'E4M7'],
    ['MAP09', 'UDTWiD.wad', 'E4M8'],

    ['MAP10', 'MINES.WAD', 'MAP01'],
    ['MAP11', 'anomaly.wad', 'MAP01'],
    ['MAP12', 'FARSIDE.WAD', 'MAP01'],
    ['MAP13', 'MANOR.WAD', 'MAP01'],
    ['MAP14', 'TTRAP.WAD', 'MAP01'],
    ['MAP15', 'TROUBLE.WAD', 'MAP01'],

    ['MAP16', 'CABALL.WAD', 'MAP24'],
    ['MAP17', 'CABALL.WAD', 'MAP25'],
    ['MAP18', 'CABALL.WAD', 'MAP26'],
    ['MAP19', 'BLOODSEA.WAD', 'MAP07'],
    ['MAP20', 'CABALL.WAD', 'MAP27'],
    ['MAP21', 'CABALL.WAD', 'MAP28'],
    ['MAP22', 'BLACKTWR.WAD', 'MAP25'],
    ['MAP23', 'MEPHISTO.WAD', 'MAP07'],
    ['MAP24', 'CABALL.WAD', 'MAP30'],
    ['MAP25', 'TEETH.WAD', 'MAP31'],
    ['MAP26', 'CABALL.WAD', 'MAP29'],
    ['MAP27', 'TEETH.WAD', 'MAP32'],

    ['MAP28', 'cpu.wad', 'MAP01'],
    ['MAP29', 'SUBSPACE.WAD', 'MAP01'],
    ['MAP30', 'COMBINE.WAD', 'MAP01'],
    ['MAP31', 'device_1.wad', 'MAP01'],
    ['MAP32', 'FISTULA.WAD', 'MAP01'],
    ['MAP33', 'SUBTERRA.WAD', 'MAP01'],
    ['MAP34', 'dmz.wad', 'MAP01'],
    ['MAP35', 'CATWALK.WAD', 'MAP01'],
    ['MAP36', 'cdk_fury.wad', 'MAP01'],
    ['MAP38', 'e_inside.wad', 'MAP01'],
    ['MAP37', 'GARRISON.WAD', 'MAP01'],
    ['MAP39', 'hive.wad', 'MAP01'],

    ['MAP40', 'TNT.WAD', 'MAP01'],
    ['MAP41', 'TNT.WAD', 'MAP17'],
    ['MAP42', 'TWM01.WAD', 'MAP03'],
    ['MAP43', 'PARADOX.WAD', 'MAP01'],
    ['MAP44', 'ATTACK.WAD', 'MAP01'],
    ['MAP45', 'CANYON.WAD', 'MAP01'],
    ['MAP46', 'kickdm2.wad', 'MAP01'],
]

ALL_MAPS = [
    'MAP01', 'MAP02', 'MAP03', 'MAP04', 'MAP05', 'MAP06', 'MAP07', 'MAP08', 'MAP09',
    'MAP10', 'MAP11', 'MAP12', 'MAP13', 'MAP14', 'MAP15',
    'MAP16', 'MAP17', 'MAP18', 'MAP19', 'MAP20', 'MAP21', 'MAP22', 'MAP23', 'MAP24', 'MAP25', 'MAP26', 'MAP27',
    'MAP28', 'MAP29', 'MAP30', 'MAP31', 'MAP32', 'MAP33', 'MAP34', 'MAP35', 'MAP36', 'MAP37', 'MAP38', 'MAP39',
    'MAP40', 'MAP41', 'MAP42', 'MAP43', 'MAP44', 'MAP45', 'MAP46',
]


DOOM1_MIDI = [
    'D_INTRO', 'D_INTROA', 'D_INTER', 'D_VICTOR', 'D_BUNNY',
    'D_E1M1', 'D_E1M2', 'D_E1M3', 'D_E1M4', 'D_E1M5', 'D_E1M6', 'D_E1M7', 'D_E1M8', 'D_E1M9',
    'D_E2M1', 'D_E2M2', 'D_E2M3', 'D_E2M4', 'D_E2M5', 'D_E2M6', 'D_E2M7', 'D_E2M8', 'D_E2M9',
    'D_E3M1', 'D_E3M2', 'D_E3M3', 'D_E3M4', 'D_E3M5', 'D_E3M6', 'D_E3M7', 'D_E3M8', 'D_E3M9',
    'D_E4M1', 'D_E4M2', 'D_E4M3', 'D_E4M4', 'D_E4M5', 'D_E4M6', 'D_E4M7', 'D_E4M8', 'D_E4M9',
]

DOOM2_MIDI = [
    'D_DM2TTL', 'D_DM2INT', 'D_READ_M',
    'D_RUNNIN', 'D_STALKS', 'D_COUNTD', 'D_BETWEE', 'D_DOOM',   'D_THE_DA', 'D_SHAWN',  'D_DDTBLU', 'D_IN_CIT', 'D_DEAD', 'D_STLKS2',
    'D_THEDA2', 'D_DOOM2',  'D_DDTBL2', 'D_RUNNI2', 'D_DEAD2',  'D_STLKS3', 'D_ROMERO', 'D_SHAWN2', 'D_MESSAG',
    'D_COUNT2', 'D_DDTBL3', 'D_AMPIE',  'D_THEDA3', 'D_ADRIAN', 'D_MESSG2', 'D_ROMER2', 'D_TENSE',  'D_SHAWN3', 'D_OPENIN', 'D_EVIL', 'D_ULTIMA',
]

#
# Utils
#


def log(line: str):
    global logfile

    if not logfile:
        logfile = open(LOG_FILE, 'w')

    print(line)
    logfile.write(line + '\n')


def check_wad(dir: str, wad_name: str):
    for filename in listdir(dir):
        if wad_name.lower() == filename.lower():
            return dir + filename

    return None


#
# Actual lump-to-wad extraction
#

def base_build(dir: str):
    masterpack = WAD()
    base = WAD(dir + BASE)
    tnt = WAD(dir + 'TNT.WAD')

    log('  Extracting DEMOs')
    demo1lmp = tnt.data['DEMO1'] #type:ignore
    demo1data = bytearray(demo1lmp.data)
    demo1data[3] = 0x28 # change map01 to map40
    base.data['DEMO1'] = Lump(bytes(demo1data)) #type:ignore

    demo2lmp = Lump(from_file=dir + 'DANTE25.LMP')
    demo2data = bytearray(demo2lmp.data)
    demo2data[3] = 0x01 # change map02 to map01
    base.data['DEMO2'] = Lump(bytes(demo2data)) #type:ignore

    log('  Extracting patches')
    # gotta extract the Klietech sky manually
    # since it is not located between P_* markers
    combine = WAD(DIR_SOURCE + 'COMBINE.WAD')
    sky = combine.data['RSKY1'] #type:ignore
    base.patches['MSKY3'] = sky #type:ignore
    log('    Pulling MSKY3')

    for triple in PATCH_TRIPLETS:
        wad_name = triple[1]
        wad = WAD(dir + wad_name)

        original_name = triple[2]
        slot = wad.patches[original_name] #type:ignore

        name = triple[0]
        base.patches[name] = slot #type:ignore

        log(f'    Pulling {name}')

    log('    Sorting patches')
    for slot in ALL_PATCHES:
        masterpack.patches[slot] = base.patches[slot] #type:ignore


def main():
    log('Setting up.')

    data = ZipFile(DATA_ZIP, 'r')

    temp = mkdtemp()
    data.extractall(temp)

    for file in listdir(DIR_SOURCE):
        origin = path.join(DIR_SOURCE, file)
        dest = path.join(temp, file)
        copy(origin, dest)

    log('Found all WADs!')

    log('Starting to build masterpack.wad.')
    base_build(temp + '/')

    log('Build successful')
