---
title: "Common 'vemcmd' Commands from a VEM Module on an ESX(i) Host"
author: Karim Elatov
layout: post
permalink: /2012/08/common-vemcmd-commands-from-a-vem-module-on-an-esxi-host/
dsq_thread_id:
  - 1404673320
categories: ['networking', 'vmware']
tags: ['nexus1000v', 'vem', 'vemcmd', 'virtual_ethernet_module']
---

Most of these can be seen from running a 'vem-support all' on a host, but I wanted to have a good reference point for my self.


	~ # vemcmd show card
	Card UUID type 2: c0c2ea8e-7b89-b601-dcdb-001a64dc9024
	Card name: wdc-tse-i97
	Switch name: switch
	Switch alias: DvsPortset-0
	Switch uuid: 21 ba 33 50 89 1a e8 ca-42 07 57 77 59 92 97 f4
	Card domain: 34
	Card slot: 4
	VEM Tunnel Mode: L2 Mode
	VEM Control (AIPC) MAC: 00:02:3d:10:22:03
	VEM Packet (Inband) MAC: 00:02:3d:20:22:03
	VEM Control Agent (DPA) MAC: 00:02:3d:40:22:03
	VEM SPAN MAC: 00:02:3d:30:22:03
	Primary VSM MAC : 00:50:56:b3:25:2b
	Primary VSM PKT MAC : 00:50:56:b3:25:2d
	Primary VSM MGMT MAC : 00:50:56:b3:25:2c
	Standby VSM CTRL MAC : ff:ff:ff:ff:ff:ff
	Management IPv4 address: 10.131.1.97
	Management IPv6 address: 0000:0000:0000:0000:0000:0000:0000:0000
	Secondary VSM MAC : 00:00:00:00:00:00
	Secondary L3 Control IPv4 address: 0.0.0.0
	Upgrade : Default
	Max physical ports: 32
	Max virtual ports: 216
	Card control VLAN: 1
	Card packet VLAN: 1
	Card Headless Mode : No
	Processors: 8
	Processor Cores: 8
	Processor Sockets: 2
	Kernel Memory: 54524748
	Port link-up delay: 5s
	Global UUFB: DISABLED
	Heartbeat Set: True
	PC LB Algo: source-mac
	Datapath portset event in progress : no
	Licensed: Yes


Show uptime of the VSM


	~ # vemcmd show vsm uptime
	VSM uptime (Hrs:Min:Sec): (1:38:46)


Show virtual ports connected to the VSM/VEM


	~ # vemcmd show port
	LTL VSM Port Admin Link State PC-LTL SGID Vem Port Type
	18 Eth4/2 UP UP FWD 0 vmnic1
	49 Veth3 UP UP FWD 0 test.eth0
	50 Veth4 UP UP FWD 0 OI.eth0


Show vlans used by virtual ports


	~ # vemcmd show port vlans
	Native VLAN Allowed
	LTL VSM Port Mode VLAN State Vlans
	18 Eth4/2 A 1 FWD 1


Show LTL range


	~ # vemcmd show ltl range
	LTL Range Description (null)
	0 - 0 Packet Drop
	1 - 16 Internal Use
	17 - 48 Physical NICs
	49 - 304 Virtual NICs
	305 - 312 Port Channel
	313 - 4408 VLAN broadcast and flooding
	4409 - 9336 Multicast Groups


Show Virtual Ports along with VMware DVPorts and DVPortGroups


	~ # vemcmd show pd-port
	LTL Port DVport Type Link-valid State Duplex Speed PG-Name Status Client-Name
	18 50331675 0 PHYS 1 UP 1 1000 dvportgroup-88 Success vmnic1
	49 50331676 206 VIRT 0 0 0 dvportgroup-101 Success test.eth0
	50 50331677 207 VIRT 0 0 0 dvportgroup-101 Success OI.eth0


Show virtual vs physical ports


	~ # vemcmd show portdevice type
	LTL Device Type Device Name
	18 Physical NIC vmnic1
	49 Virtual NIC test.eth0
	50 Virtual NIC OI.eth0


