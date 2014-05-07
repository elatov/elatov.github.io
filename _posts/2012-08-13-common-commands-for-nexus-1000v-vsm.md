---
title: Common Commands for Nexus 1000v VSM
author: Karim Elatov
layout: post
permalink: /2012/08/common-commands-for-nexus-1000v-vsm/
dsq_thread_id:
  - 1406849469
categories:
  - Networking
  - VMware
tags:
  - show tech-support svs
  - Virtual Supervisor Module
  - VSM
---
Most of these command can be seen by executing &#8216;show tech-suppport svs&#8217; on the VSM (Virtual Supervisor Module)

Show local time of the N1K  
	  
	switch# show clock  
	Wed Aug 8 20:42:35 UTC 2012  
	

Show the name of the N1K  
	  
	switch# show switchname  
	switch  
	

Show information and statistics of the management interface of the N1K

	  
	switch# show interface mgmt 0  
	mgmt0 is up  
	Hardware: Ethernet, address: 0050.56b3.252c (bia 0050.56b3.252c)  
	Internet Address is 10.131.6.7/21  
	MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,  
	reliability 255/255, txload 1/255, rxload 1/255  
	Encapsulation ARPA  
	full-duplex, 1000 Mb/s  
	Auto-Negotiation is turned on  
	1 minute input rate 9184 bits/sec, 9 packets/sec  
	1 minute output rate 2648 bits/sec, 1 packets/sec  
	Rx  
	94166 input packets 14974 unicast packets 16289 multicast packets  
	62903 broadcast packets 9458571 bytes  
	Tx  
	58292 output packets 57954 unicast packets 165 multicast packets  
	173 broadcast packets 10523381 bytes  
	

Show Version information of the N1K and the uptime

	  
	switch# show version  
	Cisco Nexus Operating System (NX-OS) Software  
	TAC support: http://www.cisco.com/tac  
	Copyright (c) 2002-2012, Cisco Systems, Inc. All rights reserved.  
	The copyrights to certain works contained herein are owned by  
	other third parties and are used and distributed under license.  
	Some parts of this software are covered under the GNU Public  
	License. A copy of the license is available at
	
	http://www.gnu.org/licenses/gpl.html.
	
	Software  
	loader: version unavailable   
	kickstart: version 4.2(1)SV1(5.1)  
	system: version 4.2(1)SV1(5.1)  
	kickstart image file is: bootflash:/nexus-1000v-kickstart-mz.4.2.1.SV1.5.1.b  
	in  
	kickstart compile time: 1/30/2012 17:00:00 [01/31/2012 01:49:17]  
	system image file is: bootflash:/nexus-1000v-mz.4.2.1.SV1.5.1.bin  
	system compile time: 1/30/2012 17:00:00 [01/31/2012 02:49:49]
	
	Hardware  
	cisco Nexus 1000V Chassis ("Virtual Supervisor Module")  
	Intel(R) Xeon(R) CPU with 2075740 kB of memory.  
	Processor Board ID T5056B3252C
	
	Device name: switch  
	bootflash: 1557496 kB
	
	Kernel uptime is 0 day(s), 2 hour(s), 44 minute(s), 22 second(s)
	
	plugin  
	Core Plugin, Ethernet Plugin, Virtualization Plugin  
	

Show domain information of the N1K (control and packet VLANs)

	  
	switch# show svs domain  
	SVS domain config:  
	Domain id: 34  
	Control vlan: 1  
	Packet vlan: 1  
	L2/L3 Control mode: L2  
	L3 control interface: NA  
	Status: Config push to VC successful.  
	

Show vCenter connection information

	  
	switch# show svs connections 
	
	connection VC:  
	ip address: 10.131.6.11  
	remote port: 80  
	protocol: vmware-vim https  
	certificate: default  
	datacenter name: VDC  
	admin:  
	max-ports: 8192  
	DVS uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	config status: Enabled  
	operational status: Connected  
	sync status: Complete  
	version: VMware vCenter Server 5.0.0 build-455964  
	vc-uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	

Show Module (hosts or VSMs) neighbors

	  
	switch# show svs neighbors 
	
	Active Domain ID: 34
	
	AIPC Interface MAC: 0050-56b3-252b  
	Inband Interface MAC: 0050-56b3-252d
	
	Src MAC Type Domain-id Node-id Last learnt (Sec. ago)  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---
	
	0002-3d40-2202 VEM 34 0302 10066.07  
	0002-3d40-2203 VEM 34 0402 10065.82  
	

