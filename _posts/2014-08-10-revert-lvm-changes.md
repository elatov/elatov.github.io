---
published: true
layout: post
title: "Revert LVM Changes Using LVM Metadata Backups"
author: Karim Elatov
categories: [os,storage]
tags: [linux,debian,lvm,fdisk]
---
As I was shrinking the filesystem during my [last](/2014/08/partition-zabbix-22-mysql-database/) post, I wondered if there is an easier way to undo LVM changes. I then ran into **vgcfgrestore**/**vgcfgbackup** and I decided to give it a try.

### Setup a Test LVM Configuration
So I had a 10GB disk which wasn't used for anything:

	elatov@kerch:~$sudo fdisk -l /dev/sdb

	Disk /dev/sdb: 10.7 GB, 10737418240 bytes
	255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
	Units = sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disk identifier: 0x00000000

	Disk /dev/sdb doesn't contain a valid partition table
	
So let's partition it into two 5GB partitions:

	elatov@kerch:~$sudo fdisk /dev/sdb
	Device contains neither a valid DOS partition table, nor Sun, SGI or OSF disklabel
	Building a new DOS disklabel with disk identifier 0x22f4ab55.
	Changes will remain in memory only, until you decide to write them.
	After that, of course, the previous content won't be recoverable.

	Warning: invalid flag 0x0000 of partition table 4 will be corrected by w(rite)

	Command (m for help): n
	Partition type:
	   p   primary (0 primary, 0 extended, 4 free)
	   e   extended
	Select (default p): p
	Partition number (1-4, default 1): 
	Using default value 1
	First sector (2048-20971519, default 2048): 
	Using default value 2048
	Last sector, +sectors or +size{K,M,G} (2048-20971519, default 20971519): +5G 

	Command (m for help): n
	Partition type:
	   p   primary (1 primary, 0 extended, 3 free)
	   e   extended
	Select (default p): p
	Partition number (1-4, default 2): 
	Using default value 2
	First sector (10487808-20971519, default 10487808): 
	Using default value 10487808
	Last sector, +sectors or +size{K,M,G} (10487808-20971519, default 20971519): 
	Using default value 20971519

	Command (m for help): p

	Disk /dev/sdb: 10.7 GB, 10737418240 bytes
	255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
	Units = sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disk identifier: 0x22f4ab55

	   Device Boot      Start         End      Blocks   Id  System
	/dev/sdb1            2048    10487807     5242880   83  Linux
	/dev/sdb2        10487808    20971519     5241856   83  Linux

	Command (m for help): t
	Partition number (1-4): 1
	Hex code (type L to list codes): 8e
	Changed system type of partition 1 to 8e (Linux LVM)

	Command (m for help): t
	Partition number (1-4): 2
	Hex code (type L to list codes): 8e
	Changed system type of partition 2 to 8e (Linux LVM)

	Command (m for help): p

	Disk /dev/sdb: 10.7 GB, 10737418240 bytes
	255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
	Units = sectors of 1 * 512 = 512 bytes
	Sector size (logical/physical): 512 bytes / 512 bytes
	I/O size (minimum/optimal): 512 bytes / 512 bytes
	Disk identifier: 0x22f4ab55

	   Device Boot      Start         End      Blocks   Id  System
	/dev/sdb1            2048    10487807     5242880   8e  Linux LVM
	/dev/sdb2        10487808    20971519     5241856   8e  Linux LVM

	Command (m for help): w
	The partition table has been altered!

	Calling ioctl() to re-read partition table.
	Syncing disks.

Now we have two partitions:

	elatov@kerch:~$lsblk /dev/sdb
	NAME   MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
	sdb      8:16   0  10G  0 disk 
	├─sdb1   8:17   0   5G  0 part 
	└─sdb2   8:18   0   5G  0 part 

So let's add the first one as a physical Volume to LVM:

	elatov@kerch:~$sudo pvcreate /dev/sdb1
	  Writing physical volume data to disk "/dev/sdb1"
	  Physical volume "/dev/sdb1" successfully created

Now let's add a new volume group:

	elatov@kerch:~$sudo vgcreate test /dev/sdb1
	  Volume group "test" successfully created
	elatov@kerch:~$sudo vgs test
	  VG   #PV #LV #SN Attr   VSize VFree
	  test   1   0   0 wz--n- 5.00g 5.00g
	  
Now let's add a new logical volume taking up all the free space:

	elatov@kerch:~$sudo lvcreate -l +100%FREE -n lv test
	  Logical volume "lv" created
	elatov@kerch:~$sudo lvs test
	  LV   VG   Attr     LSize Pool Origin Data%  Move Log Copy%  Convert
	  lv   test -wi-a--- 5.00g     

So now we have **/dev/sdb1** used for the **test-lv** LV:

	elatov@kerch:~$lsblk /dev/sdb
	NAME               MAJ:MIN RM SIZE RO TYPE MOUNTPOINT
	sdb                  8:16   0  10G  0 disk 
	├─sdb1               8:17   0   5G  0 part 
	│ └─test-lv (dm-2) 254:2    0   5G  0 lvm  
	└─sdb2               8:18   0   5G  0 part 
	
