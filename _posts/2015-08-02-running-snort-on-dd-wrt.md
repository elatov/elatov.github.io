---
published: true
layout: post
title: "Running Snort on DD WRT"
author: Karim Elatov
categories: [networking,security,home_lab]
tags: [dd_wrt,snort]
---
So after trying out the [TEE module with DD-WRT](/2015/07/compile-iptables-tee-module-for-dd-wrt/), I decided to directly run **snort** on the dd-wrt router. My router is an ARM router and runs the KONG build. From the [opkg.ipk not found 404](http://www.dd-wrt.com/phpBB2/viewtopic.php?t=276631&postdays=0&postorder=asc&start=15) thread, we can use **entware** instead of **optware** on this router. The direct page with all the instructions is at [how to install entware on ARM.md](https://gist.github.com/dreamcat4/6e58639288c1a1716b85).

### Add a USB Drive to the Router

Plugin a USB stick into the router and enable USB support. To enable USB support login to the admin web interface and go to **Services** -> **USB** -> **enable Core USB Support** -> **Enable USB Storage Support**:

![sda-mounted-dd-wrt](https://dl.dropboxusercontent.com/u/24136116/blog_pics/snort-ddwrt/sda-mounted-dd-wrt_g.png)

After you save and apply settings the disk will now show up in the OS:

	root@DD-WRT:~# fdisk -l /dev/sda
	
	Disk /dev/sda: 8004 MB, 8004304896 bytes
	247 heads, 62 sectors/track, 1020 cylinders
	Units = cylinders of 15314 * 512 = 7840768 bytes
	
	   Device Boot      Start         End      Blocks  Id System



At this point we can partition the USB drive with **fdisk**. All of the instructions for that are laid out in [How To - Format And Partition External Storage Device](http://www.dd-wrt.com/wiki/index.php/How_to_-_Format_and_Partition_External_Storage_Device). After I partitioned the disk I had to follow the instructions laid out in [Can't mount ext3 USB Drive - WNDR3700](http://www.dd-wrt.com/phpBB2/viewtopic.php?t=82049&view=next&sid=3c2ec10482f44bbad36ebaa95a6a22e3) to mount it manually:

	root@DD-WRT:~# mkfs.ext3 /dev/sda1
	root@DD-WRT:~# insmod jbd
	root@DD-WRT:~# insmod mbcache
	root@DD-WRT:~# insmod ext3
	root@DD-WRT:~# mount /dev/sda1 /mnt/sda1

### Install ARM Entware

I mostly followed the instructions laid out in [how to install entware on ARM.md](https://gist.github.com/dreamcat4/6e58639288c1a1716b85). Here is what I did:

	root@DD-WRT:~#mkdir /tmp/mnt/sda1/opt
	root@DD-WRT:~#mount -o bind /tmp/mnt/sda1/opt /opt
	root@DD-WRT:~#cd /tmp/mnt/sda1
	root@DD-WRT:/tmp/mnt/sda1# wget http://qnapware.zyxmon.org/binaries-armv7/installer/entware_install_arm.sh
	Connecting to qnapware.zyxmon.org (81.4.123.217:80)
	entware_install_arm. 100% |*****************************************|  1711   0:00:00 ETA
	root@DD-WRT:/tmp/mnt/sda1# ./entware_install_arm.sh 
	Info: Checking for prerequisites and creating folders...
	Warning: Folder /opt exists!
	Info: Opkg package manager deployment...
	Connecting to qnapware.zyxmon.org (81.4.123.217:80)
	opkg                 100% |*****************************************|   128k  0:00:00 ETA
	Connecting to qnapware.zyxmon.org (81.4.123.217:80)
	opkg.conf            100% |*****************************************|   146   0:00:00 ETA
	Connecting to qnapware.zyxmon.org (81.4.123.217:80)
	ld-2.20.so           100% |*****************************************|   131k  0:00:00 ETA
	Connecting to qnapware.zyxmon.org (81.4.123.217:80)
	libc-2.20.so         100% |*****************************************|  1190k  0:00:00 ETA
	Info: Basic packages installation...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/Packages.gz.
	Updated list of available packages in /opt/var/opkg-lists/packages.
	Installing glibc-opt (2.20-5) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/glibc-opt_2.20-5_armv7soft.ipk.
	Installing libc (2.20-8b) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/libc_2.20-8b_armv7soft.ipk.
	Installing libgcc (4.8.3-8b) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/libgcc_4.8.3-8b_armv7soft.ipk.
	Installing libstdcpp (4.8.3-8b) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/libstdcpp_4.8.3-8b_armv7soft.ipk.
	Installing libpthread (2.20-8b) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/libpthread_2.20-8b_armv7soft.ipk.
	Installing librt (2.20-8b) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/librt_2.20-8b_armv7soft.ipk.
	Installing locales (2.20-8b) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/locales_2.20-8b_armv7soft.ipk.
	Downloading http://qnapware.zyxmon.org/binaries-armv7/locales_2.20-8b_armv7soft.ipk.
	Installing findutils (4.5.14-1) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/findutils_4.5.14-1_armv7soft.ipk.
	Installing terminfo (5.9-1c) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/terminfo_5.9-1c_armv7soft.ipk.
	Configuring libgcc.
	Configuring libc.
	Configuring terminfo.
	Configuring locales.
	Entware-arm uses separate locale-archive file independent from main system
	Creating locale archive - /opt/usr/lib/locale/locale-archive
	Adding en_EN.UTF-8
	Adding ru_RU.UTF-8
	/opt/usr/lib/locale/locale-archive found
	You can download locale sources from http://qnapware.zyxmon.org/sources/i18n.tar.gz
	You can add new locales for Entware-arm using /opt/bin/localedef.new
	Configuring libpthread.
	Configuring libstdcpp.
	Configuring librt.
	Configuring findutils.
	Configuring glibc-opt.
	Info: Congratulations!
	Info: If there are no errors above then Entware.arm successfully initialized.
	Info: Add /opt/bin & /opt/sbin to your PATH variable
	Info: Add '/opt/etc/init.d/rc.unslung start' to startup script for Entware.arm services to start
	Info: Found a Bug? Please report at https://github.com/zyxmon/entware-arm/issues

As a quick test I made sure I could reach the repo:
 
	root@DD-WRT:~# which opkg
	/opt/bin/opkg
	root@DD-WRT:~# opkg update
	Downloading http://qnapware.zyxmon.org/binaries-armv7/Packages.gz.
	Updated list of available packages in /opt/var/opkg-lists/packages.

Now as a quick let's install another version of the **ip** utility:

	root@DD-WRT:~# opkg install ip-legacy
	Installing ip-legacy (2.6.39-1) to root...
	Downloading http://qnapware.zyxmon.org/binaries-armv7/ip-legacy_2.6.39-1_armv7soft.ipk.
	Configuring ip-legacy.
	root@DD-WRT:~# /opt/sbin/ip -4 a
	1: lo: <LOOPBACK,MULTICAST,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN 
	    inet 127.0.0.1/8 brd 127.255.255.255 scope host lo
	9: br0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP 
	    inet 192.168.1.1/24 brd 192.168.1.255 scope global br0
	       valid_lft forever preferred_lft forever


### Install and Configure Snort
Snort is part of the **entware** packages:

	root@DD-WRT:~# opkg find snort
	snort - 2.9.7.2-1 - Snort is an open source network intrusion detection and prevention system.
	 It is capable of performing real-time traffic analysis, alerting, blocking
	 and packet logging on IP networks.  It utilizes a combination of protocol
	 analysis and pattern matching in order to detect anomalies, misuse and
	 attacks.

So a simple:

	root@DD-WRT:~# opkg install snort

Will take care of the install, after that I just followed the instructions from my [previous blog post](/2014/04/snort-debian/). First let's delete all the separate rule files directives (since I will just use **pulledpork** to get them in one file):

	root@DD-WRT:~# sed -i '' '/^include \$RULE_PATH\/.*.rules$/d' /opt/etc/snort/snort.conf

Now let's modify some of the main config file:

	root@DD-WRT:~# vi /etc/opt/snort/snort.conf

And let's modify the following in that file:

	- ipvar HOME_NET any
	- ipvar EXTERNAL_NET any
	+ ipvar HOME_NET [192.168.0.0/16,10.0.0.0/8]
	+ ipvar EXTERNAL_NET !$HOME_NET
	- var WHITE_LIST_PATH ../rules
	- var BLACK_LIST_PATH ../rules
	- var RULE_PATH ../rules
	- var PREPROC_RULE_PATH ../preproc_rules
	+ var WHITE_LIST_PATH rules
	+ var BLACK_LIST_PATH rules
	+ var RULE_PATH rules
	+ var PREPROC_RULE_PATH preproc_rules
	+ include $RULE_PATH/local.rules
	+ include $RULE_PATH/snort.rules

Also update the path to dynamic preprocessor libraries in the same file:

	dynamicpreprocessor directory /opt/lib/snort_dynamicpreprocessor                                 
	dynamicengine /opt/lib/snort_dynamicengine/libsf_engine.so                                
	#dynamicdetection directory /opt/lib/snort_dynamicrules


### Copy the Snort Rules to DD-WRT
First let's create the rules directory and install **rsync**:

	root@DD-WRT:~# mkdir /opt/etc/snort/rules
	root@DD-WRT:~# opkg install rsync

I then grabbed the rules from my *FreeBSD* machine:

	elatov@moxz:~$ sudo pulledpork.pl -c /usr/local/etc/pulledpork/pulledpork.conf -l -w

Copy the rules to dd-wrt:

	elatov@moxz:~$rsync -rvzzP /usr/local/etc/snort/rules/snort.rules root@wrt:/opt/etc/snort/rules/. --rsync-path=/opt/bin/rsync
	elatov@moxz:~$rsync -rvzzP /usr/local/etc/snort/sid-msg.map  root@wrt:/opt/etc/snort/rules/. --rsync-path=/opt/bin/rsync

Create a simple local rule:

	root@DD-WRT:~# cat /opt/etc/snort/rules/local.rules 
	suppress gen_id 129, sig_id 12

Copy the **threshold** conf:

	elatov@moxz~$scp /usr/local/etc/snort/threshold.conf root@wrt:/opt/etc/snort/.

Create white list rules:

	root@DD-WRT:~#touch /opt/etc/snort/rules/black_list.rules
	root@DD-WRT:~#touch /opt/etc/snort/rules/white_list.rules


Initially after starting snort it was running out of memory:

	Jul 18 19:32:32 DD-WRT kern.warn kernel: snort invoked oom-killer: gfp_mask=0x200da, order=0, oom_score_adj=0
	Jul 18 19:32:32 DD-WRT kern.warn kernel: CPU: 1 PID: 4169 Comm: snort Tainted: P3.10.54 #259

### Enable Swap on DD-WRT

So let's enable swap on the dd-wrt router. First let's create the swap file:

	root@DD-WRT:/tmp/mnt/sda1/swap# dd if=/dev/zero of=swap.file bs=1M count=1024
	1024+0 records in
	1024+0 records out

Now put a swap file system on the swap file:

	root@DD-WRT:/tmp/mnt/sda1/swap# mkswap swap.file 
	Setting up swapspace version 1, size = 1073737728 bytes
	UUID=23ac1ac1-4f88-439e-90a6-50cd1f9aba2d

Lastly let's enable the swap file:

	root@DD-WRT:/tmp/mnt/sda1/swap# swapon swap.file 

Lastly use the free utility to confirm it's enabled:

	root@DD-WRT:/tmp/mnt/sda1/swap# free
	             total         used         free       shared      buffers
	Mem:        255812       246968         8844            0         2048
	-/+ buffers:             244920        10892
	Swap:      1048572            0      1048572


### Start Snort

As a quick test start snort to make sure it launches all the way:

	root@DD-WRT:~#snort -A console -c /opt/etc/snort/snort.conf -i br0 --daq-dir /opt/lib/daq -l /mnt/sda1/var/log/ -p

After some time you will see the following:

	pcap DAQ configured to passive.
	Acquiring network traffic from "br0".
	Reload thread starting...
	Reload thread started, thread 0xa5608460 (4843)
	Decoding Ethernet
	
	        --== Initialization Complete ==--
	
	   ,,_     -*> Snort! <*-
	  o"  )~   Version 2.9.7.2 GRE (Build 177)
	   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
	           Copyright (C) 2014 Cisco and/or its affiliates. All rights reserved.
	           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
	           Using libpcap version 1.5.3
	           Using PCRE version: 8.36 2014-09-26
	           Using ZLIB version: 1.2.8
	
	           Rules Engine: SF_SNORT_DETECTION_ENGINE  Version 2.4  <Build 1>
	           Preprocessor Object: SF_DNS  Version 1.1  <Build 4>
	           Preprocessor Object: SF_SSLPP  Version 1.1  <Build 4>
	 		   Preprocessor Object: SF_SSH  Version 1.1  <Build 3>
	           Preprocessor Object: SF_GTP  Version 1.1  <Build 1>
	           Preprocessor Object: SF_SIP  Version 1.1  <Build 1>
	           Preprocessor Object: SF_FTPTELNET  Version 1.2  <Build 13>
	           Preprocessor Object: SF_MODBUS  Version 1.1  <Build 1>
	           Preprocessor Object: SF_REPUTATION  Version 1.1  <Build 1>
	           Preprocessor Object: SF_SMTP  Version 1.1  <Build 9>
	           Preprocessor Object: SF_IMAP  Version 1.0  <Build 1>
	           Preprocessor Object: SF_SDF  Version 1.1  <Build 1>
	           Preprocessor Object: SF_POP  Version 1.0  <Build 1>
	           Preprocessor Object: SF_DNP3  Version 1.1  <Build 1>
	           Preprocessor Object: SF_DCERPC2  Version 1.0  <Build 3>
	Commencing packet processing (pid=4789)
	07/18-14:40:18.240118  [**] [1:2013505:1] ET POLICY GNU/Linux YUM User-Agent Outbound likely related to package management [**] [Classification: Potential Corporate Privacy Violation] [Priority: 1] {TCP} 192.168.1.100:34805 -> 185.93.1.19:80

The CPU was way over utilized so after running snort for 30 minutes, I stopped it. I am sure I could optimize it to use less rules and less processing options, but I will leave that for another day. I just wanted to see if it can at least run.
