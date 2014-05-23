---
title: 'Seeing High KAVG with Microsoft Cluster Services  (MSCS) RDMs'
author: Karim Elatov
layout: post
permalink: /2012/08/seeing-high-kavg-with-microsoft-cluster-services-mscs-rdms/
dsq_thread_id:
  - 1404673480
categories:
  - Storage
  - VMware
tags:
  - CONS/S Field
  - esxtop
  - MSCS
  - Perennially Reserved
  - RDM
  - SCSI Reservation Conflicts
  - Scsi.CRTimeoutDuringBoot
---
I came across an interesting issue the other day. I would randomly see high KAVG and QAVG on my ESX hosts. It would look something like this:

![high-kavg-1](https://github.com/elatov/uploads/raw/master/2012/08/high-kavg-1.png)

We can see that there actually isn't that much IO going to that LUN. As the issue was happening, I would see the following in the logs:


	Aug 16 20:09:17 vmkernel: 3:12:40:56.871 cpu16:4112)ScsiDeviceIO: 1688: Command 0x1a to device "naa.60060xxxx" failed H:0x5 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	Aug 16 20:09:57 vmkernel: 3:12:41:36.916 cpu5:4101)ScsiDeviceIO: 1688: Command 0x28 to device "naa.60060xxxx" failed H:0x5 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	Aug 16 20:10:37 vmkernel: 3:12:42:16.972 cpu6:4102)ScsiDeviceIO: 1688: Command 0x28 to device "naa.60060xxxxx" failed H:0x5 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.
	Aug 16 20:10:37 vmkernel: 3:12:42:16.972 cpu1:1551133)WARNING: Partition: 801: Partition table read from device naa.60060xxx failed: I/O error
	Aug 16 20:11:17 vmkernel: 3:12:42:56.982 cpu4:4100)ScsiDeviceIO: 1688: Command 0x28 to device "naa.60060xxxx" failed H:0x5 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.


