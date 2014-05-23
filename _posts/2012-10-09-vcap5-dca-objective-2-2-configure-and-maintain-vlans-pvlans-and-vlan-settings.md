---
title: VCAP5-DCA Objective 2.2 – Configure and Maintain VLANs, PVLANs and VLAN Settings
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-2-2-configure-and-maintain-vlans-pvlans-and-vlan-settings/
dsq_thread_id:
  - 1413715339
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify types of VLANs and PVLANs

From [vSphere Networkin ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf):

> **VLAN Configuration**
> Virtual LANs (VLANs) enable a single physical LAN segment to be further segmented so that groups of ports are isolated from one another as if they were on physically different segments.
>
> Configuring ESXi with VLANs is recommended for the following reasons.
>
> *   It integrates the host into a pre-existing environment.
> *   It secures network traffic.
> *   It reduces network traffic congestion.
> *   iSCSI traffic requires an isolated network.
>
> You can configure VLANs in ESXi using three methods: External Switch Tagging (EST), Virtual Switch Tagging (VST), and Virtual Guest Tagging (VGT).
>
> With EST, all VLAN tagging of packets is performed on the physical switch. Host network adapters are connected to access ports on the physical switch. Port groups that are connected to the virtual switch must have their VLAN ID set to 0.
>
> With VST, all VLAN tagging of packets is performed by the virtual switch before leaving the host. Host network adapters must be connected to trunk ports on the physical switch. Port groups that are connected to the virtual switch must have an appropriate VLAN ID specified.
>
> With VGT, all VLAN tagging is performed by the virtual machine. VLAN tags are preserved between the virtual machine networking stack and external switch when frames are passed to and from virtual switches. Physical switch ports are set to trunk port.
>
> **NOTE** When using VGT, you must have an 802.1Q VLAN trunking driver installed on the virtual machine.

From the same document:

> **Private VLANs**
> Private VLANs are used to solve VLAN ID limitations and waste of IP addresses for certain network setups.
>
> A private VLAN is identified by its primary VLAN ID. A primary VLAN ID can have multiple secondary VLAN IDs associated with it. Primary VLANs are **Promiscuous**, so that ports on a private VLAN can communicate with ports configured as the primary VLAN. Ports on a secondary VLAN can be either **Isolated**, communicating only with promiscuous ports, or **Community**, communicating with both promiscuous ports and other ports on the same secondary VLAN.
>
> To use private VLANs between a host and the rest of the physical network, the physical switch connected to the host needs to be private VLAN-capable and configured with the VLAN IDs being used by ESXi for the private VLAN functionality. For physical switches using dynamic MAC+VLAN ID based learning, all corresponding private VLAN IDs must be first entered into the switch's VLAN database.
>
> To configure distributed ports to use Private VLAN functionality, you must create the necessary Private VLANs on the vSphere distributed switch to which the distributed ports are connected.

### Determine use cases for and configure VLAN Trunking

If you want to allow multiple VLANs through a single physical switch port then setup a VLAN Trunk on the physical switch and do VST from the Standard Virtual Switch or Distributed Virtual Switch. If you plan to do VGT then set the VLAN to 4095 on the SVS or set a port group type to VLAN Trunk for the DVS.

To configure VST on the SVS (Standard Virtual Switch), click properties on the vSwitch, then select a port-group and then click edit. Then Under the "General" tab assign a VLAN under "VLAN ID". The window looks like this:

![vst_svs](https://github.com/elatov/uploads/raw/master/2012/09/vst_svs.png)

To do the same thing on the DVS (Distributed Virtual Switch). Go To "Networking" View -> Right Click on your DVPortGroup and Select "Edit Settings -> Click on VLAN -> Change the "VLAN type" to VLAN and assign a VLAN ID. It will look like this:

![vst_dvs](https://github.com/elatov/uploads/raw/master/2012/09/vst_dvs.png)

To configure VGT on the SVS under the same properties window where you set the VLAN above, just set it to 4095. It looks like this:

![vgt_svs](https://github.com/elatov/uploads/raw/master/2012/09/vgt_svs.png)

After this is done you will need to setup the GOS (Guest Operating System) to tag the vlan.

To do VGT with DVS. Go To "Networking" View -> Right Click on your DVPortGroup and Select "Edit Settings -> Click on VLAN -> Change the "VLAN type" to "VLAN Trunking" and under the "VLAN trunk range" enter vlans that will be tagged within the GOS. It will look like this:

![vgt_dvs](https://github.com/elatov/uploads/raw/master/2012/09/vgt_dvs.png)

### Determine use cases for and configure PVLANs

From VMware KB [1010691](http://kb.vmware.com/kb/1010691) here is a pretty good diagram:

![pvlans_vmware](https://github.com/elatov/uploads/raw/master/2012/09/pvlans_vmware.png)

Basically if you want to add an extra layer of security for your environment and you have a use case for the PVLANs types (isolated, community, and promiscuous) then setup VLANs. As a side note physical switch configuration is required. More information on the physical switch setup can be seen in "[VLANs and Trunking](http://www.ciscopress.com/articles/article.asp?p=29803&#038;seqNum=6)"

To configure it on the DVS, from "[vSphere Networking ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-networking-guide.pdf)":

> **Create a Private VLAN**
> You can create a private VLAN for use on a vSphere distributed switch and its associated distributed ports.
> **Procedure**
> 1 Log in to the vSphere Client and select the Networking inventory view.
> 2 Right-click the vSphere distributed switch in the inventory pane, and select Edit Settings.
> 3 Select the Private VLAN tab.
> 4 Under Primary Private VLAN ID, click [Enter a Private VLAN ID here], and enter the number of the primary private VLAN.
> 5 Click anywhere in the dialog box, and then select the primary private VLAN that you just added. The primary private VLAN you added appears under Secondary Private VLAN ID.
> 6 For each new secondary private VLAN, click [Enter a Private VLAN ID here] under Secondary Private VLAN ID, and enter the number of the secondary private VLAN.
> 7 Click anywhere in the dialog box, select the secondary private VLAN that you just added, and select either Isolated or Community for the port type.
> 8 Click OK.

Here is how the screen looks like:

![pvlans_dvs](https://github.com/elatov/uploads/raw/master/2012/09/pvlans_dvs.png)

**NOTE** Make sure your primary VLAN is not used for anything else, or the above setup will fail (ie, if you had a portgroup set to use VLAN 100 as regular vlan, the private VLAN setup will fail).

After that is done, for your DVPortGroup set the "VLAN type" to Private VLAN and select the appropriate PVLAN. The screen will look like this:

![pvlans_dvpg](https://github.com/elatov/uploads/raw/master/2012/09/pvlans_dvpg.png)

### Use command line tools to troubleshoot and identify VLAN configurations

Check VLAN assignments on SVS:


	esxcli network vswitch standard portgroup list


Check VLAN assignments on DVS. "Networking" View -> Select DVS -> Select the "Networks" Tab. It will look something like this:

![dvs_vlans_view](https://github.com/elatov/uploads/raw/master/2012/09/dvs_vlans_view.png)

or run the following:


	net-dvs -l