Show all interfaces (brief)

	  
	switch# show interface brief 
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Port VRF Status IP Address Speed MT  
	U  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	mgmt0 -- up 10.131.6.7 1000 15  
	00
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Ethernet VLAN Type Mode Status Reason Speed Po  
	rt  
	Interface Ch  
	#  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Eth3/2 1 eth access up none 1000  
	Eth4/2 1 eth access up none 1000 
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Vethernet VLAN Type Mode Status Reason Speed  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Veth1 1 virt access up none auto  
	Veth2 1 virt access up none auto  
	Veth3 -- virt access up none auto  
	Veth4 -- virt access up none auto 
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Port VRF Status IP Address Speed MT  
	U  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	control0 -- up -- 1000 15  
	00  
	

Show all interface information and statistics

	  
	switch# show interface  
	mgmt0 is up  
	Hardware: Ethernet, address: 0050.56b3.252c (bia 0050.56b3.252c)  
	Internet Address is 10.131.6.7/21  
	MTU 1500 bytes, BW 1000000 Kbit, DLY 10 usec,  
	reliability 255/255, txload 1/255, rxload 1/255  
	Encapsulation ARPA  
	full-duplex, 1000 Mb/s  
	Auto-Negotiation is turned on  
	1 minute input rate 6424 bits/sec, 9 packets/sec  
	1 minute output rate 1928 bits/sec, 0 packets/sec  
	Rx  
	98426 input packets 15507 unicast packets 17070 multicast packets  
	65849 broadcast packets 9840349 bytes  
	Tx  
	58723 output packets 58369 unicast packets 173 multicast packets  
	181 broadcast packets 10614603 bytes
	
	Ethernet3/2 is up  
	Hardware: Ethernet, address: 0050.565c.9056 (bia 0050.565c.9056)  
	Port-Profile is sys-uplink-access  
	MTU 1500 bytes  
	Encapsulation ARPA  
	Port mode is access  
	full-duplex, 1000 Mb/s  
	5 minute input rate 40328 bits/second, 42 packets/second  
	5 minute output rate 3472 bits/second, 1 packets/second  
	Rx  
	3151995 Input Packets 1534396 Unicast Packets  
	1821987 Multicast Packets 4318543 Broadcast Packets  
	452038538 Bytes  
	Tx  
	245815 Output Packets 75155 Unicast Packets  
	0 Multicast Packets 169660 Broadcast Packets 74201 Flood Packets  
	44531923 Bytes  
	4 Input Packet Drops 0 Output Packet Drops
	
	Ethernet4/2 is up  
	Hardware: Ethernet, address: 0050.565c.9026 (bia 0050.565c.9026)  
	Port-Profile is sys-uplink-access  
	MTU 1500 bytes  
	Encapsulation ARPA  
	Port mode is access  
	full-duplex, 1000 Mb/s  
	5 minute input rate 41528 bits/second, 43 packets/second  
	5 minute output rate 2112 bits/second, 0 packets/second  
	Rx  
	3227490 Input Packets 1454181 Unicast Packets  
	1581164 Multicast Packets 3977494 Broadcast Packets  
	465458486 Bytes  
	Tx  
	153129 Output Packets 74711 Unicast Packets  
	0 Multicast Packets 32 Broadcast Packets 1219 Flood Packets  
	39355184 Bytes  
	2 Input Packet Drops 0 Output Packet Drops
	
	Vethernet1 is up  
	Port description is vCloud\_Director\_RHEL5.6, Network Adapter 2  
	Hardware: Virtual, address: 0050.56b3.06d1 (bia 0050.56b3.06d1)  
	Owner is VM "vCloud\_Director\_RHEL5.6", adapter is Network Adapter 2  
	Active on module 3  
	VMware DVS port 101  
	Port-Profile is Con_Pack  
	Port mode is access  
	5 minute input rate 0 bits/second, 0 packets/second  
	5 minute output rate 32776 bits/second, 32 packets/second  
	Rx  
	5 Input Packets 25 Unicast Packets  
	0 Multicast Packets 16 Broadcast Packets  
	300 Bytes  
	Tx  
	3450234 Output Packets 301373 Unicast Packets  
	49686 Multicast Packets 4484787 Broadcast Packets 2399244 Flood Packets  
	1153582487 Bytes  
	0 Input Packet Drops 0 Output Packet Drops
	
	Vethernet2 is up  
	Port description is Nexus1000V-4.2.1.SV1.5.1, Network Adapter 1  
	Hardware: Virtual, address: 0050.56b3.252b (bia 0050.56b3.252b)  
	Owner is VM "Nexus1000V-4.2.1.SV1.5.1", adapter is Network Adapter 1  
	Active on module 3  
	VMware DVS port 100  
	Port-Profile is Con_Pack  
	Port mode is access  
	5 minute input rate 4240 bits/second, 2 packets/second  
	5 minute output rate 34400 bits/second, 33 packets/second  
	Rx  
	217323 Input Packets 447187 Unicast Packets  
	238 Multicast Packets 275158 Broadcast Packets  
	39434742 Bytes  
	Tx  
	3781434 Output Packets 448316 Unicast Packets  
	70652 Multicast Packets 6760722 Broadcast Packets 2327452 Flood Packets  
	1230453905 Bytes  
	238 Input Packet Drops 0 Output Packet Drops  
	

