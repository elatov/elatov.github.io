---
title: VCAP5-DCA Objective 6.4 – Troubleshoot Storage Performance and Connectivity
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-6-4-troubleshoot-storage-performance-and-connectivity/
categories: ['storage', 'certifications', 'vcap5_dca', 'vmware']
tags: ['queue_depth', 'davg', 'psp','nmp', 'tur', 'iscsi', 'performance','esxtop','vmfs','gpt']
---

### Identify logs used to troubleshoot storage issues

- **/var/log/vmkernel.log** - generic NMP messages, iSCSI and fibre channel messages, drivers and so on
- **/var/log/vmkwarning.log** - generic storage messages, like disconnects
- **/var/log/storagerm.log** - If SIOC is enabled then all the logs regarding that will be here

### Describe the attributes of the VMFS-5 file system

From "[VMware vSphere VMFS](https://www.vmware.com/pdf/vmfs-best-practices-wp.pdf)":

> **Features of VMFS **
> The following technical features of VMFS are among those that make it suitable for use in a virtual environment:
>
> *   Automated file system with hierarchical directory structure
> *   Optimization for virtual machines in a clustered environment
> *   Lock management and distributed logical volume management
> *   Dynamic datastore expansion by spanning multiple storage extents
> *   CFS with journal logging for fast recovery
> *   Thin-provisioned virtual disk format for space optimization
> *   Virtual machine–level point-in-time snapshot copy management
> *   Encapsulation of the entire virtual machine state in a single directory
> *   Support for VMware vSphere Storage APIs – Array Integration (VAAI)

Also from "[VMware vSphere VMFS-5 Upgrade Considerations](http://www.vmware.com/files/pdf/techpaper/VMFS-5_Upgrade_Considerations.pdf)":

> **VMFS-5 Enhancements**
> The following is a complete list of enhancements made in VMFS-5.
> **New Unified 1MB File Block Size**
> Earlier versions of VMFS used 1, 2, 4 or 8MB file blocks. These larger blocks were needed to create large files (>256GB). These different file blocks sizes are no longer needed to create large files on VMFS-5. Very large files can now be created on VMFS-5 using the new unified 1MB file blocks. Earlier versions of VMFS will still have to use larger file blocks to create large files.
> **Large Single Extent Volumes**
> In earlier versions of VMFS, the largest single extent was 2TB - 512 bytes. An extent is a partition on which one can place a VMFS. To create a 64TB VMFS-5, one needed to create 32 x 2TB extents/partitions and join them together. With VMFS-5, this limit for a single extent/partition has been increased to 64TB. This significantly reduces the management overhead when using very large VMFS volumes.
> **Smaller Sub-Blocks**
> VMFS-5 introduces smaller sub-blocks. Sub-blocks are now 8KB rather than 64KB as used in the earlier versions. With VMFS-5, small files (< 8KB, but > 1KB) in size will consume only 8KB rather than 64KB. This will reduce the amount of disk space stranded by small files. Also, there are many more sub-blocks in VMFS-5 than there were in VMFS-3 (32,000 on VMFS-5 compared to approximately 4,000 on VMFS-3).
> **Small File Support**
> VMFS-5 introduces support for very small files. For files less than or equal to 1KB, VMFS-5 uses the file descriptor location in the metadata for storage rather than file blocks. When these files grow beyond 1KB, they will then start to use the new 8KB sub-blocks. This will again reduce the amount of disk space stranded by very small files.
> **Increased File Count**
> VMFS-5 introduces support for greater than 120,000 files, a four-fold increase when compared to the number of files supported on VMFS-3, which was approximately 30,000.
> **ATS Enhancement**
> The Atomic Test & Set (ATS) Hardware Acceleration primitive is now used throughout VMFS-5 for file locking. ATS is a part of VAAI (vSphere Storage APIs for Array Integration). This enhancement improves the file locking performance over earlier versions of VMFS.
> **GPT**
> To handle much larger partition sizes, the GUID Partition Table (GPT) format will now be used to create VMFS-5 volumes. Historically, Master Boot Record (MBR) was used; however, this was limited to a maximum partition size of approximately 2TB. GPT overcomes this limitation and allows for much larger partitions to handle single extents up to 64TB (using VMFS-5).
> **New Starting Sector**
> VMFS-5 partitions will now have a starting sector of 2048. This is different from VMFS-3 which had a starting sector of 128. Moving to a starting sector of 2048 helps avoid alignment issues.

