# Masterpack for Doom II

![Master Levels](./misc/masterpack.jpg "Master Levels")

The 'Master Levels for Doom II' were by far the lowest quality official release by id Software in it's classic days.

In short, it is a grabbag collection of various unstructured, unorganized WAD files, all made by various map authors with a wide variety of styles and design conventions.

Most of the authors involved in the project, made these maps with the intention of them being a part of larger episode overarching a certain theme, with John Anderson, for example, directing a series of 9 total levels themed around the first third of Dante Alighieri's Divine Comedy, Inferno.

However, most of these authors would go on, after the release of the Master Levels release later, freely available WADs which continued or preceeded the former levels in continuity or level design, many of which were originally piched to id Software for inclusion in the original release.

With all this in mind, why should anyone play the official in their original amorphous format? Why should we accept the way things are? Why should we allow people to miss out on the great works of these authors just because the pieces are all over the place?

This script fixes that, all content by the authors past, present and future to the Master Levels is now brought together in a single WAD file for your enjoyment. All 45 relevant (plus 1 bonus) map are now fully playable as 5 separate, organized episodes. And with this, you can now properly enjoy the works of Doom's early great authors, some of early Doom's most timeless work.

Here are the included episodes (and for a detailed list check out this [table](./misc/full_maps.csv)):
```txt
Inferno     -  9 maps - John "Dr. Sleep" Anderson, Rest In Peace
Titan       -  6 maps - James "Jim" Flynn, Rest In Peace
Cabal       - 12 maps - Sverre "Soundblock" Kvernmo
Klietech    - 12 maps - Christen Klie
Lost Levels -  7 maps - Tom "Paradox" Mustaine, Theresa Chasar, and Tim Willits
```

Note: The last map by "Dr. Sleep" in his Inferno series, "Lethe" or "Waters of Lethe", is long known to be the Doom community's most important piece of "lost media", having no more proof than the author's own words and a single screenshot of the map to show for it's existence. In this mapset, it is substituted by "[An End to Darkness](https://doomwiki.org/wiki/E4M8:_An_End_to_Darkness_(Ultimate_Doom_the_Way_id_Did))" by [Xaser Acheron](https://doomwiki.org/wiki/Xaser) from the communinty project "[Utimate Doom The Way id Did](https://doomwiki.org/wiki/Ultimate_Doom_the_Way_id_Did)".

# Instructions

In order to use this script correctly you will the following, from your Steam installation of Ultimate Doom and Doom II (keeping in mind, these are the original DOS version of the IWADs and PWADs, the Unity ones will not work):

- Ultimate Doom, `DOOM.WAD`
- Doom II: Hell on Earth, `DOOM2.WAD`
- TNT: Evilution, `TNT.WAD`
- All 20 of the Master Levels for Doom II:
	- Inferno
		- `VIRGIL.WAD`
		- `MINOS.WAD`
		- `NESSUS.WAD`
		- `GERYON.WAD`
		- `VESPERAS.WAD`
	- Titan
		- `MANOR.WAD`
		- `TTRAP.WAD`
	- Cabal
		- `BLODDSEA.WAD`
		- `BLACKTWR.WAD`
		- `MEPHISTO.WAD`
		- `TEETH.WAD`
	- Klietech
		- `SUBSPACE.WAD`
		- `COMBINE.WAD`
		- `FISTULA.WAD`
		- `SUBTERRA.WAD`
		- `CATWALK.WAD`
		- `GARRISON.WAD`
	- Lost Levels
		- `PARADOX.WAD`
		- `ATTACK.WAD`
		- `CANYON.WAD`

To find these files, starting on your Steam library, check out [this](./misc/STEAM.md) tutorial.

Once you have all the WAD files, drop them in the `source/` directory and run the script as the following:

```bash
$ python3 masterpack.py
```

It will generate a `masterpack.log` file containing the output of the script, if it was successful or not.

And, if nothing went wrong, you will now be the proud owner of your own copy of `masterpack.wad`.

To play this, run it with a modern Doom source port, with xMAPINFO support, such as DSDA-Doom, Woof!, Eternity or the ZDoom family.

```bash
# With DSDA
$ dsda-doom -file masterpack.wad -complevel 1.9

# Or Woof!
$ woof -file masterpack.wad -complevel vanilla

# Or even ZDoom-family ports
$ zdoom -file masterpack.wad
$ gzdoom -file masterpack.wad
```

# Legalese

Project: `Master Level Masterpack`  
Files: `*`  
Copyright: © 2024 Guilherme Marques Miranda  

Project: `WadSmoosh`  
Files: `src/masterpack.py`  
Copyright: © 2018 Jean-Paul LeBreton  

Project: `Works of the Masters`  
Files: `src/base.wad`  
Copyright: © 2020 Jean-Paul LeBreton  

Project: `Omgifol`  
Files: `src/omg/*`  
Copyright: © 2005 Fredrik Johansson, 2017 Devin Acker  
