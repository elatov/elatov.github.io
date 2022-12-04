---
title: VCAP5-DCA Objective 1.1 – Implement and Manage Complex Storage Solutions
author: Karim Elatov
layout: post
permalink: /2012/10/vcap5-dca-objective-1-1-implement-and-manage-complex-storage-solutions/
categories: ['storage','certifications', 'vcap5_dca', 'vmware']
tags: ['performance', 'fiber_channel', 'iscsi', 'psa', 'vaai', 'snapshot_lun', 'raid','npiv','vmfs']
---

### Identify RAID levels

From the [wikipedia](http://en.wikipedia.org/wiki/RAID) page

> **RAID 0** (block-level striping without parity or mirroring) has no (or zero) redundancy. It provides improved performance and additional storage but no fault tolerance. Hence simple stripe sets are normally referred to as RAID 0. Any drive failure destroys the array, and the likelihood of failure increases with more drives in the array (at a minimum, catastrophic data loss is almost twice as likely compared to single drives without RAID). A single drive failure destroys the entire array because when data is written to a RAID 0 volume, the data is broken into fragments called blocks. The number of blocks is dictated by the stripe size, which is a configuration parameter of the array. The blocks are written to their respective drives simultaneously on the same sector. This allows smaller sections of the entire chunk of data to be read off each drive in parallel, increasing bandwidth. RAID 0 does not implement error checking, so any error is uncorrectable. More drives in the array means higher bandwidth, but greater risk of data loss.
>
> ![raid0 wiki VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/raid0-wiki.png)

RAID 1, from the same wikipedia page:

> In **RAID 1** (mirroring without parity or striping), data is written identically to two drives, thereby producing a "mirrored set"; the read request is serviced by either of the two drives containing the requested data, whichever one involves least seek time plus rotational latency. Similarly, a write request updates the strips of both drives. The write performance depends on the slower of the two writes (i.e., the one that involves larger seek time and rotational latency); at least two drives are required to constitute such an array. While more constituent drives may be employed, many implementations deal with a maximum of only two; of course, it might be possible to use such a limited level 1 RAID itself as a constituent of a level 1 RAID, effectively masking the limitation.The array continues to operate as long as at least one drive is functioning. With appropriate operating system support, there can be increased read performance, and only a minimal write performance reduction; implementing RAID 1 with a separate controller for each drive in order to perform simultaneous reads (and writes) is sometimes called "multiplexing" (or "duplexing" when there are only two drives).
>
> ![raid 1 wiki VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/raid-1-wiki.png)

RAID 5, from the wiki page:

> **RAID 5** (block-level striping with distributed parity) distributes parity along with the data and requires all drives but one to be present to operate; the array is not destroyed by a single drive failure. Upon drive failure, any subsequent reads can be calculated from the distributed parity such that the drive failure is masked from the end user. However, a single drive failure results in reduced performance of the entire array until the failed drive has been replaced and the associated data rebuilt. Additionally, there is the potentially disastrous RAID 5 write hole. RAID 5 requires at least three disks.
>
> ![raid 5 wiki VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/raid-5-wiki.png)

And finally Raid 10, from the wiki page:

> In **RAID 10** (mirroring and striping), data is written in stripes across the primary disks and then mirrored to the secondary disks. A typical RAID 10 configuration consists of four drives. Two for striping and two for mirroring. A RAID 10 configuration takes the best concepts of RAID 0 and RAID 1 and combines them to provide better performance along with the reliability of parity without actually having parity as with RAID 5 and RAID 6. RAID 10 is often referred to as RAID 1+0 (mirrored+striped).

And from [this](http://en.wikipedia.org/wiki/Nested_RAID_levels) wiki page:

![raid10 wiki VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/raid10-wiki.png)

If you want to know about read and write penalties, I would check out "[Calculate IOPS in a storage array](https://www.yellow-bricks.com/2009/12/23/iops/)". From the last link:

![raid io impact VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/raid_io_impact.png)

### Identify supported HBA types

From "[Storage Protocol Comparison – A vSphere Perspective](http://blogs.vmware.com/vsphere/2012/02/storage-protocol-comparison-a-vsphere-perspective.html)":

> Fiber Channel can run on 1Gb/2Gb/4Gb/8Gb & 16Gb, but 16Gb HBAs must be throttled to run at 8Gb in vSphere 5.0.
> ...
> ...
> For iSCSI
>
> 1.  NIC with iSCSI capabilities using Software iSCSI initiator & accessed using a VMkernel (vmknic) port
> 2.  Dependant Hardware iSCSI initiator
> 3.  Independent Hardware iSCSI initiator

If you want to make sure your make and model of the HBA is supported, check the VMware [Storage I/O Performance on VMware vSphere 5.1 over 16 Gigabit Fibre Channel](http://www.vmware.com/go/hcl)"

### Identify virtual disk format types

Check out [VCAP5-DCD Objective 3.5](/2012/09/vcap5-dcd-objective-3-5-determine-virtual-machine-configuration-for-a-vsphere-5-physical-design/)

Also check out this picture:

![vmdk types VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/vmdk-types.png)

### Determine use cases for and configure VMware DirectPath I/O

From "[Configuration Examples and Troubleshooting for VMDirectPath](http://www.vmware.com/pdf/vsp_4_vmdirectpath_host.pdf)":

> VMDirectPath allows guest operating systems to directly access an I/O device, bypassing the virtualization layer. This direct path, or passthrough can improve performance for VMware ESX™ systems that utilize high‐speed I/O devices, such as 10 Gigabit Ethernet.

From "[How to access USB and Other PCI Devices in VMware ESXi4 VMs with VMDirectPath](https://petri.com/vmware-esxi4-vmdirectpath)", here is a good diagram:

![vm direct path io VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/vm-direct_path_io.png)

The above page has good example of how to set it up. Also check out VMware KB [VMware VMDirectPath I/O](http://kb.vmware.com/kb/1010789) for a list of supported hardware.

### Determine requirements for and configure NPIV

To start off here is a good diagram of how it works from "[N-Port Virtualization in the Data Center](http://www.cisco.com/en/US/prod/collateral/ps4159/ps6409/ps5989/ps9898/white_paper_c11-459263.html)"

![npiv cisco VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/npiv_cisco.png)

From the VMware Blog "[NPIV: N-Port ID Virtualization](http://blogs.vmware.com/vsphere/2011/11/npiv-n-port-id-virtualization.html)"

> Let's start by describing what this feature is. NPIV stands for N-Port ID Virtualization. It is an ANSI T11 standard that describes how a single Fibre Channel Physical HBA port can register with a fabric using several worldwide port names (WWPNs), what might be considered Virtual WWNs. This in turn means that since there a multiple Virtual HBAs per physical HBA, we can allow WWNs to be assigned to each VM

The above blog, has a step by step process on how to set it up as well. Another good article that has a step by step process is "[NPIV support in VMware ESX4](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/Brocade_NPIV_ESX3.5_WP.pdf)":

![npiv slog VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/npiv_slog.png)

The above page also has snapshots of how to set it. Most of the links are reffering to vSphere 4.x but that is okay, not much has changed since 3.x days. From the above VMware blog:

> As you might see from the screenshots that I am using, the implementation is not being done on vSphere 5.0 but on a much earlier version of vSphere. However the steps haven't changed one bit since we first brought out support for NPIV back in ESX 3.

### Determine appropriate RAID level for various Virtual Machine workloads

From the Microsoft Article "[Planning the Layout and RAID Level of Volumes](https://docs.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2003/cc786889(v=ws.10))":

![data type with characteristics VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/data_type_with_characteristics.png)

and from the same site:

![raid type with factors VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/raid_type_with_factors.png)

Also check out [VCAP5-DCD Objective 3.3](/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/)

### Apply VMware storage best practices

Each vendor has their own best practices. Check out the following pages for a couple of vendors:

*   [Using VMware vSphere with EMC Symmetrix Storage](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/h2529-vmware-esx-svr-w-symmetrix-wp-ldv.pdf)
*   [HP Enterprise Virtual Array Family with VMware vSphere 4.0 , 4.1 and 5.0 Configuration Best Practices](http://www.vmware.com/files/pdf/techpaper/hp-enterprise-virtual-array-family-vsphere-configuration.pdf)
*   [Using EMC VNX Storage with VMware vSphere](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/h8229-vnx-vmware-tb.pdf)
*   [NetApp and VMware vSphere Storage Best Practices](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/tr-3749.pdf)

Check out [VCAP5-DCD Objective 3.3](/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/) for more information.

### Understand use cases for Raw Device Mapping

Check out [VCAP5-DCD Objective 3.5](/2012/09/vcap5-dcd-objective-3-5-determine-virtual-machine-configuration-for-a-vsphere-5-physical-design/)

### Configure vCenter Server storage filters

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

> When you perform VMFS datastore management operations, vCenter Server uses default storage protection filters. The filters help you to avoid storage corruption by retrieving only the storage devices that can be used for a particular operation. Unsuitable devices are not displayed for selection. You can turn off the filters to view all devices.

Also from the same article:

![storage filters VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/storage-filters.png)

And more:

> **Procedure**
> 1 In the vSphere Client, select Administration > vCenter Server Settings.
> 2.In the settings list, select Advanced Settings.
> 3 In the Key text box, type a key
> ![key filter name VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/key-filter-name.png)
> 4 In the Value text box, type False for the specified key.
> 5 Click Add.
> 6 Click OK

### Understand and apply VMFS re-signaturing

From "[vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf)":

> **Managing Duplicate VMFS Datastores**
>
> When a storage device contains a VMFS datastore copy, you can mount the datastore with the existing signature or assign a new signature.
>
> Each VMFS datastore created in a storage disk has a unique UUID that is stored in the file system superblock. When the storage disk is replicated or snapshotted, the resulting disk copy is identical, byte-for-byte, with the original disk. As a result, if the original storage disk contains a VMFS datastore with UUID X, the disk copy appears to contain an identical VMFS datastore, or a VMFS datastore copy, with exactly the same UUID X.
>
> ESXi can detect the VMFS datastore copy and display it in the vSphere Client. You can mount the datastore copy with its original UUID or change the UUID, thus resignaturing the datastore.
>
> In addition to LUN snapshotting and replication, the following storage device operations might cause ESXi to mark the existing datastore on the device as a copy of the original datastore:
>
> *   LUN ID changes
> *   SCSI device type changes, for example, from SCSI-2 to SCSI-3
> *   SPC-2 compliancy enablement

Once a snapshot is detected we have a couple of options:

> **Mount a VMFS Datastore with an Existing Signature**
> If you do not need to resignature a VMFS datastore copy, you can mount it without changing its signature.
>
> You can keep the signature if, for example, you maintain synchronized copies of virtual machines at a secondary site as part of a disaster recovery plan. In the event of a disaster at the primary site, you mount the datastore copy and power on the virtual machines at the secondary site.
>
> **IMPORTANT** You can mount a VMFS datastore copy only if it does not collide with the original VMFS datastore that has the same UUID. To mount the copy, the original VMFS datastore has to be offline.
>
> When you mount the VMFS datastore, ESXi allows both reads and writes to the datastore residing on the LUN copy. The LUN copy must be writable. The datastore mounts are persistent and valid across system reboots.
>
> **Prerequisites**
> Before you mount a VMFS datastore, perform a storage rescan on your host so that it updates its view of LUNs presented to it.
>
> **Procedure**
>
> 1.  Log in to the vSphere Client and select the server from the inventory panel.
> 2.  Click the Configuration tab and click Storage in the Hardware panel.
> 3.  Click Add Storage.
> 4.  Select the Disk/LUN storage type and click Next.
> 5.  From the list of LUNs, select the LUN that has a datastore name displayed in the VMFS Label column and click Next.
>     *   The name present in the VMFS Label column indicates that the LUN is a copy that contains a copy of an existing VMFS datastore.
> 6.  Under Mount Options, select Keep Existing Signature.
> 7.  In the Ready to Complete page, review the datastore configuration information and click Finish.

Another option is the following:

> **Resignature a VMFS Datastore Copy**
> Use datastore resignaturing if you want to retain the data stored on the VMFS datastore copy.
>
> When resignaturing a VMFS copy, ESXi assigns a new UUID and a new label to the copy, and mounts the copy as a datastore distinct from the original.
>
> The default format of the new label assigned to the datastore is snap-snapID-oldLabel, where snapID is an integer and oldLabel is the label of the original datastore.
>
> When you perform datastore resignaturing, consider the following points:
>
> *   Datastore resignaturing is irreversible.
> *   The LUN copy that contains the VMFS datastore that you resignature is no longer treated as a LUN copy.
> *   A spanned datastore can be resignatured only if all its extents are online.
> *   The resignaturing process is crash and fault tolerant. If the process is interrupted, you can resume it later.
> *   You can mount the new VMFS datastore without a risk of its UUID colliding with UUIDs of any other datastore, such as an ancestor or child in a hierarchy of LUN snapshots.
>
> **Prerequisites**
> To resignature a mounted datastore copy, first unmount it.
>
> Before you resignature a VMFS datastore, perform a storage rescan on your host so that the host updates its view of LUNs presented to it and discovers any LUN copies.
>
> **Procedure**
>
> 1.  Log in to the vSphere Client and select the server from the inventory panel.
> 2.  Click the Configuration tab and click Storage in the Hardware panel.
> 3.  Click Add Storage.
> 4.  Select the Disk/LUN storage type and click Next.
> 5.  From the list of LUNs, select the LUN that has a datastore name displayed in the VMFS Label column and click Next.
>     *   The name present in the VMFS Label column indicates that the LUN is a copy that contains a copy of an existing VMFS datastore.
> 6.  Under Mount Options, select Assign a New Signature and click Next.
> 7.  In the Ready to Complete page, review the datastore configuration information and click Finish.
>
> **What to do next**
> After resignaturing, you might have to do the following:
>
> *   If the resignatured datastore contains virtual machines, update references to the original VMFS datastore in the virtual machine files, including .vmx, .vmdk, .vmsd, and .vmsn.
> *   To power on virtual machines, register them with vCenter Server.

Check out one of my [1011387](/2012/08/enabling-disk-enableuuid-on-a-nested-esx-host-in-workstation/) for more info. From that KB, here are a couple of commands:

> To list the volumes detected as snapshots, run this command:
>
>
>	 # esxcli storage vmfs snapshot list
>
>
> The output appears similar to:
>
>
>	 49d22e2e-996a0dea-b555-001f2960aed8
>	 Volume Name: VMFS_1
>	 VMFS UUID: 4e26f26a-9fe2664c-c9c7-000c2988e4dd
>	 Can mount: true
>	 Reason for un-mountability:
>	 Can resignature: true
>	 Reason for non-resignaturability:
>	 Unresolved Extent Count: 1
>
>
> To mount a snapshot/replica LUN that is persistent across reboots, run this command:
>
>
>	 # esxcli storage vmfs snapshot mount -l label|-u uuid
>
>
> For example:
>
>
>	 # esxcli storage vmfs snapshot mount -l VMFS_1
>	 # esxcli storage vmfs snapshot mount -u 49d22e2e-996a0dea-b555-001f2960aed8
>
>
> To mount a snapshot/replica LUN that is not persistent across reboots, run this command:
>
>
>	 # esxcli storage vmfs snapshot mount -n -l label|-u uuid
>
>
> For example:
>
>
>	 # esxcli storage vmfs snapshot mount -n -l VMFS_1
>	 # esxcli storage vmfs snapshot mount -n -u 49d22e2e-996a0dea-b555-001f2960aed8
>
>
> To resignature a snapshot/replica LUN, run this command:
>
>
>	 # esxcli storage vmfs snapshot resignature -l label|-u uuid
>
>
> For example:
>
>
>	 # esxcli storage vmfs snapshot resignature -l VMFS_1
>	 # esxcli storage vmfs snapshot resignature -u 49d22e2e-996a0dea-b555-001f2960aed8
>

### Understand and apply LUN masking using PSA-related commands

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf)

> **Mask Paths**
> You can prevent the host from accessing storage devices or LUNs or from using individual paths to a LUN. Use the esxcli commands to mask the paths. When you mask paths, you create claim rules that assign the MASK_PATH plug-in to the specified paths.
>
> **Procedure**
> 1 Check what the next available rule ID is.
>
>	esxcli storage core claimrule list
>
> The claim rules that you use to mask paths should have rule IDs in the range of 101 – 200. If this command shows that rule 101 and 102 already exist, you can specify 103 for the rule to add.
>
> 2 Assign the MASK_PATH plug-in to a path by creating a new claim rule for the plug-in.
>
>	esxcli storage core claimrule add -P MASK_PATH
>
> 3 Load the MASK_PATH claim rule into your system.
>
>	esxcli storage core claimrule load
>
>
> 4 Verify that the MASK_PATH claim rule was added correctly.
>
>
>	 esxcli storage core claimrule list
>
>
> 5 If a claim rule for the masked path exists, remove the rule.
>
>
>	 esxcli storage core claiming unclaim
>
>
> 6 Run the path claiming rules.
>
>
>	 esxcli storage core claimrule run
>
>
> After you assign the MASK_PATH plug-in to a path, the path state becomes irrelevant and is no longer maintained by the host. As a result, commands that display the masked path's information might show the path state as dead.
>
> **Example: Masking a LUN**
> In this example, you mask the LUN 20 on targets T1 and T2 accessed through storage adapters vmhba2 and vmhba3.
>
>
>	 ~ # esxcli storage core claimrule list
>	 ~ # esxcli storage core claimrule add -P MASK_PATH -r 109 -t location -A vmhba2 -C 0 -T 1 -L 20
>	 ~ # esxcli storage core claimrule add -P MASK_PATH -r 110 -t location -A vmhba3 -C 0 -T 1 -L 20
>	 ~ # esxcli storage core claimrule add -P MASK_PATH -r 111 -t location -A vmhba2 -C 0 -T 2 -L 20
>	 ~ # esxcli storage core claimrule add -P MASK_PATH -r 112 -t location -A vmhba3 -C 0 -T 2 -L 20
>	 ~ # esxcli storage core claimrule load
>	 ~ # esxcli storage core claimrule list
>	 ~ # esxcli storage core claiming unclaim -t location -A vmhba2
>	 ~ # esxcli storage core claiming unclaim -t location -A vmhba3
>	 ~ # esxcli storage core claimrule run
>

### Analyze I/O workloads to determine storage performance requirements

Determine what kind of workload your application requires. From "[EMC CLARiiON Fibre Channel Storage Fundamentals](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/EMC_CLARiiON_Storage_System_Fundamentals_for_Performance_and_Availability_Applied_Best_Practices.pdf)":

![application io workloads VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/application_io_workloads.png)

Then use IOmeter or IOBlazer here are links to their corresponding flings:

*   [IOmeter](http://labs.vmware.com/flings/io-analyzer)
*   [IOBlazer](http://labs.vmware.com/flings/ioblazer)

There are also application specific tools:

*   [Microsoft Exchange Server 2010 Performance on VMware vSphere 5](http://www.vmware.com/techpapers/2011/microsoft-exchange-server-2010-performance-on-vsph-10204.html) (LoadGen)
*   [Performance and Scalability of Microsoft SQL Server on VMware vSphere (http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/vmware-sql-server-vsphere55-performance-white-paper.pdf) (TPC-E benchmark)
*   [Oracle Databases on VMware VMware vSphere 5 RAC Workload Characterization Study (VMware VMFS)](http://www.vmware.com/files/pdf/partners/oracle/Oracle_Databases_on_VMware_-_Workload_Characterization_Study.pdf) (SwingBench)

Use any of the tools above to get a good baseline and then plan accordingly with your SAN Array.

### Identify and tag SSD devices

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf) :

> **Tag Devices as SSD**
> You can use PSA SATP claim rules to tag SSD devices that are not detected automatically.
>
> Only devices that are consumed by the PSA Native Multipathing (NMP) plugin can be tagged.
>
> **Procedure**
> 1 Identify the device to be tagged and its SATP.
>
>
>	 esxcli storage nmp device list
>
>
> The command results in the following information.
>
>
>	 naa.6006016015301d00167ce6e2ddb3de11
>	 Device Display Name: DGC Fibre Channel Disk (naa.6006016015301d00167ce6e2ddb3de11)
>	 Storage Array Type: VMW_SATP_CX
>	 Storage Array Type Device Config: {navireg ipfilter}
>	 Path Selection Policy: VMW_PSP_MRU
>	 Path Selection Policy Device Config: Current Path=vmhba4:C0:T0:L25
>	 Working Paths: vmhba4:C0:T0:L25
>
>
> 2 Note down the SATP associated with the device.
> 3 Add a PSA claim rule to mark the device as SSD.
>
> - You can add a claim rule by specifying the device name
>
>		esxcli storage nmp satp rule add -s SATP --device device_name --option=enable_ssd
>
> - You can add a claim rule by specifying the vendor name and the model name.
>
>		esxcli storage nmp satp rule add -s SATP -V vendor_name -M model_name --option=enable_ssd
>
> - You can add a claim rule based on the transport protocol.
>
>		esxcli storage nmp satp rule add -s SATP --transport transport_protocol --option=enable_ssd
>
> - You can add a claim rule based on the driver name.
>
>		esxcli storage nmp satp rule add -s SATP --driver driver_name --option=enable_ssd
>
> 4 Unclaim the device.
>
> - You can unclaim the device by specifying the device name.
>
>		esxcli storage core claiming unclaim --type device --device device_name
>
> - You can unclaim the device by specifying the vendor name and the model name.
>
>		esxcli storage core claiming unclaim --type device -V vendor_name -M model_name
>
> - You can unclaim the device based on the transport protocol.
>
>		esxcli storage core claiming unclaim --type device --transport transport_protocol
>
> - You can unclaim the device based on the driver name.
>
>		esxcli storage core claiming unclaim --type device --driver driver_name
>
>
> 5 Reclaim the device by running the following commands.
>
>
>	 esxcli storage core claimrule load
>	 esxcli storage core claimrule run
>
>
> 6 Verify if devices are tagged as SSD.
>
>
>	 esxcli storage core device list -d device_name
>
>
> The command output indicates if a listed device is tagged as SSD.
>
>
>	 Is SSD: true
>

### Administer hardware acceleration for VAAI

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf) :

> **Display Hardware Acceleration Plug-Ins and Filter**
> To communicate with the devices that do not support the T10 SCSI standard, your host uses a combination of a single VAAI filter and a vendor-specific VAAI plug-in. Use the esxcli command to view the hardware acceleration filter and plug-ins currently loaded into your system.
>
> **Procedure**
>
> *   Run the esxcli storage core plugin list -plugin-class=value command.For value, enter one of the following options:
>     *   Type VAAI to display plug-ins.
>     *   The output of this command is similar to the following example:
>
> 			#esxcli storage core plugin list --plugin-class=VAAI
> 			Plugin name Plugin class
> 			VMW_VAAIP_EQL VAAI
> 			VMW_VAAIP_NETAPP VAAI
> 			VMW_VAAIP_CX VAAI
>
>
> *   Type Filter to display the Filter.
> *   The output of this command is similar to the following example:
>
>
> 		esxcli storage core plugin list --plugin-class=Filter
> 		Plugin name Plugin class
> 		VAAI_FILTER Filter
>

From the same article:

> **Verify Hardware Acceleration Support Status**
> Use the esxcli command to verify the hardware acceleration support status of a particular storage device.
>
> **Procedure**
>
> *   Run the esxcli storage core device list -d=device_ID command.
> *   The output shows the hardware acceleration, or VAAI, status that can be unknown, supported, or unsupported.
>
>
> 		# esxcli storage core device list -d naa.XXXXXXXXXXXX4c
> 		naa.XXXXXXXXXXXX4c
> 		Display Name: XXXX Fibre Channel Disk(naa.XXXXXXXXXXXX4c)
> 		Size: 20480
> 		Device Type: Direct-Access
> 		Multipath Plugin: NMP
> 		XXXXXXXXXXXXXXXX
> 		Attached Filters: VAAI_FILTER
> 		VAAI Status: supported
> 		XXXXXXXXXXXXXXXX
>

And more from the same document:

> **Verify Hardware Acceleration Support Details**
> Use the esxcli command to query the block storage device about the hardware acceleration support the device provides.
>
> **Procedure**
>
> *   Run the esxcli storage core device vaai status get -d=device_ID command.
> *   If the device is managed by a VAAI plug-in, the output shows the name of the plug-in attached to the device. The output also shows the support status for each T10 SCSI based primitive, if available. Output appears in the following example:
>
>
> 		# esxcli storage core device vaai status get -d naa.XXXXXXXXXXXX4c
> 		naa.XXXXXXXXXXXX4c
> 		VAAI Plugin Name: VMW_VAAIP_SYMM
> 		ATS Status: supported
> 		Clone Status: supported
> 		Zero Status: supported
> 		Delete Status: unsupported
>

### Configure and administer profile-based storage

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

> **Understanding Storage Capabilities**
> A storage capability outlines the quality of service that a storage system can deliver. It is a guarantee that the storage system can provide a specific set of characteristics for capacity, performance, availability, redundancy, and so on.
>
> If a storage system uses Storage APIs - Storage Awareness, it informs vCenter Server that it can guarantee a specific set of storage features by presenting them as a storage capability. vCenter Server recognizes the capability and adds it to the list of storage capabilities in the Manage Storage Capabilities dialog box. Such storage capabilities are system-defined. vCenter Server assigns the system-defined storage capability to each datastore that you create from that storage system.
>
> **NOTE** Because multiple system capabilities for a datastore are not supported, a datastore that spans several extents assumes the system capability of only one of its extents.
>
> You can create user-defined storage capabilities and associate them with datastores. You should associate the same user-defined capability with datastores that guarantee the same level of storage capabilities. You can associate a user-defined capability with a datastore that already has a system-defined capability. A datastore can have only one system-defined and only one user-defined capability at a time

From the same article:

> **Add a User-Defined Storage Capability**
> You can create a storage capability and assign it to a datastore to indicate the capabilities that this datastore has.
>
> **Procedure**
> 1 In the VM Storage Profiles view of the vSphere Client, click Manage Storage Capabilities.
> The Manage Storage Capabilities dialog box appears.
> 2 Click Add.
> 3 Provide a name and a description for the storage capability
> ![storage profiles user defined VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/storage_profiles_user_defined.png)
> 4 Click OK.

First go to the Home Screen:

![home vmstorage profiles VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/home_vmstorage_profiles.png)

Then click on VM Storage Profiles:

![vm storage profiles VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/vm_storage_profiles.png)

Then Click "Manage Storage Capabilities":

![manage storage capabilities VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/manage_storage_capabilities.png)

Fill out all the necessary fields and click ok:

![add storage capability VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/add_storage_capability.png)

and finally you should see this:
![added storage capability VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/added_storage_capability.png)

Next section from the guide:

> **Associate a User-Defined Storage Capability with a Datastore**
> After you create user-defined storage capabilities, you can associate them with datastores.
>
> Whether a datastore has a system-defined storage capability or not, you can assign a user-defined storage capability to it. A datastore can have only one user-defined and only one system-defined storage capability at a time.
>
> You cannot assign a user-defined storage capability to a datastore cluster. However, a datastore cluster inherits a system-defined or user-defined storage capabilities when all its datastores have the same system-defined or user-defined storage capability.
>
> **Prerequisites**
> Add a user-defined storage capability to the list of storage capabilities.
>
> Procedure
> 1 In the vSphere Client, select View > Inventory > Datastores and Datastore Clusters.
> 2 Right-click a datastore from the inventory and select Assign User-Defined Storage Capability.
> 3 Select a storage capability from the list of storage capabilities and click OK.
>
> ![associate st profile with ds VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/associate_st_profile_with_ds.png)
>
> The user-defined storage capability appears in the Storage Capabilities pane of the Summary tab of the datastore or its datastore cluster.

From the Home Screen select the Datastores view, then Right on a Datastore and Select "Assign User-Defined Storage Capability":
![right click datastore VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/right_click_datastore.png)

Then select your capability to be assigned to this datastore:

![assign storage capability to datastore VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/assign_storage_capability_to_datastore.png)

Then under Summary of the Datastore you will see your capability assigned:
![check assigned capability VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/check_assigned_capability.png)

### Prepare storage for maintenance

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

> **Unmount VMFS or NFS Datastores**
> When you unmount a datastore, it remains intact, but can no longer be seen from the hosts that you specify. The datastore continues to appear on other hosts, where it remains mounted.
>
> Do not perform any configuration operations that might result in I/O to the datastore while the unmount is in progress.
>
> NOTE vSphere HA heartbeating does not prevent you from unmounting the datastore. If a datastore is used for heartbeating, unmounting it might cause the host to fail and restart any active virtual machine. If the heartbeating check fails, the vSphere Client displays a warning.
>
> **Prerequisites**
> Before unmounting VMFS datastores, make sure that the following prerequisites are met:
>
> *   No virtual machines reside on the datastore.
> *   The datastore is not part of a datastore cluster.
> *   The datastore is not managed by Storage DRS.
> *   Storage I/O control is disabled for this datastore.
> *   The datastore is not used for vSphere HA heartbeating.
>
> **Procedure**
>
> 1.  Display the datastores.
> 2.  Right-click the datastore to unmount and select Unmount.
> 3.  If the datastore is shared, specify which hosts should no longer access the datastore.
>     1.  Deselect the hosts on which you want to keep the datastore mounted.
>         1.  By default, all hosts are selected.
>     2.  Click Next.
>     3.  Review the list of hosts from which to unmount the datastore, and click Finish.
> 4.  Confirm that you want to unmount the datastore.
>
> After you unmount a VMFS datastore, the datastore becomes inactive and is dimmed in the host's datastore
> list. An unmounted NFS datastore no longer appears on the list.

Right click on a datastore:

![right click on datastore to umount VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/right_click_on_datastore_to_umount.png)

Click on "Unmount" and you will see the following screen:

![unmount datastore VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/unmount_datastore.png)

Then click OK.

From the same guide:

> **Detach Storage Devices**
> Use the vSphere Client to safely detach a storage device from your host.
>
> You might need to detach the device to make it inaccessible to your host, when, for example, you perform a hardware upgrade on the storage side.
>
> **Prerequisites**
>
> *   The device does not contain any datastores.
> *   No virtual machines use the device as an RDM disk.
> *   The device does not contain a diagnostic partition.
>
> **Procedure**
>
> 1.  In the vSphere Client, display storage devices.
> 2.  Right-click the device to detach and select Detach.
>
> The device name is dimmed in the vSphere Client and becomes inaccessible. The operational state of the device changes to Unmounted.
>
> **What to do next**
> If multiple hosts share the device, detach the device from each host.

Click on an ESX Host -> Configuration Tab -> Storage Adapters -> Select your HBA (vmhba33) -> Select Devices -> Right Click on a path -> Select "Detach". Here is how it looks like:

![detach path VCAP5 DCA Objective 1.1 – Implement and Manage Complex Storage Solutions ](https://github.com/elatov/uploads/raw/master/2012/09/detach_path.png)

Also from the same guide:

> **Planned Device Removal**
> Planned device removal is a device disconnection detectable by an ESXi host. You can perform an orderly removal and reconnection of a storage device.
>
> Planned device removal is the intentional disconnection of a storage device. You might plan to remove a device for a variety of reasons, such as upgrading your hardware or reconfiguring your storage devices. To perform an orderly removal and reconnection of a storage device, use the following procedure:
>
> 1.  Migrate virtual machines from the device you plan to detach.
> 2.  Unmount the datastore deployed on the device.
> 3.  Detach the storage device.
>
> You can now perform a reconfiguration of the storage device by using the array console.

Also check out KB "[Detaching a datastore or storage device from multiple ESXi 5.0 hosts](http://kb.vmware.com/kb/2004605)". From the first KB:

> To unpresent a LUN from an ESXi 5.0 host from the command line:
>
> If the LUN is an RDM, skip to step 4. Otherwise, to get a list of all datastores mounted to an ESXi host, run the command:
>
>
>	 # esxcli storage filesystem list
>
>
> The output, which lists all VMFS datastores, is similar to:
>
>
>	 Mount Point Volume Name UUID Mounted Type Size Free
>	 ------------------------------------------------- ----------- ----------------------------------- ------- ------ ----------- -----------
>	 /vmfs/volumes/4de4cb24-4cff750f-85f5-0019b9f1ecf6 datastore1 4de4cb24-4cff750f-85f5-0019b9f1ecf6 true VMFS-5 140660178944 94577360896
>	 /vmfs/volumes/4c5fbff6-f4069088-af4f-0019b9f1ecf4 Storage2 4c5fbff6-f4069088-af4f-0019b9f1ecf4 true VMFS-3 146028888064 7968129024
>	 /vmfs/volumes/4c5fc023-ea0d4203-8517-0019b9f1ecf4 Storage4 4c5fc023-ea0d4203-8517-0019b9f1ecf4 true VMFS-3 146028888064 121057050624
>	 /vmfs/volumes/4e414917-a8d75514-6bae-0019b9f1ecf4 LUN01 4e414917-a8d75514-6bae-0019b9f1ecf4 true VMFS-5 146028888064 4266131456
>
>
> Unmount the datastore by running the command:
>
>
>	 # esxcli storage filesystem unmount [-u | -l <label> | -p ]
>
>
> For example, use one of these commands to unmount the LUN01 datastore:
>
>
>	 # esxcli storage filesystem unmount -l LUN01
>	 # esxcli storage filesystem unmount -u 4e414917-a8d75514-6bae-0019b9f1ecf4
>	 # esxcli storage filesystem unmount -p /vmfs/volumes/4e414917-a8d75514-6bae-0019b9f1ecf4
>
>
> Note: If the VMFS filesystem you are attempting to unmount has active I/O or has not fulfilled the prerequisites to unmount the VMFS datastore, the vmkernel logs show this error:
>
>
>	 WARNING: VC: 637: unmounting opened volume ('4e414917-a8d75514-6bae-0019b9f1ecf4' 'LUN01') is not allowed.
>	 VC: 802: Unmount VMFS volume f530 28 2 4e414917a8d7551419006bae f4ecf19b 4 1 0 0 0 0 0 : Busy
>
>
> To verify that the datastore has been unmounted, run the command:
>
>
>	 # esxcli storage filesystem list
>
>
> The output is similar to:
>
>
>	 Mount Point Volume Name UUID Mounted Type Size Free
>	 ------------------------------------------------- ----------- ----------------------------------- ------- ------ ----------- -----------
>	 /vmfs/volumes/4de4cb24-4cff750f-85f5-0019b9f1ecf6 datastore1 4de4cb24-4cff750f-85f5-0019b9f1ecf6 true VMFS-5 140660178944 94577360896
>	 /vmfs/volumes/4c5fbff6-f4069088-af4f-0019b9f1ecf4 Storage2 4c5fbff6-f4069088-af4f-0019b9f1ecf4 true VMFS-3 146028888064 7968129024
>	 /vmfs/volumes/4c5fc023-ea0d4203-8517-0019b9f1ecf4 Storage4 4c5fc023-ea0d4203-8517-0019b9f1ecf4 true VMFS-3 146028888064 121057050624
>	 LUN01 4e414917-a8d75514-6bae-0019b9f1ecf4 false VMFS-unknown version 0 0
>
>
> Note that the Mounted field is set to false, the Type field is set to VMFS-unknown version, and that no Mount Point exists.
>
> Note: The unmounted state of the VMFS datastore persists across reboots. This is the default behavior. However, it can be changed by appending the -no-persist flag.
>
> To detach the device/LUN, run this command:
>
>
>	 # esxcli storage core device set --state=off -d NAA_ID
>
>
> To verify that the device is offline, run this command:
>
>
>	 # esxcli storage core device list -d NAA_ID
>
>
> The output, which shows that the status of the disk is off, is similar to:
>
>
>	 naa.60a98000572d54724a34655733506751
>	 Display Name: NETAPP Fibre Channel Disk (naa.60a98000572d54724a34655733506751)
>	 Has Settable Display Name: true
>	 Size: 1048593
>	 Device Type: Direct-Access
>	 Multipath Plugin: NMP
>	 Devfs Path: /vmfs/devices/disks/naa.60a98000572d54724a34655733506751
>	 Vendor: NETAPP
>	 Model: LUN
>	 Revision: 7330
>	 SCSI Level: 4
>	 Is Pseudo: false
>	 Status: off
>	 Is RDM Capable: true
>	 Is Local: false
>	 Is Removable: false
>	 Is SSD: false
>	 Is Offline: false
>	 Is Perennially Reserved: false
>	 Thin Provisioning Status: yes
>	 Attached Filters:
>	 VAAI Status: unknown
>	 Other UIDs: vml.020000000060a98000572d54724a346557335067514c554e202020
>
>
> Running the partedUtil getptbl command on the device shows that the device is not found.
>
> For example:
>
>
>	 # partedUtil getptbl /vmfs/devices/disks/naa.60a98000572d54724a34655733506751
>		
>	 Error: Could not stat device /vmfs/devices/disks/naa.60a98000572d54724a34655733506751- No such file or directory.
>	 Unable to get device /vmfs/devices/disks/naa.60a98000572d54724a34655733506751
>
>
> The LUN can now be unpresented from the SAN. For more information, contact your storage array vendor.
> To rescan all devices on the ESXi host, run the command:
>
>
>	 # esxcli storage core adapter rescan [ -A vmhba# | --all ]
>
>
> The devices are automatically removed from the Storage Adapters.
>
> Note: A rescan needs to be run on all hosts that had visibility of the removed LUN.
>
> Note: When the device is detached, it stays in an unmounted state even if the device is represented (that is, the detached state is persistent). To bring the device back online, the device needs to be attached. To do this via the command line, run the command:
>
>
>	 # esxcli storage core device set --state=on -d NAA_ID
>
>
> If the device is to be permanently decommissioned from an ESXi servers(s), (that is, the LUN has been destroyed), remove the NAA entries from the host configuration by issuing these commands:
>
> To list the permanently detached devices:
>
>
>	 # esxcli storage core device detached list
>
>
> The output is similar to:
>
>
>	 Device UID State
>	 ---------------------------- -----
>	 naa.50060160c46036df50060160c46036df off
>	 naa.6006016094602800c8e3e1c5d3c8e011 off
>
>
> To permanently remove the device configuration information from the system:
>
>
>	 # esxcli storage core device detached remove -d NAA_ID
>
>
> For example:
>
>
>	 # esxcli storage core device detached remove -d naa.50060160c46036df50060160c46036df
>
>
> The reference to the device configuration is permanently removed from the ESXi host's configuration.

### Upgrade VMware storage infrastructure

From [vSphere Storage ESXi 5.0](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

> **Upgrade VMFS3 Datastores to VMFS5**
> VMFS5 is a new version of the VMware cluster file system that provides performance and scalability improvements.
> **Prerequisites**
>
> *   If you use a VMFS2 datastore, you must first upgrade it to VMFS3.
> *   All hosts accessing the datastore must support VMFS5.
> *   Verify that the volume to be upgraded has at least 2MB of free blocks available and 1 free file descriptor.
>
> **Procedure**
>
> 1.  Log in to the vSphere Client and select a host from the Inventory panel.
> 2.  Click the Configuration tab and click Storage.
> 3.  Select the VMFS3 datastore.
> 4.  Click Upgrade to VMFS5.
>     *   A warning message about host version support appears.
> 5.  Click OK to start the upgrade.
>     *   The task Upgrade VMFS appears in the Recent Tasks list.
> 6.  Perform a rescan on all hosts that are associated with the datastore.

Also from the same guide:

> **Upgrading a VMFS Datastore**
> You can upgrade a VMFS3 to VMFS5 datastore.
>
> **CAUTION** The upgrade is a one-way process. After you have converted a VMFS3 datastore to VMFS5, you cannot revert it back.
>
> When upgrading the datastore, use the following command: vmkfstools -T /vmfs/volumes/UUID
>
> **NOTE** All hosts accessing the datastore must support VMFS5 . If any ESX/ESXi host version 4.x or earlier is using the VMFS3 datastore, the upgrade fails and the host's mac address is displayed. with the Mac address details of the Host which is actively using the Datastore

### Related Posts

- [VCAP5-DCA Objective 6.1 – Configure, Manage, and Analyze vSphere Log Files](/2013/01/vcap5-dca-objective-6-1-configure-manage-and-analyze-vsphere-log-files/)
- [VCAP5-DCA Objective 5.2 – Deploy and Manage Complex Update Manager Environments](/2012/12/vcap5-dca-objective-5-2-deploy-and-manage-complex-update-manager-environments/)
- [VCAP5-DCA Objective 5.1 – Implement and Maintain Host Profiles](/2012/11/vcap5-dca-objective-5-1-implement-and-maintain-host-profiles/)
- [VCAP5-DCA Objective 4.2 – Deploy and Test VMware FT](/2012/11/vcap5-dca-objective-4-2-deploy-and-test-vmware-ft/)
- [VCAP5-DCA Objective 4.1 – Implement and Maintain Complex VMware HA Solutions](/2012/11/vcap5-dca-objective-4-1-implement-and-maintain-complex-vmware-ha-solutions/)

