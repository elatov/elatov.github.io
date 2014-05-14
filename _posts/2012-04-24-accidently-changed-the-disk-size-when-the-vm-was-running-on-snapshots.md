---
title: Accidently Changed the Disk Size when the VM was Running on Snapshots
author: Jarret Lavallee
layout: post
permalink: /2012/04/accidently-changed-the-disk-size-when-the-vm-was-running-on-snapshots/
dsq_thread_id:
  - 1405715503
categories:
  - Storage
  - VMware
tags:
  - clone
  - command line
  - failed to open parent
  - snapshots
  - vmdk
  - vmkfstools
---
Changing the size of a base VMDK when the VM is running on snapshots is a very common issue. The best way to ensure that this does not happen is to check for snapshots before doing any disk operations. To identify if a VM is running on a snapshot, please see <a title="VMware Snapshot Troubleshooting" href="http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/']);" target="_blank">VMware Snapshot Troubleshooting</a>.

If you have found yourself in a position where the size of the base disk has been increased when it was running on snapshots, there are a few things that you can try. I would suggest not to modify the original files, as it can lead to losing the data in the snapshots.

Snapshots will be invalidated if the parent disk is modified. This is because a snapshot is a list of changes that have occured since the snapshot was taken. If the starting point is changed, we cannot gurantee that the changes are valid. The host should throw a &#8220;Parent disk modified&#8221; error, as the parent disk of the snapshot has been modified.

If you have increased the partiton/filesystem in the guest operating system you may be out of luck. It should not hurt to try the steps below, but if they do not work VMware will not be able to recover data in the snapshots. If this is the case, the data is not necessarily lost. Datarecovery companies can recover the data in snapshots. I know that <a href="http://www.seagate.com/services-software/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.seagate.com/services-software/']);" target="_blank">seagate data recovery</a> can pull the data from the snapshots. Others companies may be able to as well. Please do not remove the snapshot files before contacting a data recovery service for a free estimate.

### Attempting to revert the geometry

In &#8220;<a title="Invalid Geometry" href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-incorrect-vmdk-geometry/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-incorrect-vmdk-geometry/']);">Invalid Geometry</a>&#8221; we discussed disk geomerty and how to do some basic troubleshooting. Here we will take the RW value from a snapshot and try to apply it back to the base disk. The important thing is that all operations should be clones. We do not want to modify the origional disks since modifying the origional disks can lead to dataloss.

In this section we are going to try to revert the geometry of the base disk to what it was before, and then try to clone the latest snapshot. If the base disk was not modified, the old geometry will still be valid. If the origional disk has been modified in the guest OS, this may not work.

Before we do anything, we want to make a backup of the descriptors.

	
	
	The first thing we have to do is figure out what the origional disk size was. In a healthy snapshot chain the snapshots and base disk have the same RW values, so we can pull the RW value from a snapshot to see what it should been on the base disk.
	
	# grep RW sql-000001.vmdk  
	RW 16777216 VMFSSPARSE &quot;sql-000001-delta.vmdk&quot;
	
	# grep RW sql.vmdk
	
	RW 108987324 VMFS &quot;sql-flat.vmdk&quot;  
	

The RW value of the snapshot is less that that of the base disk. We can take the smaller RW value and calculate the number of cylinders from it. A full explanation of this process is in &#8220;Invalid Geometry&#8221;.

	
	
	So we now have the new RW and cylinders values for the base disk, so let&#8217;s modify the base disk to use these values. Remember that you can use vi to manually make the changes, below we have used sed to illustrate it from the command line.
	
	# sed -i &#8216;s/RW 108987324/RW 16777216/&#8217; sql.vmdk
	
	# grep RW sql.vmdk
	
	RW 16777216 VMFS &quot;sql-flat.vmdk&quot;
	
	# sed -i &#8216;s/ddb.geometry.cylinders = &quot;[0-9]*&quot;/ddb.geometry.cylinders = &quot;1044&quot;/&#8217; sql.vmdk
	
	# grep ddb.geometry.cylinders sql.vmdk
	
	ddb.geometry.cylinders = &quot;1044&quot;  
	

After this we should run vmkfstools on the chain to see if the descriptors are consistent. Often times the CID of the base disk will be changed because the content changed. Please check the chain by using the procedure in &#8220;Mismatched parentCID/CID chain&#8221; if the command below fails.

	 # vmkfstools -v 10 -q sql-000005.vmdk  
	DISKLIB-VMFS : &quot;./sql-000005-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-flat.vmdk&quot; : open successful (23) size = 8589934592, hd = 0. Type 3  
	sql-000005.vmdk is not an rdm  
	DISKLIB-VMFS : &quot;./sql-000005-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-flat.vmdk&quot; : closed.  
	AIOMGR-S : stat o=6 r=18 w=0 i=0 br=294912 bw=0  
	

