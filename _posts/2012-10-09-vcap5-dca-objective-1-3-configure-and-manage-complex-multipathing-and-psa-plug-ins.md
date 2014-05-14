---
title: VCAP5-DCA Objective 1.3 – Configure and Manage Complex Multipathing and PSA Plug-ins
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-1-3-configure-and-manage-complex-multipathing-and-psa-plug-ins/
dsq_thread_id:
  - 1409147731
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Explain the Pluggable Storage Architecture (PSA) layout

From this VMware KB <a href="http://kb.vmware.com/kb/1011375" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1011375']);">1011375</a>:

> **Pluggable Storage Architecture (PSA)**
> 
> To manage storage multipathing, ESX/ESXi uses a special VMkernel layer, Pluggable Storage Architecture (PSA). The PSA is an open modular framework that coordinates the simultaneous operation of multiple multipathing plugins (MPPs). PSA is a collection of VMkernel APIs that allow third party hardware vendors to insert code directly into the ESX storage I/O path. This allows 3rd party software developers to design their own load balancing techniques and failover mechanisms for particular storage array. The PSA coordinates the operation of the NMP and any additional 3rd party MPP

From the <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf']);">vSphere Storage ESXi 5.0</a>:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/vsphere_storage.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/vsphere_storage.png']);"><img class="alignnone size-full wp-image-3905" title="vsphere_storage" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/vsphere_storage.png" alt="vsphere storage VCAP5 DCA Objective 1.3 – Configure and Manage Complex Multipathing and PSA Plug ins " width="441" height="572" /></a>

The PSA is made up of many other technologies, like SATP,NMP, PSP, and MPP. Actually from the same guide, here is good picture:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/PSA_Architecture.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/PSA_Architecture.png']);"><img class="alignnone size-full wp-image-3906" title="PSA_Architecture" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/PSA_Architecture.png" alt="PSA Architecture VCAP5 DCA Objective 1.3 – Configure and Manage Complex Multipathing and PSA Plug ins " width="341" height="192" /></a>

And more information from the same guide:

> **Managing Multiple Paths**  
> To manage storage multipathing, ESXi uses a collection of Storage APIs, also called the Pluggable Storage Architecture (PSA). The PSA is an open, modular framework that coordinates the simultaneous operation of multiple multipathing plug-ins (MPPs). The PSA allows 3rd party software developers to design their own load balancing techniques and failover mechanisms for particular storage array, and insert their code directly into the ESXi storage I/O path.
> 
> Topics discussing path management use the following acronyms
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/multipathing_acronyms.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/multipathing_acronyms.png']);"><img class="alignnone size-full wp-image-3907" title="multipathing_acronyms" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/multipathing_acronyms.png" alt="multipathing acronyms VCAP5 DCA Objective 1.3 – Configure and Manage Complex Multipathing and PSA Plug ins " width="588" height="175" /></a>
> 
> The VMkernel multipathing plug-in that ESXi provides by default is the VMware Native Multipathing PlugIn (NMP). The NMP is an extensible module that manages sub plug-ins. There are two types of NMP sub plugins, Storage Array Type Plug-Ins (SATPs), and Path Selection Plug-Ins (PSPs). SATPs and PSPs can be built-in and provided by VMware, or can be provided by a third party.
> 
> If more multipathing functionality is required, a third party can also provide an MPP to run in addition to, or as a replacement for, the default NMP.
> 
> When coordinating the VMware NMP and any installed third-party MPPs, the PSA performs the following tasks:
> 
> *   Loads and unloads multipathing plug-ins.
> *   Hides virtual machine specifics from a particular plug-in.
> *   Routes I/O requests for a specific logical device to the MPP managing that device.
> *   Handles I/O queueing to the logical devices.
> *   Implements logical device bandwidth sharing between virtual machines.
> *   Handles I/O queueing to the physical storage HBAs.
> *   Handles physical path discovery and removal.
> *   Provides logical device and physical path I/O statistics.
> 
> As the Pluggable Storage Architecture illustration shows, multiple third-party MPPs can run in parallel with the VMware NMP. When installed, the third-party MPPs replace the behavior of the NMP and take complete control of the path failover and the load-balancing operations for specified storage devices.

There is also an excellent blog written by Cormac Hogan on how IO is handled by PSP, check it out in &#8220;<a href="http://blogs.vmware.com/vsphere/2012/07/path-failure-and-related-satppsp-behaviour.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2012/07/path-failure-and-related-satppsp-behaviour.html']);">Path failure and related SATP/PSP behaviour</a>&#8221;

