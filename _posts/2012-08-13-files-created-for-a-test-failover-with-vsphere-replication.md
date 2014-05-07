---
title: Files created for a test failover with vSphere Replication
author: Jarret Lavallee
layout: post
permalink: /2012/08/files-created-for-a-test-failover-with-vsphere-replication/
dsq_thread_id:
  - 1404672994
categories:
  - SRM
  - VMware
tags:
  - command line
  - delta
  - light-weight-delta
  - lwd
  - PSF
  - snapshots
  - srm
  - VRMS
  - vSphere Replication
---
I have been writing a lot about SRM and vSphere Replication recently, but I have not written about how it all works. There is a great blog on <a href="http://blogs.vmware.com/uptime/2011/10/how-does-vsphere-replication-work.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/uptime/2011/10/how-does-vsphere-replication-work.html']);" target="_blank">how vSphere Replication works here</a>. Personally I like to try it out and see what changes. One of the first things I did when learning vSphere Replication was look at the files that are modified during the test failover and configuring replication.

Let&#8217;s look at a VM before we configure replication.

[code]  
\# ls -l  
-rw\---\---- 1 root root 20971520 Aug 11 04:57 sql-154ccb6d.vswp  
-rw\---\---- 1 root root 10737418240 Aug 11 04:55 sql-flat.vmdk  
-rw\---\---- 1 root root 8684 Aug 11 04:57 sql.nvram  
-rw\---\---- 1 root root 490 Aug 11 04:55 sql.vmdk  
-rw-r--r-- 1 root root 0 Aug 11 04:55 sql.vmsd  
-rwxr-xr-x 1 root root 2592 Aug 11 04:57 sql.vmx  
-rw-r--r-- 1 root root 258 Aug 11 04:57 sql.vmxf  
-rw-r--r-- 1 root root 70053 Aug 11 04:56 vmware-1.log  
-rw-r--r-- 1 root root 56345 Aug 11 05:08 vmware.log  
-rw\---\---- 1 root root 51380224 Aug 11 04:57 vmx-sql-357354349-1.vswp

[/code]

When I enable replication on the VM we can see a few changes. The first being that the psf file is added.

[code]  
-rw\---\---- 1 root root 328192 Aug 11 05:16 hbr-persistent-state-RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.psf  
[/code]

The next thing we see is that there are some more parameters added to the VMX. Most of them are the definition of the filter.

[code]  
hbr_filter.configGen = "1"  
scsi0:0.filters = "hbr_filter"  
hbr_filter.rpo = "240"  
hbr_filter.destination = "192.168.10.86"  
hbr_filter.port = "31031"  
hbr_filter.gid = "GID-fdf5516b-1345-46a3-ae18-9deff00e5f73"  
hbr_filter.protocol = "lwd"  
hbr_filter.quiesce = "false"  
hbr_filter.opp = "false"  
hbr_filter.pause = "false"  
scsi0:0.hbr_filter.rdid = "RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62"  
scsi0:0.hbr_filter.persistent = "hbr-persistent-state-RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.psf"  
[/code]

On the destination we see the following during the full sync.

[code]  
\# ls -l  
-rw\---\---- 1 root root 10737418240 Aug 11 05:17 sql-flat.vmdk  
-rw\---\---- 1 root root 490 Aug 11 05:17 sql.vmdk  
[/code]

Once the full sync has finished hbr will add the config files (hbrcfg) for the VM, the delta (hbrdisk) and replication configuration (hbrgrp).

[code]  
-rw\---\---- 1 root root 8684 Aug 11 05:33 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.3.nvram.9  
-rw\---\---- 1 root root 3201 Aug 11 05:33 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.3.vmx.7  
-rw\---\---- 1 root root 258 Aug 11 05:33 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.3.vmxf.8  
-rw\---\---- 1 root root 24576 Aug 11 05:33 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.5.281474340856749-delta.vmdk  
-rw\---\---- 1 root root 366 Aug 11 05:33 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.5.281474340856749.vmdk  
-rw\---\---- 1 root root 2743 Aug 11 05:33 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
-rw\---\---- 1 root root 10737418240 Aug 11 05:17 sql-flat.vmdk  
-rw\---\---- 1 root root 490 Aug 11 05:17 sql.vmdk  
[/code]