Show VLAN information and which ports are on which VLANs


	~ # vemcmd show vlan
	Number of valid BDS: 7
	BD 1, vdc 1, vlan 1, 5 ports
	Portlist:
	10
	12
	20 vmnic3
	49 Nexus1000V-4.2.1.SV1.4b.eth0
	50 test.eth0

	BD 10, vdc 1, vlan 10, 1 ports
	Portlist:
	20 vmnic3

	BD 20, vdc 1, vlan 20, 1 ports
	Portlist:
	20 vmnic3

	BD 3968, vdc 1, vlan 3968, 3 ports
	Portlist:
	1 inband
	5 inband port security
	11

	BD 3969, vdc 1, vlan 3969, 2 ports
	Portlist:
	8
	9

	BD 3970, vdc 1, vlan 3970, 0 ports
	Portlist:
	BD 3971, vdc 1, vlan 3971, 2 ports
	Portlist:
	14
	15



Show Trunk information, VLAN information in a more concise view


	~ # vemcmd show trunk
	Trunk port 6 native_vlan 1 CBL 1
	vlan(1) cbl 1, vlan(10) cbl 1, vlan(20) cbl 1, vlan(3968) cbl 1, vlan(3969) cbl 1, vlan(3970) cbl 1, vlan(3971) cbl 1,
	Trunk port 16 native_vlan 1 CBL 1
	vlan(1) cbl 1, vlan(10) cbl 1, vlan(20) cbl 1, vlan(3968) cbl 1, vlan(3969) cbl 1, vlan(3970) cbl 1, vlan(3971) cbl 1,


Show Mac address going through the VEM


	~ # vemcmd show portmac
	LTL Mac Address
	6 00:02:3d:80:22:03
	8 00:02:3d:40:22:03
	9 00:00:00:00:00:00
	10 00:00:00:00:00:00
	11 00:00:00:00:00:00
	12 00:00:00:00:00:00
	13 00:00:00:00:00:00
	14 00:00:00:00:00:00
	15 00:00:00:00:00:00
	16 00:00:00:00:00:00
	18 00:50:56:5c:90:26
	49 00:50:56:01:00:09
	50 00:50:56:01:00:08