### Install and Configure PSA plug-ins

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf']);">vSphere Storage ESXi 5.0</a>:

> To list VMware SATPs, run the following command:
> 
	>   
	> ~ # esxcli storage nmp satp list  
	> Name Default PSP Description  
	> \---\---\---\---\---\---\- --\---\---\---\-- -\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---\---  
	> VMW\_SATP\_ALUA VMW\_PSP\_MRU Supports non-specific arrays that use the ALUA protocol  
	> VMW\_SATP\_MSA VMW\_PSP\_MRU Placeholder (plugin not loaded)  
	> VMW\_SATP\_DEFAULT\_AP VMW\_PSP_MRU Placeholder (plugin not loaded)  
	> VMW\_SATP\_SVC VMW\_PSP\_FIXED Placeholder (plugin not loaded)  
	> VMW\_SATP\_EQL VMW\_PSP\_FIXED Placeholder (plugin not loaded)  
	> VMW\_SATP\_INV VMW\_PSP\_FIXED Placeholder (plugin not loaded)  
	> VMW\_SATP\_EVA VMW\_PSP\_FIXED Placeholder (plugin not loaded)  
	> VMW\_SATP\_ALUA\_CX VMW\_PSP_FIXED Placeholder (plugin not loaded)  
	> VMW\_SATP\_SYMM VMW\_PSP\_FIXED Placeholder (plugin not loaded)  
	> VMW\_SATP\_CX VMW\_PSP\_MRU Placeholder (plugin not loaded)  
	> VMW\_SATP\_LSI VMW\_PSP\_MRU Placeholder (plugin not loaded)  
	> VMW\_SATP\_DEFAULT\_AA VMW\_PSP_FIXED Supports non-specific active/active arrays  
	> VMW\_SATP\_LOCAL VMW\_PSP\_FIXED Supports direct attached devices  
	> 
> 
> To list multipathing modules, run the following command:
> 
	>   
	> ~ # esxcli storage core plugin list  
	> Plugin name Plugin class  
	> \---\---\---\-- -\---\---\-----  
	> NMP MP  
	> 
> 
> **Example: Defining an NMP SATP Rule**  
> The following sample command assigns the VMW\_SATP\_INV plug-in to manage storage arrays with vendor string NewVend and model string NewMod.
> 
	>   
	> \# esxcli storage nmp satp rule add -V NewVend -M NewMod -s VMW\_SATP\_INV  
	> 

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf']);">vSphere Command-Line Interface Concepts and Examples ESXi 5.0</a>&#8221;

Add a new SATP

	  
	esxcli storage nmp satp rule add --satp VMW\_SATP\_DEFAULT_AA --vendor="ABC" --model="^120*  
	

Change the SATP for a device/LUN:

	  
	esxcli storage nmp satp generic deviceconfig set -c VMW\_SATP\_ALUA_CX -d naa.xxx  
	

Change the default PSP for an SATP:

	  
	\# esxcli storage nmp satp set --default-psp VMW\_PSP\_FIXED --satp VMW\_SATP\_ALUA_CX  
	

