---
title: Recover Files from an SD Card Using Linux Utilities
author: Karim Elatov
layout: post
permalink: /2012/11/recover-files-from-an-sd-card-using-linux-utilities/
dsq_thread_id:
  - 1406057191
categories:
  - OS
tags:
  - ./configure
  - /dev/mmcblk0
  - bash
  - dd
  - fdisk
  - ffind
  - fls
  - ForeMost
  - fsstat
  - ils
  - MagicRescue
  - make
  - make install
  - photorec
  - sd card
  - Sleuth Kit
  - testdisk
  - tsk_recover
  - yum
---
I recently dropped my phone and right after I picked it back up the Android OS has been unable to see the contents of the SD Card. I had a couple of photos on there that I really wanted to keep. Luckily my laptop had an SD Card Reader and I had a Micro-SD to SD Converter from my previous efforts to transfer data to my phone. I plugged the SD card into my laptop and I saw the device without issues:

	  
	$ dmesg | tail -3  
	[ 818.930343] mmc0: new high speed SD card at address 0002  
	[ 818.994537] mmcblk0: mmc0:0002 00000 974 MiB (ro)  
	[ 818.996066] mmcblk0: p1  
	

Also checking out *fdisk*, I saw the following:

	  
	$ fdisk -l /dev/mmcblk0
	
	Disk /dev/mmcblk0: 1021 MB, 1021837312 bytes  
	256 heads, 63 sectors/track, 123 cylinders, total 1995776 sectors  
	Units = sectors of 1 * 512 = 512 bytes  
	Sector size (logical/physical): 512 bytes / 512 bytes  
	I/O size (minimum/optimal): 512 bytes / 512 bytes  
	Disk identifier: 0x69737369
	
	Device Boot Start End Blocks Id System  
	/dev/mmcblk0p1 * 2048 1995775 996864 c Unknown  
	

Before I did anything with the card, I wanted to create a disk image of the SD Card. Here is what I ran to accomplish this:

	  
	$ dd if=/dev/mmcblk0 of=sd.img  
	1995776+0 records in  
	1995776+0 records out  
	1021837312 bytes (1.0 GB) copied, 72.4206 s, 14.1 MB/s  
	

Then after doing some research I decided to try out two utilities. One is called "<a href="http://www.cgsecurity.org/wiki/PhotoRec" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cgsecurity.org/wiki/PhotoRec']);">PhotoRec</a>" (it's part of an application called "<a href="http://www.cgsecurity.org/wiki/TestDisk" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cgsecurity.org/wiki/TestDisk']);">TestDisk</a>"), the other is called "<a href="http://www.sleuthkit.org/sleuthkit/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.sleuthkit.org/sleuthkit/']);">Sleuth Kit</a>". The first one was available in the yum repositories:

	  
	$ yum search photorec  
	Loaded plugins: presto, refresh-packagekit  
	updates | 4.7 kB 00:00  
	updates/primary_db | 5.5 MB 00:04  
	updates/pkgtags | 331 B 00:00  
	============================ N/S Matched: photorec =============================  
	testdisk.i686 : Tool to check and undelete partition, PhotoRec recovers lost  
	: files
	
	Name and summary matches only, use "search all" for everything.  
	

To install the package I ran the following:

	  
	$ sudo yum install testdisk  
	Loaded plugins: presto, refresh-packagekit  
	adobe-linux-i386 | 951 B 00:00  
	fedora/17/i386/metalink | 19 kB 00:00  
	updates/17/i386/metalink | 12 kB 00:00  
	updates | 4.7 kB 00:00  
	updates/primary_db | 5.5 MB 00:02  
	Resolving Dependencies  
	--> Running transaction check  
	--> Package testdisk.i686 0:6.13-1.fc17 will be installed  
	--> Finished Dependency Resolution
	
	Dependencies Resolved
	
	================================================================================  
	Package Arch Version Repository Size  
	================================================================================  
	Installing:  
	testdisk i686 6.13-1.fc17 fedora 368 k
	
	Transaction Summary  
	================================================================================  
	Install 1 Package
	
	Total download size: 368 k  
	Installed size: 1.3 M  
	Is this ok [y/N]: y  
	Downloading Packages:  
	testdisk-6.13-1.fc17.i686.rpm | 368 kB 00:00  
	Running Transaction Check  
	Running Transaction Test  
	Transaction Test Succeeded  
	Running Transaction  
	Installing : testdisk-6.13-1.fc17.i686 1/1  
	Verifying : testdisk-6.13-1.fc17.i686 1/1 
	
	Installed:  
	testdisk.i686 0:6.13-1.fc17 
	
	Complete!  
	

