---
title: Installing be2iscsi Driver Version 4.1.334.3 on HP BL495c G6 with NC553m CNAs Causes ESXi Host to PSOD
author: Karim Elatov
layout: post
permalink: /2012/11/installing-be2iscsi-version-4-1-334-3-on-bl495c-g6-for-nc553m-cnas-causes-esxi-host-to-psod/
dsq_thread_id:
  - 1407612394
categories:
  - Networking
  - Storage
  - VMware
tags:
  - be2iscsi
  - be2net
  - be_char_ioctl
  - BL495c
  - hp recipe
  - NC553m
  - PSOD
  - vmkload_mod
---
We were looking at the* September 2012 VMware FW and Software Recipe* page and we wanted to install the latest be2iscsi driver. From the page here is the recommended version:

![iscsi_hp_recipes](https://github.com/elatov/uploads/raw/master/2012/11/iscsi_hp_recipes.png)

Here is VMware HCL [link](http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&#038;productid=19645&#038;deviceCategory=io&#038;keyword=nc553m&#038;page=1&#038;display_interval=10&#038;sortColumn=Partner&#038;sortOrder=Asc) for the CNA.

After we installed the driver and rebooted the host, we saw the following PSOD:

![psod_be2iscsi](https://github.com/elatov/uploads/raw/master/2012/11/psod_be2iscsi.png)

here is the backtrace:


	0x412242f1a850:[0x41803745573e]be_char_ioctl'@'<None>#<None>+0xc8 stack: 0x412242f1ad21
	0x412242f1a960:[0x418037646620]LinuxCharIoctl'@'com.vmware.driverAPI#9.2+0x127 stack: 0x412242f27040
	0x412242f1a9e0:[0x418036d51292]VMKAPICharDevDevfsWrapIoctl'@'vmkernel#nover+0x109 stack: 0x412242f1aa
	0x412242f1ac10:[0x4180370dc4d8]DevFSIoctl'@'vmkernel#nover+0x9bf stack: 0x412242f1ad8c
	0x412242f1ac70:[0x41803709d35d]FSS2_IoctlByFH'@'vmkernel#nover+0x434 stack: 0xbcd42f1ad20
	0x412242f1acc0:[0x41803709ceb0]FSS_IoctlByFH'@'vmkernel#nover+0x8f stack: 0xffd6223cc0105500
	0x412242f1ace0:[0x41803745573e]UserFile_PassthroughIoctl'@'<None>#<None>+0x41 stack: 0x412242f1ad60
	0x412242f1ad60:[0x418037511822]UserVmfs_Ioctl'@'<None>#<None>+0xa9 stack: 0x41003eba39e0
	0x412242f1adc0:[0x4180374744b4]LinuxFileDesc_Ioctl'@'<None>#<None>+0x163 stack: 0x412242f1ae00
	0x412242f1af10:[0x418036d3e0e9]User_LinuxSyscallHandler@vmkernel#nover+0x1c stack: 0xffd62258


we see a *be* and that is pointing to the *be2net* or *be2iscsi* driver causing the PSOD. We were already updating to the latest version of the be2iscsi driver, so the next thing to try is to update the *be2net* driver. I rebooted the host and the *be2iscsi* driver was automatically removed and the host rebooted fine (no PSODs were seen). I checked out the driver version of be2net, and I saw the following:


	~ # vmkload_mod -s be2net | head -4
	vmkload_mod module information
	input file: /usr/lib/vmware/vmkmod/be2net
	License: GPL
	Version: Version 4.0.88.0, Build: 515841, Interface: 9.2 Built on: Oct 28 2011


I actually ran into VMware KB [2007397](http://kb.vmware.com/kb/2007397), from that KB:

> **Emulex OneConnect driver not supported on vSphere 5.0 for HP hardware**
> ...
> ...
> HP has recalled firmware version 4.0.348.0, which was compatible with the vSphere 5.0 async be2net driver version 4.0.355-1. For more information, see the HP Advisory http://h20000.www2.hp.com/bizsupport/TechSupport/Document.jsp?objectID=c03005737.
>
> **Resolution**
> To resolve this issue, contact HP for the newer Emulex firmware.
>
> For ESXi 5.0, use these drivers:
>
> be2net: 4.0.355.1: http://downloads.vmware.com/d/details/dt_esxi50_emulex_be2net_403551/dHRAYnQqQHBiZHAlJQ
> be2iscsi: 4.0.317.0: http://downloads.vmware.com/d/details/dt_esxi50_emulex_oce11100_403170/dHRAYnRqdCViZHAlJQ
> lpfc: 8.2.2.105.36: http://downloads.vmware.com/d/details/dt_esxi50_emulex_lpfc820_82210536/dHRAYnRoZCViZHAlJQ

I decided to update my *be2net* driver from 4.0.88 to 4.0.355 (link to driver is above). I installed the driver and rebooted, here is how my driver/firmware looked like:


	~ # ethtool -i vmnic4
	driver: be2net
	version: 4.0.355.1
	firmware-version: 4.1.450.16
	bus-info: 0000.0e:00.0


And I didn't see another PSOD. I then re-installed *be2iscsi* version 4.1.334.3 on the same host. I then rebooted one more time and no PSOD occurred. It looks like I needed to update the *be2net* driver first, before applying the latest *be2iscsi* driver.

