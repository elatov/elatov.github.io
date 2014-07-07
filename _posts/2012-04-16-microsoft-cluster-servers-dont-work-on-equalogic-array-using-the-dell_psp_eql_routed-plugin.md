---
published: true
title: "Microsoft Cluster Servers Don't Work on Equalogic Array Using the DELL_PSP_EQL_ROUTED Plugin"
author: Karim Elatov
layout: post
permalink: /2012/04/microsoft-cluster-servers-dont-work-on-equalogic-array-using-the-dell_psp_eql_routed-plugin/
dsq_thread_id:
  - 1408177985
categories: ['storage', 'vmware']
tags: ['dell_psp_eql_routed', 'equallogic', 'exscli', 'mscs', 'psp', 'rdm', 'vmw_satp_eql', 'vmw_satp_fixed']
---

Recently I ran into an issue with Microsoft Cluster Servers (MSCS) on two VMware VMs. The first VM would boot up just fine, but the second VM would take a long time to boot up and sometimes it wouldn't boot at all. I tracked down the naa of the RDM that was used for MSCS VM and I took a look at the settings of that LUN:


	# esxcli nmp device list -d  naa.6090a088006f910fe8df241e1a01d012
	naa.6090a088006f910fe8df241e1a01d012
	Device Display Name: EQLOGIC iSCSI Disk (naa.6090a088006f910fe8df241e1a01d012)
	Storage Array Type: VMW_SATP_EQL
	Storage Array Type Device Config: SATP VMW_SATP_EQL does not support device configuration.
	Path Selection Policy: DELL_PSP_EQL_ROUTED
	Path Selection Policy Device Config: PSP DELL_PSP_EQL_ROUTED does not support device configuration.
	Working Paths: vmhba33:C7:T12:L0, vmhba33:C6:T12:L0, vmhba33:C4:T12:L0, vmhba33:C3:T12:L0, vmhba33:C5:T12:L0, vmhba33:C0:T12:L0

	# esxcfg-mpath -b -d naa.6090a088006f910fe8df241e1a01d012
	naa.6090a088006f910fe8df241e1a01d012 : EQLOGIC iSCSI Disk (naa.6090a088006f910fe8df241e1a01d012)
	vmhba33:C7:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d060002 PortalTag=1
	vmhba33:C6:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d050003 PortalTag=1
	vmhba33:C4:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d030002 PortalTag=1
	vmhba33:C3:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d020003 PortalTag=1
	vmhba33:C5:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d040003 PortalTag=1
	vmhba33:C0:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d000002 PortalTag=1


As you can see the SATP used is VMW_SATP_EQL and the PSP used is DELL_PSP_EQL_ROUTED for that LUN. The PSP is DELL_PSP_EQL_ROUTED works in a very similar way as VMW_PSP_RR. All paths are seen as active and IO can go across all the paths. Per KB [EqualLogic PS6000X](http://kb.vmware.com/kb/1037959)) we can see that a FIXED pathing policy can be used for this Array, so let's set the pathing policy to FIXED for the RDMs used for MSCS:


	# esxcli nmp device setpolicy --psp VMW_PSP_FIXED -d naa.6090a088006f910fe8df241e1a01d012


After that we don't see all the paths set as working paths:


	# esxcli nmp device list -d  naa.6090a088006f910fe8df241e1a01d012
	naa.6090a088006f910fe8df241e1a01d012
	Device Display Name: EQLOGIC iSCSI Disk (naa.6090a088006f910fe8df241e1a01d012)
	Storage Array Type: VMW_SATP_EQL
	Storage Array Type Device Config: SATP VMW_SATP_EQL does not support device configuration.
	Path Selection Policy: VMW_PSP_FIXED
	Path Selection Policy Device Config: {preferred=vmhba33:C7:T12:L0;current=vmhba33:C7:T12:L0}
	Working Paths: vmhba33:C7:T12:L0


After setting changing the PSP, both VMs booted up just fine and didn't have any issue sharing the RDM. Since we are using iSCSI, I would also recommend not presenting RDMs but instead using an in-guest iSCSI initiator to get to a supported configuration. See [this KB](http://kb.vmware.com/kb/1037959) for more information on supported MSCS configurations.

