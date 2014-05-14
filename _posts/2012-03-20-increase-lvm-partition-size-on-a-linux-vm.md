---
title: Increase LVM Partition Size on a Linux VM
author: Karim Elatov
layout: post
permalink: /2012/03/increase-lvm-partition-size-on-a-linux-vm/
dsq_thread_id:
  - 1404672895
categories:
  - Home Lab
  - OS
  - Storage
  - VMware
tags:
  - ext3
  - linux
  - lvm
  - partition
---
I am running out of space on two Linux Servers that are on an ESX host and are utilizing LVMs (<a href="http://content.hccfl.edu/pollock/AUnix1/LVM.htm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://content.hccfl.edu/pollock/AUnix1/LVM.htm']);">What is LVM?</a>). I will extend the Logical Volume partition using two different methods. The first method is not very safe but will save partition numbers, and the second method is safer but will waste partitions.

# Method #1: Less safe, uses less partitions

Here is how the first server looks like:

	[root@rac1 ~]# vgdisplay
	--- Volume group ---
	VG Name VolGroup00
	System ID
	Format lvm2
	Metadata Areas 1
	Metadata Sequence No 3
	VG Access read/write
	VG Status resizable
	MAX LV 0
	Cur LV 2
	Open LV 2
	Max PV 0
	Cur PV 1
	Act PV 1
	VG Size 9.88 GB
	PE Size 32.00 MB
	Total PE 316
	Alloc PE / Size 316 / 9.88 GB
	Free PE / Size 0 / 0
	VG UUID JXKHMj-aQOn-X8Tq-Wgol-iDMm-Tiij-48PkgU
	
	[root@rac1 ~]# lvdisplay
	--- Logical volume ---
	LV Name /dev/VolGroup00/LogVol00
	VG Name VolGroup00
	LV UUID 0kzGWf-69Cp-u6nE-fYhG-XWz2-rp5u-Rn0c5s
	LV Write Access read/write
	LV Status available
	# open 1
	LV Size 7.91 GB
	Current LE 253
	Segments 1
	Allocation inherit
	Read ahead sectors auto
	- currently set to 256
	Block device 253:0
	
	--- Logical volume ---
	LV Name /dev/VolGroup00/LogVol01
	VG Name VolGroup00
	LV UUID I5kdNW-eTni-93Og-DxR2-ESsf-FcXd-RsrXt9
	LV Write Access read/write
	LV Status available
	# open 1
	LV Size 1.97 GB
	Current LE 63
	Segments 1
	Allocation inherit
	Read ahead sectors auto
	- currently set to 256
	Block device 253:1

Our Logical Volume Group (VolGroup00) is 9.88 GB and is split up into two Logical Volumes (similar to partitions).

LogVol00 (7.9GB) which is our root parition:

	[root@rac1 ~]# df -h
	Filesystem                      Size Used Avail Use% Mounted on
	/dev/mapper/VolGroup00-LogVol00 7.7G 6.9G 421M 95%   /
	/dev/sda1                       99M  16M  78M  17%   /boot
	tmpfs                           1.5G 164M 1.4G 11%   /dev/shm

and the second Logical Volume (LogVol01) is 1.9GB and is our swap &#8220;partition&#8221;:

	[root@rac1 ~]# swapon -s
	Filename Type Size Used Priority
	/dev/mapper/VolGroup00-LogVol01 partition 2064376 813344 -1

This Logical Volume Group is created from a Physical Volume (the physical parition /dev/sda2):

	[root@rac1 ~]# pvdisplay
	--- Physical volume ---
	PV Name /dev/sda2
	VG Name VolGroup00
	PV Size 9.90 GB / not usable 22.76 MB
	Allocatable yes (but full)
	PE Size (KByte) 32768
	Total PE 316
	Free PE 0
	Allocated PE 316
	PV UUID lr3bvw-L6B4-ncRF-0PeY-Xd68-gohh-8aMR15

and here is how the physical disk is paritioned:

	[root@rac1 ~]# fdisk -l /dev/sda
	Disk /dev/sda: 10.7 GB, 10737418240 bytes
	255 heads, 63 sectors/track, 1305 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 1305 10377990 8e Linux LVM

