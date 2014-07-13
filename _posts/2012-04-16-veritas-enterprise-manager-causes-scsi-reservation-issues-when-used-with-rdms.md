---
published: true
title: Veritas Enterprise Manager Causes SCSI Reservation issues when used with RDMs
author: Karim Elatov
layout: post
permalink: /2012/04/veritas-enterprise-manager-causes-scsi-reservation-issues-when-used-with-rdms/
categories: ['storage', 'vmware']
tags: ['fiber_channel', 'nmp', 'fdisk', 'rdm', 'scsi_reservations']
---

I recently ran into an issue where a customer was seeing "SCSI Reservation" messages on one of their hosts. I asked for a log bundle (KB [653](http://kb.vmware.com/kb/653)), and they had sent me one. I was looking over the vmkernel logs (/var/log/vmkernel) and I saw the following:


	vmkernel.9:Mar 10 01:00:45 esx_host vmkernel: 97:00:40:02.937 cpu15:14570)VMW_SATP_SVC: satp_svc_UpdatePath: Failed to update path "vmhba2:C0:T1:L80" state. Status=SCSI reservation conflict


Looking at the frequency of the message and what LUN kept having the issue, I saw the following:


	me@my_server:log$ grep 'reservation conflict' vmkernel* | awk '{print $13}' | sort | uniq -c
	5432 "vmhba1:C0:T0:L80"
	5432 "vmhba1:C0:T1:L80"
	5432 "vmhba1:C0:T2:L80"
	5432 "vmhba1:C0:T3:L80"
	5432 "vmhba2:C0:T1:L80"
	5432 "vmhba2:C0:T2:L80"
	5432 "vmhba2:C0:T3:L80"


It looks like it's only happening on Lun 80 and here is the info for that LUN:

First here is the 'esxcli nmp device' output for that lun:


	fc.20000000c9b96378:10000000c9b96378-fc.500507680100c7ad:500507680120c7ad-naa.600507680180863d6800000000000062
	Runtime Name: vmhba1:C0:T3:L80
	Device: naa.600507680180863d6800000000000062
	Device Display Name: IBM Fibre Channel Disk (naa.600507680180863d6800000000000062)
	Group State: active
	Array Priority: 0
	Storage Array Type Path Config: SATP VMW_SATP_SVC does not support path configuration.
	Path Selection Policy Path Config: {current: no; preferred: no}


Secondly, here is the esxcfg-scsidevs output for that LUN:


	naa.600507680180863d6800000000000062
	Device Type: Direct-Access
	Size: 30720 MB
	Display Name: IBM Fibre Channel Disk (naa.600507680180863d6800000000000062)
	Multipath Plugin: NMP
	Console Device: /dev/sdcs
	Devfs Path: /vmfs/devices/disks/naa.600507680180863d6800000000000062
	Vendor: IBM Model: 2145 Revis: 0000
	SCSI Level: 6 Is Pseudo: false Status: on
	Is RDM Capable: true Is Removable: false
	Is Local: false
	Other Names:
	vml.0200500000600507680180863d6800000000000062323134352020
	VAAI Status: unknown


Lastly, here is the fdisk output for that LUN:


	Disk /dev/sdcs: 32.2 GB, 32212254720 bytes
	256 heads, 63 sectors/track, 3900 cylinders, total 62914560 sectors Units = sectors of 1 * 512 = 512 bytes

	Device Boot Start End Blocks Id System
	/dev/sdcs1 1 4294967295 2147483647+ ee EFI GPT


From above, we could gather that it's a Fibre-Channel Lun of about 30GB, but the interesting thing came from the fdisk output. It had a GPT partition on that LUN, which usually means that this LUN is used as an RDM and is directly presented to the Guest OS.

I asked the customer what that RDM was used for, and to check if there is any special application within the Guest OS that would use SCSI Reservations. It turned out that it was a change within Veritas Enterprise Administrator, just had to click a button that said "Remove SCSI reservations". After that, the messages stopped showing up in the vmkernel.

### Related Posts

- [Seeing SCSI Command Aborts on an ESX 3.5 Host](/2012/05/seeing-scsi-command-aborts-esx-3-5-host/)

