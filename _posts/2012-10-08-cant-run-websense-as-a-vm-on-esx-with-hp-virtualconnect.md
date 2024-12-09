---
title: "Can't Run WebSense as a VM on ESX(i) Host with HP VirtualConnect"
author: Karim Elatov
layout: post
permalink: /2012/10/cant-run-websense-as-a-vm-on-esx-with-hp-virtualconnect/
categories: ['networking', 'vmware']
tags: ['hp_virtualconnect', 'span_port', 'vlan', 'websense']
---

We were trying to setup a VM to run WebSense on it, but we couldn't get all the traffic to reach the VM. Websense is a content filtering software, but for it to filter the content it needs to see all the traffic. When Websense runs on a physical machine it would sit in an area where it could see all the traffic. Here is a good picture of the setup from cisco community page:

![websense_in_a_routed-env](https://github.com/elatov/uploads/raw/master/2012/10/websense_in_a_routed-env.png)

Also here is the setup from the websense [install](https://www.websense.com/content/support/library/deployctr/v76/wwf_wws_sw_install.aspx) page:

![websense_how_to](https://github.com/elatov/uploads/raw/master/2012/10/websense_how_to.png)

In a virtual environment, the same is achieved my mirroring the required traffic to the switch port which in turn is connected to a vmnic (physical NIC of an ESX(i) Host) where the WebSense VM can see the traffic.

The Cisco switch was configured to SPAN the external port to the switch port which was connected to an ESXi host. I actually didn't setup the SPAN port nor did I know what hardware was used. All I knew was that if you took a laptop and plugged it into the same switch port, the mirrored traffic was seen. So here is a setup that worked just fine:

![SPAN_to_Laptop](https://github.com/elatov/uploads/raw/master/2012/10/SPAN_to_Laptop.png)

Now as soon as we plugged GigEthernet 1/8 into the ESX host we were not able to see the mirrored traffic. Now to setup ESX to run Websense, we followed the instructions laid out from WebSense site. From "[How to configure VMware to support Websense](https://www.websense.com/content/support/library/web/v71/wws_pdfs/ws_deployment_guide.pdf)":

> 1.  To see network traffic, Websense Network Agent requires a network interface card (used for monitoring) set to promiscuous mode.
>     1.  Websense running on VMware cannot see traffic that is mirrored from the switch. A packet capture will not show any traffic on the NIC. By default, the VMware NIC only accepts traffic that is specifically addressed to it. When using port span (port mirroring) the traffic is copied as is with the original destination IP’s in place. Because the traffic is not addressed to the Websense VMware NIC, the NIC drops it.
>     2.  To resolve, place the VMware NIC in promiscuous mode. This allows the NIC to accept all traffic for all destinations
>     3.  In some environments, it may be necessary to configure this NIC's portgroup to VLAN 4095 (equivalent to all).
> 2.  To use bridged networking, each virtual machine must have its own IP address.
> 3.  If your virtual machine includes multiple operating systems, each operating system must have a unique network address—even if only one operating system runs at a time. (This is a VMware requirement.)

So we basically we needed to:

*   Set the vSwitch to be in promiscuous mode. This allows every VM that is on that vSwitch to see all the traffic. Instructions laid out in VMware KB [1004099](https://knowledge.broadcom.com/external/article?legacyId=1004099)
*   If we are mirroring multiple VLANs then we need to set the VLAN Tag as 4095 on the PortGroup where the WebSense VM resides. This allows all VLANs to pass through the port group. Instructions on how to set that up are in VMware KB [1004252](https://knowledge.broadcom.com/external/article?legacyId=1004252)
*   Put the NIC inside the OS to promiscuos mode, Wireshark does this but default. This allows the VM to receive traffic destined to other address than it self or broadcasts.

So here is how the setup looked like:

![SPAN_to_vSwitch](https://github.com/elatov/uploads/raw/master/2012/10/SPAN_to_vSwitch.png)

With the above setup we couldn't see the traffic from the SPAN port. We put another VM on the same vSwitch and we saw the traffic for that VM. I then suggested booting from a Linux Live CD to see if a non-ESX host could see the traffic. After we booted into the Live CD, to make sure we were working with correct physical NIC, I asked the customer to down the switch port that is our destination Mirrored port. I wanted to see on the Linux OS which NIC goes down. When we did a 'shutdown' on the port, none of the physical NICs went down within the OS. The customer then mentioned that maybe it has something to do with the VirtualConnect. I actually didn't know that we were using a Blade Enclosure. So instead our setup actually looked like this:

![SPAN_to_virtual_connect](https://github.com/elatov/uploads/raw/master/2012/10/SPAN_to_virtual_connect.png)

The Virtual Connect adds an extra layer of network flow. As soon as I heard that we were using a Virtual Connect, we contacted HP support and they said that you can't mirror external ports to internal ones. You can mirror between internal ports but not external ports. [Here](http://h30499.www3.hp.com/t5/HP-BladeSystem-Virtual-Connect/Promiscuous-Mode-in-VC/td-p/5342417#.UG40pLTA991) is an HP communities page that talks about it. So lesson learned, you can't send mirror traffic through an HP Virtual Connect.

