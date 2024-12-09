---
published: true
title: ESX(i) Host Experiencing a lot of Active Path Changes and Disconnects to/from VNX 5300 over iSCSI
author: Karim Elatov
layout: post
permalink: /2012/08/esxi-host-experiencing-a-lot-of-active-path-changes-and-disconnects-to-vnx-5300-over-iscsi/
categories: ['networking', 'storage', 'vmware']
tags: ['performance', 'alua', 'qos', 'iscsi', 'lun_trespass', 'useano', 'vnx']
---

I was recently working on case which had the following setup:

![ESX-To-VNX](https://github.com/elatov/uploads/raw/master/2012/08/ESX-To-VNX.jpg)

Over night the even hosts would start having a lot of disconnects and path changes/thrashing. On the array end we could see a lot of logins and logouts from the hosts as well. The configuration on the host side looked really good. We had two VMkernel interface setup with iSCSI NIC binding:


	~ # esxcfg-vmknic -l
	Interface Port Group IP Address Netmask MAC Address MTU Enabled Type
	vmk0 Mgmt 10.10.222.23 255.255.255.0 00:50:56:72:5d:58 1500 true STATIC
	vmk1 vMotion 10.10.221.24 255.255.255.0 00:50:56:7a:59:e9 1500 true STATIC
	vmk2 iSCSI-VLAN22 10.10.22.102 255.255.255.0 00:50:56:73:4e:46 1500 true STATIC
	vmk3 iSCSI-VLAN24 10.10.24.102 255.255.255.0 00:50:56:78:a2:cf 1500 true STATIC


The bottom two VMkernel interfaces were used for SW-iSCSI binding:


	~ # esxcli swiscsi nic list -d vmhba39
	vmk2
	pNic name: vmnic4
	ipv4 address: 10.10.22.102
	ipv4 net mask: 255.255.255.0
	ipv6 addresses:
	mac address: 00:26:55:df:c9:98
	mtu: 1500
	toe: false
	tso: true
	tcp checksum: false
	vlan: true
	vlanId: 0
	ports reserved: 63488~65536
	link connected: true
	ethernet speed: 1000
	packets received: 425589374
	packets sent: 404543288
	NIC driver: e1000e
	driver version: 1.1.2-NAPI
	firmware version: 5.11-2

	vmk3
	pNic name: vmnic5
	ipv4 address: 10.10.24.102
	ipv4 net mask: 255.255.255.0
	ipv6 addresses:
	mac address: 00:26:55:df:c9:99
	mtu: 1500
	toe: false
	tso: true
	tcp checksum: false
	vlan: true
	vlanId: 0
	ports reserved: 63488~65536
	link connected: true
	ethernet speed: 1000
	packets received: 320691695
	packets sent: 311646049
	NIC driver: e1000e
	driver version: 1.1.2-NAPI



We were using vmnic4 and vmnic5 for the binding. Checking out those Nics:


	~ # esxcfg-nics -l | egrep 'vmnic4|vmnic5'
	vmnic4 0000:0b:00.00 e1000e Up 1000Mbps Full 00:26:55:df:c9:98 1500 Intel Corporation NC360T PCI Express Dual Port Gigabit Server Adapter
	vmnic5 0000:0b:00.01 e1000e Up 1000Mbps Full 00:26:55:df:c9:99 1500 Intel Corporation NC360T PCI Express Dual Port Gigabit Server Adapter


We saw that from the 'esxcli swscsi nic list' output we were using e1000e driver version 1.1.2. Checking out the [HCL](http://partnerweb.vmware.com/comp_guide2/detail.php?deviceCategory=io&productid=985&deviceCategory=io&VID=8086&DID=105e&SVID=103c&SSID=7044&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc) for the above NIC. We were at the latest version:

> ESX/ESXi 4.1 U2 e1000e version 1.1.2.1-1vmw N/A async

From the above output we could also see that Jumbo Frames were not utilized. Lastly we saw each VMkernel interface is on it's own subnet/VLAN. This is recommendation from EMC, from article "[Using EMC VNX Storage with VMware vSphere, Version 2.1](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/249258606-h8229-vnx-vmware-tb-2-pdf.pdf)":

> EMC recommends the following configuration options for VNX systems:
>
> *   Configure each adapter with an IP address from a separate network subnet.
> *   Use a separate Ethernet switch path to the VNX iSCSI Targets/Network Portals.
>
> Figure 33 on page 86 illustrates the minimum configuration for an ESXi host with two network cards. The network interface for vmk1 is configured with an IP address on the 17.24.110.0/24 subnet. The iSCSI targets on ports A4 and B4 are also configured with addresses on the 17.24.110.0 subnet. ESXi network interfaces for vmk2 and the iSCSI targets on VNX ports A5 and B5 use IP addresses on the 10.1.1.0/24 subnet. Each vmnic has two paths to the array, for a total of four paths from the host to the array.

Here is diagram from that same article:

![vnx-iscsi-setup](https://github.com/elatov/uploads/raw/master/2012/08/vnx-iscsi-setup.png)

We can confirm our configuration by looking inside the SW-iSCSI database. First dump the database into a text file:


	~ # vmkiscsid --dump-db db.txt
	Dumping Configuration DB to db.txt
	Dump Complete


The database is broken into the following sections:



	~ # grep "^=====" db.txt
	=========[ISID]=========
	=========[InitiatorNodes]=========
	=========[Targets]=========
	==================
	=========[ifaces]=========
	=========[internal]=========
	=========[nodes]=========
	==================
	==================


To figure out what IPs we are using to connect to the VNX we can check out the Target section, and search for the following:


	~ # sed -n '/Targets/,/\.address'
	'node.name'='iqn.1992-04.com.emc:cx.xxx3301534.a5'
	'node.conn[0].address'='10.10.22.21'
	'node.name'='iqn.1992-04.com.emc:cx.xxx3301534.b5'
	'node.conn[0].address'='10.10.24.21'


Since the customer was only using one port from each SP:

1.  VNX1_SPA_A5 is iqn.1992-04.com.emc:cx.xxx3301534.a5 with IP of 10.10.22.21 (vlan 22)
2.  VNX1_SPB_B5 is iqn.1992-04.com.emc:cx.xxx3301534.b5 with IP of 10.10.24.21 (vlan 24)

they decided to separate each port from each SP by subnet. Checking out the paths for one LUN I saw the following:


	~ # esxcfg-mpath -b | head -4
	naa.60060xxxxxxxxxxx : DGC iSCSI Disk (naa.60060xxxxxxxxxxxxxx)
	vmhba39:C0:T4:L12 LUN:12 state:active iscsi Adapter: iqn.1998-01.com.vmware:host2-55c15df4 Target: IQN=iqn.1992-04.com.emc:cx.xxx00113301534.b5 Alias= Session=00023d000002 PortalTag=2
	vmhba39:C0:T0:L12 LUN:12 state:active iscsi Adapter: iqn.1998-01.com.vmware:host2-55c15df4 Target: IQN=iqn.1992-04.com.emc:cx.xxx3301534.a5 Alias= Session=00023d000001 PortalTag=1


We had two active paths, one from each SP (T4 is SPB_B5 and T0 is SPA_A5). Since this was an Active/Passive array the customer enabled ALUA on the array (check out this [post](/2012/04/seeing-a-high-number-of-trespasses-from-a-clariion-array-with-esx-hosts/) if you want to know more about ALUA). From the EMC article:

> Active-Active mode (failover mode 4) — When the host initiators are configured for ALUA mode, I/Os can be serviced from either SP in the VNX. The LUN is still owned by the SP where it was created. The default SP LUN also provides the optimal I/O path for the LUN.

and from the host:


	~ # esxcli nmp device list -d naa.60060xxxx
	naa.60060xxxx
	Device Display Name: DGC iSCSI Disk (naa.60060xxxx)
	Storage Array Type: VMW_SATP_ALUA_CX
	Storage Array Type Device Config: {navireg=on, ipfilter=on}{implicit_support=on;explicit_support=on; explicit_allow=on;alua_followover=on;{TPG_id=2,TPG_state=AO}{TPG_id=1,TPG_state=ANO}}
	Path Selection Policy: VMW_PSP_FIXED_AP
	Path Selection Policy Device Config: {preferred=vmhba39:C0:T0:L12;current=vmhba39:C0:T4:L12}
	Working Paths: vmhba39:C0:T4:L12


The Path Selection Policy is set to Fixed and that is okay. From the EMC article:

> Although Fixed Path is the preferred PSP for VNX, Round Robin (VMW_PSP_RR) is also of interest in some environments due to the ability to actively distribute host I/O across all paths.
>
> Round Robin is fully supported, but Path Restore is not currently integrated for VNX LUNs. If an SP path becomes unavailable, due to an SP reboot or NDU for example, the LUN trespasses to the peer SP. The LUN does not trespass back when the SP becomes available again. This is why EMC recommends VMW_PSP_FIXED. If the path is set to Round Robin, monitor the LUN trespass occurrences through Unisphere. EMC also provides scripted tools to integrate vSphere with VNX, and posts them to the Everything VMware page on the EMC Community website. One such PowerShell script provides an automated method to detect and restore the trespassed LUNs.

After confirming that the setup is okay, checking out the logs, I saw the following:


	Aug 15 06:07:13 vobd: Aug 15 06:07:13.285: 171974745962us:  Lost connectivity to storage device naa.60060xxx. Path vmhba39:C0:T0:L0 is down. Affected datastores: "VMFS_Volume01"..
	Aug 15 06:07:13 vobd: Aug 15 06:07:13.285: 171971079169us: [vob.scsi.scsipath.pathstate.dead] scsiPath vmhba39:C0:T0:L1 changed state from on.
	Aug 15 06:07:13 vmkernel: 1:23:46:11.079 cpu23:4257)vmw_psp_fixed_ap: psp_fixed_apSelectPathToActivateInt: Changing active path from vmhba39:C0:T0:L1 to vmhba39:C0:T4:L1 for device "naa.60060xxxx".
	Aug 15 06:07:13 vmkernel: 1:23:46:11.079 cpu23:4257)VMW_SATP_ALUA: satp_alua_activatePaths: Activation disallowed due to follow-over.
	Aug 15 06:07:13 vobd: Aug 15 06:07:13.286: 171974746430us:  Lost path redundancy to storage device naa.6006xxx. Path vmhba39:C0:T0:L1 is down. Affected datastores: "VMFS_Volume02"..
	Aug 15 06:07:13 vmkernel: 1:23:46:11.099 cpu13:882014)WARNING: NMP: nmp_IssueCommandToDevice: I/O could not be issued to device "naa.6006xxx" due to Not found
	Aug 15 06:07:13 vmkernel: 1:23:46:11.099 cpu13:882014)WARNING: NMP: nmp_DeviceRetryCommand: Device "naa.60060160xxxxx": awaiting fast path state update for failover with I/O blocked. No prior reservation exists on the device.
	Aug 15 06:07:13 vmkernel: 1:23:46:11.099 cpu13:882014)WARNING: NMP: nmp_DeviceStartLoop: NMP Device "naa.6006016xxxx" is blocked. Not starting I/O from device.


