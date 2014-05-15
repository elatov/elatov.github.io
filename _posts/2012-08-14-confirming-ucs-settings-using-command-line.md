---
title: Checking UCS Settings from the UCS Manager CLI
author: Karim Elatov
layout: post
permalink: /2012/08/confirming-ucs-settings-using-command-line/
dsq_thread_id:
  - 1404672898
categories:
  - Home Lab
  - VMware
tags:
  - UCS
  - UCS Polices
  - UCS Pools
  - UCS Service Profiles
  - UCSM
  - Unified Cisco Systems
  - vHBA
  - vNIC
---
I was recently using the UCS Manager CLI and I wanted to share my findings. You can SSH to the UCSM (UCS Manager) and then run commands to figure out information about your hardware configuration. Whenever working with Cisco UCS Servers, the first thing we need to figure out is how Service Profiles are used in a UCS Environment. Cisco has an excellent article about this entitled "<a href="http://www.cisco.com/en/US/prod/collateral/ps10265/ps10281/white_paper_c11-590518.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.cisco.com/en/US/prod/collateral/ps10265/ps10281/white_paper_c11-590518.pdf']);">Understanding Cisco Unified Computing System Service Profiles</a>". Also from the "<a href="http://www.cisco.com/en/US/docs/unified_computing/ucs/sw/cli/config/guide/2.0/b_UCSM_CLI_Configuration_Guide_2_0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.cisco.com/en/US/docs/unified_computing/ucs/sw/cli/config/guide/2.0/b_UCSM_CLI_Configuration_Guide_2_0.pdf']);">Cisco UCS Manager CLI Configuration Guide, Release 2.0</a>", I like their definition:

> Service profiles are the central concept of Cisco UCS. Each service profile serves a specific purpose: ensuring that the associated server hardware has the configuration required to support the applications it will host.
> 
> The service profile maintains configuration information about the server hardware, interfaces, fabric  
> connectivity, and server and network identity. This information is stored in a format that you can manage through Cisco UCS Manager. All service profiles are centrally managed and stored in a database on the fabric interconnect.
> 
> Every server must be associated with a service profile.

Service Profiles consist of Policies:

> Policies determine how Cisco UCS components will act in specific circumstances. You can create multiple instances of most policies. For example, you might want different boot policies, so that some servers can PXE boot, some can SAN boot, and others can boot from local storage.
> 
> Policies allow separation of functions within the system. A subject matter expert can define policies that are used in a service profile, which is created by someone without that subject matter expertise. For example, a LAN administrator can create adapter policies and quality of service policies for the system. These policies can then be used in a service profile that is created by someone who has limited or no subject matter expertise with LAN administration.
> 
> You can create and use two types of policies in Cisco UCS Manager:
> 
> *   Configuration policies that configure the servers and other components
> *   Operational policies that control certain management, monitoring, and access control functions

So first find out what is the name of the server that you are working with. You can either look at the UCSM Web Page or if you know the name of the server you can find out what chassis your blade is in. To see all the available servers you can do the following:

	  
	Cisco UCS 6100 Series Fabric Interconnect  
	Using keyboard-interactive authentication.  
	Password:  
	Cisco Nexus Operating System (NX-OS) Software  
	TAC support: http://www.cisco.com/tac  
	Copyright (c) 2002-2012, Cisco Systems, Inc. All rights reserved.  
	The copyrights to certain works contained in this software are  
	owned by other third parties and used and distributed under  
	license. Certain components of this software are licensed under  
	the GNU General Public License (GPL) version 2.0 or the GNU  
	Lesser General Public License (LGPL) Version 2.1. A copy of each  
	such license is available at  
	http://www.opensource.org/licenses/gpl-2.0.php and
	
	http://www.opensource.org/licenses/lgpl-2.1.php
	
	p2-ucsm-A# show service-profile inventory  
	Service Profile Name Type Server Assignment Association  
	-------------------- ----------------- ------- ---------- -----------  
	p2-b200 Initial Template Unassigned Unassociated  
	p2-b200-1 Instance 1/1 Assigned Associated  
	p2-b200-2 Instance 1/2 Assigned Associated  
	p2-b250 Initial Template Unassigned Unassociated  
	p2-b250-3 Instance 1/3 Assigned Associated  
	

