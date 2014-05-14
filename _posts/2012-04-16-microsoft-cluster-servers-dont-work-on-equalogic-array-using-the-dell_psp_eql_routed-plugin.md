---
title: 'Microsoft Cluster Servers Don&#8217;t Work on Equalogic Array Using the DELL_PSP_EQL_ROUTED Plugin'
author: Karim Elatov
layout: post
permalink: /2012/04/microsoft-cluster-servers-dont-work-on-equalogic-array-using-the-dell_psp_eql_routed-plugin/
dsq_thread_id:
  - 1408177985
categories:
  - Storage
  - VMware
tags:
  - DELL_PSP_EQL_ROUTED
  - EqualLogic
  - exscli
  - MSCS
  - PSP
  - RDM
  - VMW_SATP_EQL
  - VMW_SATP_FIXED
---
Recently I ran into an issue with Microsoft Cluster Servers (MSCS) on two VMware VMs. The first VM would boot up just fine, but the second VM would take a long time to boot up and sometimes it wouldn&#8217;t boot at all. I tracked down the naa of the RDM that was used for MSCS VM and I took a look at the settings of that LUN:

	  
	# esxcli nmp device list -d  naa.6090a088006f910fe8df241e1a01d012  
	naa.6090a088006f910fe8df241e1a01d012  
	Device Display Name: EQLOGIC iSCSI Disk (naa.6090a088006f910fe8df241e1a01d012)  
	Storage Array Type: VMW\_SATP\_EQL  
	Storage Array Type Device Config: SATP VMW\_SATP\_EQL does not support device configuration.  
	Path Selection Policy: DELL\_PSP\_EQL_ROUTED  
	Path Selection Policy Device Config: PSP DELL\_PSP\_EQL_ROUTED does not support device configuration.  
	Working Paths: vmhba33:C7:T12:L0, vmhba33:C6:T12:L0, vmhba33:C4:T12:L0, vmhba33:C3:T12:L0, vmhba33:C5:T12:L0, vmhba33:C0:T12:L0
	
	# esxcfg-mpath -b -d naa.6090a088006f910fe8df241e1a01d012  
	naa.6090a088006f910fe8df241e1a01d012 : EQLOGIC iSCSI Disk (naa.6090a088006f910fe8df241e1a01d012)  
	vmhba33:C7:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d060002 PortalTag=1  
	vmhba33:C6:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d050003 PortalTag=1  
	vmhba33:C4:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d030002 PortalTag=1  
	vmhba33:C3:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d020003 PortalTag=1  
	vmhba33:C5:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d040003 PortalTag=1  
	vmhba33:C0:T12:L0 LUN:0 state:active iscsi Adapter: iqn.1998-01.com.vmware:xxxxx  Target: IQN=iqn.2001-05.com.equallogic:xxxxx Alias= Session=00023d000002 PortalTag=1  
	

As you can see the SATP used is VMW\_SATP\_EQL and the PSP used is DELL\_PSP\_EQL\_ROUTED for that LUN. The PSP is DELL\_PSP\_EQL\_ROUTED works in a very similar way as VMW\_PSP\_RR. All paths are seen as active and IO can go across all the paths. Per KB <a href="http://kb.vmware.com/kb/1037959" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1037959']);">1037959</a>, we can&#8217;t use RR for MSCS nor can we use iSCSI, but hey. So looking at the HCL for that SAN (<a href="http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=10040&deviceCategory=san&partner=23&keyword=EQ&arrayTypes=1&isSVA=1&page=2&display_interval=10&sortColumn=Partner&sortOrder=As" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=san&productid=10040&deviceCategory=san&partner=23&keyword=EQ&arrayTypes=1&isSVA=1&page=2&display_interval=10&sortColumn=Partner&sortOrder=As']);">EqualLogic PS6000X</a>) we can see that a FIXED pathing policy can be used for this Array, so let&#8217;s set the pathing policy to FIXED for the RDMs used for MSCS:

	  
	# esxcli nmp device setpolicy --psp VMW\_PSP_FIXED -d naa.6090a088006f910fe8df241e1a01d012  
	

After that we don&#8217;t see all the paths set as working paths:

	  
	# esxcli nmp device list -d  naa.6090a088006f910fe8df241e1a01d012  
	naa.6090a088006f910fe8df241e1a01d012  
	Device Display Name: EQLOGIC iSCSI Disk (naa.6090a088006f910fe8df241e1a01d012)  
	Storage Array Type: VMW\_SATP\_EQL  
	Storage Array Type Device Config: SATP VMW\_SATP\_EQL does not support device configuration.  
	Path Selection Policy: VMW\_PSP\_FIXED  
	Path Selection Policy Device Config: {preferred=vmhba33:C7:T12:L0;current=vmhba33:C7:T12:L0}  
	Working Paths: vmhba33:C7:T12:L0  
	

After setting changing the PSP, both VMs booted up just fine and didn&#8217;t have any issue sharing the RDM. Since we are using iSCSI, I would also recommend not presenting RDMs but instead using an in-guest iSCSI initiator to get to a supported configuration. See <a href="http://kb.vmware.com/kb/1037959" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1037959']);" target="_blank">this KB</a> for more information on supported MSCS configurations.

