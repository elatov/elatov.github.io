---
title: 'Advanced Snapshot Troubleshooting: Non-Linear VMware Snapshot Chain'
author: Jarret Lavallee
layout: post
permalink: /2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/
dsq_thread_id:
  - 1404673128
categories:
  - Storage
  - VMware
tags:
  - clone
  - command line
  - snapshots
  - troubleshooting
  - vmkfstools
---
Recently, I wrote up an article about <a title="VMware Snapshot Troubleshooting" href="http://virtuallyhyper.com/?p=703" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/?p=703']);">VMware Snapshot Troubleshooting</a>. In the article we discussed how to do some basic snapshot troubleshooting. Today, we will look a little deeper into non-Linear VMware Snapshot Chains.

A non-linear snapshot chain is when the snapshot chain is out of numerical order. That is to say when the snapshots are not numbered vmname-000001.vmdk, vmname-000002.vmdk &#8230; vmname-00000N.vmdk. This is not a real problem, but can make the snapshot confusing to understand.

## Causes

This can happen under multiple circumstances, so we will cover most common causes. The important part is that this is completely normal and should not affect the snapshot chain.

### VM&#8217;s with disks across datastores

When a disk is added to a VM, the host will check to see if the vmname.vmdk disk already exists. If it does exist, the new name of the disk will be incremented by 1 (with an \_) until it finds a unique name for the disk. So if a VM already has 2 disks on the datastore, the host should create a disk named vmname\_2.vmdk because vmname.vmdk and vmname_1.vmdk already exist.

When a host goes to put a new disk on a datastore that does not have a vmname.vmdk on it already, it will create the disk with the default name vmname.vmdk. Since this is the default behavior, we get in a situation where VMs will have the same named disk across multiple datastores. Both of these disks are named sql.vmdk.

Below is an example of a VM that has a disk across multiple datastores. We can see that the disk attached to scsi0:1 is on a different datastore because the absolute path is specified. scsi0:0 uses the relative path since it is on the same datastore as the VMX.

	# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql.vmdk&quot;  
	scsi0:1.fileName = &quot;/vmfs/volumes/4e264751-cf9b8809-301e-00e08176b934/sql/sql.vmdk&quot;

When we take a snapshot of a VM, the snapshot name will have the <a href="http://www.manpagez.com/man/1/basename" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.manpagez.com/man/1/basename']);" target="_blank">basename</a> of it&#8217;s parent. Since both disks have the same name, we would expect the snapshots to have the same name. The snapshot process will create the snapshot for the first disk first, so it will get the name sql-000001.vmdk. Since this file already exists when creating the snapshot for the second disk, the name will be incremented to sql-000002.vmdk.

	# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql-000001.vmdk&quot;  
	scsi0:1.fileName = &quot;sql-000002.vmdk&quot;
	
	\# grep parentFileNameHint sql-000001.vmdk  
	parentFileNameHint=&quot;sql.vmdk&quot;
	
	\# grep parentFileNameHint sql-000002.vmdk  
	parentFileNameHint=&quot;/vmfs/volumes/4e264751-cf9b8809-301e-00e08176b934/sql/sql.vmdk&quot;  
	

If we were to add more snapshots to this VM, the first disk would have snapshots sql-000001.vmdk, sql-000003.vmdk &#8230; sql-00000N.vmdk. The second disk would have snapshots sql-000002.vmdk, sql-000004.vmdk &#8230; sql-00000N.vmdk.

**NOTE:** This behavior has changed in ESXi 5.x. The default snapshot behavior is to keep the snapshots with the parent disks. This can be changed by setting the <a href="http://kb.vmware.com/kb/2007563" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2007563']);" target="_blank">snapshot.redoNotWithParent</a> flag.

**NOTE:** The snapshots do not have to be in the VMX directory. They could have been changed in 4.x with the <a href="http://kb.vmware.com/kb/1002929" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002929']);" target="_blank">workingDir</a> flag.

## Snapshots mid-chain that have been removed

When snapshots that are in the middle of a chain are deleted, the snapshot names are reused for later snapshots. This can create a situation where the numbering scheme of the snapshots does not follow a sequential order.