### Use esxcli to troubleshoot multipathing and PSA-related issues

This was covered in "[VCAP5-DCA Objective 1.1](/2012/10/vcap5-dca-objective-1-3-configure-and-manage-complex-multipathing-and-psa-plug-ins/)"

### Use esxcli to troubleshoot VMkernel storage module configurations

From "[vSphere Troubleshooting ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-troubleshooting-guide.pdf)"

> **Adjust Queue Depth for QLogic and Emulex HBAs**
> If you are not satisfied with your host's performance, change the maximum queue depth for the QLogic or Emulex HBA.
>
> To adjust the maximum queue depth parameter, use the vCLI commands.
>
> **Prerequisites**
> Install vCLI or deploy the vSphere Management Assistant (vMA) virtual machine. See Getting Started with vSphere Command-Line Interfaces. For troubleshooting , run esxcli commands in the ESXi Shell.
>
> **Procedure**
>
> 1.  Verify which HBA module is currently loaded by entering one of the following commands:
>
>	     *   For QLogic:`esxcli system module list |grep qla`
>	     *   For Emulex:`esxcli system module list |grep lpfc`
>
> 2.  Adjust the queue depth for the appropriate module.
>
>	     *   For QLogic:`esxcli  system module parameters set -m qla2xxx -p ql2xmaxqdepth=value`
>	     *   For Emulex:`]esxcli system module parameters set -m lpfc820 -p lpfc0_lun_queue_depth=value`
>
> 3.  Reboot your host.
> 4.  Verify your changes by running the following command: `esxcli system module parameters list -m=module`
>
>       **module** is your QLogic or Emulex module, such as lpfc820 or qla2xxx.

Here is more from the same guide:

> **Adjust Maximum Queue Depth for Software iSCSI**
> If you notice unsatisfactory performance for your software iSCSI LUNs, change their maximum queue depth by running the esxcli commands.
>
> **Prerequisites**
 > Install vCLI or deploy the vSphere Management Assistant (vMA) virtual machine. See Getting Started with vSphere Command-Line Interfaces. For troubleshooting, you can run esxcli commands in the ESXi Shell.
>
> **Procedure**
>
> 1.  Run the following command:
>
>           esxcli system module parameters set -m iscsi_vmk -p iscsivmk_LunQDepth=value
>
>     The iscsivmk_LunQDepth parameter sets the maximum number of outstanding commands, or queue depth, for each LUN accessed through the software iSCSI adapter. The default value is 128.
>
> 2. Reboot your system.
> 3. Verify your changes by running the
>
>           esxcli system module parameters list -m iscsi_vmk
>

### Use esxcli to troubleshoot iSCSI related issues
From "[vSphere Command-Line Interface Concepts and Examples](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-command-line-interface-solutions-and-examples-guide.pdf)":

> Check whether software iSCSI is enabled:
>
>     ~ # esxcli iscsi software get
>     true
>
> List the targets that we connect to:
>
>     ~ # esxcli iscsi adapter discovery sendtarget list
>     Adapter Sendtarget
>     ------- ------------------
>     vmhba33 192.168.1.107:3260
>
> If you using static targets, run the following:
>
>     ~ # esxcli iscsi adapter discovery statictarget list
>
> List the luns that are you connecting to and their status:
>
>     ~ # esxcli iscsi adapter target list
>     Adapter Target Max Cons Discovery Method Last Error
>     ------- ------------------------------------------------------------------- -------- ---------------- -----------
>     vmhba33 iqn.2010-09.org.openindiana:02:d5773f2f-d5b1-6c61-8ad4-b5a2dac34294 0 SENDTARGETS No Error
>     vmhba33 iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb 0 SENDTARGETS Unqualified Login Status. (Error=0x40000)
>
> List target information:
>
>     ~ # esxcli iscsi adapter target portal list
>     Adapter Target IP Port Tpgt
>     ------- ------------------------------------------------------------------- ------------- ---- ----
 >     vmhba33 iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb 192.168.1.107 3260 1
