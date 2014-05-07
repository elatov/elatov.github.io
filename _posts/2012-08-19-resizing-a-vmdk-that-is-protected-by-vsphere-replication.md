---
title: Resizing a VMDK that is protected by vSphere Replication
author: Jarret Lavallee
layout: post
permalink: /2012/08/resizing-a-vmdk-that-is-protected-by-vsphere-replication/
dsq_thread_id:
  - 1406853126
categories:
  - SRM
  - VMware
  - vTip
tags:
  - clone
  - command line
  - srm
  - vmdk
  - vmkfstools
  - vSphere Replication
  - vtip
---
I have been writing a lot about vSphere Replication recently. I just deployed it again while writing <a title="Using a Custom Root CA Certificates with vSphere Replication" href="http://virtuallyhyper.com/2012/08/using-a-custom-ca-with-vsphere-replication/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/using-a-custom-ca-with-vsphere-replication/']);" target="_blank">this post</a> and I keep finding limitations of the software. It is a 1.0 product, so the features will be comming in future releases along with fixes to many of the issues we have seen. One thing that I found in my lab was resizing a VMDK does not work with vSphere replication. The limitation does make sense as it changing the medium that we are replicating.

The way to resize the disk is to unconfigure replication, increase the disk, and reconfigure replication. The problem with this is that when we un-configure replication the VMDK on the recovery site will be removed and so we will have to do a initial replication again. In my lab its not a big deal because I have a 1Gbit connection between sites, but that would be terrible if you had to replicate 1TB of data over a WAN.

I can think of 2 workarounds for this situation. Both workarounds center around having a disk on the recovery side that we use as an inital sync point when we reconfigure replication for the VM. For both of the workarounds we also need to get our seed disk. To obtain the seed disks there are 2 ways and each are described below, but I am sure there are other ways.

## Obtain the seed disk

### Option 1: Use the original seed disk

When initally setting up vSphere Replication, you can choose to use a seed disk. You would have sent a hard copy of the VM to the remote site and used that VMDK to start the seed. In this manner, vSphere Replication would have only replicated the changes from the base disk. It is a good idea to keep a copy of this disk on the recovery site so that you have an initial sync point if anything goes wrong. In the case of resizing, we can use the seed disk to resize and use as the sync point. If you still have it, copy the seed disk over to the datastore that we want the VM to be replicated to.

### Option 2: Clone the replicated disk to be the initial sync point

Instead of using an old seed disk, we can use a copy of the replica disk. This will be up to date, so the replication changes will not be substantial. If you have read through <a title="Files created for a test failover with vSphere Replication" href="http://virtuallyhyper.com/2012/08/files-created-for-a-test-failover-with-vsphere-replication/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/files-created-for-a-test-failover-with-vsphere-replication/']);" target="_blank">this post</a>, you know the format of the files on the recovery site. Knowing this structure we can make a copy of the VMDK(s) and then use them when we are reconfiguring replication.

Let&#8217;s take a look at the files on the recovery site for this VM. We can see that there is a flat file and a delta file. The new changes will temporarily be put into the delta and then pushed into the flat file. What we want to do is clone the flat file when there is no sync going on, as this will be the time when there is no lock on the file.

	  
	\# ls -lh  
	-rw\---\---- 1 root root 8.5k Aug 14 21:36 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.86.nvram.258  
	-rw\---\---- 1 root root 3.2k Aug 14 21:36 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.86.vmx.256  
	-rw\---\---- 1 root root 258 Aug 14 21:36 hbrcfg.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.86.vmxf.257  
	-rw\---\---- 1 root root 24.0k Aug 14 21:36 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.87.281473597897102-delta.vmdk  
	-rw\---\---- 1 root root 367 Aug 14 21:37 hbrdisk.RDID-aa0132e8-3cc4-4d2b-ab71-4fda0b4a4f62.87.281473597897102.vmdk  
	-rw\---\---- 1 root root 2.7k Aug 14 21:37 hbrgrp.GID-fdf5516b-1345-46a3-ae18-9deff00e5f73.txt  
	-rw\---\---- 1 root root 10.0G Aug 14 21:37 sql-flat.vmdk  
	-rw\---\---- 1 root root 606 Aug 14 21:37 sql.vmdk  
	

