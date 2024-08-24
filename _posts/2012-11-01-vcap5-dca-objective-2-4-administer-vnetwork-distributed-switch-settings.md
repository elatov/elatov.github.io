---
title: VCAP5-DCA Objective 2.4 – Administer vNetwork Distributed Switch Settings
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-2-4-administer-vnetwork-distributed-switch-settings/
categories: ['certifications', 'networking', 'vcap5_dca', 'vmware']
tags: ['dvs','dvs_port_binding']
---

### Describe the relationship between vDS and the vSS

vSS (virtual Standard Switch) is just a regular vswitch and is configured on a per host basis. Most of the configurations are stored under /etc/vmware/esx.conf


	/net/vswitch/child[0000]/capabilities/ChecksumOffload = "true"
	/net/vswitch/child[0000]/capabilities/VlanTag = "true"
	/net/vswitch/child[0000]/capabilities/VlanUntag = "true"
	/net/vswitch/child[0000]/cdp/status = "listen"
	/net/vswitch/child[0000]/name = "vSwitch0"
	/net/vswitch/child[0000]/numPorts = "128"
	/net/vswitch/child[0000]/portgroup/child[0000]/name = "Management Network"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/hasUplinkOrder = "true"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/linkCriteria/beacon = "ignore"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/linkCriteria/fullDuplex = "ignore"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/linkCriteria/minSpeed = "10"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/linkCriteria/pctError = "ignore"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/maxActive = "1"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/notifySwitch = "true"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/reversePolicy = "true"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/rollingRestoration = "false"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/team = "lb_srcid"
	/net/vswitch/child[0000]/portgroup/child[0000]/teamPolicy/uplinks[0000]/pnic = "vmnic0"
	/net/vswitch/child[0000]/securityPolicy/forgedTx = "true"
	/net/vswitch/child[0000]/securityPolicy/interPgTx = "true"
	/net/vswitch/child[0000]/securityPolicy/localPackets = "true"
	/net/vswitch/child[0000]/securityPolicy/macChange = "true"
	/net/vswitch/child[0000]/securityPolicy/promiscuous = "false"
	/net/vswitch/child[0000]/shapingPolicy/enabled = "false"
	/net/vswitch/child[0000]/teamPolicy/hasUplinkOrder = "true"
	/net/vswitch/child[0000]/teamPolicy/linkCriteria/beacon = "ignore"
	/net/vswitch/child[0000]/teamPolicy/linkCriteria/fullDuplex = "ignore"
	/net/vswitch/child[0000]/teamPolicy/linkCriteria/minSpeed = "10"
	/net/vswitch/child[0000]/teamPolicy/linkCriteria/pctError = "ignore"
	/net/vswitch/child[0000]/teamPolicy/maxActive = "1"
	/net/vswitch/child[0000]/teamPolicy/notifySwitch = "true"
	/net/vswitch/child[0000]/teamPolicy/reversePolicy = "true"
	/net/vswitch/child[0000]/teamPolicy/rollingRestoration = "false"
	/net/vswitch/child[0000]/teamPolicy/team = "lb_srcid"
	/net/vswitch/child[0000]/teamPolicy/uplinks[0000]/pnic = "vmnic0"
	/net/vswitch/child[0000]/uplinks/child[0000]/pnic = "vmnic0"


The vDS (virtual Distributed Switch) contains multiple proxy switches, which reside on each host that sync together with vCenter to have a single management point. Most of the configurations are in the vCenter Database. But each host contains a /etc/vmware/dvsdata file and .dvsData folder on some of your datastores. From "[vDS config location and HA](https://blogs.vmware.com/vsphere/2011/06/vds-config-location-and-ha.html)":

