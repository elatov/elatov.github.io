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
I had a customer trying to cold migrate a VM across datacenters (across a WAN connection). Probably not the best setup, but it should work. Here is good white paper that talks about vCenter in WAN environments: <a href="http://www.vmware.com/files/pdf/techpaper/VMW-WP-Performance-vCenter.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/VMW-WP-Performance-vCenter.pdf']);">Performance of VMware vCenter  Operations in a ROBO Environment</a> and here is a good vmware communities page that talks about similar topics: <a href="http://communities.vmware.com/docs/DOC-11492" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-11492']);">Proven Practice: ROBO - Managing Remote ESX Hosts Over WAN with VirtualCenter</a>. Now the flow of traffic looks something like the following:<a href="http://virtuallyhyper.com/wp-content/uploads/2012/03/Two_ESX_Connected_With_WAN.jpg" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/03/Two_ESX_Connected_With_WAN.jpg']);"><img class="alignnone size-full wp-image-554" title="Two_ESX_Connected_With_WAN" src="http://virtuallyhyper.com/wp-content/uploads/2012/03/Two_ESX_Connected_With_WAN.jpg" alt="Two ESX Connected With WAN Timeouts During a Cold Migration Across Datacenters" width="912" height="170" /></a>  
Both of the hosts are managed by the same vCenter server. So we are trying to move the VM from ESX_1 to ESX_2. I definitely agree that there are much better solutions and here is a great tech paper that talks about some of the alternatives: <a href="http://www.emc.com/collateral/software/white-papers/h8063-data-migration-vsphere-wp.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.emc.com/collateral/software/white-papers/h8063-data-migration-vsphere-wp.pdf']);">Data Migrations Techniques for VMware vSphere</a>, but we were just stuck with this setup for now.  
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

1.  <span style="line-height: 22px;">VMware Converter (VMware communities <a href="http://communities.vmware.com/message/1247172" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/message/1247172']);">1247172</a>)</span>
2.  <span style="line-height: 22px;">Veeam FastSCP (Veeam Communites <a href="http://forums.veeam.com/viewtopic.php?f=4&t=9500" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://forums.veeam.com/viewtopic.php?f=4&t=9500']);">9500</a>)</span>
3.  <span style="line-height: 22px;">SSH with gunzip (<a href="http://download3.vmware.com/vmworld/2006/mdc9586.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://download3.vmware.com/vmworld/2006/mdc9586.pdf']);">VMworld presentation</a>)</span>

I would, of course, recommend fixing the issue upstream, because moving VMDKs manually (workarounds #2 and #3) could possibly cause other issues, but the above workarounds will get the files across without any time-out issues.

