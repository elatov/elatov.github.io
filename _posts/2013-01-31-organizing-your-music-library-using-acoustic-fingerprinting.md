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
  - lastfm-fpclient
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
<p>I wrote a <a href="http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/installing-subsonic-on-fedora-17/']);">previous</a> post about running <em>subsonic</em>. I really liked the software cause it uses the file system directory structure as your music library. I have a lot of custom playlists and they don&#8217;t belong to any album, therefore I organize my playlists by folders. Some of these songs are from Russian CDs which are combinations of songs for that year (this is pretty typical in Russia, it&#8217;s equivalent of the &#8220;<a href="http://www.nowthatsmusic.com/home/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.nowthatsmusic.com/home/']);">Now, That&#8217;s What I Call Music</a>&#8221; CDs in the US).</p>
<p>I used to have an <em>iPod</em> and I used to use <em>Songbird</em> as my music player and this ended up messing up my file names and even the <em>id3</em> tags of the audio files. For example here is a sample folder with my songs:</p>
	[elatov@moxz mus_2003]$ ls -1 
	Àëñó-Â÷åðà.mp3 
	??-??.mp3 
	Газманов\_Олег-На\_заре.mp3
	
<p>The first one is not even in Russian (or rather it&#8217;s not displaying in the Cyrillic alphabet), it&#8217;s looks like the encoding is all messed up. The second one is a bunch of question marks, so the conversion was messed up at some point. And the last one is actually in Russian.</p>
<p>My goal was to rename all the files to the following format: <strong>ARTIST-TITLE.EXT</strong>. I wasn&#8217;t worried about <em>id3</em> tags, just the file names for now. I also wanted the filenames to be in English so I could search the title without the need to change my character set. So I wanted to &#8220;transliterate&#8221; the file names from Russian/Cyrillic to English/Roman. The process is also called &#8220;Romanization&#8221; or as I have mentioned, transliteration. If you want more information about Romanization/Transliteration, check out <a href="http://en.wikipedia.org/wiki/Romanization_of_Russian" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Romanization_of_Russian']);">this</a> wikipedia page.</p>
<p>For example &#8220;<em>hello</em>&#8221; in Russian is &#8220;<em>привет</em>&#8220;, the transliteration of that would be: &#8220;<em>privet</em>&#8221; (hopefully that makes sense).</p>
<p>At first I ran across an article entitled &#8220;<a href="http://superuser.com/questions/95425/auto-tagging-mp3s" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://superuser.com/questions/95425/auto-tagging-mp3s']);">Auto-tagging MP3s</a>&#8220;. It has a list of application that do auto tagging by querying the <em>id3</em> tags of the file and then showing the correct artist or title name (some even do a search against an online database). Some of the applications listed in that page are:</p>
<ul>
<li><a style="line-height: 22px; font-size: 13px;" href="http://musicbrainz.org/doc/MusicBrainz_Picard" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://musicbrainz.org/doc/MusicBrainz_Picard']);">picard</a></li>
<li><a style="line-height: 22px; font-size: 13px;" href="http://projects.gnome.org/easytag/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://projects.gnome.org/easytag/']);">EasyTAG</a></li>
<li><a style="line-height: 22px; font-size: 13px;" href="http://beets.radbox.org/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://beets.radbox.org/']);">beets</a></li>
<li><a style="line-height: 22px; font-size: 13px;" href="http://www.jthink.net/jaikoz/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.jthink.net/jaikoz/']);">Jaikoz</a> </li>
</ul>
<p>I tried some of the applications, but they couldn&#8217;t find any information on my songs. Here is a screenshot of  <em>picard</em> for my 3 songs:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_no_match_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_no_match_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_no_match_g.png" alt="picard no match g Organizing Your Music Library Using Acoustic Fingerprinting" width="883" height="576" class="alignnone size-full wp-image-5946" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>Notice at the bottom it says &#8220;No Matching Tracks above the threshold for file&#8221;. I tried enabling Fingerprinting:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_finger_printing_enabled.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_finger_printing_enabled.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_finger_printing_enabled.png" alt="picard finger printing enabled Organizing Your Music Library Using Acoustic Fingerprinting" width="761" height="538" class="alignnone size-full wp-image-5944" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>I also enabled the <em>lastfm</em> plugin:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_lastfm_plugin.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_lastfm_plugin.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/picard_lastfm_plugin.png" alt="picard lastfm plugin Organizing Your Music Library Using Acoustic Fingerprinting" width="764" height="537" class="alignnone size-full wp-image-5945" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>But neither of those options/plugins were able to identify my songs, I tried the other utilities but it was to no avail. It looks like <em>musicbrainz</em> or similar databases are album centric. From the <a href="http://musicbrainz.org/doc/MusicBrainz_Picard" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://musicbrainz.org/doc/MusicBrainz_Picard']);">picard</a> home page:</p>
<blockquote>
<p>When tagging files, Picard uses an album-oriented approach. This approach allows it to utilize the <em>MusicBrainz</em> data as effectively as possible and correctly tag your music.</p>
</blockquote>
<p>But remember I wasn&#8217;t trying to tag albums, but rather single tracks. I then tried out <em>beets</em>, I even enabled the <em>chroma</em>/<em>Acoustid</em> plugin to enable acoustic fingerprinting, but it was the same thing. Check it out:</p>
	[elatov@moxz mus]$ grep plugin ~/.beetsconfig 
	plugins: chroma
	
<p>Now for <em>beets</em>:</p>
	[elatov@moxz mus]$ beet import mus_2003 
	/mnt/data/mus_2003 
	No matching release found for 3 tracks. 
	For help, see: https://github.com/sampsyo/beets/wiki/FAQ#wiki-nomatch 
	[U]se as-is, as Tracks, Skip, Enter search, enter Id, aBort?
	
<p>but it was the same thing, it couldn&#8217;t match anything. However beets is also album oriented, from the <a href="https://beets.readthedocs.org/en/stable/guides/tagger.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://beets.readthedocs.org/en/stable/guides/tagger.html']);">beets</a> page:</p>
<blockquote>
<p>Your music should be organized by album into directories. That is, the tagger assumes that each album is in a single directory. These directories can be arbitrarily deep (like music/2010/hiphop/seattle/freshespresso/glamour), but any directory with music files in it is interpreted as a separate album. This means that your flat directory of six thousand uncategorized MP3s won’t currently be autotaggable. (This will change eventually.)</p>
</blockquote>
<p>If the acoustic fingerprinting would&#8217;ve worked, it would have been sweet (<em>beets</em> looks really cool). After I fix all my file names and tags, I might use <em>beets</em> to manage my library just cause it looks so cool and flexible.</p>
<p>I then ran into <a href="https://github.com/echonest/echoprint-codegen#codegen-for-echoprint" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/echonest/echoprint-codegen#codegen-for-echoprint']);">echoprint</a>. They provide source for an application which allows you to pass in an audio file and it will query their online database and will show you the title of the song. I downloaded the source from <a href="https://github.com/echonest/echoprint-codegen" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/echonest/echoprint-codegen']);">here</a>. From the <em>ReadMe</em>, here are the requirements:</p>
<blockquote>
<p>Requirements<br /> For libcodegen</p>
<ul>
<li>Boost >= 1.35 </li>
<li>zlib </li>
</ul>
<p>Additional requirements for the codegen binary</p>
<ul>
<li>&#91;TagLib&#93;(http://developer.kde.org/~wheeler/taglib.html &#8220;TagLib&#8221;) </li>
<li>ffmpeg &#8211; this is called via shell and is not linked into codegen  </li>
</ul>
</blockquote>
<p>Here is an example from their site on how to compile the application, once you have all the prerequisites setup:</p>
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
	
<p>I was able to compile the source, and then trying to query one of the songs, I saw the following:</p>
	[elatov@moxz mus_2003]$ ~/downloads/echoprint-codegen-release-4.12/echoprint-codegen \?\?-\?\?.mp3 10 30 
	{"metadata":{"artist":"A. Russo &amp; K. Agati ", "release":"", "title":"Mechti Zbilis'", "genre":"Other", 
	"bitrate":128,"sample_rate":44100, "duration":184, "filename":"??-??.mp3", "samples_decoded":330902, "given_duration":30, "start_offset":10, "version":4.12, "codegen_time":0.666698, "decode_time":5.102925}, "code_count":798, "code":"eJztWG2SLSkK3ZIoo", "tag":0} 
	
<p>That actually looked okay. For testing reasons, I wanted to write a python script to basically try to acoustically fingerprint every file in a directory. I haven&#8217;t done python in a while, so I just went with it. I actually decided to parse the output of the above command and then rename the file accordingly. Hindsight, I should have used a python API provided for <em>echoprint</em>, but I was too anxious and I just went for it. Here is how my python script looked like:</p>
<pre class="brush: /bin/env python ; notranslate"># -*- coding: UTF-8 -*- 
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
if len(cyr_str) &gt; index+1:
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

<p>There are not a lot of checks in the script, and I am sure there are a lot of things wrong with the script. Bear in mind this is probably the 3rd python script I ever wrote in my life, so please don&#8217;t judge <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Organizing Your Music Library Using Acoustic Fingerprinting" class="wp-smiley" title="Organizing Your Music Library Using Acoustic Fingerprinting" />  It doesn&#8217;t even check if the folder, that you passed to it, exists. I can&#8217;t stress enough that this is a poorly written script <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Organizing Your Music Library Using Acoustic Fingerprinting" class="wp-smiley" title="Organizing Your Music Library Using Acoustic Fingerprinting" />  To make things worse, I even &#8220;borrowed&#8221; the &#8216;translit&#8217; function from <a href="http://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://stackoverflow.com/questions/14173421/use-string-translate-in-python-to-transliterate-cyrillic']);">here</a>.</p>
<p>Anyways I created a backup of my playlist and then tried to fix the file names. Here is backup:</p>
	[elatov@moxz mus]$ rsync -avzP mus_2003/. mus_2003.bak
	
<p>Now to run the script on the playlist:</p>
	[elatov@moxz mus]$ ./af_ep.py mus_2003 
	mus_2003/Газманов\_Олег-На\_заре.mp3 
	Renaming from mus_2003/Газманов\_Олег-На\_заре.mp3 to mus_2003/Gazmanov_Oleg-Na_Zare.mp3 
	mus_2003/Àëñó-Â÷åðà.mp3 
	Renaming from mus_2003/Àëñó-Â÷åðà.mp3 to mus_2003/-.mp3 
	mus_2003/??-??.mp3 
	Renaming from mus_2003/??-??.mp3 to mus_2003/A_Russo_K_Agati-Mechti_Zbilis.mp3 
	
<p>That actually is pretty decent, not the best but okay. What I realized is that, if the file is not identifiable then it just takes the <em>id3</em> tag and shows you that as the result. So the second song (that had the weird character set) must of had broken <em>id3</em> tags and <em>echoprint</em> wasn&#8217;t able to fingerprint it. So let&#8217;s run the command manually and check what the second file returned:</p>
	[elatov@moxz mus_2003.bak]$ ~/downloads/echoprint-codegen-release-4.12/echoprint-codegen Àëñó-Â÷åðà.mp3 10 30 
	{"metadata":{"artist":"Àëñó", "release":"", "title":"Â÷åðà", "genre":"Pop", "bitrate":160,"sample_rate":44100, "duration":184, 
	"filename":"Àëñó-Â÷åðà.mp3", "samples_decoded":330902, 
	"given_duration":30, "start_offset":10, "version":4.12, 
	"codegen_time":0.610735, "decode_time":5.342479}, "code_count":702, 
	"code":"eJylmW2OpCcMh", "tag":0} 
	
<p>Now checking out the <em>id3</em> tags, I saw the following:</p>
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
	
<p>We can see that the &#8220;Artist&#8221; and &#8220;Title&#8221; returned from <em>echoprint</em> are the same as the file name and the <em>id3</em> tags. I found another python script, which checks the <em>id3</em> tags and fixes the character set on them. It&#8217;s called <a href="http://sourceforge.net/projects/tag2utf/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://sourceforge.net/projects/tag2utf/']);">tag2utf</a>. After I downloaded the script, here is how it looked like when executed:</p>
	[elatov@moxz mus]$ ./tag2utf.py mus_2003.bak/
	1 file(s) finded in the mus_2003.bak/
	
	[c] If charset of tags is cp1251:
	Àëñó-Â÷åðà.mp3 Вчера Алсу
	
	[k] If charset of tags is koi8-r:
	Àëñó-Â÷åðà.mp3 бВЕПЮ юКЯС
	
	Select charset:
	's' - skip this file(s)
	c
	
<p>So the above script shows you two different character sets that it can fix. If the translation looks good (in my case the <em>cp1251</em> character set looked correct) then you can choose that character set to be fixed. Now checking the <em>id3</em> tag, I saw the following:</p>
	[elatov@moxz mus_2003.bak]$ exiftool Àëñó-Â÷åðà.mp3 | grep -E "^Artist|Title" 
	Title : Вчера 
	Artist : Алсу
	
<p>That looks exactly right. Now running <strong>echoprint-codegen</strong>, we get the following:</p>
	[elatov@moxz mus_2003.bak]$ ~/downloads/echoprint-codegen-release-4.12/echoprint-codegen Àëñó-Â÷åðà.mp3 10 30 
	{"metadata":{"artist":"Алсу", "release":"", "title":"Вчера", "genre":"Pop",
	 "bitrate":160,"sample_rate":44100, "duration":184, "filename":"Àëñó-Â÷åðà.mp3",
	 "samples_decoded":330902, "given_duration":30, "start_offset":10, "version":4.12,
	 "codegen_time":0.592142, "decode_time":6.291707}, "code_count":702, "code":"eJylmW",
	 "tag":0} 
	
<p>So <em>echoprint</em> wasn&#8217;t that helpful. But now re-running my script again, after the character set was fixed, I saw the following before the fix:</p>
	[elatov@moxz best]$ ls mus_2003 
	Àëñó-Â÷åðà.mp3 ??-??.mp3 Газманов\_Олег-На\_заре.mp3
	
<p>and then running the script again:</p>
	[elatov@moxz best]$ ./af_ep.py mus_2003 
	mus_2003/Газманов\_Олег-На\_заре.mp3 
	Renaming from mus_2003/Газманов\_Олег-На\_заре.mp3 to mus_2003/Gazmanov_Oleg-Na_Zare.mp3 
	mus_2003/Àëñó-Â÷åðà.mp3 
	Renaming from mus_2003/Àëñó-Â÷åðà.mp3 to mus_2003/Alsu-Vchera.mp3 
	mus_2003/??-??.mp3 
	Renaming from mus_2003/??-??.mp3 to mus_2003/A_Russo_K_Agati-Mechti_Zbilis.mp3
	
<p>and lastly, here is the aftermath:</p>
	[elatov@moxz best]$ ls mus_2003 
	Alsu-Vchera.mp3 A_Russo_K_Agati-Mechti_Zbilis.mp3 Gazmanov_Oleg-Na_Zare.mp3 
	
<p>That looked perfect except that it fails back to tags if the file can&#8217;t be fingerprinted. What if the tags were gone and we can&#8217;t fingerprint it. If I was doing this across regular/popular/US songs, I bet the above would&#8217;ve sufficed for my library. I then ran into <a href="http://forum.xbmc.org/showthread.php?tid=37230" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.xbmc.org/showthread.php?tid=37230']);">this</a> <em>xbmc</em> forum. From that Forum:</p>
<blockquote>
<ul>
<li><strong>Last.fm fingerprints</strong> Uses an open source library to fingerprint and a web service to identify the song. Used by banshee-extension-lastfm fingerprint, for example.</li>
<li><strong>MusicDNS/PUID</strong> Open source fingerprinting with libofa, closed database queries. MusicDNS was sold to Sony-owned Gracenote and is expected to be shit-canned. Thus, MusicBrainz is ditching it for Echoprint &amp; Acoustid (see above article from 6/23/11).</li>
<li><strong>ENMFP (Echo Nest Musical Fingerprint)</strong> powered by The Echo Nest Closed source fingerprinter, free for use subject to the terms of the Echo Nest Terms Of Service.</li>
<li><strong>Echoprint</strong> powered by The Echo Nest MIT-licensed fingerprinter named Echoprint Codegen, public API (works with Echoprints and proprietary ENMFP&#8217;s), and a permissive license for their database. </li>
<li><strong>Acoustid</strong> fingerprint LGPL fingerprinter named Chromaprint, open web service. </li>
</ul>
<p>From my research, here&#8217;s where fingerprinting stands</p>
<p>Last.fm is a safe bet with 90 million songs indexed and a rock-solid API. ENMFP and Echoprints both use the same Echo Nest API; the ENMFP database spans 30 million songs, whereas the Echoprints database only covers 13 million songs. The Acoustid database is an unknown (small) size, not to mention inaccessible for the last week due to a database rebuild. Currently, the MusicBrainz database supports MusicDNS PUID fingerprints; Echoprint support is available on one of their test servers, and Acoustid fingerprint support will (probably) be added in the unspecified future.</p>
</blockquote>
<p>So I decided to check out any APIs for <em>lastfm</em>, and I ran across &#8220;<a href="http://pypi.python.org/pypi/pylastfp/0.1" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pypi.python.org/pypi/pylastfp/0.1']);">pylastfp</a>&#8220;. From their page:</p>
<blockquote>
<p>This is a Python interface to Last.fm&#8217;s acoustic fingerprinting library (called fplib) and its related API services. It performs fingerprint extraction, fingerprint ID lookup, and track metadata lookup.</p>
</blockquote>
<p>It also comes with some helpers for decoding audio files  It&#8217;s funny cause also from their page:</p>
<blockquote>
<p>This library is by Adrian Sampson. It includes the fplib source code, which is by Last.fm. fplib is licensed under the LGPLv3, so pylastfp uses the same license. pylastfp was written to be used with beets, which you should probably check out.</p>
</blockquote>
<p>It looks like this was written for <em>beets</em>, I wonder if I was mis-using <em>beets</em>, or maybe it wasn&#8217;t implemented yet. Regardless, the modules comes with a script which allows you to fingerprint files. So first let&#8217;s check to see if the tags are broken:</p>
	[elatov@moxz mus_2003]$ exiftool Alsu-Vchera.mp3 | grep -E "^Artist|Title" 
	Title : Â÷åðà 
	Artist : Àëñó
	
<p>Now using <strong>pylastfm</strong>, what do we find?:</p>
	[elatov@moxz mus_2003]$ lastmatch.py Alsu-Vchera.mp3 
	1.000000: Алсу - Вчера 
	0.049488: Алсу - vchera 
	0.044369: Àëñó - Â÷åðà 
	0.018771: Ąėńó - Ā÷åšą 
	0.013652: Àëñó - Â÷å›à
	
<p>That looks great. It looks like <em>lastfm</em> has a little bit more entries than <em>echoprint</em>. The &#8220;<strong>lastmatch.py</strong>&#8221; was a python script, so I borrowed some of their contents and integrated it into my script. Here is how my final script looked like:</p>
<pre class="brush: /bin/env python; notranslate"># -*- coding: UTF-8 -*-

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
if len(cyr_str) &gt; index+1:
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

<p>So this is the fourth python script I wrote, therefore you know that it basically sucks. I am sure there are a bunch of things I could fix, but the basic functionality is there. So now running the script on files with broken tags and file names. First before:</p>
	[elatov@moxz best]$ ls mus_2003 Àëñó-Â÷åðà.mp3 ??-??.mp3 Газманов\_Олег-На\_заре.mp3
	
<p>Now the script:</p>
	[elatov@moxz mus]$ ./af_lf.py mus_2003 
	mus_2003/Газманов\_Олег-На\_заре.mp3 
	Renaming from mus_2003/Газманов\_Олег-На\_заре.mp3 to mus_2003/Oleg_Gazmanov-Na_Zare.mp3 
	mus_2003/Àëñó-Â÷åðà.mp3 
	Renaming from mus_2003/Àëñó-Â÷åðà.mp3 to mus_2003/Alsu-Vchera.mp3 
	mus_2003/??-??.mp3 
	Renaming from mus_2003/??-??.mp3 to mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3
	
<p>And now it looks like this after:</p>
	[elatov@moxz mus]$ ls mus_2003 
	Alsu-Vchera.mp3 Oleg_Gazmanov-Na_Zare.mp3 Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3
	
<p>We can even see that the third song now has a longer name, since it was actually fingerprinted against the <em>lastfm</em> database. But this doesn&#8217;t fix the tags, just the file names. As a side note I also ran across &#8220;<a href="https://github.com/lastfm/Fingerprinter" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://github.com/lastfm/Fingerprinter']);">lastfm fingerprinter</a>&#8220;. It&#8217;s very similar to <strong>echoprint-codegen</strong>, just for <em>lastfm</em>. After I compiled the application here is how the output looks like:</p>
	[elatov@moxz mus_2003]$ ~/downloads/Fingerprinter-master/bin/lastfm-fpclient Alsu-Vchera.mp3 &lt;?xml version="1.0" encoding="utf-8"?&gt; 
	&lt;lfm status="ok"&gt; 
	&lt;tracks&gt; 
	&lt;track rank="1"&gt; 
	&lt;name&gt;Вчера&lt;/name&gt; 
	&lt;duration&gt;219&lt;/duration&gt; 
	&lt;artist&gt; &lt;name&gt;Алсу&lt;/name&gt;
	
<p>As you can see the output is in <em>XML</em>, but you could always program/script around that.</p>
<p>At this point we have all the audio files named <strong>ARTIST-TITLE.EXT</strong>. The artist and the title were acoustically fingerprinted against the <em>lastfm</em> database. However the tags are still messed up. For example here are the tags from my files:</p>
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
	TPE1 (Lead performer(s)/Soloist(s)): 07&lt;0=&gt;2 ;53 
	
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
	Artist: A. Russo &amp; K. Agati 
	Album : Year: , 
	Genre: Other (12) 
	Comment: 
	id3v2 tag info for mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3: 
	TIT2 (Title/songname/content description): Mechti Zbilis' 
	TCON (Content type): 
	Other (12) 
	TPE1 (Lead performer(s)/Soloist(s)): A. Russo &amp; K. Agati 
	
<p>We can see that both <em>id3v1</em> and <em>id3v2</em> tags are all over the place. If you wanted to, you could strip all the tags, like so:</p>
	[elatov@moxz data]$ find mus_2003 -name "*.mp3" -exec id3v2 -D {} \; 
	Stripping id3 tag in "mus_2003/Oleg_Gazmanov-Na_Zare.mp3"...id3v1 and v2 stripped. 
	Stripping id3 tag in "mus_2003/Alsu-Vchera.mp3"...id3v1 and v2 stripped. 
	Stripping id3 tag in "mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3"...id3v1 and v2 stripped. 
	
<p>And now checking the tags:</p>
	[elatov@moxz data]$ find mus_2003 -name "*.mp3" -exec id3v2 -l {} \; 
	mus_2003/Oleg_Gazmanov-Na_Zare.mp3: No ID3 tag 
	mus_2003/Alsu-Vchera.mp3: No ID3 tag 
	mus_2003/Orbakayte_Kristina_Russo_Avraam-Lyubovi_Kotoroy_Bolishe_Net.mp3: No ID3 tag
	
<p>And now we can use <em>EasyTag</em> to fill the tags from our file names. First start up <em>EasyTag</em>, it will look like this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_started.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_started.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_started.png" alt="easytag started Organizing Your Music Library Using Acoustic Fingerprinting" width="1038" height="689" class="alignnone size-full wp-image-5958" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>Then navigate to your folder/playlist, it will looks something like this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/easy_tag_load_folder.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/easy_tag_load_folder.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/easy_tag_load_folder.png" alt="easy tag load folder Organizing Your Music Library Using Acoustic Fingerprinting" width="1038" height="690" class="alignnone size-full wp-image-5959" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>We can see that, 3 files were found (which is expected) and the <em>id3</em> tags are blank. Then select all 3 files and go to &#8220;Scanner&#8221; -> &#8220;Fill Tags&#8221;, it will look like this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/easy_tag_scanner_fill_tags_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/easy_tag_scanner_fill_tags_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/easy_tag_scanner_fill_tags_g.png" alt="easy tag scanner fill tags g Organizing Your Music Library Using Acoustic Fingerprinting" width="1039" height="692" class="alignnone size-full wp-image-5960" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>After you select that, a window will pop up. Here you can define the pattern of your file names. In my case my files were named &#8220;<strong>ARTIST-TITLE</strong>&#8221; which in <em>easytag</em> will translate to &#8220;%a-%t&#8221;. So I entered that pattern and I saw the following:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/fill_tag_pattern.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/fill_tag_pattern.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/fill_tag_pattern.png" alt="fill tag pattern Organizing Your Music Library Using Acoustic Fingerprinting" width="398" height="115" class="alignnone size-full wp-image-5961" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>You can see it even shows what it matched for the first file. To fill in the tags, just click on the &#8220;Green Folder&#8221; button and it will start filling in the tags. After it&#8217;s done, in the logs pane you can see if it was successful and now the tags will be filled in. It will look like this:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/fill_tags_after_scan.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/fill_tags_after_scan.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/fill_tags_after_scan.png" alt="fill tags after scan Organizing Your Music Library Using Acoustic Fingerprinting" width="1040" height="685" class="alignnone size-full wp-image-5962" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>After that, to save the changes, close the scanner window and go to &#8220;File&#8221; -> &#8220;Save Files&#8221;:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_savefiles_g.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_savefiles_g.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_savefiles_g.png" alt="easytag savefiles g Organizing Your Music Library Using Acoustic Fingerprinting" width="1041" height="694" class="alignnone size-full wp-image-5965" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>After you hit &#8220;Save Files&#8221;, it will ask you to confirm and you can check the box &#8220;Repeat Action for the rest of the files&#8221; so it does it to all of them:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/confirm_save_files.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/confirm_save_files.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/confirm_save_files.png" alt="confirm save files Organizing Your Music Library Using Acoustic Fingerprinting" width="296" height="120" class="alignnone size-full wp-image-5966" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>After it&#8217;s done, in the logs pane you will see messages like &#8220;Updated Tag&#8221; like so:</p>
<p><a href="http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_saved_tags.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_saved_tags.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/01/easytag_saved_tags.png" alt="easytag saved tags Organizing Your Music Library Using Acoustic Fingerprinting" width="1039" height="626" class="alignnone size-full wp-image-5967" title="Organizing Your Music Library Using Acoustic Fingerprinting" /></a></p>
<p>Now checking that tags on all the files:</p>
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
	
<p>That looks pretty good, it&#8217;s clean and concise <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Organizing Your Music Library Using Acoustic Fingerprinting" class="wp-smiley" title="Organizing Your Music Library Using Acoustic Fingerprinting" />  Be careful on stripping all the tags. I only did this cause I knew my tags were messed up, if you have appropriate tags and you remove them then they are gone forever.</p>
<p class="wp-flattr-button"><a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/01/organizing-your-music-library-using-acoustic-fingerprinting/" title=" Organizing Your Music Library Using Acoustic Fingerprinting" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:acoustic fingerprinting,acoustid,beets,character set,chromaprint,cyrillic,EasyTag,echoprint,echoprint-codegen,exiftool,id3-tags,id3v1,id3v2,lastfm,lastfm-fpclient,lastmatch.py,MusicBrainz,picard,pylastfp,python,romanization,songbird,subsonic,tag2utf.py,transliterate,blog;button:compact;">I wrote a previous post about running subsonic. I really liked the software cause it uses the file system directory structure as your music library. I have a lot of...</a></p>