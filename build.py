#!/usr/bin/env python3

from os import listdir

VERSION = '0.1'

logfile  = None
LOG_FILE = 'masterpack.log'

DIR_DATA   = 'data/'
DIR_SOURCE = 'source_wads/'
DIR_WAD    = 'wad/'
DIR_DEST   = 'build/'

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
	'CATWALK.WAD' ,
	'GARRISON.WAD',
	# Lost Levels
	'PARADOX.WAD',
	'ATTACK.WAD',
	'CANYON.WAD',
]

MASTER_LEVELS_WADS_LUMPS = {
	# Ultimate Doom
	'DOOM.WAD'    : 'doom.txt',
	# Final Doom, TNT: Evilution
	'TNT.WAD'     : 'tnt.txt',
	# Inferno
	'VIRGIL.WAD'  : 'virgil.wad',
	'MINOS.WAD'   : 'minos.txt',
	'NESSUS.WAD'  : 'nessus.txt',
	'GERYON.WAD'  : 'geryon.txt',
	'VESPERAS.WAD': 'vesperas.txt',
	# Titan
	'MANOR.WAD'   : 'manor.txt',
	'TTRAP.WAD'   : 'ttrap.txt',
	# Cabal
	'BLOODSEA.WAD': 'bloodsea.txt',
	'BLACKTWR.WAD': 'blacktwr.txt',
	'MEPHISTO.WAD': 'mephisto.txt',
	'TEETH.WAD'   : 'teeth.txt',
	# Klietech
	'SUBSPACE.WAD': 'subspace.txt',
	'COMBINE.WAD' : 'combine.txt',
	'FISTULA.WAD' : 'fistula.txt',
	'SUBTERRA.WAD': 'subterra.txt',
	'CATWALK.WAD' : 'catwalk.txt',
	'GARRISON.WAD': 'garrison.txt',
	# Lost Levels
	'PARADOX.WAD': 'paradox.wad',
	'ATTACK.WAD' : 'attack.txt',
	'CANYON.WAD' : 'canyon.txt',
}

MASTER_LEVELS_WADS_SHA256SUM = {
	# Ultimate Doom
	'DOOM.WAD'    : '',
	# Final Doom, TNT: Evilution
	'TNT.WAD'     : '',
	# Inferno
	'VIRGIL.WAD'  : '',
	'MINOS.WAD'   : '',
	'NESSUS.WAD'  : '',
	'GERYON.WAD'  : '',
	'VESPERAS.WAD': '',
	# Titan
	'MANOR.WAD'   : '',
	'TTRAP.WAD'   : '',
	# Cabal
	'BLOODSEA.WAD': '',
	'BLACKTWR.WAD': '',
	'MEPHISTO.WAD': '',
	'TEETH.WAD'   : '',
	# Klietech
	'SUBSPACE.WAD': '',
	'COMBINE.WAD' : '',
	'FISTULA.WAD' : '',
	'SUBTERRA.WAD': '',
	'CATWALK.WAD' : '',
	'GARRISON.WAD': '',
	# Lost Levels
	'PARADOX.WAD': '',
	'ATTACK.WAD' : '',
	'CANYON.WAD' : '',
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
