---
title: 'Virtual Machine Clone Fails with &#8216;A general system error occurred: Configuration information is inaccessible&#8217; Error Message'
author: Karim Elatov
layout: post
permalink: /2012/10/virtual-machine-clone-fails-with-a-general-system-error-occurred-configuration-information-is-inaccessible/
dsq_thread_id:
  - 1405927143
categories:
  - Storage
  - VMware
tags:
  - Change Block Tracking
  - clone
  - CTK
  - IDE Hard Disk
  - ide0:0.ctkEnabled
---
Recently ran into an issue when cloning a VM. The clone would start and would run and at about 99% it would fail with the following error:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/clone_fail_1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/clone_fail_1.png']);"><img class="alignnone size-full wp-image-4140" title="clone_fail_1" src="http://virtuallyhyper.com/wp-content/uploads/2012/10/clone_fail_1.png" alt="clone fail 1 Virtual Machine Clone Fails with A general system error occurred: Configuration information is inaccessible Error Message" width="1154" height="178" /></a>

Checking out the /var/log/vmware/hostd.log file, I saw the following error:

	  
	[2012-10-03 22:19:06.743 62040B90 error 'App' opID=D6A05DBB-0000170C-d4-bd-7b] Failed to get data ring: vmodl.fault.InvalidArgument  
	[2012-10-03 22:19:06.783 62040B90 error 'vm:/vmfs/volumes/4f5275da-25b5f33c-40e5-0019b9d0aecd/New Virtual Machine/New Virtual Machine.vmx' opID=D6A05DBB-0000170C-d4-bd-7b] vim.VirtualMachine vim.VirtualMachine:512 does not have any configuration information.  
	

It looks like as it was creating the newly cloned VM, it would fail with some invalid configuration message. I actually ran across VMware KB <a href="http://kb.vmware.com/kb/2012959" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2012959']);">2012959</a>. The KB matched my above message and from KB here are the symptoms:

> Possible scenarios to consider:
> 
> *   Cloning an ide-disk virtual machine to the same ESX/ESXi 4.x host with CBT enabled fails
> *   Cloning an ide-disk virtual machine from ESX/ESXi 4.x host to ESXi 5.0 host with CBT enabled is successful.
> *   Cloning a SCSI-disk virtual machine from ESX/ESXi 4.x host to another ESX/ESXi 4.x host is successful.
> 
> This KB only applies if all of the following statements are true:
> 
> *   The VM in question uses IDE disks and Change Block Tracking (also referred to as CTK)
> *   vCenter Server version is 5.0 or higher
> *   The ESX(i) Server holding the VM is on version 4.x

First I wanted to check if this vm has CTK enabled. Looking at the vmx file, I see the following:

	  
	/vmfs/volumes/4f5275da-25b5f33c-40e5-0019b9d0aecd/vm/ # grep ide0 vm.vmx | grep ctk  
	ide0:0.ctkEnabled = "TRUE"  
	

That was the case. Then checking out the version of ESXi:

	  
	~ # vmware -lv  
	VMware ESXi 4.1.0 build-348481  
	VMware ESXi 4.1.0 Update 1  
	

I was definitely on version 4 of ESXi, lastly vCenter was at version 5. So I matched all the symptoms. I then followed the instructions in the KB on how to get around the issue:

> To disable CBT in the configuration (.vmx) file:
> 
> 1.  Power-off the virtual machine.
> 2.  Right click on the virtual machine and click Edit Settings.
> 3.  Click the Options tab then click General.
> 4.  Click Configuration Parameters.
> 5.  Locate the values below for the IDE disk and set the values to FALSE.  
>     for example:  
	>       
	>     ide0:0.ctkEnabled = "TRUE"  
	>     ctkEnabled = "TRUE"  
	>     
> 6.  Click OK then OK again.
> 7.  Power-on the virtual machine and retry the clone operation.

After disabling Change Block Tracking on the IDE Hard Drive, the clone succeeded without any issues.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/10/virtual-machine-clone-fails-with-a-general-system-error-occurred-configuration-information-is-inaccessible/" title=" Virtual Machine Clone Fails with &#8216;A general system error occurred: Configuration information is inaccessible&#8217; Error Message" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Change Block Tracking,clone,CTK,IDE Hard Disk,ide0:0.ctkEnabled,blog;button:compact;">Recently ran into an issue when cloning a VM. The clone would start and would run and at about 99% it would fail with the following error: Checking out the...</a>
</p>