The application is GUI driven but to launch it, here is what I ran:

	  
	$ photorec sd.img  
	

Here is how it looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photo_rec_screen_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photo_rec_screen_1.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photo_rec_screen_1.png" alt="photo rec screen 1 Recover Files from an SD Card Using Linux Utilities" title="photo_rec_screen_1" width="735" height="455" class="alignnone size-full wp-image-4861" /></a>

After I selected 'proceed', I saw a screen which determined my partition type:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_part_window.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_part_window.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_part_window.png" alt="photorec part window Recover Files from an SD Card Using Linux Utilities" title="photorec_part_window" width="735" height="455" class="alignnone size-full wp-image-4868" /></a>

From here you can go to 'File Opt' and select what files to search for, but since it was just a 1GB SD Card, I decided to recover as much as possible. So I just selected 'search':

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_screen_3.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_screen_3.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_screen_3.png" alt="photorec screen 3 Recover Files from an SD Card Using Linux Utilities" title="photorec_screen_3" width="735" height="455" class="alignnone size-full wp-image-4869" /></a>

At this screen it's asking you to choose the partition type. My SD Card used to be Fat32, so I selected the 'other' option:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_free_vs_whole.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_free_vs_whole.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_free_vs_whole.png" alt="photorec free vs whole Recover Files from an SD Card Using Linux Utilities" title="photorec_free_vs_whole" width="735" height="455" class="alignnone size-full wp-image-4870" /></a>

Usually deleted files reside in the free unallocated space, but again since this was a 1GB image, I decided to search all the space. So I selected 'whole':

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_select_dir.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_select_dir.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_select_dir.png" alt="photorec select dir Recover Files from an SD Card Using Linux Utilities" title="photorec_select_dir" width="735" height="455" class="alignnone size-full wp-image-4872" /></a>

This next screen asked the output directory to save the recovered files to. Before launching photorec, I created a folder called 'recovery', so I scrolled down to that folder and then typed 'C'. After I did that, the recovery process started and here is how it looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_progress.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_progress.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_progress.png" alt="photorec progress Recover Files from an SD Card Using Linux Utilities" title="photorec_progress" width="735" height="455" class="alignnone size-full wp-image-4873" /></a>

After the process finished I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_recovery_finished.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_recovery_finished.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/photorec_recovery_finished.png" alt="photorec recovery finished Recover Files from an SD Card Using Linux Utilities" title="photorec_recovery_finished" width="735" height="455" class="alignnone size-full wp-image-4874" /></a>

So it recovered 426 file total, I then quit the program and went to check out the contents of '~/recovery/recup_dir.1':

	  
	$ ls  
	f0021929.mp3 f0885289.mp3 f0992873.png f1013961.png f1045577.png  
	f0036649.mp3 f0897513.mp3 f0992905.png f1014025.png f1045609.png  
	f0058021.png f0923049.mp3 f0993001.png f1014153.png f1045705.png  
	f0058286.png f0945641.mp3 f0993033.png f1014217.png f1045769.png  
	f0058322_assets.zip f0961065.mp3 f0993257.png f1014281.png f1045865.png  
	f0063657.mp3 f0968137.mp3 f0994473.png f1014377.png f1045993.png  
	f0071945.mp3 f0968193.mp3 f0994505.png f1014441.png f1046089.png  
	f0081097.mp3 f0978697.jpg f0994601.png f1014473.jar f1046121.png  
	f0097545.mp3 f0979401.jpg f0994660.txt f1015497.png f1046217.png  
	f0098241.mp3 f0979753.jpg f0994697.png f1015561.mp3 f1046281.png  
	f0113033.mp3 f0982759.mp3 f0994801.mp3 f1015593.png f1046345.png  
	f0125705.mp3 f0982852.txt f0994825.png f1015625.png f1046409.png  
	f0135881.jpg f0982897.mp3 f0995945.jpg f1015721.png f1046473.png  
	f0135913.jpg f0983272.mp3 f0996457.jpg f1015817.png f1046537.png  
	f0135945.jpg f0983371.mp3 f0997257.jpg f1015881.png f1046633.png  
	f0135977.jpg f0983423.mp3 f0997673.jpg f1015913.png f1046665.png  
	f0136009.jpg f0983804.mp3 f0998505.jpg f1015945.png f1046761.png  
	f0136073.jpg f0985289.sqlite f0998953.png f1016041.jar f1046793.png  
	f0136137.jpg f0985481.png f0999017.png f1016873.png f1046889.png  
	f0136201.jpg f0985577.png f0999049.png f1016905.png f1046953.png  
	

