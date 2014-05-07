---
title: Decrease Initial Replication Bandwidth and Time with vSphere Replication
author: Jarret Lavallee
layout: post
permalink: /2012/08/save-initial-replication-bandwidth-with-vsphere-replication/
dsq_thread_id:
  - 1404673432
categories:
  - SRM
  - VMware
  - vTip
tags:
  - bandwidth
  - clone
  - srm
  - vmdk
  - vmkfstools
  - VRMS
  - vSphere Replication
  - vtip
---
vSphere Replication has a great feature that allows us to specify the seed disk for the inital sync. The idea is that you can ship a hard copy of the VMDKs over to the recovery site and then use these VMDKs as the inial sync. vSphere Replication will then use this disk to calculate the changes and then do an incremental sync. This can significantly decrease the amount of bandwidth that is used for the inital sync. 

This great feature will allow us to save bandwidth on a per VM basis, but we can use it to save even more. Say, for example, you have many VMs that came from the same template. Why couldn&#8217;t we just copy the template over to the recovery site and use that as our seed disk? The minimum that this will do is save us from syncing the OS files multiple times, which could be multiple GB per VM. In this manner we do not have to physically ship anything over, but we can save bandwith and decrease inital sync times.

First we need to copy the template over to the recovery site. Once the template is on the recovery site, we can copy the disk over to be the seed disk for each VM. In this case I have copied my template over to the recovery site. I can now create a folder and clone the seed disk. 

	  
	\# mkdir /vmfs/volumes/dr/webserver  
	\# vmkfstools -d thin -i /vmfs/volumes/dr/template/template.vmdk /vmfs/volumes/dr/webserver/webserver.vmdk  
	Destination disk format: VMFS thin-provisioned  
	Cloning disk '/vmfs/volumes/dr/template/template.vmdk'...  
	Clone: 100% done.  
	

Now we can update the descriptor to match the UUID of the protected site descriptor. On the protected site we can get the UUID of the disk.

	  
	\# grep uuid webserver.vmdk  
	ddb.uuid = "60 00 C2 96 a4 c8 0d bf-5b 26 af 92 63 56 ee 79"  
	

Now on the recovery edit the descriptor /vmfs/volumes/dr/webserver/webserver.vmdk. Replace the existing UUID with the one we found on the protected site.

Replace  
	  
	ddb.uuid = "60 00 C2 97 37 2f b4 9b-4f 08 67 98 11 4c 96 e8"  
	

With 

	  
	ddb.uuid = "60 00 C2 96 a4 c8 0d bf-5b 26 af 92 63 56 ee 79"  
	

Now that the vmdk has been added from the template to the recovery site VM directory and we fixed the UUID, we can set up replication.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/Initial-Copy-Confirmation-Seed-Disk.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/Initial-Copy-Confirmation-Seed-Disk.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/08/Initial-Copy-Confirmation-Seed-Disk.png" alt="Initial Copy Confirmation Seed Disk Decrease Initial Replication Bandwidth and Time with vSphere Replication" title="Initial Copy Confirmation - Seed Disk" width="574" height="161" class="aligncenter size-full wp-image-2483" /></a>

After configuring the replication we can check the replication state. In the output below we can see about 1.9MB transfered out of 1.1GB checksummed

	  
	\# vim-cmd hbrsvc/vmreplica.getState 8  
	Retrieve VM running replication state:  
	The VM is configured for replication. Current replication state: Group: GID-4d007bd1-6279-474f-8eb2-6d016bfdac97 (generation=349359825571115)  
	Group State: full sync (10% done: checksummed 1.1 GB of 10 GB, transferred 1.9 MB of 1.9 MB)  
	DiskID RDID-50435ddb-d688-47cc-af26-7cc2aa6e948e State: full sync (checksummed 1.1 GB of 10 GB, transferred 1.9 MB of 1.9 MB)  
	

If you do this for all of the VMs that used that template, you can save a significant amount of bandwidth while initially setting up the replication. 

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/save-initial-replication-bandwidth-with-vsphere-replication/" title=" Decrease Initial Replication Bandwidth and Time with vSphere Replication" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:bandwidth,clone,srm,vmdk,vmkfstools,VRMS,vSphere Replication,vtip,blog;button:compact;">vSphere Replication has a great feature that allows us to specify the seed disk for the inital sync. The idea is that you can ship a hard copy of the...</a>
</p>