Each Server has a Service Profile Attached to it. I will be working with p2-b200-1 Service Profile, which corresponds to Chassis 1, Server 2. So let's check out the HBAs that are available for this server:

	  
	p2-ucsm-A# scope chassis 1  
	p2-ucsm-A /chassis # scope server 2  
	p2-ucsm-A /chassis/server # scope adapter 1  
	p2-ucsm-A /chassis/server/adapter # show host-fc-if
	
	FC Interface:  
	Id Wwn Model Name Operability  
	---------- ----------------------- ---------- ---------- -----------  
	1 20:00:00:25:B5:02:0B:02 N20-AC0002 fc1 Operable  
	2 20:00:00:25:B5:02:0A:02 N20-AC0002 fc0 Operable  
	

We can see we have two HBAs on the server and their corresponding WWPNs. We can also check out the available NICs:

	  
	p2-ucsm-A /chassis/server/adapter # show host-eth-if
	
	Eth Interface:  
	ID Dynamic MAC Address Name Operability  
	---------- ------------------- ---------- -----------  
	1 00:25:B5:02:01:01 eth0 Operable  
	2 00:25:B5:02:02:01 eth1 Operable  
	3 00:25:B5:02:03:01 eth2 Operable  
	4 00:25:B5:02:04:01 eth3 Operable  
	7 00:25:B5:02:07:01 eth6 Operable  
	8 00:25:B5:02:08:01 eth7 Operable  
	

You can see that there are different MACs and WWPNs assigned for this server. To see the distinguished name of you adapters you can run the following:

	  
	p2-ucsm-A /chassis/server # show server adapter vnics
	
	Eth Interface:
	
	Adapter Interface Vnic Dn Dynamic MAC Addr Type  
	------- --------- ---------- ---------------- ----  
	1 1 org-root/ls-p2-b200-1/ether-eth0 00:25:B5:02:01:02 Ether  
	1 2 org-root/ls-p2-b200-1/ether-eth1 00:25:B5:02:02:02 Ether  
	1 3 org-root/ls-p2-b200-1/ether-eth2 00:25:B5:02:03:02 Ether  
	1 4 org-root/ls-p2-b200-1/ether-eth3 00:25:B5:02:04:02 Ether  
	1 7 org-root/ls-p2-b200-1/ether-eth6 00:25:B5:02:07:02 Ether  
	1 8 org-root/ls-p2-b200-1/ether-eth7 00:25:B5:02:08:02 Ether
	
	FC Interface:
	
	Adapter Interface Vnic Dn Dynamic WWPN Type  
	------- --------- ---------- ------------ ----  
	1 1 org-root/ls-p2-b200-1/fc-fc1 20:00:00:25:B5:02:0B:01 Fc  
	1 2 org-root/ls-p2-b200-1/fc-fc0 20:00:00:25:B5:02:0A:01 Fc  
	

The WWPNs and the MACs are assigned to the devices, this is actually defined in the pools. From the config guide:

> Pools are collections of identities, or physical or logical resources, that are available in the system. All pools increase the flexibility of service profiles and allow you to centrally manage your system resources.
> 
> You can use pools to segment unconfigured servers or available ranges of server identity information into groupings that make sense for the data center. For example, if you create a pool of unconfigured servers with similar characteristics and include that pool in a service profile, you can use a policy to associate that service profile with an available, unconfigured server.
> 
> If you pool identifying information, such as MAC addresses, you can pre-assign ranges for servers that will host specific applications. For example, all database servers could be configured within the same range of MAC addresses, UUIDs, and WWNs.