Here is the configuration file (click to expand).

[code title="hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt" collapse="true"]  
.encoding = "UTF-8"

\# VMware HBR Replication Group Recovery Descriptor  
state.version.major = "1"  
state.version.minor = "5"  
state.version.patch = "0"  
state.created = "1344663239"

\# Group-wide state  
group.configDir.ds = "501d996c-86c66169-eea2-005056b007c1"  
group.configDir.relpath = "sql"  
group.id = "GID-fdf5516b-1345-46a3-ae18-9deff00e5f73"  
group.rpo = "240"  
group.paused = "0"  
group.instanceSeq = "1822568202"  
group.instanceAborted = "0"

\# VMs  
group.vms = "1"  
vm.0.id = "GID-fdf5516b-1345-46a3-ae18-9deff00e5f73"

\# Group instances  
group.instances = "1"  
instance.0.label = "replica-0"  
instance.0.start = "2"  
instance.0.complete = "0"  
instance.0.transferBytes = "12599"  
instance.0.diskCount = "1"

\# 0 RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62  
instance.0.fileCount = "3"  
instance.0.file.0.id = "sql.vmx"  
instance.0.file.0.path.ds = "501d996c-86c66169-eea2-005056b007c1"  
instance.0.file.0.path.relpath = "sql/hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.3.vmx.7"  
instance.0.file.0.fileType = "0"  
instance.0.file.1.id = "sql.vmxf"  
instance.0.file.1.path.ds = "501d996c-86c66169-eea2-005056b007c1"  
instance.0.file.1.path.relpath = "sql/hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.3.vmxf.8"  
instance.0.file.1.fileType = "1"  
instance.0.file.2.id = "sql.nvram"  
instance.0.file.2.path.ds = "501d996c-86c66169-eea2-005056b007c1"  
instance.0.file.2.path.relpath = "sql/hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.3.nvram.9"  
instance.0.file.2.fileType = "2"

\# -- Group disk state  
disk.count = "1"

\# \---- Disk 0 RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62  
disk.0.id = "RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62"  
disk.0.cid = "831cb64ef8b9617e977d8a43fffffffe"  
disk.0.generation = "68889438896102"  
disk.0.uncnf = "0"  
disk.0.instance.0.path.ds = "501d996c-86c66169-eea2-005056b007c1"  
disk.0.instance.0.path.relpath = "sql/sql.vmdk"  
disk.0.instance.0.toolsVersion = "0"  
disk.0.instance.0.cylinders = "1305"  
disk.0.instance.0.heads = "255"  
disk.0.instance.0.sectors = "63"  
disk.0.instance.0.biosCylinders = "0"  
disk.0.instance.0.biosHeads = "0"  
disk.0.instance.0.biosSectors = "0"  
disk.0.instance.0.groupInstance = "0"  
disk.0.instance.0.transferBytes = "0"  
disk.0.instance.0.transferSeconds = "2"  
disk.0.instance.0.quiescedType = "0"  
disk.0.instance.0.isComplete = "1"  
disk.0.instance.1.path.ds = "501d996c-86c66169-eea2-005056b007c1"  
disk.0.instance.1.path.relpath = "sql/hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.5.281474340856749.vmdk"  
disk.0.instance.1.toolsVersion = "0"  
disk.0.instance.1.cylinders = "0"  
disk.0.instance.1.heads = "0"  
disk.0.instance.1.sectors = "0"  
disk.0.instance.1.biosCylinders = "0"  
disk.0.instance.1.biosHeads = "0"  
disk.0.instance.1.biosSectors = "0"  
disk.0.instance.1.isComplete = "0"  
state.complete = "1"  
[/code]

I installed an OS on the VM and forced another full sync. We can see the data getting replicated and put into the delta file temporarily.

