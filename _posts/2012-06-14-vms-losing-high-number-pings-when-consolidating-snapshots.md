---
title: VMs Losing High Number of Pings When Consolidating Snapshots
author: Karim Elatov
layout: post
permalink: /2012/06/vms-losing-high-number-pings-when-consolidating-snapshots/
dsq_thread_id:
  - 1407445607
categories:
  - Storage
  - VMware
tags:
  - CBT
  - Change Block Tracking
  - EqualLogic PS4100X
  - IOMeter
  - Snapshot Consolidation
  - snapshots
  - Unstun Time
---
I had an interesting issue that took a while to solve. Whenever we consolidated snapshots it would take a while and the VM would lose a high number of pings. Some ping loss is okay and is expected since we are stunning the VM during the commit of the snapshot. More information on snapshot consolidation can be found in VMware KB <a href="http://kb.vmware.com/kb/1002836" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002836']);">1002836</a>.  However an excessive amount of ping loss should not be seen. Looking over the vmware.log file of the VM we saw the following messages:

	  
	2012-03-23T16:22:51.876Z| vcpu-0| Checkpoint_Unstun: vm stopped for 3658889 us  
	

That is the time it took for the VM to unstun. Looking over the history of VM and taking a look at how long some other unstun times looked like, we saw the following:

	  
	$ grep Unstun vmware* | awk '{print $7}' | sort -nr | head  
	237087978  
	236039834  
	206802872  
	187750987  
	184177029  
	183631162  
	179726671  
	178677816  
	177677873  
	175575889  
	

It looks like some snapshots took 237 seconds (237087978us) to unstun, that is a pretty long time. I asked the customer to test some other settings while doing a snapshot removal (disable cbt, no vmware tools, and local storage vs shared storage). Here is a table of our results:

<table border="0">
  <tr>
    <td align="center" valign="middle">
    </td>
    
    <th colspan="4" align="center" valign="middle">
      With VMware Tools
    </th>
    
    <th colspan="4" align="center" valign="middle">
      Without VMware Tools
    </th>
  </tr>
  
  <tr align="center">
    <td>
    </td>
    
    <td colspan="2" align="center">
      Without CBT
    </td>
    
    <td colspan="2" align="center">
      With CBT
    </td>
    
    <td colspan="2" align="center">
      Without CBT
    </td>
    
    <td colspan="2" align="center">
      With CBT
    </td>
  </tr>
  
  <tr align="center">
    <td>
    </td>
    
    <td align="center">
      No_I/O
    </td>
    
    <td align="center">
      I/O
    </td>
    
    <td align="center">
      No_I/O
    </td>
    
    <td align="center">
      I/O
    </td>
    
    <td align="center">
      No_I/O
    </td>
    
    <td align="center">
      I/O
    </td>
    
    <td align="center">
      No_I/O
    </td>
    
    <td align="center">
      I/O
    </td>
  </tr>
  
  <tr>
    <td>
      SAN
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
  </tr>
  
  <tr>
    <td>
      Create_Snapshot
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
      2
    </td>
    
    <td>
      2
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
      2
    </td>
    
    <td>
      2
    </td>
  </tr>
  
  <tr>
    <td>
      Remove_Snapshot
    </td>
    
    <td>
    </td>
    
    <td>
      4
    </td>
    
    <td>
      4
    </td>
    
    <td>
      7
    </td>
    
    <td>
      1
    </td>
    
    <td>
      5
    </td>
    
    <td>
      4
    </td>
    
    <td>
      7
    </td>
  </tr>
  
  <tr>
    <td>
      Local
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
  </tr>
  
  <tr>
    <td>
      Create_Snapshot
    </td>
    
    <td>
    </td>
    
    <td>
    </td>
    
    <td>
      1
    </td>
    
    <td>
      1
    </td>
    
    <td>
       0
    </td>
    
    <td>
       1
    </td>
    
    <td>
      1
    </td>
    
    <td>
       1
    </td>
  </tr>
  
  <tr>
    <td>
      Remove_Snapshot
    </td>
    
    <td>
    </td>
    
    <td>
      1
    </td>
    
    <td>
       0
    </td>
    
    <td>
      3
    </td>
    
    <td>
      1
    </td>
    
    <td>
       3
    </td>
    
    <td>
       1
    </td>
    
    <td>
       3
    </td>
  </tr>
