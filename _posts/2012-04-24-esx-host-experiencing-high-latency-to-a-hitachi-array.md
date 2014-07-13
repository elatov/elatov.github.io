---
title: ESX Host Experiencing High Latency to a Hitachi HDS Array
author: Karim Elatov
layout: post
permalink: /2012/04/esx-host-experiencing-high-latency-to-a-hitachi-array/
categories: ['storage', 'vmware']
tags: ['performance', 'nmp','psp', 'davg', 'hitachi_hds', 'scsi_reservations']
---

Recently I received a call from a European customer saying that they were having performance issues with their VMs. Whenever I hear performance issues, I automatically think esxtop. To check out some good articles regarding esxtop and troubleshooting performance issues, check out my previous post ([vReference pdf](/2012/04/ubuntu-11-10-vms-experience-high-storage-latency-on-esxi-5-0/). Here are a couple of pictures from that pdf:

![esxtop_threshold_1](https://github.com/elatov/uploads/raw/master/2012/04/esxtop_threshold_1.png)

![esxtop_threshold_2](https://github.com/elatov/uploads/raw/master/2012/04/esxtop_threshold_2.png)

**Note:** Some good ones to note are DAVG (25ms) and KAVG (2ms)

I asked the customer if they had made any recent changes to the environment. They mentioned that two days ago they had found a bad [SAN - IBM TotalStorage Switch ISL Trunking](http://en.wikipedia.org/wiki/Gigabit_interface_converter)), directly from the article:

> The ISL Trunking feature allows up to four Interswitch Links (ISLs) to merge logically into a single link. An ISL is a connection between two switches through an Expansion Port (E_Port). When using ISL Trunking to aggregate bandwidth of up to four ports, the speed of the ISLs between switches in a fabric is quadrupled. For example, at 2 Gb/s speeds, trunking delivers ISL throughput of up to 8 Gb per second. ISL Trunking supports high-bandwidth, large-scale SANs which include core switches. The primary task of ISL Trunking is to route data and edge switches that aggregate connections to servers and storage. ISL Trunking simplifies network design and reduces the cost of storage management by optimizing bandwidth utilization and enabling load balancing of traffic at the frame-level. The ISL Trunking feature has many advantages, for example, it ensures optimal ISL bandwidth use across trunked links, while preserving in-order delivery. ISL Trunking uses frame-level load balancing, as opposed to Fibre Channel Shortest Path First (FSPF), to achieve faster fabric convergence, as well as higher availability in the fabric.

Having heard that something with the SAN environment had changed, I fired up **esxtop** and went to the disk device view (by typing 'u'). Here is what I saw:

![high_davg_to_hitachi_array_1](https://github.com/elatov/uploads/raw/master/2012/04/high_davg_to_hitachi_array_1.png)

Multiple LUNs are seeing a value above 1000ms for the DAVG/cmd value. The DAVG values stayed that way the whole time (these weren't just spikes) and it was the same thing across multiple hosts. So we are definitely above the recommended threshold value for DAVG of 25ms. I asked them what was the model of the array that they were utilizing and they told me it was the HDS (Hitachi Data Systems) USP 1100. The first thing I checked out was, if it was on the HCL and it was ([HDS USP 1100](http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=1445&deviceCategory=san&partner=39&keyword=USP%201100&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc)). The next thing to check is to make sure that the PSP (Pathing Selection Policy) was set correctly. I checked the setting and all the hosts was using a FIXED pathing policy. I also checked out the logs under **/var/log/vmkernel** and I saw the following:

![sync_CR_messages_to_hitachi_array_1](https://github.com/elatov/uploads/raw/master/2012/04/sync_CR_messages_to_hitachi_array_1.png)

So we were seeing SCSI Reservation Conflict Messages. There is a great KB on Analyzing the 'Sync CR' messages, VMware KB [1030381](http://kb.vmware.com/kb/1005009) this is what SYNC CR messages mean:

> **VMK_SCSI_DEVICE_RESERVATION_CONFLICT = 0x18**
> vmkernel: 1:08:40:03.933 cpu5:4736)ScsiDeviceToken: 115: Completed IO with status H:0x0 D:0x18 P:0x0 after losingreservation on device naa.6006016026601d007c174a7aa292df11
>
> This status is returned when a LUN is in a Reserved status and commands from initiators that did not place that SCSI reservation attempt to issue commands to it. Rarely will you ever see a device status of 0x18 in the format shown above. The most common form of a RESERVATION CONFLICT status message is seen as follows:
>
> vmkernel: 12:17:46:05.000 cpu12:4108)ScsiCore: 1181: Sync CR (opcode 28) at 992 (wid 4121)
>
> The opcode or SCSI Command Operation Code referenced in this message is 28 or 0x28. This is a READ(10) command or a 10 byte READ, which is a command to be issued by a VM.

That is exactly what we were seeing (a READ command failing due to a SCSI reservation conflict). The above messages are basically a retry count down (a SCSI command has failed and it is retrying that command, after a certain amount of retries it fails), and eventually show you the LUN that has the stuck reservation, like this (from KB [1005009](http://kb.vmware.com/kb/1005009)):

> SCSI: vm 1043: 5522: Sync CR at 64
> SCSI: vm 1043: 5522: Sync CR at 48
> SCSI: vm 1043: 5522: Sync CR at 32
> SCSI: vm 1043: 5522: Sync CR at 16
> SCSI: vm 1043: 5522: Sync CR at 0
> WARNING: SCSI: 5532: Failing I/O due to too many reservation conflicts
> WARNING: SCSI: 5628: status SCSI reservation conflict, rstatus 0xc0de01 for vmhba1:0:7. residual R 919, CR 0, ER 3
> WARNING: J3: 1970: Error committing txn to slot 0: SCSI reservation conflict

In my case the run-time path (vmhba1:0:7) message never showed up, which means that the SCSI command actually gets through (eventually) and it was just taking a while. Given the latency that we saw from above, this isn't unexpected. If the run-time path messages eventually showed then you can use the instructions laid out in VMware KB [1021187](http://kb.vmware.com/kb/1021187) to send a **LUN RESET** to clear any stuck SCSI Reservations.

There is also a VMware KB specifically for Hitachi Arrays regarding SCSI Reservations conflicts ([1005010](http://kb.vmware.com/kb/1005010)). From that article there are some good things to check on the array side to prevent SCSI Reservations Conflicts, here is a list:

> *   VMware recommends using non-LUSE based LUNs for VMFS volumes
> *   If you are using LUSE based LUNs, make sure that the Microcode version on the array is at least 50-07-66-00/00 then enable Host Mode Option 19
> *   On USP V and USP virtual machines, set the Host Mode to “VMware”

There is also another VMware KB ([3408142](http://kb.vmware.com/kb/3408142)) regarding SCSI Reservations issue on HDS arrays, which makes the same recommendations and also mentions that some **SYNC CRs** are okay:

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

I asked the SAN admin to take a look at the performance and we noticed that all the traffic was going through just one Storage Processor while the other one was not utilized at all. I then looked over the Hitachi document [Optimizing the Hitachi Universal Storage Platform Family in VMware Environments](http://www.hds.com/assets/pdf/optimizing-the-hitachi-virtual-storage-platform-best-practices-guide.pdf) and I saw the following:

> For ESX 3.5 and earlier, Hitachi recommends using a fixed path policy for all of its storage systems. For ESX 4 and higher, Hitachi recommends using VMware’s round robin multipathing policy.

And from the [HCL](http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=1445&deviceCategory=san&partner=39&keyword=USP%201100&isSVA=1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc) page of the array, I saw the following:

> **Attention:** Storage partners using ESX 4.0 or later may recommend VMW_PSP_RR for path failover policy for certain storage array models. If desired, contact the storage array manufacturer for recommendation and instruction to set VMW_PSP_RR appropriately.

We were actually using ESX 4.0, so I decided to change the pathing policy from FIXED to Round Robin. I followed the instructions from Jarret's post [Changing the Path Selection Policy to Round Robin](http://virtuallyhyper.com/2012/03/changing-the-path-selection-policy-to-round-robin/). The syntax of my command was a little different, since the customer was not running ESXi 5.0 but ESX 4.0. I ran the following:


    ~ # esxcfg-scsidevs -c | egrep -o "^naa.[0-9a-f]+" | grep naa.60060e800 | xargs -n 1 esxcli nmp device setpolicy --psp VWM_PSP_RR --device


**Note:** More information regarding changing the PSP on devices and the command line difference between ESX versions, can be found at VMware KB [1036189](http://kb.vmware.com/kb/1036189)

I did that across all the hosts and then after 5-10 minutes the DAVG went down, the SYNC CR messages stopped, and the performance of the VMs returned to normal.

