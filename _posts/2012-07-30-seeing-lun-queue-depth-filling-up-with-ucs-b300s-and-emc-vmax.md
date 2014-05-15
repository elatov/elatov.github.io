---
title: Seeing LUN Queue Depth Filling up with UCS B230/B200 using Cisco VICs and EMC VMAX
author: Karim Elatov
layout: post
permalink: /2012/07/seeing-lun-queue-depth-filling-up-with-ucs-b300s-and-emc-vmax/
dsq_thread_id:
  - 1404673321
categories:
  - Storage
  - VMware
tags:
  - Adapter Queue Length
  - Adaptive Queue Depth Algorithm
  - AQLEN
  - Disk.SchedNumReqOutstanding
  - DQLEN
  - DSNRO
  - LUN/Device Queue Length
  - Queue Depth
  - SIOC
  - Storage Queues
---
Recently I ran into an issue where the device queue length was filling up. Looking at esxtop here is how it looked like:<img class="alignnone size-full wp-image-1777" title="full_queue_depth_s" src="http://virtuallyhyper.com/wp-content/uploads/2012/07/full_queue_depth_s.png" alt="full queue depth s Seeing LUN Queue Depth Filling up with UCS B230/B200 using Cisco VICs and EMC VMAX" width="1617" height="184" />As I ran into this issue I realized I didn't really know of all the different aspects of all the different queues at different storage layers. I also didn't realize of all the possible ways to help out with the issue. First let's tackle the description of all the different queues at different layers. There is an excellent VMware blog on this topic: "<a href="http://blogs.vmware.com/vsphere/2012/07/troubleshooting-storage-performance-in-vsphere-part-5-storage-queues.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2012/07/troubleshooting-storage-performance-in-vsphere-part-5-storage-queues.html']);">Troubleshooting Storage Performance in vSphere – Storage Queues</a>". I will shamelessly copy their diagram just to make it easier to follow the blog:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/07/storage_queues1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/07/storage_queues1.png']);"><img class="alignnone size-full wp-image-1779" title="storage_queues" src="http://virtuallyhyper.com/wp-content/uploads/2012/07/storage_queues1.png" alt="storage queues1 Seeing LUN Queue Depth Filling up with UCS B230/B200 using Cisco VICs and EMC VMAX" width="836" height="624" /></a>

Here is an excerpt from the same blog:

> A World queue (a queue per virtual machine), an Adapter queue (a queue per HBA in the host), and a Device/LUN queue (a queue per LUN per Adapter). Finally at the bottom of the storage stack there are queues at the storage device, for instance the front-end storage port has a queue for all incoming I/Os on that port.

and also this:

> As you can see, the I/O requests flow into the per virtual machine queue, which then flows into the per HBA queue, and then finally the I/O flows from the adapter queue into the per LUN queue for the LUN the I/O is going to. From the default sizes you can see that each VM is able to issue 32 concurrent I/O requests, the adapter queue beneath it is generally quite large and can normally accept all those I/O requests, but the LUN queue beneath that typically only has a size of 32 itself.

If you want to check what your queues are currently set to, you can take a look at <a href="http://kb.vmware.com/kb/1027901" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1027901']);">VMware KB 1027901</a>.

Not a lot of things touch upon for the Adapter Queue Length (AQLEN). The Emulex driver has an option for this (but apparently this is not settable after ESX 3.5, more information <a href="http://www.yellow-bricks.com/2008/01/31/queue-depth-and-alike-settings-lost-after-an-upgrade-to-esx-35/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2008/01/31/queue-depth-and-alike-settings-lost-after-an-upgrade-to-esx-35/']);">here</a>):

	  
	~ # vmkload_mod -s lpfc820 | grep lpfc_hba_queue_depth -A 1  
	lpfc_hba_queue_depth: int  
	Max number of FCP commands we can queue to a lpfc HBA  
	

If you are using Software iSCSI there is an option for this as well:

	  
	~ # vmkload_mod -s iscsi_vmk | grep iscsivmk_HostQDepth -A 1  
	iscsivmk_HostQDepth: int  
	Maximum Outstanding Commands Per Adapter  
	

