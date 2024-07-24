---
title: VCAP5-DCD Objective 3.2 – Create a vSphere 5 Physical Network Design from an Existing Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-3-2-create-a-vsphere-5-physical-network-design-from-an-existing-logical-design/
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['fcoe', 'trunk_port', 'stp', 'port_channel','vlan', 'logical_design']
---

### Describe VLAN options, including Private VLANs, with respect to virtual and physical switches

From VMware KB [1003806](http://kb.vmware.com/kb/1003806):

> Virtual LAN (VLAN) implementation is recommended in ESX/ESXi networking environments because:
>
> *   It integrates ESX/ESXi into a pre-existing network
> *   It secures network traffic
> *   It reduces network traffic congestion
> *   iSCSI traffic requires isolated network
>
> There are three methods of VLAN tagging that can be configured on ESXi:
>
> *   External Switch Tagging (EST)
> *   Virtual Switch Tagging (VST)
> *   Virtual Guest Tagging (VGT)

Here is EST:

> **External Switch Tagging**
>
> *   All VLAN tagging of packets is performed on the physical switch.
> *   ESX host network adapters are connected to access ports on the physical switch.
> *   The portroups connected to the virtual switch must have their VLAN ID set to 0.
> *   See this example snippet of a code from a Cisco switch port configuration:
>     `switchport mode access`
>     `switchport access vlan x`

Here is VST:

> **Virtual Switch Tagging**
>
> *   All VLAN tagging of packets is performed by the virtual switch before leaving the ESX/ESXi host.
> *   The ESX host network adapters must be connected to trunk ports on the physical switch.
> *   The portgroups connected to the virtual switch must have an appropriate VLAN ID specified.
> *   See the following example snippet of code from a Cisco switch port configuration:
>     `switchport trunk encapsulation dot1q`
>     `switchport mode trunk`
>     `switchport trunk allowed vlan x,y,z`
>     `spanning-tree portfast trunk`
>
> **Note**: The Native VLAN is not tagged and thus requires no VLAN ID to be set on the ESX/ESXi portgroup.

Here is VGT:

> **Virtual Guest Tagging**
>
> *   All VLAN tagging is performed by the virtual machine.
> *   You must install an 802.1Q VLAN trunking driver inside the virtual machine.
> *   VLAN tags are preserved between the virtual machine networking stack and external switch when frames are passed to/from virtual switches.
> *   Physical switch ports are set to trunk port.
> *   See this example snippet of code from a Cisco switch port configuration:
>     `switchport trunk encapsulation dot1q`
>     `switchport mode trunk`
>     `switchport trunk allowed vlan x,y,z`
>     `spanning-tree portfast trunk`

From the [vShpere Documentation](https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-networking/GUID-35B40B0B-0C13-43B2-BC85-18C9C91BE2D4.html):

> **Private VLANs**
> Private VLANs are used to solve VLAN ID limitations and waste of IP addresses for certain network setups.
>
> A private VLAN is identified by its primary VLAN ID. A primary VLAN ID can have multiple secondary VLAN IDs associated with it. Primary VLANs are **Promiscuous**, so that ports on a private VLAN can communicate with ports configured as the primary VLAN. Ports on a secondary VLAN can be either **Isolated**, communicating only with promiscuous ports, or **Community**, communicating with both promiscuous ports and other ports on the same secondary VLAN.
>
> To use private VLANs between a host and the rest of the physical network, the physical switch connected to the host needs to be private VLAN-capable and configured with the VLAN IDs being used by ESXi for the private VLAN functionality. For physical switches using dynamic MAC+VLAN ID based learning, all corresponding private VLAN IDs must be first entered into the switch's VLAN database.
>
> To configure distributed ports to use Private VLAN functionality, you must create the necessary Private VLANs on the vSphere distributed switch to which the distributed ports are connected.

Also check out "[VLANs and Trunking](http://www.ciscopress.com/articles/article.asp?p=29803&seqNum=6)" for sample PVLAN configuration on a Cisco Switch.

### Describe switch-specific settings for ESXi-facing ports, including but not limited to (STP,Jumbo Frames, Load-balancing, Trunking)

From "[VMware Virtual Networking Concepts](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/virtual_networking_concepts.pdf)":

> **Spanning Tree Protocol Not Needed**
> VMware Infrastructure 3 enforces a single-tier networking topology. In other words, there is no way to interconnect multiple virtual switches, thus the network cannot be configured to introduce loops. As a result, Spanning Tree Protocol (STP) is not needed and is not present.
>
> ...
> ...
>
> To minimize delays, disable the following on the physical switch:
>
> *   Spanning tree protocol (STP) — disable STP on physical network interfaces connected to the ESX Server host. For Cisco-based networks, enable port fast mode for access interfaces or portfast trunk mode for trunk interfaces (saves about 30 seconds during initialization of the physical switch port).
> *   Etherchannel negotiation, such as PAgP or LACP — must be disabled because they are not supported.
> *   Trunking negotiation (saves about four seconds).

From VMware KB [1003712](http://kb.vmware.com/kb/1003712):

> Jumbo Frames is officially supported in ESXi/ESX 4.x and later. For Jumbo Frames to be effective, the network must support Jumbo Frames (end-to-end). Configuration of Jumbo Frames on virtual switches is currently only available from the command line. Configuration of Jumbo Frames on vNetwork Distributed Switches can be done from vCenter.
>
> **Notes:**
>
> *   In ESX 4.x and 5.0, Jumbo Frames are supported on 1GB or 10GB NICs and you can update the MTU on a newly created port group or pre-existing port group.
> *   Jumbo Frames up to 9KB (9000 bytes) are supported.
> *   Like TSO, Jumbo Frames are supported in the guest operating system and in the ESX host kernel TCP/IP stack only in the context of ethernet network. They are limited to data networking only.
>
> To set up and verify physical network switch for Jumbo Frames, consult your vendor documentation. This example sets up and verifies the CISCO 3750 physical network switch for Jumbo Frames:
>
>     3750(config)# system mtu jumbo 9000
>     3750(config)# exit
>     3750# reload
>     3750# show system mtu
>     System MTU size is 1500 bytes
>     System Jumbo MTU size is 9000 bytes
>

### Describe network redundancy considerations at each individual component level

From this [PDF](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf):

> Create a single virtual Switch with teamed NICs across separate switches![redundant-switches](https://github.com/elatov/uploads/raw/master/2012/08/redundant-switches.png)

### Cite virtual switch security policies and settings

From "[VMware Virtual Networking Concepts](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/virtual_networking_concepts.pdf)":

> **Layer 2 Security Features**
> The virtual switch has the ability to enforce security policies to prevent virtual machines from impersonating other nodes on the network. There are three components to this feature.
>
> *   Promiscuous mode is disabled by default for all virtual machines. This prevents them from seeing unicast traffic to other nodes on the network.
> *   MAC address change lockdown prevents virtual machines from changing their own unicast addresses. This also prevents them from seeing unicast traffic to other nodes on the network, blocking a potential security vulnerability that is similar to but narrower than promiscuous mode.
> *   Forged transmit blocking, when you enable it, prevents virtual machines from sending traffic that appears to come from nodes on the network other than themselves

### Based on the service catalog and given functional requirements, for each service: Determine the most appropriate networking technologies for the design

There are actually a lot of good VMware networking designs at the [blog](http://kendrickcoleman.com/index.php/Tech-Blog/vmware-vsphere-5-host-nic-network-design-layout-and-vswitch-configuration-major-update.html) written by Kendick Coleman. Each design has it's pros and cons. Here is a design factoring in redundancy:

![example_of_redundant_vmware-network-design](https://github.com/elatov/uploads/raw/master/2012/08/example_of_redundant_vmware-network-design.png)

### Determine and explain the selected network teaming and failover solution

From "[VMware Virtual Networking Concepts](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/virtual_networking_concepts.pdf)":

> **NIC Teaming**
> You can connect a single virtual switch to multiple physical Ethernet adapters using the VMware Infrastructure feature called NIC teaming. A team can share the load of traffic between physical and virtual networks among some or all of its members and provide passive failover in the event of a hardware failure or a network outage. You can set NIC teaming policies at the port group level.
>
> **Note:** All physical switch ports in the same team must be in the same Layer 2 broadcast domain.
>
> **Route based on the originating virtual switch port ID**
>
> *   Choose an uplink based on the virtual port where the traffic entered the virtual switch. This is the default configuration and the one most commonly deployed.
> *   When you use this setting, traffic from a given virtual Ethernet adapter is consistently sent to the same physical adapter unless there is a failover to another adapter in the NIC team
>
> **Route based on source MAC hash**
>
> *   Choose an uplink based on a hash of the source Ethernet MAC address.
> *   When you use this setting, traffic from a given virtual Ethernet adapter is consistently sent to the same physical adapter unless there is a failover to another adapter in the NIC team.
> *   This setting provides an even distribution of traffic if the number of virtual Ethernet adapters is greater than the number of physical adapters
>
> **Route based on IP hash**
>
> *   Choose an uplink based on a hash of the source and destination IP addresses of each packet. (For non-IP packets, whatever is at those offsets is used to compute the hash.)Evenness of traffic distribution depends on the number of TCP/IP sessions to unique destinations. There is no benefit for bulk transfer between a single pair of hosts.
> *   All adapters in the NIC team must be attached to the same physical switch or an appropriate set of stacked physical switches. (Contact your switch vendor to find out whether 802.3ad teaming is supported across multiple stacked chassis.) That switch or set of stacked switches must be 802.3ad-compliant and configured to use that link-aggregation standard in static mode (that is, with no LACP). All adapters must be active.

And from the same document:

> **Failover Configurations**
> When you configure network failover detection you specify which of the following methods to use for failover detection:
>
> **Link Status only**
> Relies solely on the link status provided by the network adapter. This detects failures, such as cable pulls and physical switch power failures, but it cannot detect configuration errors, such as a physical switch port being blocked by spanning tree or misconfigured to the wrong VLAN or cable pulls on the other side of a physical switch.
>
> **Beacon Probing**
> Sends out and listens for beacon probes — Ethernet broadcast frames sent by physical adapters to detect upstream network connection failures — on all physical Ethernet adapters in the team, as shown in Figure 4. It uses this information, in addition to link status, to determine link failure. This detects many of the failures mentioned above that are not detected by link status alone, however beacon probing should not be used as a substitute for a robust redundant Layer 2 network design. Beacon probing is most useful to detect failures in the closest switch to the ESX Server hosts, where the failure does not cause a link-down event for the host

### Implement logical Trust Zones using network security/firewall technologies.

From a [VMUG Presentation](http://www.cpd.iit.edu/netsecure08/ROBERT_RANDELL.pdf):

![trust_zone_vcd](https://github.com/elatov/uploads/raw/master/2012/08/trust_zone_vcd.png)

### Based on service level requirements, determine appropriate network performance characteristics.

From the "[VMware vSphere Distributed Switch Best Practices](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vsphere-distributed-switch-best-practices-white-paper.pdf)", BTW great paper:

![type-of-net-traffic](https://github.com/elatov/uploads/raw/master/2012/08/type-of-net-traffic.png)

Based on the type of traffic they can use NIOC to allocate appropriate bandwidth. Here is an example from one of the designs:

![nioc_example](https://github.com/elatov/uploads/raw/master/2012/08/nioc_example.png)

### Given a current network configuration as well as technical requirements and constraints,determine the appropriate virtual switch solution: vSphere Standard Switch, vSphere Distributed Switch, Third-party solutions (ex. Nexus 1000V),Hybrid solutions

Here is a [link](http://www.cisco.com/en/US/prod/collateral/switches/ps9441/ps9902/solution_overview_c22-526262.pdf) that talks about all the different features of all the different virtual Switches. Here is just a snippet from the page:

![vswitch-feature-comparison](https://github.com/elatov/uploads/raw/master/2012/08/vswitch-feature-comparison.png)

If there is a requirement to use any of those then pick accordingly. I would use the N1K if I needed advanced features like ACLs, LACP, and SNMP. I would use the VMware DVS if I was using LLDP, centralized management and NIOC. I would the standard switch if it was a simple setup and none of the advanced feature were necessary. Finally the hybrid is good, because you can leave you mgmt network on the standard switch and if vCenter goes down then you network will be still okay.

### Based on an existing logical design, determine appropriate host networking resources

Plan ahead and see whether you need 1Gb or 10Gb. Also if you are planning to use VMdirect-IO Path, then you will need to plan ahead and get more NICs for other VMs. Also remember the Max Guide. For 4.1 only 4x10Gb NICs are supported and on ESX 5.x only 8x10Gb. Other limitation for 1Gb also apply and they are on a per-driver basis. Here are links to both of the Max Config guides:

*   [Configuration Maximums VMware vSphere 4.1](http://www.vmware.com/pdf/vsphere4/r41/vsp_41_config_max.pdf)
*   [Configuration Maximums VMware vSphere 5.0](https://www.vmware.com/pdf/vsphere5/r50/vsphere-50-configuration-maximums.pdf)

Also remember to put your 10Gb NIcs on PCIe 8x slots. If possible use NetQueue, helps with performance with 10Gb NICs.

### Properly apply converged networking considering VMware best practices If limited on 10Gb NICs utilize NIOC as described in 

[VMware Network I/O Control: Architecture, Performance and Best Practices VMware vSphere 4.1](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmware_netioc_bestpractices-white-paper.pdf)":

> Network convergence using 10GbE technology provides enormous opportunities for IT administrators and architects to simplify the physical network infrastructure while improving performance. Administrators and architects need a simple and reliable way to enable prioritization of critical traffic over the physical network if and when contention for those resources occurs. The Network I/O Control (NetIOC) feature available in VMware® vSphere™ 4.1 (“vSphere”) addresses these challenges by introducing a software approach to partitioning physical network bandwidth among the different types of network traffic flows. It does so by providing appropriate quality of service (QoS) policies enforcing traffic isolation, predictability and prioritization, therefore helping IT organizations overcome the contention resulting from consolidation.
>
> ...
> ...
>
> NetIOC enables the convergence of diverse workloads on a single networking pipe. It provides sufficient controls to the vSphere administrator in the form of limits and shares parameters to enable and ensure predictable network performance when multiple traffic types contend for the same physical network resources.

Also if an FCoE capable infrastructure is already in place then definitely try to use it. This way your CNA (Converged Network Adapter) can be used as a NIC (Network Interface Controller) and and HBA (Host Bus Adapter). You will definitely save on PCI slots and you won't have a need for a LAN switch and a SAN switch. An FCoE enabled switch will replace both. With FCoE make sure flow control is working properly. FCoE is a lossless protocol and it utilizes pause frames to appropriate notion if congestion is taking place. If you want to read up on FCoE I would suggest reading : "[QLogic Adapters and Cisco Nexus 5000 Series Switches: Fibre Channel over Ethernet Design Guide](http://www.cisco.com/en/US/prod/collateral/switches/ps9441/ps9670/white_paper_c11-569320_v1.pdf)"

Check out the [APAC BrownBag Session 3](https://professionalvmware.com/vmware-certifications/), it covers most of the material above.

