---
published: true
layout: post
title: "Mac OS X Mount NTFS"
author: Karim Elatov
description: ""
categories: [os,storage]
tags: [ntfs,mac,fdisk,gdisk,diskutil,gpt,mbr]
---
I had a USB stick laying around and I had to put **HFS+** on it to do some Mac OS X specific activities. Initially I had NTFS on it (just so I could use the usb stick across all OSes), and I wanted to format it back to NTFS using Mac OS X. As I was reading up on the process, I realized there are a couple of different ways to the approach.

### Install ntfs-3g
I already had mac-ports setup on my mac (check out [this](/2013/07/mount-various-file-system-with-autofs-on-mac-os-x-mountain-lion/) post on the install process). After you have mac-ports installed, you can use the following to install **ntfs-3g** :

	~$sudo port install ntfs-3g

That will come with all the necessary tools to use NTFS (mount NTFS as read-write and to actually format partitions as NTFS) on Mac OS X. 

	~$port contents ntfs-3g | grep bin
	  /opt/local/bin/lowntfs-3g
	  /opt/local/bin/ntfs-3g
	  /opt/local/bin/ntfs-3g.probe
	  /opt/local/bin/ntfs-3g.secaudit
	  /opt/local/bin/ntfs-3g.usermap
	  /opt/local/bin/ntfscat
	  /opt/local/bin/ntfscluster
	  /opt/local/bin/ntfscmp
	  /opt/local/bin/ntfsfix
	  /opt/local/bin/ntfsinfo
	  /opt/local/bin/ntfsls
	  /opt/local/sbin/mkfs.ntfs
	  /opt/local/sbin/mkntfs
	  /opt/local/sbin/ntfsclone
	  /opt/local/sbin/ntfscp
	  /opt/local/sbin/ntfslabel
	  /opt/local/sbin/ntfsresize
	  /opt/local/sbin/ntfsundelete


BTW I was on Mac OS X Mavericks:

	~$sw_vers 
	ProductName:	Mac OS X
	ProductVersion:	10.9.2
	BuildVersion:	13C64

### NTFS with MBR Using fdisk

So plug in the drive and check out it's partitions:

	~$diskutil list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:     FDisk_partition_scheme                        *8.0 GB     disk2
	   1:                 DOS_FAT_32 UNTITLED                8.0 GB     disk2s1

**FDisk_partition_scheme** is the **MBR** style scheme and it looks like it has a FAT filesystem on it. So let's erase the disk partition information from the drive:

	~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 count=1
	1+0 records in
	1+0 records out
	512 bytes transferred in 0.002081 secs (246017 bytes/sec)

Now checking out the drive, I don't have any partitions on it:

	~$diskutil list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:                                                   *8.0 GB     disk2


Now let's initialize the **MBR** style partition scheme on the disk

	~$sudo fdisk -i -a dos /dev/disk2
		-----------------------------------------------------
		------ ATTENTION - UPDATING MASTER BOOT RECORD ------
		-----------------------------------------------------
	
	Do you wish to write new MBR and partition table? [n] y

The above will also create a FAT partition on the disk. So let's change the partition type with **fdisk** to NTFS:

	~$sudo fdisk -e /dev/disk2
	fdisk: 1> print
	Disk: /dev/disk2	geometry: 973/255/63 [15633408 sectors]
	Offset: 0	Signature: 0xAA55
	         Starting       Ending
	 #: id  cyl  hd sec -  cyl  hd sec [     start -       size]
	------------------------------------------------------------------------
	 1: 0B 1023 254  63 - 1023 254  63 [         2 -   15633406] Win95 FAT-32
	 2: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 3: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 4: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	fdisk: 1> edit 1
	         Starting       Ending
	 #: id  cyl  hd sec -  cyl  hd sec [     start -       size]
	------------------------------------------------------------------------
	 1: 0B 1023 254  63 - 1023 254  63 [         2 -   15633406] Win95 FAT-32
	Partition id ('0' to disable)  [0 - FF]: [B] (? for help) 07
	Do you wish to edit in CHS mode? [n] n
	Partition offset [0 - 15633408]: [63] 
	Partition size [1 - 15633345]: [15633345] 
	fdisk:*1> print
	Disk: /dev/disk2	geometry: 973/255/63 [15633408 sectors]
	Offset: 0	Signature: 0xAA55
	         Starting       Ending
	 #: id  cyl  hd sec -  cyl  hd sec [     start -       size]
	------------------------------------------------------------------------
	 1: 07    0   1   1 - 1023 254  63 [        63 -   15633345] HPFS/QNX/AUX
	 2: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 3: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 4: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	fdisk:*1> write


