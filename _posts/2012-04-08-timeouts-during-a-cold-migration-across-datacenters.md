---
title: Timeouts During a Cold Migration Across Datacenters
author: Karim Elatov
layout: post
permalink: /2012/04/timeouts-during-a-cold-migration-across-datacenters/
dsq_thread_id:
  - 1406848402
categories:
  - Networking
  - VMware
tags:
  - NFC
  - ROBO
  - VEEAM FastSCP
  - VMware Converter
  - WAN
---
I had a customer trying to cold migrate a VM across datacenters (across a WAN connection). Probably not the best setup, but it should work. Here is good white paper that talks about vCenter in WAN environments: ![Two_ESX_Connected_With_WAN](https://github.com/elatov/uploads/raw/master/2012/03/Two_ESX_Connected_With_WAN.jpg)
Both of the hosts are managed by the same vCenter server. So we are trying to move the VM from ESX_1 to ESX_2. I definitely agree that there are much better solutions and here is a great tech paper that talks about some of the alternatives: [Data Migrations Techniques for VMware vSphere](http://www.emc.com/collateral/software/white-papers/h8063-data-migration-vsphere-wp.pdf), but we were just stuck with this setup for now.
Whenever we tried to cold migrate, we would see the following in the vpxa logs (/var/log/vmware/vpx/vpxa.log in ESX 4.x or /var/log/vpxa.log in ESXi 5.0) of the source host:


	2012-03-14 16:31:45.288 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcNetTcpWrite: bWritten: -1
	[2012-03-14 16:31:45.288 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcNet_Send: requested 262040, sent only -1 bytes
	[2012-03-14 16:31:45.288 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcFile_SendMessage: data send failed:
	[2012-03-14 16:31:45.288 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcBuf_Send: failed to send next file portion
	[2012-03-14 16:31:45.288 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] Nfc_PutFile: failed to send the buffer
	[2012-03-14 16:31:45.324 1C69CB90 error 'App' opID=C65743A5-0000024D-5c] [VpxNfcClient] File transfer  failed:
	[2012-03-14 16:31:45.324 1C69CB90 verbose 'App' opID=C65743A5-0000024D-5c] [VpxNfcClient] Closing NFC connection to server
	[2012-03-14 16:31:45.324 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcNetTcpWrite: bWritten: -1
	[2012-03-14 16:31:45.324 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcNet_Send: requested 264, sent only -1 bytes
	[2012-03-14 16:31:45.324 1C69CB90 warning 'Libs' opID=C65743A5-0000024D-5c] [NFC ERROR] NfcSendMessage: send failed:
	[2012-03-14 16:31:45.325 1C69CB90 verbose 'PropertyProvider' opID=C65743A5-0000024D-5c] RecordOp ASSIGN: info.state, task-10646
	[2012-03-14 16:31:45.325 1C69CB90 verbose 'PropertyProvider' opID=C65743A5-0000024D-5c] RecordOp ASSIGN: info.cancelable, task-10646


We see a lot of Network File Copy (NFC) errors, NFC is the protocol used to transfer files between hosts when using the management agents. We see from the logs that we are unable to receive the expected data. NFC is a really sensitive protocol and any packet loss would cause the NFC process to time-out.

After further investigation it turned out that the network provider switches were experiencing high packet loss. After updating the network equipment, the packet loss stopped and the cold migrations were able to succeed without any issues.

If you are unable to get into the network provider switches or it's too much of a hassle, some temporary workarounds could be:

1.  VMware Converter - VMware communities [1247172](http://communities.vmware.com/message/1247172)
2.  [Veeam FastSCP](http://www.veeam.com/vmware-esxi-fastscp.html)
3.  SSH with gunzip - [VMworld presentation](http://download3.vmware.com/vmworld/2006/mdc9586.pdf)

I would, of course, recommend fixing the issue upstream, because moving VMDKs manually (workarounds #2 and #3) could possibly cause other issues, but the above workarounds will get the files across without any time-out issues.

