---
title: Lost NFS Connectivity from ESX(i) Host when NAS is Another Subnet
author: Karim Elatov
layout: post
permalink: /2012/11/lost-nfs-connectivity-from-esxi-host-when-nas-is-another-subnet/
dsq_thread_id:
  - 1406624842
categories:
  - Networking
  - Storage
  - VMware
tags:
  - esxcfg-nas
  - esxcfg-route
  - nfs
  - NFS Disconnect
  - RPC error 13
  - static route
---
All of a sudden on my ESXi host we saw a disconnect from our NAS. I saw the following in the logs:

	  
	Nov 8 10:10:53 vmkernel: O:O1:19:58.809 cpu10:4922)WARNING: NFS: 898: RPC error 13 (RPC was aborted due to timeout) trying to get port for Mount Program (100005) Version (3) Protocol (TCP) on Server (10.178.250.10)  
	

So the IP of my NAS was 10.178.250.10, here is the NAS information from the host:

	  
	~ # esxcfg-nas -l  
	NAS_1 is /vol/data1 from 10.178.250.10  
	

Now checking over our vmkernel interfaces, I saw the following:

	  
	~ # esxcfg-vmknic -l  
	Interface Port Group/DVPort IP Address Netmask Broadcast MAC Address MTU Enabled  
	vmkO Management Network 10.178.47.98 255.255.255.128 10.178.47.127 OO:26:55:3J:69:52 1500 true  
	vmk1 NFS 10.178.46.6 255.255.255.240 10.178.46.15 OO:50:56:Jd:03:Od 1500 true  
	

Then checking over the routes on the hosts, I saw the following:

	  
	~ # esxcfg-route -l  
	VMkernel Routes:  
	Network Network Gateway  
	1O.178.46.O 255.255.255.240 Local Subnet  
	1O.178.47.O 255.255.255.128 Local Subnet  
	default O.O.O.O 10.178.47.1  
	

So the intent is to connect through vmk1 (our NFS interface, 10.178.46.6). Since our NAS is on a different subnet (10.178.250.10) from the NFS and management interfaces, we will use the default gateway (10.178.47.1) to connect to it. Also, since our management interface (10.178.47.98) is on the same subnet as the default gateway (10.178.47.1), we will actually use that interface to connect to the NAS (10.178.250.10). Recently the Storage team added some more security and only allowed the NFS interface (10.178.46.6) to connect to it. That is why our NFS disconnected. 

Luckily there was another default gateway where the NFS interface resided. That IP was 10.178.46.1. So what we could do is add a static route, and when we connect to the 10.178.250.10 (NAS) network, we should go through the 10.178.46.1 gateway. Here is what we ran to accomplish that:

	  
	~ # esxcfg-route -a 10.178.250.0/24 10.178.46.1  
	Adding static route 10.178.250.0/24 to VMkernel  
	

After I ran the above, I saw the following in the logs:

	  
	Nov 8 10:45:19 vmkernel: O:O1:54:24.995 cpu3:42254)Tcpip_Socket: 1087: add dstAddr=Oxfab20a, netMask=Oxffffff, gwAddr=O12eb20a8 ifName=OxO, ifNameLen=O  
	Nov 8 10:45:27 vmkernel: O:O1:54:32.538 cpu7:4922)NFS: 286: Restored connection to server 10.178.250.10 mount point /vol/data1, mounted as a20f9958-58eaf9ec-0000-000000000 ("NFS_1")  
	

Also saw the following output:

	  
	~ # esxcfg-nas -l  
	NAS_1 is /vol/data1 from 10.178.250.10 mounted  
	

Notice the &#8220;mounted&#8221; field is showing up now. Here is how the routing table looked like on the ESXi host, after the addition of the static route:

	  
	~ # esxcfg-route -l  
	VMkernel Routes:  
	Network Network Gateway  
	1O.178.46.O 255.255.255.240 Local Subnet  
	1O.178.47.O 255.255.255.128 Local Subnet  
	1O.178.250.O 255.255.255.O 10.178.46.1  
	default O.O.O.O 10.178.47.1  
	

So here is how the network looked like:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/11/static_route_example.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/11/static_route_example.jpg']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/11/static_route_example.jpg" alt="static route example Lost NFS Connectivity from ESX(i) Host when NAS is Another Subnet" title="static_route_example" width="972" height="560" class="alignnone size-full wp-image-4989" /></a>

In the beginning we were connecting through the top switch (mgmt\_switch) and since the new security in place, we couldn&#8217;t go that way. After we added the static route, we were connecting through the bottom switch (NFS\_Switch) and that is the way it&#8217;s supposed to be. I realize the setup is not the best, and the best way to fix this would be to put the NAS server on the same network (10.178.46.x) as the NFS interface (for performance and security reasons) but some times the physical setup is outside of our control.

<p class="wp-flattr-button">
	  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/11/lost-nfs-connectivity-from-esxi-host-when-nas-is-another-subnet/" title=" Lost NFS Connectivity from ESX(i) Host when NAS is Another Subnet" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:esxcfg-nas,esxcfg-route,nfs,NFS Disconnect,RPC error 13,static route,blog;button:compact;">All of a sudden on my ESXi host we saw a disconnect from our NAS. I saw the following in the logs:  Nov 8 10:10:53 vmkernel: O:O1:19:58.809 cpu10:4922)WARNING: NFS:...</a>
	</p>