> *   The .dvsData folder is only created if you have a VM on that datastore that is attached to a vDS. Thus if there is only VM’s that is attached to a vSwitch on a datastore there will not be a .dvsData folder. Also only the datastore that holds the .vmx config file will have the .dvsData folder.
> *   Inside the .dvsData folder there is a UUID number for each vDS switch.
> *   Inside the UUID folder is a smaller file that is a number. This number corresponds to the ethernetx.dvs.portId inside the .vmx file of a VM. Below we can see that ethernet0.dvs.portId=10.
>
> ![.dvsData_example](https://github.com/elatov/uploads/raw/master/2012/10/dvsData_example.png)
> ...
> ...
>
> *   /etc/vmware/dvsdata.db
>     *   Updated by hostd every 5 min
>     *   Contains data for persistent vdPorts (vmkernel)
> *   The smaller files (“10" in our case)
>     *   Updated with vdPort information every 5 min by hostd
>     *   Contains data for the VM’s vNIC’s that is attached to the vDS

Also check out this great post by Duncan Epping "[Digging deeper into the VDS construct](http://www.yellow-bricks.com/2012/02/23/digging-deeper-into-the-vds-construct/)"

### Understand the use of command line tools to configure appropriate vDS settings on an ESXi host

This was covered in the previous objectives

### Determine use cases for and apply Port Binding settings

From VMware KB [1022312](http://kb.vmware.com/kb/1022312):

> **Static binding**
>
> When you connect a virtual machine to a port group configured with static binding, a port is immediately assigned and reserved for it, guaranteeing connectivity at all times. The port is disconnected only when the virtual machine is removed from the port group. You can connect a virtual machine to a static-binding port group only through vCenter Server.
>
> **Note:** Static binding is the default setting, recommended for general use.
>
> **Dynamic binding**
>
> In a port group configured with dynamic binding, a port is assigned to a virtual machine only when the virtual machine is powered on and its NIC is in a connected state. The port is disconnected when the virtual machine is powered off or the virtual machine's NIC is disconnected. Virtual machines connected to a port group configured with dynamic binding must be powered on and off through vCenter.
>
> Dynamic binding can be used in environments where you have more virtual machines than available ports, but do not plan to have a greater number of virtual machines active than you have available ports. For example, if you have 300 virtual machines and 100 ports, but never have more than 90 virtual machines active at one time, dynamic binding would be appropriate for your port group.
>
> **Note:** Dynamic binding is deprecated in ESXi 5.0.
>
> **Ephemeral binding**
>
> In a port group configured with ephemeral binding, a port is created and assigned to a virtual machine when the virtual machine is powered on and its NIC is in a connected state. The port is deleted when the virtual machine is powered off or the virtual machine's NIC is disconnected.
>
> Ephemeral port assignments can be made through ESX/ESXi as well as vCenter, giving you the flexibility to manage virtual machine connections through the host when vCenter is down. Although only ephemeral binding allows you to modify virtual machine network connections when vCenter is down, network traffic is unaffected by vCenter failure regardless of port binding type.
>
> **Note:** Ephemeral portgroups should be used only for recovery purposes when you want to provision ports directly on host bypassing vCenter Server, not for any other case. This is true for several reasons:
>
> <p style="padding-left: 30px;">
>   **Scalability**
> </p>
>
> <p style="padding-left: 30px;">
>   An ESX/ESXi 4.x host can support up to 1016 ephemeral portgroups and an ESXi 5.x host can support up to 256 ephemeral portgroups. Since ephemeral portgroups are always pushed to hosts, this effectively is also the vCenter Server limit. For more information, see Configuration Maximums for VMware vSphere 5.0 and Configuration Maximums for VMware vSphere 4.1.
> </p>
>
> <p style="padding-left: 30px;">
>   **Performance**
> </p>
>
> <p style="padding-left: 30px;">
>   Every operation, including add-host and virtual machine power operation, is slower comparatively because ports are created/destroyed in the operation code path. Virtual machine operations are far more frequent than host-add or switch-operations, so ephemeral ports are more demanding in general.
> </p>
>
> <p style="padding-left: 30px;">
>   Non-persistent (that is, "ephemeral") ports
> </p>
>
> <p style="padding-left: 30px;">
>   Port-level permissions and controls are lost across power cycles, so no historical context is saved.
> </p>

To change the settings go to "Networking" View -> Right Click on a DVPortGroup -> Edit settings. It will look something like this:

![dvs_port_binding](https://github.com/elatov/uploads/raw/master/2012/10/dvs_port_binding.png)

### Configure Live Port Moving

From [Public Docs](https://kb.vmware.com/s/article/1010593):

> **Edit Advanced dvPort Group Properties**
> Use the dvPort Group Properties dialog box to configure advanced dvPort group properties such as port override settings.
> Procedure
>
> 1.  In the vSphere Client, display the Networking inventory view and select the dvPort group.
> 2.  From the Inventory menu, select Network > Edit Settings.
> 3.  Select Advanced to edit the dvPort group properties.
>     *   Select Allow override of port policies to allow dvPort group policies to be overridden on a per-port level.
>     *   Click Edit Override Settings to select which policies can be overridden.
>     *   Choose whether to allow live port moving.
>     *   Select Configure reset at disconnect to discard per-port configurations when a dvPort is disconnected from a virtual machine.
> 4.  Click OK.

Here is how the GUI looks like:

![live_port_migrating](https://github.com/elatov/uploads/raw/master/2012/10/live_port_migrating.png)

### Given a set of network requirements, identify the appropriate distributed switch technology to use

From "[Virtual Networking Features of VMware vSphere Distributed Switch and Cisco Nexus 1000V Series Switches](http://www.cisco.com/en/US/prod/collateral/switches/ps9441/ps9902/solution_overview_c22-526262.pdf)", here is a good feature list of the DVS:

![p1_dvs_features](https://github.com/elatov/uploads/raw/master/2012/10/p1_dvs_features.png)

![p2_dvs_features](https://github.com/elatov/uploads/raw/master/2012/10/p2_dvs_features.png)

![p3_dvs_features](https://github.com/elatov/uploads/raw/master/2012/10/p3_dvs_features.png)

Everything depends on the requirements, if you need QOS, then you can set that up. If you need to monitor the your network traffic then you can use NetFlow. If you need resource allocation then use NIOC. If you need DMZs then use PVLANs or just regular VLANs. The sky is the limit :)

### Configure and administer vSphere Network I/O Control

From "[vSphere Networking ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-networking-guide.pdf)":

> **vSphere Network I/O Control**
> Network resource pools determine the bandwidth that different network traffic types are given on a vSphere distributed switch.
>
> When network I/O control is enabled, distributed switch traffic is divided into the following predefined network resource pools: Fault Tolerance traffic, iSCSI traffic, vMotion traffic, management traffic, vSphere Replication (VR) traffic, NFS traffic, and virtual machine traffic.
>
> You can also create custom network resource pools for virtual machine traffic. You can control the bandwidth each network resource pool is given by setting the physical adapter shares and host limit for each network resource pool.
>
> The physical adapter shares assigned to a network resource pool determine the share of the total available bandwidth guaranteed to the traffic associated with that network resource pool. The share of transmit bandwidth available to a network resource pool is determined by the network resource pool's shares and what other network resource pools are actively transmitting. For example, if you set your FT traffic and iSCSI traffic resource pools to 100 shares, while each of the other resource pools is set to 50 shares, the FT traffic and iSCSI traffic resource pools each receive 25% of the available bandwidth. The remaining resource pools each receive 12.5% of the available bandwidth. These reservations apply only when the physical adapter is saturated.
>
> The host limit of a network resource pool is the upper limit of bandwidth that the network resource pool can use.
>
> Assigning a QoS priority tag to a network resource pool applies an 802.1p tag to all outgoing packets associated with that network resource pool.

Also from the same document:

> **Enable Network I/O Control on a vSphere Distributed Switch**
> Enable network resource management to use network resource pools to prioritize network traffic by type.
> **Prerequisites**
> Verify that your datacenter has at least one vSphere distributed switch version 4.1.0 or later.
> **Procedure**
>
> 1.  Log in to the vSphere Client and select the Networking inventory view.
> 2.  Select the vSphere distributed switch in the inventory pane.
> 3.  On the Resource Allocation tab, click Properties.
> 4.  Select Enable Network I/O Control on this vSphere ditributed switch, and click OK.

Here is how it looks in vCenter:

![enable_nioc](https://github.com/elatov/uploads/raw/master/2012/10/enable_nioc.png)

There is also a very good example in the VMware blog "[vSphere 5 New Networking Features – Enhanced NIOC](https://blogs.vmware.com/vsphere/2011/08/vsphere-5-new-networking-features-enhanced-nioc.html)". From the blog:

> **User-Defined Network Resource Pools**
>
> User-defined network resource pools in vSphere 5 provide an ability to add new traffic types beyond the standard system traffic types that are used for I/O scheduling.
>
> Figure below shows an example of a user-defined resource pool with shares, limits and IEEE 802.1p tag parameters described in a table. In this example, Tenant 1 and Tenant 2 are two user-defined resource pools with virtual machines connected to their respective independent port groups. Tenant 1, with three virtual machines, has five I/O shares. Tenant 2, with one virtual machine, has 15 I/O shares. This indicates that during contention scenarios, Tenant 2 virtual machines will have a higher guaranteed share than Tenant 1 virtual machines.
>
> ![user_defined_nioc_example](https://github.com/elatov/uploads/raw/master/2012/10/user_defined_nioc_example.png)
> ...
> ...
>
> **Configuration**
>
> The new resource pools can be defined at the Distributed Switch level by selecting the resource allocation tab and clicking on new network resource pools. After a new network resource pool is defined with shares and limits parameters, that resource pool can be associated with a port group. This association of a network resource pool with a port group enables customers to allocate I/O resources to a group of virtual machines or workloads. The figure below shows the new Tenant 1 and Tenant 2 resource pools created under user-defined network resource pools.
>
> ![user_defined_network_resources](https://github.com/elatov/uploads/raw/master/2012/10/user_defined_network_resources.png)
>
> ...
> ...
>
> **IEEE 802.1p Tagging**
>
> IEEE 802.1p is a standard for enabling QoS at MAC level. The IEEE 802.1p tag provides a 3-bit field for prioritization, which allows packets to be grouped into seven different traffic classes. The IEEE doesn’t mandate or standardize the use of recommended traffic classes. However, higher-number tags typically indicate critical traffic that has higher priority. The traffic is simply classified at the source and sent to the destination. The layer-2 switch infrastructure between the source and destination handles the traffic classes according to the assigned priority. In the vSphere 5.0 release, network administrators now can tag the packets going out of the host.
>
> **Configuration**
>
> IEEE 802.1p tagging can be enabled per traffic type. Customers can select the Distributed Switch and then the resource allocation tab to see the different traffic types, including system and user-defined traffic types. After selecting a traffic type, the user can edit the QoS priority tag field by choosing any number from 1 to 7. Figure below is the screenshot of QoS priority tag configuration for the MyVMTraffic traffic type.
>
> ![nioc_qos](https://github.com/elatov/uploads/raw/master/2012/10/nioc_qos.png)

### Use command line tools to troubleshoot and identify configuration items from an existing vDS

This was covered in [VCAP5-DCA Objective 2.1](/2012/10/vcap5-dca-objective-2-1-implement-and-manage-complex-virtual-networks/)