To see what pool your vHBA belongs to, you can run the following:

	  
	p2-ucsm-A# scope service-profile server 1/2  
	p2-ucsm-A /org/service-profile # show vhba detail
	
	vHBA:  
	Name: fc0  
	Fabric ID: A  
	Dynamic WWPN: 20:00:00:25:B5:02:0A:02  
	Desired Order: Unspecified  
	Actual Order: 8  
	Desired VCon Placement: Any  
	Actual VCon Placement: 1  
	Equipment: sys/chassis-1/blade-2/adaptor-1/host-fc-2  
	Template Name: vHBA-A  
	Oper Nw Templ Name: org-root/san-conn-templ-vHBA-A  
	Persistent Binding: Disabled  
	Max Data Field Size: 2048  
	Adapter Policy: VMWare  
	Oper Adapter Policy: org-root/fc-profile-VMWare  
	WWPN Pool: WWPN_Pod2_A  
	Oper Ident Pool Name: org-root/wwn-pool-WWPN_Pod2_A  
	Pin Group:  
	QoS Policy:  
	Oper QoS Policy:  
	Stats Policy: default  
	Oper Stats Policy: org-root/thr-policy-default  
	Current Task:
	
	Name: fc1  
	Fabric ID: B  
	Dynamic WWPN: 20:00:00:25:B5:02:0B:02  
	Desired Order: Unspecified  
	Actual Order: 7  
	Desired VCon Placement: Any  
	Actual VCon Placement: 1  
	Equipment: sys/chassis-1/blade-2/adaptor-1/host-fc-1  
	Template Name: vHBA-B  
	Oper Nw Templ Name: org-root/san-conn-templ-vHBA-B  
	Persistent Binding: Disabled  
	Max Data Field Size: 2048  
	Adapter Policy: VMWare  
	Oper Adapter Policy: org-root/fc-profile-VMWare  
	WWPN Pool: WWPN_Pod2_B  
	Oper Ident Pool Name: org-root/wwn-pool-WWPN_Pod2_B  
	Pin Group:  
	QoS Policy:  
	Oper QoS Policy:  
	Stats Policy: default  
	Oper Stats Policy: org-root/thr-policy-default  
	Current Task:  
	

You can see that vHBA1 (fc0) is from WWPN_Pod2_A and vHBA2 (fc1) is from WWPN_Pod2_B. To see a list of defined pools you can run the following:

	  
	p2-ucsm-A# scope org  
	p2-ucsm-A /org # show wwn-pool
	
	WWN Pool:  
	Name Purpose Size Assigned  
	-------------------- ------------------- ---------- --------  
	default Port Wwn Assignment 0 0  
	node-default Node Wwn Assignment 0 0  
	USL_Pod2 Node Wwn Assignment 3 3  
	WWPN_Pod2_A Port Wwn Assignment 3 3  
	WWPN_Pod2_B Port Wwn Assignment 3 3  
	

We are using the bottom two. Just to see the pattern of the pool let's check out one of them:

	  
	p2-ucsm-A# scope org  
	p2-ucsm-A /org # scope wwn-pool WWPN_Pod2_A  
	p2-ucsm-A /org/wwn-pool # show expand
	
	WWN Pool:  
	Name: WWPN_Pod2_A  
	Purpose: Port Wwn Assignment  
	Size: 3  
	Assigned: 3
	
	WWN Initiator Block:  
	From To  
	----------------------- --  
	20:00:00:25:B5:02:0A:00 20:00:00:25:B5:02:0A:02
	
	WWN Initiator:  
	Id: 20:00:00:25:B5:02:0A:00  
	Name:  
	Assigned: Yes  
	Assigned To Dn: org-root/ls-p2-b250-3/fc-fc0
	
	Id: 20:00:00:25:B5:02:0A:01  
	Name:  
	Assigned: Yes  
	Assigned To Dn: org-root/ls-p2-b200-1/fc-fc0
	
	Id: 20:00:00:25:B5:02:0A:02  
	Name:  
	Assigned: Yes  
	Assigned To Dn: org-root/ls-p2-b200-2/fc-fc0  
	

