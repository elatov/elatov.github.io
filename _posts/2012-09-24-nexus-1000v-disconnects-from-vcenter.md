---
title: Nexus 1000v Disconnects from vCenter
author: Karim Elatov
layout: post
permalink: /2012/09/nexus-1000v-disconnects-from-vcenter/
categories: ['networking', 'vmware']
tags: ['drs', 'nexus_1000v', 'vsm']
---

Looking over the VSM logs (show tech svs), I saw the following:


	2012 Sep 1 21:05:42.599 n1k_vsm %VMS-3-CONNECTION_ERROR: Unable to communicate with vCenter Server/ESX. Disconnecting..
	2012 Sep 1 21:05:42.599 n1k_vsm %VMS-5-CONN_DISCONNECT: Connection 'vcenter' disconnected from the vCenter Server.
	2012 Sep 1 21:06:23 n1k_vsm %LOCAL7-4-SYSTEM_MSG: service ssh, IPV6_ADDRFORM - dcos-xinetd[3775]
	2012 Sep 1 21:06:23 n1k_vsm %AUTH-3-SYSTEM_MSG: error: Could not load host key: /isan/etc/ssh_host_dsa_key - sshd[21319]
	2012 Sep 1 21:06:23.348 n1k_vsm %RADIUS-3-RADIUS_ERROR_MESSAGE: setsockopt success, Using src-intf: for sock 22. Error: Success
	2012 Sep 1 21:08:42.381 n1k_vsm %VMS-5-CONN_CONNECT: Connection 'vcenter' connected to the vCenter Server.
	2012 Sep 1 21:08:45.301 n1k_vsm %MSP-5-DOMAIN_CFG_SYNC_DONE: Domain config successfully pushed to the management server.
	2012 Sep 1 21:08:46.752 n1k_vsm %VMS-5-VMS_PPM_SYNC_COMPLETE: Sync between Port-Profile Manager and local vCenter Server cache complete


So we lost connection for about 3 minutes, but we see that in the mean time there were other log messages. My first hunch was to try to rule out networking, if there were no log messages between the disconnect then I would think it was a resource issue, however that was not the case.

We put the vCenter VM and the N1K VSM on the same host to see what happens. As soon as we did that the disconnects stopped. That right away told me that it's an external networking issue. The customer actually didn't want to deal with his networking team, so we setup DRS VM-To-VM Affinity rules to ensure that these two VMs always stayed together and all was well.