Show all Layer 2 Information, if using network segments, the bridge domains will be seen here as well


	~ # vemcmd show l2 all
	Bridge domain 1 brtmax 4096, brtcnt 53, timeout 300
	VLAN 1, swbd 1, ""
	Flags: P - PVLAN S - Secure D - Drop
	Type MAC Address LTL timeout Flags PVLAN
	Dynamic 00:50:56:ae:00:02 18 151
	Dynamic 00:50:56:ae:00:00 18 36
	Dynamic 00:50:56:b3:11:7e 18 17
	Dynamic 00:50:56:b1:00:0c 18 60
	Dynamic 00:0c:29:57:a9:bb 18 95
	Static 00:02:3d:20:22:03 12 0
	Dynamic 00:02:3d:20:22:02 18 26
	Dynamic 00:50:56:95:5a:11 18 109
	Dynamic 00:50:56:95:5a:08 18 5
	Static 00:02:3d:60:22:00 5 0
	Dynamic 00:50:56:bd:20:23 18 227
	Dynamic 00:00:5e:00:01:12 18 1
	Dynamic 00:0c:29:ac:e5:bc 18 220
	Dynamic 00:50:56:83:00:01 18 218
	Dynamic 00:50:56:bd:00:0c 18 23
	Dynamic 00:50:56:b3:25:2b 18 0
	Dynamic 00:50:56:8e:1d:3c 18 17
	Dynamic 00:0c:29:09:a7:fc 18 175
	Dynamic 00:50:56:87:00:10 18 1
	Dynamic 00:50:56:95:0d:9f 18 147
	Static 00:02:3d:10:22:03 2 0
	Dynamic 00:50:56:98:00:28 18 95
	Dynamic 00:50:56:95:3c:9e 18 78
	Dynamic 00:50:56:a6:00:01 18 33
	Dynamic 00:50:56:99:09:05 18 1
	Dynamic 00:0c:29:b3:03:75 18 133
	Static 00:02:3d:80:22:03 6 0
	Dynamic 00:0c:29:e4:bc:cf 18 4
	Dynamic 00:0c:29:e9:f2:0c 18 176
	Dynamic 00:50:56:3f:ab:ae 18 1
	Dynamic 00:50:56:b2:50:0f 18 1
	Dynamic 00:0c:29:ae:b9:db 18 267
	Dynamic 00:0c:29:34:26:d8 18 186
	Static 00:02:3d:40:22:03 10 0
	Dynamic 00:50:56:a0:b8:06 18 17
	Dynamic 00:1d:71:9a:9e:40 18 3
	Dynamic 00:13:f5:01:00:71 18 120
	Dynamic 00:13:f5:01:00:41 18 103
	Dynamic 00:13:f5:01:00:51 18 104
	Dynamic 00:13:f5:01:00:21 18 119
	Dynamic 00:13:f5:01:00:31 18 81
	Dynamic 00:13:f5:01:00:81 18 301
	Dynamic 00:13:f5:01:01:61 18 99
	Dynamic 00:50:56:9f:42:82 18 24
	Dynamic 00:13:f5:01:01:51 18 221
	Dynamic 00:13:f5:01:01:01 18 172
	Dynamic 00:50:56:3f:ac:de 18 9
	Dynamic 00:50:56:9f:01:64 18 15
	Dynamic 00:50:56:b6:65:d7 18 35
	Static 00:02:3d:30:22:03 3 0
	Dynamic 00:50:56:b0:27:fb 18 21
	Dynamic 00:50:56:3f:cd:ae 18 1
	Dynamic 00:50:56:a1:13:53 18 1

	Bridge domain 2 brtmax 4096, brtcnt 1, timeout 300
	VLAN 3970, swbd 3970, ""
	Flags: P - PVLAN S - Secure D - Drop
	Type MAC Address LTL timeout Flags PVLAN
	Static 00:02:3d:80:22:03 6 0

	Bridge domain 3 brtmax 4096, brtcnt 2, timeout 300
	VLAN 3969, swbd 3969, ""
	Flags: P - PVLAN S - Secure D - Drop
	Type MAC Address LTL timeout Flags PVLAN
	Static 00:02:3d:40:22:03 8 0
	Static 00:02:3d:80:22:03 6 0

	Bridge domain 4 brtmax 4096, brtcnt 3, timeout 300
	VLAN 3968, swbd 3968, ""
	Flags: P - PVLAN S - Secure D - Drop
	Type MAC Address LTL timeout Flags PVLAN
	Static 00:02:3d:80:22:03 6 0
	Static 00:02:3d:20:22:03 1 0
	Static 00:02:3d:60:22:03 5 0

	Bridge domain 5 brtmax 4096, brtcnt 1, timeout 300
	VLAN 3971, swbd 3971, ""
	Flags: P - PVLAN S - Secure D - Drop
	Type MAC Address LTL timeout Flags PVLAN
	Static 00:02:3d:80:22:03 6 0

	Bridge domain 6 brtmax 4096, brtcnt 0, timeout 300
	Segment ID 5000, swbd 4096, "dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f"

	Bridge domain 7 brtmax 4096, brtcnt 0, timeout 300
	Segment ID 5001, swbd 4097, "dvs.VCDVSorg_net_using_n1k_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565"

	Bridge domain 9 brtmax 4096, brtcnt 2, timeout 300
	Segment ID 5003, swbd 4099, "dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8"
	Flags: P - PVLAN S - Secure D - Drop
	Type MAC Address LTL timeout Flags PVLAN Remote IP
	Static 00:50:56:01:00:09 49 0 0.0.0.0
	Static 00:50:56:01:00:08 50 0 0.0.0.0


If using network segmentation (VXLAN or VLAN), see different Segments


	~ # vemcmd show segment
	Number of valid BDS: 8
	BD 6, vdc 1, segment id 5000, segment group IP 224.0.4.1, swbd 4096, 0 ports, "dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f"
	Portlist:
	BD 7, vdc 1, segment id 5001, segment group IP 224.0.4.2, swbd 4097, 0 ports, "dvs.VCDVSorg_net_using_n1k_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565"
	Portlist:
	BD 9, vdc 1, segment id 5003, segment group IP 224.0.4.4, swbd 4099, 2 ports, "dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8"
	Portlist:
	49 tets (37370594...5cdefd2f).eth0
	50 OI (3adadd61-7...7e42e965).eth0


