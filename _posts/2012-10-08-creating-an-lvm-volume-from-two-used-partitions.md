---
title: Creating an LVM Logical Volume From Two Used Partitions
author: Karim Elatov
layout: post
permalink: /2012/10/creating-an-lvm-volume-from-two-used-partitions/
dsq_thread_id:
  - 1421075055
categories:
  - OS
tags:
  - /etc/fstab
  - fdisk
  - Logical Group
  - Logical Volume
  - lvm
  - Physical Volume
---
I have a machine that I have been using for years, it was before I started getting into Linux. So it started out as a Windows machine, then I installed Linux on it and Dual booted it. I then updated my hard drive in size and used Acronis to transfer all the data. It was actually pretty cool, it allowed me to increase the partitions as I was cloning the data over. Since I was using Windows with Linux, I decided to use FAT32 partitions to share data between them (this was before Linux included ntfs support by default). Regardless to say I made a lot of changes to my partitioning schema and it was all over the place. Here is how my &#8216;df&#8217; output looked like.

	  
	moxz:~>df -hT | grep sda  
	/dev/sda3 ext3 56G 27G 27G 51% /  
	/dev/sda5 vfat 71G 32K 71G 1% /mnt/stuff  
	/dev/sda4 vfat 123G 64K 123G 1% /mnt/other  
	/dev/sda1 fuseblk 25G 15G 11G 59% /mnt/c  
	

I decided to create one big partition from both of the FAT partitions (sda4 and sda5). I moved all the data off the partitions and I wanted to delete the partitions, using fdisk and then just add one big one. As I was looking at the fdisk output:

	  
	moxz:~>fdisk -l
	
	Disk /dev/sda: 300.1 GB, 300090728448 bytes  
	255 heads, 63 sectors/track, 36483 cylinders, total 586114704 sectors  
	Units = sectors of 1 * 512 = 512 bytes  
	Sector size (logical/physical): 512 bytes / 512 bytes  
	I/O size (minimum/optimal): 512 bytes / 512 bytes  
	Disk identifier: 0x3d6e3d6e
	
	Device Boot Start End Blocks Id System  
	/dev/sda1 63 51215214 25607576 7 HPFS/NTFS/exFAT  
	/dev/sda2 51215220 203880914 76332847+ f W95 Ext'd (LBA)  
	/dev/sda3 * 203880915 323131409 59625247+ 83 Linux  
	/dev/sda4 328625640 586099393 128736877 c W95 FAT32 (LBA)  
	/dev/sda5 51215283 199687949 74236333+ b W95 FAT32  
	/dev/sda6 199688013 203880914 2096451 82 Linux swap / Solaris  
	

You will notice that the partitions were out of order in sectors. sda4 started at 328625640 and ended at 586099393, while sda5 started at 51215283 and ended at 199687949. So the partitions weren&#8217;t contiguous in their sectors. This posed a problem cause my original plan of deleting the partitions and adding a big one was out of the picture. 

I decided to wipe the partitions and add them as Physical Volumes to make up an LVM Logical Volume. Here are the steps that I followed to complete the transformation:

### 1. Un-Mount the FAT partitions

Make sure you have transferred the data from the partitions

	  
	moxz:~>sudo umount /dev/sda4  
	moxz:~>sudo umount /dev/sda5  
	moxz:~>df -hT | grep sda  
	/dev/sda3 ext3 56G 27G 27G 51% /  
	/dev/sda1 fuseblk 25G 15G 11G 59% /mnt/c  
	

### 2. Convert the Partition type from vfat to lvm

