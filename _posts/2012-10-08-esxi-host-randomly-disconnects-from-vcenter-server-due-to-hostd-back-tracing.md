---
title: 'ESX(i) Host  Randomly Disconnects from vCenter Server due to Hostd Backtracing'
author: Karim Elatov
layout: post
permalink: /2012/10/esxi-host-randomly-disconnects-from-vcenter-server-due-to-hostd-back-tracing/
dsq_thread_id:
  - 1406826243
categories:
  - Networking
  - VMware
tags:
  - /var/log/vmware/hostd.log
  - ESXi 4.1U3
  - Hostd Core Dump
  - vix-async-pipe-zdump.000
---
At random times, I would see the following messages from my SNMP Server regarding my ESX(i) hosts:

> Time of Event: 10/4/2012 3:05:37 AM  
> Source Machine Name: SNMP_Server  
> Object Name: SNMP: esx-08.local.com [10.0.1.159]  
> Detail Message: Retrieval of sysUpTime.0 from esx-08.local.com [10.0.1.159] resulted in an SNMP timeout.

So my ESXi host was not responding to SNMP queries. I decided to check out what was happening on the host at the time. The above messages were in local time, while the logs on an ESXi host are in UTC. So the disconnect happened at 3:05 AM CDT. Converting that time to UTC, I get the following:

	  
	$ TZ=UTC date -d '3:05 CDT Oct 4 2012'  
	Thu Oct 4 08:05:00 UTC 2012  
	

Around that time, I see the following in /var/log/messages on the ESXi Host:

	  
	Oct 4 08:02:38 vmkernel: 40:12:01:41.149 cpu13:7448)User: 2432: wantCoreDump : vix-async-pipe -enabled : 1  
	Oct 4 08:02:38 vmkernel: 40:12:01:41.386 cpu10:7448)UserDump: 1485: Dumping cartel 5551 (from world 7448) to file /var/core/vix-async-pipe-zdump.000 ...  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.021 cpu13:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.032 cpu3:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.042 cpu3:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.053 cpu13:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.063 cpu13:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.073 cpu13:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:07:36 vmkernel: 40:12:06:39.084 cpu13:19130195)hpilo 0000:01:04.2: Open could not dequeue a packet  
	Oct 4 08:11:46 vmkernel: 40:12:10:48.668 cpu15:7448)UserDump: 1587: Userworld coredump complete.  
	

It looks like hostd core dumped. I then ran across VMware KB <a href="http://kb.vmware.com/kb/2017008" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2017008']);">2017008</a> which matched my issue and symptoms. For example here are some of the symptoms:

> *   The hostd.log is terminated without mentioning rotating&#8230;
> *   You may see hostd core(s) generated under /var/core/core-vix-async-pipe-pid-EPOCH.gz

Checking out my hostd logs, I saw that it indeed terminated without the &#8216;rotating&#8230;&#8217; line:

	  
	/var/log/vmware/ # tail -2 hostd-386.log  
	[2012-10-04 08:02:36.167 1F5BDB90 verbose 'NetConfigProvider'] FetchFn: List of pnics opted out  
	[2012-10-04 08:02:37.398 1F5BDB90 verbose 'NetConfigProvider'] FetchFn: List of pnics opted out  
	

And of course here is core dump:

	  
	~ # ls /var/core/vix*  
	/var/core/vix-async-pipe-zdump.000  
	

The issue is fixed in 4.1U3. Checking out my version:

	  
	~ # vmware -v  
	VMware ESXi 4.1.0 build-702113  
	

From &#8220;<a href="http://www.virten.net/vmware/esxi-release-build-number-history/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/vmware/esxi-release-build-number-history/']);">ESXi Release and Build Number History</a>&#8220;, we can see that build # 702113 is 4.1P7 and 4.1U3 is build # 800380, so I was definitely behind on updates. After updating to 4.1U3 the random disconnects stopped.

