---
title: 'Advanced Snapshot Troubleshooting: Missing VMDK Descriptors'
author: Jarret Lavallee
layout: post
permalink: /2012/04/advanced-snapshot-troubleshooting-missing-vmdk-descriptors/
dsq_thread_id:
  - 1404809475
categories:
  - Storage
  - VMware
tags:
  - clone
  - command line
  - failed to open parent
  - snapshots
  - troubleshooting
  - vmdk
  - vmkfstools
---
A common problem with snapshots is missing descriptors. If you have been following this series of <a title="VMware Snapshot Troubleshooting" href="http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/']);" target="_blank">VMware Snapshot Troubleshooting</a>, we have touched on the descriptor properties. In this article we will go over missing descriptors.

There are some great KB articles on recreating descriptors, so we will not go into detail on doing the recreation. Please see this <a href="http://kb.vmware.com/kb/1026353_draft" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1026353_draft']);" target="_blank">VMware KB</a> for recreating a missing snapshot descriptor and this <a href="http://kb.vmware.com/kb/1002511" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002511']);" target="_blank">VMware KB</a> for recreating a base disk descriptor.

## Identifying Missing VMDK Descriptors

In most cases this is fairly obvious, but it can be a little more difficult to identify if there are many snapshots and a single missing descriptor.

Like the previous articles we will use vmkfstools to identify the missing descriptor.

[bash highlight="6"]# vmkfstools -v 10 -q sql-000005.vmdk  
DISKLIB-VMFS : "./sql-000005-delta.vmdk" : open successful (23) size = 20480, hd = 0. Type 8  
DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk" : open successful (23) size = 20480, hd = 0. Type 8  
DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk" : open successful (23) size = 20480, hd = 0. Type 8  
DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk" : open successful (23) size = 20480, hd = 0. Type 8  
DISKLIB-DSCPTR: DescriptorDetermineType: failed to open &#8216;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001.vmdk&#8217;: Could not find the file (600000003)  
DISKLIB-LINK : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001.vmdk" : failed to open (The system cannot find the file specified).  
DISKLIB-CHAIN :"sql-000005.vmdk": Failed to open parent "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001.vmdk": The system cannot find the file specified.  
DISKLIB-CHAIN : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001.vmdk" : failed to open (The parent of this virtual disk could not be opened).  
DISKLIB-VMFS : "./sql-000005-delta.vmdk" : closed.  
DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk" : closed.  
DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk" : closed.  
DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk" : closed.  
DISKLIB-LIB : Failed to open &#8216;sql-000005.vmdk&#8217; with flags 0&#215;17 The parent of this virtual disk could not be opened (23).  
Failed to open &#8216;sql-000005.vmdk&#8217; : The parent of this virtual disk could not be opened (23).  
[/bash]

In this example we are missing the descriptor for sql-000001-delta.vmdk. Let&#8217;s check to see if it exists.

[bash]# ls sql-000001.vmdk  
ls: sql-000001.vmdk: No such file or directory[/bash]

Since this descriptor is missing, we would need to recreate the descriptor. This would involve copying another snapshot&#8217;s descriptor, filling in the RW value and parentCID/CID and linking it to the delta file.

The descriptor that I recreated for this snapshot is below. The process for recreating the descriptor is in this <a href="http://kb.vmware.com/kb/1026353_draft" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1026353_draft']);" target="_blank">VMware KB</a>.

[bash]# Disk DescriptorFile  
version=1  
encoding="UTF-8"  
CID=cffffffe  
parentCID=dffffffe  
isNativeSnapshot="no"  
createType="vmfsSparse"  
parentFileNameHint="sql.vmdk"  
\# Extent description  
RW 16777216 VMFSSPARSE "sql-000001-delta.vmdk"  
[/bash]

## Recreating Multiple Missing VMDK descriptors

It becomes increasingly difficult when there are multiple VMDKs with missing descriptors. With more missing descriptors, we have more possible snapshot chain possibilities. Normally we would expect to see the snapshots in a numerical order, but if you have read the <a title="Advanced Snapshot Troubleshooting: Non-Linear VMware Snapshot Chain" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/']);" target="_blank">Non-Linear Snapshot Chain</a> post, you know that snapshots do not have to be in numerical order and not all snapshots are in the same chain. This can make recreating the snapshot chain very difficult.

There are a number of techniques that we use to try to recreate the chain. Normally we will use a combination of the strategies below.

### Identifying the Snapshot Chain by Timestamp

It is very important not to change any of the original files. If we modify the original files we can lose data. In this case we will use the timestamps of the snapshot files to identify the snapshot chain. If we had &#8220;touch&#8221;ed any of the files in this directory, we would lose the ability to identify the snapshot chain by this method.

