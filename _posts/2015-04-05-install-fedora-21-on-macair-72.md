---
published: true
layout: post
title: "Install Fedora 21 on MacAir 7,2"
author: Karim Elatov
categories: [os,storage]
tags: [mac_os_x,fedora,diskutil]
---
I decided to install Fedora 21 on a new MacBook Air.

### MacBook Air

The MacBook is the *MacBook Air (13-inch, Early 2015)* or **MacBookAir7,2**. Here is the system information:

	elatov@macair:~$system_profiler SPHardwareDataType
	Hardware:
	
	    Hardware Overview:
	
	      Model Name: MacBook Air
	      Model Identifier: MacBookAir7,2
	      Processor Name: Intel Core i7
	      Processor Speed: 2.2 GHz
	      Number of Processors: 1
	      Total Number of Cores: 2
	      L2 Cache (per Core): 256 KB
	      L3 Cache: 4 MB
	      Memory: 8 GB
	      Boot ROM Version: MBA71.0166.B00
	      SMC Version (system): 2.27f1
	      Serial Number (system): XXXXXX
	      Hardware UUID: XXXXXXXX

The install was very similar to [this](/2013/08/install-fedora-19-on-mac-book-pro/) one.

### Re-Partition the OS disk

I just started the **Disk Utility** and resized the OS (I gave the Linux OS only 25GB):

![diskutil-part-for-fed](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/diskutil-part-for-fed.png)

### Create a Bootable USB from the Fedora Live DVD ISO
After downloading the Fedora ISO, I had the following file:

	elatov@macair:~$ls -lh downloads/Fedora-Live-Workstation-x86_64-21-5.iso
	-rw-r-----  1 elatov  elatov   1.4G Mar 25 17:14 downloads/Fedora-Live-Workstation-x86_64-21-5.iso
	
First we have to convert the ISO into a DMG (I talked about different image formats [here](/2013/07/decrease-dmg-size-to-fit-on-a-single-layer-dvd/)):

	elatov@macair:~/downloads$hdiutil convert -format UDRW -o fed_21.dmg Fedora-Live-Workstation-x86_64-21-5.iso
	Reading Driver Descriptor Map (DDM : 0)…
	Reading Fedora-Live-WS-x86_64-21-5       (Apple_ISO : 1)…
	Reading Apple (Apple_partition_map : 2)…
	Reading Fedora-Live-WS-x86_64-21-5       (Apple_ISO : 3)…
	Reading EFI (Apple_HFS : 4)…
	Reading Fedora-Live-WS-x86_64-21-5       (Apple_ISO : 5)…
	Reading EFI (Apple_HFS : 6)…
	Reading Fedora-Live-WS-x86_64-21-5       (Apple_ISO : 7)…
	..............................................................................
	Elapsed Time:  7.891s
	Speed: 177.9Mbytes/sec
	Savings: 0.0%
	created: /Users/elatov/downloads/fed_21.dmg
	

I had a 32GB USB drive with an *ext3* partition on it, as soon as plug it in it would get auto mounted and here are the partitions on the USB drive:

	elatov@macair:~$diskutil  list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:     FDisk_partition_scheme                        *32.0 GB    disk2
	   1:                      Linux                         32.0 GB    disk2s1
   

So first I unmounted the USB Drive:

	elatov@macair:~$diskutil umount /Volumes/Untitled/
	Volume  on disk2s1 unmounted 

Then I removed the MBR partition scheme:

	elatov@macair:~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 count=1
	1+0 records in
	1+0 records out
	512 bytes transferred in 0.000813 secs (629761 bytes/sec)

Then the disk was blank

	elatov@macair:~$diskutil  list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:                                                   *32.0 GB    disk2
   
We can also use **diskutil** to zero out the disk:

	elatov@macair:~$diskutil partitionDisk /dev/disk2 1 "Free Space" "unused" "100%"
	Started partitioning on disk2
	Unmounting disk
	Creating the partition map
	Waiting for the disks to reappear
	Finished partitioning on disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:      GUID_partition_scheme                        *32.0 GB    disk2
	   1:                        EFI EFI                     209.7 MB   disk2s1
   
Either way after the disk is ready to be used you can then **DD** the **DMG** onto it:


	elatov@macair:~/downloads$sudo dd if=fed_21.dmg of=/dev/disk2 bs=1m
	1403+1 records in
	1403+1 records out
	1471502336 bytes transferred in 632.999466 secs (2324650 bytes/sec)

After that the USB disk will have the following disk partition:

	elatov@macair:~$diskutil list disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:     Apple_partition_scheme                        *32.0 GB    disk2
	   1:        Apple_partition_map                         8.2 KB     disk2s1
	   2:                  Apple_HFS                         5.2 MB     disk2s2
	   3:                  Apple_HFS Fedora Live             20.8 MB    disk2s3
   
If you are going to unplug the USB disk then first unmount it:

	elatov@macair:~$diskutil eject /dev/disk2
	Disk /dev/disk2 ejected

If this is the same laptop where you are going to install Fedora then just reboot the laptop.

### Installing Fedora
Right as you reboot the Mac hold down the **alt/option** key and you will see a list of available bootable devices:

![boot-menu-mac](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/boot-menu-mac.png)

Boot from the Fedora disk and the live CD will start booting. When then Live CD starts it will ask you if you want to install onto the hard disk or try the Live CD, I selected to install onto the Hard Disk. During the installation wizard I asked the install to use the free space and to create the partitions automatically and the following partitions were created:

![fedora-installer-manual-partitions](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/fedora-installer-manual-partitions.png)

After the installed finished I rebooted and I saw the GRUB menu:

![grub-menu-after-fedora-installer](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/grub-menu-after-fedora-installer.png)

Selecting the top menu booted into Fedora without issues.

### Post Install Configuration
It took about 6.6 seconds to boot into the OS:

	systemd-analyze

#### Installing the Wireless Drive

#### Fixing the Fn-F* keys

### Booting back into Mac OS X
To boot back into Mac OS X, just reboot and hold down the alt/option key and you will see the **Macintosh HD** and **Fedora** bootable devices:

![boot-menu-post-fedora-install](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/boot-menu-post-fedora-install.png)

Upon selecting Macintosh HD you will boot back into Mac OS X. Once booted you can go into System Preferences and change the Start Up Disks if you so desire:

![mac-osx-startup-after-fed-install](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/mac-osx-startup-after-fed-install.png)

Also by default the **EFI** partition from LInux will show up on your Desktop. To hide it from **Finder** you can run the following:

	elatov@macair:~$cd /Volumes
	elatov@macair:/Volmes$sudo chflags hidden Linux\ HFS+\ ESP/
