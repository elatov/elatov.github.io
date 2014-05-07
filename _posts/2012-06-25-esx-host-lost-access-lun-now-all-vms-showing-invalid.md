---
title: ESX Host Lost Access to a LUN and Now All the VMs are Showing up as Invalid
author: Karim Elatov
layout: post
permalink: /2012/06/esx-host-lost-access-lun-now-all-vms-showing-invalid/
dsq_thread_id:
  - 1404791985
categories:
  - Storage
  - VMware
tags:
  - fcalias
  - mds 9020
  - qla2xxx
  - zones
  - zonesets
  - zoning
---
I had recently received a call saying that all of the VMs are grayed out in his inventory when logged into the vCenter and checking the storage view doesn&#8217;t show any LUNS. When I logged into the system I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/05/missing_vms.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/05/missing_vms.png']);"><img class="alignnone size-full wp-image-1530" title="missing_vms" src="http://virtuallyhyper.com/wp-content/uploads/2012/05/missing_vms.png" alt="missing vms ESX Host Lost Access to a LUN and Now All the VMs are Showing up as Invalid" width="199" height="143" /></a>

When I logged into the host I wanted to make sure we are connected to the SAN appropriately, so first I checked which HBAs are active, and I saw the following:

	  
	 # esxcfg-scsidevs -a  
	vmhba0 megaraid_sas link-n/a unknown.vmhba0 (1:0.0) LSI Logic / Symbios Logic Dell PERC 6/i  
	vmhba1 qla2xxx link-n/a fc.2000001b320b9001:2100001b320b9001 (8:0.0) QLogic Corp ISP2432-based 4Gb Fibre  
	vmhba3 ata\_piix\_ link-n/a ide.vmhba3 (0:31.1) Intel Corporation 631xESB/632_ESB IDE  
	vmhba32 usb-storage link-n/a usb.vmhba32 () USB  
	vmhba33 usb-storage link-n/a usb.vmhba33 () USB  
	vmhba34 ata\_piix link-n/a ide.vmhba34 (0:31.)} Intel Corporation 631xESB/632\_ESB IDE  
	

Checking out the proc node for the card that is showing **link-na** and is the only non-local HBA (vmhba1), we saw the following:

	  
	 # cat /proc/scsi/qla2xxx/7  
	QLogic PCI to Pibre Channel Host Adapter for QLE2460:  
	Firmware uersion 4.04.09 \[IP\] \[Multi-ID\] [84XX] , Driuer uersion 8.02.01-X1-vmw43  
	BIOS version 2.02  
	FCODE version 2.00  
	EPI version 2.00  
	Flash PW version 4.03.01  
	ISP: ISP2432  
	Request Queue = 0x1d813000, Response Queue = 0x1d894000  
	Request Queue count = 4096, Response Queue count = 512  
	Total number of interrupts = 3909  
	Device queue depth = 0x20  
	Number of free request entries = 4096  
	Number of mailbo_ timeouts = 0  
	Number of ISP aborts = 0  
	Number of loop resyncs = 1  
	Host adapter:loop state = <DEAD>, flags = 0x105a83  
	Dpc flags = 0x40180c0  
	MBX flags = 0x0  
	Link down Timeout = 045  
	Port down retry = 005  
	Login retry count = 008  
	Execution throttle = 2048  
	ZIO mode = 0_6, ZIO timer = 1  
	Commands retried with dropped frame(s) = 0  
	Product ID = 0000 0000 0000 0000
	
	NPIV Supported: yes  
	Max Virtual Ports = 127
	
	SCSI Device Information:  
	scsi-qla0-adapter-node=2000001b320b9001:000000:0;  
	scsi-qla0-adapter-port=2100001b320b9001:000000:0;
	
	FC Target-Port List:
	
	FC Port Information:  
	

And of course checking for the storage devices the host sees, we saw the following:

	  
	# esxcfg-scsidevs -c  
	Deuice UID Deuice Type Console Deuice Size Plugin Display Name  
	mpx.vmhba32:C0:T0:L0 CD-ROM /dev/sr0 0MB NMP Local USB CD-ROM (mpx.vmhba32:C0:T0:L0)  
	mpx.vmhba33:C0:T0:L0 Direct-Access /dev/sda 0MB NMP USB Direct-Access (mpx.vmhba33:C0:T0:L0)  
	mpx.vmhba3:C0:T0:L0 CD-ROM /dev/sr1 0MB NMP Local HL-DT-ST CD-ROM (mpx.vmhba3:C0:T0:L0)  
	naa.6001e4f0349cda000fa0bf4703f2279a Direct-Access /dev/sdb 69376MB NMP Local DELL Disk (naa.6001e4f0349cda000fa0bf4703f2279a)  
	

