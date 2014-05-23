---
title: Decrease DMG Size to Fit on a Single Layer DVD
author: Karim Elatov
layout: post
permalink: /2013/07/decrease-dmg-size-to-fit-on-a-single-layer-dvd/
dsq_thread_id:
  - 1523376242
categories:
  - Home Lab
  - OS
tags:
  - hdiutil
  - Mac OS X
  - Sparse Image
---
I wanted to create a recovery DVD for my Mac OS X install and all I had was an old DMG of Mac OS X version 10.6.

### hdiutil Image Information

Here is the information regarding the DMG file:

    kelatov@kmac:~$hdiutil imageinfo OS_X-10.6.dmg
    Format Description: UDIF read-only compressed (zlib)
    Class Name: CUDIFDiskImage
    Checksum Type: CRC32
    Size Information:
        Compressed Ratio: 0.84183833618791892
        Total Empty Bytes: 83627520
        Sector Count: 13158216
        Total Bytes: 6737006592
        CUDIFEncoding-bytes-wasted: 0
        Total Non-Empty Bytes: 6653379072
        CUDIFEncoding-bytes-in-use: 5601069940
        Compressed Bytes: 5601069940
        CUDIFEncoding-bytes-total: 5601069940
    Checksum Value: $977CE522
    Segments:
        0: /Users/kelatov/OS_X-10.6.dmg
    Partition Information:
        0:
            Name: whole disk (Apple_HFS : 0)
            Partition Number: 0
            Checksum Type: CRC32
            Checksum Value: $D528D8A8
    Format: UDZO
    Backing Store Information:
        URL: file://localhost/Users/kelatov/OS_X-10.6.dmg
        Name: OS_X-10.6.dmg
        Class Name: CUDIFEncoding
        Backing Store Information:
            URL: file://localhost/Users/kelatov/OS_X-10.6.dmg
            Name: OS_X-10.6.dmg
            Class Name: CBSDBackingStore
    partitions:
        partition-scheme: none
        block-size: 512
        appendable: true
        partitions:
            0:
                partition-name: whole disk
                partition-start: 0
                partition-synthesized: true
                partition-length: 13158216
                partition-hint: Apple_HFS
                partition-filesystems:
                    HFS+:
        burnable: true
    udif-ordered-chunks: true
    Properties:
        Encrypted: false
        Kernel Compatible: true
        Checksummed: true
        Software License Agreement: false
        Partitioned: false
        Compressed: true
    Resize limits (per hdiutil resize -limits):
     min     cur     max
    13158216    13158216    13158216


You can see that the total size is 6737006592 bytes (about 6.3Gib). That is not going to fit on a Single Layer DVD. Here is the size information of an empty SL-DVD:

    $drutil status
     Vendor   Product           Rev
     MATSHITA DVD-R   UJ-8A8    HA13

               Type: DVD-R                Name: /dev/disk1
       Write Speeds: 2x, 4x, 8x
       Overwritable:  510:38:38         blocks:  2297888 /   4.71GB /   4.38GiB
         Space Free:  510:38:38         blocks:  2297888 /   4.71GB /   4.38GiB
         Space Used:   00:00:00         blocks:        0 /   0.00MB /   0.00MiB
        Writability: appendable, blank, overwritable
          Book Type: DVD-R (v5)
           Media ID: RITEKF1


We can see that we can fit about 4.3GiB onto a SL-DVD. When I mount the DMG, I see the following size:

    kelatov@kmac:~$hdiutil attach -nobrowse OS_X-10.6.dmg
    expected   CRC32 $977CE522
    /dev/disk2                                              /Volumes/Mac OS X Install DVD


Here is the **df** output:

    kelatov@kmac:~$df -Ph /Volumes/Mac\ OS\ X\ Install\ DVD/
    Filesystem   Size   Used  Avail Capacity  Mounted on
    /dev/disk2  6.3Gi  6.2Gi   81Mi    99%    /Volumes/Mac OS X Install DVD


Since the data is compressed the actual file is 5.2GiB:

    kelatov@kmac:~$ls -lh OS_X-10.6.dmg
    -rw-r--r--@ 1 kelatov  staff   5.2G Jul 17 18:34 OS_X-10.6.dmg


### Create a Sparse Image

Let's create a sparse image and copy the contents of the DMG to that. To create the sparse image we can run the following:

    kelatov@kmac:~$hdiutil create -size 7g -type SPARSE -fs HFS+ -volname copy image -layout NONE
    created: /Users/kelatov/image.sparseimage