We can look at the timestamps of the delta and flat files and try to determine which order they were last modified. If the parent is modified, it should invalidate the child snapshots, so we can check the timestamps to see the order. The chain would go from the oldest to newest snapshot in chronological order.

In the example below we run &#8220;ls&#8221; with reverse time, so that the most recently modified files are at the bottom. Based on the timestamps we would guess that the chain goes(from parent to child) sql.vmdk -> sql-000002-delta.vmdk -> sql-000001-delta.vmdk -> sql-000003-delta.vmdk -> sql-000004-delta.vmdk. This is the order we would try to create the snapshot chain in the descriptors.

[bash]# ls -lrt sql\*delta.vmdk sql\*flat.vmdk  
-rw&#8212;&#8212;- 1 root root 8589934592 Apr 23 23:21 sql-flat.vmdk  
-rw&#8212;&#8212;- 1 root root 20480 Apr 23 23:22 sql-000002-delta.vmdk  
-rw&#8212;&#8212;- 1 root root 20480 Apr 23 23:23 sql-000001-delta.vmdk  
-rw&#8212;&#8212;- 1 root root 20480 Apr 23 23:24 sql-000003-delta.vmdk  
-rw&#8212;&#8212;- 1 root root 20480 Apr 23 23:25 sql-000004-delta.vmdk  
[/bash]

NOTE: If you have touched the files in this directory, this method will not work because touch will update the access and modification times of the file.

You can get more information about the timestamps with the &#8220;stat&#8221; command.

