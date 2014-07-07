---
published: true
title: Running out of VMFS Heap on an ESX Host
author: Karim Elatov
layout: post
permalink: /2012/08/running-out-of-vmfs-heap-on-an-esx-host/
dsq_thread_id:
  - 1406386850
categories: ['storage', 'vmware']
tags: ['maxheapsizemb', 'unified_vmfs_block_size', 'vaai', 'vmfs_heap', 'vmfs']
---

Recently I ran into an issue where we were running out of VMFS3 Heap. We would see the following in the logs:


	2012-07-20T04:34:19.377Z cpu22:6518)WARNING: Heap: 2900: Heap_Align(vmfs3, 6184/6184 bytes, 8 align) failed. caller: 0x418031efc4e9
	2012-07-20T04:35:36.596Z cpu2:193761)WARNING: Heap: 2525: Heap vmfs3 already at its maximum size. Cannot expand.
	2012-07-20T04:36:55.375Z cpu5:8496)WARNING: Heap: 2900: Heap_Align(vmfs3, 6184/6184 bytes, 8 align) failed. caller: 0x418031efc4e9


I grabbed the logs from all the hosts in the clusters to get a feeling for how much space we are using. In the logs you can check out the *vmware-vimdump.txt* file and that will have the description of all the VMs. If you want to check all the flat files in a host's inventory you can run the following:


	$ grep "-flat.vmdk" vmware-vimdump.txt -A 3
	name = '[Datastore] vm/vm-flat.vmdk',
	type = 'diskExtent',
	size = 33130807296L
	..
	..


The list keeps going. If you want to see the sizes of all the VMDKs you can do this:


	$ grep "label = 'Hard disk" vmware-vimdump.txt -A 1 | grep summary| awk '{print $3, $4}' | head -10
	'41,943,040 KB'
	'10,485,760 KB'
	'20,971,520 KB'
	'41,943,040 KB'
	'262,144,000 KB'
	'41,943,040 KB'
	'10,485,760 KB'
	'41,943,040 KB'
	'10,485,760 KB'
	'523,239,424 KB'


If you want to see the whole list don't pipe the command to *head*. So I first wanted to see all the VMDK sizes across all the hosts. In my scenario I had 8 hosts, my extracted logs looked like this:


	$ for log in `ls -d esx-*`; do echo $log; done
	esx-host1.com-2012-08-20--19.28
	esx-host2.com-2012-08-20--19.36
	esx-host3.com-2012-08-20--19.44
	esx-host4.com-2012-08-20--19.52
	esx-host5.com-2012-08-20--19.21
	esx-host6.com-2012-08-20--19.59
	esx-host7.com-2012-08-20--20.07
	esx-host8.com-2012-08-20--20.15


Now to list the sum of VMDKs per host in KiloBytes we can do the following:


	$ for log in `ls -d esx-*`; do echo $log; sum=0;for vmdk in `grep "label = 'Hard disk" $log/commands/vmware-vimdump.txt -A 1 | grep summary| awk '{print $3}' | cut -d \' -f 2 | sed -e s/,//g`; do ((sum+=$vmdk)); done ; echo $sum; done
	esx-host1.com-2012-08-20--19.28
	16191900876
	esx-host2.com-2012-08-20--19.36
	26760540325
	esx-host3.com-2012-08-20--19.44
	17979932671
	esx-host4.com-2012-08-20--19.52
	17220763648
	esx-host5.com-2012-08-20--19.21
	513802240
	esx-host6.com-2012-08-20--19.59
	13561023691
	esx-host7.com-2012-08-20--20.07
	5149556735
	esx-host8.com-2012-08-20--20.15
	7482680278


Converting the values to TB here is what we get:


	$ for log in `ls -d esx-*`; do echo $log; sum=0;for vmdk in `grep "label = 'Hard disk" $log/commands/vmware-vimdump.txt -A 1 | grep summary| awk '{print $3}' | cut -d \' -f 2 | sed -e s/,//g`; do ((sum+=$vmdk)); done ; tb=`echo "scale=2;$sum / 1024 / 1024 / 1024"| bc -l`; echo $tb; done
	esx-host1.com-2012-08-20--19.28
	15.07
	esx-host2.com-2012-08-20--19.36
	24.92
	esx-host3.com-2012-08-20--19.44
	16.74
	esx-host4.com-2012-08-20--19.52
	16.03
	esx-host5.com-2012-08-20--19.21
	.47
	esx-host6.com-2012-08-20--19.59
	12.62
	esx-host7.com-2012-08-20--20.07
	4.79
	esx-host8.com-2012-08-20--20.15
	6.96