Like mentioned in the above VMware blog the typical size is 1024 (or something in the thousands) but usually the default size is good. The vendor knows the best option for this piece of hardware and it's rarely possible to change that value.

The interesting setting is the LUN/Device Queue Length (DQLEN). There are many ways to tweak this option. The first way is to do it via the driver, more on this in <a href="http://kb.vmware.com/kb/1267" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1267']);">VMware KB 1267</a>. For each of the drivers the options are the following:

	  
	~ # vmkload_mod -s lpfc820 | grep lpfc_lun_queue_depth -A 1  
	lpfc_lun_queue_depth: int  
	Max number of FCP commands we can queue to a specific LUN
	
	~ # vmkload_mod -s iscsi_vmk | grep iscsivmk_LunQDepth -A 1  
	iscsivmk_LunQDepth: int  
	Maximum Outstanding Commands Per LUN
	
	~ # vmkload_mod -s qla2xxx | grep ql2xmaxqdepth -A 1  
	ql2xmaxqdepth: int  
	Maximum queue depth to report for target devices.  
	

The Cisco VIC sets the DQLEN value to be 32. From the Cisco article "<a href="http://www.cisco.com/en/US/prod/collateral/ps10265/ps10276/whitepaper_c11-702584.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cisco.com/en/US/prod/collateral/ps10265/ps10276/whitepaper_c11-702584.html']);">Cisco Unified Computing System (UCS) Storage Connectivity Options and Best Practices with NetApp Storage</a>".

> Hardcoded Parameters
> 
> LUN Queue Depth  
> This value affects performance in a FC environment when the host throughput is limited by the various queues that exist in the FC driver and SCSI layer of the operating system
> 
> This Cisco VIC adapter sets this value to 32 per LUN on ESX and Linux and 255 on Windows and does not expose this parameter in the FC adapter policy. Emulex and Qlogic expose this setting using their host based utilities. Many customers have asked about how to change this value using the Cisco VIC adapter. Cisco is considering this request as an enhancement for a future release. However FC performance with the VIC adapter has been excellent and there no cases in evidence (that the author is aware of) indicating that this setting is not optimal at its current value. It should be noted that this is the default value recommended by VMware for ESX and other operating systems vendors.

The VMware white paper "<a href="http://www.vmware.com/files/pdf/scalable_storage_performance.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/scalable_storage_performance.pdf']);">Scalable Storage Performance</a>" describes what DQLEN is:

> The SCSI protocol allows multiple commands to be active on a LUN at the same time. SCSI device drivers have a configurable parameter called the LUN queue depth that determines how many commands can be active at one time to a given LUN. QLogic Fibre Channel HBAs support up to 255 outstanding commands per LUN,and Emulex HBAs support up to 128. However, the default value for both drivers is set to 32. If an ESX host generates more commands to a LUN than the LUN queue depth, the excess commands are queued in the ESX kernel, and this increases the latency.
> 
> SCSI device drivers have a configurable parameter called the LUN queue depth that determines how many commands to a given LUN can be active at one time. The default in ESX is 32. If an ESX host generates more commands to a LUN than the LUN queue depth, the excess commands are queued in the ESX kernel, and this increases the latency. The queue depth is per‐LUN, and not per‐initiator. The initiator (or the host bus adapter) supports many more commands (typically 2,000 to 4,000 commands per port).

There is also another way of tweaking this value and that is with Disk.SchedNumReqOutstanding (DSNRO). This actually comes before the LUN Queues. There is a very good step by step diagram of the queues at the Virtual Geek blog "<a href="http://virtualgeek.typepad.com/virtual_geek/2009/06/vmware-io-queues-micro-bursting-and-multipathing.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtualgeek.typepad.com/virtual_geek/2009/06/vmware-io-queues-micro-bursting-and-multipathing.html']);">VMware I/O queues, “micro-bursting”, and multipathing</a>". Here is the picture from that blog:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/07/all_storage_queues.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/07/all_storage_queues.png']);"><img class="alignnone size-full wp-image-1784" title="all_storage_queues" src="http://virtuallyhyper.com/wp-content/uploads/2012/07/all_storage_queues.png" alt="all storage queues Seeing LUN Queue Depth Filling up with UCS B230/B200 using Cisco VICs and EMC VMAX" width="630" height="465" /></a>

