---
published: true
title: vMotion Causes Unicast Flooding
author: Karim Elatov
layout: post
categories: [ networking, vmware ]
tags: [ unicast_flooding, vmotion]
---
I recently ran into an issue where a live migration from one host to another cause the physical switch to experience unicast flooding. After much investigation, the solution was quite simple: Don't setup your management and your vMotion network traffic to be on the same subnet. Now let's take a look as to why this is a bad idea. Another person from the VMware communities ran into the same issue ([vMotion Causing Unicast Flooding](http://communities.vmware.com/thread/306862)). He described his discoveries in the following manner. He initially saw the mgmt mac-address initiate the connection but after the connection has been established another mac-address is seen transferring the data. Now why is that? Well, let's take a closer look. Let's say we have the following setup on our ESXi host:

	~ # esxcfg-vmknic -l
	Interface Port_Group IP_Family IP_Address Netmask       Broadcast  MAC Address       MTU   Enabled Type
	vmk0     Management  IPv4      10.0.1.128 255.255.255.0 10.0.1.255 00:0c:29:2c:54:17 1500  true    DHCP
	vmk1     SC2         IPv4      10.0.1.129 255.255.255.0 10.0.1.255 00:50:56:79:aa:91 1500  true    STATIC

So we have vmk0 as 10.0.1.128 and vmk1 as 10.0.1.129 (so both of the vmkernel interfaces are on the same subnet). The vmkernel routing table will look like the following for the above setup:

	~ # esxcfg-route -l
	VMkernel Routes:
	Network   Netmask       Gateway       Interface
	10.0.1.0  255.255.255.0 Local Subnet   vmk0
	default   0.0.0.0       10.0.1.2       vmk0

Notice that the traffic destined for 10.0.1.0 subnet will leave out of vmk0 if it's using the routing table to choose its destination. During the first 10% of the vMotion that is the connection establishment stage, at that point, it uses the routing table and leaves out of vmk0 since that is the default interface that has access to that subnet. Now, after the connection is finished establishing, it then sends the traffic out of vmk1 since it's labeled as a vMotion interface at which point it ignores the routing table. I have actually seen it the other way around as well, where the connection starts out on vmk1 and then switches to vmk0; it just depends on what you are doing. In the end, my recommendation is to never have two interfaces on the same subnet, that is just asking for trouble :). There is a lot of VMware documentation that alludes to this fact, but it's never very direct. For example in this PDF, "[4.1 ESXi configuration Guide](http://www.vmware.com/pdf/vsphere4/r41/vsp_41_esxi_server_config.pdf)", under the Networking Best Practices, we see the following:

> Keep the vMotion connection on a separate network devoted to vMotion. When migration with vMotion
> occurs, the contents of the guest operating system’s memory is transmitted over the network. You can do this either by using VLANs to segment a single physical network or separate physical networks (the latter is preferable).

Personally, I would recommend to separate all of your traffic by subnets: NFS, FT, vMotion, and etc... (VMware KB [1006989](http://kb.vmware.com/kb/1006989)).The above PDF also refers to this:

> To physically separate network services and to dedicate a particular set of NICs to a specific network
> service, create a vSwitch for each service. If this is not possible, separate them on a single vSwitch by
> attaching them to port groups with different VLAN IDs. In either case, confirm with your network
> administrator that the networks or VLANs you choose are isolated in the rest of your environment and
> that no routers connect them.

VMware KB [2010877](http://kb.vmware.com/kb/2010877) talks about the same thing. It also mentions the difference between ESX vs. ESXi, but that is another topic for another post :).

**Update**: If you ABSOLUTELY MUST go against best practices, Joe posted about a "workaround" here: [Against Best Practices: vMotion and Management on the Same Network](http://virtuallyhyper.com/2012/04/against-best-practices-vmotion-and-management-on-the-same-network/)