[bash]# stat sql-flat.vmdk  
File: "sql-flat.vmdk"  
Size: 8589934592 Blocks: 0 IO Block: 131072 regular file  
Device: 74927d2ea26a622ch/8399913894246244908d Inode: 100683076 Links: 1  
Access: (0600/-rw&#8212;&#8212;-) Uid: ( 0/ root) Gid: ( 0/ root)  
Access: 2012-04-23 23:22:56.000000000  
Modify: 2012-04-23 23:21:33.000000000  
Change: 2012-04-23 23:21:33.000000000  
[/bash]

### Identifying the Snapshot Chain by the VMSD file

We previously talked about the VMSD file, which keeps track of the snapshot chain. Since we are missing the descriptors, we can use this file to get an idea of what the chain should be.

Let&#8217;s take a look at a VMSD.

[bash]# cat sql.vmsd  
.encoding = "UTF-8"  
snapshot.lastUID = "18"  
snapshot.current = "18"  
snapshot0.uid = "15"  
snapshot0.filename = "sql-Snapshot15.vmsn"  
snapshot0.displayName = "sad"  
snapshot0.createTimeHigh = "310880"  
snapshot0.createTimeLow = "-365210110"  
snapshot0.numDisks = "1"  
snapshot0.disk0.fileName = "sql.vmdk"  
snapshot0.disk0.node = "scsi0:0"  
snapshot1.uid = "16"  
snapshot1.filename = "sql-Snapshot16.vmsn"  
snapshot1.parent = "15"  
snapshot1.displayName = "aksdn"  
snapshot1.createTimeHigh = "310880"  
snapshot1.createTimeLow = "-326194126"  
snapshot1.numDisks = "1"  
snapshot1.disk0.fileName = "sql-000002.vmdk"  
snapshot1.disk0.node = "scsi0:0"  
snapshot2.uid = "17"  
snapshot2.filename = "sql-Snapshot17.vmsn"  
snapshot2.parent = "16"  
snapshot2.displayName = "alkBS"  
snapshot2.createTimeHigh = "310880"  
snapshot2.createTimeLow = "-253322069"  
snapshot2.numDisks = "1"  
snapshot2.disk0.fileName = "sql-000001.vmdk"  
snapshot2.disk0.node = "scsi0:0"  
snapshot3.uid = "18"  
snapshot3.filename = "sql-Snapshot18.vmsn"  
snapshot3.parent = "17"  
snapshot3.displayName = "ASKDB"  
snapshot3.description = ""  
snapshot3.createTimeHigh = "310880"  
snapshot3.createTimeLow = "-185420900"  
snapshot3.numDisks = "1"  
snapshot3.disk0.fileName = "sql-000003.vmdk"  
snapshot3.disk0.node = "scsi0:0"  
snapshot.numSnapshots = "4"  
[/bash]

There is some key information in the file above that will help us recreate the chain.

The number of snapshots that the VMSD knows about.

[bash]snapshot.numSnapshots = "4"[/bash]

The UID of the current snapshot

[bash]snapshot.current = "18"[/bash]

The snapshot vmsn name.

[bash]snapshot3.filename = "sql-Snapshot18.vmsn"[/bash]

The UID of the parent snapshot

[bash]snapshot3.parent = "17"[/bash]

The number of disks on the VM when the snapshot was taken.

[bash]snapshot3.numDisks = "1"[/bash]

The file name of the snapshot disk.

[bash]snapshot3.disk0.fileName = "sql-000003.vmdk"[/bash]

What the scsi ID of the disk is.

[bash]snapshot3.disk0.node = "scsi0:0"[/bash]

Since it gave us the name of the snapshots we can rebuild the chain. If we look at the VMSD we can see that each snapshot has a UID and a parent UID, similar to the parentCID/CID chain. If we follow the chain we can see that the snapshot chain goes (from parent to child) sql.vmdk -> sql-000002.vmdk -> sql-000001.vmdk -> sql-000003.vmdk.

NOTE: the VMSD does not list the current running snapshot. We would look to the VMX to find that sql-000004.vmdk is the current running snapshot. We would then link sql-000003.vmdk to be the parent of sql-000004.vmdk.

### Identifying the Snapshot Chain by the VMSN files

If the timestamps of the delta files do not give us any hints to what the snapshot chain is and the VMSD file did not help, we can check the timestamps of the VMSN files. These are created at the same time as the snapshots. We need to look at the timestamps of the VMSN files and then correlate these back to the correct delta files to get a good idea of what the snapshot chain is. The problem is that these files do not always get cleaned up, so there may be a few extra laying around.

If we look at the timestamps of the VMSN files we can see that the order is 15 -> 16 -> 17 -> 18.

[bash]# ls -lrt *.vmsn  
-rw&#8212;&#8212;- 1 root root 18529 Apr 23 23:22 sql-Snapshot15.vmsn  
-rw&#8212;&#8212;- 1 root root 18529 Apr 23 23:23 sql-Snapshot16.vmsn  
-rw&#8212;&#8212;- 1 root root 18529 Apr 23 23:24 sql-Snapshot17.vmsn  
-rw&#8212;&#8212;- 1 root root 18529 Apr 23 23:25 sql-Snapshot18.vmsn  
[/bash]

Now we have to correlate the VMSN files to the delta files. To do this we need to look inside the VMSN files. These are binary files, but the can be read out to using &#8220;cat&#8221;. I would not suggest &#8220;cat&#8221;ing these files if you took a memory snapshot (if the size is larger than a few MB). The VMSN keeps a copy of the VMX packed on the beginning of the binary file. So if we look at the VMX, we can see what vmdk it points to.

We can &#8220;cat&#8221; the files to find the snapshot the VM was running on.

[bash]# cat sql-Snapshot15.vmsn |grep vmdk  
scsi0:0.fileName = "sql-000001.vmdk"[/bash]

If a memory snapshot was taken, we can use hexdump. It is a bit more difficult to read, but we can see that it is at sql-000001.vmdk

[bash]# hexdump -C sql-Snapshot15.vmsn | grep vmdk -C 1  
000003f0 69 6c 65 4e 61 6d 65 20 3d 20 22 73 71 6c 2d 30 |ileName = "sql-0|  
00000400 30 30 30 30 31 2e 76 6d 64 6b 22 0a 73 63 73 69 |00001.vmdk".scsi|  
00000410 30 3a 30 2e 64 65 76 69 63 65 54 79 70 65 20 3d |0:0.deviceType =|  
[/bash]

So we can check all of the snapshot files and get a good idea of what snapshots are in the chain. The command below will list the vmsn files in reversed time and grep for vmdk out of each of them.

[bash]# ls -rt sql-Snapshot1*.vmsn |xargs -n1 cat |grep vmdk  
scsi0:0.fileName = "sql-000001.vmdk"  
scsi0:0.fileName = "sql-000002.vmdk"  
scsi0:0.fileName = "sql-000001.vmdk"  
scsi0:0.fileName = "sql-000003.vmdk"  
[/bash]

The command above has two refferences to sql-000001.vmdk in it. Since we cannot use the same snapshot twice in the chain, we know that there is only one correct entry. Since the newer snapshots would be created later, we can infer that the first VMSN was never cleaned up. The chain in this situation would be sql.vmdk -> sql-000002.vmdk -> sql-000001.vmdk -> sql-000003.vmdk.

After the chain has been identified with any of the methods above, recreate the descriptors and check them with vmkfstools. If everything checks out, I would suggest doing a clone of the latest snapshot using vmkfstools as described in <a title="VMware Snapshot Troubleshooting" href="http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/']);" target="_blank">VMware Snapshot Troubleshooting</a>. This will not modify the files, so if we guessed wrong on he chain we can change the order of the chain and try again.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-missing-vmdk-descriptors/" title=" Advanced Snapshot Troubleshooting: Missing VMDK Descriptors" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:clone,command line,failed to open parent,snapshots,troubleshooting,vmdk,vmkfstools,blog;button:compact;">A common problem with snapshots is missing descriptors. If you have been following this series of VMware Snapshot Troubleshooting, we have touched on the descriptor properties. In this article we...</a>
</p>