[code]  
\# vim-cmd hbrsvc/vmreplica.getState 7  
Retrieve VM running replication state:  
The VM is configured for replication. Current replication state: Group: GID-fdf5516b-1345-46a3-ae18-9deff00e5f73 (generation=77634542849735)  
Group State: full sync (24% done: checksummed 2.2 GB of 10 GB, transferred 240.5 MB of 240.5 MB)  
DiskID RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62 State: full sync (checksummed 2.2 GB of 10 GB, transferred 259.5 MB of 259.5 MB)  
[/code]

Here is the delta file on the DR datastore.

[code]  
-rw\---\---- 1 root root 259.5M Aug 11 06:06 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.5.281474340856749-delta.vmdk  
[/code]

Immediately after the full sync is finished the LWD is being sent over.

[code]  
\# vim-cmd hbrsvc/vmreplica.getState 7  
Retrieve VM running replication state:  
The VM is configured for replication. Current replication state: Group: GID-fdf5516b-1345-46a3-ae18-9deff00e5f73 (generation=81583558736608)  
Group State: lwd delta (instanceId=replica-0) (68% done: transferred 100.1 MB of 146.3 MB)  
DiskID RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62 State: lwd delta (transferred 100.1 MB of 146.3 MB)  
[/code]

Once that was sent over, the delta was pushed into the flat file on the dr site. Also note that the config files were incremented.

[code]  
\# ls -lh  
-rw\---\---- 1 root root 8.5k Aug 11 06:22 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.4.nvram.12  
-rw\---\---- 1 root root 3.2k Aug 11 06:22 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.4.vmx.10  
-rw\---\---- 1 root root 258 Aug 11 06:22 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.4.vmxf.11  
-rw\---\---- 1 root root 24.0k Aug 11 06:23 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.6.327059739-delta.vmdk  
-rw\---\---- 1 root root 360 Aug 11 06:25 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.6.327059739.vmdk  
-rw\---\---- 1 root root 2.7k Aug 11 06:25 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
-rw\---\---- 1 root root 10.0G Aug 11 06:25 sql-flat.vmdk  
-rw\---\---- 1 root root 490 Aug 11 06:25 sql.vmdk  
[/code]

An incremental replication kicks off after within my RPO.

[code]  
\# vim-cmd hbrsvc/vmreplica.getState 7  
Retrieve VM running replication state:  
The VM is configured for replication. Current replication state: Group: GID-fdf5516b-1345-46a3-ae18-9deff00e5f73 (generation=83918097705771)  
Group State: lwd delta (instanceId=replica-2) (23% done: transferred 78.7 MB of 336.6 MB)  
DiskID RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62 State: lwd delta (transferred 78.7 MB of 336.6 MB)  
[/code]

We see the delta getting inflated and new copies of the config files copied over.

[code]  
\# ls -lrth  
-rw\---\---- 1 root root 3.2k Aug 11 06:22 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.4.vmx.10  
-rw\---\---- 1 root root 258 Aug 11 06:22 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.4.vmxf.11  
-rw\---\---- 1 root root 8.5k Aug 11 06:22 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.4.nvram.12  
-rw\---\---- 1 root root 490 Aug 11 06:25 sql.vmdk  
-rw\---\---- 1 root root 10.0G Aug 11 06:25 sql-flat.vmdk  
-rw\---\---- 1 root root 2.7k Aug 11 06:25 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
-rw\---\---- 1 root root 258 Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.5.vmxf.14  
-rw\---\---- 1 root root 3.2k Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.5.vmx.13  
-rw\---\---- 1 root root 8.5k Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.5.nvram.15  
-rw\---\---- 1 root root 258 Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.6.vmxf.17  
-rw\---\---- 1 root root 3.2k Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.6.vmx.16  
-rw\---\---- 1 root root 360 Aug 11 06:34 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.6.327059739.vmdk  
-rw\---\---- 1 root root 8.5k Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.6.nvram.18  
-rw\---\---- 1 root root 112.0M Aug 11 06:35 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.6.327059739-delta.vmdk  
[/code]

After the sync, the delta gets pushed into the flat file again.