The recovery process recovered the file by the inode number and just stored everything in the 'recup_dir' folder. Checking out how many jpeg files it recovered, I saw the following:

	  
	$ find recovery/ -name '*.jpg' | wc -l  
	61  
	

There was a couple of duplicates but that was okay. I was pretty impressed with the results. 

Next I wanted to try out Sleuth Kit. Unfortunately that application is not in the yum repositories, so I had to compile it myself. I first downloaded the source:

	  
	$ ls sleu*  
	sleuthkit-4.0.1.tar.gz  
	

I then extracted the source:

	  
	$ tar xzvf sleuthkit-4.0.1.tar.gz  
	sleuthkit-4.0.1/  
	sleuthkit-4.0.1/aclocal.m4  
	sleuthkit-4.0.1/bindings/  
	sleuthkit-4.0.1/ChangeLog.txt  
	sleuthkit-4.0.1/config/  
	sleuthkit-4.0.1/configure  
	...  
	...  
	sleuthkit-4.0.1/bindings/java/doxygen/Doxyfile  
	sleuthkit-4.0.1/bindings/java/doxygen/main.dox  
	

I never like running 'sudo make install', so I created a folder under */usr/local* and gave myself permission to that folder:

	  
	$ sudo mkdir /usr/local/sleuthkit  
	$ sudo chown elatov:elatov /usr/local/sleuthkit  
	

I then configured the package to install into my newly created directory:

	  
	$ cd sleuthkit-4.0.1/  
	$ ./configure --prefix=/usr/local/sleuthkit  
	checking for a BSD-compatible install... /usr/bin/install -c  
	checking whether build environment is sane... yes  
	checking for a thread-safe mkdir -p... /usr/bin/mkdir -p  
	checking for gawk... gawk  
	...  
	...  
	config.status: executing depfiles commands  
	config.status: executing libtool commands  
	config.status: executing tsk3/tsk_incs.h commands  
	

The configure process didn't fail so then I decided to build/make the application:

	  
	$ make -j 4  
	Making all in tsk3  
	make[1]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/tsk3'  
	make all-recursive  
	make[2]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/tsk3'  
	Making all in base  
	make[3]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/tsk3/base'  
	/bin/sh ../../libtool --tag=CC --mode=compile gcc -DHAVE_CONFIG_H -I. -I../../tsk3 -I../.. -Wall -g -O2 -pthread -I/usr/local/include -MT md5c.lo -MD -MP -MF .deps/md5c.Tpo -c -o md5c.lo md5c.c  
	...  
	...  
	libtool: link: g++ -g -O2 -pthread -o posix_cpp_style posix-cpp-style.o -L/usr/local/lib ../tsk3/.libs/libtsk3.a -ldl -lz -pthread  
	make[1]: Leaving directory '/home/elatov/downloads/sleuthkit-4.0.1/samples'  
	Making all in man  
	make[1]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/man'  
	make[1]: Nothing to be done for 'all'.  
	make[1]: Leaving directory '/home/elatov/downloads/sleuthkit-4.0.1/man'  
	make[1]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1'  
	make[1]: Nothing to be done for 'all-am'.  
	make[1]: Leaving directory '/home/elatov/downloads/sleuthkit-4.0.1'  
	

So the compile finished with success as well, which is always good news. I then installed the package:

	  
	$ make install  
	Making install in tsk3  
	make[1]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/tsk3'  
	Making install in base  
	make[2]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/tsk3/base'  
	make[3]: Entering directory '/home/elatov/downloads/sleuthkit-4.0.1/tsk3/base'  
	make[3]: Nothing to be done for 'install-exec-am'.  
	make[3]: Nothing to be done for 'install-data-am'.  
	...  
	...  
	/bin/sh /home/elatov/downloads/sleuthkit-4.0.1/config/install-sh -c -m 644 'tsk3/auto/tsk_auto.h' '/usr/local/sleuthkit/include/tsk3/auto/tsk_auto.h'  
	make[2]: Leaving directory '/home/elatov/downloads/sleuthkit-4.0.1'  
	make[1]: Leaving directory '/home/elatov/downloads/sleuthkit-4.0.1'  
	

