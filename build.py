#!/usr/bin/env python3

from os import listdir

VERSION = '0.1'

logfile = None
LOG_FILE = 'masterpack.log'

DIR_DATA = 'data/'
DIR_SOURCE = 'source_wads/'
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
	'CATWALK.WAD' ,
	'GARRISON.WAD',
	# Lost Levels
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
	'ATTACK.WAD': 'attack.txt',
	'CANYON.WAD': 'canyon.txt',
}

def log(line: str):
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

def get_report_found():
	found_wads = []
	for wadname in MASTER_LEVELS_WADS:
		if get_wad_filename(wadname):
			found_wads.append(wadname)
	return found_wads

def main() -> None :
	raise NotImplementedError(
	"""
	>:(
	Not implemented yet.
	Get to writing, lazy ass."""
	)

if __name__ == '__main__':
	main()