List all the plugins:

	  
	~ # esxcli storage core plugin registration list  
	Module Name Plugin Name Plugin Class Dependencies Full Path  
	\---\---\---\---\---\---\- --\---\---\---\---\---\-- -\---\---\---\-- -\---\---\---\---\---\---\---\---\---\- --\---\----  
	mask\_path\_plugin MASK_PATH MP  
	nmp NMP MP  
	vmw\_satp\_symm VMW\_SATP\_SYMM SATP  
	vmw\_satp\_svc VMW\_SATP\_SVC SATP  
	vmw\_satp\_msa VMW\_SATP\_MSA SATP  
	vmw\_satp\_lsi VMW\_SATP\_LSI SATP  
	vmw\_satp\_inv VMW\_SATP\_INV SATP vmw\_satp\_lib_cx  
	vmw\_satp\_eva VMW\_SATP\_EVA SATP  
	vmw\_satp\_eql VMW\_SATP\_EQL SATP  
	vmw\_satp\_cx VMW\_SATP\_CX SATP vmw\_satp\_lib_cx  
	vmw\_satp\_alua\_cx VMW\_SATP\_ALUA\_CX SATP vmw\_satp\_alua,vmw\_satp\_lib_cx  
	vmw\_satp\_lib_cx None SATP  
	vmw\_satp\_alua VMW\_SATP\_ALUA SATP  
	vmw\_satp\_default\_ap VMW\_SATP\_DEFAULT\_AP SATP  
	vmw\_satp\_default\_aa VMW\_SATP\_DEFAULT\_AA SATP  
	vmw\_satp\_local VMW\_SATP\_LOCAL SATP  
	vmw\_psp\_lib None PSP  
	vmw\_psp\_mru VMW\_PSP\_MRU PSP vmw\_psp\_lib  
	vmw\_psp\_rr VMW\_PSP\_RR PSP vmw\_psp\_lib  
	vmw\_psp\_fixed VMW\_PSP\_FIXED PSP vmw\_psp\_lib  
	vmw\_vaaip\_emc None VAAI  
	vmw\_vaaip\_mask VMW\_VAAIP\_MASK VAAI  
	vmw\_vaaip\_symm VMW\_VAAIP\_SYMM VAAI vmw\_vaaip\_emc  
	vmw\_vaaip\_netapp VMW\_VAAIP\_NETAPP VAAI  
	vmw\_vaaip\_lhn VMW\_VAAIP\_LHN VAAI  
	vmw\_vaaip\_hds VMW\_VAAIP\_HDS VAAI  
	vmw\_vaaip\_eql VMW\_VAAIP\_EQL VAAI  
	vmw\_vaaip\_cx VMW\_VAAIP\_CX VAAI vmw\_vaaip\_emc,vmw\_satp\_lib_cx  
	vaai\_filter VAAI\_FILTER Filter  
	

List all the devices claimed by NMP:

	  
	~ # esxcli storage nmp device list  
	naa.600144f0928c010000004fc511ec0001  
	Device Display Name: OI iSCSI Disk (naa.600144f0928c010000004fc511ec0001)  
	Storage Array Type: VMW\_SATP\_ALUA  
	Storage Array Type Device Config: {implicit\_support=on;explicit\_support=off; explicit\_allow=on;alua\_followover=on;{TPG\_id=0,TPG\_state=AO}}  
	Path Selection Policy: VMW\_PSP\_MRU  
	Path Selection Policy Device Config: Current Path=vmhba33:C0:T0:L0  
	Path Selection Policy Device Custom Config:  
	Working Paths: vmhba33:C0:T0:L0  
	

List all the PSPs:

	  
	~ # esxcli storage nmp psp list  
	Name Description  
	\---\---\---\---\- --\---\---\---\---\---\---\---\---\---\----  
	VMW\_PSP\_MRU Most Recently Used Path Selection  
	VMW\_PSP\_RR Round Robin Path Selection  
	VMW\_PSP\_FIXED Fixed Path Selection  
	

Change PSP for device/LUN:

	  
	esxcli storage nmp device set -d naa.xx -P VMW\_PSP\_MRU  
	

### Understand different multipathing policy functionalities

From the <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf']);">vSphere Storage ESXi 5.0</a> :

> By default, the VMware NMP supports the following PSPs:
> 
> **VMW\_PSP\_MRU** The host selects the path that it used most recently. When the path becomes unavailable, the host selects an alternative path. The host does not revert back  
> to the original path when that path becomes available again. There is no preferred path setting with the MRU policy. MRU is the default policy for most active-passive storage devices.
> 
> Displayed in the vSphere Client as the Most Recently Used (VMware) path selection policy.
> 
> **VMW\_PSP\_FIXED** The host uses the designated preferred path, if it has been configured. Otherwise, it selects the first working path discovered at system boot time. If you want the host to use a particular preferred path, specify it manually. Fixed is the default policy for most active-active storage devices.
> 
> **NOTE** If the host uses a default preferred path and the path&#8217;s status turns to Dead, a new path is selected as preferred. However, if you explicitly designate the preferred path, it will remain preferred even when it becomes inaccessible.
> 
> Displayed in the vSphere Client as the Fixed (VMware) path selection policy.
> 
> **VMW\_PSP\_RR** The host uses an automatic path selection algorithm rotating through all active paths when connecting to active-passive arrays, or through all available paths when connecting to active-active arrays. RR is the default for a number of arrays and can be used with both active-active and active-passive arrays to implement load balancing across paths for different LUNs.
> 
> Displayed in the vSphere Client as the Round Robin (VMware) path selection policy

