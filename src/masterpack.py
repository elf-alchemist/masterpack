#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>
#
# Description:
#     Masterpack build script. Bring together all Master Levels for Doom II in one single package.

from os import listdir, path
from shutil import copy
from tempfile import mkdtemp
from hashlib import sha256
from zipfile import ZipFile

from omg.wad import WAD
from omg.mapedit import MapEditor

logfile = None
LOG_FILE = 'build.log'

BUFFER_SIZE = 16384

DIR_SOURCE = 'source/'

BASE = 'base.wad'
MASTERPACK = 'masterpack.wad'

ALL_WADS = [
    'DOOM.WAD', 'TNT.WAD',
    'DANTE25.WAD', 'ACHRON22.WAD', 'VIRGIL.WAD', 'MINOS.WAD', 'NESSUS.WAD', 'GERYON.WAD', 'VESPERAS.WAD', 'UDTWiD.wad',
    'MINES.WAD', 'anomaly.wad', 'FARSIDE.WAD', 'MANOR.WAD', 'TTRAP.WAD', 'TROUBLE.WAD',
    'CABALL.WAD', 'BLOODSEA.WAD', 'BLACKTWR.WAD', 'MEPHISTO.WAD', 'TEETH.WAD',
    'cpu.wad', 'SUBSPACE.WAD', 'COMBINE.WAD', 'device_1.wad', 'FISTULA.WAD', 'SUBTERRA.WAD', 'dmz.wad', 'CATWALK.WAD', 'cdk_fury.wad', 'GARRISON.WAD', 'e_inside.wad', 'hive.wad',
    'TWM01.WAD', 'PARADOX.WAD', 'ATTACK.WAD', 'CANYON.WAD', 'kickdm2.wad',
    'ultimidi.wad', 'midtwid2.wad',
]

SHA256_DIGEST = {
    'data.zip': 'eeaea73652980fc5068266a5d077394e5847acfeaae500c1794c84adccbcf8c5',

    'DOOM.WAD': '6fdf361847b46228cfebd9f3af09cd844282ac75f3edbb61ca4cb27103ce2e7f',
    'TNT.WAD': 'c0a9c29d023af2737953663d0e03177d9b7b7b64146c158dcc2a07f9ec18f353',

    'DANTE25.WAD': '8ac0ce535c75027f46a8909ad6fa7c173ba1457a76167a05ac2213d5606cf902',
    'ACHRON22.WAD': '9c285f5b14b5a26a5e46e0c5566a1fbfc94a170a9d0d6c2dee19069b3e4d5423',
    'VIRGIL.WAD': 'c468a1684be8e8055fca52c0c0b3068893481dbaeff0d25f2d72a13b340dff09',
    'MINOS.WAD': 'fc3996e52b527dd4d7e76b023eebaa0c18263c94e21115b06ba64c8cda371ec0',
    'NESSUS.WAD': '05a2e5f7e13acfe21895f6ad2ecd216052d8c5c4bcb65b67745678ca0ae3e0dc',
    'GERYON.WAD': 'ec5c0b1b846764d4b7cc8038e5fac1b1562627d0bcca413a55e918d3141cbfbc',
    'VESPERAS.WAD': '14a515f480455a4bd23c8204d9d236c9ba18c147e8c10a364300832ee804fea3',
    'UDTWiD.wad': '523108f0341da424fc390c2a43cb3a9d418f0137298e85b19d12272da4021ec7',

    'MINES.WAD': '4156ed584a667f3d97cd4e3795e0cafa7194404855d9c88826e6e417da9e5d5d',
    'anomaly.wad': 'e0d3efc52add92974cf989c34ce93dbb35149041a1192a2ea169e24922490dad',
    'FARSIDE.WAD': '55e40715b49c201ea035eef00b5ece40243ca217a56b20c1fb7625c7103ac277',
    'MANOR.WAD': 'fe0a502310ef1b32597e2e82d6f7f12ad77cb603ac5838056dee86f4bae31e2f',
    'TTRAP.WAD': '90c7d8fc103e7b02b9602d5eb37fa439da1c5880355e4ee9fa53428ef30dcf45',
    'TROUBLE.WAD': '8f89694bdaeb10709acea88423929bf4ea75cfc8f6d406565151076ccbc365f5',

    'CABALL.WAD': '5ed07c63382124793eb8c2881a4d85da15d430d32265c14d8452930ef3f2c2c4',
    'BLOODSEA.WAD': '1b1acb09f4319db32903dc502d84fc034d21611e375771f4aaac66fafabea39a',
    'BLACKTWR.WAD': 'a0120667412fcf293ea13cdc31c1fa0626d7828f83a195aa09f4170797d07473',
    'MEPHISTO.WAD': '585040c5408bc66583dbe1b8e36d009c81799f7dbebd002af48e4c00088bfbd5',
    'TEETH.WAD': '629e2a6eb1a0234ef0f152384a01130b3d8cd0e44f6c292463dbc2d6ae34d14e',

    'cpu.wad': '9377554a75a18eaa2cd60a8707040efeaa21d136e842b0060d4262972f6b790f',
    'SUBSPACE.WAD': '2c61963efe338abc38b13fb01f238fd95d6b0e2a627ca78db038b9761ff6e6ac',
    'COMBINE.WAD': 'fef0ac1090ba2f0bce92503625047d726c2d8d1964561bd557234e7ab6202dff',
    'device_1.wad': 'f1493e01d7f3fdcda098ebf4c48560fe098b9c56610650b44bd535e0255d7d54',
    'FISTULA.WAD': '864d51febc039b1431c5d75fb051f567433adbddce4bb4d8b6e959fc0b414724',
    'SUBTERRA.WAD': '3dba2abcb85ae3685c259b21bd867d542439c591c12162a36066f1fbab6cbdd8',
    'dmz.wad': '365e62691813d9653d588c65590b889cf0fb16276363c3d5454fbcabbb45eaea',
    'CATWALK.WAD': 'ce1241e16b2e8bb8bbceea84a281e81f865c52670e4eb3649dc7372870985b77',
    'cdk_fury.wad': '1cafc59bd422991c93f9c34830793375c9914cf4ffae88db927867d6871888a8',
    'GARRISON.WAD': '7a7a37d1f31c51ced17167f5283daffef27d79310df0c96b13f4cb1723a2417c',
    'e_inside.wad': 'f5f97aa3f09c97a99f3721aeda32037e55cf4f936f9a74fa8d4c5bcf57ab3eae',
    'hive.wad': '754479211ffcbf240c08c6cdc6c1912f1c2eee3626682d04fe286a8fb55d1d70',

    'TWM01.WAD': '15d81c07374893165971e4ab79af2523729e6acf55688237734f821c771536aa',
    'PARADOX.WAD': '4e9f37b8209dc7006637050876d917e9a68b053ef24e17725432781b00969bdf',
    'ATTACK.WAD': '4b9a404a4ee43ed33f7c2e208269b84b58ccfec5823afa1fe50e3dd08e927622',
    'CANYON.WAD': 'a2dd18d174d25a5d31046114bf73d87e9e13e49e9e6b509b2c9942e77d4c9ecf',
    'kickdm2.wad': '18902e534468304ee505e6c95755592acf6a91a90672152fcaf2f552d0cee786',

    'ultimidi.wad': 'cff289109308dceffb0f2e9361196bda1c35edca7665c5ad604d335ad8d756c5',
    'midtwid2.wad': '54806d8606273cda58db29477fb3fc8be8e40c774f587dda217dab1015e1547b',
}

