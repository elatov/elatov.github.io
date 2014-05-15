---
title: "Can't Set X520 10GbE Intel NIC to Auto Negotiate on ESX(i)"
author: Karim Elatov
layout: post
permalink: /2012/10/cant-set-x520-10gbe-intel-nic-to-auto-negotiate-on-esxi/
dsq_thread_id:
  - 1410006010
categories:
  - Networking
  - VMware
tags:
  - auto-negotiate
  - DID
  - esxcfg-nics
  - ethtool -i
  - ixgbe
  - mount ISO
  - scp
  - SDID
  - SVID
  - tree
  - VID
  - vim-cmd hostsvc/maintenance_mode_enter
  - vim-cmd hostsvc/runtimeinfo
  - vmkchdev
  - vmkload_mod
  - VMware HCL
  - X520 10GbE
---
We were following the instructions laid out in VMware KB <a href="http://kb.vmware.com/kb/1004089" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1004089']);">1004089</a> to set a NIC to auto negotiate with the upstream switch. Upon running the command, we would see the following message:

	  
	~ # esxcfg-nics -a vmnic7  
	Error: Invalid argument: Invalid argument  
	

Here is the model of NIC:

	  
	~ # esxcfg-nics -l | grep vmnic7  
	vmnic7 ixgbe Up 10000Mbps Full Intel Corporation Ethernet X520 10GbE Dual Port KX4-KR Mezz  
	

And here is the Vendor information of the NIC.

	  
	~ # vmkchdev -l | grep vmnic7  
	000:002:00.0 8086:10f8 8086:000c vmkernel vmnic7  
	

Lastly, here is the ESXi version of the host:

	  
	~ # vmware -lv  
	VMware ESXi 4.1.0 build-502767  
	VMware ESXi 4.1.0 Update 2  
	

We went to VMware <a href="http://www.vmware.com/resources/compatibility/search.php?deviceCategory=io" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/search.php?deviceCategory=io']);">HCL</a> and entered the following information under the "IO Devices" Section of the HCL:

> VID 8086  
> DID 10f8  
> SVID 8086  
> SDID 000c

That led us to the <a href="http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=17547&deviceCategory=io&VID=8086&DID=10F8&SVID=8086&SSID=000C&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=17547&deviceCategory=io&VID=8086&DID=10F8&SVID=8086&SSID=000C&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc']);">HCL</a> page for the Card. From that page, I saw the following information:

> ESX / ESXi 4.1 U2 ixgbe version 3.9.13 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 3.7.13 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 3.6.5 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 3.4.23 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 3.1.17.1 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 2.0.84.9 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 2.0.62.4.8 N/A async  
> ESX / ESXi 4.1 U2 ixgbe version 2.0.38.2.5.1 N/A async

So the latest driver for this card is 3.9.13, while we were running the following:

	  
	~ # ethtool -i vmnic7  
	driver: ixgbe  
	version: 3.1.17.1-NAPI  
	firmware-version: 1.0-3  
	bus-info: 0000:02:00.0  
	

We decided to try out the latest driver. <a href="https://my.vmware.com/web/vmware/details?downloadGroup=DT-ESX4X-Intel-ixgbe-3913&productId=230" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://my.vmware.com/web/vmware/details?downloadGroup=DT-ESX4X-Intel-ixgbe-3913&productId=230']);">Here</a> is the link to the ixgbe 3.9.13 driver for ESX(i) 4.x. We read over the instructions laid out in the VMware KB Entitled <a href="http://kb.vmware.com/kb/1032936" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1032936']);">Installing async drivers on ESX/ESXi 4.x</a> and here are the instructions from the KB:

> **Existing ESX or ESXi Installation using esxupdate and Datastore Browser**
> 
> An existing ESX or ESXi host can install offline bundles that have been copied from the Async release ISO to the ESX or ESXi host.
> 
> 1.  Extract the contents of the ISO file.
> 2.  Identify the .zip file(s).
> 3.  Using Datastore Browser, upload the .zip file(s) to an ESX or ESXi host's datastore.
> 4.  Log in to the ESX or ESXi host using an account with administrator privileges, such as root.
> 5.  Enter maintenance mode.
> 6.  Navigate to /vmfs/volumes// and locate the .zip file.
> 7.  Run this command to install drivers using the offline bundle:  
	>       
	>     esxupdate --bundle=OFFLINE_BUNDLE.zip update  
	>      
> 8.  Reboot the ESX or ESXi host.
> 9.  Exit maintenance mode.

Here is what I did to get the offline zip file from the ISO (I used my fedora laptop). After I downloaded the driver, I had the following file:

	  
	$ ls -l | grep iso  
	-rw-rw-r-- 1 elatov elatov 1906688 Oct 27 12:43 vmware-esx-drivers-net-ixgbe_400.3.9.13-1vmw.2.17.249663.697530.iso  
	