So /dev/sda1 is formated ext3 and is our boot partition and the /dev/sda2 partition is of type LVM and it&#8217;s split up into the two different Logical Volumes that I described above. For the first server, I will expand the vmdk from 10GB to 17GB and then resize the /dev/sda2 partition to be 17GB and then resize the Volume Group (VG) to be the same size. At that point, I will be able to extend the Logical Volume (LV) up to 17GB &#8211; 2GB (for swap) ~15GB, and lastly I will grow the filesystem on that LV and we will be all set. So let&#8217;s get started on this. Here is how the physical disk looks like after I expand the disk:

	[root@rac1 ~]# fdisk -l /dev/sda
	
	Disk /dev/sda: 18.2 GB, 18253611008 bytes
	255 heads, 63 sectors/track, 2219 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 1305 10377990 8e Linux LVM

Notice the new size :). So let&#8217;s go ahead and resize the partition with fdisk (delete and re-create with new size):

	[root@rac1 ~]# fdisk /dev/sda
	
	The number of cylinders for this disk is set to 2219.
	There is nothing wrong with that, but this is larger than 1024,
	and could in certain setups cause problems with:
	1) software that runs at boot time (e.g., old versions of LILO)
	2) booting and partitioning software from other OSs
	(e.g., DOS FDISK, OS/2 FDISK)
	
	Command (m for help): p
	
	Disk /dev/sda: 18.2 GB, 18253611008 bytes
	255 heads, 63 sectors/track, 2219 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 1305 10377990 8e Linux LVM
	
	Command (m for help): d
	Partition number (1-4): 2
	
	Command (m for help): n
	Command action
	e extended
	p primary partition (1-4)
	p
	Partition number (1-4): 2
	First cylinder (14-2219, default 14):
	Using default value 14
	Last cylinder or +size or +sizeM or +sizeK (14-2219, default 2219):
	Using default value 2219
	
	Command (m for help): t
	Partition number (1-4): 2
	Hex code (type L to list codes): 8e
	Changed system type of partition 2 to 8e (Linux LVM)
	
	Command (m for help): p
	
	Disk /dev/sda: 18.2 GB, 18253611008 bytes
	255 heads, 63 sectors/track, 2219 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 2219 17719695 8e Linux LVM
	
	Command (m for help): w
	The partition table has been altered!
	
	Calling ioctl() to re-read partition table.
	
	WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
	The kernel still uses the old table.
	The new table will be used at the next reboot.
	Syncing disks.

Now notice the &#8220;Device or resource busy&#8221; message. This is expected since we are currently mounting that Volume and the OS is running off of it :). So let&#8217;s go ahead and reboot the Virtual Machine (VM) just to make sure the kernel is updated with our recent changes. When we come back, we should see fdisk listing the correct size of the partition:

	[root@rac1 ~]# fdisk -l /dev/sda
	Disk /dev/sda: 18.2 GB, 18253611008 bytes
	255 heads, 63 sectors/track, 2219 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 2219 17719695 8e Linux LVM

But let&#8217;s check out the new Size of the Physical Volume (PV):

	[root@rac1 ~]# pvdisplay | grep PV Size
	PV Size 9.90 GB / not usable 22.76 MB

Huh? That is not the size that I want :). Let&#8217;s tell the Logical Volume Manager (LVM) to rescan the Physical Volume (PV):

	[root@rac1 ~]# pvresize /dev/sda2
	Physical volume "/dev/sda2" changed
	1 physical volume(s) resized / 0 physical volume(s) not resized

And now let&#8217;s check out the new size:

	[root@rac1 ~]# pvdisplay | grep PV Size
	PV Size 16.90 GB / not usable 24.20 MB

That looks better. So now let&#8217;s check out how much free space the VG has:

	[root@rac1 ~]# vgdisplay | grep Free
	Free PE / Size 224 / 7.00 GB

Yay! Let&#8217;s go ahead and add that space to the LV:

* Note- some people use lvresize or lvextend for the below operation, either one will work, it just depends on your preference. (<a href="http://www.redhat.com/archives/linux-lvm/2011-March/msg00042.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.redhat.com/archives/linux-lvm/2011-March/msg00042.html']);">lvextend and lvresize</a>)

