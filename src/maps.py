#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
# SPDX-FileCopyrightText: Copyright 2024 Guilherme M. Miranda <alchemist.software@proton.me>

import os
import hashlib
import omg

log_file = None
log_path = 'masterpack.log'
buffer_size = 16384
source_dir = 'source/'

all_wads = [
    'DOOM.WAD', 'TNT.WAD',
    'DANTE25.WAD', 'ACHRON22.WAD', 'VIRGIL.WAD', 'MINOS.WAD', 'NESSUS.WAD', 'GERYON.WAD', 'VESPERAS.WAD', 'UDTWiD.wad',
    'MINES.WAD', 'anomaly.wad', 'FARSIDE.WAD', 'MANOR.WAD', 'TTRAP.WAD', 'TROUBLE.WAD',
    'CABALL.WAD', 'BLOODSEA.WAD', 'BLACKTWR.WAD', 'MEPHISTO.WAD', 'TEETH.WAD',
    'cpu.wad', 'SUBSPACE.WAD', 'COMBINE.WAD', 'device_1.wad', 'FISTULA.WAD', 'SUBTERRA.WAD', 'dmz.wad', 'CATWALK.WAD', 'cdk_fury.wad', 'GARRISON.WAD', 'e_inside.wad', 'hive.wad',
    'TWM01.WAD', 'PARADOX.WAD', 'ATTACK.WAD', 'CANYON.WAD', 'kickdm2.wad',
]

checksum = {
    '6fdf361847b46228cfebd9f3af09cd844282ac75f3edbb61ca4cb27103ce2e7f': 'DOOM.WAD',
    'c0a9c29d023af2737953663d0e03177d9b7b7b64146c158dcc2a07f9ec18f353': 'TNT.WAD',

    '8ac0ce535c75027f46a8909ad6fa7c173ba1457a76167a05ac2213d5606cf902': 'DANTE25.WAD',
    '9c285f5b14b5a26a5e46e0c5566a1fbfc94a170a9d0d6c2dee19069b3e4d5423': 'ACHRON22.WAD',
    'c468a1684be8e8055fca52c0c0b3068893481dbaeff0d25f2d72a13b340dff09': 'VIRGIL.WAD',
    'fc3996e52b527dd4d7e76b023eebaa0c18263c94e21115b06ba64c8cda371ec0': 'MINOS.WAD',
    '05a2e5f7e13acfe21895f6ad2ecd216052d8c5c4bcb65b67745678ca0ae3e0dc': 'NESSUS.WAD',
    'ec5c0b1b846764d4b7cc8038e5fac1b1562627d0bcca413a55e918d3141cbfbc': 'GERYON.WAD',
    '14a515f480455a4bd23c8204d9d236c9ba18c147e8c10a364300832ee804fea3': 'VESPERAS.WAD',
    '523108f0341da424fc390c2a43cb3a9d418f0137298e85b19d12272da4021ec7': 'UDTWiD.wad',

    '4156ed584a667f3d97cd4e3795e0cafa7194404855d9c88826e6e417da9e5d5d': 'MINES.WAD',
    'e0d3efc52add92974cf989c34ce93dbb35149041a1192a2ea169e24922490dad': 'anomaly.wad',
    '55e40715b49c201ea035eef00b5ece40243ca217a56b20c1fb7625c7103ac277': 'FARSIDE.WAD',
    'fe0a502310ef1b32597e2e82d6f7f12ad77cb603ac5838056dee86f4bae31e2f': 'MANOR.WAD',
    '90c7d8fc103e7b02b9602d5eb37fa439da1c5880355e4ee9fa53428ef30dcf45': 'TTRAP.WAD',
    '8f89694bdaeb10709acea88423929bf4ea75cfc8f6d406565151076ccbc365f5': 'TROUBLE.WAD',

    '5ed07c63382124793eb8c2881a4d85da15d430d32265c14d8452930ef3f2c2c4': 'CABALL.WAD',
    '1b1acb09f4319db32903dc502d84fc034d21611e375771f4aaac66fafabea39a': 'BLOODSEA.WAD',
    'a0120667412fcf293ea13cdc31c1fa0626d7828f83a195aa09f4170797d07473': 'BLACKTWR.WAD',
    '585040c5408bc66583dbe1b8e36d009c81799f7dbebd002af48e4c00088bfbd5': 'MEPHISTO.WAD',
    '629e2a6eb1a0234ef0f152384a01130b3d8cd0e44f6c292463dbc2d6ae34d14e': 'TEETH.WAD',

    '9377554a75a18eaa2cd60a8707040efeaa21d136e842b0060d4262972f6b790f': 'cpu.wad',
    '2c61963efe338abc38b13fb01f238fd95d6b0e2a627ca78db038b9761ff6e6ac': 'SUBSPACE.WAD',
    'fef0ac1090ba2f0bce92503625047d726c2d8d1964561bd557234e7ab6202dff': 'COMBINE.WAD',
    'f1493e01d7f3fdcda098ebf4c48560fe098b9c56610650b44bd535e0255d7d54': 'device_1.wad',
    '864d51febc039b1431c5d75fb051f567433adbddce4bb4d8b6e959fc0b414724': 'FISTULA.WAD',
    '3dba2abcb85ae3685c259b21bd867d542439c591c12162a36066f1fbab6cbdd8': 'SUBTERRA.WAD',
    '365e62691813d9653d588c65590b889cf0fb16276363c3d5454fbcabbb45eaea': 'dmz.wad',
    'ce1241e16b2e8bb8bbceea84a281e81f865c52670e4eb3649dc7372870985b77': 'CATWALK.WAD',
    '1cafc59bd422991c93f9c34830793375c9914cf4ffae88db927867d6871888a8': 'cdk_fury.wad',
    '7a7a37d1f31c51ced17167f5283daffef27d79310df0c96b13f4cb1723a2417c': 'GARRISON.WAD',
    'f5f97aa3f09c97a99f3721aeda32037e55cf4f936f9a74fa8d4c5bcf57ab3eae': 'e_inside.wad',
    '754479211ffcbf240c08c6cdc6c1912f1c2eee3626682d04fe286a8fb55d1d70': 'hive.wad',

    '15d81c07374893165971e4ab79af2523729e6acf55688237734f821c771536aa': 'TWM01.WAD',
    '4e9f37b8209dc7006637050876d917e9a68b053ef24e17725432781b00969bdf': 'PARADOX.WAD',
    '4b9a404a4ee43ed33f7c2e208269b84b58ccfec5823afa1fe50e3dd08e927622': 'ATTACK.WAD',
    'a2dd18d174d25a5d31046114bf73d87e9e13e49e9e6b509b2c9942e77d4c9ecf': 'CANYON.WAD',
    '18902e534468304ee505e6c95755592acf6a91a90672152fcaf2f552d0cee786': 'kickdm2.wad',
}

