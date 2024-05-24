import os
import sys
import tarfile
import hashlib
import xdelta3

if getattr(sys, 'frozen', False):
    base_path = sys._MEIPASS #type:ignore
else:
    base_path = os.path.abspath('.')

log_file = None
log_path = 'masterpack.log'
file_buffer = 16384
source_dir = 'source/'

checksum = {
    '6fdf361847b46228cfebd9f3af09cd844282ac75f3edbb61ca4cb27103ce2e7f': 'DOOM.WAD',
    'c0a9c29d023af2737953663d0e03177d9b7b7b64146c158dcc2a07f9ec18f353': 'TNT.WAD',

    'c468a1684be8e8055fca52c0c0b3068893481dbaeff0d25f2d72a13b340dff09': 'VIRGIL.WAD',
    'fc3996e52b527dd4d7e76b023eebaa0c18263c94e21115b06ba64c8cda371ec0': 'MINOS.WAD',
    '05a2e5f7e13acfe21895f6ad2ecd216052d8c5c4bcb65b67745678ca0ae3e0dc': 'NESSUS.WAD',
    'ec5c0b1b846764d4b7cc8038e5fac1b1562627d0bcca413a55e918d3141cbfbc': 'GERYON.WAD',
    '14a515f480455a4bd23c8204d9d236c9ba18c147e8c10a364300832ee804fea3': 'VESPERAS.WAD',

    'fe0a502310ef1b32597e2e82d6f7f12ad77cb603ac5838056dee86f4bae31e2f': 'MANOR.WAD',
    '90c7d8fc103e7b02b9602d5eb37fa439da1c5880355e4ee9fa53428ef30dcf45': 'TTRAP.WAD',

    '1b1acb09f4319db32903dc502d84fc034d21611e375771f4aaac66fafabea39a': 'BLOODSEA.WAD',
    'a0120667412fcf293ea13cdc31c1fa0626d7828f83a195aa09f4170797d07473': 'BLACKTWR.WAD',
    '585040c5408bc66583dbe1b8e36d009c81799f7dbebd002af48e4c00088bfbd5': 'MEPHISTO.WAD',
    '629e2a6eb1a0234ef0f152384a01130b3d8cd0e44f6c292463dbc2d6ae34d14e': 'TEETH.WAD',

    '2c61963efe338abc38b13fb01f238fd95d6b0e2a627ca78db038b9761ff6e6ac': 'SUBSPACE.WAD',
    'fef0ac1090ba2f0bce92503625047d726c2d8d1964561bd557234e7ab6202dff': 'COMBINE.WAD',
    '864d51febc039b1431c5d75fb051f567433adbddce4bb4d8b6e959fc0b414724': 'FISTULA.WAD',
    '3dba2abcb85ae3685c259b21bd867d542439c591c12162a36066f1fbab6cbdd8': 'SUBTERRA.WAD',
    'ce1241e16b2e8bb8bbceea84a281e81f865c52670e4eb3649dc7372870985b77': 'CATWALK.WAD',
    '7a7a37d1f31c51ced17167f5283daffef27d79310df0c96b13f4cb1723a2417c': 'GARRISON.WAD',

    '4e9f37b8209dc7006637050876d917e9a68b053ef24e17725432781b00969bdf': 'PARADOX.WAD',
    '4b9a404a4ee43ed33f7c2e208269b84b58ccfec5823afa1fe50e3dd08e927622': 'ATTACK.WAD',
    'a2dd18d174d25a5d31046114bf73d87e9e13e49e9e6b509b2c9942e77d4c9ecf': 'CANYON.WAD',
}

archive_wads = [
    'DOOM.WAD', 'TNT.WAD',
    'VIRGIL.WAD', 'MINOS.WAD', 'NESSUS.WAD', 'GERYON.WAD', 'VESPERAS.WAD',
    'MANOR.WAD', 'TTRAP.WAD',
    'BLOODSEA.WAD', 'BLACKTWR.WAD', 'MEPHISTO.WAD', 'TEETH.WAD',
    'SUBSPACE.WAD', 'COMBINE.WAD', 'FISTULA.WAD', 'SUBTERRA.WAD', 'CATWALK.WAD', 'GARRISON.WAD',
    'PARADOX.WAD', 'ATTACK.WAD', 'CANYON.WAD',
]


def get_wad_hash(wad_path: str):
    sha256hash = hashlib.sha256()

    file_handler = open(wad_path, 'rb')

    while True:
        data = file_handler.read(file_buffer)
        if not data:
            break
        sha256hash.update(data)

    return sha256hash.hexdigest()

def create_wad_archive(tar_path: str, wad_files: list[str]) -> None:
    def reset_tarinfo(tar_info: tarfile.TarInfo):
        tar_info.uid = 0
        tar_info.gid = 0
        tar_info.uname = ''
        tar_info.gname = ''
        tar_info.mtime = 0
        tar_info.mode = 0o644
        return tar_info

    with tarfile.open(tar_path, 'w') as tar:
        for wad_file in sorted(wad_files):
            tar_info = tar.gettarinfo(wad_file)
            tar_info = reset_tarinfo(tar_info)
            with open(wad_file, 'rb') as file_handle:
                tar.addfile(tar_info, file_handle)
    print(f"Created reproducible tar file: {tar_path}")

create_wad_archive('master.tar', archive_wads)