**WARNING**: this will delete the partitions and without recovery steps, you won&#8217;t be able to mount them back. 

	  
	moxz:~>sudo fdisk /dev/sda  
	Welcome to fdisk (util-linux 2.21.2).
	
	Changes will remain in memory only, until you decide to write them.  
	Be careful before using the write command.
	
	Command (m for help): p
	
	Disk /dev/sda: 300.1 GB, 300090728448 bytes  
	255 heads, 63 sectors/track, 36483 cylinders, total 586114704 sectors  
	Units = sectors of 1 * 512 = 512 bytes  
	Sector size (logical/physical): 512 bytes / 512 bytes  
	I/O size (minimum/optimal): 512 bytes / 512 bytes  
	Disk identifier: 0x3d6e3d6e
	
	Device Boot Start End Blocks Id System  
	/dev/sda1 63 51215214 25607576 7 HPFS/NTFS/exFAT  
	/dev/sda2 51215220 203880914 76332847+ f W95 Ext'd (LBA)  
	/dev/sda3 * 203880915 323131409 59625247+ 83 Linux  
	/dev/sda4 328625640 586099393 128736877 c W95 FAT32 (LBA)  
	/dev/sda5 51215283 199687949 74236333+ b W95 FAT32  
	/dev/sda6 199688013 203880914 2096451 82 Linux swap / Solaris
	
	Command (m for help): t  
	Partition number (1-6): 4  
	Hex code (type L to list codes): 8e  
	Changed system type of partition 4 to 8e (Linux LVM)
	
	Command (m for help): t  
	Partition number (1-6): 5  
	Hex code (type L to list codes): 8e  
	Changed system type of partition 5 to 8e (Linux LVM)
	
	Command (m for help): p
	
	Disk /dev/sda: 300.1 GB, 300090728448 bytes  
	255 heads, 63 sectors/track, 36483 cylinders, total 586114704 sectors  
	Units = sectors of 1 * 512 = 512 bytes  
	Sector size (logical/physical): 512 bytes / 512 bytes  
	I/O size (minimum/optimal): 512 bytes / 512 bytes  
	Disk identifier: 0x3d6e3d6e
	
	Device Boot Start End Blocks Id System  
	/dev/sda1 63 51215214 25607576 7 HPFS/NTFS/exFAT  
	/dev/sda2 51215220 203880914 76332847+ f W95 Ext'd (LBA)  
	/dev/sda3 * 203880915 323131409 59625247+ 83 Linux  
	/dev/sda4 328625640 586099393 128736877 8e Linux LVM  
	/dev/sda5 51215283 199687949 74236333+ 8e Linux LVM  
	/dev/sda6 199688013 203880914 2096451 82 Linux swap / Solaris
	
	Command (m for help): w  
	The partition table has been altered!
	
	Calling ioctl() to re-read partition table.
	
	WARNING: Re-reading the partition table failed with error 16: Device or resource busy.  
	The kernel still uses the old table. The new table will be used at  
	the next reboot or after you run partprobe(8) or kpartx(8)
	
	WARNING: If you have created or modified any DOS 6.x  
	partitions, please see the fdisk manual page for additional  
	information.  
	Syncing disks.  
	

You can then run partprobe to make sure the kernel is updated regarding the new partitions:

	  
	moxz:~>sudo partprobe -s  
	/dev/sda: msdos partitions 1 2 <5 6> 3 4  
	

If you want to be safe you can reboot the machine just to make sure all is well. If you end up going that route, comment out anything regarding those partitions from &#8216;/etc/fstab&#8217; file. Here are the entries that I have in my /etc/fstab file:

	  
	moxz:~>grep -E 'stuff|other' /etc/fstab  
	UUID=15F8-0D7C /mnt/stuff vfat uid=500,umask=0077,shortname=winnt 0 0  
	UUID=4694-216B /mnt/other vfat uid=500,umask=0077,shortname=winnt 0 0  
	

Comment them out and reboot.

### 3. Add the partitions as Physical Volumes to LVM

This is done with pvcreate:

	  
	moxz:~>sudo pvcreate /dev/sda4 /dev/sda5  
	Writing physical volume data to disk "/dev/sda4"  
	Physical volume "/dev/sda4" successfully created  
	Writing physical volume data to disk "/dev/sda5"  
	Physical volume "/dev/sda5" successfully created  
	