Since vmkfstools ran through, the descriptors are consistent, let&#8217;s kick off a clone of the VMDK. If the clone succeeds, attach it to another VM to verify the data. If the clone fails, the base disk has likely changed too much and a data recovery service should be contacted.

	# vmkfstools -d thin -i sql-000005.vmdk sql.cloned.vmdk  
	Destination disk format: VMFS thin-provisioned  
	Cloning disk &#8216;sql-000005.vmdk&#8217;&#8230;  
	Clone: 100% done.  
	

The clone above succeeded so I created a new VM and attached the disk to it. If you would like to do this through the command line, please see &#8220;Cloning a VM from the Command Line&#8221;.

In this case, powering up the new VM works. So now it is time to check the consistency of the data in the guest OS. I would advise asking the application administrator to verify this for you.

### Restoring the base VMDK from a backup

If the option above failed there is another option. The snapshots depend on a base disk that has not been modified. Often times the snapshots were left over because of failed backups. This could mean that the backup software has a backup of the base disk before it was modified. Check with your backup admin or on your backup server to see if you have a backup of the base disk. If you have one you think could be in the time frame, restore the vmdk on to a datastore. Make sure not to overwrite the existing base disk.

Once you have the disk restored to a datastore, we can modify oldest snapshot in the chain to point to this base disk and try to clone the snapshots to a new disk.

First let&#8217;s find the oldest snapshot in the chain.

	# grep vmdk sql.vmx  
	scsi0:0.fileName = &quot;sql-000005.vmdk&quot;
	
	# vmkfstools -v 10 -q sql-000005.vmdk
	
	DISKLIB-VMFS : &quot;./sql-000005-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-flat.vmdk&quot; : open successful (23) size = 8589934592, hd = 0. Type 3  
	DISKLIB-LINK : DiskLinkIsAttachPossible: the capacity of each link is different (291212371 != 16777216).  
	DISKLIB-CHAIN : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql.vmdk&quot; : failed to open (The capacity of the parent virtual disk and the capacity of the child disk are different).  
	DISKLIB-VMFS : &quot;./sql-000005-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-flat.vmdk&quot; : closed.  
	DISKLIB-LIB : Failed to open &#8216;sql-000005.vmdk&#8217; with flags 0&#215;17 The capacity of the parent virtual disk and the capacity of the child disk are different (67).  
	Failed to open &#8216;sql-000005.vmdk&#8217; : The capacity of the parent virtual disk and the capacity of the child disk are different (67).  
	

The highlighted line above shows sql-000001.vmdk was the last snapshot before we tried opening the base disk. Let&#8217;s confirm with the parentFileNameHint.

	# grep parentFileNameHint sql-000001.vmdk  
	parentFileNameHint=&quot;sql.vmdk&quot;  
	

I have restored the disk I believe to be the original base disk to /vmfs/volumes/iscsi_dev/sql.restored/sql.vmdk, so we can link sql-000001.vmdk to this disk and try to clone it. The changes can be made manually with vi, but I have chosen to use sed in this example.

First we make a backup of the sql-000001.vmdk.

	
	
	Now we modify the parentFileNameHint to point to the restored disk. In sed we have to escape the &#8220;/&#8221; characters, so there is a &#8220;\&#8221; before ever &#8220;/&#8221;.
	
	

Let&#8217;s confirm the changes are what we wanted them to be.

	
	
	# grep parentFileNameHint sql-000001.vmdk
	
	parentFileNameHint=&quot;/vmfs/volumes/iscsi_dev/sql.restored/sql.vmdk&quot;  
	

Now that we made the modifications, we can confirm the descriptors with vmkfstools. If it fails with a RW value problem, this disk is likely not the original disk. If it fails with a parentCID/CID problem please see &#8220;Invalid parentCID/CID chain&#8221;

	# vmkfstools -v 10 -q sql-000005.vmdk  
	DISKLIB-VMFS : &quot;./sql-000005-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : open successful (23) size = 20480, hd = 0. Type 8  
	DISKLIB-VMFS : &quot;/vmfs/volumes/iscsi_dev/sql.restored/sql-flat.vmdk&quot; : open successful (23) size = 8589934592, hd = 0. Type 3  
	sql-000005.vmdk is not an rdm  
	DISKLIB-VMFS : &quot;./sql-000005-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000004-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000003-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000002-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/sql/sql-000001-delta.vmdk&quot; : closed.  
	DISKLIB-VMFS : &quot;/vmfs/volumes/iscsi_dev/sql.restored/sql-flat.vmdk&quot; : closed.  
	AIOMGR-S : stat o=6 r=18 w=0 i=0 br=294912 bw=0  
	

In this case, the descriptors line up and so we can try to clone the disk.

	# vmkfstools -d thin -i sql-000005.vmdk sql.cloned.vmdk  
	Destination disk format: VMFS thin-provisioned  
	Cloning disk &#8216;sql-000005.vmdk&#8217;&#8230;  
	Clone: 100% done.  
	

The clone above succeeded so I created a new VM and attached the disk to it. If you would like to do this through the command line, please see &#8220;Cloning a VM from the Command Line&#8221;.

In this case, powering up the new VM works. So now it is time to check the consistency of the data in the guest OS. I would advise asking the application administrator to verify this for you.