So our range is defined as follows; 20:00:00:25:B5:02:0A:00 to  20:00:00:25:B5:02:0A:02. To get a list of all the WWPNs assigned from this pool in a concise manner you can run the following:

	  
	p2-ucsm-A /org/wwn-pool # show initiator
	
	WWN Initiator:  
	Id Name Assigned Assigned To Dn  
	----------------------- ---------- -------- --------------  
	20:00:00:25:B5:02:0A:00 Yes org-root/ls-p2-b250-3/fc-fc0  
	20:00:00:25:B5:02:0A:01 Yes org-root/ls-p2-b200-1/fc-fc0  
	20:00:00:25:B5:02:0A:02 Yes org-root/ls-p2-b200-2/fc-fc0  
	

You can check similar setting for the mac pools as well. If you have two IO Modules in the enclosure/chassis then you define two fabrics; a and b. We had two modules:

	  
	p2-ucsm-A# scope chassis 1  
	p2-ucsm-A /chassis # show iom
	
	IOM:  
	ID Side Fabric ID Overall Status  
	---------- ----- --------- --------------  
	1 Left A Operable  
	2 Right B Operable
	
	

You can also check if the server is connected to both IOMs:

	  
	p2-ucsm-A# scope server 1/2  
	p2-ucsm-A /chassis/server # show status detail  
	Server 1/2:  
	Name:  
	User Label:  
	Slot Status: Equipped  
	Conn Path: A,B  
	Conn Status: A,B  
	Managing Instance: A  
	Availability: Unavailable  
	Admin State: In Service  
	Overall Status: Ok  
	Oper Qualifier: N/A  
	Discovery: Complete  
	Current Task:  
	

We can see our connection path is to A and B, both of our fabrics. For each Fabric we usually have a fabric-interconnect:

	  
	p2-ucsm-A# show fabric-interconnect
	
	Fabric Interconnect:  
	ID OOB IP Addr OOB Gateway OOB Netmask Operability  
	---- --------------- --------------- --------------- -----------  
	A 10.102.100.13 10.102.100.1 255.255.255.0 Operable  
	B 10.102.100.15 10.102.100.1 255.255.255.0 Operable  
	

Usually you setup "pinning" to pin you HBAs and NICs to a certain IO module, for load balancing. From the Config Guide:

> Pinning in Cisco UCS is only relevant to uplink ports. You can pin Ethernet or FCoE traffic from a given  
> server to a specific uplink Ethernet port or uplink FC port.
> 
> When you pin the NIC and HBA of both physical and virtual servers to uplink ports, you give the fabric  
> interconnect greater control over the unified fabric. This control ensures more optimal utilization of uplink port bandwidth.
> 
> Cisco UCS uses pin groups to manage which NICs, vNICs, HBAs, and vHBAs are pinned to an uplink port. To configure pinning for a server, you can either assign a pin group directly, or include a pin group in a vNIC policy, and then add that vNIC policy to the service profile assigned to that server. All traffic from the vNIC or vHBA on the server travels through the I/O module to the same uplink port.

To check which HBA goes to which fabric we can run the following:

	
	
	p2-ucsm-A# scope service-profile server 1/2  
	p2-ucsm-A /org/service-profile # show vhba
	
	vHBA:  
	Name Fabric ID Dynamic WWPN  
	---------- --------- ------------  
	fc0 A 20:00:00:25:B5:02:0A:02  
	fc1 B 20:00:00:25:B5:02:0B:02  
	

Each Fabric usually has a vSAN defined for it. To see the definition of each fabric we can check out the settings for each vHBA:

	  
	p2-ucsm-A# scope service-profile server 1/2  
	p2-ucsm-A /org/service-profile # scope vhba fc0  
	p2-ucsm-A /org/service-profile/vhba # show fc-if
	
	Fibre Channel Interface:  
	Name: P2-VSAN-A  
	vSAN ID: 205  
	Operational VSAN: fabric/san/A/net-P2-VSAN-A  
	

