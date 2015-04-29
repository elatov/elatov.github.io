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

	[elatov@localhost ~]$ systemd-analyze
	Startup finished in 845ms (kernel) + 2.434s (initrd) + 3.052s (userspace) = 6.332s

#### Installing the Wireless Driver
I had a thunderbolt-to-ethernet adapter, after plugging it in, the *tg3* driver picked it up:

	[elatov@localhost ~]$ lspci -k
	0a:00.0 Ethernet controller: Broadcom Corporation NetXtreme BCM57762 Gigabit Ethernet PCIe
    Subsystem: Apple Inc. Device 00f6
    Kernel driver in use: tg3
    Kernel modules: tg3

and the ethernet device showed up:

	[elatov@localhost ~]$ ip -4 a
	1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN mode DEFAULT group default
	    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
	2: ens9: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN mode DEFAULT group default qlen 1000
	    link/ether 0c:4d:e9:a0:c0:aa brd ff:ff:ff:ff:ff:ff
	    
After using Network Manager I got an IP via DHCP and then I updated all the packages:

	[elatov@localhost ~]$ sudo yum update

Then I installed the **kernel-devel** package along with the **kmod-wl** package:

	[elatov@localhost ~]$ sudo yum install kmod-wl kernel-devel
	
Then after the reboot I was able to see the wireless device:

	[elatov@localhost ~]$ iw dev
	phy#0
	    Interface wlp3s0
	        ifindex 2
	        wdev 0x1
	        addr 34:36:3b:8a:7d:6c

and **wl0** is the driver

	[elatov@localhost ~]$ ethtool -i wlp3s0
	driver: wl0
	version: 6.30.223.248 (r487574)
	firmware-version:
	bus-info:
	supports-statistics: no
	supports-test: no
	supports-eeprom-access: no
	supports-register-dump: no
	supports-priv-flags: no

#### Fixing the Brightness Button

I realized the Brightness Buttons *F1* and *F2* weren't working on Gnome-Shell. The the notification showed up but it didn't change anything. So I ran across [this](https://ask.fedoraproject.org/en/question/26364/cannot-adjust-brightness/) and the fix is to add the following to GRUB:

	[elatov@localhost ~]$ grep LINUX /etc/default/grub
	GRUB_CMDLINE_LINUX="rd.lvm.lv=fedora/swap rd.lvm.lv=fedora/root rhgb quiet acpi_backlight=vendor"

and then to re-generate the grub menu:

	[elatov@localhost ~]$ sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg

#### Fix the ~ key

Upon pushing the tilde key (~) I was seeing the greater than sign (>). The bug is described [here](https://bugzilla.redhat.com/show_bug.cgi?id=1025041) and to fix that issue I modified the GRUB config again to have the following:

	[elatov@localhost ~]$ grep GRUB_CMDLINE_LINUX /etc/default/grub
	GRUB_CMDLINE_LINUX="rd.lvm.lv=fedora/swap rd.lvm.lv=fedora/root rhgb quiet acpi_backlight=vendor hid_apple.iso_layout=0"

And then after re-genenating the GRUB menu one more time and rebooting the issue was fixed.

### Booting back into Mac OS X
To boot back into Mac OS X, just reboot and hold down the alt/option key and you will see the **Macintosh HD** and **Fedora** bootable devices:

![boot-menu-post-fedora-install](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/boot-menu-post-fedora-install.png)

Upon selecting Macintosh HD you will boot back into Mac OS X. Once booted you can go into System Preferences and change the Start Up Disks if you so desire:

![mac-osx-startup-after-fed-install](https://googledrive.com/host/0B4vYKT_-8g4IWE9kS2hMMmFuXzg/macair_fed21/mac-osx-startup-after-fed-install.png)

Also by default the **EFI** partition from LInux will show up on your Desktop. To hide it from **Finder** you can run the following:

	elatov@macair:~$cd /Volumes
	elatov@macair:/Volmes$sudo chflags hidden Linux\ HFS+\ ESP/

### Booting into Mac OS X with GRUB
By default the GRUB menu will contain entries for Mac OS X, but when you try to boot from one of the enries you will recieve the following errors:

	error: can't find command 'xnu_uuid'
	error: can't find command 'xnu_kernel64'
	error: can't find command 'xnu_kextdir'

The issue is described [here](https://bugzilla.redhat.com/show_bug.cgi?id=893179) and [here](http://comments.gmane.org/gmane.comp.boot-loaders.grub.devel/22598). It sounds like chainloading is a way to go, so I ended up adding the following config:

	[elatov@localhost ~]$ $sudo cat /etc/grub.d/40_custom
	#!/bin/sh
	exec tail -n +3 $0
	# This file provides an easy way to add custom menu entries.  Simply type the
	# menu entries you want to add after this comment.  Be careful not to change
	# the 'exec tail' line above.
	menuentry "MacOS X Yosemite" {
	        insmod hfsplus
	        set root=(hd1,gpt3)
	        chainloader /System/Library/CoreServices/boot.efi
	        boot
	}
	
I chose **gpt3** cause that's where the Apple Boot partition was

	[elatov@localhost ~]$ sudo fdisk -l | grep boot
	/dev/sda3  186509544 187779079   1269536 619.9M Apple boot
	
And I found a pretty good example of the config [here](http://forums.fedoraforum.org/archive/index.php/t-288002.html). Then I re-generated the GRUB menu, rebooted and chose the "Mac OS X Yosemite" entry and I saw Mac OS X boot up.
