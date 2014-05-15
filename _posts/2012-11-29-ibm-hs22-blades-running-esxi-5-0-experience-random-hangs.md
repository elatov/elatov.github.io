---
title: IBM HS22 Blades Running ESXi 5.0 Experience Random Hangs
author: Karim Elatov
layout: post
permalink: /2012/11/ibm-hs22-blades-running-esxi-5-0-experience-random-hangs/
dsq_thread_id:
  - 1404673715
categories:
  - Storage
  - VMware
tags:
  - esxcli storage core
  - IBM HS22
  - interrupt remapping
  - iovDisableIR
  - performance has deteriorated
  - Transient file system condition
---
Every couple of days we would see one of our ESXi host disconnect from vCenter and it would stay disconnected until we rebooted the host. Checking out the logs, prior to the reboot we would see the following:

	  
	2012-10-25T16:00:08.637Z cpu12:3560)FSS: 890: Failed to get object 1 4 8d08ab 0 0 0 0 0 0 0 0 0 0 0 :Transient file system condition, suggest retry  
	2012-10-25T16:00:10.347Z cpu0:3560)FSS: 890: Failed to get object 1 4 8d0d71 0 0 0 0 0 0 0 0 0 0 0 :Transient file system condition, suggest retry  
	2012-10-25T16:00:12.642Z cpu10:3560)FSS: 890: Failed to get object 1 4 8d1291 0 0 0 0 0 0 0 0 0 0 0 :Transient file system condition, suggest retry  
	2012-10-25T16:00:12.977Z cpu13:3564)FSS: 890: Failed to get object 1 4 8d137a 0 0 0 0 0 0 0 0 0 0 0 :Transient file system condition, suggest retry  
	2012-10-25T16:00:37.702Z cpu1:737163)WARNING: VMotionRecv: 2618: 1351180724378133 D: World 737163 waited 23.610 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.702Z cpu14:736629)WARNING: VMotionRecv: 2618: 1351180723972539 D: World 736629 waited 23.596 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.705Z cpu10:734554)WARNING: VMotionRecv: 2618: 1351180724378135 D: World 734554 waited 23.615 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.707Z cpu5:734555)WARNING: VMotionRecv: 2618: 1351180724378135 D: World 734555 waited 23.607 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.708Z cpu9:737164)WARNING: VMotionRecv: 2618: 1351180724378133 D: World 737164 waited 23.621 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.709Z cpu9:736630)WARNING: VMotionRecv: 2618: 1351180723972539 D: World 736630 waited 23.620 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.709Z cpu1:736597)WARNING: VMotionRecv: 2618: 1351180724378134 D: World 736597 waited 23.619 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:37.710Z cpu6:736598)WARNING: VMotionRecv: 2618: 1351180724378134 D: World 736598 waited 23.612 seconds to leave low memory state on dest host during pre-copy. May cause unexpected VMotion failures!  
	2012-10-25T16:00:49.911Z cpu3:3560)FSS: 890: Failed to get object 1 4 8d1f1a 0 0 0 0 0 0 0 0 0 0 0 :Transient file system condition, suggest retry  
	2012-10-25T16:01:54.286Z cpu2:8054)WARNING: ScsiDeviceIO: 1218: Device naa.600508e000000000e51b24d0a7fad20e performance has deteriorated. I/O latency increased from average value of 16512 microseconds to 331746 microseconds.  
	TSC: 0 cpu0:0)Boot: 167: Parsing boot option module /useropts.gz  
	

We would see a lot 'Transient file system condition, suggest retry' messages, which point to a storage issue. The message doesn't point out which LUN/Device is experiencing the issue, however the last message before the reboot is the following:

	  
	2012-10-25T16:01:54.286Z cpu2:8054)WARNING: ScsiDeviceIO: 1218: Device naa.600508e000000000e51b24d0a7fad20e performance has deteriorated. I/O latency increased from average value of 16512 microseconds to 331746 microseconds.  
	

We also see a couple of vMotions fail, but this is due to the fact that the host was hung. Looking for just the message from above and searching for which LUN is experiencing the issue, I saw the following:

	  
	~ # grep 'performance has deteriorated' /var/log/vmkernel.log | awk '{print $6}' | sort | uniq -c  
	3247 naa.600508e000000000e51b24d0a7fad20e  
	

There was only one LUN experiencing slow response times. Checking out for that LUN, I saw the following:

	  
	~ # esxcli storage core device list | grep ^naa.600508e000000000e51b24d0a7fad20e -A 23  
	naa.600508e000000000e51b24d0a7fad20e:  
	Display Name: LSILOGIC Serial Attached SCSI Disk (naa.600508e000000000e51b24d0a7fad20e)  
	Has Settable Display Name: true  
	Size: 139236  
	Device Type: Direct-Access  
	Multipath Plugin: NMP  
	Devfs Path: /vmfs/devices/disks/naa.600508e000000000e51b24d0a7fad20e  
	Vendor: LSILOGIC  
	Model: Logical Volume  
	Revision: 3000  
	SCSI Level: 2  
	Is Pseudo: false  
	Status: degraded  
	Is RDM Capable: true  
	Is Local: false  
	Is Removable: false  
	Is SSD: false  
	Is Offline: false  
	Is Perennially Reserved: false  
	Thin Provisioning Status: unknown  
	Attached Filters:  
	VAAI Status: unsupported  
	Other UIDs: vml.0200000000600508e000000000e51b24d0a7fad20e4c6f67696361  
	

So it was the local disk that was experiencing the issue and probably causing the host to hang. I later came across <a href="http://www-947.ibm.com/support/entry/portal/docdisplay?brand=5000008&#038;lndocid=MIGR-5089360" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www-947.ibm.com/support/entry/portal/docdisplay?brand=5000008&lndocid=MIGR-5089360']);">this</a> IBM article, here is content from the article:

> **Symptom**  
> BladeCenter HS22 or BladeCenter HS22V systems running VMware ESXi 5.0 disconnect from vCenter during runtime. The systems are either using local hard drives or drives attached via the Serial Attached SCSI (SAS) pass-thru Combination Input Output Vertical (CIOv) adapter.
> 
> **Solution**  
> IBM recommends disabling interrupt remapping within the operating system for HS22 and HS22V blades. Instructions for disabling interrupt remapping can be found in the following VMware Knowledge Base (KB) article:
> 
> http://kb.vmware.com/kb/1030265
> 
> **Additional Information**  
> Disabling interrupt remapping eliminates support for x2apic mode. X2apic mode provides 32-bit Central Processing Unit (CPU) addressability for interrupt delivery. Without x2apic, the system can only support a maximum of 255 processor cores.  
> Systems with VMware 4.x installed will not see this issue. 

That matched my issue pretty closely. I went ahead and followed the instruction laid out in VMware KB <a href="http://kb.vmware.com/kb/1030265" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1030265']);">1030265</a> and ran the following:

	  
	~ # esxcfg-advcfg -k TRUE iovDisableIR  
	

Since rebooting the host (to apply the above setting), we haven't seen any more disconnects from the blades.