Here is how it looks like before the extent:

	[root@rac1 ~]# lvdisplay /dev/VolGroup00/LogVol00
	--- Logical volume ---
	LV Name /dev/VolGroup00/LogVol00
	VG Name VolGroup00
	LV UUID 0kzGWf-69Cp-u6nE-fYhG-XWz2-rp5u-Rn0c5s
	LV Write Access read/write
	LV Status available
	# open 1
	LV Size 7.91 GB
	Current LE 253
	Segments 1
	Allocation inherit
	Read ahead sectors auto
	- currently set to 256
	Block device 253:0

and here is the lvextent and the new size:

	[root@rac1 ~]# lvextend -l +100%FREE /dev/VolGroup00/LogVol00
	Extending logical volume LogVol00 to 14.91 GB
	Logical volume LogVol00 successfully resized
	
	[root@rac1 ~]# lvdisplay /dev/VolGroup00/LogVol00
	--- Logical volume ---
	LV Name /dev/VolGroup00/LogVol00
	VG Name VolGroup00
	LV UUID 0kzGWf-69Cp-u6nE-fYhG-XWz2-rp5u-Rn0c5s
	LV Write Access read/write
	LV Status available
	# open 1
	LV Size 14.91 GB
	Current LE 477
	Segments 2
	Allocation inherit
	Read ahead sectors auto
	- currently set to 256
	Block device 253:0

So we are done right? Well, check out the output of df:

	[root@rac1 ~]# df -h
	Filesystem                      Size Used Avail Use% Mounted on
	/dev/mapper/VolGroup00-LogVol00 7.7G 6.9G 409M  95%  /
	/dev/sda1                       99M  16M  78M   17%  /boot
	tmpfs                           1.5G 164M 1.4G  11%  /dev/shm

It looks like we have to now resize the file system:

	[root@rac1 ~]# resize2fs /dev/VolGroup00/LogVol00
	resize2fs 1.39 (29-May-2006)
	Filesystem at /dev/VolGroup00/LogVol00 is mounted on /; on-line resizing required
	Performing an on-line resize of /dev/VolGroup00/LogVol00 to 3907584 (4k) blocks.
	The filesystem on /dev/VolGroup00/LogVol00 is now 3907584 blocks long.

And now for the new size:

	[root@rac1 ~]# df -h
	Filesystem                      Size Used Avail Use% Mounted on
	/dev/mapper/VolGroup00-LogVol00 15G  6.9G 6.9G  51%  /
	/dev/sda1                       99M  16M  78M   17%  /boot
	tmpfs                           1.5G 164M 1.4G  11%  /dev/shm

