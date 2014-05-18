---
title: Seeing SCSI Command Aborts on an ESX 3.5 Host
author: Karim Elatov
layout: post
permalink: /2012/05/seeing-scsi-command-aborts-esx-3-5-host/
dsq_thread_id:
  - 1409590662
categories:
  - Storage
  - VMware
tags:
  - HBA Firmware
  - lpfc
  - SCSI Aborts
  - SCSI Reservation Conflicts
  - SCSI Reservations
---
I recently ran into an interesting issue with an ESX 3.5 host. We were seeing SCSI aborts on multiple hosts. Looking at the logs of one of the hosts we saw the following:


	Apr 26 20:29:30 esx_host1 vmkernel: 84:04:56:07.658 cpu3:1037)FS3: 1974: Checking if lock holders are live for lock [type 10c00001 offset 67555328 v 34, hb offset 3526656
	Apr 26 20:29:30 esx_host1 vmkernel: gen 7154, mode 1, owner 4f096eb7-8e0556eb-f0fe-002264fb5e26 mtime 4089393]
	Apr 27 10:14:42 esx_host1 vmkernel: 84:18:41:17.645 cpu3:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x83
	Apr 27 10:14:43 esx_host1 vmkernel: 84:18:41:18.916 cpu3:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x83 x128
	Apr 27 10:14:43 esx_host1 vmkernel: 84:18:41:18.916 cpu3:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x88
	Apr 27 10:14:44 esx_host1 vmkernel: 84:18:41:20.188 cpu3:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x88 x128
	Apr 27 10:14:48 esx_host1 vmkernel: 84:18:41:23.990 cpu3:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x83
	Apr 27 10:14:49 esx_host1 vmkernel: 84:18:41:25.262 cpu3:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x83 x128
	Apr 27 10:14:49 esx_host1 vmkernel: 84:18:41:25.262 cpu3:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x88
	Apr 27 10:14:50 esx_host1 vmkernel: 84:18:41:26.487 cpu2:1094)VSCSIFs: 439: fd 4113 status Busy
	Apr 27 10:14:50 esx_host1 vmkernel: 84:18:41:26.487 cpu2:1094)VSCSIFs: 439: fd 4114 status Busy
	Apr 27 10:14:51 esx_host1 vmkernel: 84:18:41:26.534 cpu3:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x88 x128
	Apr 27 10:14:51 esx_host1 vmkernel: 84:18:41:26.534 cpu3:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x8e
	Apr 27 10:14:52 esx_host1 vmkernel: 84:18:41:27.806 cpu3:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x8e x128
	Apr 27 10:14:52 esx_host1 vmkernel: 84:18:41:27.856 cpu1:1114)Fil3: 4940: READ error 0xbad00e5
	...
	...
	...
	Apr 27 10:19:31 esx_host1 vmkernel: 84:18:46:06.993 cpu2:1043)WARNING: SCSI: 2909: CheckUnitReady on vmhba1:0:132 returned Storage initiator error 0x7/0x0 sk 0x0 asc 0x0 ascq 0x0
	Apr 27 10:19:37 esx_host1 vmkernel: 84:18:46:13.230 cpu3:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x83
	Apr 27 10:19:39 esx_host1 vmkernel: 84:18:46:14.495 cpu3:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x83 x128
	Apr 27 10:19:39 esx_host1 vmkernel: 84:18:46:14.545 cpu1:1039)WARNING: FS3: 4784: Reservation error: Timeout


