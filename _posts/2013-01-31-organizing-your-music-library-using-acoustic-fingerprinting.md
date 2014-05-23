---
title: Organizing Your Music Library Using Acoustic Fingerprinting
author: Karim Elatov
layout: post
permalink: /2013/01/organizing-your-music-library-using-acoustic-fingerprinting/
dsq_thread_id:
  - 1406365792
categories:
  - Home Lab
  - OS
tags:
  - acoustic fingerprinting
  - acoustid
  - beets
  - character set
  - chromaprint
  - cyrillic
  - EasyTag
  - echoprint
  - echoprint-codegen
  - exiftool
  - id3-tags
  - id3v1
  - id3v2
  - lastfm
  - lastfm-fpclientG
  - lastmatch.py
  - MusicBrainz
  - picard
  - pylastfp
  - python
  - romanization
  - songbird
  - subsonic
  - tag2utf.py
  - transliterate
---
I wrote a [Now, That's What I Call Music](http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/)" CDs in the US).

I used to have an *iPod* and I used to use *Songbird* as my music player and this ended up messing up my file names and even the *id3* tags of the audio files. For example here is a sample folder with my songs:

	[elatov@moxz mus_2003]$ ls -1
	Àëñó-Â÷åðà.mp3
	??-??.mp3
	Газманов_Олег-На_заре.mp3


The first one is not even in Russian (or rather it's not displaying in the Cyrillic alphabet), it's looks like the encoding is all messed up. The second one is a bunch of question marks, so the conversion was messed up at some point. And the last one is actually in Russian.

My goal was to rename all the files to the following format: **ARTIST-TITLE.EXT**. I wasn't worried about *id3* tags, just the file names for now. I also wanted the filenames to be in English so I could search the title without the need to change my character set. So I wanted to "transliterate" the file names from Russian/Cyrillic to English/Roman. The process is also called "Romanization" or as I have mentioned, transliteration. If you want more information about Romanization/Transliteration, check out [this](http://en.wikipedia.org/wiki/Romanization_of_Russian) wikipedia page.

For example *hello* in Russian is *привет*, the transliteration of that would be: *privet* (hopefully that makes sense).

At first I ran across an article entitled "[Auto-tagging MP3s](http://superuser.com/questions/95425/auto-tagging-mp3s)". It has a list of application that do auto tagging by querying the *id3* tags of the file and then showing the correct artist or title name (some even do a search against an online database). Some of the applications listed in that page are:

- <a style="line-height: 22px; font-size: 13px;" href="http://musicbrainz.org/doc/MusicBrainz_Picard">picard</a>
- <a style="line-height: 22px; font-size: 13px;" href="http://projects.gnome.org/easytag/">EasyTAG</a>
- <a style="line-height: 22px; font-size: 13px;" href="http://beets.radbox.org/">beets</a>
- <a style="line-height: 22px; font-size: 13px;" href="http://www.jthink.net/jaikoz/">Jaikoz</a>

I tried some of the applications, but they couldn't find any information on my songs. Here is a screenshot of  *picard* for my 3 songs:

![picard no match g Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/picard_no_match_g.png)

Notice at the bottom it says "No Matching Tracks above the threshold for file". I tried enabling Fingerprinting:

![picard finger printing enabled Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/picard_finger_printing_enabled.png)

I also enabled the *lastfm* plugin:

![picard lastfm plugin Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/picard_lastfm_plugin.png)

But neither of those options/plugins were able to identify my songs, I tried the other utilities but it was to no avail. It looks like *musicbrainz* or similar databases are album centric. From the [picard](http://musicbrainz.org/doc/MusicBrainz_Picard) home page:

> When tagging files, Picard uses an album-oriented approach. This approach allows it to utilize the MusicBrainz data as effectively as possible and correctly tag your music.

But remember I wasn't trying to tag albums, but rather single tracks. I then tried out **beets**, I even enabled the *chroma*/*Acoustid* plugin to enable acoustic fingerprinting, but it was the same thing. Check it out:

	[elatov@moxz mus]$ grep plugin ~/.beetsconfig
	plugins: chroma

Now for *beets*:

	[elatov@moxz mus]$ beet import mus_2003
	/mnt/data/mus_2003
	No matching release found for 3 tracks.
	For help, see: https://github.com/sampsyo/beets/wiki/FAQ#wiki-nomatch
	[U]se as-is, as Tracks, Skip, Enter search, enter Id, aBort?

but it was the same thing, it couldn't match anything. However beets is also album oriented, from the [beets](https://beets.readthedocs.org/en/stable/guides/tagger.html) page:

> Your music should be organized by album into directories. That is, the tagger assumes that each album is in a single directory. These directories can be arbitrarily deep (like music/2010/hiphop/seattle/freshespresso/glamour), but any directory with music files in it is interpreted as a separate album. This means that your flat directory of six thousand uncategorized MP3s won’t currently be autotaggable. (This will change eventually.)

If the acoustic fingerprinting would've worked, it would have been sweet (*beets* looks really cool). After I fix all my file names and tags, I might use *beets* to manage my library just cause it looks so cool and flexible.

I then ran into [here](https://github.com/echonest/echoprint-codegen#codegen-for-echoprint). From the **ReadMe**, here are the requirements:

> Requirements for libcodegen
>
> - Boost >= 1.35
> - zlib
>
> Additional requirements for the codegen binary
>
> - [TagLib](http://developer.kde.org/~wheeler/taglib.html)
> - ffmpeg - this is called via shell and is not linked into codegen

Here is an example from their site on how to compile the application, once you have all the prerequisites setup:

	~$ git clone -b release-4.12 git://github.com/echonest/echoprint-codegen.git
	Cloning into 'echoprint-codegen'...
	remote: Counting objects: 665, done.
	remote: Compressing objects: 100% (280/280), done.
	remote: Total 665 (delta 428), reused 612 (delta 376)
	Receiving objects: 100% (665/665), 1.40 MiB | 578 KiB/s, done.
	Resolving deltas: 100% (428/428), done.
	~$ cd echoprint-codegen/
	~/echoprint-codegen$ cd src/
	~/echoprint-codegen/src$ vi Makefile # edit BOOST_CFLAGS and other variables as necessary
	~/echoprint-codegen/src$ make

I was able to compile the source, and then trying to query one of the songs, I saw the following:

	[elatov@moxz mus_2003]$ ~/downloads/echoprint-codegen-release-4.12/echoprint-codegen \?\?-\?\?.mp3 10 30
	{"metadata":{"artist":"A. Russo & K. Agati ", "release":"", "title":"Mechti Zbilis'", "genre":"Other",
	"bitrate":128,"sample_rate":44100, "duration":184, "filename":"??-??.mp3", "samples_decoded":330902, "given_duration":30, "start_offset":10, "version":4.12, "codegen_time":0.666698, "decode_time":5.102925}, "code_count":798, "code":"eJztWG2SLSkK3ZIoo", "tag":0}

That actually looked okay. For testing reasons, I wanted to write a python script to basically try to acoustically fingerprint every file in a directory. I haven't done python in a while, so I just went with it. I actually decided to parse the output of the above command and then rename the file accordingly. Hindsight, I should have used a python API provided for *echoprint*, but I was too anxious and I just went for it. Here is how my python script looked like:

	#!/bin/env python
	coding: UTF-8 -*-
	import os,sys,json,subprocess,re

	rootdir = sys.argv[1]

	def translit(cyr_str):

	capital_letters = { u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D', u'Е': u'E', u'Ё': u'E', u'Ж': u'j', u'З': u'Z', u'И': u'I', u'Й': u'Y', u' К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O', u'П': u'P', u'Р': u'R ', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F', u'Х': u'H', u'Ц': u'Ts', u'Ч ': u'Ch', u'Ш': u'Sh', u'Щ': u'Sch', u'Ъ': u'y', u'Ы': u'Y', u'Ь': u'i', u'Э': u'E', u'Ю': u'Yu', u'Я': u'Ya' }

	lower_case_letters = { u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'j', u'з': u'z', u'и': u'i', u'й': u'y', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o', u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'y', u'ы': u'y', u'ь': u'i', u'э': u'e', u'ю': u'yu', u'я': u'ya' }

	translit_string = ""

	for index, char in enumerate(cyr_str):
	if char in lower_case_letters.keys():
	char = lower_case_letters[char]
	elif char in capital_letters.keys():
	char = capital_letters[char]
	if len(cyr_str) > index+1:
	if cyr_str[index+1] not in lower_case_letters.keys():
	char = char.upper()
	else:
	char = char.upper()
	translit_string += char

	return translit_string

	def get_finger_print(audio_file):
	results = subprocess.Popen(['/home/elatov/downloads/echoprint-codegen-release-4.12/echoprint-codegen',audio_file,'10','40'],stdout=subprocess.PIPE)
	r=results.communicate()[0]
	data=json.loads(r)
	if data[0].has_key('error'):
	print data[0]['error']
	song_title=("failed")
	song_artist=("failed")
	else:
	song_title=data[0]['metadata']['title']
	song_artist=data[0]['metadata']['artist']

	if isinstance(song_artist,unicode):
	song_artist = translit(data[0]['metadata']['artist'])
	if isinstance(song_title,unicode):
	song_title = translit(data[0]['metadata']['title'])

	return song_title,song_artist

	def clean_up_names(string):
	string=(re.sub("['\"]", "", string))
	string=(re.sub("[^\w]+", "_", string))
	string=(re.sub("[_]+", "_", string))
	if string.endswith('_'):
	string=string[:-1]
	if string.startswith('_'):
	string=string[1:]
	string=string.title()

	return string

	for path, subdirs, files in os.walk(rootdir):
	for name in files:
	print os.path.join(path,name)
	(s_title,s_artist)=get_finger_print(os.path.join(path, name))
	s_title_c=clean_up_names(s_title)
	s_artist_c=clean_up_names(s_artist)
	if (s_title_c != 'Failed') and (s_artist_c != 'Failed'):
	ext=os.path.splitext(name)[1].lower()
	filename="%s-%s%s" % (s_artist_c,s_title_c,ext)
	src=os.path.join(path,name)
	dst=os.path.join(path,filename)
	if str(dst) != src:
	print ("Renaming from " + src + " to " + str(dst))
	os.rename(src,dst)


There are not a lot of checks in the script, and I am sure there are a lot of things wrong with the script. Bear in mind this is probably the 3rd python script I ever wrote in my life, so please don't judge :) It doesn't even check if the folder, that you passed to it, exists. I can't stress enough that this is a poorly written script :)

To make things worse, I even "borrowed" the 'translit' function from [here](http://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic).

Anyways I created a backup of my playlist and then tried to fix the file names. Here is backup:

	[elatov@moxz mus]$ rsync -avzP mus_2003/. mus_2003.bak

Now to run the script on the playlist:

	[elatov@moxz mus]$ ./af_ep.py mus_2003
	mus_2003/Газманов_Олег-На_заре.mp3
	Renaming from mus_2003/Газманов_Олег-На_заре.mp3 to mus_2003/Gazmanov_Oleg-Na_Zare.mp3
	mus_2003/Àëñó-Â÷åðà.mp3
	Renaming from mus_2003/Àëñó-Â÷åðà.mp3 to mus_2003/-.mp3
	mus_2003/??-??.mp3
	Renaming from mus_2003/??-??.mp3 to mus_2003/A_Russo_K_Agati-Mechti_Zbilis.mp3

That actually is pretty decent, not the best but okay. What I realized is that, if the file is not identifiable then it just takes the *id3* tag and shows you that as the result. So the second song (that had the weird character set) must of had broken *id3* tags and *echoprint* wasn't able to fingerprint it. So let's run the command manually and check what the second file returned:

	[elatov@moxz mus_2003.bak]$ ~/downloads/echoprint-codegen-release-4.12/echoprint-codegen Àëñó-Â÷åðà.mp3 10 30
	{"metadata":{"artist":"Àëñó", "release":"", "title":"Â÷åðà", "genre":"Pop", "bitrate":160,"sample_rate":44100, "duration":184,
	"filename":"Àëñó-Â÷åðà.mp3", "samples_decoded":330902,
	"given_duration":30, "start_offset":10, "version":4.12,
	"codegen_time":0.610735, "decode_time":5.342479}, "code_count":702,
	"code":"eJylmW2OpCcMh", "tag":0}

Now checking out the *id3* tags, I saw the following:

	[elatov@moxz mus_2003.bak]$ exiftool -json Àëñó-Â÷åðà.mp3
	{
	"SourceFile": "Àëñó-Â÷åðà.mp3",
	"ExifToolVersion": 9.12,
	"FileName": "Àëñó-Â÷åðà.mp3",
	"Directory": ".",
	"FileSize": "3.5 MB",
	"FileModifyDate": "2013:01:29 13:29:27-08:00",
	"FileAccessDate": "2013:01:29 15:45:10-08:00",
	"FileInodeChangeDate": "2013:01:29 15:36:05-08:00",
	"FilePermissions": "rwx------",
	"FileType": "MP3",
	"MIMEType": "audio/mpeg",
	"MPEGAudioVersion": 1,
	"AudioLayer": 3,
	"AudioBitrate": "160 kbps",
	"SampleRate": 44100,
	"ChannelMode": "Stereo",
	"MSStereo": "Off",
	"IntensityStereo": "Off",
	"CopyrightFlag": false,
	"OriginalMedia": true,
	"Emphasis": "None",
	"ID3Size": 2307,
	"Track": "",
	"EncodedBy": "",
	"UserDefinedURL": "http://www.delit.net",
	"Copyright": "",
	"Genre": "Pop",
	"Album": "",
	"Year": 2002,
	"Title": "Â÷åðà",
	"Composer": "",
	"OriginalArtist": "",
	"Artist": "Àëñó",
	"Comment": "http://www.delit.net",
	"DateTimeOriginal": 2002,
	"Duration": "0:03:04 (approx)"
	}

We can see that the "Artist" and "Title" returned from **echoprint** are the same as the file name and the *id3* tags. I found another python script, which checks the *id3* tags and fixes the character set on them. It's called [tag2utf](http://sourceforge.net/projects/tag2utf/). After I downloaded the script, here is how it looked like when executed:

	[elatov@moxz mus]$ ./tag2utf.py mus_2003.bak/
	1 file(s) finded in the mus_2003.bak/

	[c] If charset of tags is cp1251:
	Àëñó-Â÷åðà.mp3 Вчера Алсу

	[k] If charset of tags is koi8-r:
	Àëñó-Â÷åðà.mp3 бВЕПЮ юКЯС

	Select charset:
	's' - skip this file(s)
	c

So the above script shows you two different character sets that it can fix. If the translation looks good (in my case the *cp1251* character set looked correct) then you can choose that character set to be fixed. Now checking the *id3* tag, I saw the following:

	[elatov@moxz mus_2003.bak]$ exiftool Àëñó-Â÷åðà.mp3 | grep -E "^Artist|Title"
	Title : Вчера
	Artist : Алсу

That looks exactly right. Now running **echoprint-codegen**, we get the following:

	[elatov@moxz mus_2003.bak]$ ~/downloads/echoprint-codegen-release-4.12/echoprint-codegen Àëñó-Â÷åðà.mp3 10 30
	{"metadata":{"artist":"Алсу", "release":"", "title":"Вчера", "genre":"Pop",
	 "bitrate":160,"sample_rate":44100, "duration":184, "filename":"Àëñó-Â÷åðà.mp3",
	 "samples_decoded":330902, "given_duration":30, "start_offset":10, "version":4.12,
	 "codegen_time":0.592142, "decode_time":6.291707}, "code_count":702, "code":"eJylmW",
	 "tag":0}

So *echoprint* wasn't that helpful. But now re-running my script again, after the character set was fixed, I saw the following before the fix:

	[elatov@moxz best]$ ls mus_2003
	Àëñó-Â÷åðà.mp3 ??-??.mp3 Газманов_Олег-На_заре.mp3

and then running the script again:

	[elatov@moxz best]$ ./af_ep.py mus_2003
	mus_2003/Газманов_Олег-На_заре.mp3
	Renaming from mus_2003/Газманов_Олег-На_заре.mp3 to mus_2003/Gazmanov_Oleg-Na_Zare.mp3
	mus_2003/Àëñó-Â÷åðà.mp3
	Renaming from mus_2003/Àëñó-Â÷åðà.mp3 to mus_2003/Alsu-Vchera.mp3
	mus_2003/??-??.mp3
	Renaming from mus_2003/??-??.mp3 to mus_2003/A_Russo_K_Agati-Mechti_Zbilis.mp3

and lastly, here is the aftermath:

	[elatov@moxz best]$ ls mus_2003
	Alsu-Vchera.mp3 A_Russo_K_Agati-Mechti_Zbilis.mp3 Gazmanov_Oleg-Na_Zare.mp3

That looked perfect except that it fails back to tags if the file can't be fingerprinted. What if the tags were gone and we can't fingerprint it. If I was doing this across regular/popular/US songs, I bet the above would've sufficed for my library. I then ran into [this](http://forum.xbmc.org/showthread.php?tid=37230) *xbmc* forum. From that Forum:

> - **Last.fm fingerprints** - Uses an open source library to fingerprint and a web service to identify the song. Used by banshee-extension-lastfm fingerprint, for example.
> - **MusicDNS/PUID** - Open source fingerprinting with libofa, closed database queries. MusicDNS was sold to Sony-owned Gracenote and is expected to be shit-canned. Thus, MusicBrainz is ditching it for Echoprint & Acoustid (see above article from 6/23/11).
> - **ENMFP (Echo Nest Musical Fingerprint)** - powered by The Echo Nest Closed source fingerprinter, free for use subject to the terms of the Echo Nest Terms Of Service.
> - **Echoprint** - powered by The Echo Nest MIT-licensed fingerprinter named Echoprint Codegen, public API (works with Echoprints and proprietary ENMFP's), and a permissive license for their database.
> - **Acoustid** - fingerprint LGPL fingerprinter named Chromaprint, open web service.
>
> From my research, here's where fingerprinting stands
>
> Last.fm is a safe bet with 90 million songs indexed and a rock-solid API. ENMFP and Echoprints both use the same Echo Nest API; the ENMFP database spans 30 million songs, whereas the Echoprints database only covers 13 million songs. The Acoustid database is an unknown (small) size, not to mention inaccessible for the last week due to a database rebuild. Currently, the MusicBrainz database supports MusicDNS PUID fingerprints; Echoprint support is available on one of their test servers, and Acoustid fingerprint support will (probably) be added in the unspecified future.

So I decided to check out any APIs for **lastfm**, and I ran across "[pylastfp](http://pypi.python.org/pypi/pylastfp/0.1)". From their page:

> This is a Python interface to Last.fm's acoustic fingerprinting library (called fplib) and its related API services. It performs fingerprint extraction, fingerprint ID lookup, and track metadata lookup.

It also comes with some helpers for decoding audio files  It's funny cause also from their page:

This library is by Adrian Sampson. It includes the fplib source code, which is by Last.fm. fplib is licensed under the LGPLv3, so pylastfp uses the same license. pylastfp was written to be used with beets, which you should probably check out.

It looks like this was written for **beets**, I wonder if I was mis-using **beets**, or maybe it wasn't implemented yet. Regardless, the modules comes with a script which allows you to fingerprint files. So first let's check to see if the tags are broken:

	[elatov@moxz mus_2003]$ exiftool Alsu-Vchera.mp3 | grep -E "^Artist|Title"
	Title : Â÷åðà
	Artist : Àëñó

Now using **pylastfm**, what do we find?:

	[elatov@moxz mus_2003]$ lastmatch.py Alsu-Vchera.mp3
	1.000000: Алсу - Вчера
	0.049488: Алсу - vchera
	0.044369: Àëñó - Â÷åðà
	0.018771: Ąėńó - Ā÷åšą
	0.013652: Àëñó - Â÷å›à

That looks great. It looks like **lastfm** has a little bit more entries than **echoprint**. The **lastmatch.py** was a python script, so I borrowed some of their contents and integrated it into my script. Here is how my final script looked like:

	#!/bin/env python
	-*- coding: UTF-8 -*-

	import sys,os,re
	import lastfp

	rootdir = sys.argv[1]

	def translit(cyr_str):
	capital_letters = { u'А': u'A', u'Б': u'B', u'В': u'V', u'Г': u'G', u'Д': u'D', u'Е': u'E', u'Ё': u'E', u'Ж': u'j', u'З': u'Z', u'И': u'I', u'Й': u'Y', u'К': u'K', u'Л': u'L', u'М': u'M', u'Н': u'N', u'О': u'O', u'П': u'P', u'Р': u'R', u'С': u'S', u'Т': u'T', u'У': u'U', u'Ф': u'F', u'Х': u'H', u'Ц': u'Ts', u'Ч': u'Ch', u'Ш': u'Sh', u'Щ': u'Sch', u'Ъ': u'y', u'Ы': u'Y', u'Ь': u'i', u'Э': u'E', u'Ю': u'Yu', u'Я': u'Ya' }

	lower_case_letters = { u'а': u'a', u'б': u'b', u'в': u'v', u'г': u'g', u'д': u'd', u'е': u'e', u'ё': u'e', u'ж': u'j', u'з': u'z', u'и': u'i', u'й': u'y', u'к': u'k', u'л': u'l', u'м': u'm', u'н': u'n', u'о': u'o', u'п': u'p', u'р': u'r', u'с': u's', u'т': u't', u'у': u'u', u'ф': u'f', u'х': u'h', u'ц': u'ts', u'ч': u'ch', u'ш': u'sh', u'щ': u'sch', u'ъ': u'y', u'ы': u'y', u'ь': u'i', u'э': u'e', u'ю': u'yu', u'я': u'ya' }

	translit_string = ""

	for index, char in enumerate(cyr_str):
	if char in lower_case_letters.keys():
	char = lower_case_letters[char]
	elif char in capital_letters.keys():
	char = capital_letters[char]
	if len(cyr_str) > index+1:
	if cyr_str[index+1] not in lower_case_letters.keys():
	char = char.upper()
	else:
	char = char.upper()
	translit_string += char

	return translit_string

	def get_finger_print(audio_file):
	API_KEY = '7821ee9bf9937b7f94af2abecced8ddd'
	xml = lastfp.gst_match(API_KEY, audio_file)
	matches = lastfp.parse_metadata(xml)

	song_artist = matches[0]['artist']
	song_title = matches[0]['title']

	if isinstance(song_artist,unicode):
	song_artist = translit(matches[0]['artist'])
	if isinstance(song_title,unicode):
	song_title = translit(matches[0]['title'])

	return song_title,song_artist
	def clean_up_names(string):
	string=(re.sub("['\"]", "", string))
	string=(re.sub("[^\w]+", "_", string))
	string=(re.sub("[_]+", "_", string))
	if string.endswith('_'):
	string=string[:-1]
	if string.startswith('_'):
	string=string[1:]
	string=string.title()

	return string

	for path, subdirs, files in os.walk(rootdir):
	for name in files:
	print os.path.join(path,name)
	(s_title,s_artist)=get_finger_print(os.path.join(path, name))
	s_title_c=clean_up_names(s_title)
	s_artist_c=clean_up_names(s_artist)
	if (s_title_c != 'Failed') and (s_artist_c != 'Failed'):
	ext=os.path.splitext(name)[1].lower()
	filename="%s-%s%s" % (s_artist_c,s_title_c,ext)
	src=os.path.join(path,name)
	dst=os.path.join(path,filename)
	if str(dst) != src:
	print ("Renaming from " + src + " to " + str(dst))
	os.rename(src,dst)

So this is the fourth python script I wrote, therefore you know that it basically sucks. I am sure there are a bunch of things I could fix, but the basic functionality is there. So now running the script on files with broken tags and file names. First before:

	[elatov@moxz best]$ ls mus_2003 Àëñó-Â÷åðà.mp3 ??-??.mp3 Газманов_Олег-На_заре.mp3

Now the script:

	[elatov@moxz mus]$ ./af_lf.py mus_2003
	mus_2003/Газманов_Олег-На_заре.mp3
	Renaming from mus_2003/Газманов_Олег-На_заре.mp3 to mus_2003/Oleg_Gazmanov-Na_Zare.mp3
	mus_2003/Àëñó-Â÷åðà.mp3
	Renaming from mus_2003/Àëñó-Â÷åðà.mp3 to mus_2003/Alsu-Vchera.mp3
	mus_2003/??-??.mp3
	Renaming from mus_2003/??-??.mp3 to mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3

And now it looks like this after:

	[elatov@moxz mus]$ ls mus_2003
	Alsu-Vchera.mp3 Oleg_Gazmanov-Na_Zare.mp3 Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3

We can even see that the third song now has a longer name, since it was actually fingerprinted against the *lastfm* database. But this doesn't fix the tags, just the file names. As a side note I also ran across "[lastfm fingerprinter](https://github.com/lastfm/Fingerprinter)". It's very similar to **echoprint-codegen**, just for *lastfm*. After I compiled the application here is how the output looks like:

	[elatov@moxz mus_2003]$ ~/downloads/Fingerprinter-master/bin/lastfm-fpclient Alsu-Vchera.mp3
	<xml version="1.0" encoding="utf-8"?>
	<lfm status="ok">
	<tracks>
	<track rank="1">
	<name>Вчера</name>
	<duration>219</duration>
	<artist> <name>Алсу</name>

As you can see the output is in *XML*, but you could always program/script around that.

At this point we have all the audio files named **ARTIST-TITLE.EXT**. The artist and the title were acoustically fingerprinted against the *lastfm* database. However the tags are still messed up. For example here are the tags from my files:

	[elatov@moxz data]$ find mus_2003 -name "*.mp3" -exec id3v2 -l {} \;
	id3v1 tag info for mus_2003/Oleg_Gazmanov-Na_Zare.mp3:
	Title : ?? ????
	Artist: ???????? ????
	Album :
	Year: 2003,
	Genre: Other (12) Comment: http://delit.net
	Track: 13
	id3v2 tag info for mus_2003/Oleg_Gazmanov-Na_Zare.mp3:
	TCOP (Copyright message):
	TYER (Year): 2003
	TRCK (Track number/Position in set): 13
	TCON (Content type): Pop (13)
	COMM (Comments): ()[eng]: http://delit.net
	WXXX (User defined URL link): (): http://delit.net
	TENC (Encoded by): NetStream AudioLab
	TIT2 (Title/songname/content description): 0 70@5
	TCOM (Composer):
	TOPE (Original artist(s)/performer(s)):
	TPE1 (Lead performer(s)/Soloist(s)): 07<0=>2 ;53

	id3v1 tag info for mus_2003/Alsu-Vchera.mp3:
	Title : ���
	Artist: ��
	Album :
	Year: 2002,
	Genre: Pop (13)
	Comment: http://www.delit.net
	id3v2 tag info for mus_2003/Alsu-Vchera.mp3:
	TRCK (Track number/Position in set):
	TENC (Encoded by):
	WXXX (User defined URL link): (): http://www.delit.net
	TCOP (Copyright message):
	TCON (Content type): Pop (13)
	TALB (Album/Movie/Show title):
	TYER (Year): 2002
	COMM (Comments): ()[eng]: http://www.delit.net
	TIT2 (Title/songname/content description): ���
	TCOM (Composer):
	TOPE (Original artist(s)/performer(s)):
	TPE1 (Lead performer(s)/Soloist(s)): ��
	COMM (Comments): ()[]: http://www.delit.net

	id3v1 tag info for mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3:
	Title : Mechti Zbilis'
	Artist: A. Russo & K. Agati
	Album : Year: ,
	Genre: Other (12)
	Comment:
	id3v2 tag info for mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3:
	TIT2 (Title/songname/content description): Mechti Zbilis'
	TCON (Content type):
	Other (12)
	TPE1 (Lead performer(s)/Soloist(s)): A. Russo & K. Agati

We can see that both *id3v1* and *id3v2* tags are all over the place. If you wanted to, you could strip all the tags, like so:

	[elatov@moxz data]$ find mus_2003 -name "*.mp3" -exec id3v2 -D {} \;
	Stripping id3 tag in "mus_2003/Oleg_Gazmanov-Na_Zare.mp3"...id3v1 and v2 stripped.
	Stripping id3 tag in "mus_2003/Alsu-Vchera.mp3"...id3v1 and v2 stripped.
	Stripping id3 tag in "mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3"...id3v1 and v2 stripped.

And now checking the tags:

	[elatov@moxz data]$ find mus_2003 -name "*.mp3" -exec id3v2 -l {} \;
	mus_2003/Oleg_Gazmanov-Na_Zare.mp3: No ID3 tag
	mus_2003/Alsu-Vchera.mp3: No ID3 tag
	mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3: No ID3 tag

And now we can use **EasyTag** to fill the tags from our file names. First start up *EasyTag*, it will look like this:

![easytag started Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/easytag_started.png)

Then navigate to your folder/playlist, it will looks something like this:

![easy tag load folder Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/easy_tag_load_folder.png)

We can see that, 3 files were found (which is expected) and the *id3* tags are blank. Then select all 3 files and go to "Scanner" -> "Fill Tags", it will look like this:

![easy tag scanner fill tags g Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/easy_tag_scanner_fill_tags_g.png)

After you select that, a window will pop up. Here you can define the pattern of your file names. In my case my files were named **ARTIST-TITLE** which in *easytag* will translate to "%a-%t". So I entered that pattern and I saw the following:

![fill tag pattern Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/fill_tag_pattern.png)

You can see it even shows what it matched for the first file. To fill in the tags, just click on the "Green Folder" button and it will start filling in the tags. After it's done, in the logs pane you can see if it was successful and now the tags will be filled in. It will look like this:

![fill tags after scan Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/fill_tags_after_scan.png)

After that, to save the changes, close the scanner window and go to "File" -> "Save Files":

![easytag savefiles g Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/easytag_savefiles_g.png)

After you hit "Save Files", it will ask you to confirm and you can check the box "Repeat Action for the rest of the files" so it does it to all of them:

![confirm save files Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/confirm_save_files.png)

After it's done, in the logs pane you will see messages like "Updated Tag" like so:

![easytag saved tags Organizing Your Music Library Using Acoustic Fingerprinting](https://github.com/elatov/uploads/raw/master/2013/01/easytag_saved_tags.png)

Now checking that tags on all the files:

	[elatov@moxz data]$ find mus_2003 -name "*.mp3" -exec id3v2 -l {} \;
	id3v1 tag info for mus_2003/Oleg_Gazmanov-Na_Zare.mp3:
	Title : Na_Zare
	Artist: Oleg_Gazmanov
	Album : Year: , Genre: Unknown (255)
	Comment:
	mus_2003/Oleg_Gazmanov-Na_Zare.mp3: No ID3v2 tag

	id3v1 tag info for mus_2003/Alsu-Vchera.mp3:
	Title : Vchera
	Artist: Alsu
	Album : Year: , Genre: Unknown (255)
	Comment:
	mus_2003/Alsu-Vchera.mp3: No ID3v2 tag

	id3v1 tag info for mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3:
	Title : Lyubovi_Kotoroy_Bolishe_Net
	Artist: Orbakayte_Kristina_Russo_Avraam
	Album : Year: , Genre: Unknown (255)
	Comment:
	mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3: No ID3v2 tag

That looks pretty good, it's clean and concise :) Be careful on stripping all the tags. I only did this cause I knew my tags were messed up, if you have appropriate tags and you remove them then they are gone forever.
