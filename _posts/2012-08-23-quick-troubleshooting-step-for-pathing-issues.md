---
title: Quick Troubleshooting Step for Pathing Issues
author: Karim Elatov
layout: post
permalink: /2012/08/quick-troubleshooting-step-for-pathing-issues/
dsq_thread_id:
  - 1405582137
categories:
  - Home Lab
  - Storage
  - VMware
  - vTip
tags:
  - disable path
  - Disk.PathEvalTime
  - esxcfg-mpath
  - esxcfg-rescan
  - H:0x8
  - TUR
---
I was having weird issues in our lab. When IO was going down one HBA, all was well, but when it went down the other path, it was very intermittent. Here is how the pathing looked like for one of the LUNs:

	  
	~ # esxcfg-mpath -b -d naa.60a9800064655a77524a6c4938685950  
	naa.60a9800064655a77524a6c4938685950 : NETAPP Fibre Channel Disk (naa.60a9800064655a77524a6c4938685950)  
	vmhba1:C0:T1:L1 LUN:1 state:active fc Adapter: WWNN: 20:01:00:25:b5:00:00:0d WWPN: 20:00:00:25:b5:0a:00:0d Target: WWNN: 50:0a:09:80:8f:3f:52:ad WWPN: 50:0a:09:82:9f:3f:52:ad  
	vmhba1:C0:T2:L1 LUN:1 state:active fc Adapter: WWNN: 20:01:00:25:b5:00:00:0d WWPN: 20:00:00:25:b5:0a:00:0d Target: WWNN: 50:0a:09:80:8f:3f:52:ad WWPN: 50:0a:09:82:8f:3f:52:ad  
	vmhba2:C0:T1:L1 LUN:1 state:active fc Adapter: WWNN: 20:01:00:25:b5:00:00:0d WWPN: 20:00:00:25:b5:0b:00:0d Target: WWNN: 50:0a:09:80:8f:3f:52:ad WWPN: 50:0a:09:81:9f:3f:52:ad  
	vmhba2:C0:T2:L1 LUN:1 state:active fc Adapter: WWNN: 20:01:00:25:b5:00:00:0d WWPN: 20:00:00:25:b5:0b:00:0d Target: WWNN: 50:0a:09:80:8f:3f:52:ad WWPN: 50:0a:09:81:8f:3f:52:ad  
	

We have two HBAs and two paths from each HBAs coming to a grand total of 4 paths per LUN. I wanted to see how the rescan times compared between the two HBAs:

	  
	~ # time esxcfg-rescan vmhba1  
	real 0m 1.90s  
	user 0m 0.07s  
	sys 0m 0.00s
	
	~ # time esxcfg-rescan vmhba2  
	real 2m 21.39s  
	user 0m 0.07s  
	sys 0m 0.00s  
	

As the second rescan was going, I saw the following in the logs:

	  
	2010-10-30T02:20:55.012Z cpu12:4290)<6>qla2xxx 0000:04:00.1: scsi(3:1:1): Abort command succeeded -- 1 29950.  
	2010-10-30T02:20:55.013Z cpu14:4110)NMP: nmp_ThrottleLogForDevice:2318: Cmd 0x28 (0x412441199080) to dev "naa.60a9800064655a77524a6c4938685950" on path "vmhba2:C0:T1:L1" Failed: H:0x8 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.Act:EVAL  
	2010-10-30T02:20:55.013Z cpu14:4110)WARNING: NMP: nmp_DeviceRequestFastDeviceProbe:237:NMP device "naa.60a9800064655a77524a6c4938685950" state in doubt; requested fast path state update...  
	

Notice how long the second rescan was. It was much longer than the first one, and I saw that we were having communication issues with device &#8220;naa.60a9800064655a77524a6c4938685950&#8243; over the path &#8220;vmhba2:C0:T1:L1&#8243;. 

The first message indicates that the command was aborted for scsi(3:1:1), which translates to LUN 1:

	  
	2010-10-30T02:20:55.012Z cpu12:4290)<6>qla2xxx 0000:04:00.1: scsi(3:1:1): Abort command succeeded -- 1 29950.  
	

The second line, is the vmkernel noticing that a command aborted, specifically command 0&#215;28, which is a 10 byte READ command. 

	  
	2010-10-30T02:20:55.013Z cpu14:4110)NMP: nmp_ThrottleLogForDevice:2318: Cmd 0x28 (0x412441199080) to dev "naa.60a9800064655a77524a6c4938685950" on path "vmhba2:C0:T1:L1" Failed: H:0x8 D:0x0 P:0x0 Possible sense data: 0x0 0x0 0x0.Act:EVAL  
	

The NMP (Native Multipath Plugin) returns a Host status of 0&#215;8, which translates to VMK\_SCSI\_HOST_RESET. More information on SCSI Host statuses can be at VMware KB <a href="http://kb.vmware.com/kb/1029039" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1029039']);">1029039</a>. From that KB:

> VMK\_SCSI\_HOST_RESET = 0&#215;08 or 0&#215;8
> 
> This status is returned when the HBA driver has aborted the I/O. It can also occur if the HBA does a reset of the target.

This makes sense since we aborted the IO. Then the last line:

	  
	2010-10-30T02:20:55.013Z cpu14:4110)WARNING: NMP: nmp_DeviceRequestFastDeviceProbe:237:NMP device "naa.60a9800064655a77524a6c4938685950" state in doubt; requested fast path state update...  
	

When a command is aborted, a TUR (TEST\_UNIT\_READY) command is issued down the path where the command did not complete to ensure that this path is still good to use. More information on path failover be seen in VMware KB <a href="http://kb.vmware.com/kb/1027963" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1027963']);">1027963</a>. 

A TUR is issued every 300 seconds as part of the path evaluation, this behavior can be changed with a variable called &#8220;Disk.PathEvalTime&#8221;, however in our case a TUR is issued immediately due to the aborted command. More information on Disk.PathEvalTime can be seen in VMware KB <a href="http://kb.vmware.com/kb/1004378" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1004378']);">1004378</a>.

So I went ahead and disabled that path since we were having issues sending IO down that path:

	  
	~ # esxcli storage core path set --state off -p vmhba2:C0:T1:L1  
	~ # time esxcfg-rescan vmhba2  
	real 0m 1.35s  
	user 0m 0.07s  
	sys 0m 0.00s  
	

Notice that the rescan time went down and I no longer saw the above messages. From this point I would track down the path and see where the issue exists but this is just a quick troubleshooting step to see if a path is causing issues.