It looks like all of a sudden at Apr 27th at 10:14 AM the lpfc (emulex) driver started aborting SCSI
commands. I found VMware KB [1004157](http://kb.vmware.com/kb/1004157) that matched the above messages.

The KB talks about some possibilities as to why this could happen and some possible fixes as well:

> 1.  <span style="line-height: 22px;">Exceeding ESX LUN and/or Path Maximum Limits.<br /> </span>
> 2.  <span style="line-height: 22px;">Update the HBA Emulex HBA firmware.</span>
> 3.  <span style="line-height: 22px;">Consider reseating the HBAs on the server and trying different PCI slots. Some PCI-X slots operate at different bus speeds (for example, 100Mhz vs. 133MHz). It is possible that the HBA is not able to issue commands through the PCI bridge to the device. As a result, I/O commands are aborted then retried.</span>
> 4.  <span style="line-height: 22px;">On SUN's X4200 servers that use re-branded Emulex HBAs and running ESX server 3.01/3.02, install patches ESX-1003355 (ESX 3.01) and patch ESX-1003177 (ESX 3.02).  </span>
> 5.  <span style="line-height: 22px;">If this is seen on multiple ESX servers, it is likely that there is a problem at the FC fabric level or at the storage array level. Looking at the switch logs and/or the array logs, you may find some additional clues. </span>

On another host, I saw the following:


	Apr 27 10:15:02 esx_host2 vmkernel: 110:04:47:54.368 cpu0:1039)FS3: 4828: Reclaimed timed out heartbeat [HB state abcdef02 offs
	et 3526656 gen 50 stamp 9521259362672 uuid 4f096eb7-8e0556eb-f0fe-002264fb5e26 jrnl drv 4.31]
	Apr 27 10:16:27 esx_host2 vmkernel: 110:04:49:19.318 cpu0:1039)SCSI: vm 1039: 109: Sync CR at 64
	Apr 27 10:16:28 esx_host2 vmkernel: 110:04:49:20.266 cpu0:1039)SCSI: vm 1039: 109: Sync CR at 48
	Apr 27 10:16:29 esx_host2 vmkernel: 110:04:49:21.227 cpu0:1039)SCSI: vm 1039: 109: Sync CR at 32
	Apr 27 10:16:30 esx_host2 vmkernel: 110:04:49:22.213 cpu0:1039)SCSI: vm 1039: 109: Sync CR at 16
	Apr 27 10:16:31 esx_host2 vmkernel: 110:04:49:23.213 cpu2:1039)SCSI: vm 1039: 109: Sync CR at 0
	Apr 27 10:16:31 esx_host2 vmkernel: 110:04:49:23.213 cpu2:1039)WARNING: SCSI: 119: Failing I/O due to too many reservation conflicts


It looks like the other host was having SCSI reservation issues. I found another VMware KB [1021187](http://kb.vmware.com/kb/1021187) that matched the symptoms of both hosts. From the second KB article here is scenario that could cause the above symptoms:

> 1.  ESX host X's HBA sends a SCSI reserve command to the array to reserve LUN Y.
> 2.  Array places reservation on LUN Y for the initiator.
> 3.  ESX host X's HBA goes into internal fatal error state and no longer responds to/issue commands, particularly a SCSI release.
> 4.  Driver starts to abort commands in flight since they did not complete before the timeout period.
> 5.  ESX SCSI mid layer reports a Storage Initiator Error when trying to communicate with the HBA.
> 6.  No hosts can complete I/O requests to LUN Y since it has a reservation on it for the initiator in ESX host X.
> 7.  All hosts return a SCSI Reservation Conflict status from the array when attempting to issue I/O to LUN Y.
> 8.  ESX host X is shutdown/rebooted.
> 9.  The reboot causes the HBAs in that host to drop from the fabric.
> 10. The array sees the HBAs drop off the fabric and proceeds to clear any pending reservations from those initiators.
> 11. The other ESX hosts are now able to do I/O to LUN Y and are no longer getting SCSI Reservation Conflict statuses

The above article mentions that we could do a LUN reset but from the logs, both of the hosts stop having issues on Apr 27th at 10:26 AM:


	Apr 27 10:26:17 esx_host1 vmkernel: 84:18:52:53.181 cpu1:1062)lpfc0:0712:FPe:SCSI layer issued abort device Data: x0 x83
	Apr 27 10:26:18 esx_host1 vmkernel: 84:18:52:54.442 cpu1:1062)lpfc0:0749:FPe:Completed Abort Task Set Data: x0 x83 x128
	Apr 27 10:26:19 esx_host1 vmkernel: 84:18:52:54.493 cpu2:1036)FSS: 390: Failed with status Timeout (ok to retry) for f530 28 2 49e64214 77691c3 230046ec 62f5247d 4 1 0 0 0 0 0
	Apr 27 16:44:59 esx_host1 vmkernel: 85:01:11:34.664 cpu1:1112)DevFS: 2221: Unable to find device: 1d3b014-New Virtual Machine_2-000001-delta.vmdk
	Apr 27 16:44:59 esx_host1 vmkernel: 85:01:11:34.678 cpu1:1112)DevFS: 2221: Unable to find device: 200d-New Virtual Machine_1-000001-delta.vmdk