I noticed that the DMG didn't have a partition schema so I did the same thing for the Sparse Image.

### Restore DMG to a Sparse Image

Now we can mount the sparse file. First let's unmount the DMG:

    kelatov@kmac:~$hdiutil detach /Volumes/Mac\ OS\ X\ Install\ DVD/
    "disk2" unmounted.
    "disk2" ejected.


Now let's mount the Sparse Image:

    kelatov@kmac:~$hdiutil attach -nobrowse image.sparseimage
    /dev/disk2                                              /Volumes/copy


Now we can use **asr** (Apple Software Restore) to basically do a block level copy of the DMG onto the Sparse Image. First let's scan our DMG:

    kelatov@kmac:~$sudo asr -imagescan OS_X-10.6.dmg
    Block checksum: ....10....20....30....40....50....60....70....80....90....100
    asr: successfully scanned image "/Users/kelatov/OS_X-10.6.dmg"


Now for the copy/restore:

    kelatov@kmac:~$asr -s OS_X-10.6.dmg -t /Volumes/copy -erase
        Validating target...done
        Validating source...done
        Erase contents of /dev/disk2 (/Volumes/copy)? [ny]: y
        Retrieving scan information...done
        Validating sizes...done
        Restoring  ....10....20....30....40....50....60....70....80....90....100
        Verifying  ....10....20....30....40....50....60....70....80....90....100
        Remounting target volume...done


Checking the size of the Sparse Image:

    kelatov@kmac:~$du -sh image.sparseimage
    6.2G    image.sparseimage


After the copy the Sparse was mounted and checking the maximum size:

    kelatov@kmac:~$df -Ph /Volumes/Mac\ OS\ X\ Install\ DVD/
    Filesystem   Size   Used  Avail Capacity  Mounted on
    /dev/disk2  7.0Gi  6.2Gi  824Mi    89%    /Volumes/Mac OS X Install DVD


Notice the maximum size is 7.0GiB, which is what we created the Sparse File to be. Notice that since we did a block level copy the Volume Name was also copied.

### Clean Up Un-necessary Files in the New Sparse Image

The Sparse Image is already mounted so let's clean it up. The Mac OS X install CD contains a lot of printer Drivers, Language Packages, and X11 tools. For recovery purposes we don't need those. To clean up the Sparse Image, I ran the following:

    kelatov@kmac:~$cd /Volumes/Mac\ OS\ X\ Install\ DVD/System/Installation/Packages/
    kelatov@kmac:/Volumes/Mac OS X Install DVD/System/Installation/Packages$rm -rf Norwegian.pkg Russian.pkg Polish.pkg Portuguese.pkg SimplifiedChinese.pkg Spanish.pkg Swedish.pkg TraditionalChinese.pkg Japanese.pkg Italian.pkg German.pkg French.pkg Finnish.pkg Danish.pkg Dutch.pkg Korean.pkg HP_* Canon_* Lexmark_* X11User.pkg Samsung_Common.pkg BrazilianPortuguese.pkg Brother_* EPSON_*
    kelatov@kmac:/Volumes/Mac OS X Install DVD/System/Installation/Packages$rm -rf ../../../Optional\ Installs.localized/Packages/


After you are done cleaning up superflous files, the used size should be about 4.2GiB:

    kelatov@kmac:~$df -Ph /Volumes/Mac\ OS\ X\ Install\ DVD/
    Filesystem   Size   Used  Avail Capacity  Mounted on
    /dev/disk2  7.0Gi  4.2Gi  2.8Gi    61%    /Volumes/Mac OS X Install DVD


### Compact Sparse Image

Now we can reclaim the unused space in the Sparse image and resize it:

    kelatov@kmac:~$hdiutil compact image.sparseimage
    Starting to compact…
    Reclaiming free space…
    ...............................................................................
    Finishing compaction…
    ...............................................................................
    Reclaimed 1.9 GB out of 2.8 GB possible.


Notice we didn't get all of the possible space. Looking over the size information of the image, we see the following:

    hdiutil imageinfo image.sparseimage | grep "Size Information" -A 6
    Size Information:
        Total Bytes: 7516192768
        Compressed Ratio: 1
        Sector Count: 14680064
        Total Non-Empty Bytes: 4639948800
        Compressed Bytes: 7516192768
        Total Empty Bytes: 2876243968


we can also check the limits set on the Sparse file:

    kelatov@kmac:~$hdiutil resize -limits image.sparseimage
     min     cur     max
    13158272    14680064    34359738368