Nothing but local storage was seen.The reason why the VMs were showing up grayed out was because the HBA used to connect the SAN was down.

We moved the HBA around and it was discovered that the original HBA went bad and now the stand-by HBA had to be used. After we had moved all the cables around, we saw link up from the esx host for the good HBA:

	  
	 # cat /proc/scsi/qla2xxx/7  
	QLogic PCI to Pibre Channel Host Adapter for QLE2460:  
	Firmware uersion 4.04.09 \[IP\] \[Multi-ID\] [84XX] , Driuer uersion 8.02.01-X1-vmw43  
	BIOS version 2.02  
	FCODE version 2.00  
	EPI version 2.00  
	Flash PW version 4.03.01  
	ISP: ISP2432  
	Request Queue = 0x1d813000, Response Queue = 0x1d894000  
	Request Queue count = 4096, Response Queue count = 512  
	Total number of interrupts = 3909  
	Device queue depth = 0x20  
	Number of free request entries = 4095  
	Number of mailbo_ timeouts = 0  
	Number of ISP aborts = 0  
	Number of loop resyncs = 1  
	Host adapter:loop state = <READY> , flags = 0x105ac3  
	Dpc flags = 0x0  
	MBX flags = 0x0  
	Link down Timeout = 045  
	Port down retry = 005  
	Login retry count = 008  
	Execution throttle = 2048  
	ZIO mode = 0_6, ZIO timer = 1  
	Commands retried with dropped frame(s) = 0  
	Product ID = 0000 0000 0000 0000
	
	NPIV Supported: yes  
	Max Virtual Ports = 127
	
	SCSI Device Information:  
	scsi-qla0-adapter-node=2000001b320b9001:000000:0;  
	scsi-qla0-adapter-port=2100001b320b9001:000000:0;
	
	FC Target-Port List:
	
	FC Port Information:  
	

But now we had to modify the zoning on the SAN switch to allow the new WWN of the HBA to have access to the EMC SAN. The customer was using an MDS 9020 Cisco San switch:

	  
	san_switch# show hardware
	
	Cisco MDS 9000 FabricWare  
	Copyright (C) 2002-2005, by Cisco Systems, Inc.  
	and its suppliers. All rights reserued.  
	Copyrights to certain works contained herein are owned by  
	third parties, and used and distributed under license.  
	Portions of this software are gouerned by the GNU Public License,  
	which is available at http://www.gnu.org/licenses/gpl.html.
	
	Software  
	system: 2.1(3)  
	system compile time: Wed Jul 5 13:21:55 2006
	
	Hardware  
	san_switch uptime is 381 days 4 hours 14 minute(s) 3 second(s)
	
	Last reset at 32933643 usecs after Thu Nou 13 19:29:26 2008  
	Reason: ResetByInstaller
	
	\---\---\---\---\---\---\---\---\---\---  
	Switch hardware ID information  
	\---\---\---\---\---\---\---\---\---\---
	
	MDS Switch is booted up  
	Model number is DS-C9020-20K9  
	H/W uersion is 2.0  
	Part Number is xxxx xx  
	Part Reuision is xxx  
	Serial number is xxxxxxxx  
	CLEI code is xxxxxx  
	

First we needed to make sure that we see our WWN logged into the switch:

	  
	san_switch# show flogi database  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	INTERFACE FCID PORT\_NAME NODE\_NAME  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----
	
	fc1/3 0x760200 50:03:08:c0:9c:00:80:01 50:03:08:c0:9c:00:80:00  
	fc1/4 0x760300 21:00:00:e0:8b:93:8d:5a 20:00:00:e0:8b:93:8d:5a  
	fc1/7 0x760600 21:00:00:1b:32:0b:46:01 20:00:00:1b:32:0b:46:01  
	fc1/8 0x760700 21:00:00:1b:32:82:54:af 20:00:00:1b:32:82:54:af  
	fc1/9 0x760800 21:00:00:1b:32:82:f4:b2 20:00:00:1b:32:82:f4:b2  
	fc1/10 0x760900 21:00:00:1b:32:0b:d8:00 20:00:00:1b:32:0b:d8:00  
	fc1/11 0x760a00 21:00:00:1b:32:0b:10:01 20:00:00:1b:32:0b:10:01  
	fc1/12 0x760b00 21:00:00:1b:32:0b:91:00 20:00:00:1b:32:0b:91:00  
	fc1/13 0x760c00 21:00:00:1b:32:0b:2a:01 20:00:00:1b:32:0b:2a:01  
	fc1/14 0x760d00 50:06:01:68:41:e0:b9:44 50:06:01:60:c1:e0:b9:44  
	fc1/15 0x760e00 50:06:01:60:41:e0:b9:44 50:06:01:60:c1:e0:b9:44  
	fc1/17 0x761000 21:00:00:e0:8b:93:56:37 20:00:00:e0:8b:93:56:37  
	fc1/19 0x761200 21:00:00:1b:32:0b:49:01 20:00:00:1b:32:0b:49:01  
	fc1/20 0x761300 21:00:00:1b:32:0b:90:01 20:00:00:1b:32:0b:90:01
	
	Total number of flogi = 14  
	