As a side note if you don't initialize the **MBR** scheme and you use **fdisk** it will ask you to initialize the partition table:

	~$sudo fdisk -e /dev/disk2
	The signature for this MBR is invalid.
	Would you like to initialize the partition table? [y] y
	Enter 'help' for information
	fdisk:*1> print
	Disk: /dev/disk2	geometry: 973/255/63 [15633408 sectors]
	Offset: 0	Signature: 0xAA55
	         Starting       Ending
	 #: id  cyl  hd sec -  cyl  hd sec [     start -       size]
	------------------------------------------------------------------------
	 1: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 2: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 3: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 4: 00    0   0   0 -    0   0   0 [         0 -          0] unused   
	
	
	Writing MBR at offset 0.

But then you will have create the partition with **fdisk** manually and it will create a FAT partition, which we will have to change later to NTFS (so inititiazing with disk from the command is faster... I think).

At this point you should see the following on the usb drive:

	~$diskutil list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:     FDisk_partition_scheme                        *8.0 GB     disk2
	   1:               Windows_NTFS                         8.0 GB     disk2s1

Now we format our partition as NTFS:

	~$sudo mkntfs -FQ /dev/disk2s1 
	The partition start sector was not specified for /dev/disk2s1 and it could not be obtained automatically.  It has been set to 0.
	The number of sectors per track was not specified for /dev/disk2s1 and it could not be obtained automatically.  It has been set to 0.
	The number of heads was not specified for /dev/disk2s1 and it could not be obtained automatically.  It has been set to 0.
	Cluster size has been automatically set to 4096 bytes.
	To boot from a device, Windows needs the 'partition start sector', the 'sectors per track' and the 'number of heads' to be set.
	Windows will not be able to boot from this device.
	Creating NTFS volume structures.
	mkntfs completed successfully. Have a nice day.

Lastly we can mount the partition

	~$sudo ntfs-3g /dev/disk2s1 /mnt/usb
	~$df -Ph -T osxfusefs
	Filesystem     Size   Used  Avail Capacity  Mounted on
	/dev/disk2s1  7.5Gi   39Mi  7.4Gi     1%    /mnt/usb

It will be mounted as read-write too:

	~$tail /var/log/system.log | grep ntfs-3g
	Jul  9 14:12:49 mac ntfs-3g[9795]: Mounted /dev/disk2s1 (Read-Write, label "", NTFS 3.1)
	Jul  9 14:12:49 mac ntfs-3g[9795]: Cmdline options: 
	Jul  9 14:12:49 mac ntfs-3g[9795]: Mount options: allow_other,nonempty,relatime,fsname=/dev/disk2s1,blkdev,blksize=4096

### NTFS with MBR Using diskutil and fdisk

We can also use **diskutil** to create an **MBR** partition scheme with a FAT partition all one command. First make sure nothing in on the disk:

	~$diskutil list disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:                                                   *8.0 GB     disk2

Then run the following to create the MBR Scheme and FAT 32 Partition

	~$diskutil partitionDisk disk2 MBR MS-DOS VOL 100%
	Started partitioning on disk2
	Unmounting disk
	Creating the partition map
	Waiting for the disks to reappear
	Formatting disk2s1 as MS-DOS (FAT) with name VOL
	512 bytes per physical sector
	/dev/rdisk2s1: 15602896 sectors in 1950362 FAT32 clusters (4096 bytes/cluster)
	bps=512 spc=8 res=32 nft=2 mid=0xf8 spt=32 hds=255 hid=2 drv=0x80 bsec=15633406 bspf=15238 rdcl=2 infs=1 bkbs=6
	Mounting disk
	Finished partitioning on disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:     FDisk_partition_scheme                        *8.0 GB     disk2
	   1:                 DOS_FAT_32 VOL                     8.0 GB     disk2s1

