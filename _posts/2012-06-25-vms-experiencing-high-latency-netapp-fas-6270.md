---
title: VMs are Experiencing High Latency to NetApp FAS 6240
author: Karim Elatov
layout: post
permalink: /2012/06/vms-experiencing-high-latency-netapp-fas-6270/
categories: ['networking', 'storage', 'vmware']
tags: ['performance', 'gavg', 'io_latency', 'netapp', 'nfs']
---

I was recently presented with the following environment:

{:.kt}
|VMware_ESX|NetApp  |
|----------|--------|
|ESX 4.1P03|FAS 6240|

With this setup all the VMs from the ESX that resided on the NFS Datastores exported from the NetApp Array were experiencing high GAVG. Since this is NFS we don't have DAVG or KAVG statistics. Looking at esxtop, this is what we saw:

![nfs_ds_latency_1](https://github.com/elatov/uploads/raw/master/2012/06/nfs_ds_latency_1.png)

Notice the GAVG for the to NFS datastore is ~25ms. We would consistently see 20-40ms of latency to array. Looking at the VM's latency, we saw similar numbers:

![nfs_vm_latency_1](https://github.com/elatov/uploads/raw/master/2012/06/nfs_vm_latency_1.png)

Looks like the VMs are experiencing Write Latency to the NetApp Array. Looking over the network configuation of the ESX host I saw the following:


	$ esxcfg-vmknic -l
	Interface Port Group/DVPort IP Family IP Address Netmask Broadcast MAC Address MTU TSO MSS Enabled Type
	vmk0 89 IPv4 10.195.x.22 255.255.255.0 10.195.x.255 00:50:56:78:bf:60 1500 65535 true STATIC
	vmk1 13 IPv4 10.205.x.22 255.255.255.0 10.205.x.255 00:50:56:70:d4:32 1500 65535 true STATIC


Looking at the NAS connections, I saw the following:


	$ esxcfg-nas -l
	export_1 is /vol/export_1 from 10.204.x.29 mounted
	export_2 is /vol/export_2 from 10.204.x.29 mounted
	export_3 is /vol/export_3 from 10.204.x.30 mounted
	export_4 is /vol/export_4 from 10.204.x.30 mounted
	...
	...


The first thing that stood out was the fact that the vmkernel interface used for the NFS connection (10.205.x.22) was not on the same subnet as the NAS itself (10.204.x.29).
I wanted to see what the network topology looked like, and it was something like this:

![ESX-to-NetApp_L3](https://github.com/elatov/uploads/raw/master/2012/06/ESX-to-NetApp_L3.jpg)

Layer 3 NFS is not supported with ESX until ESX 5.0U1. From the [Release Notes of 5.0U1](https://www.vmware.com/support/vsphere5/doc/vsp_esxi50_u1_rel_notes.html):

> L3-routed NFS Storage Access
>
> vSphere 5.0 Update 1 supports L3 routed NFS storage access when you ensure that your environment meets the following conditions:
>
> *   Use Cisco's Hot Standby Router Protocol (HSRP) in IP Router. If you are using non-Cisco router, be sure to use Virtual Router Redundancy Protocol (VRRP) instead.
> *   Use Quality of Service (QoS) to prioritize NFS L3 traffic on networks with limited bandwidths, or on networks that experience congestion. See your router company documentation for details.
> *   Follow Routed NFS L3 best practices recommended by storage vendor. Contact your storage vendor for details.
> *   Disable Network I/O Resource Management (NetIORM)
> *   If you are planning to use systems with top-of-rack switches or switch-dependent I/O device partitioning, contact your system vendor for compatibility and support.
>
> In an L3 environment the following additional restrictions are applicable:
>
> *   The environment does not support VMware Site Recovery Manager.
> *   The environment supports only NFS protocol. Do not use other storage protocols such as FCoE over the same physical network.
> *   The NFS traffic in this environment does not support IPv6.
> *   The NFS traffic in this environment can be routed only over a LAN. Other environments such as WAN are not supported.
> *   The environment does not support Distributed Virtual Switch (DVS).

After we moved the NetApp NAS to be on the same switch as the ESX hosts and changed the IP of the NAS to be on the same subnet as the ESX host, the latency stopped.