>     vmhba33 iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb 10.131.67.12 3260 1

From the above guide:

> You can use the following ESXCLI commands to list parameter options.
>
> *   Run *esxcli iscsi adapter param get* to list parameter options for the iSCSI adapter.
> *   Run *esxcli iscsi adapter discovery sendtarget param get* or *esxcli iscsi adapter target **portal param set* to retrieve information about iSCSI parameters and whether they are settable.
> *   Run *esxcli iscsi adapter discovery sendtarget param get* or *esxcli iscsi adapter target portal param set* to set iSCSI parameter options.

From the same guide here are the available options:

> ![iscsi parameters VCAP5 DCA Objective 6.4 – Troubleshoot Storage Performance and Connectivity ](https://github.com/elatov/uploads/raw/master/2012/12/iscsi_parameters.png)
>
> Here is an example of the parameters for the adapter:
>
>     ~ # esxcli iscsi adapter param get -A vmhba33
>     Name Current Default Min Max Settable Inherit
>     -------------------- ---------- ---------- --- -------- -------- -------
>     ErrorRecoveryLevel 0 0 0 2 false false
>     InitialLoginRetryMax 4 4 0 64 false false
>     InitialR2T false false na na false false
>     FirstBurstLength 262144 262144 512 16777215 true false
>     MaxBurstLength 262144 262144 512 16777215 true false
>     MaxRecvDataSegment 131072 131072 512 16777215 true false
>     MaxOutstandingR2T 1 1 1 8 true false
>     MaxCmds 128 128 2 2048 false false
>     ImmediateData true true na na false false
>     DefaultTime2Retain 0 0 0 60 false false
>     DefaultTime2Wait 2 2 0 60 false false
>     LoginTimeout 5 5 1 60 true false
>     LogoutTimeout 15 15 0 60 false false
>     NoopOutInterval 15 15 1 60 true false
>     NoopOutTimeout 10 10 10 30 true false
>     RecoveryTimeout 10 10 1 120 true false
>     DelayedAck false true na na true false
>     HeaderDigest prohibited prohibited na na true false
>     DataDigest prohibited prohibited na na true false
>
> Here is an example for the target parameters:
>
>     ~ # esxcli iscsi adapter target portal param get -A vmhba33 -a 192.168.1.107 -n iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb
>     Name Current Default Min Max Settable Inherit
>     -------------------- ---------- ---------- --- -------- -------- -------
>     ErrorRecoveryLevel 0 0 0 2 false true
>     InitialLoginRetryMax 4 4 0 64 false true
>     InitialR2T false false na na false true
>     FirstBurstLength 262144 262144 512 16777215 true true
>     MaxBurstLength 262144 262144 512 16777215 true true
>     MaxRecvDataSegment 131072 131072 512 16777215 true true
>     MaxOutstandingR2T 1 1 1 8 true true
>     MaxCmds 128 128 2 2048 false true
>     ImmediateData true true na na false true
>     DefaultTime2Retain 0 0 0 60 false true
>     DefaultTime2Wait 2 2 0 60 false true
>     LoginTimeout 5 5 1 60 true true
>     LogoutTimeout 15 15 0 60 false true
>     NoopOutInterval 15 15 1 60 true true
>     NoopOutTimeout 10 10 10 30 true true
>     RecoveryTimeout 10 10 1 120 true true
>     DelayedAck false true na na true true
>     HeaderDigest prohibited prohibited na na true true
>     DataDigest prohibited prohibited na na true true
>
> List the uplinks that can be used for iSCSI:
>
>     ~ # esxcli iscsi physicalnetworkportal list
>     Adapter Vmnic MAC Address MAC Address Valid Current Speed Max Speed Max Frame Size
>     ------- ------ ----------------- ----------------- ------------- --------- --------------
>     vmhba33 vmnic4 00:50:56:17:16:a5 true 1000 1000 1500
>     vmhba33 vmnic0 00:50:56:17:12:cb true 1000 1000 1500
>     vmhba33 vmnic1 00:50:56:17:16:07 true 1000 1000 1500
>     vmhba33 vmnic3 00:50:56:17:16:a4 true 1000 1000 1500
>     vmhba33 vmnic2 00:50:56:17:16:58 true 1000 1000 1500
>     vmhba33 vmnic5 00:50:56:17:16:a6 true 1000 1000 1500
>
> List vmkernel interfaces that can be used for iSCSI:
>
>     ~ # esxcli iscsi logicalnetworkportal list
>     Adapter Vmknic MAC Address MAC Address Valid Compliant
>     ------- ------ ----------------- ----------------- ---------
>     vmhba33 vmk0 00:50:56:17:12:cb true true
>     vmhba33 vmk1 00:50:56:17:16:07 true true
>     vmhba33 vmk2 00:50:56:17:16:58 true true
>
> List vmkernel interfaces used for iSCSI binding:
>
>     ~ # esxcli iscsi networkportal list
>     vmhba33
>     Adapter: vmhba33
>     Vmknic: vmk1
>     MAC Address: 00:50:56:17:16:07
>     MAC Address Valid: true
>     IPv4: 192.168.1.106
>     IPv4 Subnet Mask: 255.255.255.0
>     IPv6:
>     MTU: 1500
>     Vlan Supported: true
>     Vlan ID: 0
>     Reserved Ports: 63488~65536
>     TOE: false
>     TSO: true
>     TCP Checksum: false
>     Link Up: true
>     Current Speed: 1000
>     Rx Packets: 25089756
>     Tx Packets: 8315855
>     NIC Driver: e1000
>     NIC Driver Version: 8.0.3.1-NAPI
>     NIC Firmware Version: N/A
>     Compliant Status: compliant
>     NonCompliant Message:
>     NonCompliant Remedy:
>     Vswitch: vSwitch1
>     PortGroup: iSCSI
>     VswitchUuid:
>     PortGroupKey:
>     PortKey:
>     Duplex:
>     Path Status: active
>
> List iSCSI sessions:
>
>     ~ # esxcli iscsi session list
>     vmhba33,iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb,00023d000001
>     Adapter: vmhba33
>     Target: iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb
>     ISID: 00023d000001
>     TargetPortalGroupTag: 1
>     AuthenticationMethod: none
>     DataPduInOrder: true
>     DataSequenceInOrder: true
>     DefaultTime2Retain: 0
>     DefaultTime2Wait: 2
>     ErrorRecoveryLevel: 0
>     FirstBurstLength: 65536
>     ImmediateData: true
>     InitialR2T: true
>     MaxBurstLength: 262144
>     MaxConnections: 1
>     MaxOutstandingR2T: 1
>     TSIH: 14
>
>     vmhba33,iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb,00023d000003
>     Adapter: vmhba33
>     Target: iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb
>     ISID: 00023d000003
>     TargetPortalGroupTag: 1
>     AuthenticationMethod: none
>     DataPduInOrder: true
>     DataSequenceInOrder: true
>     DefaultTime2Retain: 0
>     DefaultTime2Wait: 2
>     ErrorRecoveryLevel: 0
>     FirstBurstLength: 65536
>     ImmediateData: true
>     InitialR2T: true
>     MaxBurstLength: 262144
>     MaxConnections: 1
>     MaxOutstandingR2T: 1
>     TSIH: 18
>
> Show connection information regarding each iSCSI session:
>
>     ~ # esxcli iscsi session connection list
>     vmhba33,iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb,00023d000001,0
>     Adapter: vmhba33
>     Target: iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb
>     ISID: 00023d000001
>     CID: 0
>     DataDigest: NONE
>     HeaderDigest: NONE
>     IFMarker: false
>     IFMarkerInterval: 0
>     MaxRecvDataSegmentLength: 131072
>     MaxTransmitDataSegmentLength: 32768
>     OFMarker: false
>     OFMarkerInterval: 0
>     ConnectionAddress: 192.168.1.107
>     RemoteAddress: 192.168.1.107
>     LocalAddress: 192.168.1.106
>     SessionCreateTime: 12/14/12 18:59:57
>     ConnectionCreateTime: 12/14/12 18:59:57
>     ConnectionStartTime: 12/14/12 18:59:57
>     State: logged_in
>
>     vmhba33,iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb,00023d000003,0
>     Adapter: vmhba33
>     Target: iqn.2010-09.org.openindiana:02:bd79a6ff-33c2-41d3-8f0e-9c8d8b6e9fcb
>     ISID: 00023d000003
>     CID: 0
>     DataDigest: NONE
>     HeaderDigest: NONE
>     IFMarker: false
>     IFMarkerInterval: 0
>     MaxRecvDataSegmentLength: 131072
>     MaxTransmitDataSegmentLength: 32768
>     OFMarker: false
>     OFMarkerInterval: 0
>     ConnectionAddress: 192.168.1.107
>     RemoteAddress: 192.168.1.107
>     LocalAddress: 192.168.1.106
>     SessionCreateTime: 12/16/12 21:02:12
>     ConnectionCreateTime: 12/16/12 21:02:12
>     ConnectionStartTime: 12/16/12 21:02:12
>     State: logged_in
>
> Perform rediscovery and rescan all storage devices
>
>     ~ # esxcli iscsi adapter discovery rediscover -A vmhba33
>     Rediscovery started
>     ~ # esxcli storage core adapter rescan -A vmhba33
>

### Troubleshoot NFS mounting and permission issues

From "[Best Practices for running VMware vSphere on Network Attached Storage](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/vmware-nfs-bestpractices-white-paper-en.pdf)"

> VMware vSphere implementation of NFS supports NFS version 3 in TCP. There is currently no support for NFS version 2, UDP, or CIFS/SMB

So make sure you NAS server supports TCP version 3. From the same document:

> If you do not have the **no_root_squash** option set, you will get the following error when you try to create a virtual machine on the NAS datastore:
>
> ![nfs access error VCAP5 DCA Objective 6.4 – Troubleshoot Storage Performance and Connectivity ](https://github.com/elatov/uploads/raw/master/2012/12/nfs_access_error.png)
>

This can be confusing since you can still create the datastore, but you will not be able to create any virtual machines on it.

You will also see the following if you are directly on the Console:

>     ~ # esxcli storage nfs list
>     Volume Name Host Share Accessible Mounted Hardware Acceleration
>     ----------- ------------- --------------- ---------- ------- ---------------------
>     NFS 192.168.1.107 /data/nfs_share true true Not Supported
>     ~ # cd /vmfs/volumes/NFS
>     /vmfs/volumes/68f39598-81703e7b # touch j
>     touch: j: Permission denied
>

Here is a good summary of some issues from the above document:

> ![common nfs issues VCAP5 DCA Objective 6.4 – Troubleshoot Storage Performance and Connectivity ](https://github.com/elatov/uploads/raw/master/2012/12/common_nfs_issues.png)

### Use esxtop/resxtop and vscsiStats to identify storage performance issues

The vscsiStats were covered in "[VCAP5-DCA Objective 3.4](/2012/11/vcap5-dca-objective-3-4-utilize-advanced-vsphere-performance-monitoring-tools/)"

As for esxtop, from [this](https://raw.githubusercontent.com/elatov/upload/master/vcap-dca/obj_62/Esxtop_Troubleshooting_eng.pdf) pdf:

> ![esxtop thresholds for disk VCAP5 DCA Objective 6.4 – Troubleshoot Storage Performance and Connectivity ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_thresholds_for_disk.png)

Here is a quick summary:

> - **KAVG**: Latency caused by VMKernel Possible cause: Queuing (wrong queue depth parameter or wrong failover policy) (Trouble when > 3)
> - **Resets/s**: number of commands reset per second (Trouble when > 1)
> - **DAVG**: Latency at the device driver level, Indicator for storage performance troubles (Trouble when > 25)
> - **ABRTS/s**: Commands aborted per second. If the storage system has not responded within 60 seconds VMs with an Windows Operating System will issue an abort. (Trouble when > 1)
> - **GAVG**: GAVG = DAVG + KAVG, what the guest actually experiences. (Trouble when > 25)

From "[Performance Troubleshooting for vSphere 4.1](http://www.vmware.com/resources/techresources/10179)":

> ![storage performance troubleshooting VCAP5 DCA Objective 6.4 – Troubleshoot Storage Performance and Connectivity ](https://github.com/elatov/uploads/raw/master/2012/12/storage_performance_troubleshooting.png)

### Configure and troubleshoot VMFS datastores using vmkfstools

From a host, we can see the following:

>     ~ # vmkfstools
>     No valid command specified
>
>     OPTIONS FOR FILE SYSTEMS:
>
>     vmkfstools -C --createfs vmfs3
>     -b --blocksize #
>     -S --setfsname fsName
>     -Z --spanfs span-partition
>     -G --growfs grown-partition
>     deviceName
>
>     -P --queryfs -h --humanreadable
>     -T --upgradevmfs
>     vmfsPath
>

From the "[vSphere Storage ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf)":

> **vmkfstools Options**
> The vmkfstools command has several options. Some of the options are suggested for advanced users only.
> The long and single-letter forms of the options are equivalent. For example, the following commands are identical.
>
>     vmkfstools --createfs vmfs5 --blocksize 1m disk_ID:P
>     vmkfstools -C vmfs5 -b 1m disk_ID:P
>
> **-v Suboption**
> The -v suboption indicates the verbosity level of the command output.
> The format for this suboption is as follows:
>
>     -v --verbose number
>
> You specify the number value as an integer from 1 through 10.
> You can specify the -v suboption with any vmkfstools option. If the output of the option is not suitable for use with the -v suboption, vmkfstools ignores -v.
>
> **File System Options**
> File system options allow you to create a VMFS file system. These options do not apply to NFS. You can perform many of these tasks through the vSphere Client.
>
> **Listing Attributes of a VMFS Volume**
> Use the vmkfstools command to list attributes of a VMFS volume.
>
>
>     -P --queryfs
>     -h --human-readable
>
> When you use this option on any file or directory that resides on a VMFS volume, the option lists the attributes of the specified volume. The listed attributes include the file system label, if any, the number of extents comprising the specified VMFS volume, the UUID, and a listing of the device names where each extent resides.
>
> You can specify the -h suboption with the -P option. If you do so, vmkfstools lists the capacity of the volume in a more readable form, for example, 5k, 12.1M, or 2.1G.
>
> **Creating a VMFS File System**
> Use the vmkfstools command to create a VMFS datastore.
>
>
>     -C --createfs [vmfs3|vmfs5]
>     -b --blocksize block_size kK|mM
>     -S --setfsname datastore
>
>
> This option creates a VMFS3 or VMFS5 datastore on the specified SCSI partition, such as disk_ID:P. The partition becomes the file system's head partition.
>
> You can specify the following suboptions with the -C option:
>
> *   **-b -blocksize** – Define the block size for the VMFS datastore.For VMFS5, the only available block size is 1MB. For VMFS3, the default block size is 1MB. Depending on your needs, the block size can be 1MB, 2MB, 4MB, and 8MB. When you enter the size, indicate the unit type by adding a suffix, such as m or M. The unit type is not case sensitive.
> *   **-S -setfsname** – Define the volume label of the VMFS datastore you are creating. Use this suboption only in conjunction with the -C option. The label you specify can be up to 128 characters long and cannot contain any leading or trailing blank spaces.
>
> After you define a volume label, you can use it whenever you specify the VMFS datastore for the vmkfstools command. The volume label appears in listings generated for the ls -l command and as a symbolic link to the VMFS volume under the /vmfs/volumes directory.
>
> To change the VMFS volume label, use the ln -sf command. Use the following as an example:
>
>     ln -sf /vmfs/volumes/UUID /vmfs/volumes/datastore
>
> datastore is the new volume label to use for the UUID VMFS.
>
> **Example for Creating a VMFS File System**
> This example illustrates creating a new VMFS datastore named my_vmfs on the naa.ID:1 partition. The file block size is 1MB.
>
>     vmkfstools -C vmfs5 -b 1m -S my_vmfs /vmfs/devices/disks/naa.ID:1
>
> **Extending an Existing VMFS Volume**
> Use the vmkfstools command to add an extent to a VMFS volume.
>
>
>     -Z --spanfs span_partition head_partition
>
>
> This option extends the VMFS file system with the specified head partition by spanning it across the partition specified by span_partition. You must specify the full path name, for example /vmfs/devices/disks/disk_ID:1. Each time you use this option, you extend a VMFS volume with a new extent so that the volume spans multiple partitions.
>
> **Example for Extending a VMFS Volume**
> In this example, you extend the logical file system by allowing it to span to a new partition.
>
>
>     vmkfstools -Z /vmfs/devices/disks/naa.disk_ID_2:1 /vmfs/devices/disks/naa.disk_ID_1:1
>
>
> The extended file system spans two partitions—naa.disk_ID_1:1 and naa.disk_ID_2:1. In this example, naa.disk_ID_1:1 is the name of the head partition.
>
> **Growing an Existing Extent**
> Instead of adding a new extent to a VMFS datastore, you can grow an existing extent using the vmkfstools -G command.
> Use the following option to increase the size of a VMFS datastore after the underlying storage had its capacity increased.
>
>
>     -G --growfs device device
>
>
> This option grows an existing VMFS datastore or its extent. For example,
>
>
>     vmkfstools --growfs /vmfs/devices/disks/disk_ID:1 /vmfs/devices/disks/disk_ID:1
>
>
> **Upgrading a VMFS Datastore**
> You can upgrade a VMFS3 to VMFS5 datastore.
> When upgrading the datastore, use the following command:
>
>     vmkfstools -T /vmfs/volumes/UUID
>

### Troubleshoot snapshot and re-signaturing issues

This was covered in "[VCAP5-DCA Objective 1.1](/2012/10/vcap5-dca-objective-1-1-implement-and-manage-complex-storage-solutions/)"

### Analyze log files to identify storage and multipathing problems

VMware KB [1027963](http://kb.vmware.com/kb/1027963) has really good examples of pathing failover and log snippets. From the KB:

> The VMware ESX/ESXi 4.x and 5.0 storage multipathing failover sequence is:
>
> 1. The connection along a given path is detected as down or offline. For example:
>
>         vmkernel: 188:04:24:16.970 cpu8:4288)WARNING: iscsi_vmk: iscsivmk_StopConnection: vmhba33:CH:0 T:1 CN:0: iSCSI connection is being marked "OFFLINE"
>
> 2. The ESX/ESXi host stops its iSCSI session. For example:
>
>         vmkernel: 188:04:24:16.970 cpu8:4288)WARNING: iscsi_vmk: iscsivmk_StopConnection: Sess [ISID: 00023d000001 TARGET: iqn.1992-04.com.emc:cx.sl7e2091300074.b1 TPGT: 2 TSIH: 0]
>       vmkernel: 188:04:24:16.970 cpu8:4288)WARNING: iscsi_vmk: iscsivmk_StopConnection: Conn [CID: 0 L: 192.168.2.16:50439 R: 192.168.2.8:3260]
>
> 3. As a result of stopping that session, the iSCSI task is aborted. For example:
>
>         vmkernel: 188:04:24:16.970 cpu11:4288)WARNING: iscsi_vmk: iscsivmk_TaskMgmtIssue: vmhba33:CH:0 T:1 L:14 : Task mgmt "Abort Task" with itt=0x5155cba9 (refITT=0x5155cb93) timed out.
>
> 4. The Native Multi-pathing Plugin detects a Host status of 0x1 for the reason that the command in-flight had failed. A host status of 0x1 translates to NO_CONNECT. For details, see SCSI events that can trigger ESX server to fail a LUN over to another path (1003433). For example:
>
>         vmkernel: 188:04:24:16.970 cpu1:4286)NMP: nmp_CompleteCommandForPath: Command 0x28 (0x41000716a200) to NMP device "naa.60060160d5c12200ccd66fd74a81de11" failed on physical path "vmhba33:C0:T1:L7" H:0x1 D:0x0 P:0x0 Possible sense data: 0x2 0x3a 0x1.
>
> 5. Once the NMP receives this host status, it will send a TEST_UNIT_READY (TUR) command down that path to confirm that it is down, before initiating a failover. For example:
>
>         vmkernel: 188:04:24:16.970 cpu1:4286)WARNING: NMP: nmp_DeviceRetryCommand: Device "naa.60060160d5c12200ccd66fd74a81de11": awaiting fast path state update for failover with I/O blocked. No prior reservation exists on the device.
>
> 6. If this command also fails, the ESX/ESXi host's Path Selection Policy (PSP) activates the next path for the device (LUN). For example:
>
>         vmkernel: 188:04:24:16.989 cpu1:4131)vmw_psp_mru: psp_mruSelectPathToActivateInt: Changing active path from vmhba33:C0:T1:L7 to vmhba33:C0:T0:L7 for device "naa.60060160d5c12200ccd66fd74a81de11".
>
> 7.  This line indicates that the path change was successful. The NMP retries the queued commands down this path to ensure they complete successfully, despite a failover condition being triggered. For example:
>
>         vmkernel: 188:04:24:17.974 cpu8:4247)WARNING: NMP: nmp_DeviceAttemptFailover: Retry world failover device "naa.60060160d5c12200ccd66fd74a81de11" - issuing command 0x41000716a200
>
> 8.  The initial commands may not immediately complete on failover (for example, if the LUN still has pending reservations). ESX/ESXi host sends a LUN reset if there is a pending SCSI reservation against the device or LUN. This ensures that the SCSI-2 based reservation from the previous initiator is broken, so that the ESX/ESXi host can resume I/O upon failover. For example:
>
>         vmkernel: 188:04:24:17.974 cpu12:4108)WARNING: NMP: nmp_CompleteRetryForPath: Retry command 0x28 (0x41000716a200) to NMP device "naa.60060160d5c12200ccd66fd74a81de11" failed on physical path "vmhba33:C0:T0:L7" H:0x0 D:0x2 P:0x0 Valid sense data: 0x6 0x29 0x0
>
>     This translates to:
>
>
>     Host Status = 0x0 = OK
>     Device Status = 0x2 = Check Condition
>     Plugin Status = 0x0 = OK
>     Sense Key = 0x6 = UNIT ATTENTION
>     Additional Sense Code/ASC Qualifier = 0x29/0x0 = POWER ON OR RESET OCCURRED
>
>     *   At this stage, the ESX/ESXi host can retry the next command in the queue:
>
>              Sep 10 13:11:18 laesx01 vmkernel: 188:04:24:17.974 cpu12:4108)WARNING: NMP: nmp_CompleteRetryForPath: Retry world on with device "naa.60060160d5c12200ccd66fd74a81de11" - retry the next command in retry queue
>              Sep 10 13:11:18 laesx01 vmkernel: 188:04:24:17.974 cpu12:4108)ScsiDeviceIO: 747: Command 0x28 to device "naa.60060160d5c12200ccd66fd74a81de11" failed H:0x0 D:0x2 P:0x0 Valid sense data: 0x6 0x29 0x0.
>              Sep 10 13:11:18 laesx01 vmkernel: 188:04:24:17.974 cpu11:4247)WARNING: NMP: nmp_DeviceAttemptFailover: Retry world failover device "naa.60060160d5c12200ccd66fd74a81de11" - issuing command 0x41000706fa00
>
>     *   Indication that the path failover was successful and commands are able to complete via the new path looks similar to:
>
>              vmkernel: 188:04:24:17.975 cpu12:4108)NMP: nmp_CompleteRetryForPath: Retry world recovered device "naa.60060160d5c12200ccd66fd74a81de11"
>
>     *   Finally, as this is a S/W iSCSI-based example, you also see the session marked "ONLINE" again:
>
>              vmkernel: 188:04:24:20.405 cpu9:4288)WARNING: iscsi_vmk: iscsivmk_StartConnection: vmhba33:CH:0 T:1 CN:0: iSCSI connection is being marked "ONLINE"
>              vmkernel: 188:04:24:20.405 cpu9:4288)WARNING: iscsi_vmk: iscsivmk_StartConnection: Sess [ISID: 00023d000001 TARGET: iqn.1992-04.com.emc:cx.sl7e2091300074.b1 TPGT: 2 TSIH: 0]
>              vmkernel: 188:04:24:20.405 cpu9:4288)WARNING: iscsi_vmk: iscsivmk_StartConnection: Conn [CID: 0 L: 192.168.2.16:52160 R: 192.168.2.8:3260]
>
>     **Note:** Since the storage stack handles failover identically for FC, this sequence, with the exception of steps 1, 2, 3, and 11, applies