Now getting a grand total of all of that, I get the following:


	$ tbsum=0;for log in `ls -d esx-*`; do echo $log; sum=0; for vmdk in `grep "label = 'Hard disk" $log/commands/vmware-vimdump.txt -A 1 | grep summary| awk '{print $3}' | cut -d \' -f 2 | sed -e s/,//g`; do ((sum+=$vmdk)); done ; tb=`echo "scale=2;$sum / 1024 / 1024 / 1024"| bc -l`; tbsum=`echo "scale=2;$tb+$tbsum"|bc -l`; echo $tb; done ;echo $tbsum
	esx-host1.com-2012-08-14--19.28
	15.07
	esx-host2.com-2012-08-20--19.36
	24.92
	esx-host3.com-2012-08-20--19.44
	16.74
	esx-host4.com-2012-08-20--19.52
	16.03
	esx-host5.com-2012-08-20--19.21
	.47
	esx-host6.com-2012-08-20--19.59
	12.62
	esx-host7.com-2012-08-20--20.07
	4.79
	esx-host8.com-2012-08-20--20.15
	6.96
	97.60


So we are approximately using 100TB of space across all the eight hosts. The issue would come up when we would consolidate the cluster to about 2 or 3 hosts. That would mean that we would have about either 50TB per host (with 2 hosts) or 33TB per host (with 3 hosts). Now looking at VMware KB [1004424](http://kb.vmware.com/kb/1004424). We can see that setting the *VMFS3.MaxHeapSizeMB* to 256MB we should be able to handle 64TB of open space. Checking our hosts, we already had that option set:


	$ for log in `ls -d esx-*`; do echo $log; grep '\.MaxHeapSizeMB' -A 1 $log/commands/esxcfg-info_-a.txt; done
	esx-host1.com-2012-08-20--19.28
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host2.com-2012-08-20--19.36
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host3.com-2012-08-20--19.44
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host4.com-2012-08-20--19.52
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host5.com-2012-08-20--19.21
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host6.com-2012-08-20--19.59
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host7.com-2012-08-20--20.07
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256
	esx-host8.com-2012-08-20--20.15
	|----Option Name..................................MaxHeapSizeMB
	|----Current Value................................256


Now that KB has a very theoretical calculation. If there were no other resources (ie just open VMDKs) then we could reach that. But if we have VAAI enabled and are using ATS, or if we use SIOC enabled on the Datastores, then these things also contribute to the VMFS heap. As we know VMFS5 uses a Unified 1MB Block size and if we have a VMDK bigger than 256GB, which is the max file size with that block size for VMFS3 (block size of 1MB), then this also uses more VMFS heap. More information on the new features of VMFS5 can be seen in the VMware blog entitled "[Low Level VAAI Behaviour](http://blogs.vmware.com/vsphere/2011/07/new-vsphere-50-storage-features-part-1-vmfs-5.html)".
All of these things make it very hard to calculate VMFS heap usage. If you want to check the current usage, you can do the following:


	~ # vsish
	/> cat /system/heaps/vmfs3-0x410016400000/stats
	Heap stats {
	Name:vmfs3
	dynamically growable:1
	physical contiguity:MM_PhysContigType: 1 -> Any Physical Contiguity
	lower memory PA limit:0
	upper memory PA limit:-1
	may use reserved memory:0
	memory pool:19
	# of ranges allocated:2
	dlmalloc overhead:1008
	current heap size:12587984
	initial heap size:2097152
	current bytes allocated:10620048
	current bytes available:1967936
	current bytes releasable:4000
	percent free of current size:15
	percent releasable of current size:0
	maximum heap size:83886080
	maximum bytes available:73266032
	percent free of max size:87
	lowest percent free of max size ever encountered:84


Keep an eye on the *percent free of max size* option, that is what your is heap currently at, and then also check out *lowest percent free of max size ever encountered*, this will tell you what the lowest value the heap has ever been. If the latter option is getting close to 20% then you might want to think about increasing your *MaxHeapSizeMB* setting per the instructions laid out in VMware KB [VMFS Heap Considerations](http://kb.vmware.com/kb/1004424)", and it talks about the default values for different versions of ESX(i) and it makes recommendations for how much space can be handled for each. From the blog:

> As a rule of thumb, we are conservatively estimating that a single ESXi host should have enough default heap space (80MB) to address around 10TB of open files/VMDKs on a VMFS-5 volume.
> ...
> ...
> If you change the advanced setting VMFS3.MaxHeapSizeMB to the maximum amount of heap (which is 256MB), we again conservatively estimate that about 30TB of open files/VMDKs can be addressed by that single ESXi host.

That is much more realistic estimation of how much open space can be handled by the different heap sizes. With the above recommendation we consolidated our cluster to 5 hosts, this way we would have about 20TB per host. Also, if ever needed to upgrade our servers then we would do a rolling reboot and one host would be down. In that scenario we would be down to 4 hosts with 25TB for each hosts and that is still acceptable.

