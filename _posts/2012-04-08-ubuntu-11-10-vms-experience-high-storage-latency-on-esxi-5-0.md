---
title: Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0
author: Karim Elatov
layout: post
permalink: /2012/04/ubuntu-11-10-vms-experience-high-storage-latency-on-esxi-5-0/
dsq_thread_id:
  - 1405152269
categories:
  - Home Lab
  - OS
  - Storage
  - VMware
tags:
  - apt-xapian-index
  - esxtop
  - io latency
  - iostat
  - ubuntu
---
I have a lab environment where I deploy about 30 VMs on one physical server and run Linux (Ubuntu 11.10) on all the VMs. Here are the specs of the physical machine:

	~ # vsish -e cat /hardware/bios/dmiInfo | head -4
	System Information (type1) {
	Product Name:Seabream
	Vendor Name:InventecESC
	Serial Number:P1237010411

	~ # vsish -e cat /hardware/cpu/cpuInfo | grep -E 'Number\ of \cores|Number\ of\ CPU'
	Number of cores:8
	Number of CPUs (threads):8

	~ # vsish -e cat /hardware/cpu/cpuModelName
	Intel(R) Xeon(R) CPU X5355 @ 2.66GHz

	~ # vsish -e cat /memory/comprehensive | head -2
	Comprehensive {
	Physical memory estimate:8388084 KB

So 8 cores at 2.66GHz and 8GB of RAM, nothing crazy. Each VM has the minimum amount of RAM (192MB) and it actually runs pretty well. I was looking over esxtop and at random period of times, I saw different VMs experiencing high latency. Here is what I saw.

![esxtop_latency](https://github.com/elatov/uploads/raw/master/2012/03/esxtop_latency.png)

To get to this screen just launch esxtop and hit 'v' for "disk VMs". On ESXi 5.0 the latency is automatically displayed in this view. If you are on 4.x, after selecting 'v' you can type in 'f' and that will show you a list of available columns, select the latency columns and you will see the same as above. From the above picture we see VM "uaclass39" and "uaclass17" experiencing latency up to 20 milliseconds. At certain times 20 VMs would experience the same issue. I saw this lantency be steady for a couple of minutes. More information regarding latency can be seen at this communities page ([Performance Troubleshooting for VMware vSphere™ 4.1](http://communities.vmware.com/docs/DOC-11812)", check out the section entitled '7.3.13. Check for Slow or Under-Sized Storage Device'.

I decided to take a look at what the VM is doing and why it was experiencing such high read and write latency. So I ssh'ed over to one of the VMs and I launched top, and here is I saw:![Ubuntu_11_10_top](https://github.com/elatov/uploads/raw/master/2012/03/Ubuntu_11_10_top.png)

Check out the %wa (it's 97%). Looking at the man page of 'top', I see the following:


	wa -- iowait
	Amount of time the CPU has been waiting for I/O to complete.


Something is doing a lot of IO and the biggest cpu and memory user is a process called update-apt-xapi. Looking at the man page of 'ps', I see the folllowing:


	PROCESS STATE CODES
	Here are the different values that the s, stat and state output
	specifiers (header "STAT" or "S") will display to describe the state of
	a process:
	D uninterruptible sleep (usually IO)
	R running or runnable (on run queue)
	S interruptible sleep (waiting for an event to complete)
	T stopped, either by a job control signal or because it is being
	traced.
	W paging (not valid since the 2.6.xx kernel)
	X dead (should never be seen)
	Z defunct ("zombie") process, terminated but not reaped by its
	parent.


I wanted to check what is in disk IO state, so I ran the below:

	root@uaclass39:~# ps -efly | grep ^D
	D root 1570 1 3 90 10 137492 58296 sleep_ 16:54 ? 00:00:15 /usr/bin/python /usr/sbin/update-apt-xapian-index --force --quiet

So it looks like the "update-apt-xapian-index" is what's causing the high disk IO. I then wanted to check how much IO was happening, so I ran the following:


	root@uaclass39:~# iostat 1 5 /dev/sda
	Linux 3.0.0-17-virtual (uaclass39) 03/29/2012 _x86_64_ (1 CPU)

	avg-cpu: %user %nice %system %iowait %steal %idle
	1.03 2.09 1.94 44.96 0.00 49.99

	Device: tps kB_read/s kB_wrtn/s kB_read kB_wrtn
	sda 169.03 5636.54 312.89 7418419 411800

	avg-cpu: %user %nice %system %iowait %steal %idle
	0.00 1.98 2.97 95.05 0.00 0.00

	Device: tps kB_read/s kB_wrtn/s kB_read kB_wrtn
	sda 609.90 16419.80 91.09 16584 92

	avg-cpu: %user %nice %system %iowait %steal %idle
	0.00 2.00 2.00 96.00 0.00 0.00

	Device: tps kB_read/s kB_wrtn/s kB_read kB_wrtn
	sda 563.00 14884.00 40.00 14884 40

	avg-cpu: %user %nice %system %iowait %steal %idle
	0.97 1.94 0.97 96.12 0.00 0.00

	Device: tps kB_read/s kB_wrtn/s kB_read kB_wrtn
	sda 779.61 20749.51 38.83 21372 40

	avg-cpu: %user %nice %system %iowait %steal %idle
	0.00 7.69 1.92 90.38 0.00 0.00

	Device: tps kB_read/s kB_wrtn/s kB_read kB_wrtn
	sda 658.65 15638.46 319.23 16264 332


We consistently see very high %iowait and our reads are at ~15-20MB/s. Don't forget this is on local storage too :)
I wanted to find out what this apt-xapian process is, I did some research and I found a bug ([363695](https://bugs.launchpad.net/ubuntu/+source/apt-xapian-index/+bug/363695)) from ubuntu. They tried to fix it by throttling the IO by using ionice, my install had that enabled:


	root@uaclass39:/etc/cron.weekly# grep -i ionice apt-xapian-index
	# ionice should not be called in a virtual environment
	egrep -q '(envID|VxID):.*[1-9]' /proc/self/status || IONICE=/usr/bin/ionice
	if [ -x "$IONICE" ]
	nice -n 19 $IONICE -c 3 $CMD --quiet


but it still caused an issue and it states that ionice should not be used in a virtualized environment. So I decided to just disable it. Since I had setup ssh keys for grading purposes, I wrote this script to disable apt-xapian-index from auto running weekly:


	#!/bin/bash

	HOSTS="uaclass01 uaclass02 uaclass03 ..."

	for i in $HOSTS;do
	echo $i
	/usr/bin/ssh $i '/bin/chmod 0 /etc/cron.weekly/apt-xapian-index'
	done


A more appropriate fix would be to completely remove the package:


	root@uaclass39:~$ dpkg -l | grep apt-xapian
	ii apt-xapian-index 0.44ubuntu4 maintenance and search tools for a Xapian index of Debian packages

	root@uaclass39:~$ apt-get --purge remove apt-xapian-index
	Reading package lists... Done
	Building dependency tree
	Reading state information... Done
	The following packages will be REMOVED:
	apt-xapian-index*
	0 upgraded, 0 newly installed, 1 to remove and 0 not upgraded.
	After this operation, 483 kB disk space will be freed.
	Do you want to continue [Y/n]? Y
	(Reading database ... 28747 files and directories currently installed.)
	Removing apt-xapian-index ...
	Removing index /var/lib/apt-xapian-index...
	Purging configuration files for apt-xapian-index ...
	Removing index /var/lib/apt-xapian-index...
	Processing triggers for man-db ...


But I didn't want to do that just yet. Just as an FYI, here are the spec of each VM:


	root@uaclass39:~# uname -a
	Linux uaclass39 3.0.0-17-virtual #30-Ubuntu SMP Thu Mar 8 23:45:51 UTC 2012 x86_64 x86_64 x86_64 GNU/Linux

	root@uaclass39:~# lsb_release -a
	No LSB modules are available.
	Distributor ID: Ubuntu
	Description: Ubuntu 11.10
	Release: 11.10
	Codename: oneiric

	root@uaclass39:~# free -m
	total used free shared buffers cached
	Mem: 176 167 8 0 10 107
	-/+ buffers/cache: 50 126
	Swap: 379 35 344

	root@uaclass39:~# x86info
	x86info v1.25. Dave Jones 2001-2009

	Found 1 CPU
	--------------------------------------------------------------------------
	EFamily: 0 EModel: 0 Family: 6 Model: 15 Stepping: 7
	CPU Model: Core 2 Quad (Kentsfield)
	Processor name string: Intel(R) Xeon(R) CPU X5355 @ 2.66GHz
	Type: 0 (Original OEM) Brand: 0 (Unsupported)
	Number of cores per physical package=1
	Number of logical processors per socket=1
	Number of logical processors per core=1
	APIC ID: 0x0 Package: 0 Core: 0 SMT ID 0



Since the apt-xapian-index just indexes all the aptitude packages, I didn't really see a problem with disabling it. After I disabled that cron job, I haven't seen any high latency on any of the VMs.

### Related Posts

- [Sharing a File Encrypted by EncFS with Android and Linux Systems with Google Drive](http://virtuallyhyper.com/2013/02/sharing-a-file-encrypted-by-encfs-with-android-and-linux-systems-with-google-drive/)
- [Plot Esxtop Data With gnuplot](http://virtuallyhyper.com/2013/01/plot-esxtop-data-with-gnuplot/)
- [VMs are Slow to Boot from an HP MSA 2000 Array](http://virtuallyhyper.com/2012/11/vms-are-slow-to-boot-from-an-hp-msa-2000-array/)
- [Seeing High KAVG with Microsoft Cluster Services  (MSCS) RDMs](http://virtuallyhyper.com/2012/08/seeing-high-kavg-with-microsoft-cluster-services-mscs-rdms/)

