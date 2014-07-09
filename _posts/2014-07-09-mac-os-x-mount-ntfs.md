---
published: false
layout: post
title: "Mac OS X Mount NTFS"
author: Karim Elatov
description: ""
categories: [os]
tags: [fdisk,gdisk,diskutil,gpt,mbr]
---
# list the partitions on a disk
elatok@usxxelatokm1:~$diskutil list /dev/disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *8.0 GB     disk2
   1:                 DOS_FAT_32 UNTITLED                8.0 GB     disk2s1

### now let's erase the disk completely
elatok@usxxelatokm1:~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 count=1
1+0 records in
1+0 records out
512 bytes transferred in 0.002081 secs (246017 bytes/sec)
elatok@usxxelatokm1:~$diskutil list /dev/disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                   *8.0 GB     disk2


# let's try an MBR msdos style partition
# first let's initialize the MBR on the Disk
elatok@usxxelatokm1:~$sudo fdisk -i -a dos /dev/disk2
	-----------------------------------------------------
	------ ATTENTION - UPDATING MASTER BOOT RECORD ------
	-----------------------------------------------------

Do you wish to write new MBR and partition table? [n] y
### change the partition type with fdisk
sudo fdisk -e /dev/disk2
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
Partition offset [0 - 15633408]: [63] n
'n' is not a valid number.
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


## also if you don't initialize the MBR scheme and you use fdisk it will ask
# you to initialize
elatok@usxxelatokm1:~$sudo fdisk -e /dev/disk2
fdisk: could not open MBR file /usr/standalone/i386/boot0: No such file or directory
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
elatok@usxxelatokm1:~$diskutil list /dev/disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *8.0 GB     disk2
   1:               Windows_NTFS                         8.0 GB     disk2s1


### now let's unmount the volume
elatok@usxxelatokm1:~$diskutil unmount /dev/disk2s1
Volume UNTITLED on disk2s1 unmounted

### format partition with NTFS
elatok@usxxelatokm1:~$sudo mkntfs -FQ /dev/disk2s1 
The partition start sector was not specified for /dev/disk2s1 and it could not be obtained automatically.  It has been set to 0.
The number of sectors per track was not specified for /dev/disk2s1 and it could not be obtained automatically.  It has been set to 0.
The number of heads was not specified for /dev/disk2s1 and it could not be obtained automatically.  It has been set to 0.
Cluster size has been automatically set to 4096 bytes.
To boot from a device, Windows needs the 'partition start sector', the 'sectors per track' and the 'number of heads' to be set.
Windows will not be able to boot from this device.
Creating NTFS volume structures.
mkntfs completed successfully. Have a nice day.

## lastly mount the partition
elatok@usxxelatokm1:~$sudo ntfs-3g /dev/disk2s1 /mnt/usb
elatok@usxxelatokm1:~$df -Ph -T osxfusefs
Filesystem     Size   Used  Avail Capacity  Mounted on
/dev/disk2s1  7.5Gi   39Mi  7.4Gi     1%    /mnt/usb
# it's mounted as read-write too:
elatok@usxxelatokm1:~$tail /var/log/system.log | grep ntfs-3g
Jul  9 14:12:49 usxxelatokm1.corp.emc.com ntfs-3g[9795]: Mounted /dev/disk2s1 (Read-Write, label "", NTFS 3.1)
Jul  9 14:12:49 usxxelatokm1.corp.emc.com ntfs-3g[9795]: Cmdline options: 
Jul  9 14:12:49 usxxelatokm1.corp.emc.com ntfs-3g[9795]: Mount options: allow_other,nonempty,relatime,fsname=/dev/disk2s1,blkdev,blksize=4096
###

### You can also use diskutil to create an MBR partition scheme with a FAT32
filesystem all one command. First make sure nothing in on the disk:

elatok@usxxelatokm1:~$diskutil list disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                   *8.0 GB     disk2

# then run the following to create the MBR Scheme and FAT 32 Partition
elatok@usxxelatokm1:~$diskutil partitionDisk disk2 MBR MS-DOS VOL 100%
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
# from here you can do the same thing, change the partition type with fdisk,
# and then use mkntfs (from the ntfs-3g package) to format it as NTFS

## BTW for reference here is a list of support file systems
elatok@usxxelatokm1:~$diskutil listFilesystems
Formattable file systems

These file system personalities can be used for erasing and partitioning.
When specifying a personality as a parameter to a verb, case is not considered.
Certain common aliases (also case-insensitive) are listed below as well.

-------------------------------------------------------------------------------
PERSONALITY                     USER VISIBLE NAME                               
-------------------------------------------------------------------------------
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
###

### Now let's create a GPT partition schema and put NTFS on the first partition
# clear out the partitions and make sure nothing is one them
elatok@usxxelatokm1:~$diskutil list disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                   *8.0 GB     disk2