To check the NIC pinning we can run the following:  
	  
	p2-ucsm-A# scope service-profile server 1/2  
	p2-ucsm-A /org/service-profile # show vnic
	
	vNIC:  
	Name Fabric ID Dynamic MAC Addr  
	---------- --------- ----------------  
	eth0 A 00:25:B5:02:01:01  
	eth1 A 00:25:B5:02:02:01  
	eth2 A 00:25:B5:02:03:01  
	eth3 A 00:25:B5:02:04:01  
	eth6 A 00:25:B5:02:07:01  
	eth7 A 00:25:B5:02:08:01  
	

For each of the interfaces you can define a set of allowed VLANs, to see what they are you can run the following:

	  
	p2-ucsm-A /org/service-profile # scope vnic eth0  
	p2-ucsm-A /org/service-profile/vnic # show eth-if
	
	Ethernet Interface:  
	Name: Management  
	Dynamic MAC Addr: 00:25:B5:02:01:01  
	Default Network: No  
	VLAN ID: 200  
	Operational VLAN: fabric/lan/net-Management
	
	Name: ServiceConsole  
	Dynamic MAC Addr: 00:25:B5:02:01:01  
	Default Network: Yes  
	VLAN ID: 201  
	Operational VLAN: fabric/lan/net-ServiceConsole
	
	Name: Storage1  
	Dynamic MAC Addr: 00:25:B5:02:01:01  
	Default Network: No  
	VLAN ID: 203  
	Operational VLAN: fabric/lan/net-Storage1
	
	Name: storage2  
	Dynamic MAC Addr: 00:25:B5:02:01:01  
	Default Network: No  
	VLAN ID: 204  
	Operational VLAN: fabric/lan/net-storage2
	
	Name: vlan260  
	Dynamic MAC Addr: 00:25:B5:02:01:01  
	Default Network: No  
	VLAN ID: 260  
	Operational VLAN: fabric/lan/net-vlan260
	
	Name: vmotion  
	Dynamic MAC Addr: 00:25:B5:02:01:01  
	Default Network: No  
	VLAN ID: 202  
	Operational VLAN: fabric/lan/net-vmotion  
	

That is a list of allowed VLANs for that Nic.

To see how the physical ports correspond to the virtual ports on the Fabric Interconnect we can run the following:

	  
	p2-ucsm-A# scope service-profile server 1/2  
	p2-ucsm-A /org/service-profile # show circuit  
	Service Profile: p2-b200-2  
	Server: 1/2  
	Fabric ID: A  
	VIF vNIC Link State Overall Status Prot State Prot Role Admin Pin Oper Pin Transport  
	---- ------ ----------- -------------- ------------- ----------- ---------- ---------- ---------  
	43 Error Error 0/0 0/0 Unknown  
	711 eth0 Up Active No Protection Unprotected 0/0 0/11 Ether  
	712 eth1 Up Active No Protection Unprotected 0/0 0/11 Ether  
	713 eth2 Up Active No Protection Unprotected 0/0 0/11 Ether  
	714 eth3 Up Active No Protection Unprotected 0/0 0/11 Ether  
	717 eth6 Up Active No Protection Unprotected 0/0 0/11 Ether  
	718 eth7 Up Active No Protection Unprotected 0/0 0/11 Ether  
	720 fc0 Up Active No Protection Unprotected 0/0 2/1 Fc  
	8912 Up Active No Protection Unprotected 0/0 0/0 Ether  
	Fabric ID: B  
	VIF vNIC Link State Overall Status Prot State Prot Role Admin Pin Oper Pin Transport  
	---- ------ ----------- -------------- ------------- ----------- ---------- ---------- ---------  
	44 Error Error 0/0 0/0 Unknown  
	719 fc1 Up Active No Protection Unprotected 0/0 0/0 Fc  
	8911 Up Active No Protection Unprotected 0/0 0/0 Ether  
	