That finished without issue also. I then checked out the contents of the package and it looked like this:

	  
	$ ls -l /usr/local/sleuthkit/  
	total 16  
	drwxrwxr-x 2 elatov elatov 4096 Nov 18 10:06 bin  
	drwxrwxr-x 3 elatov elatov 4096 Nov 18 10:06 include  
	drwxrwxr-x 2 elatov elatov 4096 Nov 18 10:06 lib  
	drwxrwxr-x 4 elatov elatov 4096 Nov 18 10:06 share  
	

So this was a pretty standard install, *bin* is where all the binaries reside, *include* is where the header files are, *lib* is for static or shared libraries, and lastly *share* is where the documentation is located. Here is a list of all the binaries:

	  
	$ ls /usr/local/sleuthkit/bin  
	blkcalc fcat hfind img_cat jls mmstat tsk_comparedir  
	blkcat ffind icat img_stat mactime sigfind tsk_gettimes  
	blkls fls ifind istat mmcat sorter tsk_loaddb  
	blkstat fsstat ils jcat mmls srch_strings tsk_recover  
	

If you want to find out what each command does you can check out the man page in the following manner:

	  
	$ man -M /usr/local/sleuthkit/share/man/ fls  
	

After checking out the man pages, and some documentation online I realized I can check out the files on an image by running *fls*, like so:

	  
	$ /usr/local/sleuthkit/bin/fls -r -p sd.img | less  
	d/d 2172934: dcim/Camera  
	r/r 2173447: dcim/Camera/1232307374107.jpg  
	r/r 2173450: dcim/Camera/1232328935754.jpg  
	r/r 2173453: dcim/Camera/1234505181782.jpg  
	r/r 2173456: dcim/Camera/1226525485803.jpg  
	r/r 2173459: dcim/Camera/1238175243749.jpg  
	r/r 2173462: dcim/Camera/20090317205732.jpg  
	r/r 2173465: dcim/Camera/20090317205749.jpg  
	r/r 2173468: dcim/Camera/1238175807932.jpg  
	r/r 2173471: dcim/Camera/1238176478351.jpg  
	r/r 2173474: dcim/Camera/1238193400644.jpg  
	r/r * 2173477: dcim/Camera/1229791492195.jpg  
	r/r * 2173480: dcim/Camera/1230047324210.jpg  
	

This lists the inode number, full path of the file and the file name. That was pretty cool. Also notice the star (*) next to some files, that means it's a deleted file. If you want, you can also list all the inodes in the image by running *ils*. Here is how it looks like:

	  
	$ /usr/local/sleuthkit/bin/ils sd.img | less  
	class|host|device|start_time  
	ils|klaptop||1353505471  
	st_ino|st_alloc|st_uid|st_gid|st_mtime|st_atime|st_ctime|st_crtime|st_mode|st_nlink|st_size  
	10|f|0|0|1226207720|1226127600|0|1226207720|777|0|16384  
	20|f|0|0|1239120060|1239084000|0|1239120060|777|0|0  
	565|f|0|0|1226207530|1226127600|0|1226207530|777|0|16384  
	2165254|f|0|0|1226209944|1233903600|0|1226209944|777|0|13193  
	2165256|f|0|0|1226209948|1233903600|0|1226209948|777|0|15410  
	2165258|f|0|0|1226209952|1237442400|0|1226209952|777|0|11310  
	

To recover a file you can run *icat*. For example let's say I wanted to recover ' dcim/Camera/1229791492195.jpg' from the above output. We know the inode number of that file is '2173480'. To recover that file, I would run the following:

	  
	$ /usr/local/sleuthkit/bin/icat -r sd.img 2173480 > 1229791492195.jpg  
	

If you know the inode number, then you can use *ffind* to find the exact location of that file on the file system. Here is an example:

	  
	$ /usr/local/sleuthkit/bin/ffind -a sd.img 2173480  
	* /dcim/Camera/1230047324210.jpg  
	

