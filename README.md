# Masterpack for Doom II

![Master Levels](./misc/masterpack.jpg "Master Levels")

The 'Master Levels for Doom II' were by far the lowest quality official release by id Software in it's classic days.

In short, it is a grab-bag collection of various unstructured, unorganized WAD files, all made by various map authors with a wide variety of styles and design conventions.

Most of the authors involved in the project, made these maps with the intention of them being a part of larger episode or campaign overarching a certain theme even before being contacted by id Software for this project of theirs. John W. Anderson, for example, directing a series of 9 total levels themed around the first third of Dante Alighieri's Divine Comedy, Inferno.

However, not all maps made by these authors were accepted by id Software, being later released freely by their creators after the fact, with some of them even continuing their work further, beyond the original submitted level sets.

With all this in mind, why should anyone play the works of these masters in their original amorphous format? Why should we accept the way things are? Why should we allow people to miss out on the great works of these authors just because the pieces are all over the place? Why should we be holden by the shackles of someone else's bad decisions? Why are we not allowed to have fun with some of the best level designers of 1995?

This script fixes that and much more, by taking everything made by the authors past, present and future to the original Master Levels release and bringing it together in a single WAD file for your enjoyment. All 45 relevant (plus 1 bonus) map are now fully playable as 5 separate, organized episodes. And with this, you can now properly enjoy the works of Doom's early great authors, some of early Doom's most timeless work.

Here are the included episodes (and for a detailed list check out this [table](./misc/full_maps.csv)):
```txt
  Inferno     -  9 maps - John "Dr. Sleep" Anderson, Rest In Peace
  Titan       -  6 maps - James "Jim" Flynn, Rest In Peace
  Cabal       - 12 maps - Sverre "Soundblock" Kvernmo
  Klietech    - 12 maps - Christen Klie
  Lost Levels -  7 maps - Tom "Paradox" Mustaine, Theresa Chasar, and Tim Willits
```

Note about Waters of Lethe: The last Canto of the Inferno series, is long known to be the Doom community's [most important piece of lost media](https://www.doomworld.com/forum/topic/128173-known-lost-wads-of-our-history/), having no more proof than the author's own words and a single screenshot of the map to show for it's existence. In this map set, it is substituted by "[An End to Darkness](https://doomwiki.org/wiki/E4M8:_An_End_to_Darkness_(Ultimate_Doom_the_Way_id_Did))", by [Xaser Acheron](https://doomwiki.org/wiki/Xaser), an homage to [Dr. Sleep](https://doomwiki.org/wiki/John_Anderson_(Dr._Sleep)), inspired by the only know screenshot of Lethe.

Note about Kick Attack: The only map to not have anything to do with the original Master Levels project is Boot Assault, a  version of [Kick Attack!](https://doomwiki.org/wiki/Kick_Attack!) for Doom II stripped of it's custom graphics. Coming from the commercial collaboration between RC Cola and id Software, organized and led by Tim Willits and released in early 1996, shortly after the release of the Master Levels, it is attached here by level design similarity, in order to round off the end of the "Lost Levels" episodes.

# Inspiration

The infamy of the Master Levels in well known and understood in the Classic Doom community. As many have criticized the level design of some of the maps, the repetitive lack of proper music choice for many maps, amongst other issues plaguing the official release.

Many have attempted to improve upon this botched release, from [Peter "Megasphere" Lawrence](https://doomwiki.org/wiki/Peter_Lawrence_(MegaSphere)), who created the [Master Levels 25th Anniversary MIDI Pack](https://doomwiki.org/wiki/Master_Levels_for_Doom_II_25th_Anniversary_MIDI_Pack) made specifically for each map in the the set, or [Devalaous](https://www.doomworld.com/profile/8995-devalaous/), who created a [QoL patch](https://www.doomworld.com/forum/topic/119465-the-master-levels-upgradeqol-pack-updatedfixed-27224/) to be used on top of PSN Doom's `masterlevels.wad`. But, by far, the most important improvement made to this highly underrated map set was made by [JP LeBreton](https://doomwiki.org/wiki/Jean-Paul_LeBreton), when he released the [Works of the Masters](https://jp.itch.io/deluxe-master-levels), a PWAD for his [WadSmoosh](https://jp.itch.io/wadsmoosh) utility, a complete set of maps returning all of the missing maps by the involved authors.

WotM is a fundamentally game changing mod for the Master Levels, by reattaching all of the missing maps, most of which remain less known even in the core Doom community cultural sphere. Merging together all of the levels in their originally intended complete form, WotM not only refreshes the Master Levels, not only does it give them new life, it shines their glory brightly, allowing them to be taken a serious piece of Doom mapping work.

By simply giving the maps an episodic structure, as they were all supposed to have, JP completely fixed the fundamental issues with these WADs, by letting anyone to play these levels as one single package, he allowed me and many other players to enjoy the work of Doom's early great authors. By questioning the way we are supposed to play the Master Levels, they were completely reinvented, given new purpose, shown what they could be something great.

However, for how great WS and WotM are, they remain exclusive to the popular [GZDoom](https://doomwiki.org/wiki/GZDoom), severely limiting it to the community members that do not use the highly advanced source port. In the wake of my parting with GZDoom, to me using Woof! as my preferred source port, I set out to rebuild this superb "deluxe version" of the Master Levels, into something more palatable for the rest of the Classic Doom audience.

I started out using [SLADE3](https://slade.mancubus.net/) to extract the content of LeBreton's masters.pk3 into the more vanilla-friendly formats, using a plain WAD file (instead of GZDoom's pk3 format), the "TEXTURE1" and "SWITCHES" lumps (as opposed to TEXTURES and ANIMDEFS), etc. But soon, I came to a realization that my work could've fallen in vain, as a commercial release can not be redistributed, I came to thought of imitating @JPL once more, and needed a build script utility of my own. And that is when I decided to start making the Masterpack for Doom II, so everyone, and everyone, can enjoy the Master Levels the way they were meant to, the way the authors had intended, or at least as close to the best of the best as we can get.

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
		- `BLOODSEA.WAD`
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

# Or Odamex
$ odamex -file masterpack.wad

# Or even ZDoom-family ports
$ zdoom -file masterpack.wad
$ qzdoom -file masterpack.wad
$ lzdoom -file masterpack.wad
$ gzdoom -file masterpack.wad
$ zandronum -file masterpack.wad
```

# Legalese

Master Level Masterpack  
Copyright © 2024 Guilherme Marques Miranda  

WideHud  
Copyright © 2013 NightFright  

WidePix  
Copyright © 2020 Nash Muhandes  

WadSmoosh  
Copyright © 2018 Jean-Paul LeBreton  

Works of the Masters  
Copyright © 2020 Jean-Paul LeBreton  

Omgifol  
Copyright © 2005 Fredrik Johansson, 2017 Devin Acker  

Doom, Doom II and Master Levels for Doom II
Copyright © 1993, 1994, 1995 id Software