So let's connect to FI (Fabric Interconnect) A and see if we can confirm the virtual port of fc0 (remember the WWPN of that vHBA is the following 20:00:00:25:B5:02:0A:02). There are two ways to go about it. First we can find the interface our self and make sure it corresponds with 720:

	  
	p2-ucsm-A# connect nxos a  
	Cisco Nexus Operating System (NX-OS) Software  
	TAC support: http://www.cisco.com/tac  
	Copyright (c) 2002-2012, Cisco Systems, Inc. All rights reserved.  
	The copyrights to certain works contained in this software are  
	owned by other third parties and used and distributed under  
	license. Certain components of this software are licensed under  
	the GNU General Public License (GPL) version 2.0 or the GNU  
	Lesser General Public License (LGPL) Version 2.1. A copy of each  
	such license is available at  
	http://www.opensource.org/licenses/gpl-2.0.php and
	
	http://www.opensource.org/licenses/lgpl-2.1.php
	
	p2-ucsm-A(nxos)# show npv flogi-table | inc 20:00:00:25:b5:02:0a:02  
	vfc720 205 0xd40005 20:00:00:25:b5:02:0a:02 20:00:00:25:b5:02:00:02 fc2/1  
	

That actually looks good, we see that it corresponds to vfc720 and it's on vSAN 205. We can go further and make sure the config matches our server and the interface is up:

	  
	p2-ucsm-A(nxos)# show run int vfc720
	
	!Command: show running-config interface vfc720  
	!Time: Tue Aug 14 03:54:59 2012
	
	version 5.0(3)N2(2.1w)
	
	interface vfc720  
	bind interface Vethernet8912  
	switchport trunk allowed vsan 205  
	switchport description server 1/2, VHBA fc0  
	no shutdown
	
	p2-ucsm-A(nxos)# show int vfc720  
	vfc720 is trunking  
	Bound interface is Vethernet8912  
	Port description is server 1/2, VHBA fc0  
	Hardware is Virtual Fibre Channel  
	Port WWN is 22:cf:00:05:73:f3:17:ff  
	Admin port mode is F, trunk mode is on  
	snmp link state traps are enabled  
	Port mode is TF  
	Port vsan is 205  
	Trunk vsans (admin allowed and active) (205)  
	Trunk vsans (up) (205)  
	Trunk vsans (isolated) ()  
	Trunk vsans (initializing) ()  
	1 minute input rate 0 bits/sec, 0 bytes/sec, 0 frames/sec  
	1 minute output rate 0 bits/sec, 0 bytes/sec, 0 frames/sec  
	7905603 frames input, 14934600272 bytes  
	2 discards, 0 errors  
	8466443 frames output, 15137370704 bytes  
	0 discards, 0 errors  
	last clearing of "show interface" counters never  
	Interface last changed at Fri Aug 10 19:25:38 2012  
	

That all looks good and we can see that it's actually bound to Vethernet8912, so let's check out that interface to make sure it's good:

	  
	p2-ucsm-A(nxos)# show run int Vethernet8912
	
	!Command: show running-config interface Vethernet8912  
	!Time: Tue Aug 14 03:56:21 2012
	
	version 5.0(3)N2(2.1w)
	
	interface Vethernet8912  
	description server 1/2, VHBA fc0  
	pinning server  
	no cdp enable  
	switchport access vlan 2051  
	bind interface Ethernet1/1/2 channel 720  
	service-policy type queuing input default-in-policy  
	no shutdown
	
	p2-ucsm-A(nxos)# show int Vethernet8912  
	Vethernet8912 is up  
	Bound Interface is Ethernet1/1/2  
	Hardware: Virtual, address: 0005.73f3.17c0 (bia 0005.73f3.17c0)  
	Description: server 1/2, VHBA fc0  
	Encapsulation ARPA  
	Port mode is access  
	EtherType is 0x8100  
	Rx  
	7905601 unicast packets 2 multicast packets 0 broadcast packets  
	7905603 input packets 14934600272 bytes  
	0 input packet drops  
	Tx  
	8466443 unicast packets 0 multicast packets 0 broadcast packets  
	8466443 output packets 15137370704 bytes  
	0 flood packets  
	0 output packet drops  
	

We can see that the description matches our port "server 1/2, VHBA fc0" which is what we were trying to track down.