From here you can do the same thing, change the partition type with **fdisk**,
and then use **mkntfs** (from the **ntfs-3g** package) to format it as NTFS. BTW for reference here is a list of supported file systems by **diskutil**:

	~$diskutil listFilesystems
	Formattable file systems
	
	These file system personalities can be used for erasing and partitioning.
	When specifying a personality as a parameter to a verb, case is not considered.
	Certain common aliases (also case-insensitive) are listed below as well.
	
	------------------------------------------------------------------------
	PERSONALITY                     USER VISIBLE NAME                               
	------------------------------------------------------------------------
	ExFAT                           ExFAT                                           
	Free Space                      Free Space                                      
	  (or) free
	MS-DOS                          MS-DOS (FAT)                                    
	MS-DOS FAT12                    MS-DOS (FAT12)                                  
	MS-DOS FAT16                    MS-DOS (FAT16)                                  
	MS-DOS FAT32                    MS-DOS (FAT32) (or) fat32
	HFS+                            Mac OS Extended                                 
	Case-sensitive HFS+             Mac OS Extended (Case-sensitive)  (or) hfsx
	Case-sensitive Journaled HFS+   Mac OS Extended (Case-sensitive, Journaled) (or) jhfsx
	Journaled HFS+                  Mac OS Extended (Journaled) (or) jhfs+

### NTFS with GPT Using gpt and gdisk

Now let's create a **GPT** partition scheme and put NTFS on the first partition. Let's clear out the partitions and make sure nothing is one them:

	~$diskutil list disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:                                                   *8.0 GB     disk2

To put a **GPT** partition scheme, run the following:

	~$sudo gpt create /dev/disk2
	~$diskutil list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:      GUID_partition_scheme                        *8.0 GB     disk2
   
You can also use **gpt** to confirm the **GPT** Partition scheme is on there:

	~$sudo gpt -vv show /dev/disk2
	gpt show: disk2: mediasize=8004304896; sectorsize=512; blocks=15633408
	gpt show: disk2: PMBR at sector 0
	gpt show: disk2: Pri GPT at sector 1
	gpt show: disk2: Sec GPT at sector 15633407
	     start      size  index  contents
	         0         1         PMBR
	         1         1         Pri GPT header
	         2        32         Pri GPT table
	        34  15633341         
	  15633375        32         Sec GPT table
	  15633407         1         Sec GPT header

Now let's use **gdisk** to create a partition of type NTFS on it:

	~$sudo gdisk /dev/disk2
	GPT fdisk (gdisk) version 0.8.10
	
	Partition table scan:
	  MBR: protective
	  BSD: not present
	  APM: not present
	  GPT: present
	
	Found valid GPT with protective MBR; using GPT.
	
	Command (? for help): n
	Partition number (1-128, default 1): 
	First sector (34-15633374, default = 2048) or {+-}size{KMGTP}: 
	Last sector (2048-15633374, default = 15633374) or {+-}size{KMGTP}: 
	Current type is 'Apple HFS/HFS+'
	Hex code or GUID (L to show codes, Enter = af00): 0700
	Changed type of partition to 'Microsoft basic data'
	
	Command (? for help): print
	Disk /dev/disk2: 15633408 sectors, 7.5 GiB
	Logical sector size: 512 bytes
	Disk identifier (GUID): C7AE32D1-0DBD-4C3F-8EC2-02C26106BEDF
	Partition table holds up to 128 entries
	First usable sector is 34, last usable sector is 15633374
	Partitions will be aligned on 2048-sector boundaries
	Total free space is 2014 sectors (1007.0 KiB)
	
	Number  Start (sector)    End (sector)  Size       Code  Name
	   1            2048        15633374   7.5 GiB     0700  Microsoft basic data
	
	Command (? for help): w
	
	Final checks complete. About to write GPT data. THIS WILL OVERWRITE EXISTING
	PARTITIONS!!
	
	Do you want to proceed? (Y/N): y
	OK; writing new GUID partition table (GPT) to /dev/disk2.
	Warning: The kernel may continue to use old or deleted partitions.
	You should reboot or remove the drive.
	The operation has completed successfully.