To edit this option you can follow instructions from <a href="http://kb.vmware.com/kb/1268" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1268']);">VMware KB 1268</a>. There is a caveat with this option. From the above KB:

> **Note:** This limit does not apply when only one virtual machine is active on a Datastore/LUN. In that case, the bandwidth is limited by the queue depth of the storage adapter.

So this option works only with multiple VMs on the same datastore. Here is more information from the above VMware white paper:

> This means that if two virtual machines have their virtual disks on two different LUNs, each virtual machine can generate as many active commands as the LUN queue depth. But if the two virtual machines have their virtual disks on the same LUN (VMFS volume), the total number of active commands that the two virtual machines combined can generate without incurring queuing delays is equal to the LUN queue depth. More specifically, when virtual machines share a LUN, the total number of outstanding commands permitted from all virtual machines to that LUN is governed by the Disk.SchedNumReqOutstanding configuration parameter that can be set using VirtualCenter. If the total number of outstanding commands from all virtual machines exceeds this parameter, the excess commands are queued in the ESX kernel.

And one more note regarding DSNRO, from the same PDF:

> Also make sure to set the Disk.SchedNumReqOutstanding parameter to the same value as the queue depth. If this parameter is given a higher value than the queue depth, it is still capped at the queue depth. However, if this parameter is given a lower value than the queue depth, only that many outstanding commands are issued from the ESX kernel to the LUN from all virtual machines. The Disk.SchedNumReqOutstanding setting has no effect when there is only one virtual machine issuing I/O to the LUN.

So when modifying the LUN Queue Length on the HBA drivers also modify the DSNRO accordingly. Because DQLEN will be set to the minimum of the two. If you want to read more on how DSNRO works, I suggest reading this yellow brick blog "<a href="http://www.yellow-bricks.com/2011/06/23/disk-schednumreqoutstanding-the-story/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2011/06/23/disk-schednumreqoutstanding-the-story/']);">Disk.SchedNumReqOutstanding the story</a>".

There are two other things that can affect the DQLEN value. The first one is the adaptive queue depth algorithm. More information can be found in the <a href="http://kb.vmware.com/kb/1008113" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1008113']);">VMware KB 1008113</a>. From that KB:

> VMware ESX 3.5 Update 4 and ESX 4.0 introduces an adaptive queue depth algorithm that adjusts the LUN queue depth in the VMkernel I/O stack. This algorithm is activated when the storage array indicates I/O congestion by returning a BUSY or QUEUE FULL status. These status codes may indicate congestion at the LUN level or at the port (or ports) on the array. When congestion is detected, VMkernel throttles the LUN queue depth. The VMkernel attempts to gradually restore the queue depth when congestion conditions subside.
> 
> This algorithm can be activated by changing the values of the QFullSampleSize and QFullThreshold parameters. When the number of QUEUE FULL or BUSY conditions reaches the QFullSampleSize value, the LUN queue depth reduces to half of the original value. When the number of good status conditions received reaches the QFullThreshold value, the LUN queue depth increases one at a time.

If you see the SCSI Sense Codes mentioned in the above KB then you know your DQLEN value is impacted.

The second way the DQLEN can be impacted is by enabling SIOC on the Datastore. From the initial VMware blog:

> Today using features like Storage I/O Control (SIOC), vSphere can mitigate that virtual machine and vSphere host noisy neighbor risk through a more elegant and fair mechanism. Therefore, today if you are noticing that your device queues are constantly bumping up to their maximum limits, it would be recommended to increase the Device/LUN depth and use SIOC to help mitigate any potential noisy neighbor problem. A quick little note, SIOC controls storage workloads by modify the Device/LUN queue depth, but SIOC cannot increase the device queue depth beyond the configured maximum. So you have to bump up the maximum yourself if your workloads need larger queues, and then let SIOC reduce it when needed.

One note about SIOC is, if enabled it will ignore the DSNRO variable and adjusts the DQLEN to match the performance of the LUN.