We can do a similar thing for eth0 (vNic1) as well.  
	  
	p2-ucsm-A /chassis/server/adapter # connect nxos a  
	Cisco Nexus Operating System (NX-OS) Software  
	TAC support: http://www.cisco.com/tac  
	Copyright (c) 2002-2012, Cisco Systems, Inc. All rights reserved.  
	The copyrights to certain works contained in this software are  
	owned by other third parties and used and distributed under  
	license. Certain components of this software are licensed under  
	the GNU General Public License (GPL) version 2.0 or the GNU  
	Lesser General Public License (LGPL) Version 2.1. A copy of each  
	such license is available at  
	http://www.opensource.org/licenses/gpl-2.0.php and
	
	http://www.opensource.org/licenses/lgpl-2.1.php
	
	p2-ucsm-A(nxos)# show mac address-table | inc 0025.b502.0101  
	* 201 0025.b502.0101 static 0 F F Veth711  
	p2-ucsm-A(nxos)# show run int Veth711
	
	!Command: show running-config interface Vethernet711  
	!Time: Tue Aug 14 04:25:42 2012
	
	version 5.0(3)N2(2.1w)
	
	interface Vethernet711  
	description server 1/2, VNIC eth0  
	switchport mode trunk  
	no pinning server sticky  
	pinning server pinning-failure link-down  
	switchport trunk native vlan 201  
	switchport trunk allowed vlan 200-204,260  
	bind interface Ethernet1/1/2 channel 711  
	service-policy type queuing input default-in-policy  
	no shutdown
	
	p2-ucsm-A(nxos)# show int Veth711  
	Vethernet711 is up  
	Bound Interface is Ethernet1/1/2  
	Hardware: Virtual, address: 0005.73f3.17c0 (bia 0005.73f3.17c0)  
	Description: server 1/2, VNIC eth0  
	Encapsulation ARPA  
	Port mode is trunk  
	EtherType is 0x8100  
	Rx  
	2344115 unicast packets 6 multicast packets 177584 broadcast packets  
	2521705 input packets 238901890 bytes  
	0 input packet drops  
	Tx  
	1758473 unicast packets 4688714 multicast packets 243995 broadcast packets  
	6691182 output packets 580388547 bytes  
	0 flood packets  
	0 output packet drops  
	

The description fits and the appropriate VLANs are allowed.

We can also check out the local disk policy:

	  
	p2-ucsm-A /chassis/server # scope raid-controller 1 sas  
	p2-ucsm-A /chassis/server/raid-controller # show local-disk
	
	Local Disk:  
	ID: 1  
	Block Size: 512  
	Blocks: 143638992  
	Size (MB): 70136  
	Operability: N/A  
	Presence: Equipped
	
	ID: 2  
	Block Size: 512  
	Blocks: 143638992  
	Size (MB): 70136  
	Operability: N/A  
	Presence: Equipped  
	

You can also check the boot order defined for the host:

	  
	p2-ucsm-A /chassis/server # show boot-order
	
	Boot Definition:  
	Full Name: sys/chassis-1/blade-2/boot-policy  
	Reboot on Update: Yes
	
	Boot LAN:  
	Order: 3
	
	LAN Image Path:  
	Type: Primary  
	VNIC: eth0
	
	Boot Storage:  
	Order: 2
	
	SAN Image:  
	Type: Primary  
	VHBA: fc0
	
	SAN Image Path:  
	Type: Primary
	
	Type: Secondary
	
	Type: Secondary  
	VHBA: fc1
	
	SAN Image Path:  
	Type: Primary
	
	Type: Secondary
	
	Boot virtual media:  
	Order: 1  
	Access: Read Only  
	

We can see that the boot order is the following:

1. CD-ROM  
2. Boot From SAN, first fc0 then fc1  
2. PXE Boot from eth0