List the different broadcast domains (usually different VLANs)


	~ # vemcmd show bd
	Number of valid BDS: 8
	BD 1, vdc 1, vlan 1, swbd 1, 3 ports, ""
	Portlist:
	BD 2, vdc 1, vlan 3970, swbd 3970, 0 ports, ""
	Portlist:
	BD 3, vdc 1, vlan 3969, swbd 3969, 2 ports, ""
	Portlist:
	8
	9

	BD 4, vdc 1, vlan 3968, swbd 3968, 3 ports, ""
	Portlist:
	1 inban
	5 inband port securit
	11

	BD 5, vdc 1, vlan 3971, swbd 3971, 2 ports, ""
	Portlist:
	14
	15

	BD 6, vdc 1, segment id 5000, segment group IP 224.0.4.1, swbd 4096, 0 ports, "dvs.VCDVStest-93aa922b-260b-4cf1-a47b-561d8736c70f"
	Portlist:
	BD 7, vdc 1, segment id 5001, segment group IP 224.0.4.2, swbd 4097, 0 ports, "dvs.VCDVSorg_net_using_n1k_vcd-ni_pool-25717f9d-78cc-48c1-8506-c38b429f3565"
	Portlist:
	BD 9, vdc 1, segment id 5003, segment group IP 224.0.4.4, swbd 4099, 2 ports, "dvs.VCDVStg-267074fa-608b-4c2a-8b98-5ffce69aa5f8"
	Portlist:
	49 test (37370594...5cdefd2f).eth0
	50 OI (3adadd61-7...7e42e965).eth0


Show the designated receiver, when using port-channel usefull to see which vmnic is used


	~ # vemcmd show dr
	Number of valid BDS: 8
	BD 1, vdc 1, vlan 1, 3 ports, DR 18, multi_uplinks FALSE
	Portlist:
	10
	12
	18 DR vmnic1

	BD 2, vdc 1, vlan 3970, 0 ports, DR 0, multi_uplinks FALSE
	Portlist:
	BD 3, vdc 1, vlan 3969, 2 ports, DR 0, multi_uplinks FALSE
	Portlist:
	8
	9

	BD 4, vdc 1, vlan 3968, 3 ports, DR 0, multi_uplinks FALSE
	Portlist:
	1 inban
	5 inband port securit
	11

	BD 5, vdc 1, vlan 3971, 2 ports, DR 0, multi_uplinks FALSE
	Portlist:
	14
	15

	BD 6, vdc 1, vlan 0, 0 ports, DR 0, multi_uplinks FALSE
	Portlist:
	BD 7, vdc 1, vlan 0, 0 ports, DR 0, multi_uplinks FALSE
	Portlist:
	BD 9, vdc 1, vlan 0, 2 ports, DR 0, multi_uplinks FALSE
	Portlist:
	49 test (37370594...5cdefd2f).eth0
	50 OI (3adadd61-7...7e42e965).eth0


Show packet statistics


	~ # vemcmd show packets
	LTL RxUcast TxUcast RxMcast TxMcast RxBcast TxBcast Txflood Rxdrop Txdrop Name
	8 166959 165382 0 0 679 163054 163054 0 0
	9 165382 166959 0 0 163054 679 167638 0 0
	10 166959 1501464 0 48422 685 4314976 5699480 0 0
	11 5449 2721 0 0 0 0 2721 0 0
	12 2721 1333409 0 48422 6 4315655 5697486 0 0
	18 1439150 71686 1550391 0 3885930 32 1170 2 0 vmnic1
	49 0 0 0 108 60 129 237 0 0 test.eth0
	50 0 0 218 0 259 12 12 0 0 OI.eth0


Check port-security information, if used


	~ # vemcmd show port security
	*T = Trunk
	*A = Access
	*P = Promiscous
	*I = Isolated
	*C = Community
	LTL VSM Port Mode PortSec PVLAN SVLAN
	18 Eth4/2 A
	49 Veth3 A
	50 Veth4 A


Show ingress (incoming) port drops


	~ # vemcmd show port-drops ingress
	LTL VSM Port Ingress DHCP ACL QoS Ingress Layer2 L3 LISP Netflow VSIM Sr Decisio L3 LISP L3 LISP L2 LISP VSIM Ds Flood
	18 Eth4/2 4 0 0 0 0 96931 0 0 0 0 0 0 0 0 0
	49 Veth3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0
	50 Veth4 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0


Show egress (outgoing) port drops


	~ # vemcmd show port-drops egress
	LTL VSM Port L3 Mod L2 LISP EgressS DHCP EgressV EgressV QoS ACL Netflow Egress
	18 Eth4/2 0 0 0 0 0 0 0 0 0 117
	49 Veth3 0 0 0 0 0 0 0 0 0 0
	50 Veth4 0 0 0 0 0 0 0 0 0 0
	Mcast 0 0 0 0 0 0 0 0 0 0
	Flood 0 0 0 0 0 0 0 0 0 0


Check to see if using a UCS Palo Card


	~ # vemcmd show palo-enic
	LTL Port DVport PaloNic Client-Name
	18 50331675 0 No vmnic1