That is what we wanted to see. By the way, resize2fs works on ext3 online only (<a href="http://linux.die.net/man/8/resize2fs" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://linux.die.net/man/8/resize2fs']);">resize2fs(8) &#8211; Linux man page</a>). Other OSes provide ext2online (<a href="http://linux.die.net/man/8/ext2online" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://linux.die.net/man/8/ext2online']);">ext2online(8) &#8211; Linux man page</a>). Like I mentioned, this was probably not the safest way of doing this, so let&#8217;s go ahead and reboot the OS and force a filesystem check, just to be safe:

	[root@rac1 ~]# touch /forcefsck ; reboot
	
	Broadcast message from root (pts/1) (Sun Mar 18 13:36:22 2012):
	
	The system is going down for reboot NOW!

You can launch your vSphere client to check out the progress of the fsck.

# Method #2: Safest, requires additional partitions

Now for the second machine we will keep it safe. The second machine that I used had a very similar hard drive/partition layout:

	[root@rac2 ~]# fdisk -l /dev/sda
	
	Disk /dev/sda: 10.7 GB, 10737418240 bytes
	255 heads, 63 sectors/track, 1305 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 1305 10377990 8e Linux LVM
	
	[root@rac2 ~]# df -h
	Filesystem                      Size Used Avail Use% Mounted on
	/dev/mapper/VolGroup00-LogVol00 7.7G 6.3G 991M  87%  /
	/dev/sda1                       99M  16M  78M   17%  /boot
	tmpfs                           1.5G 164M 1.4G  11%  /dev/shm
	
	[root@rac2 ~]# pvs
	PV VG Fmt Attr PSize PFree
	/dev/sda2 VolGroup00 lvm2 a- 9.88G 0
	
	[root@rac2 ~]# vgs
	VG #PV #LV #SN Attr VSize VFree
	VolGroup00 1 2 0 wz--n- 9.88G 0
	
	[root@rac2 ~]# lvs
	LV VG Attr LSize Origin Snap% Move Log Copy% Convert
	LogVol00 VolGroup00 -wi-ao 7.91G
	LogVol01 VolGroup00 -wi-ao 1.97G

On the second machine, we are going to expand the VMDK, create a new partition from the newly expanded space, add that new partition as a PV, and then do the same steps as before. Most of the steps can be seen at the following VMware KB (<a href="http://kb.vmware.com/kb/1006371" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1006371']);">1006371</a>). Here is how fdisk looks like after I expanded the vmdk:

	[root@rac2 ~]# fdisk -l /dev/sda
	
	Disk /dev/sda: 17.1 GB, 17179869184 bytes
	255 heads, 63 sectors/track, 2088 cylinders
	Units = cylinders of 16065 * 512 = 8225280 bytes
	
	Device Boot Start End Blocks Id System
	/dev/sda1 * 1 13 104391 83 Linux
	/dev/sda2 14 1305 10377990 8e Linux LVM

Let&#8217;s create a partition from the new space:

	[root@rac2 ~]# fdisk /dev/sda
	
	The number of cylinders for this disk is set to 2088.
	There is nothing wrong with that, but this is larger than 1024,
	and could in certain setups cause problems with:
	1) software that runs at boot time (e.g., old versions of LILO)
	2) booting and partitioning software from other OSs
	(e.g., DOS FDISK, OS/2 FDISK)
	
	Command (m for help): n
	Command action
	e extended
	p primary partition (1-4)
	p
	Partition number (1-4): 3
	First cylinder (1306-2088, default 1306):
	Using default value 1306
	Last cylinder or +size or +sizeM or +sizeK (1306-2088, default 2088):
	Using default value 2088
	
	Command (m for help): t
	Partition number (1-4): 3
	Hex code (type L to list codes): 8e
	Changed system type of partition 3 to 8e (Linux LVM)
	
	Command (m for help): w
	The partition table has been altered!
	
	Calling ioctl() to re-read partition table.
	
	WARNING: Re-reading the partition table failed with error 16: Device or resource busy.
	The kernel still uses the old table.
	The new table will be used at the next reboot.
	Syncing disks.

Notice the same message as before regarding the device being busy. This time, since we are not touching the partition that is our root directory, we are in a safer place. Let&#8217;s run partprobe and confirm that we see 3 partitions:

	[root@rac2 ~]# partprobe -s /dev/sda
	/dev/sda: msdos partitions 1 2 3

Now let&#8217;s add the new partition as a PV:

	[root@rac2 ~]# pvcreate /dev/sda3
	Physical volume "/dev/sda3" successfully created

and let&#8217;s check the size:

	[root@rac2 ~]# pvdisplay /dev/sda3
	"/dev/sda3" is a new physical volume of "6.00 GB"
	--- NEW Physical volume ---
	PV Name /dev/sda3
	VG Name
	PV Size 6.00 GB
	Allocatable NO
	PE Size (KByte) 0
	Total PE 0
	Free PE 0
	Allocated PE 0
	PV UUID wvL3Vz-EEw3-FPGS-4hMo-7UZn-8ZXH-dDCkmt

Now let&#8217;s add the new PV to the VG:

	[root@rac2 ~]# vgextend VolGroup00 /dev/sda3
	Volume group "VolGroup00" successfully extended

Let&#8217;s ensure that the new space is there:

	[root@rac2 ~]# vgdisplay
	--- Volume group ---
	VG Name VolGroup00
	System ID
	Format lvm2
	Metadata Areas 2
	Metadata Sequence No 4
	VG Access read/write
	VG Status resizable
	MAX LV 0
	Cur LV 2
	Open LV 2
	Max PV 0
	Cur PV 2
	Act PV 2
	VG Size 15.84 GB
	PE Size 32.00 MB
	Total PE 507
	Alloc PE / Size 316 / 9.88 GB
	Free PE / Size 191 / 5.97 GB
	VG UUID W2Towj-pGXi-HokR-Xc80-N3o3-i8GL-4XYLEc