### Perform command line configuration of multipathing options

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf']);">vSphere Command-Line Interface Concepts and Examples ESXi 5.0</a> :

> List all devices with their corresponding paths, state of the path, adapter type, and other information:
> 
	>   
	> esxcli storage core path list  
	> 
> 
> Limit the display to only a specified path or device:
> 
	>   
	> esxcli storage core path list --path vmhba32:C0:T1:L0  
	> esxcli storage core path list --device naa.xxx  
	> 
> 
> List detailed information for the paths for the device specified with &#8211;device:
> 
	>   
	> esxcli storage core path list -d naa.xxx  
	> 
> 
> Set the state of a LUN path to off:
> 
	>   
	> esxcli storage core path set --state off --path vmhba32:C0:T1:L0  
	> 
> 
> Set the path state to active again:
> 
	>   
	> esxcli storage core path set --state active --path vmhba32:C0:T1:L0  
	> 
> 
> Set the path policy using esxcli:
> 
	>   
	> esxcli storage nmp device set --device naa.xxx --psp VMW\_PSP\_RR  
	> 
> 
> If you specified the VMW\_PSP\_FIXED policy, you must make sure the preferred path is set  
> correctly. Check which path is the preferred path for a device:
> 
	>   
	> esxcli storage nmp psp fixed deviceconfig get --device naa.xxx  
	> 
> 
> Change the preferred path:
> 
	>   
	> esxcli storage nmp psp fixed deviceconfig set --device naa.xxx --path vmhba3:C0:T5:L3  
	> 
> 
> **To view and manipulate round robin path selection settings with ESXCLI**  
> Retrieve path selection settings for a device that is using the roundrobin PSP
> 
	>   
	> esxcli storage nmp psp roundrobin deviceconfig get --device naa.xxx  
	> 
> 
> Set the path selection. You can specify when the path should change, and whether unoptimized paths should be included.
> 
> Use &#8211;bytes or &#8211;iops to specify when the path should change, as in the following examples:
> 
> Set the device specified by &#8211;device to switch to the next path each time 12345 bytes have been sent along the current path.
> 
	>   
	> esxcli storage nmp psp roundrobin deviceconfig set --type "bytes" -B 12345 --device naa.xxx  
	> 
> 
> Set the device specified by &#8211;device to switch after 4200 I/O operations have been performed on a path.
> 
	>   
	> esxcli storage nmp psp roundrobin deviceconfig set --type=iops --iops 4200 --device naa.xxx  
	> 

### Change a multipath policy

From above:

> Set the path policy using esxcli:
> 
	>   
	> esxcli storage nmp device set --device naa.xxx --psp VMW\_PSP\_RR  
	> 

### Configure Software iSCSI port binding

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf']);">vSphere Command-Line Interface Concepts and Examples ESXi 5.0</a>:

Create a virtual Switch and enable jumbo frames on it:

	  
	~ # esxcli network vswitch standard add -v vSwitch1  
	~ # esxcli network vswitch standard set -m 9000 -v vSwitch1  
	

Create a PortGroup that will be used for iSCSI:

	  
	~ # esxcli network vswitch standard portgroup add -p iSCSI1 -v vSwitch1  
	

Add a vmkernel interface to our iSCSI PortGroup

	  
	esxcli network ip interface add -i vmk4 -p iSCSI1  
	esxcli network ip interface ipv4 set -i vmk4 -I 1.1.1.2 -N 255.255.255.0 -t static  
	

Enable software iSCSI

	  
	esxcli iscsi software set --enabled=true  
	

Check the status:

	  
	esxcli iscsi software get  
	

Check whether a network portal, that is, a bound port, exists for iSCSI traffic.

	  
	esxcli iscsi adapter list  
	

Bind the vmkernel interface to the sw-iSCSI vmhba:

	  
	esxcli iscsi networkportal add -n vmk4 -A vmhba3#  
	

With dynamic discovery, all storage targets associated with a host name orIP address are discovered.You run the following command.

	  
	esxcli iscsi adapter discovery sendtarget add --address='ip/dns[:port]' --adapter=vmhba3#  
	

After setup is complete, perform rediscovery and rescan all storage devices

	  
	esxcli iscsi adapter discovery rediscover  
	esxcli storage core adapter rescan --adapter=vmhba36  
	