PATCH_TRIPLETS = [
    ['MSKY1', 'UDTWiD.wad', 'SKY4'],
    ['MSKY2_1', 'MINES.WAD', 'STARS'],
    ['MSKY2_2', 'MINES.WAD', 'STARS1'],
    ['MSKY2_3', 'MINES.WAD', 'STARSAT'],

    ['DRSLEEP', 'UDTWiD.wad', 'DRSLEEP'],
    # ['', 'ACHRON22.WAD', 'SKY1'], <-- unused because MSKY1 is a MUCH better fit for Inferno

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
    ['SW2_3', 'DOOM.WAD', 'SW2_3'],
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
    'REDWALL1',
    'REDWALL2',

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
    ['MAP10', 'SW2COMP', 'TT2COMP'],
    ['MAP10', 'SW1STON1', 'TT1STON1'],
    ['MAP10', 'SW2STON1', 'TT2STON1'],
    ['MAP11', 'SW1STON2', 'TT1STON2'],
    ['MAP11', 'SW2STON2', 'TT2STON2'],
    ['MAP12', 'SW1BRIK', 'TT1BRIK'],
    ['MAP12', 'SW2BRIK', 'TT2BRIK'],
    ['MAP12', 'SW1STON3', 'TT1STON3'],
    ['MAP12', 'SW2STON3', 'TT2STON3'],
    ['MAP12', 'SW1STON4', 'TT1STON4'],
    ['MAP12', 'SW2STON4', 'TT2STON4'],
    ['MAP15', 'SW1VINE', 'TT1VINE'],
    ['MAP15', 'SW2VINE', 'TT2VINE'],
    ['MAP15', 'SW1PIPE', 'TT1PIPE'],
    ['MAP15', 'SW2PIPE', 'TT2PIPE'],
    ['MAP15', 'SW1STON5', 'TT1STON5'],
    ['MAP15', 'SW2STON5', 'TT2STON5'],
    ['MAP15', 'SW1STON6', 'TT1STON6'],
    ['MAP15', 'SW2STON6', 'TT2STON6'],
    ['MAP15', 'SW1STON7', 'TT1STON7'],
    ['MAP15', 'SW2STON7', 'TT2STON7'],
    ['MAP15', 'PIC00', 'PORTAL01'],
    ['MAP15', 'PIC01', 'PORTAL02'],
    ['MAP15', 'PIC06', 'PORTAL03'],
    ['MAP15', 'PIC07', 'PORTAL04'],
    ['MAP15', 'PIC13', 'PORTAL05'],
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


def log(line: str) -> None:
    global logfile

    if not logfile:
        logfile = open(LOG_FILE, 'w')

    print(line)
    logfile.write(line + '\n')


def check_wad(dir: str, wad_name: str) -> str | None:
    for filename in listdir(dir):
        if wad_name.lower() == filename.lower():
            return dir + filename

    return None


#
# Check WAD data
#


def get_wad_pre_hash(wad_name: str) -> str | None:
    if wad_name not in SHA256_DIGEST:
        return None

    return SHA256_DIGEST[wad_name]


def get_wad_hash(wad_path: str) -> str | None:
    sha256hash = sha256()

    file_handler = open(wad_path, 'rb')

    while True:
        data = file_handler.read(BUFFER_SIZE)
        if not data:
            break
        sha256hash.update(data)

    return sha256hash.hexdigest()


def check_all_wads(dir: str):
    found_wads: list[str] = []
    for wad in ALL_WADS:
        if check_wad(dir, wad) == None:
            log(f'  {wad} is missing.')
            break
        if get_wad_hash(dir + wad) != get_wad_pre_hash(wad):
            log(f'  {wad} checksum does not match. Do you have the right version?')
        found_wads.append(wad)

    return found_wads

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


def base_build(dir: str) -> None:
    masterpack = WAD()
    base = WAD(BASE)

    midi1 = WAD(dir + 'ultimidi.wad')
    midi2 = WAD(dir + 'midtwid2.wad')

    log('  Extracting patches...')
    # gotta extract the Klietech sky manually
    # since it is not located between P_* markers
    combine = WAD(DIR_SOURCE + 'COMBINE.WAD')
    sky = combine.data['RSKY1']
    base.patches['MSKY3'] = sky
    log('    MSKY3')

    for triple in PATCH_TRIPLETS:
        wad_name = triple[1]
        wad = WAD(dir + wad_name)

        original_name = triple[2]
        slot = wad.patches[original_name]

        name = triple[0]
        base.patches[name] = slot

        log(f'    {name}')

    log('  Extracting maps...')
    for triple in ALL_MAP_TRIPLETS:
        wad_name = triple[1]
        wad = WAD(dir + wad_name)

        original_slot = triple[2]
        slot = wad.maps[original_slot]

        slot = triple[0]
        base.maps[slot] = slot
        log(f'    Pulled {slot}...')

    log('  Fixing maps...')
    for triplet in SIDEDEF_SWITCH_TRIPLETS:
        slot = triplet[0]
        map_edit = MapEditor(base.maps[slot])

        initial_tex = triplet[1]
        desired_tex = triplet[2]

        massive_simple_sidedef_switch(map_edit, initial_tex, desired_tex)
        base.maps[slot] = map_edit.to_lumps()
        log(f'    Fixing {slot}...')

    log('  Organizing lumps...')
    masterpack.data += base.data
    masterpack.txdefs += base.txdefs
    masterpack.sprites += base.sprites
    masterpack.graphics += base.graphics

    log('    Sorting MIDIs...')
    for midi in DOOM1_MIDI:
        masterpack.music[midi] = midi1.music[midi]

    log('    Sorting MIDIs...')
    for midi in DOOM2_MIDI:
        masterpack.music[midi] = midi2.music[midi]

    log('    Sorting maps...')
    for slot in ALL_MAPS:
        masterpack.maps[slot] = base.maps[slot]

    log('    Sorting patches...')
    for slot in ALL_PATCHES:
        masterpack.patches[slot] = base.patches[slot]

    log('  Creating masterpack.wad...')
    masterpack.to_file(MASTERPACK)


def main() -> None:
    log('Setting up.')

    temp = mkdtemp()
    data = ZipFile('data.zip', 'r')
    data.extractall(temp)

    for file in listdir(DIR_SOURCE):
        origin = path.join(DIR_SOURCE, file)
        dest = path.join(temp, file)
        copy(origin, dest)

    log('Checking wads.')
    found_wads = check_all_wads(temp + '/')

    if sorted(found_wads) != sorted(ALL_WADS):
        log('Error: Did not find all wads.')
        log('Check build.log for more details.')
        log('Build failed. Exiting...')
        exit(1)
    log('Found all WADs!')

    log('Starting to build masterpack.wad.')
    base_build(temp + '/')

    log('Build successful.')
    exit(0)


if __name__ == '__main__':
    main()
