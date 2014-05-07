---
title: What is the difference between a Redo log and a Snapshot?
author: Jarret Lavallee
layout: post
permalink: /2012/09/what-is-the-difference-between-a-redo-log-and-a-snapshot/
dsq_thread_id:
  - 1408510969
categories:
  - VMware
  - vTip
tags:
  - redo logs
  - snapshots
  - vmdk
  - vmfsSparse
---
Most people confuse redo logs with snapshots, but there is a subtle difference in the terminology. If you look at my <a href="http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/']);" title="VMware Snapshot Troubleshooting" target="_blank">previous post about snapshots</a>, it goes into how to identify and troubleshoot snapshots. 

You will see the two words used interchangeabley within vCenter and ESX hosts. Many of the error messages will refer to a snapshot by calling it a redo log. This is from legacy terminology. Back in the <a href="http://www.rtfm-ed.co.uk/docs/vmwdocs/whitepaper-vmware-esx2.x-redo-demystified.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.rtfm-ed.co.uk/docs/vmwdocs/whitepaper-vmware-esx2.x-redo-demystified.pdf']);" target="_blank">ESX 2.x</a> days redo logs were <a href="http://kb.vmware.com/kb/1004458" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1004458']);" target="_blank">essentially snapshots</a>. In the ESX 3.5+ days we call them snapshots. 

If you see errors in vCenter about redo logs, it is likely that you are having problems with snapshots. Some common examples are below.

*   <a href="http://kb.vmware.com/kb/1006585" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1006585']);" target="_blank">msg.hbacommon.corruptredo:The redolog of server1-000001.vmdk has been detected to be corrupt. The virtual machine needs to be powered off. If the problem still persists, you need to discard the redolog</a>
*   <a href="http://kb.vmware.com/kb/1002103" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002103']);" target="_blank">There is no more space for the redo log of server1-000001.vmdk</a>

Redo logs are created when the VM is using <a href="http://www.vspecialist.co.uk/non-persistent-disks-with-vms/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vspecialist.co.uk/non-persistent-disks-with-vms/']);" target="_blank">independent non-persistent disks</a>. With an independent non-persistent disk the changes are not written to disk. So you can run a VM off of a disk, and every time you reset the VM it will revert to the previous state. The question is where are the changes written? We would expect the changes to be written to a snapshot, but this is not the case. A redo log is created to store the changes. 

[code]  
~ # ls -lh \*REDO\*  
-rw\---\---- 1 root root 336.0M Sep 7 06:36 android.vmdk-delta.REDO_TkLU1V  
-rw\---\---- 1 root root 322 Sep 7 06:29 android.vmdk.REDO_TkLU1V  
[/code]

The format is the <a href="http://kb.vmware.com/kb/1026353" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1026353']);" target="_blank">same as a snapshot</a>. Below is the descriptor of the redo log. 

[code]  
~ # cat android.vmdk.REDO_TkLU1V  
\# Disk DescriptorFile  
version=1  
encoding="UTF-8"  
CID=9ab16ab9  
parentCID=c3d4fd75  
isNativeSnapshot="no"  
createType="vmfsSparse"  
parentFileNameHint="android.vmdk"  
\# Extent description  
RW 41943040 VMFSSPARSE "android.vmdk-delta.REDO_TkLU1V"

\# The Disk Data Base  
#DDB

ddb.longContentID = "e6d6c9b8c7164488a10a36b39ab16ab9"  
[/code]

The redo logs are delta disks just like the snapshots.

[code]  
\# ls -lh /dev/deltadisks/  
-rw\---\---- 1 root root 20.0G Sep 7 07:12 1b85f783-android.vmdk-delta.REDO_TkLU1V  
-rw\---\---- 1 root root 20.0G Sep 7 07:12 4c2fd4a3-sql-000002-delta.vmdk  
-rw\---\---- 1 root root 30.0G Sep 7 07:12 699e82ec-sql_1-000002-delta.vmdk  
-r--r--r-- 1 root root 0 Sep 7 07:12 control  
[/code]

So they are essentially the same. The real difference is that redo logs are deleted as a part of the VM being shut down. If a VM with non-persistent disks is powered on and there are redo logs, they will automatically be deleted. If the disks have been changed to persistent, the host will ask if you want to delete or commit the changes in the redo logs. 

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/redo-log-delete.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/redo-log-delete.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/09/redo-log-delete.png" alt="redo log delete What is the difference between a Redo log and a Snapshot?" title="redo log delete confirmation" width="358" height="193" class="aligncenter size-full wp-image-3432" /></a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/09/what-is-the-difference-between-a-redo-log-and-a-snapshot/" title=" What is the difference between a Redo log and a Snapshot?" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:redo logs,snapshots,vmdk,vmfsSparse,blog;button:compact;">Most people confuse redo logs with snapshots, but there is a subtle difference in the terminology. If you look at my previous post about snapshots, it goes into how to...</a>
</p>