Checking out the frequency of the path thrashing and what LUN this kept happening to, I saw the following:


	/var/log # grep 'Changing active path from' messages* | awk '{print $12,$14}' | sort | uniq -c | sort -nr | head
	24 vmhba39:C0:T4:L1 vmhba39:C0:T0:L1
	24 vmhba39:C0:T0:L1 vmhba39:C0:T4:L1
	5 vmhba39:C0:T5:L1 vmhba39:C0:T2:L1
	5 vmhba39:C0:T4:L9 vmhba39:C0:T0:L9
	5 vmhba39:C0:T4:L15 vmhba39:C0:T0:L15
	5 vmhba39:C0:T4:L12 vmhba39:C0:T0:L12
	5 vmhba39:C0:T4:L10 vmhba39:C0:T0:L10
	5 vmhba39:C0:T2:L1 vmhba39:C0:T5:L1
	5 vmhba39:C0:T0:L9 vmhba39:C0:T4:L9
	5 vmhba39:C0:T0:L15 vmhba39:C0:T4:L15


We saw LUN 1 jump back an forth between both of Targets 24 times but we also saw other LUNs jump back and forth as well. The above messages matched VMware KB [2005369](https://knowledge.broadcom.com/external/article?legacyId=2005369). I asked the customer if we were seeing trespasses and we did, but not as much as we saw of Login and Logout events on the array. Checking the logs to see if we disconnected from the array, I saw the following:


	/var/log # egrep 'OFFLINE|ONLINE' messages* | awk '{print $9,$10,$17}' | sort | uniq -c
	5 vmhba39:CH:0 T:0 "OFFLINE"
	6 vmhba39:CH:0 T:0 "ONLINE"
	5 vmhba39:CH:0 T:4 "OFFLINE"
	5 vmhba39:CH:0 T:4 "ONLINE"


Looks like we disconnected from both of the Targets about the same amount of times but we re-connected as well. Looking closer into the devices, I noticed that for some LUNs were using the non-optimized path:


	~ # esxcli nmp path list -d naa.60060xxxx
	iqn.1998-01.com.vmware:host2,iqn.1992-04.com.emc:cx.xxx3301534.b5,t,2-naa.60060xxx
	Runtime Name: vmhba39:C0:T4:L12
	Device: naa.60060xxxx
	Device Display Name: DGC iSCSI Disk (naa.6006xxxx)
	Group State: active unoptimized
	Array Priority: 1
	Storage Array Type Path Config: {TPG_id=2,TPG_state=ANO,RTP_id=12,RTP_health=UP}
	Path Selection Policy Path Config: {current: no; preferred: yes}

	iqn.1998-01.com.vmware:host2,iqn.1992-04.com.emc:cx.xxx3301534.a5,t,1-naa.60060xxxx
	Runtime Name: vmhba39:C0:T2:L12
	Device: naa.60060xxxx
	Device Display Name: DGC iSCSI Disk (naa.60060xxxx)
	Group State: active
	Array Priority: 0
	Storage Array Type Path Config: {TPG_id=1,TPG_state=AO,RTP_id=6,RTP_health=UP}
	Path Selection Policy Path Config: {current: yes; preferred: no}


Notice "Path Selection Policy Path Config" setting. If were using the active optimized path we would see '{current: yes; preferred: yes}', but we didn't see that. From the above VMware KB, here are some reasons why we would use a non-optimized path:

> There are two use-cases for using the active non-optimized ALUA paths:
>
> *   When there are no optimized paths available.
> *   During SAN boot, the multi-path driver is not loaded yet, and the simple BIOS SAN boot agent uses whatever paths it finds first.

or if we explicitly set it to do so:

> if the Path Selection policy (PSP) is configured to use the active non-optimized (ANO) path to issue I/O.

The PSP setting is only available for Round Robin and not for Fixed:

> Some ALUA arrays automatically initiate a LUN failover (trespass) when enough I/O is directed to a non-optimized path. This happens so I/O is internally re-directed to an active optimized path.
>
> Configuring PSP_RR to use ANO paths for such arrays can result in path thrashing and poor I/O performance.

So in our case, since the active optimized path was unavailable we started using the non-optimized path. During our trouble shooting efforts we trespassed all the LUNs over to SPB and left it over night and the issue didn't occur. As soon as we trespassed the LUNs back to SPA the issue came up again. The customer replaced the whole SPA on the VNX but it didn't help out.

After the above test we knew that it had to do something with VLAN 22(path to SPA), because when we only used VLAN 24 (path to SPB) we didn't see any issues. After much investigation it turned out that one of the stacked switches had QOS enabled and that was causing a bottle neck. The customer ran the following command on the offending switch:

	no mls qos


and the path thrashing stopped.

So here is a summary of what happened. One of the stacked switches had QOS enabled. This caused a bottle neck with one of the paths. The ESX host would eventually lose the bad/degraded path cause it would send too much IO down that path and it would fail. After losing the path, it would start using the non-optimized path. When VNX receives 128K IOPs via a non-optimized path it will trespass that LUN to other SP cause it sees that too much IO is trying to get to LUN via the other SP/path. There is a good discussion about this in the EMC Communities, [here](https://www.dell.com/community/VMware/lun-tresspass-and-round-robin/td-p/6876460):

> After 128,000 I/O via the non-optimized paths, the system will make the decision to trespass the LUN (implicit trespass) instead of maintaining the non-optimal paths of an extra hop.

Eventually the path would become available and we would switch back to the optimized path and the cycle would start all over again. At times a trespass wouldn't occur and we would just jump back and forth between the paths.