We see a gap in the above logs, and from the other host, we saw a similar gap in the logs:


	Apr 27 10:25:49 esx_host2 vmkernel: 110:04:58:40.966 cpu0:1039)SCSI: vm 1039: 109: Sync CR at 64
	Apr 27 10:25:49 esx_host2 vmkernel: 110:04:58:41.276 cpu2:1037)SCSI: vm 1037: 109: Sync CR at 64
	Apr 27 10:25:50 esx_host2 vmkernel: 110:04:58:41.990 cpu0:1039)SCSI: vm 1039: 109: Sync CR at 48
	Apr 27 10:25:50 esx_host2 vmkernel: 110:04:58:42.252 cpu2:1037)SCSI: vm 1037: 109: Sync CR at 48
	Apr 27 10:25:51 esx_host2 vmkernel: 110:04:58:43.161 cpu0:1039)FS3: 4828: Reclaimed timed out heartbeat [HB state abcdef02 offset 3526656 gen 50 stamp 9521343377967 uuid 4f096eb7-8e0556eb-f0fe-002264fb5e26 jrnl drv 4.31]
	Apr 27 16:59:58 esx_host2 vmkernel: 110:11:32:49.390 cpu0:1035)World: vm 1150: 895: Starting world vmware-vmx with flags 4


It sounded like esx_host1 had an issue talking to the array (possible causes in KB [1004157](http://kb.vmware.com/kb/1004157)) from
10:14 to 10:26 and that caused the other host esx_host2 to have SCSI Reservation issues (scenario
described in KB [1021187](http://kb.vmware.com/kb/1021187)). After some time, esx_host1 was finally able to connect to the array and release the stuck SCSI reservation.

Looking over esx_host1 I  also saw a lot of these messages during the time issue:


	Apr 27 10:25:33 esx_host1 vmkernel: 84:18:52:08.503 cpu0:1043)WARNING: SCSI: 2909: CheckUnitReady on vmhba1:0:149 returned Storage initiator error 0x7/0x0 sk 0x0 asc 0x0 ascq 0x0
	Apr 27 10:25:54 esx_host1 vmkernel: 84:18:52:29.768 cpu0:1043)WARNING: SCSI: 2909: CheckUnitReady on vmhba1:0:150 returned Storage initiator error 0x7/0x0 sk 0x0 asc 0x0 ascq 0x0


Now checking for that message and looking at which LUNs exhibited the issue, I saw the following:


	kelatov@machine:log$ grep CheckUnitReady vmkernel.1 | awk '{print $12}' | sort | uniq -c
	1 vmhba1:0:129
	1 vmhba1:0:130
	1 vmhba1:0:132
	1 vmhba1:0:133
	1 vmhba1:0:134
	1 vmhba1:0:135
	1 vmhba1:0:136
	1 vmhba1:0:137
	1 vmhba1:0:138
	1 vmhba1:0:139
	1 vmhba1:0:140
	1 vmhba1:0:141
	1 vmhba1:0:142
	1 vmhba1:0:143
	1 vmhba1:0:144
	1 vmhba1:0:145
	1 vmhba1:0:146
	1 vmhba1:0:147
	1 vmhba1:0:148
	1 vmhba1:0:149
	1 vmhba1:0:150


That is a lot of LUNS from the same HBA. Those messages are described in VMware KB [1029456](http://kb.vmware.com/kb/1029456), and the suggestion is to update the firmware:

> <div>
>   There is no Sense Key or Addition Sense Code/ASC Qualifier information for this status as this is a host side condition.
> </div>
>
> <div>
>
> </div>
>
> <div>
>   This issue can occur if the affected hosts are using Emulex 2Gb, 4Gb and 8Gb HBA's with old or outdated firmware. For example, 4GB HBA Firmware Versions 2.10*, 2.5*, 2.7*, and 2.80* and 2GB HBA Firmware Versions: 1.8*, 1.90*, and 1.91* are outdated.
> </div>

We updated the firmware on the HBAs and the issues stopped.

