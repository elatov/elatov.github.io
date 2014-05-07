---
title: Adding a Physical Disk as a Mirror to an Existing Zpool
author: Jarret Lavallee
layout: post
permalink: /2012/08/adding-a-disk-as-a-mirror-to-an-existing-zpool/
dsq_thread_id:
  - 1404673394
categories:
  - Home Lab
  - vTip
  - ZFS
tags:
  - mirror
  - NCP
  - Nexenta
  - OS
  - Solaris
  - syspool
  - vtip
  - ZFS
---
Recently the disk that my syspool sits on started to lock up on my Nexenta (NCP) server. I decided to take this opportunity to set up a mirror to migrate the syspool (rpool) to another disk. Attaching a disk as a mirror is normally pretty easy, but this disk did not have any slices on it. Below is how I was able to mirror the OS and migrate to a new syspool disk with out taking any downtime.

First present a new disk to the server and rescan for the disk.

	  
	\# devfsadm -c disk  
	

Now check for the disk.

	  
	\# echo |format  
	Searching for disks...done
	
	AVAILABLE DISK SELECTIONS:  
	0. c8t0d0  
	/pci@0,0/pci15ad,1976@10/sd@0,0  
	1. c8t1d0  
	/pci@0,0/pci15ad,1976@10/sd@1,0  
	2. c8t2d0  
	/pci@0,0/pci15ad,1976@10/sd@2,0
	
	...
	
	Specify disk (enter its number): Specify disk (enter its number):  
	

In this case c8t1d0 is my new disk. Below is my existing syspool (please ignore the older format message. I am still running 26 on my syspool)

	  
	\# zpool status syspool  
	pool: syspool  
	state: ONLINE  
	status: The pool is formatted using an older on-disk format. The pool can  
	still be used, but some features are unavailable.  
	action: Upgrade the pool using 'zpool upgrade'. Once this is done, the  
	pool will no longer be accessible on older software versions.  
	scan: scrub repaired 0 in 0h10m with 0 errors on Mon Aug 13 09:02:23 2012  
	config:
	
	NAME STATE READ WRITE CKSUM  
	syspool ONLINE 0 0 0  
	c8t0d0s0 ONLINE 0 0 0
	
	errors: No known data errors  
	

So we will need to attach the disk as a mirror of c8t0d0s0. The problem is that c8t1d0 does not have a slice, so we can either create one using partition in format, or we can clone the slice from c8t0d0s0. Below we will clone the slice from c8t0d0s0.

	  
	\# prtvtoc /dev/dsk/c8t0d0s0 |fmthard -s - /dev/rdsk/c8t1d0s0  
	fmthard: New volume table of contents now in place.  
	

Now let&#8217;s add the disk as a mirror to c8t0d0s0. The -f is to force the operation.

	  
	\# zpool attach -f syspool c8t0d0s0 c8t1d0s0  
	

Now we need to install grub to make the new disk bootable.

	  
	root@fileserver2:/boot/grub# installgrub /boot/grub/stage1 /boot/grub/stage2 /dev/rdsk/c8t1d0s0  
	stage1 written to partition 0 sector 0 (abs 4096)  
	stage2 written to partition 0, 274 sectors starting at 50 (abs 4146)  
	

Let&#8217;s check the status of the resilver.

	  
	\# zpool status syspool  
	pool: syspool  
	state: ONLINE  
	status: The pool is formatted using an older on-disk format. The pool can  
	still be used, but some features are unavailable.  
	action: Upgrade the pool using 'zpool upgrade'. Once this is done, the  
	pool will no longer be accessible on older software versions.  
	scan: resilvered 6.51G in 0h4m with 0 errors on Mon Aug 13 09:07:23 2012  
	config:
	
	NAME STATE READ WRITE CKSUM  
	syspool ONLINE 0 0 0  
	mirror-0 ONLINE 0 0 0  
	c8t0d0s0 ONLINE 0 0 0  
	c8t1d0s0 ONLINE 0 0 0
	
	errors: No known data errors  
	

So now it is setup and ready to run as a mirrored zpool. In my case I wanted to remove the original drive, which can be done with the following command.

	  
	\# zpool detach syspool c8t1d0s0  
	

I would recommend running the syspool on a mirror, as I will when I replace the original disk.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/adding-a-disk-as-a-mirror-to-an-existing-zpool/" title=" Adding a Physical Disk as a Mirror to an Existing Zpool" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:mirror,NCP,Nexenta,OS,Solaris,syspool,vtip,ZFS,blog;button:compact;">Recently the disk that my syspool sits on started to lock up on my Nexenta (NCP) server. I decided to take this opportunity to set up a mirror to migrate...</a>
</p>