Same thing from here, we can format it with **mkntfs** and mount it with **ntfs-3g**.

### Remove GPT Partition Scheme

To remove the GPT paritition scheme first unmount the drive and then use **gdisk** :

	~$sudo gdisk /dev/disk2
	GPT fdisk (gdisk) version 0.8.10
	
	Partition table scan:
	  MBR: protective
	  BSD: not present
	  APM: not present
	  GPT: present
	
	Found valid GPT with protective MBR; using GPT.
	
	Command (? for help): x
	
	Expert command (? for help): z
	About to wipe out GPT on /dev/disk2. Proceed? (Y/N): y
	Warning: The kernel may continue to use old or deleted partitions.
	You should reboot or remove the drive.
	GPT data structures destroyed! You may now partition the disk using fdisk or
	other utilities.
	Blank out MBR? (Y/N): Y


At this point the disk should be empty:

	~$diskutil list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:                                                   *8.0 GB     disk2

We can also use **dd** to zero out both locations (GPT is stored/resides in two locations: at the beginning and end of the disk). From the `gpt show` command we can see where the end is:

	~$sudo gpt -v show /dev/disk2
	gpt show: /dev/disk2: mediasize=8004304896; sectorsize=512; blocks=15633408
	     start      size  index  contents
	         0         1         PMBR
	         1         1         Pri GPT header
	         2        32         Pri GPT table
	        34  15633341         
	  15633375        32         Sec GPT table
	  15633407         1         Sec GPT header

First let's zero out the secondary (end of the disk) GPT table:

	~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 seek=15633341
	dd: /dev/disk2: end of device
	68+0 records in
	67+0 records out
	34304 bytes transferred in 0.023648 secs (1450607 bytes/sec)
	elatok@usxxelatokm1:~$sudo gpt -v show /dev/disk2
	gpt show: /dev/disk2: mediasize=8004304896; sectorsize=512; blocks=15633408
	     start      size  index  contents
	         0         1         PMBR
	         1         1         Pri GPT header
	         2        32         Pri GPT table
	        34  15633374         

The **seek** value is basically the value of the end of the partition seen from the `gpt show` command.

Now let's do the primary (begining of disk) GPT Table:

	~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 count=2
	2+0 records in
	2+0 records out
	1024 bytes transferred in 0.000777 secs (1317879 bytes/sec)
	elatok@usxxelatokm1:~$sudo gpt -v show /dev/disk2
	gpt show: /dev/disk2: mediasize=8004304896; sectorsize=512; blocks=15633408
	gpt show: /dev/disk2: MBR not found at sector 0
	     start      size  index  contents
	         0  15633408  

And now the GPT partition scheme should be gone:

	~$sudo gdisk -l /dev/disk2
	GPT fdisk (gdisk) version 0.8.10
	
	Partition table scan:
	  MBR: not present
	  BSD: not present
	  APM: not present
	  GPT: not present
	
	Creating new GPT entries.
	Disk /dev/disk2: 15633408 sectors, 7.5 GiB
	Logical sector size: 512 bytes
	Disk identifier (GUID): 89DB6480-47BC-49C3-B8F9-827D9B7F9A39
	Partition table holds up to 128 entries
	First usable sector is 34, last usable sector is 15633374
	Partitions will be aligned on 2048-sector boundaries
	Total free space is 15633341 sectors (7.5 GiB)
	
	Number  Start (sector)    End (sector)  Size       Code  Name