[code]  
\# ls -lrth  
-rw\---\---- 1 root root 258 Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.6.vmxf.17  
-rw\---\---- 1 root root 3.2k Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.6.vmx.16  
-rw\---\---- 1 root root 8.5k Aug 11 06:34 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.6.nvram.18  
-rw\---\---- 1 root root 24.0k Aug 11 06:36 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.7.203603438-delta.vmdk  
-rw\---\---- 1 root root 490 Aug 11 06:38 sql.vmdk  
-rw\---\---- 1 root root 10.0G Aug 11 06:38 sql-flat.vmdk  
-rw\---\---- 1 root root 360 Aug 11 06:38 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.7.203603438.vmdk  
-rw\---\---- 1 root root 2.7k Aug 11 06:38 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
[/code]

Next I kicked off a test failover. As we would expect, the sync once sends a LWD. Once the incremental is done, a new folder is created on the dr datastore. The folder is a UUID associated with the snapshot.

[code]  
\# ls -ld 52bcb8b0-7d08-a617-a517-c202d792ea43/  
drwxr-xr-x 1 root root 1540 Aug 11 06:42 52bcb8b0-7d08-a617-a517-c202d792ea43/  
[/code]

If we look inside the folder we see the following.

[code]  
\# ls -l  
-rw\---\---- 1 root root 16801792 Aug 11 06:44 hbrimagedisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62-delta.vmdk  
-rw\---\---- 1 root root 407 Aug 11 06:42 hbrimagedisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.vmdk  
-rw\---\---- 1 root root 268435456 Aug 11 06:42 sql-a798dd20.vswp  
-rw\---\---- 1 root root 8684 Aug 11 06:42 sql.nvram  
-rw\---\---- 1 root root 0 Aug 11 06:42 sql.vmsd  
-rw\---\---- 1 root root 2849 Aug 11 06:42 sql.vmx  
-rw\---\---- 1 root root 258 Aug 11 06:42 sql.vmxf  
-rw-r--r-- 1 root root 56698 Aug 11 06:43 vmware.log  
-rw\---\---- 1 root root 51380224 Aug 11 06:42 vmx-sql-2811813152-1.vswp  
[/code]

We have the usual config files, log files and a vswp for the VM to run. The interesting thing above is the hbrimagedisk files. This is a snapshot that links back to the replica flat file. All of the changes that occur durring the test failover go. Below is the hbrimagedisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.vmdk.

[code]  
\# Disk DescriptorFile  
version=1  
encoding="UTF-8"  
CID=b9807598  
parentCID=984805a6  
isNativeSnapshot="no"  
createType="vmfsSparse"  
parentFileNameHint="/vmfs/volumes/501d996c-86c66169-eea2-005056b007c1/sql/sql.vmdk"  
\# Extent description  
RW 20971520 VMFSSPARSE "hbrimagedisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62-delta.vmdk"

\# The Disk Data Base  
#DDB

ddb.longContentID = "d5586c4dfa9408454587f26db9807598"  
[/code]

While the VM is in test failover, no new changes can be written to the flat file on the dr site. If we did write changes to it it would invalidate the test failover snapshot. So when we send a new LWD it will create a new delta and merge the changes into the original delta. You will also notice that there is a new delta created while the changes get merged into the original. Here are the files on the dr datastore while a LWD is being sent (at 100%).

[code]  
drwxr-xr-x 1 root root 1.5k Aug 11 06:42 52bcb8b0-7d08-a617-a517-c202d792ea43  
-rw\---\---- 1 root root 8.5k Aug 11 15:17 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.47.nvram.141  
-rw\---\---- 1 root root 3.2k Aug 11 15:17 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.47.vmx.139  
-rw\---\---- 1 root root 258 Aug 11 15:17 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.47.vmxf.140  
-rw\---\---- 1 root root 8.5k Aug 11 15:32 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.48.nvram.144  
-rw\---\---- 1 root root 3.2k Aug 11 15:32 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.48.vmx.142  
-rw\---\---- 1 root root 258 Aug 11 15:32 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.48.vmxf.143  
-rw\---\---- 1 root root 8.5k Aug 11 06:41 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.7.nvram.21  
-rw\---\---- 1 root root 3.2k Aug 11 06:41 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.7.vmx.19  
-rw\---\---- 1 root root 258 Aug 11 06:41 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.7.vmxf.20  
-rw\---\---- 1 root root 368.0M Aug 11 15:33 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.48.280456830786583-delta.vmdk  
-rw\---\---- 1 root root 431 Aug 11 15:32 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.48.280456830786583.vmdk  
-rw\---\---- 1 root root 24.0k Aug 11 15:33 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.49.3616717730050-delta.vmdk  
-rw\---\---- 1 root root 430 Aug 11 15:33 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.49.3616717730050.vmdk  
-rw\---\---- 1 root root 288.0M Aug 11 15:34 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.8.281474412040766-delta.vmdk  
-rw\---\---- 1 root root 366 Aug 11 15:34 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.8.281474412040766.vmdk  
-rw\---\---- 1 root root 4.2k Aug 11 15:17 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
-rw\---\---- 1 root root 10.0G Aug 11 06:41 sql-flat.vmdk  
-rw\---\---- 1 root root 606 Aug 11 06:42 sql.vmdk  
[/code]

