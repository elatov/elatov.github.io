---
title: ESXi Host Shows as Disconnected from vCenter due to Heap Depletion
author: Karim Elatov
layout: post
permalink: /2012/08/esxi-host-shows-as-disconnected-from-vcenter-due-to-heap-depletion/
dsq_thread_id:
  - 1406279066
categories:
  - Networking
tags:
  - Deep Security Virtual Appliance
  - DSVA
  - hostd
  - netGPHeap
  - vpxa
  - vShield EndPoint
---
I recently had a very interesting issue. An ESXi host was showing up as disconnected in vCenter, however going directly to the host worked fine. Trying to reconnect the host back in vCenter would fail. Just from the previous discoveries we knew that something was wrong with the vpxa service on the host. On ESX(i) there are two processes that run. First is the hostd agent, it's best described in VMware KB [1002849](http://kb.vmware.com/kb/1002849):

> The vmware-hostd management service is the main communication channel between ESX/ESXi hosts and VMkernel. If vmware-hostd fails, ESX/ESXi hosts disconnects from vCenter Server/VirtualCenter and cannot be managed, even if you try to connect to the ESX/ESXi host directly

Second is the vpxa agent, and that is best described in VMware KB [1006128](http://kb.vmware.com/kb/1006128):

> The vCenter Server Agent, also referred to as vpxa or the vmware-vpxa service, is what allows a vCenter Server to connect to a ESX host. Specifically, vpxa is the communication conduit to the hostd, which in turn communicates to the ESX kernel.

So if connecting to an ESX(i) directly with a vSphere Client then you are connecting to hostd. If you are connecting to host via vCenter then you are connecting to vpxa. From the above scenario it looks like vpxa is working properly for some reason. We ssh'ed over to the ESXi host and checked out */var/log/messages* file and we saw the following:


	Jul 26 01:26:46 vmkernel: 7:21:06:31.191 cpu3:33421)WARNING: Heap: 2218: Heap netGPHeap already at its maximumSize. Cannot expand.
	Jul 26 01:26:46 vmkernel: 7:21:06:31.191 cpu3:33421)WARNING: Heap: 2481: Heap_Align(netGPHeap, 4364/4364 bytes, 8 align) failed. caller: 0x41801c90bb4e
	Jul 26 01:26:46 vmkernel: 7:21:06:31.195 cpu2:33595)WARNING: Heap: 2218: Heap netGPHeap already at its maximumSize. Cannot expand.
	Jul 26 01:26:46 vmkernel: 7:21:06:31.195 cpu2:33595)WARNING: Heap: 2481: Heap_Align(netGPHeap, 4364/4364 bytes, 8 align) failed. caller: 0x41801c90bb4e
	Jul 26 01:26:46 vmkernel: 7:21:06:31.199 cpu3:14258)User: 2432: wantCoreDump : vpxa -enabled : 1
	Jul 26 01:26:46 vmkernel: 7:21:06:31.383 cpu11:14258)UserDump: 1485: Dumping cartel 14235 (from world 14258) to file /var/core/vpxa-zdump.000 ...