</table>

VMware tools didn&#8217;t make a difference, CBT did make a difference but that is expected. Doing I/O inside the VM also made a difference, this was expected as well. The most important data point was the fact that with Local storage it was actually working as expected while on the SAN it was not. Next we decided to run IOmeter tests between the two storage types, and here are the results:

<table border="0" frame="VOID" rules="NONE" cellspacing="0">
  <tr align="center" valign="middle">
    <th align="center" valign="middle">
    </th>
    
    <th align="center" valign="middle">
      Test_Type
    </th>
    
    <th align="center" valign="middle">
      Read_IOPS
    </th>
    
    <th align="center" valign="middle">
      Read_MB
    </th>
    
    <th align="center" valign="middle">
      Avg_Read_Resp
    </th>
    
    <th align="center" valign="middle">
      Write_IOPs
    </th>
    
    <th align="center" valign="middle">
      Write_MB
    </th>
    
    <th align="center" valign="middle">
      Avg_Write_Resp
    </th>
  </tr><colgroup> <col width="100" /> <col width="117" /> <col width="83" /> <col width="71" /> <col width="141" /> <col width="82" /> <col width="73" /> <col width="142" /></colgroup> 
  
  <tr>
    <td align="LEFT" height="17">
      SAN
    </td>
    
    <td align="LEFT">
      4K_100%_Read
    </td>
    
    <td align="RIGHT">
      6125
    </td>
    
    <td align="RIGHT">
      23
    </td>
    
    <td align="RIGHT">
      5.22
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      Local
    </td>
    
    <td align="LEFT">
      4K_100%_Read
    </td>
    
    <td align="RIGHT">
      7754
    </td>
    
    <td align="RIGHT">
      30
    </td>
    
    <td align="RIGHT">
      4.12
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      SAN
    </td>
    
    <td align="LEFT">
      4K_0%_Read
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
      8258
    </td>
    
    <td align="RIGHT">
      32
    </td>
    
    <td align="RIGHT">
      3.8
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      Local
    </td>
    
    <td align="LEFT">
      4K_0%_Read
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
      30337
    </td>
    
    <td align="RIGHT">
      118
    </td>
    
    <td align="RIGHT">
      1.05
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      SAN
    </td>
    
    <td align="LEFT">
      16K_100%_Read
    </td>
    
    <td align="RIGHT">
      5214
    </td>
    
    <td align="RIGHT">
      81
    </td>
    
    <td align="RIGHT">
      6.13
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      Local
    </td>
    
    <td align="LEFT">
      16K_100%_Read
    </td>
    
    <td align="RIGHT">
      21885
    </td>
    
    <td align="RIGHT">
      341
    </td>
    
    <td align="RIGHT">
      1.46
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      SAN
    </td>
    
    <td align="LEFT">
      16K_0%_Read
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
      5100
    </td>
    
    <td align="RIGHT">
      79
    </td>
    
    <td align="RIGHT">
      6.27
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      Local
    </td>
    
    <td align="LEFT">
      16K_0%_Read
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
      7889
    </td>
    
    <td align="RIGHT">
      123
    </td>
    
    <td align="RIGHT">
      4.05
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      SAN
    </td>
    
    <td align="LEFT">
      32K_100%_Read
    </td>
    
    <td align="RIGHT">
      3469
    </td>
    
    <td align="RIGHT">
      108
    </td>
    
    <td align="RIGHT">
      9.22
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      Local
    </td>
    
    <td align="LEFT">
      32K_100%_Read
    </td>
    
    <td align="RIGHT">
      15789
    </td>
    
    <td align="RIGHT">
      493
    </td>
    
    <td align="RIGHT">
      2.02
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      SAN
    </td>
    
    <td align="LEFT">
      32K_0%_Read
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
      3195
    </td>
    
    <td align="RIGHT">
      99
    </td>
    
    <td align="RIGHT">
      10.01
    </td>
  </tr>
  
  <tr>
    <td align="LEFT" height="17">
      Local
    </td>
    
    <td align="LEFT">
      32K_0%_Read
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
    </td>
    
    <td align="RIGHT">
      4054
    </td>
    
    <td align="RIGHT">
      126
    </td>
    
    <td align="RIGHT">
      7.89
    </td>
  </tr>