When the incremental sync is finished, the new delta (hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.48.280456830786583-delta.vmdk) is merged into the original delta (hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.8.281474412040766-delta.vmdk). The delta is then removed.

[code]  
drwxr-xr-x 1 root root 1.5k Aug 11 06:42 52bcb8b0-7d08-a617-a517-c202d792ea43  
-rw\---\---- 1 root root 8.5k Aug 11 15:32 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.48.nvram.144  
-rw\---\---- 1 root root 3.2k Aug 11 15:32 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.48.vmx.142  
-rw\---\---- 1 root root 258 Aug 11 15:32 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.48.vmxf.143  
-rw\---\---- 1 root root 8.5k Aug 11 06:41 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.7.nvram.21  
-rw\---\---- 1 root root 3.2k Aug 11 06:41 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.7.vmx.19  
-rw\---\---- 1 root root 258 Aug 11 06:41 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.7.vmxf.20  
-rw\---\---- 1 root root 24.0k Aug 11 15:33 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.49.3616717730050-delta.vmdk  
-rw\---\---- 1 root root 429 Aug 11 15:35 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.49.3616717730050.vmdk  
-rw\---\---- 1 root root 368.0M Aug 11 15:35 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.8.281474412040766-delta.vmdk  
-rw\---\---- 1 root root 366 Aug 11 15:35 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.8.281474412040766.vmdk  
-rw\---\---- 1 root root 4.2k Aug 11 15:35 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
-rw\---\---- 1 root root 10.0G Aug 11 06:41 sql-flat.vmdk  
-rw\---\---- 1 root root 606 Aug 11 06:42 sql.vmdk  
[/code]

So when we cleanup the test failover, we will see the folder (52bcb8b0-7d08-a617-a517-c202d792ea43) removed. We will then see the big delta (hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.8.281474412040766-delta.vmdk) committed into flat file (sql-flat.vmdk). I cleaned up the test failover and here is the folder after.

[code]  
-rw\---\---- 1 root root 258 Aug 11 16:19 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.52.vmxf.155  
-rw\---\---- 1 root root 3301 Aug 11 16:19 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.52.vmx.154  
-rw\---\---- 1 root root 8684 Aug 11 16:19 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.52.nvram.156  
-rw\---\---- 1 root root 24576 Aug 11 16:19 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.53.200892301402003-delta.vmdk  
-rw\---\---- 1 root root 4319 Aug 11 16:19 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
-rw\---\---- 1 root root 606 Aug 11 16:25 sql.vmdk  
-rw\---\---- 1 root root 10737418240 Aug 11 16:25 sql-flat.vmdk  
-rw\---\---- 1 root root 367 Aug 11 16:25 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.53.200892301402003.vmdk  
[/code]

Notice that the there is a new delta (hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.53.200892301402003-delta.vmdk) that is only 24k (one subblock).

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/files-created-for-a-test-failover-with-vsphere-replication/" title=" Files created for a test failover with vSphere Replication" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:command line,delta,light-weight-delta,lwd,PSF,snapshots,srm,VRMS,vSphere Replication,blog;button:compact;">I have been writing a lot about SRM and vSphere Replication recently, but I have not written about how it all works. There is a great blog on how vSphere...</a>
</p>