Show the running configuration of the N1K

	  
	switch# show running-config 
	
	!Command: show running-config  
	!Time: Wed Aug 8 20:53:10 2012
	
	version 4.2(1)SV1(5.1)  
	no feature telnet  
	feature segmentation  
	feature network-segmentation-manager
	
	username admin password 5 $1$o.Nq/qPt$oaW.ZuXxW/EIXeuK2igXr1 role network-adm  
	in
	
	banner motd #Nexus 1000v Switch#
	
	ssh key rsa 2048  
	ip domain-lookup  
	vem 3  
	host vmware id 80c34566-7e89-b601-b4f9-001a64dc9054  
	vem 4  
	host vmware id c0c2ea8e-7b89-b601-dcdb-001a64dc9024  
	...  
	...  
	

Show Modules (VEM or VSM)

	  
	switch# show module  
	Mod Ports Module-Type Model Status  
	\--- \---\-- -\---\---\---\---\---\---\---\---\---\---\- --\---\---\---\---\---\- --\---\---\----  
	1 0 Virtual Supervisor Module Nexus1000V active *  
	3 248 Virtual Ethernet Module NA ok  
	4 248 Virtual Ethernet Module NA ok
	
	Mod Sw Hw  
	\--- \---\---\---\---\---\--- \---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	1 4.2(1)SV1(5.1) 0.0  
	3 4.2(1)SV1(5.1) VMware ESXi 5.0.0 Releasebuild-469512 (3.0)  
	4 4.2(1)SV1(5.1) VMware ESXi 5.0.0 Releasebuild-469512 (3.0) 
	
	Mod MAC-Address(es) Serial-Num  
	\--- \---\---\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---  
	1 00-19-07-6c-5a-a8 to 00-19-07-6c-62-a8 NA  
	3 02-00-0c-00-03-00 to 02-00-0c-00-03-80 NA  
	4 02-00-0c-00-04-00 to 02-00-0c-00-04-80 NA
	
	Mod Server-IP Server-UUID Server-Name  
	\--- \---\---\---\---\--- \---\---\---\---\---\---\---\---\---\---\---\--- \---\---\---\---\---\---  
	--  
	1 10.131.6.7 NA NA  
	3 10.131.1.98 80c34566-7e89-b601-b4f9-001a64dc9054 10.131.1.98  
	4 10.131.1.97 c0c2ea8e-7b89-b601-dcdb-001a64dc9024 10.131.1.97
	
	* this terminal session  
	

Show modules uptime

	  
	switch# show module uptime  
	\---\--- Module 1 \-----  
	Module Start Tme: Wed Aug 8 18:01:24 2012  
	Up Time: 0 day(s), 2 hour(s), 53 minute(s), 35 second(s)  
	\---\--- Module 3 \-----  
	Module Start Tme: Wed Aug 8 18:01:55 2012  
	Up Time: 0 day(s), 2 hour(s), 53 minute(s), 4 second(s)  
	\---\--- Module 4 \-----  
	Module Start Tme: Wed Aug 8 18:01:56 2012  
	Up Time: 0 day(s), 2 hour(s), 53 minute(s), 3 second(s)  
	