VMware KB [1016106](http://kb.vmware.com/kb/1016106), matches the error. We were using MSCS but already had the patch applied mentioned in the above KB and the following option set:

> ESXi 4.1: VMware ESXi 4.1 Patch ESXi410-201107401-BG: Updates Firmware (2000609)
> ESX/ESXi 4.1: Change the advanced option Scsi.CRTimeoutDuringBoot to 1.

I also wanted to confirm the device that was experiencing the high KAVG was in fact an RDM. Checking the RDM vmdk of my VM I found the VML identifier of the RDM:


	# vmkfstools -q /vmfs/volumes/datastore/MSCS_NODE/MSCS_NODE_3.vmdk
	Disk /vmfs/volumes/datastore/MSCS_NODE/MSCS_NODE_3.vmdk is a Passthrough Raw Device Mapping
	Maps to: vml.0200050000600601603df02d00d06e9cf71b6fe111565241494420


Searching for that vml, I saw the following:


	~ # esxcfg-scsidevs -l | grep vml.0200050000600601603df02d00d06e9cf71b6fe111565241494420 -B 12
	naa.60060xxxxx
	Device Type: Direct-Access
	Size: 20480 MB
	Display Name: DGC iSCSI Disk (naa.60060xxxx)
	Multipath Plugin: NMP
	Console Device: /vmfs/devices/disks/naa.60060160xxxx
	Devfs Path: /vmfs/devices/disks/naa.60060xxxx
	Vendor: DGC Model: VRAID Revis: 0531
	SCSI Level: 4 Is Pseudo: false Status: on
	Is RDM Capable: true Is Removable: false
	Is Local: false
	Other Names:
	vml.0200050000600601603df02d00d06e9cf71b6fe111565241494420


it did correspond to one of the NAAs that I saw the high KAVG for. I wanted to see if I was seeing Reservation Conflicts on the devices that were experiencing the high KAVG. So I followed the instructions described in the yellow brick blog entitled "[Did you know? SCSI Reservations…](http://www.yellow-bricks.com/2010/10/26/did-you-know-scsi-reservations/)". This is what I saw in my esxtop output:

![high-kavg-with-rsrv-confl](https://github.com/elatov/uploads/raw/master/2012/08/high-kavg-with-rsrv-confl.png)

We can see that the column "CONS/S" has a high number for the device that is experiencing the high KAVG. Also looking at the device statistics:


	~ # vsish -e cat /storage/scsifw/devices/naa.60060xxxx/stats
	Statistics {
	commands:11816
	blocksRead:36628
	blocksWritten:0
	readOps:7468
	writeOps:0
	reserveOps:0
	reservationConflicts:10221
	total cmds split:0
	total pae cmds:0
	per split-type stats:Split type statistics {
	align:0
	maxxfer:0
	pae:0
	sgsize:0
	forcedCopy:0
	forcedSplit:0
	}


We can see that we have a high number of Reservation Conflicts on this device. This is a known issue and from this VMware KB [1009287](http://kb.vmware.com/kb/1009287) here is why:

> This issue may occur if:
>
> *   The ESX host is hosting a passive Microsoft Cluster node. This includes ESX hosts that are exposed to the LUNs used for MSCS but have no virtual machines that participate in Microsoft clustering.
> *   The virtual machine configured for the Microsoft Cluster uses an RDM. This includes RDMs exposed to the virtual machine with virtual SCSI bus sharing set to either Physical or Virtual.
>
> When ESX hosts a virtual machine in these scenarios, attempts by any ESX host (other than the one that is hosting the Active node) to conduct I/O to the LUNs used by the Microsoft Cluster results in an I/O error. This behavior is expected as the active Microsoft Cluster node maintains a SCSI reservation on the RDM LUNs.

To fix this issue you can try the following:

> To workaround this issue:
>
> *   For ESX machines that host virtual machines that participate in Microsoft Clustering and virtual machines that are configured like the above scenarios, perform the Rescan/Storage addition on the machines hosting the active Microsoft cluster node. If you want to perform those operations on the other ESX machine hosting the Passive Microsoft Cluster node, make that node Active.
> *   For ESX machines that are exposed to the LUNs used by Microsoft Clustering and no virtual machine on these hosts are involved in MSCS, VMware recommends that you do not expose the LUNs used by MSCS to ESX hosts that are not part of the Cluster configuration.
>
> **Note**: If a host is exhibiting these symptoms and does not host any of the MSCS virtual machine nodes, you may want to consider masking out the LUNs for these hosts.

If you have the luxury of updating to ESXi 5.0 then there is another fix for this. You can set the LUN as perennially reserved and then you won't run into this issue. More info from VMware KB [1016106](http://kb.vmware.com/kb/1016106):

> ESXi 5.0 uses a different technique to determine if Raw Device Mapped (RDM) LUNs are used for MSCS cluster devices, by introducing a configuration flag to mark each device as "perennially reserved" that is participating in an MSCS cluster. During a boot of an ESXi system the storage mid-layer attempts to discover all devices presented to an ESXi system during device claiming phase. However, MSCS LUNs that have a permanent SCSI reservation cause the boot process to elongate as the ESX cannot interrogate the LUN due to the persistent SCSI reservation placed on a device by an active MSCS Node hosted on another ESXi host.
>
> Configuring the device to be perennially reserved is local to each ESXi system, and must be performed on every ESXi 5.0 system that has visibility to each device participating in an MSCS cluster. This improves the boot time for all ESXi hosts that have visibility to the device(s).

Also from the same KB:

> To mark the MSCS LUNs as permanently reserved on an already upgraded ESXi 5.0 host.
>
> 1.  Determine which RDM LUNs are part of an MSCS cluster.
> 2.  From the vSphere Client, select a virtual machine that has a mapping to the MSCS cluster RDM devices.
> 3.  Edit your Virtual Machine settings and navigate to your Mapped RAW LUNs.
> 4.  Select Manage Paths to display the device properties of the Mapped RAW LUN and the device identifier (that is, the naa ID).
> 5.  Take note of the naa ID, which is a globally unique identifier for your shared device.
> 6.  Use the esxcli command to mark the device as perennially reserved:
>     1.  esxcli storage core device setconfig -d naa.id -perennially-reserved=true
> 7.  To verify that the device is perennially reserved, run this command:
>     1.  esxcli storage core device list -d naa.id
>     2.  In the output of the esxcli command, search for the entry Is Perennially Reserved: true. This shows that the device is marked as perennially reserved.
> 8.  Repeat the procedure for each Mapped RAW LUN that is participating in the MSCS cluster.
>
> **Note**: The configuration is permanently stored with the ESXi host and persists across reboots. To remove the perennially reserved flag, run this command:
>
> esxcli storage core device setconfig -d naa.id -perennially-reserved=false

This actually didn't negatively impact any of VMs or hosts, I just wanted to know what was going on. I left the setup as is and didn't see any issues, but once I update to ESXi 5.0 I will definitely set all the RDM LUNs used for MSCS as perennially reserved.

