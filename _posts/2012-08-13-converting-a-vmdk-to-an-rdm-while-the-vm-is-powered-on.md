---
title: Converting a VMDK to an RDM while the VM is powered on
author: Jarret Lavallee
layout: post
permalink: /2012/08/converting-a-vmdk-to-an-rdm-while-the-vm-is-powered-on/
dsq_thread_id:
  - 1406574244
categories:
  - Storage
  - VMware
  - vTip
tags:
  - clone
  - RDM
  - storage vmotion
  - vim-cmd
  - Virtual RDM
  - vmkfstools
---
I recently had a customer that inadvertently converted his virtual RDM to virtual disks. He had storage vMotioned the VM and the disks were converted to VMDKs. There are many migrations that can convert an RDM to a VMDK. Check out <a href="http://blogs.vmware.com/vsphere/2012/02/migrating-rdms-and-a-question-for-rdm-users.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2012/02/migrating-rdms-and-a-question-for-rdm-users.html']);" target="_blank">this article</a> on what to expect when migrating VMs with RDMs.

VMware has a <a href="http://kb.vmware.com/kb/3443266" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/3443266']);" target="_blank">KB article</a> on converting VMDKs to RDMs, so the customer went off and converted his VMDKs back to RDMs with out losing any data.

This got me wondering if I can do this without bringing the VM down. I decided to test this out in my lab.

**Note:** I was able to get this working. Please use the following at your own risk.

I created a VM with a VMDK and presented a new LUN. The LUN needs to be the same size as the VMDK. With the VM powered on I took a snapshot.

	  
	~ # vim-cmd vmsvc/getallvms |grep test  
	282 test [iscsi_dev] test/test.vmx winNetEnterprise64Guest vmx-07  
	~ # vim-cmd vmsvc/snapshot.create 282 test  
	Create Snapshot:  
	

Let&#8217;s confirm the snapshot chain.

	  
	~ # cd /vmfs/volumes/iscsi_dev/test  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # grep parentFileNameHint test-000001.vmdk  
	parentFileNameHint="test.vmdk"  
	

So the snapshot links back to test.vmdk. Let&#8217;s check the locks on the VMDKs.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # vmkfstools -D test-000001-delta.vmdk  
	Lock [type 10c00001 offset 138997760 v 589, hb offset 3907584  
	gen 4851, mode 1, owner 4fbbf995-325ce3c2-e7ee-bcaec58ad83d mtime 730751 nHld 0 nOvf 0]  
	Addr <4, 310, 46>, gen 584, links 1, type reg, flags 0, uid 0, gid 0, mode 600  
	len 24576, nb 1 tbz 0, cow 0, newSinceEpoch 0, zla 1, bs 1048576
	
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # vmkfstools -D test-flat.vmdk  
	Lock [type 10c00001 offset 138977280 v 582, hb offset 3907584  
	gen 4851, mode 2, owner 00000000-00000000-0000-000000000000 mtime 730756 nHld 1 nOvf 0]  
	RO Owner[0] HB Offset 3907584 4fbbf995-325ce3c2-e7ee-bcaec58ad83d  
	Addr <4, 310, 36>, gen 573, links 1, type reg, flags 0, uid 0, gid 0, mode 600  
	len 10737418240, nb 0 tbz 0, cow 0, newSinceEpoch 0, zla 3, bs 1048576  
	

Since test-flat.vmdk only has a RO lock, we can clone it to the RDM. Let&#8217;s clone the VMDK to a virtual RDM.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # vmkfstools -i test.vmdk -d rdm:/vmfs/devices/disks/naa.600144f0e8cb470000005025b86b0003 test_new.vmdk  
	Destination disk format: raw disk mapping to '/vmfs/devices/disks/naa.600144f0e8cb470000005025b86b0003'  
	Cloning disk 'test.vmdk'...  
	Clone: 100% done.  
	

Now test.vmdk should be the same as test_new.vmdk, so the snapshot should be able to link back to the RDM. We just need to link it back. First let&#8217;s get the CID of the RDM VMDK and then we will edit the snapshot VMDK to link back.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # grep CID test_new.vmdk  
	CID=f147dbae  
	parentCID=ffffffff  
	

Now edit the following lines in the test-000001.vmdk to match what we found in the RDM VMDK.

	  
	parentCID=f147dbae  
	parentFileNameHint="test_new.vmdk"  
	

Next we need to get the VM to use the test_new.vmdk and lock the RDM instead of test-flat.vmdk. The trick is to take a new snapshot. It will close the old files and then reopen the new chain, which is now linked to the RDM. Note that this will crash the VM if the RDM and the VMDK were not exactly the same size.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # vim-cmd vmsvc/snapshot.create 282 rdm  
	Create Snapshot:  
	

If we look in the vmware.log we can see the host opening the test_new.vmdk.

	  
	2012-08-11T02:44:28.797Z| vcpu-0| DISK: OPEN scsi0:0 '/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test/test-000002.vmdk' persistent R[]  
	2012-08-11T02:44:28.804Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test/test-000002-delta.vmdk" : open successful (10) size = 45056, hd = 104270632. Type 8  
	2012-08-11T02:44:28.804Z| vcpu-0| DISKLIB-DSCPTR: Opened [0]: "test-000002-delta.vmdk" (0xa)  
	2012-08-11T02:44:28.804Z| vcpu-0| DISKLIB-LINK : Opened '/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test/test-000002.vmdk' (0xa): vmfsSparse, 41943040 sectors / 20 GB.  
	2012-08-11T02:44:28.812Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test/test-000001-delta.vmdk" : open successful (14) size = 45056, hd = 103238442. Type 8  
	2012-08-11T02:44:28.812Z| vcpu-0| DISKLIB-DSCPTR: Opened [0]: "test-000001-delta.vmdk" (0xe)  
	2012-08-11T02:44:28.812Z| vcpu-0| DISKLIB-LINK : Opened '/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test/test-000001.vmdk' (0xe): vmfsSparse, 41943040 sectors / 20 GB.  
	2012-08-11T02:44:28.819Z| vcpu-0| DISKLIB-VMFS : "/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test/test_new-rdm.vmdk" : open successful (14) size = 21474836480, hd = 88918827. Type 10  
	2012-08-11T02:44:28.819Z| vcpu-0| DISKLIB-DSCPTR: Opened [0]: "test_new-rdm.vmdk" (0xe)  
	

We can check the snapshots link back to the RDM.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # vmkfstools -q test-000002.vmdk  
	Disk test-000002.vmdk is a Non-passthrough Raw Device Mapping  
	Maps to: vml.0200090000600144f0e8cb470000005025b86b0003434f4d535441  
	

Now we can commit the snapshots into the RDM.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # vim-cmd vmsvc/snapshot.removeall 282  
	Remove All Snapshots:  
	

Confirm that it is now running on the RDM.

	  
	/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/test # grep vmdk test.vmx  
	scsi0:0.fileName = "test_new.vmdk"  
	

Everything worked as I had hoped. I would not use this in a production environment as it has not been fully vetted, but it is nice to know that the option is there.

