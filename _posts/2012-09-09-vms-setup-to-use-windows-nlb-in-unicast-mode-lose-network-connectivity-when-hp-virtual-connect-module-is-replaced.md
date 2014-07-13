---
title: VMs Setup to Use Windows NLB in Unicast Mode Lose Network Connectivity When HP Virtual Connect Module is Replaced
author: Karim Elatov
layout: post
permalink: /2012/09/vms-setup-to-use-windows-nlb-in-unicast-mode-lose-network-connectivity-when-hp-virtual-connect-module-is-replaced/
categories: ['networking', 'vmware']
tags: ['garp', 'hp_virtualconnect', 'windows_nlb']
---

A VirtualConnect Module was being replaced on an HP Enclosure and only the VMs used for Windows NLB lost network connectivity.  If you are not too familiar with the HP VirtualConnect I would suggest reading "[HP Virtual Connect traffic flow](http://h20000.www2.hp.com/bc/docs/support/SupportManual/c01990371/c01990371.pdf)", here is a good picture:

![flex-fabric](https://github.com/elatov/uploads/raw/master/2012/09/flex-fabric.png)

In the above picture, Flex Fabric Interconnect is our Virtual Connect Interconnect Module. Flex Fabric is an extension of the Virtual Connect Module. From "[HP BladeSystem c-Class architecture](http://h20000.www2.hp.com/bc/docs/support/SupportManual/c00810839/c00810839.pdf)":

> **Virtual Connect**
> Virtual Connect includes a set of interconnect modules and embedded software that implements server-edge virtualization. It puts an abstraction layer between the servers and the external networks
>
> Virtual Connect uses connection profiles in combination with dynamic pools of unique MAC and WWN addresses to establish server connections to LANs and SANs. The server connection profiles contain MAC, WWN, and boot-from-SAN definitions assigned to BladeSystem enclosure bays and not to individual servers. The physical server in each bay uses the MAC and WWN assignments in the bay profile instead of its default NIC or HBA addresses. Even if you replace a server, the MAC and WWN assignments for the device bay remain constant, and the change is invisible to the network.
>
> ![vc-server-edge](https://github.com/elatov/uploads/raw/master/2012/09/vc-server-edge.png)
>
> **Virtual Connect Flex-10 **
> Virtual Connect Flex-10 technology is a hardware-based technology. It lets you separate the
> bandwidth of a single 10GbE port into four physical network connections (FlexNIC) or three physical NIC devices and one physical HBA device. Through the Virtual Connect management interface, you can allocate the bandwidth in 100 Mb increments up to 10 Gb/s. You can also change the allocated bandwidth of an active FlexNIC or FlexHBA without rebooting the server. Each blade server can have up to four times as many network connections without adding NIC or HBA cards or switches.
>
> **Virtual Connect FlexFabric**
> HP Virtual Connect FlexFabric interconnect modules and FlexFabric adapters extend Flex 10
> technology to include data and storage traffic within each 10 Gb server connection. This allows you to allocate LAN and SAN fabrics of a single 10 GbE data stream into four separate connections— one connection for each server port can be allocated to storage (FlexHBA) for either FCoE or iSCSI. You can adjust the bandwidth and routing information of each connection. A FlexFabric adapter functions as a standard NIC, a Flex-10 NIC, or a converged network adapter (CNA). To aggregate the LAN and SAN data, the FlexFabric adapter encapsulates Fibre Channel frames as FCoE or uses iSCSI along with the Ethernet LAN data. You can configure FlexFabric adapters to support either FCoE or iSCSI, but not concurrent streams of both. When the data stream enters the Virtual Connect FlexFabric interconnect module, the converged LAN and SAN traffic separate. Data streams leaving the BladeSystem enclosure use traditional Ethernet and storage (FC or SCSI) protocols. As a result, Flex-10 technology with FlexFabric adapters and VC FlexFabric modules provides a significant reduction in cabling, switches, and required ports at the server edge.

Also from "[Overview of HP Virtual Connect technologies](http://h20000.www2.hp.com/bc/docs/support/SupportManual/c00814156/c00814156.pdf)":

> **FlexNIC capabilities**
> Flex-10 and FlexFabric adapters allow you to partition a 10 Gb link into several smaller bandwidth FlexNICs. Virtual machine applications often require increased network connections per server, increasing network complexity while reducing the number of server resources. Virtual Connect addresses this issue by letting you divide a 10 Gb network connection into four independent FlexNIC server connections. A FlexNIC is a physical PCIe function (PF) that appears to the system ROM, OS, or hypervisor as a discrete physical NIC with its own driver instance. It is not a virtual NIC contained in a software layer.
>
> ![flex-10-adapters](https://github.com/elatov/uploads/raw/master/2012/09/flex-10-adapters.png)

Here is another picture of the HP Virtual Connect FlexFabric InterConnect Module :

![flex-fabric2](https://github.com/elatov/uploads/raw/master/2012/09/flex-fabric2.png)

Sometimes the Virtual Connect Module technology is just bundled as one technology, but in reality it consists of a couple of things. From "[HP Virtual Connect for the Cisco Network Administrator](http://h20000.www2.hp.com/bc/docs/support/SupportManual/c01386629/c01386629.pdf)":

> **Virtual Connect Components**
> There are three key components that make up the Virtual Connect infrastructure. Two
> components are hardware and one component is software. The three key components are
> Virtual Connect Ethernet modules, Virtual Connect Fibre Channel modules, Virtual Connect
> Manager (VCM).
>
> ![hp-vc-components](https://github.com/elatov/uploads/raw/master/2012/09/hp-vc-components.png)

There also many different types of Virtual Connect Modules:

![diff-vcs](https://github.com/elatov/uploads/raw/master/2012/09/diff-vcs.png)

So with the Virtual Connect FlexFabric Module you pass-through both NICs and HBAs. This is actually exactly what we were replacing in our setup.

Let's get back on track. Upon replacing the Virtual Connect Module (VCM), VMs that were using Windows NLB, lost network connectivity. We had two Virtual Connect Modules and they were setup in an Active/Active Manner. This picture from "[HP Virtual Connect Ethernet Cookbook: Single and Multi Enclosure Domain (Stacked) Scenarios](http://h20000.www2.hp.com/bc/docs/support/SupportManual/c01990371/c01990371.pdf)" depicts our setup pretty well:

![flex-10-server-profile-a_a](https://github.com/elatov/uploads/raw/master/2012/09/flex-10-server-profile-a_a.png)

I wasn't present when the VMC replacement took place but we grabbed logs right as the incident occurred. From the logs, I saw the following NICs on the HP Blade Server:


	commands$ head -11 nicinfo.sh.txt
	Network Interface Cards Information.

	Name PCI Device Driver Link Speed Duplex MAC Address MTU Description
	----------------------------------------------------------------------------------------
	vmnic0 0000:002:00.0 be2net Up 1000 Full 00:17:a4:77:00:c6 1500 Emulex Corporation NC553i 10Gb 2-port FlexFabric Converged Network Adapter
	vmnic1 0000:002:00.1 be2net Up 1000 Full 00:17:a4:77:00:c8 1500 Emulex Corporation NC553i 10Gb 2-port FlexFabric Converged Network Adapter
	vmnic2 0000:002:00.4 be2net Up 4000 Full 00:17:a4:77:00:ca 1500 Emulex Corporation NC553i 10Gb 2-port FlexFabric Converged Network Adapter
	vmnic3 0000:002:00.5 be2net Up 4000 Full 00:17:a4:77:00:cc 1500 Emulex Corporation NC553i 10Gb 2-port FlexFabric Converged Network Adapter
	vmnic4 0000:002:00.6 be2net Up 1000 Full 00:17:a4:77:00:ce 1500 Emulex Corporation NC553i 10Gb 2-port FlexFabric Converged Network Adapter
	vmnic5 0000:002:00.7 be2net Up 1000 Full 00:17:a4:77:00:d0 1500 Emulex Corporation NC553i 10Gb 2-port FlexFabric Converged Network Adapter


So we had 6 NICs presented to the Host and they are a Flex-10 CNA (so we can partition one port into many virtual ports, this was described above). Now as the VCM was pulled I saw the following in the 'vmkernel.log' file:


	2012-08-30T05:42:07.494Z cpu9:4105)vmnic0 : 02:00.0 Link Down
	2012-08-30T05:42:07.494Z cpu21:4117)vmnic2 : 02:00.4 Link Down
	2012-08-30T05:42:07.494Z cpu21:4117)vmnic4 : 02:00.6 Link Down
	2012-08-30T05:42:07.494Z cpu0:4804)lpfc820 0000:02:00.2: 0:1305 Link Down Event x2 received Data: x2 x20 x800110 x0 x0
	2012-08-30T05:42:17.496Z cpu18:4759) rport-0:0-3: blocked FC remote port time out: saving binding
	2012-08-30T05:42:17.496Z cpu15:4766) rport-0:0-2: blocked FC remote port time out: saving binding
	2012-08-30T05:42:17.496Z cpu16:4804)lpfc820 0000:02:00.2: 0:(0):0203 Devloss timeout on WWPN 20:23:00:02:ac:00:13:f0 NPort x013500 Data: x0 x7 x0
	2012-08-30T05:42:17.496Z cpu16:4804)lpfc820 0000:02:00.2: 0:(0):0203 Devloss timeout on WWPN 21:23:00:02:ac:00:13:f0 NPort x012800 Data: x0 x7 x0


