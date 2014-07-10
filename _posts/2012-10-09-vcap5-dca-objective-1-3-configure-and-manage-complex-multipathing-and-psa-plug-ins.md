---
title: VCAP5-DCA Objective 1.3 – Configure and Manage Complex Multipathing and PSA Plug-ins
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-1-3-configure-and-manage-complex-multipathing-and-psa-plug-ins/
dsq_thread_id:
  - 1409147731
categories: ['storage','certifications', 'vcap5_dca', 'vmware']
tags: ['psa','satp','psp']
---

### Explain the Pluggable Storage Architecture (PSA) layout

From this VMware KB [1011375](http://kb.vmware.com/kb/1011375):

> **Pluggable Storage Architecture (PSA)**
>
> To manage storage multipathing, ESX/ESXi uses a special VMkernel layer, Pluggable Storage Architecture (PSA). The PSA is an open modular framework that coordinates the simultaneous operation of multiple multipathing plugins (MPPs). PSA is a collection of VMkernel APIs that allow third party hardware vendors to insert code directly into the ESX storage I/O path. This allows 3rd party software developers to design their own load balancing techniques and failover mechanisms for particular storage array. The PSA coordinates the operation of the NMP and any additional 3rd party MPP

From the [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

![vsphere_storage](https://github.com/elatov/uploads/raw/master/2012/09/vsphere_storage.png)

The PSA is made up of many other technologies, like SATP,NMP, PSP, and MPP. Actually from the same guide, here is good picture:

![PSA_Architecture](https://github.com/elatov/uploads/raw/master/2012/09/PSA_Architecture.png)

And more information from the same guide:

> **Managing Multiple Paths**
> To manage storage multipathing, ESXi uses a collection of Storage APIs, also called the Pluggable Storage Architecture (PSA). The PSA is an open, modular framework that coordinates the simultaneous operation of multiple multipathing plug-ins (MPPs). The PSA allows 3rd party software developers to design their own load balancing techniques and failover mechanisms for particular storage array, and insert their code directly into the ESXi storage I/O path.
>
> Topics discussing path management use the following acronyms
>
> ![multipathing_acronyms](https://github.com/elatov/uploads/raw/master/2012/09/multipathing_acronyms.png)
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

There is also an excellent blog written by Cormac Hogan on how IO is handled by PSP, check it out in "[Path failure and related SATP/PSP behaviour](http://blogs.vmware.com/vsphere/2012/07/path-failure-and-related-satppsp-behaviour.html)"

### Install and Configure PSA plug-ins

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

> To list VMware SATPs, run the following command:
>
>
>	 ~ # esxcli storage nmp satp list
>	 Name Default PSP Description
>	 ------------------- ------------- -------------------------------------------------------
>	 VMW_SATP_ALUA VMW_PSP_MRU Supports non-specific arrays that use the ALUA protocol
>	 VMW_SATP_MSA VMW_PSP_MRU Placeholder (plugin not loaded)
>	 VMW_SATP_DEFAULT_AP VMW_PSP_MRU Placeholder (plugin not loaded)
>	 VMW_SATP_SVC VMW_PSP_FIXED Placeholder (plugin not loaded)
>	 VMW_SATP_EQL VMW_PSP_FIXED Placeholder (plugin not loaded)
>	 VMW_SATP_INV VMW_PSP_FIXED Placeholder (plugin not loaded)
>	 VMW_SATP_EVA VMW_PSP_FIXED Placeholder (plugin not loaded)
>	 VMW_SATP_ALUA_CX VMW_PSP_FIXED Placeholder (plugin not loaded)
>	 VMW_SATP_SYMM VMW_PSP_FIXED Placeholder (plugin not loaded)
>	 VMW_SATP_CX VMW_PSP_MRU Placeholder (plugin not loaded)
>	 VMW_SATP_LSI VMW_PSP_MRU Placeholder (plugin not loaded)
>	 VMW_SATP_DEFAULT_AA VMW_PSP_FIXED Supports non-specific active/active arrays
>	 VMW_SATP_LOCAL VMW_PSP_FIXED Supports direct attached devices
>
>
> To list multipathing modules, run the following command:
>
>
>	 ~ # esxcli storage core plugin list
>	 Plugin name Plugin class
>	 ----------- ------------
>	 NMP MP
>
>
> **Example: Defining an NMP SATP Rule**
> The following sample command assigns the VMW_SATP_INV plug-in to manage storage arrays with vendor string NewVend and model string NewMod.
>
>
>	 # esxcli storage nmp satp rule add -V NewVend -M NewMod -s VMW_SATP_INV
>

From "[vSphere Command-Line Interface Concepts and Examples ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf)"

Add a new SATP


	esxcli storage nmp satp rule add --satp VMW_SATP_DEFAULT_AA --vendor="ABC" --model="^120*


Change the SATP for a device/LUN:


	esxcli storage nmp satp generic deviceconfig set -c VMW_SATP_ALUA_CX -d naa.xxx


Change the default PSP for an SATP:


	# esxcli storage nmp satp set --default-psp VMW_PSP_FIXED --satp VMW_SATP_ALUA_CX


List all the plugins:


	~ # esxcli storage core plugin registration list
	Module Name Plugin Name Plugin Class Dependencies Full Path
	------------------- ------------------- ------------ ----------------------------- ---------
	mask_path_plugin MASK_PATH MP
	nmp NMP MP
	vmw_satp_symm VMW_SATP_SYMM SATP
	vmw_satp_svc VMW_SATP_SVC SATP
	vmw_satp_msa VMW_SATP_MSA SATP
	vmw_satp_lsi VMW_SATP_LSI SATP
	vmw_satp_inv VMW_SATP_INV SATP vmw_satp_lib_cx
	vmw_satp_eva VMW_SATP_EVA SATP
	vmw_satp_eql VMW_SATP_EQL SATP
	vmw_satp_cx VMW_SATP_CX SATP vmw_satp_lib_cx
	vmw_satp_alua_cx VMW_SATP_ALUA_CX SATP vmw_satp_alua,vmw_satp_lib_cx
	vmw_satp_lib_cx None SATP
	vmw_satp_alua VMW_SATP_ALUA SATP
	vmw_satp_default_ap VMW_SATP_DEFAULT_AP SATP
	vmw_satp_default_aa VMW_SATP_DEFAULT_AA SATP
	vmw_satp_local VMW_SATP_LOCAL SATP
	vmw_psp_lib None PSP
	vmw_psp_mru VMW_PSP_MRU PSP vmw_psp_lib
	vmw_psp_rr VMW_PSP_RR PSP vmw_psp_lib
	vmw_psp_fixed VMW_PSP_FIXED PSP vmw_psp_lib
	vmw_vaaip_emc None VAAI
	vmw_vaaip_mask VMW_VAAIP_MASK VAAI
	vmw_vaaip_symm VMW_VAAIP_SYMM VAAI vmw_vaaip_emc
	vmw_vaaip_netapp VMW_VAAIP_NETAPP VAAI
	vmw_vaaip_lhn VMW_VAAIP_LHN VAAI
	vmw_vaaip_hds VMW_VAAIP_HDS VAAI
	vmw_vaaip_eql VMW_VAAIP_EQL VAAI
	vmw_vaaip_cx VMW_VAAIP_CX VAAI vmw_vaaip_emc,vmw_satp_lib_cx
	vaai_filter VAAI_FILTER Filter


List all the devices claimed by NMP:


	~ # esxcli storage nmp device list
	naa.600144f0928c010000004fc511ec0001
	Device Display Name: OI iSCSI Disk (naa.600144f0928c010000004fc511ec0001)
	Storage Array Type: VMW_SATP_ALUA
	Storage Array Type Device Config: {implicit_support=on;explicit_support=off; explicit_allow=on;alua_followover=on;{TPG_id=0,TPG_state=AO}}
	Path Selection Policy: VMW_PSP_MRU
	Path Selection Policy Device Config: Current Path=vmhba33:C0:T0:L0
	Path Selection Policy Device Custom Config:
	Working Paths: vmhba33:C0:T0:L0


List all the PSPs:


	~ # esxcli storage nmp psp list
	Name Description
	------------- ---------------------------------
	VMW_PSP_MRU Most Recently Used Path Selection
	VMW_PSP_RR Round Robin Path Selection
	VMW_PSP_FIXED Fixed Path Selection


Change PSP for device/LUN:


	esxcli storage nmp device set -d naa.xx -P VMW_PSP_MRU


### Understand different multipathing policy functionalities

From the [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf) :

> By default, the VMware NMP supports the following PSPs:
>
> **VMW_PSP_MRU** The host selects the path that it used most recently. When the path becomes unavailable, the host selects an alternative path. The host does not revert back
> to the original path when that path becomes available again. There is no preferred path setting with the MRU policy. MRU is the default policy for most active-passive storage devices.
>
> Displayed in the vSphere Client as the Most Recently Used (VMware) path selection policy.
>
> **VMW_PSP_FIXED** The host uses the designated preferred path, if it has been configured. Otherwise, it selects the first working path discovered at system boot time. If you want the host to use a particular preferred path, specify it manually. Fixed is the default policy for most active-active storage devices.
>
> **NOTE** If the host uses a default preferred path and the path's status turns to Dead, a new path is selected as preferred. However, if you explicitly designate the preferred path, it will remain preferred even when it becomes inaccessible.
>
> Displayed in the vSphere Client as the Fixed (VMware) path selection policy.
>
> **VMW_PSP_RR** The host uses an automatic path selection algorithm rotating through all active paths when connecting to active-passive arrays, or through all available paths when connecting to active-active arrays. RR is the default for a number of arrays and can be used with both active-active and active-passive arrays to implement load balancing across paths for different LUNs.
>
> Displayed in the vSphere Client as the Round Robin (VMware) path selection policy

### Perform command line configuration of multipathing options

From [vSphere Command-Line Interface Concepts and Examples ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf) :

> List all devices with their corresponding paths, state of the path, adapter type, and other information:
>
>
>	 esxcli storage core path list
>
>
> Limit the display to only a specified path or device:
>
>
>	 esxcli storage core path list --path vmhba32:C0:T1:L0
>	 esxcli storage core path list --device naa.xxx
>
>
> List detailed information for the paths for the device specified with -device:
>
>
>	 esxcli storage core path list -d naa.xxx
>
>
> Set the state of a LUN path to off:
>
>
>	 esxcli storage core path set --state off --path vmhba32:C0:T1:L0
>
>
> Set the path state to active again:
>
>
>	 esxcli storage core path set --state active --path vmhba32:C0:T1:L0
>
>
> Set the path policy using esxcli:
>
>
>	 esxcli storage nmp device set --device naa.xxx --psp VMW_PSP_RR
>
>
> If you specified the VMW_PSP_FIXED policy, you must make sure the preferred path is set
> correctly. Check which path is the preferred path for a device:
>
>
>	 esxcli storage nmp psp fixed deviceconfig get --device naa.xxx
>
>
> Change the preferred path:
>
>
>	 esxcli storage nmp psp fixed deviceconfig set --device naa.xxx --path vmhba3:C0:T5:L3
>
>
> **To view and manipulate round robin path selection settings with ESXCLI**
> Retrieve path selection settings for a device that is using the roundrobin PSP
>
>
>	 esxcli storage nmp psp roundrobin deviceconfig get --device naa.xxx
>
>
> Set the path selection. You can specify when the path should change, and whether unoptimized paths should be included.
>
> Use -bytes or -iops to specify when the path should change, as in the following examples:
>
> Set the device specified by -device to switch to the next path each time 12345 bytes have been sent along the current path.
>
>
>	 esxcli storage nmp psp roundrobin deviceconfig set --type "bytes" -B 12345 --device naa.xxx
>
>
> Set the device specified by -device to switch after 4200 I/O operations have been performed on a path.
>
>
>	 esxcli storage nmp psp roundrobin deviceconfig set --type=iops --iops 4200 --device naa.xxx
>

### Change a multipath policy

From above:

> Set the path policy using esxcli:
>
>
>	 esxcli storage nmp device set --device naa.xxx --psp VMW_PSP_RR
>

### Configure Software iSCSI port binding

From [vSphere Command-Line Interface Concepts and Examples ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf):

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


