---
title: A Few Words on VOMA
author: Jarret Lavallee
layout: post
permalink: /2012/09/a-few-words-on-voma/
dsq_thread_id:
  - 1404673439
categories:
  - Storage
  - VMware
tags:
  - 5.1
  - corruption
  - ESXi
  - filesystem
  - heartbeat
  - vmfs
  - vmfs3
  - VMFS5
  - voma
---
VOMA is the vSphere On-Disk Metadata Analyzer that shipped with ESXi 5.1. It allows you to check the metadata on a LUN without having to upload a dump to support. Cormac Hogan did a write up introducing the feature on <a href="http://cormachogan.com/2012/09/04/vsphere-5-1-storage-enhancements-part-1-vmfs-5/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://cormachogan.com/2012/09/04/vsphere-5-1-storage-enhancements-part-1-vmfs-5/']);" target="_blank" class="broken_link">his blog</a>. I am not going to go really deep into the tool, but I can speak about the operation.

**Note:** If you suspect corruption on the VMFS volume please **do not** change anything on the datastore. VOMA is a great tool, but should really only be run with someone that knows what implications the output means, so I suggest calling support if you suspect any corruption.

VOMA operates in read-only mode, meaning that it will not fix any errors. It requires the datastore to only be accessed by the host running VOMA. So you will have to unmount the datastore on the other hosts.

When running VOMA, we need to give it the path to the partition with VMFS on it. We can get that path pretty easily.

	  
	\# esxcfg-scsidevs -m |grep iscsi_test  
	naa.600144f0e8cb470000005053b9b50001:1 /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001:1 505427ac-3acc9d52-406d-d027886f3502 0 iscsi_test  
	

We can run the tool against the datastore. Note that in this case are using the full path to the partition. The &#8216;:1&#8242; denotes the first partition.

	  
	\# voma -m vmfs -f check -d /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001:1  
	Checking if device is actively used by other hosts  
	Found 1 actively heartbeating hosts on device '/vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001:1'  
	1): MAC address d0:27:88:6f:38:82  
	

VOMA tells us that other hosts are accessing this datastore so we cannot do anything with it. I stopped the VMs on the other host and ran the command again.

	  
	\# voma -m vmfs -f check -d /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001:1  
	Checking if device is actively used by other hosts  
	Running VMFS Checker version 0.9 in check mode  
	Initializing LVM metadata, Basic Checks will be done  
	Phase 1: Checking VMFS header and resource files  
	Detected file system (labeled:'iscsi_test') with UUID:505427ac-3acc9d52-406d-d027886f3502, Version 5:58  
	Phase 2: Checking VMFS heartbeat region  
	Phase 3: Checking all file descriptors.  
	Phase 4: Checking pathname and connectivity.  
	Phase 5: Checking resource reference counts.
	
	Total Errors Found: 0  
	

We can see that there are no problems on this volume. To illustrate what the output looks like with a bad heartbeat, I corrupted a heartbeat. To do this I wrote some random data over the heartbeat that sits in the sector starting at 0&#215;1500000. 0&#215;1500000 offset means that it is 22020096 bytes from the begining of the disk, so using dd we can seek to this offset and write 512 bytes (one sector). For more information about offsets please see <a href="http://virtuallyhyper.com/2012/09/recreating-vmfs-partitions-using-hexdump" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/recreating-vmfs-partitions-using-hexdump']);" target="_blank">this post</a>. Running the following command **will cause heartbeat corruption**. 

	  
	\# dd if=/dev/random of=/vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001 bs=1 count=512 seek=22020096 conv=notrunc  
	

Below is the output with a <a href="http://kb.vmware.com/kb/1020645" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1020645']);" target="_blank">corrupt heartbeat</a>, if your datastore looks like this, VMware support may be able to repair the damage.

	  
	\# voma -m vmfs -f check -d /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001:1  
	Checking if device is actively used by other hosts  
	Running VMFS Checker version 0.9 in check mode  
	Initializing LVM metadata, Basic Checks will be done  
	Phase 1: Checking VMFS header and resource files  
	Detected file system (labeled:'iscsi_test') with UUID:505427ac-3acc9d52-406d-d027886f3502, Version 5:58  
	Phase 2: Checking VMFS heartbeat region  
	ON-DISK ERROR: Invalid HB address  
	Phase 3: Checking all file descriptors.  
	Phase 4: Checking pathname and connectivity.  
	Phase 5: Checking resource reference counts.
	
	Total Errors Found: 1  
	

From the output above, you can see that there is a single error found on the datastore. The error is that the heartbeat address is invalid. If you see this message please contact VMware support.

One interesting thing about VOMA, is that it gets a reservation on the volume to do the scan. This is to have atonamous metadata. It would be impossible to check the metadata if it was constantly changing. So you will see out of band reservation messages in the logs when running VOMA.

	  
	2012-09-15T07:31:59.579Z cpu0:66489)Resv: 407: Executed out-of-band reserve on naa.600144f0e8cb470000005053b9b50001  
	2012-09-15T07:32:00.246Z cpu2:66489)Resv: 407: Executed out-of-band release on naa.600144f0e8cb470000005053b9b50001  
	