sidedef_switch_triplet = [
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

all_map_triplets = [
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

all_maps = [
    'MAP01', 'MAP02', 'MAP03', 'MAP04', 'MAP05', 'MAP06', 'MAP07', 'MAP08', 'MAP09',
    'MAP10', 'MAP11', 'MAP12', 'MAP13', 'MAP14', 'MAP15',
    'MAP16', 'MAP17', 'MAP18', 'MAP19', 'MAP20', 'MAP21', 'MAP22', 'MAP23', 'MAP24', 'MAP25', 'MAP26', 'MAP27',
    'MAP28', 'MAP29', 'MAP30', 'MAP31', 'MAP32', 'MAP33', 'MAP34', 'MAP35', 'MAP36', 'MAP37', 'MAP38', 'MAP39',
    'MAP40', 'MAP41', 'MAP42', 'MAP43', 'MAP44', 'MAP45', 'MAP46',
]

def log(line: str) -> None:
    global log_file
    if not log_file:
        log_file = open(log_path, 'w')
    print(line)
    log_file.write(line + '\n')

def get_hash_digest(wad_path: str) -> str:
    hash_sha256: hashlib._Hash = hashlib.sha256()
    with open(wad_path, 'rb') as file_handler:
        while True:
            data = file_handler.read(buffer_size)
            if not data:
                break
            hash_sha256.update(data)
    return hash_sha256.hexdigest()

def validate_hash_digest(wad_hash: str) -> str | None:
    hash_result = checksum.get(wad_hash, None)
    return hash_result

def validate_wads() -> bool:
    wads_match = True
    for wad in all_wads:
        wad_path = os.path.join(source_dir + wad)
        hash_digest = get_hash_digest(wad_path)
        wad_name = validate_hash_digest(hash_digest)
        if wad_name != wad:
            log(f'  {wad} does not match checksum')
            wads_match = False
    return wads_match

def massive_simple_sidedef_switch(map: omg.MapEditor, initial_tx: str, desired_tx: str):
    for sidedef in map.sidedefs:
        if sidedef.tx_up == initial_tx:
            sidedef.tx_up = desired_tx
        if sidedef.tx_mid == initial_tx:
            sidedef.tx_mid = desired_tx
        if sidedef.tx_low == initial_tx:
            sidedef.tx_low = desired_tx

def maps_build():
    masterpack = omg.WAD()
    base = omg.WAD()

    log('  Extracting maps')
    for triple in all_map_triplets:
        wad_name = triple[1]
        wad = omg.WAD(wad_name)

        original_slot = triple[2]
        map = wad.maps[original_slot] #type:ignore

        slot = triple[0]
        base.maps[slot] = map #type:ignore
        log(f'    Pulling {slot}')

    log('  Fixing maps')
    for triplet in sidedef_switch_triplet:
        slot = triplet[0]
        map_edit = omg.MapEditor(base.maps[slot]) #type:ignore

        initial_tex = triplet[1]
        desired_tex = triplet[2]

        massive_simple_sidedef_switch(map_edit, initial_tex, desired_tex)
        base.maps[slot] = map_edit.to_lumps() #type:ignore
        log(f'    Fixing {slot}')

    log('    Sorting maps')
    for slot in all_maps:
        masterpack.maps[slot] = base.maps[slot] #type:ignore

    masterpack.to_file('masterpack-maps.wad')
