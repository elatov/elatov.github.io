---
title: VCAP5-DCA Objective 2.3 – Deploy and Maintain Scalable Virtual Networking
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-2-3-deploy-and-maintain-scalable-virtual-networking/
categories: ['networking', 'certifications', 'vcap5_dca', 'vmware']
tags: ['iscsi', 'stp','beacon_probing']
---

### Identify VMware NIC Teaming policies

From "[vSphere Networking ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-networking-guide.pdf)"

> **Edit Failover and Load Balancing Policy for a vSphere Standard Switch**
> Use Load Balancing and Failover policies to determine how network traffic is distributed between adapters and how to reroute traffic in the event of an adapter failure.
>
> The Failover and Load Balancing policies include the following parameters:
>
> *   Load Balancing policy: The Load Balancing policy determines how outgoing traffic is distributed among the network adapters assigned to a standard switch. Incoming traffic is controlled by the Load Balancing policy on the physical switch.
> *   Failover Detection: Link Status/Beacon Probing
> *   Network Adapter Order (Active/Standby)
>
> In some cases, you might lose standard switch connectivity when a failover or failback event occurs. This causes the MAC addresses used by virtual machines associated with that standard switch to appear on a different switch port than they previously did. To avoid this problem, put your physical switch in portfast or portfast trunk mode.

From the same document:

> In the Load Balancing list, select an option for how to select an uplink.
>
> ![load_balancing_algorithms](https://github.com/elatov/uploads/raw/master/2012/09/load_balancing_algorithms.png)
>
> In the Network failover detection list, select the option to use for failover detection.
>
> ![network_failover_detection](https://github.com/elatov/uploads/raw/master/2012/09/network_failover_detection.png)

Also from the same document, here is a summary of all the policies:

> Specify the settings in the Policy Exceptions group
>
> ![portgroup_network_policies](https://github.com/elatov/uploads/raw/master/2012/09/portgroup_network_policies.png)

### Identify common network protocols

When it comes to virtual switch talking to the physical network these are involved:

STP - Spanning Tree Issue (it's recommended to be disable or at least set portfast, more information in VMware KB [1003804](https://knowledge.broadcom.com/external/article?legacyId=1003804) )
LACP - Link Aggregation Control Protocol only supported with 5.1
Etherchannel - Supported only with the IP_hash Algorithtm (for sample config check out VMware KB [1004048](https://knowledge.broadcom.com/external/article?legacyId=1004048)
QOS - Quality of Service, with VMware only 802.1p tagging is supported (for a good example check out [What’s New in VMware vSphere 5.0 Networking](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/whats-new-vmware-vsphere-50-networking-technical-whitepaper.pdf))

### Understand the NIC Teaming failover types and related physical network settings

There are two options as described above, "Link Status Only" and Beacon Probing. For "Link Status Only" make sure you have a consistent negotiation policy set. For 1GB it's recommended to set auto/auto negotiation from the physical switch and from the physical NIC. If that is set properly then failover should be pretty smooth.

### Determine and apply Failover settings

This was discussed in the above objectives.

### Configure explicit failover to conform with VMware best practices

If you are using Software iSCSI and you want to utilized MPIO (MultiPath IO) then you will need to bind each vmk to a vmnic.

From "[vSphere Storage ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf)":

> **Change Port Group Policy for iSCSI VMkernel Adapters**
> If you use a single vSphere standard switch to connect VMkernel to multiple network adapters, change the port group policy, so that it is compatible with the iSCSI network requirements.
>
> By default, for each virtual adapter on the vSphere standard switch, all network adapters appear as active. You must override this setup, so that each VMkernel interface maps to only one corresponding active NIC. For example, vmk1 maps to vmnic1, vmk2 maps to vmnic2, and so on.
>
> **Prerequisites**
> Create a vSphere standard switch that connects VMkernel with physical network adapters designated for iSCSI traffic. The number of VMkernel adapters must correspond to the number of physical adapters on the vSphere standard switch.
>
> **Procedure**
> 1 Log in to the vSphere Client and select the host from the inventory panel.
> 2 Click the Configuration tab and click Networking.
> 3 Select the vSphere standard switch that you use for iSCSI and click Properties.
> 4 On the Ports tab, select an iSCSI VMkernel adapter and click Edit.
> 5 Click the NIC Teaming tab and select Override switch failover order.
> 6 Designate only one physical adapter as active and move all remaining adapters to the Unused Adapters category.
> 7 Repeat Step 4 through Step 6 for each iSCSI VMkernel interface on the vSphere standard switch.

If you are limited on NICs you can have one vSwitch with two uplinks. Inside the vswitch you can have two portgroups, 1 for Management and 1 for vMotion (each should be on a separate VLAN). You can set vmnic0 to be active for Management and set vmnic1 as standby. Set the failover policy the opposite for vMotion, vmnic1 active and vmnic0 as standvy. With this setup you can have redundancy and no two types of traffic sharing the same NIC (isolation).

### Configure port groups to properly isolate network traffic

Use VST and trunk ports on the physical switch and try to isolate your traffic by physical nics as well. Here is a pretty good example:

![vswitch_example](https://github.com/elatov/uploads/raw/master/2012/10/vswitch_example.png)

