---
title: Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File
author: Karim Elatov
layout: post
permalink: /2013/09/combine-vobsub-subidx-format-subtitles-single-subrip-srt-format-file/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1751052072
categories:
  - OS
tags:
  - SubRip
  - tesseract
  - VobSub
---
I recently had a situation where I had 2 *Avi* files and 2 *Sub/Idx* files, and I just wanted to combine them into one *Avi* file and one *srt* file. Here are the files that I started out with:

    $ ls
    file1.avi  file1.sub  file2.idx
    file1.idx  file2.avi  file2.sub
    

## Difference between VobSub and SRT

From <a href="http://www.afterdawn.com/guides/archive/subtitle_formats_explained.cfm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.afterdawn.com/guides/archive/subtitle_formats_explained.cfm']);">Subtitle Formats Explained</a>:

> Most subtitles consist purely of text characters. Since text is also some of the easiest data to store and compress it makes sense to store subtitles as simple text files or a text stream within a video file. Although it&#8217;s normal for all subtitles to start out this way, that doesn&#8217;t mean that&#8217;s how they&#8217;re stored.
> 
> As a matter of fact subtitles on DVDs aren&#8217;t actually text. They&#8217;re actually encoded as raster graphics. Much like the way characters on older text-based computer interfaces, they&#8217;re actually just a collection of dots on a grid. These images are put over the top of the video frame when displayed.

More from the same site:

> VobSub subtitles have become very common because it&#8217;s easy to get them from DVDs. In fact, VobSub basically just re-packages the images from the DVD into a file that has the extension of .SUB and additional information in another file with an extension of .IDX. They&#8217;re generally referred to as either VobSub or IDX + SUB (IDX/SUB) subtitles. Information in the IDX file tells media player software the color of the subtitles, their position on the screen, when they appear and disappear, and a number of other important pieces of information.