the values are in 512 sized sectors. So our minimum possible size is (13158272 * 512) 6737035264 bytes. So I can resize the image to that by running the following:

    kelatov@kmac:~$hdiutil resize -size min image.sparseimage
    kelatov@kmac:~$hdiutil imageinfo image.sparseimage | grep "Size Information" -A 6
    Size Information:
        Total Bytes: 6737035264
        Compressed Ratio: 1
        Sector Count: 13158272
        Total Non-Empty Bytes: 4638900224
        Compressed Bytes: 6737035264
        Total Empty Bytes: 2098135040


Notice the size has changed, but it didn't go as low as 4.3GiB (as shown by Total Non-Empty Bytes). The reason for this is because the sparse image is not defragmented. This is discussed in "[Defragmentation and disk images](http://www.eonlinegratis.com/2013/how-to-reclaim-allmost-free-space-from-a-sparsebundle-on-os-x/)".

From here we have two options. If you have access to iDefrag then you can use that to defragment the Sparse Image to reclaim more space, or we can create a smaller Sparse Image and copy the contents manually.

### Use iDefrag to Defragment the Sparse Image

Luckily, I had iDefrag :). Mount your Sparse image:

    kelatov@kmac:~$hdiutil attach image.sparseimage


then start up iDefrag and you will see you drive there. Click "Go" and it will start defragmenting:

