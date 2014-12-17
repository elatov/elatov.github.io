---
published: true
layout: post
title: "Live Resize Root Filesystem on FreeBSD 10"
author: Karim Elatov
categories: [os]
tags: [freebsd,gpart]
---
I was running out of space on my FreeBSD machine and I decided to expand the root partition (and the fileystem on it).Before any changes, here is what I had:

	elatov@moxz:~$gpart show da0
	=>      34  31457213  da0  GPT  (15G)
	        34       128    1  freebsd-boot  (64K)
	       162  29360000    2  freebsd-ufs  (14G)
	  29360162   1572864    3  freebsd-swap  (768M)
	  30933026    524221       - free -  (256M)

Then I powered down the system and increased the space on the FreeBSD VM. After that I powered it on and saw the new free space:

	elatov@moxz:~$gpart show da0
	=>      34  52428733  da0  GPT  (25G)
	        34       128    1  freebsd-boot  (64K)
	       162  29360000    2  freebsd-ufs  (14G)
	  29360162   1572864    3  freebsd-swap  (768M)
	  30933026  21495741       - free -  (10G)

Since I will be doing this on a mounted system I had to disable the GEOM safety features:

	elatov@moxz:~$sudo sysctl kern.geom.debugflags=16
	kern.geom.debugflags: 0 -> 16

**NOTE:** after a reboot, this will be reset to the default setting.

Since the swap partition is in the middle of our partitions, we have to disable it. I had it as the 3rd partition:

	elatov@moxz:~$swapinfo
	Device          1K-blocks     Used    Avail Capacity
	/dev/da0p3         786432        0   786432     0%

Then I ran the following to disable it:

	elatov@moxz:~$sudo swapoff /dev/da0p3
	elatov@moxz:~$swapinfo
	Device          1K-blocks     Used    Avail Capacity

Then to delete the partition:

	elatov@moxz:~$sudo gpart delete -i 3 da0
	da0p3 deleted
	elatov@moxz:~$gpart show da0
	=>      34  52428733  da0  GPT  (25G)
	        34       128    1  freebsd-boot  (64K)
	       162  29360000    2  freebsd-ufs  (14G)
	  29360162  23068605       - free -  (11G)

Now let's resize the second partition, which is the root partition:

	elatov@moxz:~$df -Ph
	Filesystem    Size    Used   Avail Capacity  Mounted on
	/dev/da0p2     14G     12G    565M    96%    /
	devfs         1.0K    1.0K      0B   100%    /dev
	
	elatov@moxz:~$sudo gpart resize -i 2 -a 4k -s 24G da0
	da0p2 resized
	elatov@moxz:~$gpart show da0
	=>      34  52428733  da0  GPT  (25G)
	        34       128    1  freebsd-boot  (64K)
	       162  50331646    2  freebsd-ufs  (24G)
	  50331808   2096959       - free -  (1.0G)

Now let's re-create the swap partition:

	elatov@moxz:~$sudo gpart add -t freebsd-swap -a 4k -s 768M da0
	da0p3 added
	elatov@moxz:~$gpart show da0
	=>      34  52428733  da0  GPT  (25G)
	        34       128    1  freebsd-boot  (64K)
	       162  50331646    2  freebsd-ufs  (24G)
	  50331808   1572864    3  freebsd-swap  (768M)
	  51904672    524095       - free -  (256M)

Everything looks good so far. It looks like you can resize the **ufs** filesystem on the fly starting with FreeBSD 10. From [here](https://www.freebsd.org/doc/handbook/disks-growing.html):

> Growing a live UFS file system is only possible in FreeBSD 10.0-RELEASE and later. For earlier versions, the file system must not be mounted.

Luckily I was on FreeBSD 10:

	elatov@moxz:~$freebsd-version
	10.0-RELEASE-p14

So let's give it a shot, here is the before:

	elatov@moxz:~$df -Ph
	Filesystem    Size    Used   Avail Capacity  Mounted on
	/dev/da0p2     14G     12G    565M    96%    /
	devfs         1.0K    1.0K      0B   100%    /dev

First I went ahead and stopped as many services as I could (**mysql**,**apache24**,**splunk** and so on), and then gave it a try:

	elatov@moxz:~$sudo growfs /dev/da0p2
	Device is mounted read-write; resizing will result in temporary write suspension for /.
	It's strongly recommended to make a backup before growing the file system.
	OK to grow filesystem on /dev/da0p2, mounted on /, from 14GB to 24GB? [Yes/No] yes
	super-block backups (for fsck -b #) at:
	 29491712, 30773952, 32056192, 33338432, 34620672, 35902912, 37185152,
	 38467392, 39749632, 41031872, 42314112, 43596352, 44878592, 46160832,
	 47443072, 48725312, 50007552

It looked good (and it was really quick so I wasn't worried about any writes getting delayed):

	elatov@moxz:~$df -Ph
	Filesystem    Size    Used   Avail Capacity  Mounted on
	/dev/da0p2     23G     12G    9.5G    56%    /
	devfs         1.0K    1.0K      0B   100%    /dev

I then rebooted the system one more time to make sure all is well and it was.