So let's put **ext4** on the LV:

	elatov@kerch:~$sudo mkfs.ext4 /dev/mapper/test-lv 
	mke2fs 1.42.5 (29-Jul-2012)
	Filesystem label=
	OS type: Linux
	Block size=4096 (log=2)
	Fragment size=4096 (log=2)
	Stride=0 blocks, Stripe width=0 blocks
	327680 inodes, 1309696 blocks
	65484 blocks (5.00%) reserved for the super user
	First data block=0
	Maximum filesystem blocks=1342177280
	40 block groups
	32768 blocks per group, 32768 fragments per group
	8192 inodes per group
	Superblock backups stored on blocks: 
		32768, 98304, 163840, 229376, 294912, 819200, 884736

	Allocating group tables: done                            
	Writing inode tables: done                            
	Creating journal (32768 blocks): done
	Writing superblocks and filesystem accounting information: done 

Now let's mount it under **/test**:

	elatov@kerch:~$sudo mkdir /test
	elatov@kerch:~$sudo mount /dev/mapper/test-lv /test

	elatov@kerch:~$df -h -t ext4
	Filesystem              Size  Used Avail Use% Mounted on
	/dev/mapper/test-lv     5.0G  138M  4.6G   3% /test

### Create a Backup of the LVM metadata
Before we go any further let's make a backup:

	elatov@kerch:~$sudo vgcfgbackup -f /etc/lvm/backup/mybackup test
	  Volume group "test" successfully backed up.

You can check out available backups but running **vgcfgrestore**:

	elatov@kerch:~$sudo vgcfgrestore -l test

	  File:		/etc/lvm/archive/test_00000-1866804748.vg
	  VG name:    	test
	  Description:	Created *before* executing 'vgcreate test /dev/sdb1'
	  Backup Time:	Sun Aug 10 08:47:36 2014


	  File:		/etc/lvm/archive/test_00001-1148580986.vg
	  VG name:    	test
	  Description:	Created *before* executing 'lvcreate -l +100%FREE -n lv test'
	  Backup Time:	Sun Aug 10 08:50:52 2014


	  File:		/etc/lvm/backup/mybackup
	  VG name:    	test
	  Description:	Created *after* executing 'vgcfgbackup test'
	  Backup Time:	Sun Aug 10 08:55:10 2014

Notice there are archives and backups. By default, before any **lvm** command is executed a backup is created:

	elatov@kerch:~$grep 'archive =' /etc/lvm/lvm.conf -B 3
		# Should we maintain an archive of old metadata configurations.
		# Use 1 for Yes; 0 for No.
		# On by default.  Think very hard before turning this off.
		archive = 1

