---
title: ESX Host Experiencing High Latency to a Hitachi HDS Array
author: Karim Elatov
layout: post
permalink: /2012/04/esx-host-experiencing-high-latency-to-a-hitachi-array/
dsq_thread_id:
  - 1404673207
categories:
  - Storage
  - VMware
tags:
  - davg
  - ESX
  - Hitachi HDS
---
Recently I received a call from a European customer saying that they were having performance issues with their VMs. Whenever I hear performance issues, I automatically think esxtop. To check out some good articles regarding esxtop and troubleshooting performance issues, check out my previous post (<a href="http://virtuallyhyper.com/2012/04/ubuntu-11-10-vms-experience-high-storage-latency-on-esxi-5-0/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/ubuntu-11-10-vms-experience-high-storage-latency-on-esxi-5-0/']);">Ubuntu 11.10 VMs Experience High Storage Latency on ESXi 5.0</a>). Also, to check out the threshold values for some of the esxtop metrics, I would suggest looking at this <a href="http://www.vreference.com/public/vReference-esxtop1.2.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vreference.com/public/vReference-esxtop1.2.pdf']);">vReference pdf</a>. Here are a couple of pictures from that pdf:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/04/esxtop_threshold_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/04/esxtop_threshold_1.png']);"><img class="alignnone size-full wp-image-1264" title="esxtop_threshold_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/04/esxtop_threshold_1.png" alt="esxtop threshold 1 ESX Host Experiencing High Latency to a Hitachi HDS Array" width="642" height="295" /></a>

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/04/esxtop_threshold_2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/04/esxtop_threshold_2.png']);"><img class="alignnone size-full wp-image-1265" title="esxtop_threshold_2" src="http://virtuallyhyper.com/wp-content/uploads/2012/04/esxtop_threshold_2.png" alt="esxtop threshold 2 ESX Host Experiencing High Latency to a Hitachi HDS Array" width="636" height="82" /></a>

**Note:** Some good ones to note are DAVG (25ms) and KAVG (2ms)

I asked the customer if they had made any recent changes to the environment. They mentioned that two days ago they had found a bad <a href="http://en.wikipedia.org/wiki/Gigabit_interface_converter" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://en.wikipedia.org/wiki/Gigabit_interface_converter']);">GBIC</a> on one of the SAN switches that was part of an ISL Trunk between their SAN Switches. An ISL Trunk is described in this great IBM article (<a href="http://www.redbooks.ibm.com/abstracts/tips0043.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.redbooks.ibm.com/abstracts/tips0043.html']);">SAN &#8211; IBM TotalStorage Switch ISL Trunking</a>), directly from the article:

> The ISL Trunking feature allows up to four Interswitch Links (ISLs) to merge logically into a single link. An ISL is a connection between two switches through an Expansion Port (E_Port). When using ISL Trunking to aggregate bandwidth of up to four ports, the speed of the ISLs between switches in a fabric is quadrupled. For example, at 2 Gb/s speeds, trunking delivers ISL throughput of up to 8 Gb per second. ISL Trunking supports high-bandwidth, large-scale SANs which include core switches. The primary task of ISL Trunking is to route data and edge switches that aggregate connections to servers and storage. ISL Trunking simplifies network design and reduces the cost of storage management by optimizing bandwidth utilization and enabling load balancing of traffic at the frame-level. The ISL Trunking feature has many advantages, for example, it ensures optimal ISL bandwidth use across trunked links, while preserving in-order delivery. ISL Trunking uses frame-level load balancing, as opposed to Fibre Channel Shortest Path First (FSPF), to achieve faster fabric convergence, as well as higher availability in the fabric.