The last line matches the WWN from the above output of the proc node information from the host:

	  
	SCSI Device Information:  
	scsi-qla0-adapter-node=2000001b320b9001:000000:0;  
	scsi-qla0-adapter-port=2100001b320b9001:000000:0;  
	

The customer was utilizing *fcalias*es, *zones*, and *zonesets* for his zoning, pretty standard practice on the MDS Series. More information regarding *fcalias*es, *zones*, and *zonesets* can be found in the article entitled &#8220;<a href="http://blog.scottlowe.org/2009/08/24/new-users-guide-to-configuring-cisco-mds-zones-via-cli/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.scottlowe.org/2009/08/24/new-users-guide-to-configuring-cisco-mds-zones-via-cli/']);">New User’s Guide to Configuring Cisco MDS Zones via CLI</a>&#8221; and of course from <a href="http://www.cisco.com/en/US/docs/storage/san_switches/mds9000/sw/rel_1_x/1_0_2/san-os/configuration/guide/ZoneCnfg.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cisco.com/en/US/docs/storage/san_switches/mds9000/sw/rel_1_x/1_0_2/san-os/configuration/guide/ZoneCnfg.html']);">Cisco&#8217;s Manual</a> of the switch. So we had to modify the *fcalias* (basically an alias for a wwn, but has other functions as well) and remove the original pWWN and add the new one:

	  
	san_switch# conf t  
	Enter configuration commands, one per line.
	
	san\_switch(config)# fcalias name ESXHOST3\_VMHBA2  
	san_switch(config-fcalias)# no member pwwn 21:00:00:1b:32:0b:8f:01  
	san_switch(config-fcalias)# member pwwn 21:00:00:1b:32:0b:90:01  
	san_switch(config-fcalias)#  
	

After modifying the fcalias we double checked that the *zones * (collection of fcaliases that can talk to each other) configuration has been updated:

	  
	san_switch# show zones  
	zoneset name zonesetnew  
	...  
	...  
	Zone name ESXHOST\_3\_VMHBA2  
	fcalias name ESXHOST\_3\_VMHBA2  
	pwwn 21:00:00:1b:32:0b:90:01  
	fcalias name CX3-40C_SPA  
	pwwn 50:06:01:60:41:e0:b9:44  
	fcalias name CX3-40C_SPB  
	pwwn 50:06:01:68:41:e0:b9:44  
	

That looked good, now looking at the *active zoneset* (collection of zone configurations that define access to the whole fabric, to better understand differences between zones and zoneset check out<a href="http://www.cisco.com/en/US/docs/storage/san_switches/mds9000/sw/rel_1_x/1_0_2/san-os/configuration/guide/ZoneCnfg.html#wp1082143" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cisco.com/en/US/docs/storage/san_switches/mds9000/sw/rel_1_x/1_0_2/san-os/configuration/guide/ZoneCnfg.html#wp1082143']);"> Figure 12-3 Hierarchy of Zone Sets, Zones, and Zone Members</a> from the Manual of the MDS SAN Switch) we saw the following.

	  
	san_switch# show zoneset active  
	zoneset name zonesetnew  
	...  
	...  
	zone name ESXHOST\_3\_VMHBA2  
	pwwn 21:00:00:1b:32:0b:8f:01  
	pwwn 50:06:01:60:41:e0:b9:44  
	pwwn 50:06:01:68:41:e0:b9:44  
	

It was still showing the old pWWN. We had to commit the changes that we had made by activating the zoneset:

	  
	san_switch)# conf t  
	san_switch(config)# zoneset activate name zonesetnew  
	Zoneset activation initiated. check zone status  
	san_switch(config)# end  
	san_switch#  
	

After that we ran *show zoneset active* and we didn&#8217;t see any asterisks (*) next to any zones, which means that all the zones loaded up just fine. And also after doing a rescan from the ESX host, all the original LUNs showed up on the host and all the grayed out VMs came be into inventory without any issues.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/06/esx-host-lost-access-lun-now-all-vms-showing-invalid/" title=" ESX Host Lost Access to a LUN and Now All the VMs are Showing up as Invalid" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:fcalias,mds 9020,qla2xxx,zones,zonesets,zoning,blog;button:compact;">I had recently received a call saying that all of the VMs are grayed out in his inventory when logged into the vCenter and checking the storage view doesn&#8217;t show...</a>
</p>