So we didn't really have to create our own, but instead of checking all the archives we know exactly which one we want to back up to. You can also check out the contents of the backup if you desire:

	elatov@kerch:~$sudo cat /etc/lvm/backup/mybackup
	# Generated by LVM2 version 2.02.95(2) (2012-03-06): Sun Aug 10 10:09:59 2014

	contents = "Text Format Volume Group"
	version = 1

	description = "vgcfgbackup -f /etc/lvm/backup/mybackup test"

	creation_host = "kerch"	# Linux kerch 3.2.0-4-amd64 #1 SMP Debian 3.2.60-1+deb7u3 x86_64
	creation_time = 1407686999	# Sun Aug 10 10:09:59 2014

	test {
		id = "gQ7NxF-uSH4-NsDQ-oWi2-jc2J-Ky6Z-TMy5n6"
		seqno = 3
		format = "lvm2" # informational
		status = ["RESIZEABLE", "READ", "WRITE"]
		flags = []
		extent_size = 8192		# 4 Megabytes
		max_lv = 0
		max_pv = 0
		metadata_copies = 0

		physical_volumes {

			pv0 {
				id = "JIrYxo-FzX5-5oMa-qwO7-SPnQ-noZ2-K4WEY5"
				device = "/dev/sdb1"	# Hint only

				status = ["ALLOCATABLE"]
				flags = []
				dev_size = 10485760	# 5 Gigabytes
				pe_start = 2048
				pe_count = 1279	# 4.99609 Gigabytes
			}
		}

		logical_volumes {

			lv {
				id = "VUA3s7-4sqU-ujuX-uHeH-CBYa-VTgk-rah3lr"
				status = ["READ", "WRITE", "VISIBLE"]
				flags = []
				creation_host = "kerch"
				creation_time = 1407682252	# 2014-08-10 08:50:52 -0600
				segment_count = 1

				segment1 {
					start_extent = 0
					extent_count = 1279	# 4.99609 Gigabytes

					type = "striped"
					stripe_count = 1	# linear

					stripes = [
						"pv0", 0
					]
				}
			}
		}
	}

We can see all the Volume information (size, extents....etc). 

### Increase the size of the Logical Volume
So let's say at this point you need some extra space. So let's add the second partition to our **test** logical volume:

	elatov@kerch:~$sudo pvcreate /dev/sdb2
	  Writing physical volume data to disk "/dev/sdb2"
	  Physical volume "/dev/sdb2" successfully created
	elatov@kerch:~$sudo vgextend test /dev/sdb2
	  Volume group "test" successfully extended
	  
Now let's extend the Logical Volume:

	elatov@kerch:~$sudo lvextend -l +100%FREE /dev/mapper/test-lv
	  Extending logical volume lv to 9.99 GiB
	  Logical volume lv successfully resized
	  
Lastly let's resize the filesystem to match the new size:

	elatov@kerch:~$sudo resize2fs -p /dev/mapper/test-lv 
	resize2fs 1.42.5 (29-Jul-2012)
	Filesystem at /dev/mapper/test-lv is mounted on /test; on-line resizing required
	old_desc_blocks = 1, new_desc_blocks = 1
	Performing an on-line resize of /dev/mapper/test-lv to 2619392 (4k) blocks.
	The filesystem on /dev/mapper/test-lv is now 2619392 blocks long.

	elatov@kerch:~$df -h -t ext4
	Filesystem              Size  Used Avail Use% Mounted on
	/dev/mapper/test-lv     9.9G  140M  9.2G   2% /test
	
That all looks good.

### Decrease the size of the Logical Volume
Now let's say you don't need the extra space and you wanted to revert the above changes. First we need to shrink the filesystem and online filesystem shrinking is not supported. So let's unmount the filesystem and then resize the filesystem:

	elatov@kerch:~$sudo umount /test
	elatov@kerch:~$sudo e2fsck -f /dev/mapper/test-lv 
	e2fsck 1.42.5 (29-Jul-2012)
	Pass 1: Checking inodes, blocks, and sizes
	Pass 2: Checking directory structure
	Pass 3: Checking directory connectivity
	Pass 4: Checking reference counts
	Pass 5: Checking group summary information
	/dev/mapper/test-lv: 11/655360 files (0.0% non-contiguous), 76783/2619392 blocks
	
	elatov@kerch:~$sudo resize2fs -p /dev/mapper/test-lv 4G
	resize2fs 1.42.5 (29-Jul-2012)
	Resizing the filesystem on /dev/mapper/test-lv to 1048576 (4k) blocks.
	Begin pass 3 (max = 80)
	Scanning inode table          XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
	The filesystem on /dev/mapper/test-lv is now 1048576 blocks long.

	elatov@kerch:~$sudo e2fsck -f /dev/mapper/test-lv 
	e2fsck 1.42.5 (29-Jul-2012)
	Pass 1: Checking inodes, blocks, and sizes
	Pass 2: Checking directory structure
	Pass 3: Checking directory connectivity
	Pass 4: Checking reference counts
	Pass 5: Checking group summary information
	/dev/mapper/test-lv: 11/262144 files (0.0% non-contiguous), 51790/1048576 blocks
	