Show VEM connection counters  
	  
	switch# show module vem counters  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	Mod InNR OutMI InMI OutHBeats InHBeats InsCnt RemCnt Crit Tx Errs  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	3 1 1 1 10417 10416 1 0 0  
	4 1 1 1 10417 10414 1 0 0  
	

Show module to vem mapping (even the disconnected VEMs)

	  
	switch# show module vem mapping  
	Mod Status UUID License Status  
	\--- \---\---\---\-- -\---\---\---\---\---\---\---\---\---\---\---\-- -\---\---\---\----  
	3 powered-up 80c34566-7e89-b601-b4f9-001a64dc9054 licensed  
	4 absent c0c2ea8e-7b89-b601-dcdb-001a64dc9024 licensed  
	

Show VEM license information

	  
	switch# show module vem license-info  
	Licenses are Sticky  
	Mod Socket Count License Usage Count License Version License Status  
	\--- \---\---\---\--- \---\---\---\---\---\---\- --\---\---\---\---\- --\---\---\---\---  
	3 2 2 1.0 licensed  
	4 2 2 1.0 licensed  
	

Show license usage

	  
	switch# show license usage  
	Feature Ins Lic Status Expiry Date Comments  
	Count  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	NEXUS\_VSG\_SERVICES_PKG No 16 Unused 02 Oct 2012 -  
	NEXUS1000V\_LAN\_SERVICES_PKG No 16 In use 02 Oct 2012 -  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	--  
	

Show detailed license information  
	  
	switch# show license usage NEXUS1000V\_LAN\_SERVICES_PKG  
	\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Feature Usage Info  
	\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Installed Licenses : 0  
	Default Eval Licenses : 16  
	Max Overdraft Licenses : 0  
	Installed Licenses in Use : 0  
	Overdraft Licenses in Use : 0  
	Default Eval Lic in Use : 4  
	Default Eval days left : 55  
	Licenses Available : 12  
	Shortest Expiry : 02 Oct 2012  
	\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Application  
	\---\---\---\---\---\---\---\---\---\---\---\---\----  
	VEM 3 - Socket 1  
	VEM 3 - Socket 2  
	VEM 4 - Socket 1  
	VEM 4 - Socket 2  
	\---\---\---\---\---\---\---\---\---\---\---\---\----  
	

Show all of your port-profiles

	  
	switch# show port-profile 
	
	port-profile Con_Pack  
	type: Vethernet  
	description:  
	status: enabled  
	max-ports: 32  
	min-ports: 1  
	inherit:  
	config attributes:  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	evaluated config attributes:  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	assigned interfaces:  
	Vethernet1  
	Vethernet2  
	port-group: Con_Pack  
	system vlans: 1  
	capability l3control: no  
	capability iscsi-multipath: no  
	capability vxlan: no  
	capability l3-vn-service: no  
	port-profile role: none  
	port-binding: static
	
	port-profile Unused\_Or\_Quarantine_Uplink  
	type: Ethernet  
	description: Port-group created for Nexus1000V internal usage. Do not use.  
	status: enabled  
	max-ports: 32  
	min-ports: 1  
	inherit:  
	config attributes:  
	shutdown  
	evaluated config attributes:  
	assigned interfaces:  
	port-group: Unused\_Or\_Quarantine_Uplink  
	system vlans: none  
	capability l3control: no  
	capability iscsi-multipath: no  
	capability vxlan: no  
	capability l3-vn-service: no  
	port-profile role: none  
	port-binding: static
	
	port-profile Unused\_Or\_Quarantine_Veth  
	type: Vethernet  
	description: Port-group created for Nexus1000V internal usage. Do not use.  
	status: enabled  
	max-ports: 32  
	min-ports: 1  
	inherit:  
	config attributes:  
	shutdown  
	evaluated config attributes:  
	assigned interfaces:  
	port-group: Unused\_Or\_Quarantine_Veth  
	system vlans: none  
	capability l3control: no  
	capability iscsi-multipath: no  
	capability vxlan: no  
	capability l3-vn-service: no  
	port-profile role: none  
	port-binding: static
	
	port-profile sys-uplink-access  
	type: Ethernet  
	description:  
	status: enabled  
	max-ports: 32  
	min-ports: 1  
	inherit:  
	config attributes:  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	evaluated config attributes:  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	assigned interfaces:  
	Ethernet3/2  
	Ethernet4/2  
	port-group: sys-uplink-access  
	system vlans: 1  
	capability l3control: no  
	capability iscsi-multipath: no  
	capability vxlan: no  
	capability l3-vn-service: no  
	port-profile role: none  
	port-binding: static  
	

