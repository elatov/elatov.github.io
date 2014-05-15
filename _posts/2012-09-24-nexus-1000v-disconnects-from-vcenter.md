---
title: Nexus 1000v Disconnects from vCenter
author: Karim Elatov
layout: post
permalink: /2012/09/nexus-1000v-disconnects-from-vcenter/
dsq_thread_id:
  - 1407505965
categories:
  - Networking
  - VMware
  - vTip
tags:
  - DRS VM-to-VM Affinity
  - Nexus 1000v
  - VSM_CONN_DISCONNECT
---
Looking over the VSM logs (show tech svs), I saw the following:

	  
	2012 Sep 1 21:05:42.599 n1k\_vsm %VMS-3-CONNECTION\_ERROR: Unable to communicate with vCenter Server/ESX. Disconnecting..  
	2012 Sep 1 21:05:42.599 n1k\_vsm %VMS-5-CONN\_DISCONNECT: Connection 'vcenter' disconnected from the vCenter Server.  
	2012 Sep 1 21:06:23 n1k\_vsm %LOCAL7-4-SYSTEM\_MSG: service ssh, IPV6_ADDRFORM - dcos-xinetd[3775]  
	2012 Sep 1 21:06:23 n1k\_vsm %AUTH-3-SYSTEM\_MSG: error: Could not load host key: /isan/etc/ssh\_host\_dsa_key - sshd[21319]  
	2012 Sep 1 21:06:23.348 n1k\_vsm %RADIUS-3-RADIUS\_ERROR_MESSAGE: setsockopt success, Using src-intf: for sock 22. Error: Success  
	2012 Sep 1 21:08:42.381 n1k\_vsm %VMS-5-CONN\_CONNECT: Connection 'vcenter' connected to the vCenter Server.  
	2012 Sep 1 21:08:45.301 n1k\_vsm %MSP-5-DOMAIN\_CFG\_SYNC\_DONE: Domain config successfully pushed to the management server.  
	2012 Sep 1 21:08:46.752 n1k\_vsm %VMS-5-VMS\_PPM\_SYNC\_COMPLETE: Sync between Port-Profile Manager and local vCenter Server cache complete  
	

So we lost connection for about 3 minutes, but we see that in the mean time there were other log messages. My first hunch was to try to rule out networking, if there were no log messages between the disconnect then I would think it was a resource issue, however that was not the case.

We put the vCenter VM and the N1K VSM on the same host to see what happens. As soon as we did that the disconnects stopped. That right away told me that it's an external networking issue. The customer actually didn't want to deal with his networking team, so we setup DRS VM-To-VM Affinity rules to ensure that these two VMs always stayed together and all was well.

