---
title: VMware Snapshot Troubleshooting
author: Jarret Lavallee
layout: post
permalink: /2012/04/vmware-snapshot-troubleshooting/
dsq_thread_id:
  - 1404673028
categories:
  - Storage
  - VMware
tags:
  - clone
  - command line
  - quiesce
  - snapshots
  - Storage
  - troubleshooting
  - vmkfstools
  - vss
---
For a long time I was consistently looking into <a href="http://kb.vmware.com/kb/1015180" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1015180']);">VMware snapshot</a> issues. I developed a small course to teach basic snapshot troubleshooting snapshots along with some more advanced snapshot troubleshooting techniques. The course has been converted to this article.

The basics about snapshot are discussed in this <a href="http://kb.vmware.com/kb/1025279" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1025279']);">VMware KB</a>. In this article we will touch base on the basic snapshot operations and data safe operations.

The first thing to understand is how to properly <a href="http://kb.vmware.com/kb/1007849" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1007849']);" target="_blank">consolidate snapshots correctly</a>. If this operation fails we have to investigate the different types of errors and then troubleshoot further. Before we touch on this let&#8217;s take a look at the basic snapshot operations.

## Snapshot Operations

### Take Snapshot

We generally see snapshots taken through the API because of backup products, but they can also be taken through the vSphere Client as well. Page 145 of the <a href="http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf']);" target="_blank">Virtual Machine Administration Guide</a> describes the process of taking a snapshot.

> 1 Select Inventory > Virtual Machine > Snapshot > Take Snapshot.
> 
> 2 Type a name for your snapshot.
> 
> 3 (Optional) Type a description for your snapshot.
> 
> 4 (Optional) Select the Snapshot the virtual machine’s memory check box to capture the memory of the virtual machine.
> 
> **NOTE ** Capturing the virtual machine&#8217;s memory results in a powered off snapshot, even if the virtual machine is powered on.
> 
> 5 (Optional) Select the Quiesce guest file system (Needs VMware Tools installed) check box to pause running processes on the guest operating system so that file system contents are in a known consistent state when you take the snapshot. This step applies only to virtual machines that are powered on.
> 
> 6 Click OK. When you take the snapshot it is listed in the Recent Tasks field at the bottom of the vSphere Client.
> 
> 7 Click the target virtual machine to display tasks and events for this machine or, while the virtual machine is selected, click the Tasks & Events tab.

More information on Quiesced snapshots can be found in <a href="http://kb.vmware.com/kb/1015180" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1015180']);" target="_blank">this KB</a>. If you are having trouble taking a quiesced snapshot please see <a href="http://kb.vmware.com/kb/1007696" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1007696']);" target="_blank">this KB</a>, or <a href="http://kb.vmware.com/kb/1031298" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1031298']);" target="_blank">this KB if you are using Windows 2008 (R2)</a>.

Let&#8217;s take a look at the files that are created in a snapshot operation.

Files in the directory before the snapshot operation.

	# ls  
	vmware-1.log vps-0264bf9d.vswp vps.vmsd  
	vmware-2.log vps-flat.vmdk vps.vmx  
	vmware.log vps.nvram vps.vmxf  
	vmx-vps-40157085-1.vswp vps.vmdk  
	

Let&#8217;s check out what disk the VM is running on.

	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps.vmdk&quot;