so we saw that our vpxa agent was actually crashing and it was due to the fact that our netGPHeap (Network General Purpose Heap) was depleted. Checking out the stats of the Heap:


	~ # vsish
	/> cat /system/heaps/netGPHeap-0x410001000000/stats
	Heap stats {
	Name:netGPHeap
	dynamically growable:1
	physical contiguity:Heap_PhysContigType: 1 -> Any Physical Contiguity
	memory type:MM_AllocType: 0 -> Any
	# of ranges allocated:20
	maximum # of ranges:200
	dlmalloc overhead:2448
	current heap size:67109968
	current bytes allocated:63765168
	current bytes available:3344800
	current bytes releasable:19568
	percent free of current size:0
	percent releasable of current size:0
	maximum heap size:67109968
	maximum bytes available:3344800
	percent free of max size:0
	lowest percent free of max size ever encountered:0
	...
	...


We can see that from the bottom two lines there is no free heap left. Looking at the logs right before the heap depletion, I saw a lot of these:


	Jul 26 01:26:29 vmkernel: 7:21:06:14.107 cpu10:202157)NetPort: 1165: disabled port 0x3000007
	Jul 26 01:26:29 vmkernel: 7:21:06:14.110 cpu10:202157)NetPort: 982: enabled port 0x3000007 with mac 00:50:56:84:5a:b4
	Jul 26 01:26:32 vmkernel: 7:21:06:16.812 cpu23:45460)NetPort: 1165: disabled port 0x3000003
	Jul 26 01:26:32 vmkernel: 7:21:06:16.815 cpu23:45460)NetPort: 982: enabled port 0x3000003 with mac 00:50:56:84:5a:b1
	Jul 26 01:26:32 vmkernel: 7:21:06:16.993 cpu14:202148)NetPort: 1165: disabled port 0x3000005
	Jul 26 01:26:32 vmkernel: 7:21:06:16.997 cpu14:202148)NetPort: 982: enabled port 0x3000005 with mac 00:50:56:84:5a:ba
	Jul 26 01:26:32 vmkernel: 7:21:06:17.127 cpu7:202156)NetPort: 1165: disabled port 0x3000007
	Jul 26 01:26:32 vmkernel: 7:21:06:17.130 cpu7:202156)NetPort: 982: enabled port 0x3000007 with mac 00:50:56:84:5a:b4
	Jul 26 01:26:35 vmkernel: 7:21:06:19.822 cpu18:45460)NetPort: 1165: disabled port 0x3000003
	Jul 26 01:26:35 vmkernel: 7:21:06:19.825 cpu18:45460)NetPort: 982: enabled port 0x3000003 with mac 00:50:56:84:5a:b1
	Jul 26 01:26:35 vmkernel: 7:21:06:20.003 cpu21:202147)NetPort: 1165: disabled port 0x3000005
	Jul 26 01:26:35 vmkernel: 7:21:06:20.006 cpu21:202147)NetPort: 982: enabled port 0x3000005 with mac 00:50:56:84:5a:ba
	Jul 26 01:26:35 vmkernel: 7:21:06:20.137 cpu9:202157)NetPort: 1165: disabled port 0x3000007
	Jul 26 01:26:35 vmkernel: 7:21:06:20.140 cpu9:202157)NetPort: 982: enabled port 0x3000007 with mac 00:50:56:84:5a:b4
	Jul 26 01:26:38 vmkernel: 7:21:06:22.839 cpu13:45459)NetPort: 1165: disabled port 0x3000003
	Jul 26 01:26:38 vmkernel: 7:21:06:22.842 cpu13:45459)NetPort: 982: enabled port 0x3000003 with mac 00:50:56:84:5a:b1
	Jul 26 01:26:38 vmkernel: 7:21:06:23.026 cpu13:202148)NetPort: 1165: disabled port 0x3000005
	Jul 26 01:26:38 vmkernel: 7:21:06:23.029 cpu13:202148)NetPort: 982: enabled port 0x3000005 with mac 00:50:56:84:5a:ba
	Jul 26 01:26:38 vmkernel: 7:21:06:23.157 cpu7:202156)NetPort: 1165: disabled port 0x3000007
	Jul 26 01:26:38 vmkernel: 7:21:06:23.160 cpu7:202156)NetPort: 982: enabled port 0x3000007 with mac 00:50:56:84:5a:b4
	Jul 26 01:26:41 vmkernel: 7:21:06:25.859 cpu16:45459)NetPort: 1165: disabled port 0x3000003
	Jul 26 01:26:41 vmkernel: 7:21:06:25.862 cpu16:45459)NetPort: 982: enabled port 0x3000003 with mac 00:50:56:84:5a:b1
	Jul 26 01:26:41 vmkernel: 7:21:06:26.051 cpu20:202147)NetPort: 1165: disabled port 0x3000005
	Jul 26 01:26:41 vmkernel: 7:21:06:26.054 cpu20:202147)NetPort: 982: enabled port 0x3000005 with mac 00:50:56:84:5a:ba
	Jul 26 01:26:41 vmkernel: 7:21:06:26.177 cpu4:202156)NetPort: 1165: disabled port 0x3000007
	Jul 26 01:26:41 vmkernel: 7:21:06:26.180 cpu4:202156)NetPort: 982: enabled port 0x3000007 with mac 00:50:56:84:5a:b4
	Jul 26 01:26:44 vmkernel: 7:21:06:28.869 cpu18:45460)NetPort: 1165: disabled port 0x3000003
	Jul 26 01:26:44 vmkernel: 7:21:06:28.872 cpu18:45460)NetPort: 982: enabled port 0x3000003 with mac 00:50:56:84:5a:b1
	Jul 26 01:26:44 vmkernel: 7:21:06:29.063 cpu14:202148)NetPort: 1165: disabled port 0x3000005
	Jul 26 01:26:44 vmkernel: 7:21:06:29.066 cpu14:202148)NetPort: 982: enabled port 0x3000005 with mac 00:50:56:84:5a:ba
	Jul 26 01:26:44 vmkernel: 7:21:06:29.187 cpu4:202157)NetPort: 1165: disabled port 0x3000007
	Jul 26 01:26:44 vmkernel: 7:21:06:29.190 cpu4:202157)NetPort: 982: enabled port 0x3000007 with mac 00:50:56:84:5a:b4
	Jul 26 01:26:46 vmkernel: 7:21:06:31.191 cpu3:33421)WARNING: Heap: 2218: Heap netGPHeap already at its maximumSize. Cannot expand.