To ensure that we do not have any active replication going we can pause the replication for the VM. Then we want to clone the VMDK. To do this we can use the vmkfstools command. Below I clone it to a thin provisioned VMDK.

	  
	\# vmkfstools -d thin -i sql.vmdk sql.orig.vmdk  
	Destination disk format: VMFS thin-provisioned  
	Cloning disk 'sql.vmdk'...  
	Clone: 100% done.  
	

## Resize the disks and reconfiguring the replication

Now we have a seed VMDK that we can use, so we should remove replication on the protected site VM. This will remove all of the vSphere Replication files on the recovery site, so make sure to clone all disks attached to the VM.

After you have removed replication on the VM, you will only see the cloned disks on the recovery site.

	  
	\# ls -l  
	-rw\---\---- 1 root root 10737418240 Aug 14 21:39 sql.orig-flat.vmdk  
	-rw\---\---- 1 root root 634 Aug 14 21:40 sql.orig.vmdk  
	

We should rename them to the original names to use the seed (sneaker net) feature.

	  
	\# vmkfstools -E sql.orig.vmdk sql.vmdk  
	\# ls -l  
	-rw\---\---- 1 root root 10737418240 Aug 14 21:39 sql-flat.vmdk  
	-rw\---\---- 1 root root 629 Aug 14 22:02 sql.vmdk  
	

When we cloned the VMDK, it would have been given a new Content ID and a new UUID. On the protected site datastore, find the ddb.uuid and db.longContentID and copy them over to the recovery site VMDK. Edit the sql.vmdk and add the following lines from the protected site VMDK.

	  
	db.longContentID = "5a89cba74ae27ddd0b23c1b171f901c5"  
	ddb.uuid = "60 00 C2 99 e7 66 f6 f3-fb 6b a5 91 fa 14 b2 3e"  
	

Now we should increase the size of the disk on the protected site. Note the new size of the disk so we can increase it to the same size on the recovery site. In this case I grew the VMDK to 11G on the protected site, so I need to grow it to 11G on the recovery site.

	  
	\# vmkfstools -X 11G sql.vmdk  
	Grow: 100% done.  
	\# ls -lh  
	-rw\---\---- 1 root root 11.0G Aug 14 21:39 sql-flat.vmdk  
	-rw\---\---- 1 root root 629 Aug 14 22:04 sql.vmdk  
	

Now we can configure replication again. Make sure to select the same location that we have our seed disk. When configureing replication it will detect the seed disk and ask if you want to use it as the inital replication. We do want to do this, so click on yes.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/vSphere-Replication-Initial-Copy-Confirmation.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/vSphere-Replication-Initial-Copy-Confirmation.png']);"><img class="aligncenter size-full wp-image-2311" title="vSphere Replication - Initial Copy Confirmation" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/vSphere-Replication-Initial-Copy-Confirmation.png" alt="vSphere Replication Initial Copy Confirmation Resizing a VMDK that is protected by vSphere Replication" width="574" height="161" /></a>

Finish the wizard and it will configure replication. When it finishes the new size will be configured on both site. We can confirm, but the full sync should only be sending changes. Below we can see that only 668KB has been transferred instaed of the full 2Gb that it has already checked.

	  
	\# vim-cmd hbrsvc/vmreplica.getState 7  
	Retrieve VM running replication state:  
	The VM is configured for replication. Current replication state: Group: GID-1e53820d-0435-4227-b303-de6af47314aa (generation=55824554497837)  
	Group State: full sync (17% done: checksummed 2.0 GB of 11 GB, transferred 688 KB of 688 KB)  
	DiskID RDID-4bc95cb4-31aa-4858-9b19-6f2e02ef1393 State: full sync (checksummed 2.0 GB of 11 GB, transferred 688 KB of 688 KB)  
	

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/resizing-a-vmdk-that-is-protected-by-vsphere-replication/" title=" Resizing a VMDK that is protected by vSphere Replication" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:clone,command line,srm,vmdk,vmkfstools,vSphere Replication,vtip,blog;button:compact;">I have been writing a lot about vSphere Replication recently. I just deployed it again while writing this post and I keep finding limitations of the software. It is a...</a>
</p>