# to put a gpt schema run the following
elatok@usxxelatokm1:~$sudo gpt create disk2
elatok@usxxelatokm1:~$diskutil list disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:      GUID_partition_scheme                        *8.0 GB     disk2
# you can also use gpt to confirm the GTP Partition scheme is on there:
elatok@usxxelatokm1:~$sudo gpt -vv show disk2
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
# now let's use gdisk to create a partition of type NTFS on it
elatok@usxxelatokm1:~$sudo gdisk /dev/disk2
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

# now we can format it with mkntfs and mount it

# To remove the gpt paritition scheme run the following
# unmount the drive and then use gdisk
elatok@usxxelatokm1:~$sudo gdisk /dev/disk2
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
###

## and of course the disk should be empty
elatok@usxxelatokm1:~$diskutil list /dev/disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                   *8.0 GB     disk2
###

### You can also use dd to zero out both locations. From the gpt show command
elatok@usxxelatokm1:~$sudo gpt -v show /dev/disk2
gpt show: /dev/disk2: mediasize=8004304896; sectorsize=512; blocks=15633408
     start      size  index  contents
         0         1         PMBR
         1         1         Pri GPT header
         2        32         Pri GPT table
        34  15633341         
  15633375        32         Sec GPT table
  15633407         1         Sec GPT header

# first let's zero out the secondary
elatok@usxxelatokm1:~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 seek=15633341
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
# the seek value is basically the value of the end of the partition seen from
# the gpt show command.

# now let's do the primary
elatok@usxxelatokm1:~$sudo dd if=/dev/zero of=/dev/disk2 bs=512 count=2
2+0 records in
2+0 records out
1024 bytes transferred in 0.000777 secs (1317879 bytes/sec)
elatok@usxxelatokm1:~$sudo gpt -v show /dev/disk2
gpt show: /dev/disk2: mediasize=8004304896; sectorsize=512; blocks=15633408
gpt show: /dev/disk2: MBR not found at sector 0
     start      size  index  contents
         0  15633408  
# and now the GPT scheme should be gone
elatok@usxxelatokm1:~$sudo gdisk -l /dev/disk2
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
###


## if you want you can zero out the disk completely with diskutil
# mine takes 24 mins
elatok@usxxelatokm1:~$sudo diskutil zeroDisk /dev/disk2
Started erase on disk2
[ - 0%................................................... ]  3% 0:24:00 
###

### diskutil can create a GPT Partition Scheme and a msdos partion all in one
# swoop, make sure no partition exists
elatok@usxxelatokm1:~$diskutil list /dev/disk2
/dev/disk2
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:                                                   *8.0 GB     disk2
# then run the following
elatok@usxxelatokm1:~$diskutil partitionDisk /dev/disk2 GPT MS-DOS VOL 100%
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
# then you can just umount the disk and reformat it with ntfs-3g since it's type is already 07:

elatok@usxxelatokm1:~$sudo gdisk -l /dev/disk2
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

# it's actually strange cause regular fdisk shows it as FAT
elatok@usxxelatokm1:~$sudo fdisk /dev/disk2
Disk: /dev/disk2	geometry: 973/255/63 [15633408 sectors]
Signature: 0xAA55
         Starting       Ending
 #: id  cyl  hd sec -  cyl  hd sec [     start -       size]
------------------------------------------------------------------------
 1: EE 1023 254  63 - 1023 254  63 [         1 -     409639] <Unknown ID>
 2: 0B 1023 254  63 - 1023 254  63 [    411648 -   15220736] Win95 FAT-32
 3: 00    0   0   0 -    0   0   0 [         0 -          0] unused      
 4: 00    0   0   0 -    0   0   0 [         0 -          0] unused    

# here is the unmount
elatok@usxxelatokm1:~$sudo diskutil unmount /dev/disk2s2
Volume VOL on disk2s2 unmounted
# and the format
tok@usxxelatokm1:~$sudo mkntfs -QF /dev/disk2s2
The partition start sector was not specified for /dev/disk2s2 and it could not be obtained automatically.  It has been set to 0.
The number of sectors per track was not specified for /dev/disk2s2 and it could not be obtained automatically.  It has been set to 0.
The number of heads was not specified for /dev/disk2s2 and it could not be obtained automatically.  It has been set to 0.
Cluster size has been automatically set to 4096 bytes.
To boot from a device, Windows needs the 'partition start sector', the 'sectors per track' and the 'number of heads' to be set.
Windows will not be able to boot from this device.
Creating NTFS volume structures.
mkntfs completed successfully. Have a nice day.
# then the mount is pretty simple.


### if you want you can replace the default mount_ntfs binary to utilize the ntfs-3g command. The process is described here. Strangely enough there is another
# utility called pdisk, which allows you to create APM (Apple Partition Map) 
# partition schemes, but diskutil can do that as well.