if you want, you can zero out the disk completely with **diskutil** (this process will be longer and it depends on the size of your usb drive... mine takes 24 mins and it's 8GB).

	~$sudo diskutil zeroDisk /dev/disk2
	Started erase on disk2
	[ - 0%................................................... ]  3% 0:24:00 


### NTFS with GPT Using diskutil

**diskutil** can create a GPT Partition Scheme and an **MSDOS** partion all in one swoop, make sure no partitions exists:

	~$diskutil list /dev/disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:                                                   *8.0 GB     disk2

Then run the following to partition the drive:

	~$diskutil partitionDisk /dev/disk2 GPT MS-DOS VOL 100%
	Started partitioning on disk2
	Unmounting disk
	Creating the partition map
	Waiting for the disks to reappear
	Formatting disk2s2 as MS-DOS (FAT) with name VOL
	512 bytes per physical sector
	/dev/rdisk2s2: 15191032 sectors in 1898879 FAT32 clusters (4096 bytes/cluster)
	bps=512 spc=8 res=32 nft=2 mid=0xf8 spt=32 hds=255 hid=411648 drv=0x80 bsec=15220736 bspf=14836 rdcl=2 infs=1 bkbs=6
	Mounting disk
	Finished partitioning on disk2
	/dev/disk2
	   #:                       TYPE NAME                    SIZE       IDENTIFIER
	   0:      GUID_partition_scheme                        *8.0 GB     disk2
	   1:                        EFI EFI                     209.7 MB   disk2s1
	   2:       Microsoft Basic Data VOL                     7.8 GB     disk2s2

Then you can just umount the disk and reformat it with NTFS since it's type is already **07**:

	~$sudo gdisk -l /dev/disk2
	GPT fdisk (gdisk) version 0.8.10
	
	Warning: Devices opened with shared lock will not have their
	partition table automatically reloaded!
	Partition table scan:
	  MBR: hybrid
	  BSD: not present
	  APM: not present
	  GPT: present
	
	Found valid GPT with hybrid MBR; using GPT.
	Disk /dev/disk2: 15633408 sectors, 7.5 GiB
	Logical sector size: 512 bytes
	Disk identifier (GUID): FC0453E2-19AB-4D4B-8ED5-CA246662FE1F
	Partition table holds up to 128 entries
	First usable sector is 34, last usable sector is 15633374
	Partitions will be aligned on 8-sector boundaries
	Total free space is 3005 sectors (1.5 MiB)
	
	Number  Start (sector)    End (sector)  Size       Code  Name
	   1              40          409639   200.0 MiB   EF00  EFI System Partition
	   2          411648        15632383   7.3 GiB     0700  VOL

It's actually strange cause regular **fdisk** shows it as FAT:

	~$sudo fdisk /dev/disk2
	Disk: /dev/disk2	geometry: 973/255/63 [15633408 sectors]
	Signature: 0xAA55
	         Starting       Ending
	 #: id  cyl  hd sec -  cyl  hd sec [     start -       size]
	------------------------------------------------------------------------
	 1: EE 1023 254  63 - 1023 254  63 [         1 -     409639] <Unknown ID>
	 2: 0B 1023 254  63 - 1023 254  63 [    411648 -   15220736] Win95 FAT-32
	 3: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
	 4: 00    0   0   0 -    0   0   0 [         0 -          0] unused    

Here is the unmount:

	~$sudo diskutil unmount /dev/disk2s2
	Volume VOL on disk2s2 unmounted

And to format:

	~$sudo mkntfs -QF /dev/disk2s2
	The partition start sector was not specified for /dev/disk2s2 and it could not be obtained automatically.  It has been set to 0.
	The number of sectors per track was not specified for /dev/disk2s2 and it could not be obtained automatically.  It has been set to 0.
	The number of heads was not specified for /dev/disk2s2 and it could not be obtained automatically.  It has been set to 0.
	Cluster size has been automatically set to 4096 bytes.
	To boot from a device, Windows needs the 'partition start sector', the 'sectors per track' and the 'number of heads' to be set.
	Windows will not be able to boot from this device.
	Creating NTFS volume structures.
	mkntfs completed successfully. Have a nice day.

Just to be safe, I unplugged the usb drive and plugged it back in and Mavericks auto mounted the drive as NTFS.

### Replace mount_ntfs with ntfs-3g

By default when Mac OS X sees an NTFS Filesystem it mounts it as read-only. If you feel adventurous, you can follows the instructions laid out [here](https://trac.macports.org/wiki/howto/Ntfs3gFinder) to replace the default Mac OS NTFS mount binary. Here is the process:


> **Step 1. Install the ntfs-3g port.**
> 
> 	sudo port install ntfs-3g
> 
> **Step 2. Find out your userid and groupid.**
> 
> User ID:
> 
> 	id -u
> 	
> Group ID:
> 
> 	id -g
> 
> **Step 3. Use a modified *mount_ntfs* executable and save the OS X original to */sbin/mount_ntfs.orig*.**
> 
> 	sudo mv /sbin/mount_ntfs /sbin/mount_ntfs.orig
> 	sudo touch /sbin/mount_ntfs
> 	sudo chmod 0755 /sbin/mount_ntfs
> 	sudo chown 0:0 /sbin/mount_ntfs
> 	sudo nano /sbin/mount_ntfs
> 
> Then paste in the following code and save it by typing Control-X and pressing "Y". NOTE:
> 
> - You can optionally substitute in your User ID and Group ID (from Step 2 above) in place of 501 and 20 in lines 4 and 5 below.
> - This script also assumes the standard MacPorts install location of /opt/local/ so you will need to modify it if yours is different.
> 
> 		#!/bin/bash
> 		VOLUME_NAME="${@:$#}"
> 		VOLUME_NAME=${VOLUME_NAME#/Volumes/}
> 		USER_ID=501
> 		GROUP_ID=20
> 		TIMEOUT=20
> 		if [ `/usr/bin/stat -f "%u" /dev/console` -eq 0 ]; then
> 		        USERNAME=`/usr/bin/defaults read /Library/Preferences/com.apple.loginwindow | /usr/bin/grep autoLoginUser | /usr/bin/awk '{ print $3 }' | /usr/bin/sed 's/;//'`
> 		        if [ "$USERNAME" = "" ]; then
> 		                until [ `stat -f "%u" /dev/console` -ne 0 ] || [ $TIMEOUT -eq 0 ]; do
> 		                        sleep 1
> 		                        let TIMEOUT--
> 		                done
> 		                if [ $TIMEOUT -ne 0 ]; then
> 		                        USER_ID=`/usr/bin/stat -f "%u" /dev/console`
> 		                        GROUP_ID=`/usr/bin/stat -f "%g" /dev/console`
> 		                fi
> 		        else
> 		                USER_ID=`/usr/bin/id -u $USERNAME`
> 		                GROUP_ID=`/usr/bin/id -g $USERNAME`
> 		        fi
> 		else
> 		        USER_ID=`/usr/bin/stat -f "%u" /dev/console`
> 		        GROUP_ID=`/usr/bin/stat -f "%g" /dev/console`
> 		fi
> 		
> 		/opt/local/bin/ntfs-3g \
> 		         -o volname="${VOLUME_NAME}" \
> 		         -o local \
> 		         -o negative_vncache \
> 		         -o auto_xattr \
> 		         -o auto_cache \
> 		         -o noatime \
> 		         -o windows_names \
> 		         -o user_xattr \
> 		         -o inherit \
> 		         -o uid=$USER_ID \
> 		         -o gid=$GROUP_ID \
> 		         -o allow_other \
> 		         "$@" &> /var/log/ntfsmnt.log
> 		
> 		exit $?;

With that in place, if you ever plugin a usb-drive with NTFS on it, it will auto mount it as read-write.

Strangely enough there is another utility called **pdisk**, which allows you to create APM (Apple Partition Map) partition schemes, but **diskutil** can do that as well.
