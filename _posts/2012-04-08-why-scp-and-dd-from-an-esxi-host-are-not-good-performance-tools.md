---
title: Why SCP and DD from an ESX(i) Host are not Good Performance Tools
author: Karim Elatov
layout: post
permalink: /2012/04/why-scp-and-dd-from-an-esxi-host-are-not-good-performance-tools/
dsq_thread_id:
  - 1411159630
categories:
  - Networking
  - Storage
  - VMware
tags:
  - dd
  - io analyzer
  - netperf
  - performance
  - scp
---
I am sure many have noticed that whenever you try to scp a file to or from an ESX(i) host the performance is a little slow. Let's take the following example, here is an scp between two hosts on the same switch utilizing links that are 1GB.

	~# scp 1gb_File 10.10.10.10:/vmfs/volumes/datastore_1
	root@10.10.10.10's password:
	1gb_File                                       100% 1000MB  24.4MB/s   00:41

Now running a test with netperf from within two VMs on those two sames host, going through the same path (ie: using the same vmnics), we see the following:


	~ # /tmp/netserver
	Starting netserver at port 12865

	~ # /tmp/netperf -H 10.10.10.11 -t TCP_STREAM -l 30
	TCP STREAM TEST to 10.10.10.11
	Recv Send Send
	Socket Socket Message Elapsed
	Size Size Size Time Throughput
	bytes bytes bytes secs. 10^6bits/sec
	65536 32768 32768 30.00 939.59


So we are capable of utilizing the full 1GB but the hypervisor is limiting the userworlds other than VMs (ie: dd, scp). I do understand that this is not an apples-to-apples comparison (scp is actually reading and writing data to and from the local disks) but we are seeing scp transferring at 195Mb/s while netperf reaches 939Mb/s.

This is by design and makes perfect sense. We want all our resources dedicated to the VMs and not to any of the tools within the hypervisor. There is a pretty good article entitled [ I/O Analyzer](http://www.quora.com/What-is-the-architecture-of-VMWare-ESX-like-and-how-does-it-compare-to-other-operating-systems). It's a VMware appliance that comes pre-installed with a Linux distro and has IOmeter preloaded on it. I might do a post on how to use that tool, as well. :)

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>

  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Recover Files from an SD Card Using Linux Utilities" href="http://virtuallyhyper.com/2012/11/recover-files-from-an-sd-card-using-linux-utilities/" rel="bookmark">Recover Files from an SD Card Using Linux Utilities</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Can't Set X520 10GbE Intel NIC to Auto Negotiate on ESX(i)" href="http://virtuallyhyper.com/2012/10/cant-set-x520-10gbe-intel-nic-to-auto-negotiate-on-esxi/" rel="bookmark">Can't Set X520 10GbE Intel NIC to Auto Negotiate on ESX(i)</a>
    </li>
  </ul>
</div>