Now in the previous post, at this point I did an **lvreduce** to change the size and I had to figure out the extent size. But now let's do an LVM restore. So prior to the restore here is how the LV looked like:

	elatov@kerch:~$sudo lvdisplay -m test
	  --- Logical volume ---
	  LV Path                /dev/test/lv
	  LV Name                lv
	  VG Name                test
	  LV UUID                VUA3s7-4sqU-ujuX-uHeH-CBYa-VTgk-rah3lr
	  LV Write Access        read/write
	  LV Creation host, time kerch, 2014-08-10 08:50:52 -0600
	  LV Status              available
	  # open                 0
	  LV Size                9.99 GiB
	  Current LE             2558
	  Segments               2
	  Allocation             inherit
	  Read ahead sectors     auto
	  - currently set to     256
	  Block device           254:2

	  --- Segments ---
	  Logical extent 0 to 1278:
		Type		linear
		Physical volume	/dev/sdb1
		Physical extents	0 to 1278

	  Logical extent 1279 to 2557:
		Type		linear
		Physical volume	/dev/sdb2
		Physical extents	0 to 1278

We can see there are two segments, now for the restore. First let's remove the volume group (I wanted to disable the volume group with **vgchange -an** but it still didn't help):

	elatov@kerch:~$sudo vgchange -an test
	  0 logical volume(s) in volume group "test" now active

We can see that 0 volumes are active. If you do a restore, it will be reverted:

	elatov@kerch:~$sudo vgcfgrestore -f /etc/lvm/backup/mybackup test
	  Restored volume group test
	elatov@kerch:~$sudo vgs
	  WARNING: Inconsistent metadata found for VG test - updating to use version 6
	  VG    #PV #LV #SN Attr   VSize  VFree
	  test    2   1   0 wz--n-  9.99g    0 