I then mounted the iso:

	  
	$ sudo mkdir /media/iso  
	$ sudo mount vmware-esx-drivers-net-ixgbe_400.3.9.13-1vmw.2.17.249663.697530.iso /media/iso  
	

Then checking out the contents of the iso, I saw the following:

	  
	$ tree /media/iso  
	/media/iso  
	├── doc  
	│   ├── open\_source\_licenses\_vmware-esx-drivers-net-ixgbe\_400.3.9.13-1vmw.2.17.249663.txt  
	│   ├── README.txt  
	│   ├── release\_note\_vmware-esx-drivers-net-ixgbe_400.3.9.13-1vmw.2.17.249663.txt  
	│   └── TRANS.TBL  
	├── drivers.xml  
	├── offline-bundle  
	│   ├── INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663-offline_bundle-697530.zip  
	│   └── TRANS.TBL  
	├── source  
	│   ├── driver-source-vmware-esx-drivers-net-ixgbe_400.3.9.13-1vmw.2.17.249663.tar  
	│   └── TRANS.TBL  
	└── TRANS.TBL
	
	3 directories, 10 files  
	

I went ahead and uploaded the 'INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663-offline_bundle-697530.zip' file to the ESXi host:

	  
	$ scp /media/iso/offline-bundle/INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663-offline_bundle-697530.zip root'@'10.0.1.128:/vmfs/volumes/datastore1/.  
	root'@'10.0.1.128's password  
	INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663-o 100% 102KB 102.1KB/s 00:00  
	

I then put the host in maintenance mode.

	  
	~ # vim-cmd hostsvc/maintenance\_mode\_enter  
	'vim.Task:haTask-ha-host-vim.HostSystem.enterMaintenanceMode-20'  
	

I let DRS move all the VMs off and then confirming that the host is in maintenance mode:

	  
	~ # vim-cmd hostsvc/runtimeinfo | grep -i maint  
	inMaintenanceMode = true,  
	

That looked good. Now checking the driver version:

	  
	~ # esxupdate --bundle=/vmfs/volumes/datastore1/INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663-offline_bundle-697530.zip info  
	ID - INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663  
	Release Date - 2012-04-25T16:50:07  
	Vendor - Intel  
	Summary - ixgbe: Intel(R) 10GbE PCI Express Ethernet Connection driver  
	for VMware ESX Server 4.0  
	Severity - general  
	Urgency -  
	Category - general  
	Install Date -  
	Description - This package contains the VMware ESX 4.0 driver for the  
	Intel(R) 10GbE PCI Express Family of Server Adapters.  
	KB URL -
	
	http://www.intel.com/network/connectivity/products/server_adap
	
	ters.htm  
	Contact - linux.nics'@'intel.com  
	Compliant - False  
	RebootRequired - True  
	HostdRestart - False  
	MaintenanceMode - True  
	List of constituent VIBs:  
	cross\_vmware-esx-drivers-net-ixgbe\_400.3.9.13-1vmw.2.17.249663  
	

That also looked good, then finally installing the driver:

	  
	~ # esxupdate --bundle=/vmfs/volumes/datastore1/INT-intel-lad-ddk-ixgbe-400.3.9.13-1.249663-offline_bundle-697530.zip update  
	Unpacking cross_vmware-esx-dr.. ######################################## [100%]
	
	Removing packages :vmware-esx.. ######################################## [100%]
	
	Installing packages :cross_vm.. ######################################## [100%]
	
	Running [/usr/sbin/vmkmod-install.sh]...  
	ok.  
	The update completed successfully, but the system needs to be rebooted for the  
	changes to be effective.  
	

After the install, I rebooted the host:

	  
	~ # reboot  
	

After the host rebooted, I then exited maintenance mode:

	  
	~ # vim-cmd hostsvc/maintenance\_mode\_exit  
	'vim.Task:haTask-ha-host-vim.HostSystem.exitMaintenanceMode-18'  
	

and I was able to set the NIC to auto negotiate:

	  
	~ # esxcfg-nics -a vmnic7  
	~ # ethtool vmnic7 | grep auto  
	Supports auto-negotiation: Yes  
	Advertised auto-negotiation: Yes  
	

Lastly confirming the driver:

	  
	~ # vmkload_mod -s ixgbe | grep -i version  
	Version: Version 3.9.13-NAPI, Build: 249663, Interface: 9.0, Built on: Apr 12 2012  
	

and 

	  
	~ # ethtool -i vmnic7  
	driver: ixgbe  
	version: 3.9.13-NAPI  
	firmware-version: 0x54600001  
	bus-info: 0000:02:00.0  
	

Everything was working as expected: I had the latest driver installed and I was able to set my NIC to auto negotiate.