Having heard that something with the SAN environment had changed, I fired up **esxtop** and went to the disk device view (by typing &#8216;u&#8217;). Here is what I saw:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/04/high_davg_to_hitachi_array_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/04/high_davg_to_hitachi_array_1.png']);"><img class="alignnone size-full wp-image-1269" title="high_davg_to_hitachi_array_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/04/high_davg_to_hitachi_array_1.png" alt="high davg to hitachi array 1 ESX Host Experiencing High Latency to a Hitachi HDS Array" width="1148" height="600" /></a>

Multiple LUNs are seeing a value above 1000ms for the DAVG/cmd value. The DAVG values stayed that way the whole time (these weren&#8217;t just spikes) and it was the same thing across multiple hosts. So we are definitely above the recommended threshold value for DAVG of 25ms. I asked them what was the model of the array that they were utilizing and they told me it was the HDS (Hitachi Data Systems) USP 1100. The first thing I checked out was, if it was on the HCL and it was (<a href="http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=1445&deviceCategory=san&partner=39&keyword=USP%201100&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=1445&deviceCategory=san&partner=39&keyword=USP%201100&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc']);">HDS USP 1100</a>). The next thing to check is to make sure that the PSP (Pathing Selection Policy) was set correctly. I checked the setting and all the hosts was using a FIXED pathing policy. I also checked out the logs under **/var/log/vmkernel** and I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/04/sync_CR_messages_to_hitachi_array_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/04/sync_CR_messages_to_hitachi_array_1.png']);"><img class="alignnone size-full wp-image-1272" title="sync_CR_messages_to_hitachi_array_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/04/sync_CR_messages_to_hitachi_array_1.png" alt="sync CR messages to hitachi array 1 ESX Host Experiencing High Latency to a Hitachi HDS Array" width="1010" height="504" /></a>

So we were seeing SCSI Reservation Conflict Messages. There is a great KB on Analyzing the &#8216;Sync CR&#8217; messages, VMware KB <a href="http://kb.vmware.com/kb/1005009" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005009']);">1005009</a>. Also from KB <a href="http://kb.vmware.com/kb/1030381" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1030381']);">1030381</a> this is what SYNC CR messages mean:

> **VMK&#95;SCSI&#95;DEVICE&#95;RESERVATION&#95;CONFLICT = 0&#215;18**  
> vmkernel: 1:08:40:03.933 cpu5:4736)ScsiDeviceToken: 115: Completed IO with status H:0&#215;0 D:0&#215;18 P:0&#215;0 after losingreservation on device naa.6006016026601d007c174a7aa292df11
> 
> This status is returned when a LUN is in a Reserved status and commands from initiators that did not place that SCSI reservation attempt to issue commands to it. Rarely will you ever see a device status of 0&#215;18 in the format shown above. The most common form of a RESERVATION CONFLICT status message is seen as follows:
> 
> vmkernel: 12:17:46:05.000 cpu12:4108)ScsiCore: 1181: Sync CR (opcode 28) at 992 (wid 4121)
> 
> The opcode or SCSI Command Operation Code referenced in this message is 28 or 0&#215;28. This is a READ(10) command or a 10 byte READ, which is a command to be issued by a VM.