For some reason a couple of Virtual Ports kept going up and down over and over again. Checking out the frequency of those messages, I saw the following:


	/var/log # grep 'enabled port' messages | awk '{print $13}' | sort | uniq -c
	1618 00:50:56:84:5a:b1
	1618 00:50:56:84:5a:b4
	1617 00:50:56:84:5a:ba


That is way too much. Checking for the VMs that those Macs belong to, I saw the following:


	~ # find . -name '*.vmx' -exec grep -H '00:50:56:84:5a:b1' {} \;
	/volumes/71641d44-1e032a47/DSVA04/DSVA04.vmx:ethernet2.generatedAddress = "00:50:56:84:5a:b1"

	~ # find . -name '*.vmx' -exec grep -H '00:50:56:84:5a:b4' {} \;
	/volumes/71641d44-1e032a47/DSVA03/dsva03.vmx:ethernet2.generatedAddress = "00:50:56:84:5a:b4"

	~ # find . -name '*.vmx' -exec grep -H '00:50:56:84:5a:ba' {} \;
	/volumes/71641d44-1e032a47/DSVA01/DSVA01.vmx:ethernet2.generatedAddress = "00:50:56:84:5a:ba"


The DSVA (Deep Security Virtual Appliance) VMs were the VMs used for vShield Endpoint with TrendMicro, more information can be found here "[Trend Micro Deep Security](http://www.vmware.com/files/pdf/partners/trendmicro/vmware-trendmicro-anti-virus-virtual-datacenter-sb-en.pdf)". From the article:

> **How vShield Endpoint Works with Trend Micro Deep Security Virtual Appliance **
> vShield Endpoint is a VMware API that is leveraged by Trend Micro Deep Security. vShield Endpoint
> plugs directly into the VMware vSphere™ platform, is deployed on a per host basis, and consists of three components:
>
> *   Hardened virtual appliance (provided by Trend Micro)
> *   vShield Endpoint in-guest driver (part of VMTools)
> *   vShield Endpoint Hypervisor module connects the Deep Security virtual appliance to the inguest driver

Usually each of the DSVA VMs is deployed on one host but we had 3 on the same host. We went ahead and powered those VMs down and then checking the NetGPheap we saw the following:

	~ # vsish
	/> cat /system/heaps/netGPHeap-0x410001000000/stats
	Heap stats {
	Name:netGPHeap
	dynamically growable:1
	physical contiguity:Heap_PhysContigType: 1 -> Any Physical Contiguity
	memory type:MM_AllocType: 0 -> Any
	# of ranges allocated:20
	maximum # of ranges:200
	dlmalloc overhead:2448
	current heap size:67109968
	current bytes allocated:63765168
	current bytes available:3344800
	current bytes releasable:19568
	percent free of current size:4
	percent releasable of current size:0
	maximum heap size:67109968
	maximum bytes available:3344800
	percent free of max size:4
	lowest percent free of max size ever encountered:0
	...
	...


We got some heap back. We then restarted the vpxa agent:


	~ # /etc/opt/init.d/vmware-vpxa stop
	Stopping vmware-vpxa:success

	~ # /etc/opt/init.d/vmware-vpxa start
	Starting vmware-vpxa:success


After the restart we were able to re-connect the host back to the vCenter.

We contacted TrendMicro and it turned out that the customer had re-installed ESXi but forgot to "un-prepare" the host from the vShield Manager. This caused the manager to constantly query those VMs and it caused the host to run out of heap which in turn caused the vpxa agent to crash. After appropriately re-configuring the vShield Endpoint Deep Security Virtual Appliances, the heap was stable and didn't run out.

### Related Posts

- [ESXi hostd Crash (5.1GA) Due to Leftover SNMP Traps](http://virtuallyhyper.com/2013/08/esxi-hostd-crash-5-1ga-due-to-leftover-snmp-traps/)