</table>

Local Storage was out performing the SAN in every single test. We were using an Equallogic PS4100X Array, so we went ahead and engaged Dell and provided them with the diagnostics from the Array. After analyzing the logs, Dell provided us with the following update:

> After performing a deep analysis on the diags you provided, we have discovered the following. EQL SAN-2 is the group lead and is down to 1.5 % of pool space. EQL SAN-1 currently has 46.4% of free space. We are also not showing any snapshots or replicas on these members. At your earliest convenience, we would like to incorporate the action plan below.
> 
> 1.  We would like to do a restart on the grouplead (EQL SAN-2), to fail it over to EQL SAN-1.
> 2.  Once this is completed, then free up any space possible on EQL SAN2.
> 3.  After this, we recommend upgrading the arrays firmware to 5.2.2
> 4.  Also please upgrade ESXi 5.0.0 version to build number 653509.

After we applied all the above changes the snapshot consolidation looked much better. The customer sent me a log bundle after the above changes were applied and I saw the following:

	  
	2012-05-14T13:34:34.351Z| vcpu-0| DISKLIB-CBT : Shutting down change tracking for untracked fid 5277995.  
	2012-05-14T13:34:34.351Z| vcpu-0| DISKLIB-CBT : Successfully disconnected CBT node.  
	2012-05-14T13:34:34.366Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738354b180373f5105d/VM/VM_1-000002-delta.vmdk" : closed.  
	2012-05-14T13:34:34.368Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738-354b180373f5105d/VM/VM_1-flat.vmdk" : closed.  
	2012-05-14T13:34:34.377Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738-354b180373f5105d/VM/VM_1-000002-delta.vmdk" : open successful (1041) size = 34992128, hd = 0. Type 8  
	2012-05-14T13:34:34.377Z| vcpu-0| DISKLIB-LIB : Resuming change tracking.  
	2012-05-14T13:34:34.390Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4ecad5e9-a50e5738-354b180373f5105d/VM/VM_1-000002-delta.vmdk" : closed.  
	2012-05-14T13:34:34.412Z| vcpu-0| CPT current = 2, requesting 6  
	2012-05-14T13:34:34.412Z| vcpu-0| Checkpoint_Unstun: vm stopped for 4233332 us  
	2012-05-14T13:34:34.412Z| vcpu-1| Done Sync monModules(6).  
	2012-05-14T13:34:34.412Z| vcpu-0| Done Sync monModules(6).  
	2012-05-14T13:34:34.412Z| vcpu-0| CPT: monitor ACKing mode 6  
	

So the snapshot did happen and the unstun took 4 seconds, which was much better than ~230 seconds and is expected with active I/O and Change Block Tracking enabled.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Check if Snapshot Consolidation is Occurring in the Background on an ESX(i) Host" href="http://virtuallyhyper.com/2012/09/check-if-snapshot-consolidation-is-occurring-in-the-background/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/check-if-snapshot-consolidation-is-occurring-in-the-background/']);" rel="bookmark">Check if Snapshot Consolidation is Occurring in the Background on an ESX(i) Host</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/06/vms-losing-high-number-pings-when-consolidating-snapshots/" title=" VMs Losing High Number of Pings When Consolidating Snapshots" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:CBT,Change Block Tracking,EqualLogic PS4100X,IOMeter,Snapshot Consolidation,snapshots,Unstun Time,blog;button:compact;">Someone had asked me recently: What happens if the snapshot consolidation process take a long time and the task is no longer seen in the vShpere client? First I would...</a>
</p>