I found a forum (which is now unavailable, but the same content should be seen [here](https://access.redhat.com/solutions/144803) on this, here is a description of the issue:

> Root Cause
> 
> - LVM2 metadata is stored in a circular buffer. Older metadata may exist in the buffer if the newer metadata does not fill the buffer.
> -  If you restore metadata with a lower seqno and it doesn’t overwrite existing metadata in the buffer with a higher sequence number, the higher-sequence number metadata will be in-tact and readable.
> -  vgchange finds the newest sequence number possible and uses that version of metadata when activating a volume group. If the restored metadata is not the newest sequence number, an older sequence number may be used.
> -  If you’ve created a new LVM Physical Volume (PV) and there is no existing metadata on one or more volumes, those won’t have the higher sequence number metadata, only the restored metadata which is older, and “Inconsistent Metadata” will be reported.
> 

And here is the fix for it:

> Resolution
>
>  - Update seqno in the LVM backup file to a number higher one-higher than was reported by vgchange:
>  -  For example, if the error messages says “updating to use version 149″, change seqno to 150:
>
> 		$ grep seqno backupvg_modified.vg
> 		seqno = 150

Rather than messing with the back up file, I removed the volume group completely:

	elatov@kerch:~$sudo vgremove test
	Do you really want to remove volume group "test" containing 1 logical volumes? [y/n]: y
	  Logical volume "lv" successfully removed
	  Volume group "test" successfully removed

Then looking over the backups:

	elatov@kerch:~$sudo vgcfgrestore -l test | head -20

	  File:		/etc/lvm/archive/test_00000-1866804748.vg
	  VG name:    	test
	  Description:	Created *before* executing 'vgcreate test /dev/sdb1'
	  Backup Time:	Sun Aug 10 08:47:36 2014


	  File:		/etc/lvm/archive/test_00001-1148580986.vg
	  VG name:    	test
	  Description:	Created *before* executing 'lvcreate -l +100%FREE -n lv test'
	  Backup Time:	Sun Aug 10 08:50:52 2014


	  File:		/etc/lvm/archive/test_00002-1407279216.vg
	  VG name:    	test
	  Description:	Created *before* executing 'vgextend test /dev/sdb2'
	  Backup Time:	Sun Aug 10 09:02:11 2014

I want the one right before the **extend** command:

	elatov@kerch:~$sudo vgs test
	  Volume group "test" not found
	elatov@kerch:~$sudo vgcfgrestore -f /etc/lvm/archive/test_00002-1407279216.vg test
	  Restored volume group test
	elatov@kerch:~$sudo vgs test
	  VG   #PV #LV #SN Attr   VSize VFree
	  test   1   1   0 wz--n- 5.00g    0 
	  
Or I could've just done it from the backup that we created (either way works):

	elatov@kerch:~$sudo vgcfgrestore -f /etc/lvm/test/mybackup
		  Restored volume group test

We can see that it's 5GB. Lastly to check the segments on the LV:

	elatov@kerch:~$sudo lvdisplay -m test
	  --- Logical volume ---
	  LV Path                /dev/test/lv
	  LV Name                lv
	  VG Name                test
	  LV UUID                VUA3s7-4sqU-ujuX-uHeH-CBYa-VTgk-rah3lr
	  LV Write Access        read/write
	  LV Creation host, time kerch, 2014-08-10 08:50:52 -0600
	  LV Status              available
	  # open                 0
	  LV Size                5.00 GiB
	  Current LE             1279
	  Segments               1
	  Allocation             inherit
	  Read ahead sectors     auto
	  - currently set to     256
	  Block device           254:2

	  --- Segments ---
	  Logical extent 0 to 1278:
		Type		linear
		Physical volume	/dev/sdb1
		Physical extents	0 to 1278
   
We can see that the **/dev/sdb2** segment is no longer there. Now to mount the LV:

	elatov@kerch:~$df -h -t ext4
	Filesystem              Size  Used Avail Use% Mounted on
	/dev/mapper/test-lv     4.0G  138M  3.7G   4% /test
	
We can see the filesystem is still 4G, this is because I resized it to be a little bit smaller than the original. To get the filesystem back to the original size, just run **resize2fs** without specifying any size and it will automatically resize it to the partition size:

	elatov@kerch:~$sudo resize2fs -p /dev/mapper/test-lv 
	resize2fs 1.42.5 (29-Jul-2012)
	Filesystem at /dev/mapper/test-lv is mounted on /test; on-line resizing required
	old_desc_blocks = 1, new_desc_blocks = 1
	Performing an on-line resize of /dev/mapper/test-lv to 1309696 (4k) blocks.
	The filesystem on /dev/mapper/test-lv is now 1309696 blocks long.

	elatov@kerch:~$df -h -t ext4
	Filesystem              Size  Used Avail Use% Mounted on
	/dev/mapper/test-lv     5.0G  138M  4.6G   3% /test

For good measure do one more **fsck** on it:

	elatov@kerch:~$sudo umount /test
	elatov@kerch:~$sudo e2fsck -f /dev/mapper/test-lv 
	e2fsck 1.42.5 (29-Jul-2012)
	Pass 1: Checking inodes, blocks, and sizes
	Pass 2: Checking directory structure
	Pass 3: Checking directory connectivity
	Pass 4: Checking reference counts
	Pass 5: Checking group summary information
	/dev/mapper/test-lv: 11/327680 files (0.0% non-contiguous), 55902/1309696 blocks
	
### Modify the Backup file to Restore without Removing the Volume Group
So let's try the fix that is described in the forum. Let's figure out which sequence number we need to be higher than:

	elatov@kerch:~$sudo vgcfgrestore -f /etc/lvm/backup/mybackup test
	  Restored volume group test
	elatov@kerch:~$sudo vgs
	  WARNING: Inconsistent metadata found for VG test - updating to use version 11
	  VG    #PV #LV #SN Attr   VSize  VFree
	  kerch   1   2   0 wz--n- 15.76g    0 
	  test    2   0   0 wz--n-  9.99g 9.99g
	  
Looks like 11 is the one. Now let's find the line we need to modify:

	elatov@kerch:~$sudo grep seqno /etc/lvm/backup/mybackup
		seqno = 3
		
Let's change that setting to be *12*:

	elatov@kerch:~$sudo grep seqno /etc/lvm/backup/mybackup
		seqno = 12

and now let's try the restore (don't forget to disable the volume group with `vgchange -an test`, before applying the backup):

	elatov@kerch:~$sudo vgcfgrestore -f /etc/lvm/backup/mybackup test
	  Restored volume group test
	elatov@kerch:~$sudo vgs
	  WARNING: Inconsistent metadata found for VG test - updating to use version 13
	  Removing PV /dev/sdb2 (CxEJ9H-XKMs-jnBd-8qeY-PNYW-h4sb-eQKjMJ) that no longer belongs to VG test
	  VG    #PV #LV #SN Attr   VSize  VFree
	  kerch   1   2   0 wz--n- 15.76g    0 
	  test    1   1   0 wz--n-  5.00g    0 

Notice this time around it actually applied the backup and it removed the disk that we added to add the new space. 