Then check to make sure they are added:

	  
	moxz:~>sudo pvs  
	PV VG Fmt Attr PSize PFree  
	/dev/sda4 lvm2 a-- 122.77g 122.77g  
	/dev/sda5 lvm2 a-- 70.80g 70.80g  
	

### 4. Create a Logical Group from the Physical Volumes

This is done with the vgcreate command

	  
	moxz:~>sudo vgcreate vg_data /dev/sda4 /dev/sda5  
	Volume group "vg_data" successfully created  
	

Then check to make sure it&#8217;s the settings looks good:

	  
	moxz:~>sudo vgs  
	VG #PV #LV #SN Attr VSize VFree  
	vg_data 2 0 0 wz--n- 193.56g 193.56g  
	

We can see that the volume group is a total of the two partitions.

### 5. Create a Logical Volume Consuming the whole Volume Group

Let&#8217;s create a new logical volume and call it data taking up all the space of the logical group:

	  
	moxz:~>sudo lvcreate -n data -l 100%FREE vg_data  
	 password for elatov:  
	Logical volume "data" created  
	

Check to make sure it looks good.

	  
	moxz:~>sudo lvs  
	LV VG Attr LSize Pool Origin Data% Move Log Copy% Convert  
	data vg_data -wi-a\--- 193.56g  
	

### 6. Put a file system on the Logical Volume

I decided to make it ext3, since I won&#8217;t be sharing it with windows any more:

	  
	moxz:~>sudo mkfs.ext3 /dev/vg_data/data  
	mke2fs 1.42.3 (14-May-2012)  
	Filesystem label=  
	OS type: Linux  
	Block size=4096 (log=2)  
	Fragment size=4096 (log=2)  
	Stride=0 blocks, Stripe width=0 blocks  
	12689408 inodes, 50741248 blocks  
	2537062 blocks (5.00%) reserved for the super user  
	First data block=0  
	Maximum filesystem blocks=0  
	1549 block groups  
	32768 blocks per group, 32768 fragments per group  
	8192 inodes per group  
	Superblock backups stored on blocks:  
	32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,  
	4096000, 7962624, 11239424, 20480000, 23887872
	
	Allocating group tables: done  
	Writing inode tables: done  
	Creating journal (32768 blocks): done  
	Writing superblocks and filesystem accounting information: done  
	

### 7. Add the Logical Volume to /etc/fstab to be auto mounted on boot

First find out the UUID of the Logical Volume:

	  
	moxz:~>blkid | grep data  
	/dev/mapper/vg\_data-data: UUID="51d8cf3c-9808-438b-b49a-c533ef4b76e8" SEC\_TYPE="ext2" TYPE="ext3"  
	

Then add the following to the /etc/fstab file:

	  
	UUID=51d8cf3c-9808-438b-b49a-c533ef4b76e8 /mnt/data ext3 defaults 0 0  
	

Create the mount point and make sure you can mount it manually.

	  
	moxz:~>sudo mkdir /mnt/data  
	moxz:~>sudo mount /mnt/data  
	moxz.dnsd.me:~>df -hT | grep vg_data  
	/dev/mapper/vg_data-data ext3 191G 153M 181G 1% /mnt/data  
	

Reboot the machine and make sure it&#8217;s auto mounted.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Mounting an NTFS Volume in FreeBSD 9 with the /etc/fstab File" href="http://virtuallyhyper.com/2012/10/mounting-an-ntfs-volume-on-freebsd-9-with-etcfstab-file/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/mounting-an-ntfs-volume-on-freebsd-9-with-etcfstab-file/']);" rel="bookmark">Mounting an NTFS Volume in FreeBSD 9 with the /etc/fstab File</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/10/creating-an-lvm-volume-from-two-used-partitions/" title=" Creating an LVM Logical Volume From Two Used Partitions" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:/etc/fstab,fdisk,Logical Group,Logical Volume,lvm,Physical Volume,blog;button:compact;">In my previous post, I blogged about mounting an NTFS volume in FreeBSD. Now I decided to make the process easier by using the /etc/fstab file. I thought this would...</a>
</p>