Show port-profile information in a concise view

	  
	switch# show port-profile brief  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\-----  
	Port Profile Profile Conf Eval Assigned Child  
	Profile Type State Items Items Intfs Profs  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\-----  
	Con_Pack Vethernet 1 3 3 2 0  
	Unused\_Or\_Quarantine_Uplink Ethernet 1 1 0 0 0  
	Unused\_Or\_Quarantine_Veth Vethernet 1 1 0 0 0  
	sys-uplink-access Ethernet 1 3 3 2 0  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\-----  
	Profile Assigned Total Sys Parent Child UsedBy  
	Type Intfs Prfls Prfls Prfls Prfls Prfls  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\-----  
	Vethernet 4 8 1 7 2 2  
	Ethernet 2 3 1 3 0 1  
	

Show port-profile usage

	  
	switch# show port-profile usage 
	
	port-profile Con_Pack  
	Vethernet1  
	Vethernet2
	
	port-profile Unused\_Or\_Quarantine_Uplink
	
	port-profile Unused\_Or\_Quarantine_Veth
	
	port-profile sys-uplink-access  
	Ethernet3/2  
	Ethernet4/2  
	

Show port-profile usage with VMs name

	  
	switch# show port-profile virtual usage
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Port Profile Port Adapter Owner  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Con\_Pack Veth1 Net Adapter 2 vCloud\_Director_RHEL5.6  
	Veth2 Net Adapter 1 Nexus1000V-4.2.1.SV1.5.1  
	sys-uplink-access Eth3/2 vmnic1 10.131.1.98  
	Eth4/2 vmnic1 10.131.1.97  
	

Show port-profile usage and show mode of each interface that is part of the port-profile

	  
	switch# show port-profile expand-interface
	
	port-profile Con_Pack  
	Vethernet1  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	Vethernet2  
	switchport mode access  
	switchport access vlan 1  
	no shutdown
	
	port-profile Unused\_Or\_Quarantine_Uplink
	
	port-profile Unused\_Or\_Quarantine_Veth
	
	port-profile sys-uplink-access  
	Ethernet3/2  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	Ethernet4/2  
	switchport mode access  
	switchport access vlan 1  
	no shutdown  
	

Show internal informaion for the port-profiles (like what DVPortGroup they correspond to)

	  
	switch# show msp internal info  
	port-profile Con_Pack  
	id: 5  
	capability: 0x2  
	state: 0x1  
	type: 0x1  
	system vlan mode: access  
	system vlans: 1  
	port-binding: static  
	bind_opts: 0  
	max ports: 32  
	min ports: 1  
	used ports: 2  
	vmware config information  
	pg name: Con_Pack  
	dvs: (ignore)  
	reserved ports: 32  
	port-profile role:  
	alias information:  
	pg id: Con_Pack  
	dvs uuid:  
	type: 1  
	pg id: dvportgroup-83  
	dvs uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	type: 2  
	port-profile sys-uplink-access  
	id: 11  
	capability: 0x3  
	state: 0x1  
	type: 0x1  
	system vlan mode: access  
	system vlans: 1  
	port-binding: static  
	bind_opts: 0  
	max ports: 32  
	min ports: 1  
	used ports: 0  
	vmware config information  
	pg name: sys-uplink-access  
	dvs: (ignore)  
	reserved ports: 32  
	port-profile role:  
	alias information:  
	pg id: sys-uplink-access  
	dvs uuid:  
	type: 1  
	pg id: dvportgroup-88  
	dvs uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	type: 2  
	