We can see that vmnic0, vmnic2, and vmnic4 all went down. This is expected, since the other vmnics (vmnic1,vmnic3, and vmnic5) are configured to connect the other VCM (which was active) and didn't go down.

We were using a DVS, so just looking at the DVS section, I saw the following:


	commands$ sed -n '/DVS/,$p' esxcfg-vswitch_-l.txt
	DVS Name Num Ports Used Ports Configured Ports MTU Uplinks
	dvSwitch 256 19 256 1500 vmnic3,vmnic2

	DVPort ID In Use Client
	354 1 vmnic2
	355 1 vmnic3
	164 0
	16 1 VM1.eth0
	139 1 VM2.eth0
	264 1 VM3 ethernet0
	399 1 VM4 ethernet0
	360 1 VM5 ethernet0
	431 1 NLB_VM1 ethernet0
	430 1 NLB_VM2 ethernet0
	103 1 VM6 ethernet0
	162 1 VM7 ethernet0
	126 1 VM8 ethernet0
	11 1 VM9 ethernet0
	156 1 VM10 ethernet0
	401 1 VM11 ethernet0
	403 1 VM12 ethernet0


The VMs that had the issue were "NLB_VM1" and "NLB_VM2". Checking for the virtual ports (that these VMs correspond to) in vsish, I see that they correspond to the following:


	$ for i in `vsish -c vsi_traverse_-s.txt -e ls /net/portsets/DvsPortset-0/ports/`; do echo $i; vsish -c vsi_traverse_-s.txt -e cat /net/portsets/DvsPortset-0/ports/"$i"status|grep clientName;done
	50331649/
	clientName:Management
	50331650/
	clientName:vmnic2
	50331651/
	clientName:vmnic3
	50331678/
	clientName:VM1.eth0
	50331686/
	clientName:VM2.eth0
	50331687/
	clientName:VM3 ethernet0
	50331688/
	clientName:VM4 ethernet0
	50331689/
	clientName:VM5 ethernet0
	50331690/
	clientName:VM6 ethernet0
	50331691/
	clientName:VM7 ethernet0
	50331692/
	clientName:VM8 ethernet0
	50331693/
	clientName:VM9 ethernet0
	50331695/
	clientName:VM10 ethernet0
	50331697/
	clientName:VM11 ethernet0
	50331698/
	clientName:VM12 ethernet0
	50331700/
	clientName:NLB_VM1 ethernet0
	50331701/
	clientName:NLB_VM2 ethernet0
	50331702/