Now I took a snapshot through the vSphere Client and there are three new files (I did not include the VM&#8217;s memory when taking the snapshot). The actual snapshot is the newly created disk: vps-000001.vmdk and vps-000001-delta.vmdk. The other file, vps-Snapshot1.vmsn, is the snapshot memory file. See the &#8220;Do not trust the Snapshot Manager!&#8221; section for more information on this file.

	# ls  
	vmware-1.log vps-000001.vmdk vps.vmdk  
	vmware-2.log vps-0264bf9d.vswp vps.vmsd  
	vmware.log vps-Snapshot1.vmsn vps.vmx  
	vmx-vps-40157085-1.vswp vps-flat.vmdk vps.vmxf  
	vps-000001-delta.vmdk vps.nvram

Let&#8217;s check to see what disk the VM is running off of. We can see that it is now running off of the snapshot vps-000001.vmdk.

	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000001.vmdk&quot;

vps-000001.vmdk is a descriptor file that points to the data file. In the case of a snapshot this is a -delta file, so it contains the information about vps-000001-delta.vmdk. In the file we see parentFileNameHint which points to the descriptor of this snapshot&#8217;s parent. Since there is only one snapshot, this points to the base disk.

	# cat vps-000001.vmdk  
	\# Disk DescriptorFile  
	version=1  
	encoding=&quot;UTF-8&quot;  
	CID=4f5b98ad  
	parentCID=79229daf  
	isNativeSnapshot=&quot;no&quot;  
	createType=&quot;vmfsSparse&quot;  
	parentFileNameHint=&quot;vps.vmdk&quot;  
	\# Extent description  
	RW 20971520 VMFSSPARSE &quot;vps-000001-delta.vmdk&quot;
	
	\# The Disk Data Base  
	#DDB
	
	ddb.longContentID = &quot;193b848abd4542a6593461434f5b98ad&quot;  
	

In the descriptor above we also see a CID and parentCID. These are unique IDs for the disks and snapshots on a system. The CID is ID for this disk/snapshot. The parentCID is the CID of the parent of this disk/snapshot. We will touch more on this in the advanced troubleshooting.

### Revert to Snapshot

Reverting will restore the state of the VM when the snapshot was taken. It is also known as Restoring a snapshot. Reverting to a snapshot will **destroy all data** since the snapshot was taken so make sure to have backups before doing this operation. Page 148 of the <a href="http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf']);" target="_blank">Virtual Machine Administration Guide</a> describes the process of reverting to a snapshot.

> 1 Select Inventory > Virtual Machine > Snapshot > Snapshot Manager.
> 
> 2 In the Snapshot Manager, click a snapshot to select it.
> 
> 3 Click the Go to button to restore the virtual machine to any snapshot.
> 
> **NOTE ** Virtual machines running certain kinds of workloads might take several minutes to resume  
> responsiveness after reverting from a snapshot. This delay can be improved by increasing the guest  
> memory.
> 
> 4 Click Yes in the confirmation dialog box.

The underlying process is that it will take a new snapshot (remember that a snapshot is just a delta file) as a child of the parent disk. So you will still be running off of a snapshot until a &#8220;delete&#8221; operation takes place. To illustrate this we need to look at the command line before and after the snapshot &#8220;delete&#8221;.

As with the example in Taking a Snapshot, we have a single snapshot vps-000001.vmdk. Below is the directory listing of only the vmdks and the disk that the VM is running on.

	# ls *.vmdk  
	vps-000001-delta.vmdk vps-flat.vmdk  
	vps-000001.vmdk vps.vmdk
	
	\# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000001.vmdk&quot;  
	

I used the instructions above to revert to a previous snapshot. Since there is only a single snapshot on this VM I selected the snapshot and hit GO TO. After the snapshot reverted let&#8217;s take a look at the vmdks and the disk that the VM is running on. We notice that we are now running on a snapshot called vps-000002.vmdk and that vps-000001.vmdk is no longer there.

	# ls *.vmdk  
	vps-000002-delta.vmdk vps-flat.vmdk  
	vps-000002.vmdk vps.vmdk
	
	\# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000002.vmdk&quot;  
	

When doing a snapshot revert, the current snapshot (delta disk) will be removed and a new one will be created linking to the parent disk. Let&#8217;s confirm the parentFileNameHint in the new snapshot, vps-000002.vmdk. We can see that it does in fact link to the base disk.

	# grep parentFileNameHint vps-000002.vmdk  
	parentFileNameHint=&quot;vps.vmdk&quot;

To get back to the base disk we will need to &#8220;delete&#8221; the snapshot after reverting. The main concept is that the base disk in this case contains the state that we want to revert to, but reverting to the snapshot will leave a snapshot. So in order to revert to the original state and get off of a snapshot we need to run the revert and then run a &#8220;delete&#8221; operation on the snapshot.

I went in and &#8220;deleted&#8221; the snapshot and we no longer see any snapshots on the VM.

	# ls *.vmdk  
	vps-flat.vmdk vps.vmdk
	
	\# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps.vmdk&quot;

### Deleting Snapshots

The &#8220;delete&#8221; operation has a very deceptive name. &#8220;Deleting&#8221; a snapshot actually commits the new changes in the snapshot to the parent disk and then removes the snapshot files. Page 147 of the <a href="http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf']);" target="_blank">Virtual Machine Administration Guide</a> describes the process of &#8220;deleting&#8221; a snapshot.

> 1 Select Inventory > Virtual Machine > Snapshot > Snapshot Manager.
> 
> 2 In the Snapshot Manager, select a snapshot by clicking it.
> 
> 3 Click Delete to permanently remove a snapshot from vCenter Server.
> 
> **NOTE** Clicking &#8220;Delete All&#8221; permanently removes all snapshots from the virtual machine.
> 
> **NOTE** The &#8220;Delete&#8221; operation commits the snapshot data to the parent and removes the selected snapshot. The &#8220;Delete All&#8221; operation commits all the immediate snapshots before the &#8220;You are here&#8221; current state to the base disk and removes all existing snapshots for that virtual machine.
> 
> 4 Click Yes in the confirmation dialog box.

This is the most common operation for a snapshot. Backup software will &#8220;delete&#8221; the snapshot so that the new data is pushed back into the base disk and the VM is no longer running on a snapshot.

There are two options for doing a commit: &#8220;delete&#8221; and &#8220;delete all&#8221;. The &#8220;delete&#8221; option commits a single snapshot&#8217;s changes into it&#8217;s parent disk and then removes the snapshot files. The &#8220;Delete All&#8221; option commits all of the changes in the current chain back to the base disk and removes all snapshot files. Another consideration is that if there are multiple snapshot chains on the VM, &#8220;Delete All&#8221; will commit the current running state of the VM back into the base disk.

To illustrate what happens when we do a single &#8220;delete&#8221; operation, I have taken two snapshots on a VM. Below we can see the snapshot files and the chain.

	# ls *.vmdk  
	vps-000001-delta.vmdk vps-000002-delta.vmdk vps-flat.vmdk  
	vps-000001.vmdk vps-000002.vmdk vps.vmdk
	
	\# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000002.vmdk&quot;
	
	\# grep parentFileNameHint vps-00000?.vmdk  
	vps-000001.vmdk:parentFileNameHint=&quot;vps.vmdk&quot;  
	vps-000002.vmdk:parentFileNameHint=&quot;vps-000001.vmdk&quot;  
	

So let&#8217;s actually look at the sizes of the snapshots. Snapshots will grow by 16MB chunks. We can see that there is 0 data in vps-000001-delta.vmdk since it is only taking up one sub block (Look for a post about VMFS structure later) of 24k. vps-000002-delta.vmdk is 32MB, so it has more than 16MB of changes in it, but less than 32MB.

	# ls -lh *delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 24.0k Apr 9 19:43 vps-000001-delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 32.0M Apr 9 19:52 vps-000002-delta.vmdk

I now went in and &#8220;deleted&#8221; the second created snapshot, vps-000002.vmdk. The size reflects the changes that were committed to vps-000002.vmdk&#8217;s parent snapshot vps-000001.vmdk. vps-000001-delta.vmdk is now 32MB, which contains the changes that were in vps-000002-delta.vmdk.

	# ls -lh *delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 32.0M Apr 9 19:56 vps-000001-delta.vmdk  
	

Since the VM was in a running state, we needed a place to write the new changes while we were actively committing vps-000002.vmdk. To have a place to write the changes, we create a new snapshot that gets committed after vps-000002.vmdk is finished committing. I ran a &#8220;ls&#8221; while vps-000002.vmdk was being committed and it shows that vps-000003.vmdk was created to hold the changes during the commit.

	# ls -lh *delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 16.0M Apr 9 19:56 vps-000001-delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 32.0M Apr 9 19:56 vps-000002-delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 24.0k Apr 9 19:56 vps-000003-delta.vmdk  
	

In the output above we can also see that vps-000001-delta.vmdk is increasing in size as the changes from vps-000002-delta.vmdk are getting pushed into it. At this point in the commit it had written less than 16MB into vps-000001-delta.vmdk.

## Basic Snapshot Troubleshooting

### Determine if a VM has a Snapshot

#### Do not trust the Snapshot Manager!

The snapshot manager is a great utility, but it often has the wrong information in it. It can show that there are no snapshots on the VM when in reality the VM has snapshots. The problem was that the snapshot commit process actually removes the entry from the snapshot manager configuration file before it commits the snapshot. So we would see the snapshot manager showing that there are no snapshots, where the VM actually has many snapshots on it. <a href="http://kb.vmware.com/kb/1002310_draft" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002310_draft']);" target="_blank">VMware has a KB</a> on how to commit these snapshots.

The snapshot manager gets it&#8217;s information from a configuration file in the VM&#8217;s directory. This file is named.vmsd. It is the virtual machine snapshot descriptor file. Below we have an example of a .vmsd with a single snapshot in it.

	# cat vps.vmsd  
	.encoding = &quot;UTF-8&quot;  
	snapshot.lastUID = &quot;4&quot;  
	snapshot.current = &quot;2&quot;  
	snapshot0.uid = &quot;2&quot;  
	snapshot0.filename = &quot;vps-Snapshot2.vmsn&quot;  
	snapshot0.displayName = &quot;test1&quot;  
	snapshot0.createTimeHigh = &quot;310596&quot;  
	snapshot0.createTimeLow = &quot;938781285&quot;  
	snapshot0.numDisks = &quot;1&quot;  
	snapshot0.disk0.fileName = &quot;vps.vmdk&quot;  
	snapshot0.disk0.node = &quot;scsi0:0&quot;  
	snapshot.numSnapshots = &quot;1&quot;  
	

We can see that snapshot.numSnapshots = 1, so we only have a single snapshot. That snapshot is identified by the displayName, test1, and refers to vps-Snapshot2.vmsn. The vps-Snapshot2.vmsn file is the snapshot memory file. It actually contains a little more than just the memory. If you were to hexdump this file you would see that it is a binary file that contains a copy of the vmx at the time and more. The file points to the delta disk files as well. So this file would contain everything needed to restore to the state the VM was running at when the snapshot was taken. In this case we did not take the memory in the snapshot so it is small and does not contain the memory dump. A list of VMware files can be found <a href="https://www.vmware.com/support/ws55/doc/ws_learning_files_in_a_vm.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/support/ws55/doc/ws_learning_files_in_a_vm.html']);" target="_blank">here</a>.

Back to the Snapshot Manager, we can see that the .vmsd file is really just a text file that contains snapshot information. If this file has a syntax error or it was not updated properly, the snapshot manager would not have the correct information. It is always worth verifying if the VM actually has snapshots.

#### Using the command line to see if a VM has snapshots

The best way to determine if a VM is running on a snapshot is to query the VMX file to see what the disk it is has attached. There may be snapshot files in the VM&#8217;s directory that are not actually attached to the VM or there may be many different snapshot chains, but the VMX has the current chain.

In the example below we can see that the VM is running of snapshot vps-000001.vmdk.

	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000001.vmdk&quot;

In the example below the VM is running of a base disk on a different datastore.

	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;/vmfs/volumes/4e4043f8-160ce551-98d6-00221591be89/vps/vps.vmdk&quot;

#### Old Snapshot files can be left around in the VM&#8217;s Directory

It is not uncommon to find VMs that have old snapshot laying around that are not actually attached. This happens for various reasons. Most times it happens when someone has manually modified the VMX or cloned the VM. Before modifying anything, it is best to confirm that the snapshots are not actually in use.

To confirm we go to the command line and see what disk the VM is running on.

	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps.vmdk&quot;

In this case it is running off of the base disk, so let&#8217;s look at the VMDKs in the VM&#8217;s directory.

	# ls *.vmdk  
	vps-000001-delta.vmdk vps-000001.vmdk vps-flat.vmdk vps.vmdk  
	

We can see above that there is indeed a snapshot in the directory that is not in use by this VM. Since this VM is turned on and using the base disk, this snapshot would be invalidated. Let&#8217;s confirm that it was pointing to the base disk, vps.vmdk.

	# grep parentFileNameHint vps-000001.vmdk  
	parentFileNameHint=&quot;vps.vmdk&quot;  
	

Since the parentFileNameHint is vps.vmdk, we know that it was pointing to the base disk. Since the timestamp of the vps-flat.vmdk is newer than the vps-000001-delta.vmdk, this snapshot is likely invalidated.

	# ls -lrt *.vmdk  
	-rw&#8212;&#8212;- 1 root root 332 Apr 9 20:01 vps-000001.vmdk  
	-rw&#8212;&#8212;- 1 root root 33579008 Apr 9 22:08 vps-000001-delta.vmdk  
	-rw&#8212;&#8212;- 1 root root 513 Apr 9 22:10 vps.vmdk  
	-rw&#8212;&#8212;- 1 root root 10737418240 Apr 9 22:11 vps-flat.vmdk  
	

We can move these files out of the way and remove them at a later time. The idea behind removing them later is for the sake of data integrity. If you remove a file that contains important data, it could cost thousands of dollars to get a datarecovery company to recover it. My policy is to always create a deleteme folder and move the file there. In a week or so I will go back and remove the file.

	# mkdir deleteme  
	\# mv vps-000001.vmdk vps-000001-delta.vmdk deleteme/  
	

### Committing Snapshots

#### Delete All Snapshots

The &#8220;Delete All&#8221; option will commit the current state of the VM into the base disk and get rid of all of the snapshot files. This will clean up the snapshots and get the VM back on the base disk even if the snapshots are not showing up in Snapshot Manager.

If the &#8220;Delete All&#8221; operation has previously failed for any reason or if there are many snapshots on the VM, it should not be considered a Data Safe operation. In this situation, you should consider that the backups may not be complete or working. It is worth taking the extra time to get a file level backup before doing a snapshot commit. The reason that it is not considered safe is because it modifies the original files. There is no &#8220;undo button&#8221; for a snapshot commit, so make sure that the VM is in the right state before doing the &#8220;delete all&#8221;. That said, I have not seen an issue where a customer has run into data loss with a &#8220;delete all&#8221;.

If the VM has not had any problems doing a commit and the snapshots are not very large a &#8220;Delete All&#8221; operation is the best choice. The downsides come when there are many snapshots or the snapshots are very large. When the snapshots are very large it can take a long time for the host to read the snapshot data, calculate the current state of the data, and then write it back to the base disk one snapshot at a time. This is also very I/O intensive and has been seen to <a href="http://kb.vmware.com/kb/1002836" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002836']);" target="_blank">hang VMs</a>. It is a better idea to commit large snapshot in non production hours to avoid downtime and responsiveness issues.

When using &#8220;Delete All&#8221; snapshots, ESX/ESXi 4.0U2+ will commit the snapshots one by one into the base disk. This was changed from the previous versions where it would commit the snapshots from top to bottom. Since committing the snapshots from top to bottom would inflate the intermediate snapshots and take a large amount of space. This would often cause customers to run out of space when committing snapshots. More information about the process and space utilization can be found <a href="http://vmutils.t15.org/TVMsp/TVMsp.html#SPACE_NEEDED" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://vmutils.t15.org/TVMsp/TVMsp.html#SPACE_NEEDED']);" target="_blank">here</a>.

### Cloning Snapshots

#### Always Clone Snapshots!

Say that you were to find a VM that has snapshots on it. It could have been running off of these snapshots for a very long time, which means that you have a lot of data in the delta files. If you are using a VMDK level backup solution, you can assume that your backups are invalid as they would have been backing up the delta files. Why would you want to risk any of that data (possibly your job)?

Always clone the snapshots if there is any doubt to the backups or the integrity of the data. Cloning will not modify the original snapshots so we can always go back to the original files if we encounter problems. It is considered a data safe procedure for data integrity.

Another benefit is that cloning the snapshots is faster that committing when the snapshots are large. Cloning will read through the snapshots an determine the current state of the snapshots and then write that to a new file. This means that the maximum amount of data written will be up to the size of the base disk. Deleting snapshots can write much more.

#### VMDK level clones

Clones can be taken from the VM level and from the VMDK level. The VMDK level clones offer better flexibility in terms of what snapshot to clone from along with where it is going. The downside is that the VM should be off for the process.

When cloning a VMDK the new VMDK will not have any snapshots, but it will contain all of the data of the last snapshot that it was cloned from. There are many benefits to VMDK level clones listed below.

*   A cloned VMDK does not have any snapshots
*   Flexible
*   Can clone one VMDK at a time
*   Can clone from different snapshot levels
*   Can be canceled safely

<a href="http://kb.vmware.com/kb/1027876" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1027876']);" target="_blank">So how do we clone a VMDK</a>? Well we do this from the command line. The first thing to do is figure out what snapshot we want to clone, so determine which snapshot you want to clone and then find a location to clone it. Once you know where you can put the new clones you can use the vmkfstools command to clone the VMDK.

The syntax for the clone is below

	
	
	This example will clone the current snapshot to the same folder with a new name. The disk will be in ZeroedThick format.
	
	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000001.vmdk&quot;
	
	\# vmkfstools -i vps-000001.vmdk vps.new.vmdk  
	Destination disk format: VMFS zeroedthick  
	Cloning disk &#8216;vps-000001.vmdk&#8217;&#8230;  
	Clone: 100% done.  
	

The example below will do the same thing, but make the destination disk thin provisioned.

	# grep vmdk vps.vmx  
	scsi0:0.fileName = &quot;vps-000001.vmdk&quot;
	
	\# vmkfstools -d thin -i vps-000001.vmdk vps.new.vmdk  
	Destination disk format: VMFS thin-provisioned  
	Cloning disk &#8216;vps-000001.vmdk&#8217;&#8230;  
	Clone: 100% done.  
	

The example below will clone the snapshot to another datastore using thin.

	# vmkfstools -d thin -i vps-000001.vmdk /vmfs/volumes/iscsi_dev/vps/vps.vmdk  
	Destination disk format: VMFS thin-provisioned  
	Cloning disk &#8216;vps-000001.vmdk&#8217;&#8230;  
	Clone: 100% done  
	

#### VM Level Clones

If you feel more comfortable in the vSphere Client, or if you want a copy of the whole VM, then a VM level clone is a great option. As with the VMDK level clones the new VM will not have any snapshots and will be at the current state of the VM. This can be done with the VM on or off, but the clone will only have the data up to when the clone was initiated. vCenter is required for this operation.

Page 34 of the <a href="http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsphere4/r41/vsp_41_vm_admin_guide.pdf']);" target="_blank">Virtual Machine Administration Guide</a> describes the process of cloning the VM.

> 1 Right-click the virtual machine and select Clone.
> 
> 2 Enter a virtual machine name, select a location, and click Next.
> 
> 3 Select a host or cluster on which to run the new virtual machine.
> 
> 4 Select a resource pool in which to run the clone and click Next.
> 
> 5 Select the datastore location where you want to store the virtual machine files and click Next.
> 
> 6 Select the format for the virtual machine&#8217;s disks and click Next.
> 
> 7 Select a guest operating system customization option.
> 
> 8 Review your selections, and select whether to power on or edit the virtual machine.

### Advanced Snapshot Troubleshooting

There are many problems that one can run into with snapshot problems. The issues below are advanced and can be fixed with a little work. I will do a write up for each one and update this list to link to each article.

*   <a title="Non-Linear Snapshot Chain" href="http://virtuallyhyper.com/index.php/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/index.php/2012/04/advanced-snapshot-troubleshooting-non-linear-vmware-snapshot-chain/']);">Non-Linear Snapshot Chain</a>
*   <a href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-invalid-parentcidcid-chain/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-invalid-parentcidcid-chain/']);" title="Advanced Snapshot Troubleshooting: Invalid parentCID/CID chain" target="_blank">Invalid parentCID/CID chain</a>
*   <a href="http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-incorrect-vmdk-geometry/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/04/advanced-snapshot-troubleshooting-incorrect-vmdk-geometry/']);" title="Advanced Snapshot Troubleshooting: Incorrect VMDK Geometry" target="_blank">Incorrect VMDK Geometry</a>
*   Missing VMDK Descriptors
*   Parent Disk Modified in a Snapshot Chain
*   Concurrent Access
*   Locked VMDK

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Virtual Machine Clone Fails with &#8216;A general system error occurred: Configuration information is inaccessible&#8217; Error Message" href="http://virtuallyhyper.com/2012/10/virtual-machine-clone-fails-with-a-general-system-error-occurred-configuration-information-is-inaccessible/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/10/virtual-machine-clone-fails-with-a-general-system-error-occurred-configuration-information-is-inaccessible/']);" rel="bookmark">Virtual Machine Clone Fails with &#8216;A general system error occurred: Configuration information is inaccessible&#8217; Error Message</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="Converting a VMDK to an RDM while the VM is powered on" href="http://virtuallyhyper.com/2012/08/converting-a-vmdk-to-an-rdm-while-the-vm-is-powered-on/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/converting-a-vmdk-to-an-rdm-while-the-vm-is-powered-on/']);" rel="bookmark">Converting a VMDK to an RDM while the VM is powered on</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="PowerCLI Script to Identify Which VM is using an RDM LUN Identified by the NAA-ID of the LUN" href="http://virtuallyhyper.com/2012/06/powercli-script-identify-which-vm-using-rdm-lun-identified-naa-id-lun/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/06/powercli-script-identify-which-vm-using-rdm-lun-identified-naa-id-lun/']);" rel="bookmark">PowerCLI Script to Identify Which VM is using an RDM LUN Identified by the NAA-ID of the LUN</a>
    </li>
    <li class="SPOSTARBUST-Related-Post">
      <a title="VMs Losing High Number of Pings When Consolidating Snapshots" href="http://virtuallyhyper.com/2012/06/vms-losing-high-number-pings-when-consolidating-snapshots/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/06/vms-losing-high-number-pings-when-consolidating-snapshots/']);" rel="bookmark">VMs Losing High Number of Pings When Consolidating Snapshots</a>
    </li>
  </ul>
</div>