You can also get file system information by running *fsstat* like so:

	  
	$ /usr/local/sleuthkit/bin/fsstat sd.img | less  
	FILE SYSTEM INFORMATION  
	--------------------------------------------  
	File System Type: FAT16
	
	OEM Name: MSDOS5.0  
	Volume ID: 0x28784dda  
	Volume Label (Boot Sector): NO NAME  
	Volume Label (Root Directory):  
	File System Type Label: FAT16 
	
	Sectors before file system: 0
	
	File System Layout (in sectors)  
	Total Range: 0 - 1995775  
	* Reserved: 0 - 0  
	** Boot Sector: 0  
	* FAT 0: 1 - 244  
	* FAT 1: 245 - 488  
	* Data Area: 489 - 1995775  
	** Root Directory: 489 - 520  
	** Cluster Area: 521 - 1995752  
	** Non-clustered: 1995753 - 1995775  
	

Basically there are a lot of cool tools that allow you to check files and file system information at a lower level. There a lot of cool examples on the '<a href="http://wiki.sleuthkit.org/index.php?title=FS_Analysis" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.sleuthkit.org/index.php?title=FS_Analysis']);">FS Analysis</a>' page. 

Now I wanted to recover all the files. I ran into a couple of other links: '<a href="http://forums.gentoo.org/viewtopic-t-365703.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forums.gentoo.org/viewtopic-t-365703.html']);">Recovering files with "The Sleuth Kit"</a>' and '<a href="http://matt.matzi.org.uk/2008/07/03/reconstructing-heavily-damaged-hard-drives/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://matt.matzi.org.uk/2008/07/03/reconstructing-heavily-damaged-hard-drives/']);">Reconstructing Heavily Damaged Hard Drives</a>'. Both had their own scripts, so I borrowed most of the content and wrote my own. Here is how it looked like:

	  
	#!/bin/bash  
	# make sure 2 arguments are passed into the script  
	if [ $# -ne 2 ]; then  
	echo "supply image name and output directory name"  
	echo "ex: $0 /path/to/filesystem.img output/dir";  
	exit 1;  
	fi
	
	# Take in passed in arguments  
	IMG_FILE=$1;  
	OUTPUT_DIR=$2;
	
	# make sure Img and Directory exist  
	if [ ! -f $IMG_FILE ]; then  
	echo "Image File $IMG_FILE doesn't exist";  
	exit 1  
	fi
	
	if [ ! -d $OUTPUT_DIR ]; then  
	echo "Directory $OUTPUT_DIR doesn't exist";  
	exit 1  
	fi 
	
	# Read in the output of the fls command (part of sleuthkit)  
	/usr/local/sleuthkit/bin/fls -r -p $IMG_FILE |  
	while read line  
	do  
	# Read in 3 different variables  
	file_type='echo "$line" | awk {'print $1'}'  
	inode_number='echo "$line" | cut -d : -f 1 |awk {'print $NF'}'  
	inode_number=${inode_number%:}  
	file_name='echo "$line" | cut -f 2'
	
	#un-comment below to see what files will be recovered  
	#echo "$file_type"  
	#echo "$inode_number"  
	#echo "$file_name"
	
	# If a directory, then create it  
	if [ $file_type == "d/d" ]; then  
	mkdir -p $OUTPUT_DIR/"$file_name"  
	# Else it's a file, so recover the file to output directory  
	else  
	/usr/local/sleuthkit/bin/icat -r $IMG_FILE "$inode_number" > $OUTPUT_DIR/"$file_name"  
	fi  
	done  
	

So I ran the following to recover all the files:

	  
	$ mkdir test  
	$ ./rec_all.bash sd.img test  
	

Now checking out the contents of my output directory, I saw the following:

	  
	$ ls test  
	albumthumbs andnav2 download $FAT2 $MBR nylinda.com power_manager  
	amazonmp3 dcim $FAT1 l Music $OrphanFiles  
	

Checking out how many files I recovered, I saw the following:

	  
	$ find test | wc -l  
	510  
	

Checking out how many jpeg files I got, I saw the following:

	  
	$ find test -name "*.jpg" | wc -l  
	69  
	

Very similar results, but the recovered files had the same folder structure as the original file system, and I really liked that. After running that script, I realized that Sleuth Kit comes with a tool to recover all the files; it's called *tsk_recover*. From the man page:

	  
	$ man -M /usr/local/sleuthkit/share/man/ tsk_recover  
	TSK_RECOVER(1) TSK_RECOVER(1)
	
	NAME  
	tsk_recover - Export files from an image into a local directory
	
	

So then I ran the following:

	  
	$ mkdir test2  
	$ /usr/local/sleuthkit/bin/tsk_recover -e sd.img test2  
	Files Recovered: 380  
	

It had recovered less files than my script (380 vs 510), then checking out how many jpeg files I have:

	  
	$ find test2 -name "*.jpg"| wc -l  
	69  
	

it was the same amount. It turned out that the *tsk_recover* doesn't recover zero sized files, cause they are basically empty files, but my script wasn't that smart and just recovered everything it sees. Regardless to say, I was pretty happy with the tool as well.

After doing some research I found two more tools: <a href="http://www.itu.dk/people/jobr/magicrescue/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.itu.dk/people/jobr/magicrescue/']);">MagicRescue</a> and <a href="http://foremost.sourceforge.net/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://foremost.sourceforge.net/']);">foremost</a>. MagicRescue is no longer maintained, but I decided to give it a try. MagicRescue uses "recipes", or file signatures as I would call them, to identify a certain file type that you are looking for. The application comes with some pre-installed recipes. For example, here is what I ran to recover all the jpeg files from my image:

	  
	$ /usr/local/magicrescue/bin/magicrescue -r jpeg-jfif -r jpeg-exif -d ~/output sd.img  
	Found jpeg-jfif at 0x54D337  
	/home/elatov/output/00000054D337-0.jpg: 255236 bytes  
	Found jpeg-jfif at 0xAB53BA  
	..  
	..  
	/home/elatov/output/000020A45200-0.jpg: 27075 bytes  
	Scanning sd.img finished at 974MB  
	

Checking out the output, I saw the following:

	  
	$ ls output  
	00000054D337-0.jpg 00001DE3EE4D-0.jpg 00001E725200-0.jpg 00001F5A59CD-0.jpg  
	000000AB53BA-0.jpg 00001DE4B19D-0.jpg 00001E78D200-0.jpg 00001F5F5200-0.jpg  
	0000011E53DF-0.jpg 00001DE65200-0.jpg 00001E7C229D-0.jpg 00001F731200-0.jpg  
	0000018894CE-0.jpg 00001DE9555D-0.jpg 00001E7C49AD-0.jpg 00001F8BA93D-0.jpg  
	000001F15379-0.jpg 00001DE97C6D-0.jpg 00001E8BBBD0-0.jpg 00001F8BD200-0.jpg  
	00000232144D-0.jpg 00001DEE58AD-0.jpg 00001E8BF0BD-0.jpg 00001FA25200-0.jpg  
	0000027992AF-0.jpg 00001DF28B2A-0.jpg 00001E8C1200-0.jpg 00001FA71200-0.jpg  
	000002FA12BC-0.jpg 00001DF29ECA-0.jpg 00001E921200-0.jpg 00001FBD9200-0.jpg  
	000003731441-0.jpg 00001DF2B257-0.jpg 00001E9522FD-0.jpg 00001FC0775D-0.jpg  
	000003D61315-0.jpg 00001DF9A37D-0.jpg 00001EBA3BD0-0.jpg 00001FDC729F-0.jpg  
	000004259200-0.jpg 00001E10A6CD-0.jpg 00001EBA4F70-0.jpg 00001FDC863F-0.jpg  
	00000425D200-0.jpg 00001E1774ED-0.jpg 00001EBA62FD-0.jpg 00001FDC99CC-0.jpg  
	000004261200-0.jpg 00001E215200-0.jpg 00001EDE17CD-0.jpg 0000200F9200-0.jpg  
	000004265200-0.jpg 00001E269200-0.jpg 00001EDE3EDD-0.jpg 0000202F9200-0.jpg  
	000004269200-0.jpg 00001E275BFD-0.jpg 00001EEF25ED-0.jpg 00002045729F-0.jpg  
	

Checking out the count, I saw the following:

	  
	$ find output | wc -l  
	113  
	

Which was more than any other application that I used above, but the man page also recommends running *dupemap* to get rid of duplicates. I didn't compile that into my version, so I couldn't run it. But checking out the pictures, it actually did find a couple of more pictures than the previous two. 

Lastly running foremost. Foremost comes with a configuration file under */usr/local/foremost/etc/foremost.conf* (or where ever you decided to install the application). Inside that file there are patterns of different file types, for example I un-commented the following lines to search only for jpeg files:

	  
	jpg y 20000000 \xff\xd8\xff\xe0\x00\x10 \xff\xd9  
	jpg y 20000000 \xff\xd8\xff\xe1 \xff\xd9  
	jpg y 20000000 \xff\xd8 \xff\xd9  
	

Then running the program:

	  
	$ mkdir test3  
	$ /usr/local/foremost/bin/foremost -v -o test3 sd.img  
	Foremost version 1.5.7 by Jesse Kornblum, Kris Kendall, and Nick Mikus  
	Audit File
	
	Foremost started at Wed Nov 21 07:57:29 2012  
	Invocation: /usr/local/foremost/bin/foremost -v -o test3 sd.img  
	Output directory: /home/elatov/test3  
	Configuration file: /usr/local/foremost/etc/foremost.conf  
	------------------------------------------------------------------  
	File: sd.img  
	Start: Wed Nov 21 07:57:29 2012  
	Length: 974 MB (1021837312 bytes)
	
	Num Name (bs=512) Size File Offset Comment 
	
	0: 00010857.jpg 249 KB 5559095  
	1: 00021929.jpg 6 KB 11228090  
	2: 00021931.jpg 5 KB 11228912  
	...  
	...  
	7900: 01066249_1.jpg 51 KB 545919488  
	7901: 01066250.jpg 50 KB 545920112  
	7902: 01069609_1.jpg 26 KB 547639808  
	Finish: Wed Nov 21 07:57:46 2012
	
	7903 FILES EXTRACTED
	
	jpg:= 113  
	jpg:= 22  
	jpg:= 7768  
	------------------------------------------------------------------
	
	Foremost finished at Wed Nov 21 07:57:46 2012  
	

if you don't want to use the configuration file, you can specify what file types to search for, like this:

	  
	$ /usr/local/foremost/bin/foremost -v -t jpg -o test3 sd.img  
	

If you want to know the supported file types just check out the man page:

	  
	$ man -M /usr/local/foremost/share/man/ foremost  
	

Or you can just run the following:

	  
	$ /usr/local/foremost/bin/foremost -v -t all -o test3 sd.img  
	

and that will recover all the files.

Foremost recovered the most amount of jpeg files (7903), but most of them were unreadable. I would say it recovered maybe 1 or 2 more actual readable jpeg files than the rest.

In conclusion, there are a lot of recovery tools out there, so pick your poison:) I personally liked Sleuth Kit for recovery in general, it provided a lot of granular tools. For recovering specific type of files, each (photorec, magicrescue, and foremost) program had their own quirks. Foremost recovered the most but it took a while to manually sit and figure out which one is a valid picture. MagicRescue was good, but it didn't have that many built in recipes. PhotoRec was the easiest to use but it recovered the least amount of pictures but a lot of mp3 files :) I ran all of them and I was pleased with each one in different ways. So if you are looking for pictures in a disk image just run them all and then sort out the pictures as necessary. I will end with a quote from the man page of <a href="http://www.itu.dk/people/jobr/magicrescue/manpage.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.itu.dk/people/jobr/magicrescue/manpage.html']);">MagicRescue</a>:

> **When not to use MagicRescue**
> 
> Magic Rescue is not meant to be a universal application for file recovery. It will give good results when you are extracting known file types from an unusable file system, but for many other cases there are better tools available.
> 
> If there are intact partitions present somewhere, use gpart to find them.
> 
> If file system's internal data structures are more or less undamaged, use The Sleuth Kit. At the time of writing, it only supports NTFS, FAT, ext[23] and FFS, though.
> 
> If you are just looking for a handful of text files, your best option is most likely to search through the block device with a hex editor such as hexedit.
> 
> If Magic Rescue does not have a recipe for the file type you are trying to recover, try foremost instead. It recognizes more file types, but in most cases it extracts them simply by copying out a fixed number of bytes after it has found the start of the file. This makes post-processing the output files more difficult.
> 
> In many cases you will want to use Magic Rescue in addition to the tools mentioned above. They are not mutually exclusive, e.g. combining magicrescue with dls from The Sleuth Kit could give good results. In many cases you'll want to use magicrescue to extract its known file types and another utility to extract the rest. 

So try everything out and see what works best :) 