So our virtual ports are as follows; 50331700 is NLB_VM1, and 50331701 is NLB_VM2.

Now checking for what uplinks those are using at the time of when the logs were taken, I see the following:


	$ vsish -c vsi_traverse_-s.txt -e cat /net/portsets/DvsPortset-0/ports/50331700/teamUplink
	vmnic2
	$ vsish -c vsi_traverse_-s.txt -e cat /net/portsets/DvsPortset-0/ports/50331701/teamUplink
	vmnic2


So the uplink (vmnic2) that those two VMs were using went down. Now looking at the logs later on, I see the following:


	2012-08-30T05:51:43.931Z cpu7:4103)vmnic0 : 02:00.0 Link Up - 10 Gbps Full Duplex
	2012-08-30T05:51:44.117Z cpu23:444906)vmnic2 : 02:00.4 Link Up - 10 Gbps Full Duplex
	2012-08-30T05:51:44.230Z cpu21:444905)vmnic4 : 02:00.6 Link Up - 10 Gbps Full Duplex


So right as we replaced the VCM the NICs came up and the VMs regained network connectivity. Remember we were using NLB in Unicast mode, from this VMware KB [1006778](http://kb.vmware.com/kb/1006778):

> To configure NLB UNICAST mode:
> ESX vSwitch properties Notify Switches = NO

From the above port we know the dvports are '430' and '431'. So let's check out the setting of DVport 431:


	commands$ sed -n '/port 431:/,/port [0-9]*:/p' net-dvs_-l.txt
	port 431:
	com.vmware.common.port.alias = , propType = CONFIG
	com.vmware.common.port.connectid = 2066096687 , propType = CONFIG
	com.vmware.common.port.portgroupid = dvportgroup-1628 , propType = CONFIG
	com.vmware.common.port.block = false , propType = CONFIG
	com.vmware.common.port.ptAllowed = 0x 0. 0. 0. 0
	propType = CONFIG
	com.vmware.etherswitch.port.teaming:
	load balancing = source virtual port id
	link selection = link state up; beacon state ok; link speed>=10Mbps;
	link behavior = reverse filter; best effort on failure; shotgun on failure;
	active = dvUplink1; dvUplink2;
	standby =
	propType = CONFIG
	com.vmware.etherswitch.port.security = deny promiscuous; allow mac change; allow forged frames
	propType = CONFIG
	com.vmware.etherswitch.port.vlan = VLAN 98
	propType = CONFIG
	com.vmware.etherswitch.port.txUplink = normal , propType = CONFIG
	com.vmware.common.port.volatile.persist = /vmfs/volumes/5036eb9b-0c48192e-c742-0017a4770080/.dvsData/57 9b 3e 50 29 db d8 56-40 28 67 2d b4 1c 1b 2e/431 , propType = CONFIG
	com.vmware.common.port.volatile.vlan = VLAN 98
	propType = RUNTIME VOLATILE
	com.vmware.common.port.statistics:
	pktsInUnicast = 114179
	bytesInUnicast = 34335744
	pktsInMulticast = 10286
	bytesInMulticast = 3027483
	pktsInBroadcast = 507082
	bytesInBroadcast = 698493176
	pktsOutUnicast = 237699
	bytesOutUnicast = 143759547
	pktsOutMulticast = 10856
	bytesOutMulticast = 1688073
	pktsOutBroadcast = 2145701
	bytesOutBroadcast = 2170216215
	pktsInDropped = 0
	pktsOutDropped = 0
	pktsInException = 0
	pktsOutException = 0
	propType = RUNTIME
	com.vmware.common.port.volatile.status = inUse linkUp portID=50331701 propType = RUNTIME
	com.vmware.common.port.volatile.ptstatus = noPassthruReason=32, propType = RUNTIME
	port 430:


Notice this line:


	link behavior = reverse filter; best effort on failure; shotgun on failure;


Whenever 'Notify Switch" is enabled you see it in that line. For example we know that VM1 was okay and it was using DVport '16'. So let's check out the setting of that port:


	commands$ sed -n '/port 16:/,/port [0-9]*:/p' net-dvs_-l.txt | sed -n '/com.vmware.etherswitch.port.teaming/,/propType/p'
	com.vmware.etherswitch.port.teaming:
	load balancing = source virtual port id
	link selection = link state up; beacon state ok; link speed>=10Mbps;
	link behavior = notify switch; reverse filter; best effort on failure; shotgun on failure;
	active = dvUplink1; dvUplink2;
	standby =
	propType = CONFIG


and as we expected there is a 'notify switch' option in our 'link behavior' section. Again here is how our ports looked like:


	commands$ sed -n '/port 430:/,/port [0-9]*:/p' net-dvs_-l.txt | sed -n '/com.vmware.etherswitch.port.teaming/,/propType/p'
	com.vmware.etherswitch.port.teaming:
	load balancing = source virtual port id
	link selection = link state up; beacon state ok; link speed>=10Mbps;
	link behavior = reverse filter; best effort on failure; shotgun on failure;
	active = dvUplink1; dvUplink2;
	standby =
	propType = CONFIG

	commands$ sed -n '/port 431:/,/port [0-9]*:/p' net-dvs_-l.txt | sed -n '/com.vmware.etherswitch.port.teaming/,/propType/p'
	com.vmware.etherswitch.port.teaming:
	load balancing = source virtual port id
	link selection = link state up; beacon state ok; link speed>=10Mbps;
	link behavior = reverse filter; best effort on failure; shotgun on failure;
	active = dvUplink1; dvUplink2;
	standby =
	propType = CONFIG


So we know those two ports do not have the "Notify Switch" option set, which is good since this is necessary for NLB in unicast to work properly. Now what does the option 'notify switch' do exactly. Upon any changes to a VM, the VMkernel sends a Gratuitous ARP to the physical switch to make sure it updates it's CAM tables. If that option is disabled then the VMkernel doesn't send the GARP out and the physical switch doesn't know if a VM had moved over to another physical NIC. From VMware KB [1556](http://kb.vmware.com/kb/1556):

> In the ESX host, the VMkernel sends a RARP packet each time certain actions occur—for example, a virtual machine is powered on, experiences teaming failover, performs certain VMotion operations, and so forth. The RARP packet informs the switch of the MAC address of that virtual machine. In a NLB cluster environment, this exposes the MAC address of the cluster NIC as soon as a NLB node is powered on.

So in our case this was expected. Here is a step by step process of what happened:

1.  We removed the VCM
2.  vmnic2 goes down, vmnic3 becomes the active one
3.  Non-NLB VMs, that failed over to vmnnic3, send a GARP to the physical switch
4.  Physical switch updates the MAC addresses and what ports they are on
5.  VMs that are part of the NLB cluster in Unicast mode, don't sent out GARP to the upstream switch
6.  Physical switch doesn't update it's CAM tables, we can't reach those VMs
7.  New VCM is plugged in
8.  VMs that were using vmnic2 failback to it
9.  non-NLB VMs send GARP again, all is good
10. NLB VMs return to it's original port, MAC addresses match the MAC address table of the physical switch, we regain connectivity

So lesson learned, VMs that participate in NLB in unicast mode will be down if the there is a failover of physical NICs.

### Related Posts

- [Load Balancing IIS Sites with NLB](/2013/04/load-balancing-iis-sites-with-nlb/)