Now let&#8217;s extend the LV from the new partition that we added:

	[root@rac2 ~]# lvextend /dev/VolGroup00/LogVol00 /dev/sda3
	Extending logical volume LogVol00 to 13.88 GB
	Logical volume LogVol00 successfully resized

Like I mentioned before, we could use lvresize if we wanted to. The command would look something like this:

	[root@rac2 ~]# lvresize -l +100%FREE /dev/VolGroup00/LogVol00
	
	Now let&#8217;s make sure the size is correct:
	
	[root@rac2 ~]# lvdisplay /dev/VolGroup00/LogVol00
	--- Logical volume ---
	LV Name /dev/VolGroup00/LogVol00
	VG Name VolGroup00
	LV UUID t7d8y6-j5Xi-ZBhZ-BQ3t-KTN4-sT04-iV8Yjv
	LV Write Access read/write
	LV Status available
	# open 1
	LV Size 13.88 GB
	Current LE 444
	Segments 2
	Allocation inherit
	Read ahead sectors auto
	- currently set to 256
	Block device 253:0

Everything looks good, now for the final step, let&#8217;s resize the filesystem:

	[root@rac2 ~]# resize2fs /dev/VolGroup00/LogVol00
	resize2fs 1.39 (29-May-2006)
	Filesystem at /dev/VolGroup00/LogVol00 is mounted on /; on-line resizing required
	Performing an on-line resize of /dev/VolGroup00/LogVol00 to 3637248 (4k) blocks.
	The filesystem on /dev/VolGroup00/LogVol00 is now 3637248 blocks long.

Let&#8217;s see if the OS sees the correct size:

	[root@rac2 ~]# df -h
	Filesystem                      Size Used  Avail Use% Mounted on
	/dev/mapper/VolGroup00-LogVol00 14G  6.3G  6.5G  50%  /
	/dev/sda1                       99M  16M   78M   17%  /boot
	tmpfs                           1.5G 0     1.5G  0%   /dev/shm

Everything went well. Since this was a &#8220;safer&#8221; way of expanding the LV you can just reboot without running any fsck. I would say I am a pretty paranoid person, so I will force a fsck :).

	[root@rac2 ~]# shutdown -rF now
	
	Broadcast message from root (pts/1) (Sun Mar 18 14:19:10 2012):
	
	The system is going down for reboot NOW!

Again you can check the progress of the fsck through the vSphere Client if you desire to do so.

If you run out of partitions (4 primary or 3 primary and 1 extended with 11 logical partitions for SCSI: <a href="http://www.linuxforums.org/forum/installation/42716-maximum-partitions-linux.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linuxforums.org/forum/installation/42716-maximum-partitions-linux.html']);">Max Partitions on Linux</a>), you could always add a new disk to the VM and follow the same steps.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 4 File Systems and Such" href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/']);" rel="bookmark">RHCSA and RHCE Chapter 4 File Systems and Such</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 3 Disks and Partitioning" href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-3-disks-and-partitioning/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-3-disks-and-partitioning/']);" rel="bookmark">RHCSA and RHCE Chapter 3 Disks and Partitioning</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Creating an LVM Logical Volume From Two Used Partitions" href="http://virtuallyhyper.com/2012/10/creating-an-lvm-volume-from-two-used-partitions/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/creating-an-lvm-volume-from-two-used-partitions/']);" rel="bookmark">Creating an LVM Logical Volume From Two Used Partitions</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="WordPress &#8211; Error establishing a database connection, but able to connect via command line &#8211; SELinux and httpd" href="http://virtuallyhyper.com/2012/09/selinux-and-httpd/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/selinux-and-httpd/']);" rel="bookmark">WordPress &#8211; Error establishing a database connection, but able to connect via command line &#8211; SELinux and httpd</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Recreating VMFS Partitions using Hexdump" href="http://virtuallyhyper.com/2012/09/recreating-vmfs-partitions-using-hexdump/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/recreating-vmfs-partitions-using-hexdump/']);" rel="bookmark">Recreating VMFS Partitions using Hexdump</a>
    </li>
  </ul>
</div>