To illustrate this we will take a VM with single disk and two snapshots.

	# ls *.vmdk  
	sql-000001-delta.vmdk sql-000002-delta.vmdk sql-flat.vmdk  
	sql-000001.vmdk sql-000002.vmdk sql.vmdk
	
	\# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql-000002.vmdk&quot;
	
	\# grep parentFileNameHint sql-000002.vmdk  
	parentFileNameHint=&quot;sql-000001.vmdk&quot;
	
	\# grep parentFileNameHint sql-000001.vmdk  
	parentFileNameHint=&quot;sql.vmdk&quot;  
	

If we delete the first snapshot, the changes in sql-000001.vmdk will be pushed into sql.vmdk and the files will be removed. Then sql-000002.vmdk&#8217;s parent will be set back to sql.vmdk. The VM will continue to run off of sql-000002.vmdk.

	# ls *.vmdk  
	sql-000002-delta.vmdk sql-000002.vmdk sql-flat.vmdk sql.vmdk
	
	\# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql-000002.vmdk&quot;
	
	\# grep parentFileNameHint sql-000002.vmdk  
	parentFileNameHint=&quot;sql.vmdk&quot;  
	

Now if we were to create another snapshot, it would take the first available name, which would be sql-000001.vmdk. This would actually be the second snapshot.

	# ls *.vmdk  
	sql-000001-delta.vmdk sql-000002-delta.vmdk sql-flat.vmdk  
	sql-000001.vmdk sql-000002.vmdk sql.vmdk
	
	\# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql-000001.vmdk&quot;
	
	\# grep parentFileNameHint sql-000001.vmdk  
	parentFileNameHint=&quot;sql-000002.vmdk&quot;
	
	\# grep parentFileNameHint sql-000002.vmdk  
	parentFileNameHint=&quot;sql.vmdk&quot;  
	

The next snapshot would be named sql-000003.vmdk and so forth. It is important not to trust the numbering scheme, but rather follow the chain from with in the descriptors.

## How to Deal with Non-linear Snapshots

Chances are that there is another problem when dealing with non-linear snapshots since the number does not matter. It tends to confuse people more than causing any problem, unless the descriptors are missing.

### Confirm the chain

When dealing with any snapshot case, it is important to confirm the snapshot chain. This can me manually verified by following the parentFileNameHint as we did in the previous examples. There is also another cool trick that we can use to do all of the work for us. The vmkfstools command can verify the chain for us automatically. The command is actually designed to query an RDM pointer, but if we increase the verbosity of the command it will walk through the snapshot chain and tell us if there are problems with the descriptors.

In the example below we run the vmkfstools command on the current snapshot. It goes through and opens each of the snapshots and verifies its descriptor is consistent (CID/PID matching and RW values). It will then open the base disk and fail because the base disk is not and RDM. The failure is expected.

	# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql-000003.vmdk&quot;
	
	\# vmkfstools -v10 -q sql-000003.vmdk  
	DISKLIB-VMFS : &quot;./sql-000003-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-flat.vmdk&quot; : open successful (23) size = 8589934592, hd = 0. Type 3  
	sql-000003.vmdk is not an rdm  
	DISKLIB-VMFS : &quot;./sql-000003-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-flat.vmdk&quot; : closed.  
	AIOMGR-S : stat o=5 r=15 w=0 i=0 br=245760 bw=0  
	

In the example above we can see that the chain (from child to parent) goes sql-000003-delta.vmdk -> sql-000004-delta.vmdk -> sql-000001-delta.vmdk -> sql-000002-delta.vmdk -> sql-flat.vmdk. It did not complain about any CID/PID or RW Value mismatches, so the chain is intact.

The benefits of this command come in when there are many snapshots and when we want to confirm the consistency of the descriptors. Checking these manually is time consuming.

If the &#8220;vmkfstools -v 10 -q vmname.vmdk&#8221; command is able to open the whole chain, you can commit the snapshots or clone the VMDK. The procedures for committing and cloning are explained in &#8220;<a title="VMware Snapshot Troubleshooting" href="http://virtuallyhyper.com/?p=703" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/?p=703']);">VMware Snapshot Troubleshooting</a>&#8220;. If there are problems with the chain, an upcoming post &#8220;Advanced Snapshot Troubleshooting: Invalid PID/CID chain&#8221; should address some of these issues.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/" title=" Advanced Snapshot Troubleshooting: Non-Linear VMware Snapshot Chain" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:clone,command line,snapshots,troubleshooting,vmkfstools,blog;button:compact;">Recently, I wrote up an article about VMware Snapshot Troubleshooting. In the article we discussed how to do some basic snapshot troubleshooting. Today, we will look a little deeper into...</a>
</p>