So **VobSub** format consists of images and a descriptor file to correlate the times when each image should be displayed (this is a very oversimplified definition &#8230; there are a lot of other aspect to it as well). Here is similar description from <a href="http://wiki.multimedia.cx/index.php?title=VOBsub" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.multimedia.cx/index.php?title=VOBsub']);">VobSub</a>:

> VOBsub extracts the DVD subtitles raw PES from a DVD and dumps this to a .sub file. It also creates a .idx Index file with the times and byteoffsets for each and every single subtitle. The format has support for multiple tracks and can also be embedded in MP4 and Matroska files.

For **SRT** or (SubRip text file format), we can check out the <a href="http://en.wikipedia.org/wiki/SubRip" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/SubRip']);">wikipedia</a> page:

> The SubRip file format, as reported on the Matroska multimedia container format website, is &#8220;perhaps the most basic of all subtitle formats.&#8221;SubRip (SubRip Text) files are named with the extension .srt, and contain formatted lines of plain text in groups separated by a blank line. Subtitles are numbered sequentially, starting at 1. The timecode format used is hours:minutes:seconds,milliseconds with time units fixed to two zero padded digits and fractions fixed to three zero padded digits (00:00:00,000).

There is a lot more information regarding SubRip available here:

*   <a href="http://www.visualsubsync.org/help/srt" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.visualsubsync.org/help/srt']);">The SRT or Subrip subtitle format</a>
*   <a href="http://videosubtitles.wordpress.com/2012/11/02/subrip-srt-subtitle-format/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://videosubtitles.wordpress.com/2012/11/02/subrip-srt-subtitle-format/']);">SubRip (.srt) subtitle format</a>
*   <a href="http://matroska.org/technical/specs/subtitles/srt.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://matroska.org/technical/specs/subtitles/srt.html']);">SRT Subtitles</a>

So SubRip Format is a text file with the subtitles and timing included (again, overly simplified). There are actually a bunch of other formats. Here is a table from the wikipedia page:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/different_format_of_subtitles.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/different_format_of_subtitles.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/different_format_of_subtitles.png" alt="different format of subtitles Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" width="956" height="516" class="alignnone size-full wp-image-9446" title="Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" /></a>

But I will just be working with **vobsub** and **srt**.

## Merge 2 Avi Files

This part is really easy. You can complete this with either **mencoder**:

    yum install mencoder
    mencoder -ovc copy -oac copy file1.avi file2.avi -o files.avi
    

Or with **transcode**:

    yum install transcode
    avimerge -o files.avi -i file1.avi file2.avi
    

After that you should have one big *Avi* file.

## Convert VobSub (SUB/IDX) files into SRT subtitles with **subtitleripper**

This is actually the difficult part.

### Check for Multiple Subtitle Streams

First we should check if the **VobSub** files have multiple languages. You can do this with either **mediainfo**:

    $mediainfo file1.sub
    General
    Complete name                            : file1.sub
    Format                                   : MPEG-PS
    File size                                : 3.80 MiB
    Duration                                 : 59mn 33s
    Overall bit rate                         : 8 921 bps
    
    Text #1
    ID                                       : 189 (0xBD)-36 (0x24)
    Format                                   : RLE
    Format/Info                              : Run-length encoding
    Muxing mode                              : DVD-Video
    Duration                                 : 59mn 33s
    
    Text #2
    ID                                       : 189 (0xBD)-37 (0x25)
    Format                                   : RLE
    Format/Info                              : Run-length encoding
    Muxing mode                              : DVD-Video
    Duration                                 : 59mn 33s
    

Since we have more than two *texts* that means we have multiple languages in the **VobSub** files. Notice the ID fields: 0&#215;24 and 0&#215;25. We will actually use those later on. You can also use **tcscan** utility to check for the subtitle IDs as well:

    $ tcscan -i file1.sub
    [scan_pes.c] found first packet header at stream offset 0x0
    [scan_pes.c] found private_stream_1 stream [0xbd]
    [scan_pes.c] found padding stream [0xbe]
    [scan_pes.c] end of stream reached
    [scan_pes.c] ------------- presentation unit [0] ---------------
    [scan_pes.c] stream id [0xbd]   1946
    [scan_pes.c] stream id [0xbe]   1572
    [scan_pes.c] 3518 packetized elementary stream(s) PES packets found
    [scan_pes.c] presentation unit PU [0] contains 0 MPEG video sequence(s)
    [scan_pes.c] ---------------------------------------------------
    [scan_pes.c] (scan_pes.c) detected a total of 1 presentation unit(s) PU and 0 sequence(s)
    

Notice again we have two stream IDs: **0xbd** and **0xbe** which **mediainfo** converted for us. If you wanted to find out what language those subtitles correlate to, you can actually use **mplayer** for that. Here is an example:

    $ mplayer -vo null -ao null -frames 0 -identify file1.sub -v  2>/dev/null | grep -E '^ID_VOBSUB_ID' -A 1
    ID_VOBSUB_ID=4
    ID_VSID_4_LANG=en
    --
    ID_VOBSUB_ID=5
    ID_VSID_5_LANG=en
    

We can see that ID 4 (0&#215;24 or 0xbd) is in english (en) and ID 5 (0&#215;25 or 0xbe) is also in english. There is a brief description from <a href="http://forum.doom9.org/archive/index.php/t-89635.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forum.doom9.org/archive/index.php/t-89635.html']);">here</a>, regarding the offset and the value being in hexadecimal:

> The subtitles in MPEG program stream ( = VOB files) use IDs that start at 0&#215;20. tcextract uses those IDs (in fact, tcextract can extract arbitrary streams from PS files). mplayer simply bases its -sid parameter at 0 and adds 0&#215;20 to that value internally when selecting the appropriate stream.

The last method is by checking the **.idx** file. Here is what I saw in mine:

    $ grep ^id file1.idx -B 1
    # English
    id: en, index: 4
    --
    # English
    id: en, index: 5
    

### Extract Subtitle into a Raw Stream with **transcode**

We can use the **tcextract** utility which comes with the **transcode** package to extract the raw stream of the desired subtitle. Here is how that command looked like:

    $ tcextract -i file1.sub -x ps1 -a $((0x20 + 4)) > file1.ps1
    

Now you should have a non-zero sized file:

    $ ls -lh file1.ps1
    -rw-r--r-- 1 elatov elatov 1.2M Aug 29 19:01 file1.ps1
    

### Convert VobSub Subtitle Stream to Images with **subtitleripper**

Now we can use **subtitle2pgm** which is from the **subtitleripper** package to convert the subtitle stream to images. Here is the command for that:

    $ subtitle2pgm -i file1.ps1 -o file1 -P
    ...
    ...
    Generating image: file10786.pgm
    Generating image: file10787.pgm
    Generating image: file10788.pgm
    

For every caption it creates an image. I had this many **pgm** files:

    $ ls *.pgm | wc -l
    788
    

You can take a look and see how the image looks like with the following command:

    $ feh file10788.pgm
    

and it will look something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/feh_after_subtittle2pgm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/feh_after_subtittle2pgm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/feh_after_subtittle2pgm.png" alt="feh after subtittle2pgm Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" width="247" height="36" class="alignnone size-full wp-image-9450" title="Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" /></a>

You will also see a **.srtx** file, this is a description file of the converted images. Here is a snippet from that file:

    $ head file1.srtx
    1
    00:00:59,880 --> 00:01:07,609
    file10001.png.txt
    2
    00:01:07,689 --> 00:01:13,420
    file10002.png.txt
    3
    00:01:13,500 --> 00:01:21,200
    

With the help of **srttool** we will be able to create a single **.srt** file after we have converted the images to text. So first let&#8217;s do that.

### Convert VobSub Caption Images to Text with **tesseract**

Let&#8217;s install **tesseract**:

    $ yum install tesseract
    

Here is what I ran to convert the images to text:

    $ for f in *.pgm ;  do tesseract "$f" "$f" ; done
    

When finished, for every **.pgm** file there was a corresponding **.txt** file, like so:

    $ ls file10788*
    file10788.png  file10788.png.txt
    

Here is the converted text file:

    $ cat file10788.pgm.txt
    Still, he's got style
    

### Combine All the Text Files into an SRT File with **subtitleripper**

Since the **srtx** file (generated from **subtitle2pgm**) contains the timestamps, we can create an appropriate **srt** file from all the text files and the corresponding **.srtx** file. Here is the command to accomplish that:

    $ srttool -s -i file1.srtx -o file1.srt
    

You can confirm the file is okay, by checking out it&#8217;s contents:

    $ tail file1.srt
    787
    01:00:25,039 --> 01:00:26,559
    What the hell's that?
    
    788
    01:00:33,650 --> 01:00:35,510
    Still, he's got style
    

That looks pretty good.

### Clean Up OCR Generated SRT File

Since the OCR conversion is not perfect we should check to make sure the text looks good. You can either do this manually, by running this:

    $ ispell -d american file1.srt
    

or this

    $ aspell -d en -c file1.srt
    

Both will ask you to fix words along the way. Here is how it will look like from the terminal:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/aspell_fix_spelling.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/aspell_fix_spelling.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/aspell_fix_spelling.png" alt="aspell fix spelling Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" width="497" height="381" class="alignnone size-full wp-image-9451" title="Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" /></a>

**subtitleripper** actually provides a **sed** file to do this for us. So we can run this:

    $ sed -f /usr/share/subtitleripper/gocrfilter_en.sed file1.srt > file1_fixed.srt
    

You can check all the changes that it made by checking the differences between the files:

    $ diff file1.srt file1_fixed.srt
    110c110
    < ls that right?
    ---
    > Is that right?
    3353c3353
    < ls his face among
    ---
    > Is his face among
    

the **sed** file doesn&#8217;t do too much, it just searches for common patterns and replaces them. Here are the contents of that file:

    $ cat /usr/share/subtitleripper/gocrfilter_en.sed
    # Replace common gocr mistakes in english language
    # Please use info sed to obtain more information
    # about sed syntax or read
    # http://www.ptug.org/sed/sedfaq.htm
    # 2002-6-18: Modified to use \<..\> word boundaries.
    s/\<l\>/I/g
    s/\<l'll\>/I'll/g
    s/\<ln\>/In/g
    s/\<lt\>/It/g
    s/\<lt's\>/It's/g
    s/\<l've\>/I've/g
    s/\<l'd\>/I'd/g
    s/\<-l\>/-I/g
    s/\<l?\>/I?/g
    s/\<iust\>/just/g
    s/\<ls\>/Is/g
    s/\.iust /.just/g
    s/\<lsrael\>/Israel/g
    s/\<lgrayne\>/Igrayne/g
    s/\<lf\>/If/g
    s/\<l'm\>/I'm/g
    s/\<lt'd\>/It'd/g
    

You can add your own, if think it&#8217;s missing something. Finally just rename the files so we can stay organized:

    $ mv file1.srt file1_after_ocr.srt
    $ mv file1_fixed.srt file1.srt
    

## Convert VobSub (SUB/IDX) files into SRT subtitles with **ogmrip**

There is a similar tool that does the above in less steps, it&#8217;s called **ogmrip**. First let&#8217;s install it:

    $ yum install ogmrip
    

We don&#8217;t need the raw stream, we can just convert from **VobSub** to images directly.

### Convert VobSub to Images with **ogmrip**

Here is the command to do that:

    $ subp2pgm file1 -o file1 -s 4
    788 files generated
    

the **-s** specifies the subtitle ID (so I am picking the first english subtitles). The first *file1* specifies the basename for the **.sub** and **.idx** files. So you need to have *file1.sub* and *file1.idx* in the directory where you run that command from. After that it&#8217;s done you will have the 788 **pgm** images and an **xml** file (similar to the **.srtx** file from **subtitle2pgm** command) for the description file:

    $ ls *.pgm | wc -l
    788
    $ head file1.xml
    <?xml version="1.0" encoding="UTF-8"?>
    <subtitles>
      <subtitle id="1" start="00:00:59.826" stop="00:01:07.562">
        <image>file10001.pgm</image>
      </subtitle>
      <subtitle id="2" start="00:01:07.634" stop="00:01:13.368">
        <image>file10002.pgm</image>
      </subtitle>
      <subtitle id="3" start="00:01:13.440" stop="00:01:21.142">
        <image>file10003.pgm</image>
    

Here is how an example image looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2013/09/feh_after_subp2pgm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/09/feh_after_subp2pgm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/09/feh_after_subp2pgm.png" alt="feh after subp2pgm Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" width="265" height="48" class="alignnone size-full wp-image-9452" title="Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" /></a>

You can see that the images generated from **subtitle2pgm** (from the **subtitleripper** package) didn&#8217;t have a grey outline around the characters, where the images generated from **subp2pgm** do. Actually the **subtitle2p2gm** utility is a little more flexible and allows you to choose the font and background colors. From the **subtitle2pgm** read-me page (**/usr/share/doc/subtitleripper-0.3/README.subtitle2pgm**):

    -c <c0,c1,c2,c3>           Override the default grey levels in output image.
                               Default is 255,255,0,255.  Valid values are in the range
                               0<=c<=255 where 0 is black and 255 white.
    

So in that aspect **subtitle2pgm** (from **subtitleripper**) is a little bit better than **subp2pgm** (from **ogmrip**)

### Convert VobSub Caption Images to Text with **transcode**

We can use another utility called **pgm2txt** (from the **transcode** package), which in turn uses **gocr** to do the OCR conversion.

    $ pgm2txt file1
    

As the conversion starts, it will show you characters that it doesn&#8217;t recognize:

    Converting file10767.pgm into text
    Converting file10768.pgm into text
    
    # show box + environment
    # show box     x=  360    8 d=   3  15 r= 0 0
    # list box char:  |(94) l(92) 1(86) I(57)
    # show pattern x=  335    6 d=  53  19 t= 1 1
    OOO,,,,,,,OOO,,,,,OOO,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    OOO,,,,,,,OOO,,,,,OOOO,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    OOO,,,,,,,,,,,,,,OOOOOO,,###,,,OOO,OOOO,,,,,,,,,,,,,,
    ,OOO,,,,,,,,,,,,,OOOOOO,,###,,,OOOOOOOO,,,,,,,,,,,,,,
    ,OOOOO,,,,,,,,,,,,OOOO,,,###,,,OOOOO,,,,,,,,,,,,,,,,,
    ,,,OOOO,,,,,,,,,,,OOO,,,,###,,,OOOO,,,,,,,,,,,,,,,,,,
    ,,,,OOOO,,,,,,,,,,OOO,,,,###,,,OOOO,,,,,,,,,,,,,,,,,,
    ,,,,,OOOOO,,,,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    ,,,,,,,OOOOO,,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,OOO,,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,OOO,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    ,OO,,,,,,,OOO,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    OOO,,,,,,,OOO,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    OOO,,,,,,,OOO,,,,,OOO,,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    ,OOO,,,,,OOO,,,,,,OOOO,,,###,,,OOO,,,,,,,,,,,,,,,,,,,
    ,OOOOOOOOOOO,,,,,,OOOOO,,###,,,OOO,,,,,,,,,OOO,,,,,,,
    ,,,OOOOOOO,,,,,,,,,OOOO,,###,,,OOO,,,,,,,,,OOO,,,,,,, -
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    ,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,
    The above pattern was not recognized.
    Enter UTF8 char or string for above pattern. Leave empty if unsure.
    Press RET at the end (ALT+RET to store into RAM only):
    

So anything represented by the hash marks (#) it didn&#8217;t recognize. You can fill in the characters that you recognize (in the above example that is the **i** character). After that&#8217;s done, you can check how the text looks like :

    $ cat file10788.pgm.txt
    Still, he's got style.
    

### Combine Converted OCR VobSub Text into a Single SRT with **ogmrip**

Similar to what we did with **srttool** (from the subtitleripper package) and **.srtx** file, we can do with **subptools** (from the **ogmrip** package) and **.xml** file. Here is the command to accomplish that:

    $ subptools --convert srt -i file1.xml -o file1.srt -s
    

We can, of course, check the contents of the resulted **srt** file:

    $ tail file1.srt
    787
    01:00:24,988 --> 01:00:26,512
    What the hell's that?
    
    788
    01:00:33,596 --> 01:00:35,461
    Still, he's got style.
    

And of course you can try to fix common OCR issues with the following:

    $ sed -f /usr/share/subtitleripper/gocrfilter_en.sed file1.srt > file1_fixed.srt
    

I did a side by side comparison of the two SRT files, so I ran the following:

    $ diff tesseract/file1.srt gocr/file1.srt --side-by-side
    

and I saw the following:

    640                                640
    00:48:53,489 --> 00:48:54,510      | 00:48:53,430 --> 00:48:54,454
    Hey, you!                          | Hey, you I
    
    641                                641
    00:48:54,619 --> 00:48:55,840      | 00:48:54,564 --> 00:48:55,792
    I'm talking to you!                | I'm talking to you I
    

**Tesseract** did a little bit better. I did another comparison between **gocr** and **tesseract** (after using **subp2pgm**, instead of using **pgm2txt** I used **tesseract**). Here is what I saw there:

    $ diff --side-by-side ogmrip-tesseract/file1.srt ogmrip-gocr/file1.srt
    4                                        4
    00:01:22,829 --> 00:01:24,194            00:01:22,829 --> 00:01:24,194
    Single file!                             | sin9ie fiiei.
    
    5                                        5
    00:01:48,721 --> 00:01:51,417            00:01:48,721 --> 00:01:51,417
    Miss, did a strange man                  Miss, did a strange man
    just run past here?                      | j-ust run past here?
    
    6                                        6
    00:01:51,524 --> 00:01:54,322            00:01:51,524 --> 00:01:54,322
                                             | No
                                             <
    

It looks like **gocr** does better with single words (you can see the bottom one, **tesseract** didn&#8217;t recognize the &#8216;No&#8217;, since it&#8217;s just a single word). While **tesseract** does better with long sentences (ie &#8216;just run&#8217; vs &#8216;j-ust run&#8217;). I saw other similar conversions/mistakes.

## Convert VobSub (SUB/IDX) Files into SRT subtitles with **vobsub2srt**

There is another tool that was recently released that does all the above in one swoop. It wasn&#8217;t part of the *yum* repository so I compiled it manually.

### Install VobSub2SRT

First get the prerequisites:

    $ yum install tesseract tesseract-devel cmake libtiff-devel
    

Then get the source:

    $ mkdir vb; cd vb
    $ git clone https://github.com/ruediger/VobSub2SRT.git
    $ cd VobSub2SRT
    

Configure the package:

    ./configure -DCMAKE_INSTALL_PREFIX:PATH=/usr/local/vobsub2srt
    

Prepare the destination folder:

    $ sudo mkdir /usr/local/vobsub2srt
    $ sudo chown elatov:elatov /usr/local/vobsub2srt
    

Then build and install the package

    $ make
    $ make install
    

### Convert VobSub to SRT

Here is the command to do that:

    $ vobsub2srt --lang en file1
    Selected VOBSUB language: 4 language: en
    spudec: Error determining control type 0x38.  Skipping -6 bytes.
    SPUasm: packet too short
    Wrote Subtitles to 'file1.srt'
    

The recognition was the best on **vobsub2srt** (even though both **vobsub2srt** and **subtitle2pgm** use **tesseract**). Here are some small differences that I saw:

    $ diff --side-by-side vobsub/file1.srt subrip/file1.srt
    36                                   36
    00:05:11,711 --> 00:05:14,942        | 00:05:11,769 --> 00:05:15,000
    well...                              | we
    
    164                                  164
    00:13:58,938 --> 00:14:00,235        | 00:13:58,990 --> 00:14:00,279
    Hey, hey-~                           | Hey,he¥
    

But **subtitleripper** (**subtitle2pgm**) ended up getting more captions. If you remember above we had 788 captions, but with **vobsub2srt**, I ended up with only 786 (still really good):

    $ tail file1.srt
    785
    01:00:24,988 --> 01:00:26,512
    What the hell's that?
    786
    01:00:33,596 --> 01:00:35,461
    Still, he's got style.
    

It looks like it skipped two captions.

## Merge 2 SRT into a Single SRT file

This one isn&#8217;t that bad. After you converted from **vobsub** to **srt**, you should have the following files in the end:

    $ ls
    file1.avi   file1.srt   file2.avi  file1.srt
    file1.idx   file1.srtx  file2.idx  file2.srtx
    file1.ps1   file1.sub   file2.ps1  file2.sub
    

After the conversion, I saw the following for the second **.srt** file:

    $ head file2.srt
    1
    01:03:03,840 --> 01:03:04,820
    Stop there!
    2
    01:03:06,809 -- 01:03:07,789
    Hey, you!
    

Since the time was correct we can just concatenate the file together like so:

    $ cat file1.srt file2.srt > files.srt
    

You will notice the gap in caption number if you look inside the file:

    $ grep ^788 -A 10 files.srt
    788
    01:00:33,650 --> 01:00:35,510
    Still, he's got style
    1
    01:03:03,840 --> 01:03:04,820
    Stop there!
    2
    01:03:06,809 --> 01:03:07,789
    Hey, you!
    

So we can just renumber our caption IDs, like so:

    $ srttool -r -i files.srt -o files-sorted.srt
    

After that is done, there should be no gap in the IDs:

    $ grep ^788 -A 10 files-sorted.srt
    788
    01:00:33,650 --> 01:00:35,510
    Still, he's got style
    789
    01:03:03,840 --> 01:03:04,820
    Stop there!
    790
    01:03:06,809 --> 01:03:07,789
    Hey, you!
    

Later on, I got a good version of the **SRT** file and I wanted to compare the times from caption *788* to *789*. So I ran the following:

    $ grep '^Stop there' files-sorted.srt -B 1
    01:03:03,840 --> 01:03:04,820
    Stop there!
    $ grep '^Stop there' files-good.srt -B 1
    01:03:03,779 --> 01:03:04,768
    Stop there!
    

Notice the times are off by a millisecond, this is great. If it&#8217;s too far off you can use the subtitle delay functionality from the video player (**vlc** and **mplayer** both offer this).

## Adjusting the Time in the SRT File

If your second **.srt** file started from the beginning ie (00:00:00 and not from end of the first file). When I used **vobsub2srt** on the second file, the resulted file started with the following numbers:

    $ head file2.srt
    1
    00:00:55,335 --> 00:00:56,324
    Stop there!
    
    2
    00:00:58,304 --> 00:00:59,293
    Hey, you!
    

To adjust the time we can do the following.

### Determine Length of Movie

You can use **mediainfo** for this, like so:

    $ mediainfo -f --Inform="General;%Duration%" file1.avi
    3728475
    

that output is in milliseconds, but you can just move the decimal point by 3. Another way is using the **ffprobe** command, that comes with the **ffmpeg** package. Here is how that looks like:

    $ ffprobe -show_format file1.avi 2>&1 | grep ^duration
    duration=3728.478478
    

### Use **srttool** to Adjust the Time of the Subtitles Inside an SRT file

Now that we know the duration of the first movie, let&#8217;s adjust the times in the second **SRT** file by adding the duration of the first one. Here is the command for that:

    $ srttool -d 3728 -i file2.srt -o file2-adjusted.srt
    

Now we can just concatenate them both and reset the caption ids:

    $ cat file1.srt file2-adjusted.srt > files.srt
    $ srttool -r -i files.srt -o files-sorted.srt
    

That&#8217;s it <img src="http://virtuallyhyper.com/wp-includes/images/smilies/icon_smile.gif" alt="icon smile Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" class="wp-smiley" title="Combine VobSub (sub/idx) Format Subtitles into a Single SubRip (srt) Format File" /> As a side note, you could play the media files and include the **vobsub** subtitles like so:

    $ mplayer file1.avi -vobsub file1 -vobsubid 4
    $ vlc file1.avi --sub-file file1.sub
    