Check Mac Address Table of the N1K. If you are using bridge domains, you will see a sub section for that.

	  
	switch# show mac address-table  
	VLAN MAC Address Type Age Port Mod  
	\---\---\---+\---\---\---\---\-----+\---\----+\---\---\---+\---\---\---\---\---\---\---\---\---\---+\---  
	1 0002.3d10.2202 static 0 N1KV Internal Port 3  
	1 0002.3d20.2202 static 0 N1KV Internal Port 3  
	1 0002.3d30.2202 static 0 N1KV Internal Port 3  
	1 0002.3d40.2202 static 0 N1KV Internal Port 3  
	1 0002.3d60.2200 static 0 N1KV Internal Port 3  
	1 0002.3d60.2202 static 0 N1KV Internal Port 3  
	1 0002.3d80.2202 static 0 N1KV Internal Port 3  
	1 0050.56b3.06d1 static 0 Veth1 3  
	1 0050.56b3.252b static 0 Veth2 3  
	1 0000.5e00.0112 dynamic 1 Eth3/2 3  
	1 0002.3d20.2203 dynamic 38 Eth3/2 3  
	1 0002.3d40.2203 dynamic 1 Eth3/2 3  
	1 000c.2909.a7fc dynamic 1 Eth3/2 3  
	1 000c.2921.9e12 dynamic 11 Eth3/2 3  
	1 000c.2934.26d8 dynamic 12 Eth3/2 3  
	1 000c.2940.ea36 dynamic 6 Eth3/2 3  
	1 000c.2957.a9bb dynamic 76 Eth3/2 3  
	1 000c.2985.c376 dynamic 98 Eth3/2 3  
	1 000c.29ae.b9db dynamic 92 Eth3/2 3  
	1 000c.29b3.0375 dynamic 60 Eth3/2 3  
	1 000c.29b5.710b dynamic 2 Eth3/2 3  
	1 000c.29d7.8e4a dynamic 114 Eth3/2 3  
	1 000c.29e4.bccf dynamic 3 Eth3/2 3  
	1 000c.29e9.f20c dynamic 1 Eth3/2 3  
	1 0013.f501.0021 dynamic 164 Eth4/2 4  
	1 0013.f501.0081 dynamic 329 Eth4/2 4  
	1 0013.f501.00f1 dynamic 310 Eth4/2 4  
	1 0013.f501.0101 dynamic 14 Eth4/2 4 
	
	...  
	...  
	Bridge-domain: dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8  
	MAC Address Type Age Port IP Address Mod  
	\---\---\---\---\---\---\---\-----+\---\----+\---\---\---+\---\---\---\---\---+\---\---\---\---\---+\---  
	0050.5601.0008 static 0 Veth4 0.0.0.0 4  
	0050.5601.0009 static 0 Veth3 0.0.0.0 4  
	Total MAC Addresses: 107  
	

Show high availability status

	  
	switch# show system redundancy status  
	Redundancy role  
	\---\---\---\---\---  
	administrative: standalone  
	operational: standalone
	
	Redundancy mode  
	\---\---\---\---\---  
	administrative: HA  
	operational: None
	
	This supervisor (sup-1)  
	\---\---\---\---\---\---\-----  
	Redundancy state: Active  
	Supervisor state: Active  
	Internal state: Active with no standby 
	
	Other supervisor (sup-2)  
	\---\---\---\---\---\---\---\---  
	Redundancy state: Not present  
	