That is exactly what we were seeing (a READ command failing due to a SCSI reservation conflict). The above messages are basically a retry count down (a SCSI command has failed and it is retrying that command, after a certain amount of retries it fails), and eventually show you the LUN that has the stuck reservation, like this (from KB <a href="http://kb.vmware.com/kb/1005009" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005009']);">1005009</a>):

> SCSI: vm 1043: 5522: Sync CR at 64  
> SCSI: vm 1043: 5522: Sync CR at 48  
> SCSI: vm 1043: 5522: Sync CR at 32  
> SCSI: vm 1043: 5522: Sync CR at 16  
> SCSI: vm 1043: 5522: Sync CR at 0  
> WARNING: SCSI: 5532: Failing I/O due to too many reservation conflicts  
> WARNING: SCSI: 5628: status SCSI reservation conflict, rstatus 0xc0de01 for vmhba1:0:7. residual R 919, CR 0, ER 3  
> WARNING: J3: 1970: Error committing txn to slot 0: SCSI reservation conflict

In my case the run-time path (vmhba1:0:7) message never showed up, which means that the SCSI command actually gets through (eventually) and it was just taking a while. Given the latency that we saw from above, this isn&#8217;t unexpected. If the run-time path messages eventually showed then you can use the instructions laid out in VMware KB <a href="http://kb.vmware.com/kb/1021187" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1021187']);">1021187</a> to send a **LUN RESET** to clear any stuck SCSI Reservations.

There is also a VMware KB specifically for Hitachi Arrays regarding SCSI Reservations conflicts (<a href="http://kb.vmware.com/kb/1005010" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005010']);">1005010</a>). From that article there are some good things to check on the array side to prevent SCSI Reservations Conflicts, here is a list:

> *   VMware recommends using non-LUSE based LUNs for VMFS volumes
> *   If you are using LUSE based LUNs, make sure that the Microcode version on the array is at least 50-07-66-00/00 then enable Host Mode Option 19
> *   On USP V and USP virtual machines, set the Host Mode to “VMware” 

There is also another VMware KB (<a href="http://kb.vmware.com/kb/3408142" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/3408142']);">3408142</a>) regarding SCSI Reservations issue on HDS arrays, which makes the same recommendations and also mentions that some **SYNC CRs** are okay:

> This issue is typically usually caused by SCSI reservation failure.
> 
> To resolve this issue:  
> Ensure that you are using the minimum version of firmware code (50-07-66-00/00)  
> Set Host Mode Option = 19 to ON (This is Host Group setting)  
> Host Mode = 0A (Netware) must be used for all VMware Host Groups
> 
> These options are not accessible by customers. For further assistance, contact HDS. HDS has issued alert USP_051448 for this problem.
> 
> **Note:** SCSI reservation conflict warnings may still be present. This is normal and expected because LUNs continue to be shared in a multi-initiator environment. Host Mode Option 19 I/O improvement enables the host to retry commands with a greater probability of success.

We went on the array confirmed the following:

1.  Host Mode set 19 for the Host Group (it was)
2.  Host Mode set to 0A for the VMware Host Groups (it was)
3.  Microcode was above 50-07-66-00/00 ( we had Microcode 50-09-83/00)

I asked the SAN admin to take a look at the performance and we noticed that all the traffic was going through just one Storage Processor while the other one was not utilized at all. I then looked over the Hitachi document <a href="http://www.hds.com/assets/pdf/optimizing-the-hitachi-virtual-storage-platform-best-practices-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.hds.com/assets/pdf/optimizing-the-hitachi-virtual-storage-platform-best-practices-guide.pdf']);">Optimizing the Hitachi Universal Storage Platform Family in VMware Environments</a> and I saw the following:

> For ESX 3.5 and earlier, Hitachi recommends using a fixed path policy for all of its storage systems. For ESX 4 and higher, Hitachi recommends using VMware’s round robin multipathing policy.

And from the <a href="http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=1445&deviceCategory=san&partner=39&keyword=USP%201100&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=1445&deviceCategory=san&partner=39&keyword=USP%201100&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc']);">HCL</a> page of the array, I saw the following:

> **Attention:** Storage partners using ESX 4.0 or later may recommend VMW&#95;PSP&#95;RR for path failover policy for certain storage array models. If desired, contact the storage array manufacturer for recommendation and instruction to set VMW&#95;PSP&#95;RR appropriately.

We were actually using ESX 4.0, so I decided to change the pathing policy from FIXED to Round Robin. I followed the instructions from Jarret&#8217;s post <a href="http://virtuallyhyper.com/2012/03/changing-the-path-selection-policy-to-round-robin/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/03/changing-the-path-selection-policy-to-round-robin/']);">Changing the Path Selection Policy to Round Robin</a>. The syntax of my command was a little different, since the customer was not running ESXi 5.0 but ESX 4.0. I ran the following:

    ~ # esxcfg-scsidevs -c | egrep -o "^naa.[0-9a-f]+" | grep naa.60060e800 | xargs -n 1 esxcli nmp device setpolicy --psp VWM_PSP_RR --device 
    

**Note:** More information regarding changing the PSP on devices and the command line difference between ESX versions, can be found at VMware KB <a href="http://kb.vmware.com/kb/1036189" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1036189']);">1036189</a>

I did that across all the hosts and then after 5-10 minutes the DAVG went down, the SYNC CR messages stopped, and the performance of the VMs returned to normal.

