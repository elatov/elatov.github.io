---
title: VMs are Experiencing High Latency to NetApp FAS 6240
author: Karim Elatov
layout: post
permalink: /2012/06/vms-experiencing-high-latency-netapp-fas-6270/
dsq_thread_id:
  - 1406371674
categories:
  - Networking
  - Storage
  - VMware
tags:
  - ESX 5.0U1
  - GAVG
  - L3 NFS
  - Latency
  - NetApp 6240
  - nfs
---
I was recently presented with the following environment:

<table border="0">
  <tr>
    <td>
      VMware ESX
    </td>
    
    <td>
      NetAPP
    </td>
  </tr>
  
  <tr>
    <td>
      ESX 4.1P03
    </td>
    
    <td>
      FAS 6240
    </td>
  </tr>
</table>

With this setup all the VMs from the ESX that resided on the NFS Datastores exported from the NetApp Array were experiencing high GAVG. Since this is NFS we don&#8217;t have DAVG or KAVG statistics. Looking at esxtop, this is what we saw:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/06/nfs_ds_latency_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/06/nfs_ds_latency_1.png']);"><img class="alignnone size-full wp-image-1717" title="nfs_ds_latency_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/06/nfs_ds_latency_1.png" alt="nfs ds latency 1 VMs are Experiencing High Latency to NetApp FAS 6240" width="1268" height="404" /></a>

Notice the GAVG for the to NFS datastore is ~25ms. We would consistently see 20-40ms of latency to array. Looking at the VM&#8217;s latency, we saw similar numbers:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/06/nfs_vm_latency_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/06/nfs_vm_latency_1.png']);"><img class="alignnone size-full wp-image-1716" title="nfs_vm_latency_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/06/nfs_vm_latency_1.png" alt="nfs vm latency 1 VMs are Experiencing High Latency to NetApp FAS 6240" width="980" height="188" /></a>

Looks like the VMs are experiencing Write Latency to the NetApp Array. Looking over the network configuation of the ESX host I saw the following:

	  
	$ esxcfg-vmknic -l  
	Interface Port Group/DVPort IP Family IP Address Netmask Broadcast MAC Address MTU TSO MSS Enabled Type  
	vmk0 89 IPv4 10.195.x.22 255.255.255.0 10.195.x.255 00:50:56:78:bf:60 1500 65535 true STATIC  
	vmk1 13 IPv4 10.205.x.22 255.255.255.0 10.205.x.255 00:50:56:70:d4:32 1500 65535 true STATIC  
	

Looking at the NAS connections, I saw the following:

	  
	$ esxcfg-nas -l  
	export\_1 is /vol/export\_1 from 10.204.x.29 mounted  
	export\_2 is /vol/export\_2 from 10.204.x.29 mounted  
	export\_3 is /vol/export\_3 from 10.204.x.30 mounted  
	export\_4 is /vol/export\_4 from 10.204.x.30 mounted  
	...  
	...  
	

The first thing that stood out was the fact that the vmkernel interface used for the NFS connection (10.205.x.22) was not on the same subnet as the NAS itself (10.204.x.29).  
I wanted to see what the network topology looked like, and it was something like this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/06/ESX-to-NetApp_L3.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/06/ESX-to-NetApp_L3.jpg']);"><img class="alignnone size-full wp-image-1719" title="ESX-to-NetApp_L3" src="http://virtuallyhyper.com/wp-content/uploads/2012/06/ESX-to-NetApp_L3.jpg" alt="ESX to NetApp L3 VMs are Experiencing High Latency to NetApp FAS 6240" width="983" height="275" /></a>

Layer 3 NFS is not supported with ESX until ESX 5.0U1. From the <a href="https://www.vmware.com/support/vsphere5/doc/vsp_esxi50_u1_rel_notes.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/vsphere5/doc/vsp_esxi50_u1_rel_notes.html']);">Release Notes of 5.0U1</a>:

> L3-routed NFS Storage Access
> 
> vSphere 5.0 Update 1 supports L3 routed NFS storage access when you ensure that your environment meets the following conditions:
> 
> *   Use Cisco&#8217;s Hot Standby Router Protocol (HSRP) in IP Router. If you are using non-Cisco router, be sure to use Virtual Router Redundancy Protocol (VRRP) instead.
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

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/06/vms-experiencing-high-latency-netapp-fas-6270/" title=" VMs are Experiencing High Latency to NetApp FAS 6240" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:ESX 5.0U1,GAVG,L3 NFS,Latency,NetApp 6240,nfs,blog;button:compact;">I was recently presented with the following environment: VMware ESX NetAPP ESX 4.1P03 FAS 6240 With this setup all the VMs from the ESX that resided on the NFS Datastores...</a>
</p>