Show heap usage


	~ # vemcmd show heap
	Heap Name Objs ObjBytes Denied DenBytes Min Max MaxObj
	vns-ctlocks 1 4096 0 0 8192 8192 8192
	vns-htlocks 1 16384 0 0 20480 20480 20480
	vns-tmr 9 1049360 0 0 4880 1082128 1082128
	vns-ct 3 852088 0 0 856184 856184 856184
	vns-ft 3 1704056 0 0 1708152 1708152 1708152
	vns-ht 3 2293880 0 0 2297976 2297976 2297976
	vns-sdp 9 106788 0 0 102408 233480 233480
	lispdb 0 0 0 0 20480 102400 102400
	ipdb 0 0 0 0 20480 102400 102400
	vsim 258 800832 0 0 819200 1048576 1048576
	DHCP BT 1 16384 0 0 20480 20480 20480
	netflow 0 0 0 0 20480 50331648 50331648
	qos heap 0 0 0 0 20480 16777216 16777216
	aclflow 1 196608 0 0 204800 204800 204800
	acl 1 2584 0 0 20480 10485760 10485760
	L2Mcast heap 6 4624 0 0 102400 5120000 5120000
	datapath 4123 8924696 0 0 9216000 16384000 16384000
	FSM Infra 0 0 0 0 51200 512000 512000
	infra 0 0 0 0 20480 102400 102400


List the different DVPortGroups


	~ # vemcmd show profile
	Name ID VLAN MTU Mode Duplex Speed Tagged VLANs
	dvportgroup-83 10 1 1500 Access Full Auto
	dvportgroup-88 11 1 1500 Access Full Auto


Show generic statistics


	~ # vemcmd show stats
	LTL Received Bytes Sent Bytes Txflood Rxdrop Txdrop Name
	8 168190 33569131 329520 54978624 163592 0 0
	9 329520 54978624 168190 33569131 168190 0 0
	10 168196 42622216 5885476 1415544046 5719548 0 0
	11 5467 2248773 2730 1446900 2730 0 0
	12 2736 1529160 5717545 1395661902 5717545 0 0
	18 3116390 452766365 150665 38715488 1179 2 0 vmnic1
	49 60 7310 251 55700 251 0 0 test.eth0
	50 505 111616 12 720 12 0 0 OI.eth0


Show port channel information, if used


	~ # vemcmd show pc
	pce_ind chan pc_ltl pce_in_pc LACP SG_ID NumVethsPinned mbrs
	------- ---- ------ --------- ---- ----- -------------- ----


Show LACP information


	~ # vemcmd show pc
	pce_ind chan pc_ltl pce_in_pc LACP SG_ID NumVethsPinned mbrs
	------- ---- ------ --------- ---- ----- -------------- ----
	~ # vemcmd show lacp
	LACP Offload is Disabled
	Phy LTL List : 18
	PC LTL in LACP Carrier List : 0

	---------------------------------------------------
	LACP PDU Cache for LTL 18
	---------------------------------------------------
	Upgrade Notify is Disabled
	LACP Bit Set : No
	VSM Actor Info
	--------------
	Sys ID : Sys Pri(0), Sys MAC(00:00:00:00:00:00)
	Port ID : Key(0), Port Num(0x0), Port Pri(0)
	State : 0
	VSM Partner Info
	----------------
	Sys ID : Sys Pri(0), Sys MAC(00:00:00:00:00:00)
	Port ID : Key(0), Port Num(0x0), Port Pri(0)
	State : 0
	Upstream Actor Info
	-------------------
	Sys ID : Sys Pri(0), Sys MAC(00:00:00:00:00:00)
	Port ID : Key(0), Port Num(0x0), Port Pri(0)
	State : 0
	Upstream Partner Info
	---------------------
	Sys ID : Sys Pri(0), Sys MAC(00:00:00:00:00:00)
	Port ID : Key(0), Port Num(0x0), Port Pri(0)
	State : 0


Show pinning information, if not use LACP but static mac pinning for portchannel


	~ # vemcmd show static pinning config
	LTL IfIndex VSM_SGID Backup_SGID


Show iSCSI pinning information, if using iSCSI binding with software iSCSI from the esx host


	~ # vemcmd show iscsi pinning
	Vmknic LTL Pinned_Uplink LTL


I will try to add commands that I find useful later on.

### Related Posts

- [Quick Step by Step Guide on how to Setup the Nexus1000v Distributed Switch](/2012/08/quick-step-by-step-guide-on-how-to-setup-the-nexus1000v-distributed-switch/)