![iDefrag started Decrease DMG Size to Fit on a Single Layer DVD](https://github.com/elatov/uploads/raw/master/2013/07/iDefrag_started.png)

after it's done you will the following message:

![iDefrag finished Decrease DMG Size to Fit on a Single Layer DVD](https://github.com/elatov/uploads/raw/master/2013/07/iDefrag_finished.png)

at this point you can quit iDefrag and unmount the Sparse Image:

    kelatov@kmac:~$hdiutil detach /dev/disk2
    "disk2" unmounted.
    "disk2" ejected.


Then we can try to compact again and we will see the following:

    kelatov@kmac:~$hdiutil compact image.sparseimage
    Starting to compact…
    Reclaiming free space…
    ...............................................................................
    Finishing compaction…
    ...............................................................................
    Reclaimed 2.0 GB out of 2.0 GB possible.


Checking the new size limits:

    kelatov@kmac:~$hdiutil resize -limits image.sparseimage
     min     cur     max
    8862888 13158272    34359738368


we can go to (8862888 * 512) 4537798656 bytes (less than 4.3 GiB). Now for the actual resize:

    kelatov@kmac:~$hdiutil resize -size min image.sparseimage


and here is the new size:

    kelatov@kmac:~$hdiutil imageinfo image.sparseimage  | grep "Size Information" -A 6
    Size Information:
        Total Bytes: 4537798656
        Compressed Ratio: 1
        Sector Count: 8862888
        Total Non-Empty Bytes: 4537798656
        Compressed Bytes: 4537798656
        Total Empty Bytes: 0


that looks much better.

### Copy Contents of Sparse Image into a Smaller Sparse Image

If you don't have access to iDefrag, you can create a smaller sparse image:

    kelatov@kmac:~$hdiutil create -size 4.3g -type SPARSE -fs HFS+ -volname Small_Sparse image2 -layout NONE
    created: /Users/kelatov/image2.sparseimage


Now we can mount both our images:

    kelatov@kmac:~$hdiutil attach -nobrowse image.sparseimage
    /dev/disk2                                              /Volumes/Mac OS X Install DVD
    kelatov@kmac:~$hdiutil attach -nobrowse image2.sparseimage
    /dev/disk3                                              /Volumes/Small_Sparse


Now we can just copy from the first sparse image to the second (smaller) sparse file. First check to make sure the source is smaller than the destination:

    kelatov@kmac:~$df -Ph /Volumes/*
    Filesystem        Size   Used  Avail Capacity  Mounted on
    /dev/disk2       4.2Gi  4.2Gi    0Bi   100%    /Volumes/Mac OS X Install DVD
    /dev/disk3       4.3Gi   72Mi  4.2Gi     2%    /Volumes/Small_Sparse


**asr** used to be able to do file-level copies, but now only block level copies/restores are allowed. From the man [page](https://developer.apple.com/library/mac/#documentation/Darwin/Reference/ManPages/man8/asr.8.html):

    When run in its first form above, the --erase option must always be used,
    as asr no longer supports file copying.  Such functionality is done bet-
    ter by ditto(1).


I prefer **rsync** over **ditto** ([ditto vs. rsync](http://lists.apple.com/archives/macos-x-server/2002/Mar/msg01142.html)), so here is what I ran to copy the contents onto the smaller sparse image:

    kelatov@kmac:~$sudo rsync -avzP /Volumes/Mac\ OS\ X\ Install\ DVD/. /Volumes/Small_Sparse/.
    ...
    ...
    usr/standalone/i386/boot.efi
          319152 100%  301.72kB/s    0:00:01 (xfer#16938, to-check=0/28139)

    sent 3435096577 bytes  received 439862 bytes  6850521.31 bytes/sec
    total size is 4458227175  speedup is 1.30


From here we can either convert the Sparse Image back to a DMG or an ISO/CDR. Let's unmount both:

    kelatov@kmac:~$hdiutil detach /Volumes/Mac\ OS\ X\ Install\ DVD/
    "disk2" unmounted.
    "disk2" ejected.
    kelatov@kmac:~$hdiutil detach /Volumes/Small_Sparse/
    "disk3" unmounted.
    "disk3" ejected.


### Convert Sparse Image to DMG

We can use this command to convert our sparse image to a DMG:

    kelatov@kmac:~$hdiutil convert image.sparseimage -format UDBZ -o Mac_OS_10_6_Custom.dmg
    Preparing imaging engine…
    Reading whole disk (Apple_HFS : 0)…
    ...............................................................................
       (CRC32 $9B980201: whole disk (Apple_HFS : 0))
    Adding resources…
    ...............................................................................
    Elapsed Time:  3m 53.244s
    File size: 3404005521 bytes, Checksum: CRC32 $FD3402E5
    Sectors processed: 8862888, 8862881 compressed
    Speed: 18.6Mbytes/sec
    Savings: 25.0%
    created: /Users/kelatov/Mac_OS_10_6_Custom.dmg


Just for reference here are the available formats:

    UDRW - UDIF read/write image
    UDRO - UDIF read-only image
    UDCO - UDIF ADC-compressed image
    UDZO - UDIF zlib-compressed image
    UDBZ - UDIF bzip2-compressed image (OS X 10.4+ only)
    UFBI - UDIF entire image with MD5 checksum
    UDRo - UDIF read-only (obsolete format)
    UDCo - UDIF compressed (obsolete format)
    UDTO - DVD/CD-R master for export
    UDxx - UDIF stub image
    UDSP - SPARSE (grows with content)
    UDSB - SPARSEBUNDLE (grows with content; bundle-backed)
    RdWr - NDIF read/write image (deprecated)
    Rdxx - NDIF read-only image (Disk Copy 6.3.3 format)
    ROCo - NDIF compressed image (deprecated)
    Rken - NDIF compressed (obsolete format)
    DC42 - Disk Copy 4.2 image


taken from the man [page](https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/hdiutil.1.html). With bzip2 compression the end file will be even smaller:

    kelatov@kmac:~$du -sh Mac_OS_10_6_Custom.dmg
    3.2G    Mac_OS_10_6_Custom.dmg


Now we can burn the file, by just running:

    kelatov@kmac:~$hdiutil burn Mac_OS_10_6_Custom.dmg
    Preparing data for burn
    Opening session
    Opening track
    Writing track
    ..............................................................................
    Closing track
    ..............................................................................
    Closing session
    Finishing burn
    Verifying burn…
    Verifying
    ...............................................................................
    Burn completed successfully
    ...............................................................................
    hdiutil: burn: completed


### Convert Sparse Image to ISO

This can be accomplished with **hdiutil** in multiple ways. The first one is with the following command:

    kelatov@kmac:~$hdiutil convert image.sparseimage -format UDTO -o MAC_OS_10_6_Custom.cdr
    Reading whole disk (Apple_HFS : 0)…
    ...............................................................................
    Elapsed Time:  4m 38.798s
    Speed: 15.5Mbytes/sec
    Savings: 0.0%
    created: /Users/kelatov/MAC_OS_10_6_Custom.cdr


the second way is like this:

    kelatov@kmac:~$sudo hdiutil makehybrid -iso -joliet -o MAC_OS_10_6_Custom.iso image.sparseimage
    Creating hybrid image...
    ..............................................................................


both can be burned by using the 'hdiutil burn' command or with any burning software.

## Mac OS X 10.8 Recovery Options

Since I was on Mac OS 10.8 there are a couple of other options for recovery media.

### 1. Resize OS X Mountain Lion installer to fit on a 4.7 GB DVD

The 10.8 Installer is downloadable via App Store and even though it's doesn't fit on a regular DVD you just have to copy the contents into a smaller image. No deletion of any files is necessary. The instructions on how to accomplish that are here:

*   [Resize OS X Mountain Lion installer to fit on a single layer 4.7 GB DVD](https://raymii.org/s/tutorials/OS-X-Mountain_Lion_iso_resize_to_fit_on_a_single_layer_dvd.html)
*   [How to Install OS X Mountain Lion from a Single-Layer DVD](http://alexcline.net/2012/07/28/how-to-install-os-x-mountain-lion-from-a-single-layer-dvd/)
*   [How To Create a Bootable Mountain Lion (OS X 10.8) Installation DVD](http://www.hightechdad.com/2012/07/25/how-to-create-a-bootable-mountain-lion-os-x-10-8-installation-dvd-or-usb-drive/)
*   [Burn OS X Mountain Lion installer to single-layer DVD](http://hints.macworld.com/article.php?story=20120727121953498)

From the bottom link (Mac OS X hints), here is a snippet of the code that can accomplishes our goal:

	#!/bin/bash
	rm -f /private/tmp/Mountain\ Lion\ DVD\ Image\ read-write.dmg # Remove any old copies of the DVD image before we begin.

	echo "Creating DVD Image..."
	hdiutil create -size 4.2g -volname "Mac OS X Install ESD" /private/tmp/Mountain\ Lion\ DVD\ Image\ read-write.dmg -fs HFS+ -layout SPUD

	hdiutil attach -nobrowse ~/Desktop/InstallESD.dmg
	hdiutil attach -nobrowse /private/tmp/Mountain\ Lion\ DVD\ Image\ read-write.dmg

	echo "Copying Mountain Lion to new image..."
	cp -pRv /Volumes/Mac\ OS\ X\ Install\ ESD/* /Volumes/Mac\ OS\ X\ Install\ ESD\ 1/

	hdiutil detach /Volumes/Mac\ OS\ X\ Install\ ESD\ 1
	hdiutil detach /Volumes/Mac\ OS\ X\ Install\ ESD

	echo "Converting to read-only..."
	hdiutil convert /private/tmp/Mountain\ Lion\ DVD\ Image\ read-write.dmg -format UDZO -o ~/Desktop/Mountain\ Lion\ DVD\ Image.dmg

	rm -f /private/tmp/Mountain\ Lion\ DVD\ Image\ read-write.dmg

	echo "Image Creation Complete. Please burn '~/Desktop/Mountain Lion DVD Image.dmg' to a DVD using Disk Utility."
	open ~/Desktop/


### 2. Mac OS X 10.8 Has a Built-in Recovery Partition

From "[OS X Recovery](http://www.apple.com/osx/recovery/)":

> **The new Mac safety net.**
> OS X Recovery lets you repair disks or reinstall OS X without the need for a physical install disc. Since OS X Recovery is built into your Mac, it’s always there when you need it. Even if you don’t need it, it’s good to know it’s there. And you don’t have to search through original packaging to find install DVDs to get your Mac back up and running.
>
> **Command-R to the rescue.**
> Just hold down **Command-R** during startup and OS X Recovery springs into action. It lets you choose from common utilities: You can run Disk Utility to check or repair your hard drive, erase your hard drive and reinstall a fresh copy of OS X, or restore your Mac from a Time Machine backup. You can even use Safari to get help from Apple Support online. And if OS X Recovery encounters problems, it will automatically connect to Apple over the Internet.

So I can just reboot the Mac and hold Command-R to get into recovery mode.

### 3. Use OS X Lion's Recovery Disk Assistant to create a bootable USB recovery Disk

Starting with OS X Lion, you can create a recovery USB disk to help with recovery. Instructions on how to do that are here:

*   [Using OS X Lion's Recovery Disk Assistant](http://macs.about.com/od/usingyourmac/ss/Using-Os-X-Lions-Recovery-Disk-Assistant_2.htm)
*   [OS X: About Recovery Disk Assistant](http://support.apple.com/kb/ht4848)

From "[OS X Recovery Disk Assistant v1.0](http://support.apple.com/kb/dl1433)":

> The OS X Recovery Disk Assistant lets you create OS X Recovery on an external drive that has all of the same capabilities as the built-in OS X Recovery: reinstall Lion or Mountain Lion, repair the disk using Disk Utility, restore from a Time Machine backup, or browse the web with Safari.

Well at least I have a cheap bootable OS 10.6 DVD now :)
