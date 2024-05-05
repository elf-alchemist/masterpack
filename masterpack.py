#!/usr/bin/env python3

from os import listdir

VERSION = '0.1'

logfile = None
LOG_FILE = 'masterpack.log'

DIR_DATA = 'data/'
DIR_SOURCE = 'source_wads/'
DIR_WAD = 'wad/'
DIR_DEST = 'build/'

MASTER_LEVELS_WADS = [
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

MASTER_LEVELS_WADS_LUMPS = {
    # Ultimate Doom
    'DOOM.WAD': 'doom.txt',
    # Final Doom, TNT: Evilution
    'TNT.WAD': 'tnt.txt',
    # Inferno
    'VIRGIL.WAD': 'virgil.wad',
    'MINOS.WAD': 'minos.txt',
    'NESSUS.WAD': 'nessus.txt',
    'GERYON.WAD': 'geryon.txt',
    'VESPERAS.WAD': 'vesperas.txt',
    # Titan
    'MANOR.WAD': 'manor.txt',
    'TTRAP.WAD': 'ttrap.txt',
    # Cabal
    'BLOODSEA.WAD': 'bloodsea.txt',
    'BLACKTWR.WAD': 'blacktwr.txt',
    'MEPHISTO.WAD': 'mephisto.txt',
    'TEETH.WAD': 'teeth.txt',
    # Klietech
    'SUBSPACE.WAD': 'subspace.txt',
    'COMBINE.WAD': 'combine.txt',
    'FISTULA.WAD': 'fistula.txt',
    'SUBTERRA.WAD': 'subterra.txt',
    'CATWALK.WAD': 'catwalk.txt',
    'GARRISON.WAD': 'garrison.txt',
    # Lost Levels
    'PARADOX.WAD': 'paradox.wad',
    'ATTACK.WAD': 'attack.txt',
    'CANYON.WAD': 'canyon.txt',
}

MASTER_LEVELS_WADS_SHA256_CHECK_SUM = {
    # Ultimate Doom
    'DOOM.WAD': '6fdf361847b46228cfebd9f3af09cd844282ac75f3edbb61ca4cb27103ce2e7f',
    # Final Doom, TNT: Evilution
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


def log(line: str) -> None:
    global logfile
    if not logfile:
        logfile = open(LOG_FILE, 'w')
    print(line)
    logfile.write(line + '\n')


def get_wad_filename(wad_name: str):
    wad_name += '.wad'
    for filename in listdir(DIR_SOURCE):
        if wad_name.lower() == filename.lower():
            return DIR_SOURCE + filename
    return None


def get_report_found() -> list[str]:
    found_wads: list[str] = []
    for wadname in MASTER_LEVELS_WADS:
        if get_wad_filename(wadname):
            found_wads.append(wadname)
    return found_wads


def main() -> None:
    raise NotImplementedError(
        """
	>:(
	Not implemented yet.
	Get to writing, lazy ass."""
    )


if __name__ == '__main__':
    main()
