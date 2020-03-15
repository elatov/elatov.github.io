---
title: Check if Snapshot Consolidation is Occurring in the Background on an ESX(i) Host
author: Karim Elatov
layout: post
permalink: /2012/09/check-if-snapshot-consolidation-is-occurring-in-the-background/
categories: ['storage', 'vmware']
tags: ['powercli', 'rvtools', 'vcheck', 'vm_snapshot']
---

Someone had asked me recently: What happens if the snapshot consolidation process take a long time and the task is no longer seen in the vShpere client? First I would recommend to login directly to the host and check if the VM has a running task. An example can be seen in VMware KB [1013003](http://kb.vmware.com/kb/1013003). From the KB, first find the VM_ID of your VM:


	~ # vmware-vim-cmd vmsvc/getallvms
	Vmid Name File Guest OS Version Annotation
	112 VM-1 [Datastore] VM-3/VM-3.vmx winLonghornGuest vmx-04
	128 VM-2 [Datastore] VM-3/VM-3.vmx winXPProGuest vmx-04
	144 VM-3 [Datastore] VM-3/VM-3.vmx winNetStandardGuest vmx-04


Let's say we were committing snapshots on VM-1, so our VM_ID is 112. Then check for active tasks for that VM, by running the following:


	~ # vmware-vim-cmd vmsvc/get.tasklist 112
	(ManagedObjectReference) [
	'vim.Task:haTask-112-vim.VirtualMachine.createSnapshot-3887'
	]


Each task has an identifier as well. From the above output we see that out task identifier is '3887'. If you want you can check for more information regarding that task, you can do it like so:


	~ # vmware-vim-cmd vimsvc/task_info 3887
	(vmodl.fault.ManagedObjectNotFound) {
	dynamicType = <unset>,
	faultCause = (vmodl.MethodFault) null,
	obj = 'vim.Task:3887',
	msg = "The object has already been deleted or has not been completely created",
	}


This is a pretty quick test to see if there is a snapshot commit in progress. Another thing you can do is check if there is actual changes going on with the vmdk files. When you commit a snapshot you basically take the delta files and merge them into the base disk. If you want to know more about the snapshots, I would suggest reading "[Troubleshooting Virtual Machine snapshot problems](http://virtuallyhyper.com/2012/04/vmware-snapshot-troubleshooting/)" written by Ruben Gargia. To see if there are changes happening with the vmdks you can run the following command:


For ESX:


	# cd /vmfs/volumes/Storage1/VM-1
	# watch -d "ls -l --full-time *-delta.vmdk *-flat.vmdk"


For ESXi:


	~ # cd /vmfs/volumes/datastore1/VM-1
	/vmfs/volumes/datastore1/VM-1 # watch -d 'ls -lut | grep -E "delta|flat"'


The above command is described in VMware KB [1007566](http://kb.vmware.com/kb/1007566), from that KB:

> for "watch"
> -d highlights the differences between successive updates
>
> for 'ls'
> -t sorts by modification time
> -l shows a long listing which displays additional information regarding the files themselves.
> -u sorts by and shows access time

When you run the command it will basically execute 'ls' with the above parameters every 2 seconds and any changes that occur with updated time or size differences will be highlighted.

The task timing out from the vShpere Client is actually expected. From VMware KB [1004790](http://kb.vmware.com/kb/1004790):

> vCenter has a default 15 minute timeout for any task.
> ...
> ...
>
> **Note:** In the case of snapshot consolidation, even though the VI Client timeout occurs, the operation on the ESX host is still running. You can verify by observing the .vmdk file for the virtual machine. It is updated every minute which means the delta files are being committed to the .vmdk file.

In the same KB it talks about increasing the timeout, from the KB:

> To increase the timeout values for the virtual machine migration task, add the following timeout parameter in the vpxd.cfg file:
>
>
> 	<config>
> 	..
> 	<task>
> 	<timeout>10800</timeout>
> 	</task>
> 	..
> 	</config>
>
>
> Note: The value 10800 can be changed based on your requirements. This example uses 10800 seconds, or 3 hours.

The example in the KB shows you how to change it from the default value of 15 minutes to 3 hours, probably an over kill but then you make sure the corner case of long snapshot consolidation timing out won't happen again.

Personally, I think the real fix to this issue is to follow best practices. From VMware KB [1025279](http://kb.vmware.com/kb/1025279) The title of the KB is "Best practices for virtual machine snapshots in the VMware environment". Here is the important bullet point from that KB:

> - Use no single snapshot for more than 24-72 hours.
> 	- This prevents snapshots from growing so large as to cause issues when deleting/committing them to the original virtual machine disks. Take the snapshot, make the changes to the virtual machine, and delete/commit the snapshot as soon as you have verified the proper working state of the virtual machine.
>	- Be especially diligent with snapshot use on high-transaction virtual machines such as email and database servers. These snapshots can very quickly grow in size, filling datastore space. Commit snapshots on these virtual machines as soon as you have verified the proper working state of the process you are testing.

Most of the time I see the removal task take a while, when the snapshot (delta) file is huge. If we can prevent delta files from getting large, we can prevent the task from taking more that 15 minutes to complete (under normal conditions). There are many ways to make that happen, but we need to be proactive.

The first way is to setup vCenter Alarms to warn us when VMs have snapshots. VMware KB [1018029](http://kb.vmware.com/kb/1018029) has instructions on how to set that up.

Second way is to use other tools like powerCLI to run through your VM Inventory to create list of VMs which have snapshots. Check out "[vCheck (Daily Report)](http://www.virtu-al.net/2009/06/22/powercli-snapreminder/)". You can set it as a scheduled task and it will run and generate a report of your VMware inventory. Among many other statistics it will report VMs with snapshots.

Lastly you can use third party tools like [RVtools](http://www.robware.net/) to generate a listing of VMs that have snapshots.

In conclusion there are many ways on how to check if VM is still going through snapshot consolidation. However instead of using those tools, be proactive and keep an eye on your environment and don't let your VMs have snapshots older than 3 days. Check out [VMware Snapshot Alerting and Reporting](https://www.vladan.fr/create-vcenter-alarm-vms-running-snapshots/), an example of how someone got in trouble with snapshots and started to monitor for snapshots after the incident.

### Related Posts

- [Snapshots Take a Long Time When "Keep Memory" is Enabled](http://virtuallyhyper.com/2013/04/snapshots-take-a-long-time-when-keep-memory-is-checked/)

