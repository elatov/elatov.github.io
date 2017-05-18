---
published: true
layout: post
title: "Build Your Own ZFS Home Storage Server"
author: Karim Elatov
categories: [storage]
tags: [zfs,omnios]
---
After getting some basic performance statistics for a very setup describe in my [previous blog](/2014/01/zfs-iscsi-benchmarks-tests/), I decided to put together my own box that will be my ZFS based Storage Server. There are a bunch of sample setups and they vary in price and perforance, here are a few I ran into:

* [Building a Homemade SAN on the Cheap: 32TB for $1,500](http://thehomeserverblog.com/esxi-storage/building-a-homemade-san-on-the-cheap-32tb-for-1500/)
* [How to build your own 180TB RAID6 storage array for $9,305](http://www.extremetech.com/computing/178757-how-to-build-your-own-180tb-raid6-storage-array-for-9305)
* [DIY NAS: 2015 Edition](http://blog.brianmoses.net/2015/01/diy-nas-2015-edition.html)

My setup is closer to the last one on the list. Since was this going to be in my home, I didn't really want to be loud but I will wanted it to be powerful enough.

### The Hardware

After looking through various pages and comparing different specs, I ended up getting the following parts:

* 3 x Seagate 2TB Desktop HDD SATA 6Gb/s 64MB Cache 3.5-Inch Internal Bare Drive (ST2000DM001) (3 x $71)
* Asus Z87I-Deluxe LGA 1150 Intel Z87 Mini ITX Motherboard ($157)
* 2 x Samsung 840 EVO 250GB 2.5-Inch SATA III Internal SSD (MZ-7TE250BW) ( 2 x $102)
* Kingston ValueRAM 16GB Kit (2x8GB Modules) 1333MHz DDR3 PC3-10666 ECC CL9 DIMM Intel Certified Server Memory KVR13E9K2/16I ($300)
* Lian Li PC-Q25B Black Aluminum Mini-ITX Tower Computer Case ($118)
* Intel I3-4130T 2.90 3 LGA 1150 Processor BX80646I34130T ($129)
* Corsair CX Series 430 Watt ATX/EPS Modular 80 PLUS Bronze ATX12V/EPS12V 384 Power Supply CX430M ($45)
* 3 x Monoprice 18-Inch SATA III 6.0 Gbps Cable with Locking Latch and 90-Degree Plug - Blue (3 x $3)
* Type 3 Flat Black SATA Cable With 4 Connectors CP-8920113 ($5)

Here is a picture while I was putting everything together :)

![storage-server-parts](https://seacloud.cc/d/480b5e8fcd/files/?p=/zfs-perf-biy-san/storage-server-parts.jpg&raw=1) 

### Local SSD Performance Tests
Initially I wanted to see how my SSDs performed and here were some dd results:

	root@zfs:~# dd if=/dev/zero of=dd.test bs=1M count=5K
	5120+0 records in
	5120+0 records out
	5368709120 bytes (5.4 GB) copied, 9.44135 s, 569 MB/s
	
My plan wasn't to use those directly, with ZFS we can use them for **L2ARC** Cache and as a **ZIL** pool. But I wanted to check what the SSDs were capable of.

#### ZIL 
There are a bunch of sites that talk about what **ZIL** is and what it's used for, I found these two sites the most useful:

* [Setting Up Separate ZFS Log Devices](http://docs.oracle.com/cd/E19253-01/819-5461/gfgaa/index.html)
* [Solaris ZFS, Synchronous Writes and the ZIL Explained](http://constantin.glez.de/blog/2010/07/solaris-zfs-synchronous-writes-and-zil-explained)

From the top site:

> The ZFS intent log (ZIL) is provided to satisfy POSIX requirements for synchronous transactions. For example, databases often require their transactions to be on stable storage devices when returning from a system call. NFS and other applications can also use fsync() to ensure data stability. By default, the ZIL is allocated from blocks within the main storage pool. In this Solaris release, you can decide if you want the ZIL blocks to continue to be allocated from the main storage pool or from a separate log device. Better performance might be possible by using separate intent log devices in your ZFS storage pool, such as with NVRAM or a dedicated disk.

And from the second site:

> Using a ZIL is faster than writing to the regular pool structure, because it doesn't come with the overhead of updating file system metadata and other housekeeping tasks. But having the ZIL on the same disk as the rest of the pool introduces a competition between the ZIL and the regular pool structure, fighting over precious IOPS resources, resulting in bad performance whenever there's a significant portion of synchronous writes.
> 
> ..
> ..
> 
> But the biggest benefit can be obtained by using ZIL devices that can execute writes fast. Really fast. And that's why we at Oracle like to make such a great fuzz about Flash memory devices. From Oracle's Sun F5100 Flash Storage Array to the Sun Flash Accelerator F20, both running on cool, space-saving Flash Modules, to standard, enterprise-class SATA/SAS SSDs.

#### L2ARC

I found a pretty good blog: [ZFS L2ARC](http://synccore.co.in/caching-technology/) and that describes what **L2ARC** is:

> The "ARC" is the ZFS main memory cache (in DRAM), which can be accessed with sub microsecond latency. An ARC read miss would normally read from disk, at millisecond latency (especially random reads). The L2ARC sits in-between, extending the main memory cache using fast storage devices - such as flash memory based SSDs (solid state disks).
> ..
> ..
> A previous ZFS feature (the ZIL) allowed you to add SSD disks as log devices to improve write performance. This means ZFS provides two dimensions for adding flash memory to the file system stack: the L2ARC for random reads, and the ZIL for writes.

The page [Explanation of ARC and L2ARC](http://www.zfsbuild.com/2010/04/15/explanation-of-arc-and-l2arc/) was pretty informative as well:

> ZFS includes two exciting features that dramatically improve the performance of read operations. I’m talking about ARC and L2ARC. ARC stands for adaptive replacement cache. ARC is a very fast cache located in the server’s memory (RAM). The amount of ARC available in a server is usually all of the memory except for 1GB.
> ..
> ..
> Another thing to remember is you still need to use SLC SSD drives for the ZIL drives, even when you use MLC SSD drives for cache drives. The SLC SSD drives used for ZIL drives dramatically improve the performance of write actions. The MLC SSD drives used as cache drives are use to improve read performance.


So there you have it, to increase write performance add an SSD drive as a **ZIL** device and to increase random read performance add an SSD drive as an **cache** device (**L2ARC**).

#### Adding ZIL and L2ARC Devices
Here is what I ran to add each:

	root@zfs:~# zpool add data log c2t0d0
	root@zfs:~# zpool add data cache c2t1d0
	
You can confirm both are added by using the **status** command:

	root@zfs:~#zpool status data
	  pool: data
	 state: ONLINE
	  scan: scrub repaired 0 in 1h35m with 0 errors on Fri Nov 13 04:05:40 2015
	config:
	
	        NAME        STATE     READ WRITE CKSUM
	        data        ONLINE       0     0     0
	          c2t3d0    ONLINE       0     0     0
	          c2t4d0    ONLINE       0     0     0
	        logs
	          c2t1d0    ONLINE       0     0     0
	        cache
	          c2t0d0    ONLINE       0     0     0
	
	errors: No known data errors


So before using the SSDs as **ZIL** and **L2ARC**, doing a quick DD test to the HDDs, I saw the following:

	root@zfs:~# dd if=/dev/zero of=/dev/dsk/c2t3d0p0 bs=1M count=2K
	2048+0 records in
	2048+0 records out
	2147483648 bytes (2.1 GB) copied, 12.8074 s, 168 MB/s
	root@zfs:~# dd if=/dev/zero of=/dev/dsk/c2t4d0p0 bs=1M count=2K
	2048+0 records in
	2048+0 records out
	2147483648 bytes (2.1 GB) copied, 12.1698 s, 176 MB/s

Then here is the after test:

	root@zfs:~# /usr/gnu/bin/dd if=/dev/zero of=/data/test.dd bs=1M count=5K
	5120+0 records in
	5120+0 records out
	5368709120 bytes (5.4 GB) copied, 11.718 s, 458 MB/s

We are definitely enjoying the SSDs cache here :) Here is the **DD** test from the *napp-it* interface with both ZIL and L2ARC (the read test is awesome):

![dd-test-new-storage-box](https://seacloud.cc/d/480b5e8fcd/files/?p=/zfs-perf-biy-san/dd-test-new-storage-box.png&raw=1)

### Remote iSCSI Performance Tests
I ran the same tests that I ran in the original post and here were the results for small IO:

![iom-small-res.png](https://seacloud.cc/d/480b5e8fcd/files/?p=/zfs-perf-biy-san/iom-small-res.png&raw=1)

The results were very similar to the original test and that's because I am still getting stuck at my 1GB NIC and Switch limitation. I think in the future I will try get a hold of a Switch that can do port link aggregation and install a multiport NIC on the ZFS machine to setup link aggreation on that side as well ([Overview of Link Aggregations](https://docs.oracle.com/cd/E23824_01/html/821-1458/fpjvl.html))

My backups were completing much faster now, here are the results after the storage upgrade:

![backups-after-storage-upgrade](https://seacloud.cc/d/480b5e8fcd/files/?p=/zfs-perf-biy-san/backups-after-storage-upgrade.png&raw=1)

You can see the results before the upgrade in my [old post](/2014/02/esxi-backups-zfs-xsibackup/).