Show Virtual Interfaces

	  
	switch# show int virtual 
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Port Adapter Owner Mod Host  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Veth1 Net Adapter 2 vCloud\_Director\_RHEL5.6 3 10.131.1.98  
	Veth2 Net Adapter 1 Nexus1000V-4.2.1.SV1.5.1 3 10.131.1.98  
	Veth3 Net Adapter 1 tets (37370594-b4c9-433e 4 10.131.1.97  
	Veth4 Net Adapter 1 OI (3adadd61-75c1-4af2-9 4 10.131.1.97  
	

Show Virtual Ports and their corresponding DVPorts

	  
	switch# show int virtual port-mapping 
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Port Hypervisor Port Binding Type Status Reason  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Veth1 DVPort101 static up none  
	Veth2 DVPort100 static up none  
	Veth3 DVPort206 static up none  
	Veth4 DVPort207 static up none  
	

Show description of virtual ports

	  
	switch# show interface virtual description
	
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Interface Description  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----  
	Veth1 vCloud\_Director\_RHEL5.6, Network Adapter 2  
	Veth2 Nexus1000V-4.2.1.SV1.5.1, Network Adapter 1  
	Veth3 tets (37370594-b4c9-433e-b070-c3265cdefd2f), Network Adapter 1  
	Veth4 OI (3adadd61-75c1-4af2-9d76-ff467e42e965), Network Adapter 1  
	

Show VLAN information

	  
	switch# show vlan
	
	VLAN Name Status Ports  
	\---\- --\---\---\---\---\---\---\---\---\---\--- \---\---\--- \---\---\---\---\---\---\---\---\---\----  
	1 default active Veth1, Veth2, Eth3/2, Eth4/2
	
	VLAN Type  
	\---\- --\---  
	1 enet 
	
	Remote SPAN VLANs  
	\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\----
	
	Primary Secondary Type Ports  
	\---\---\- --\---\---\- --\---\---\---\---\- --\---\---\---\---\---\---\---\---\---\---\---\---\-----
	
	

Show Network Segmentation Manager (NSM) (usually used with vCloud Director) internal information

	  
	switch# show system internal nsmgr info
	
	network dvs.VCDVSorg\_net\_using\_n1k\_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565  
	template name: vcd-ni-pol  
	max ports: 0  
	vlan id: 0  
	segment id: 5001  
	multicast ip: 224.0.4.2  
	port_binding: "static auto expand"  
	tenant uuid: e461e9cc-1205-40f4-9f36-ad0e841d9c73  
	mgmt srv uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	dvs uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	pool type: isolation  
	template type: 1
	
	network dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8  
	template name: vcd-ni-pol  
	max ports: 0  
	vlan id: 0  
	segment id: 5003  
	multicast ip: 224.0.4.4  
	port_binding: "static auto expand"  
	tenant uuid: e461e9cc-1205-40f4-9f36-ad0e841d9c73  
	mgmt srv uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	dvs uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	pool type: isolation  
	template type: 1  
	

Show NSM Status

	  
	switch# show network-segment manager switch  
	switch: default_switch  
	state: enabled  
	dvs-uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4  
	dvs-name: switch  
	mgmt-srv-uuid: 40C987D3-60EC-47A3-8E53-1708035AE618  
	reg status: registered  
	last alert: 16 seconds ago  
	connection status: connected  
	

Show Network Segment policy Usage

	  
	switch# show network-segment policy usage
	
	network-segment policy default\_segmentation\_template
	
	network-segment policy default\_vlan\_template
	
	network-segment policy vcd-ni-pol  
	dvs.VCDVSorg\_net\_using\_n1k\_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565  
	dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8  
	

Show network segments

	  
	switch# show network-segment network
	
	network dvs.VCDVSorg\_net\_using\_n1k\_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565  
	tenant id: e461e9cc-1205-40f4-9f36-ad0e841d9c73  
	network-segment policy: vcd-ni-pol  
	segment id: 5001  
	multicast ip: 224.0.4.2
	
	network dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8  
	tenant id: e461e9cc-1205-40f4-9f36-ad0e841d9c73  
	network-segment policy: vcd-ni-pol  
	segment id: 5003  
	multicast ip: 224.0.4.4  
	

Show CDP (Cisco Discover Protocol) neighbors

	  
	switch# show cdp neighbors  
	Capability Codes: R - Router, T - Trans-Bridge, B - Source-Route-Bridge  
	S - Switch, H - Host, I - IGMP, r - Repeater,  
	V - VoIP-Phone, D - Remotely-Managed-Device,  
	s - Supports-STP-Dispute
	
	Device-ID Local Intrfce Hldtme Capability Platform Port ID
	
	lab.test.com.commgmt0 140 S I WS-C2960G-48T Gig0/2  
	

Show different bridge domains when using network segments

	  
	switch# show bridge-domain 
	
	Bridge-domain dvs.VCDVSorg\_net\_using\_n1k\_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38  
	b429f3565 (0 ports in all)  
	Segment ID: 5001 (Manual/Active)  
	Group IP: 224.0.4.2  
	State: UP Mac learning: Enabled
	
	Bridge-domain dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8  
	(2 ports in all)  
	Segment ID: 5003 (Manual/Active)  
	Group IP: 224.0.4.4  
	State: UP Mac learning: Enabled  
	Veth3, Veth4  
	

<p class="wp-flattr-button">
	  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/common-commands-for-nexus-1000v-vsm/" title=" Common Commands for Nexus 1000v VSM" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:show tech-support svs,Virtual Supervisor Module,VSM,blog;button:compact;">Most of these command can be seen by executing &#8216;show tech-suppport svs&#8217; on the VSM (Virtual Supervisor Module) Show local time of the N1K  switch# show clock Wed Aug...</a>
	</p>