If you want to see what WWPNs are used for the boot from SAN you can run the following:

	  
	p2-ucsm-A /chassis/server # show boot-order detail
	
	Boot Definition:  
	Full Name: sys/chassis-1/blade-2/boot-policy  
	Reboot on Update: Yes  
	Description:  
	Enforce Vnic Name: No
	
	Boot LAN:  
	Order: 3
	
	LAN Image Path:  
	Type: Primary  
	VNIC: eth0
	
	Boot Storage:  
	Order: 2
	
	SAN Image:  
	Type: Primary  
	VHBA: fc0
	
	SAN Image Path:  
	Type: Primary  
	LUN: 0  
	WWN: 50:0A:09:83:8D:1F:72:B5
	
	Type: Secondary  
	LUN: 0  
	WWN: 50:0A:09:84:8D:1F:72:B5
	
	Type: Secondary  
	VHBA: fc1
	
	SAN Image Path:  
	Type: Primary  
	LUN: 0  
	WWN: 50:0A:09:83:8D:1F:72:B5
	
	Type: Secondary  
	LUN: 0  
	WWN: 50:0A:09:84:8D:1F:72:B5
	
	Boot virtual media:  
	Order: 1  
	Access: Read Only  
	

Now we can see that we will connect to first "50:0A:09:83:8D:1F:72:B5" using fc0 and then to "50:0A:09:84:8D:1F:72:B5". If that doesn't work we will use fc1 to either connect to "50:0A:09:83:8D:1F:72:B5" or "50:0A:09:84:8D:1F:72:B5". To see the available boot-order policies you can run the following:

	  
	p2-ucsm-A# scope org  
	p2-ucsm-A /org # show boot-policy
	
	Boot Policy:  
	Name Purpose Reboot on Update  
	-------------------- ----------- ----------------  
	default Operational No  
	diag Utility No  
	Local_Only Operational Yes  
	NetBoot Operational No  
	P2-SAN-Boot Operational Yes  
	SAN_NET_Boot Operational Yes  
	utility Utility No  
	

Then you can drill further down to see what the policy is made up of:

	  
	p2-ucsm-A /org # scope boot-policy Local_Only  
	p2-ucsm-A /org/boot-policy # show expand
	
	Boot Policy:  
	Name: Local_Only  
	Purpose: Operational  
	Reboot on Update: Yes
	
	Boot Storage:  
	Order: 1
	
	Local Storage:  
	Name: local-storage  
	

If I find any more interesting commands, I will definitely update this post.

More stuff I found, here is how you can check what LUNs an HBA is connecting to:

First list the available adapters on a blade:

	  
	p1-ucsm-A# show server adapter 9/1  
	Server 9/1:  
	Adapter PID Vendor Serial Overall Status  
	------- ---------- ----------------- ------------ --------------  
	1 N20-AC0002 Cisco Systems Inc QCI1515ACEY Operable  
	

Then Connect to the adapter and confirm the model and do the rest

	  
	p1-ucsm-A# connect adapter 9/1/1  
	adapter 9/1/1 # connect  
	adapter 9/1/1 # show-identity  
	description: "Cisco UCS VIC M81KR Adapter"  
	hw_version: "A2"  
	sw_version: "2.0(1w)"  
	adapter 9/1/1 (top):1# attach-fls  
	adapter 9/1/1 (fls):1# vnic  
	---- ---- ---- ------- -------  
	vnic ecpu type state lif  
	---- ---- ---- ------- -------  
	13 1 fc active 10  
	14 2 fc active 11  
	adapter 9/1/1 (fls):2# lunlist 13  
	vnic : 13 lifid: 10  
	- FLOGI State : init (fc_id 0x000000)  
	- PLOGI Sessions  
	- WWNN 50:0a:09:81:8d:df:db:4c WWPN 50:0a:09:81:8d:df:db:4c fc_id 0x000000  
	- LUN's configured (SCSI Type, Version, Vendor, Serial No.)  
	LUN ID : 0x0000000000000000 access failure  
	- REPORT LUNs Query Response  
	LUN ID : 0x0000000000000000  
	- Nameserver Query Response  
	- WWPN : 50:0a:09:81:8d:df:db:4c  
	- WWPN : 50:0a:09:82:9f:3f:52:ad  
	- WWPN : 50:0a:09:82:8f:3f:52:ad  
	

