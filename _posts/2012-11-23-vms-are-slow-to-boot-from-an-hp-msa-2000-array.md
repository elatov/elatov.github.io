---
title: VMs are Slow to Boot from an HP MSA 2000 Array
author: Karim Elatov
layout: post
permalink: /2012/11/vms-are-slow-to-boot-from-an-hp-msa-2000-array/
dsq_thread_id:
  - 1404673734
categories:
  - Storage
  - VMware
tags:
  - davg
  - Drive Channel 0 link degraded
  - esxtop
  - HP MSA 2000
  - qla24xx_abort_command
---
We were trying to power on a couple of VMs on an ESX 3.5 host and they would take forever to boot. Opening esxtop and checking the latency to the array we saw the following:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/esxtop_latency_msa_2000.png" alt="esxtop latency msa 2000 VMs are Slow to Boot from an HP MSA 2000 Array" title="esxtop_latency_msa_2000" width="1141" height="207" class="alignnone size-full wp-image-4786" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/esxtop_latency_msa_2000.png)

At the same time we saw a lot of aborts to the array:


	Nov 14 01:15:37 esx vmkernel: 0:02:09:02.494 cpu3:1043)FS3: 4831: Reclaimed timed out heartbeat [HB state abcdef02 offset 3159552 gen 174 stamp 7738206575 uuid 50a2d28e-497dcab4-7e86-001b78bbdd58 jrnl <FB 121075> drv 4.31]
	Nov 14 01:15:46 esx vmkernel: 0:02:09:11.075 cpu0:1066)<6>qla24xx_abort_command(0): handle to abort=122
	Nov 14 01:15:46 esx vmkernel: 0:02:09:11.075 cpu0:1035)StorageMonitor: 196: vmhba1:0:1:0 status = 0/2 0x0 0x0 0x0
	Nov 14 01:15:50 esx vmkernel: 0:02:09:14.987 cpu0:1024)StorageMonitor: 196: vmhba1:0:1:0 status = 0/2 0x0 0x0 0x0
	Nov 14 01:15:51 esx vmkernel: 0:02:09:16.149 cpu0:1066)<6>qla24xx_abort_command(0): handle to abort=132


The IO was aborting cause the latency was so high, as we see from the esxtop output above, it's at 5000ms. While I was looking at esxtop I saw values up to 10000ms. We decided to check out the array manager. We logged into the MSA web based management and as soon as we logged in, we saw the following pop up:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/msa_degraded_message_c1.png" alt="msa degraded message c1 VMs are Slow to Boot from an HP MSA 2000 Array" title="msa_degraded_message_c1" width="692" height="468" class="alignnone size-full wp-image-4787" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/msa_degraded_message_c1.png)

Here are the messages:

> Drive Channel 0 link degraded (Excessive LIPs)

As soon as we saw that message, the customer mentioned that they had a failed hard drive but they have since 'offlined' the drive and the spare took over. We checked out the event view, and we saw the following:

[<img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/errors_in_event_on_msa_c.png" alt="errors in event on msa c VMs are Slow to Boot from an HP MSA 2000 Array" title="errors_in_event_on_msa_c" width="783" height="652" class="alignnone size-full wp-image-4788" />](http://virtuallyhyper.com/wp-content/uploads/2012/11/errors_in_event_on_msa_c.png)

Here are the messages that stood out were:

> Disk channel error (Channel:0 Id 16: SN 9QK0R36 Encl:1 Slot:0) I/O Timeout
> Disk detected error (Channel:0 Id 138: SN 9QK0R36 Encl:1 Slot:0) Key,Code,Qual=(02h,04h,00h) cdb:0000000000 CmdSpc:0h FRU:0h SnsKeySpc:0h Not Ready LUN not ready

We contacted HP and they mentioned that even though the disk is offline/disabled, it could still be causing an issue. We tried to get a log bundle from the web management interface but it never completed since the array was so slow. HP then suggested to completely remove the disk. After we removed the bad hard driver, the latency subsided and we were able to power on VMs without issues.

