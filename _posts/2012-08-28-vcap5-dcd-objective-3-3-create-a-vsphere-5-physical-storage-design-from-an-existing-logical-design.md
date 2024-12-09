---
title: VCAP5-DCD Objective 3.3 – Create a vSphere 5 Physical Storage Design from an Existing Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/
categories: ['storage', 'certifications', 'vcap5_dcd', 'vmware']
tags: ['fcoe', 'fiber_channel', 'san_zoning', 'sioc', 'vmotion', 'iscsi', 'port_channel', 'alua', 'psp','raid', 'vaai', 'physical_design', 'logical_design']
---

### Describe selection criteria for commonly used RAID types

From "[Best Practices for Microsoft SQL Server on Hitachi Universal Storage Platform VM](https://raw.githubusercontent.com/elatov/upload/master/vcap-dcd/3-3/best-practices-for-microsoft-sql-server-on-hitachi-universal-storage-platform-vm.pdf)":

> RAID-1+ is best suited to applications with low cache-hit ratios, such as random I/O activity, and with high write-to-read ratios.
>
> Place database and log files on physically separate RAID groups.
>
> Place log files on RAID-1+ rather than RAID-5, depending on the log files capacity and performance requirements. If high write rates are expected, use RAID-1+ to ensure achieving your performance requirements.
>
> The overhead of RAID-5 is equivalent to one disk drive, regardless of the size of the array group. RAID-5 is best suited to applications using mostly sequential reads.

And from "[VDI & Storage: Deep Impact](https://github.com/elatov/uploads/raw/master/2014/02/VDI_Storage.pdf)":

> RAID5 - With 15,000 RPM disks the amount of read IOPS are somewhere in the 150-160 range while write IOPS are closer to the 35-45 range.
>
> RAID1 - With RAID1 the data is read from one of the two disks in a set and written to both. So for 15,000 RPM disks, the figures for a RAID1 set are still 150-160 IOPS for reads, but 70-80 for writes.
>
> RAID0 - If used, the amount of IOPS a RAID0 set can provide with 15,000 RPM disks is 150-160 for reads and 140-150 for writes.

Here is a diagram from the above pdf:

![raid-with-iops](https://github.com/elatov/uploads/raw/master/2012/08/raid-with-iops.png)

and also here is similar diagram from [this](https://blogs.vmware.com/vsphere/2012/06/troubleshooting-storage-performance-in-vsphere-part-2.html) VMware blog:

![sizing-storage](https://github.com/elatov/uploads/raw/master/2012/08/sizing-storage.png)

If you want information on how each RAID works, I would suggest reading "[Understanding RAID Performance at Various Levels](https://www.arcserve.com/blog/understanding-raid-performance-various-levels)".

### Based on the service catalog and given functional requirements, for each service: Determine the most appropriate storage technologies for the design.

I would check out the VMware blog "[Storage Protocol Comparison – A vSphere Perspective](https://blogs.vmware.com/vsphere/2012/02/storage-protocol-comparison-a-vsphere-perspective.html)". Here is a snippet from that page:

![prot-comp](https://github.com/elatov/uploads/raw/master/2012/08/prot-comp.png)

And also from "[Storage Considerations for VMware View](https://github.com/elatov/uploads/raw/master/2012/09/view_storage_considerations.pdf)":

![no_of_vm_on_prot](https://github.com/elatov/uploads/raw/master/2012/08/no_of_vm_on_prot.png)

From "[Storage Protocol Choices & Storage Best Practices for VMware ESX](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/storage-best-practices.pdf)" here is an example setup using all the protocols:

![vmware-multi-protocol-storage](https://github.com/elatov/uploads/raw/master/2012/08/vmware-multi-protocol-storage.png)

Also depending on what application needs to be run, check some requirements. Here is an example from "[Design and Sizing Examples: Microsoft Exchange Solutions on VMware](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/exchange_best_practices.pdf)":

![exchange_storage_setup](https://github.com/elatov/uploads/raw/master/2012/08/exchange_storage_setup.png)

Lastly the array vendor also provide their capabilities as well, from "[Using EMC VNX Storage with VMware vSphere](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/249258606-h8229-vnx-vmware-tb-2-pdf.pdf)":

![vnx-tiers](https://github.com/elatov/uploads/raw/master/2012/08/vnx-tiers.png)

Depending on the environment choose the storage protocol that will best fill the needs. Also be realistic, if the customer wants too much performance but can't afford a Fiber Channel Switch or a Fiber Channel Array then set the expectation accordingly.

### Create a physical storage design based on selected storage array capabilities, including but not limited to: Active/Active, Active/Passive, ALUA, VAAI, VASA, PSA (including PSPs and SATPs)

Each Array has their best practices, I would suggest following those. Let's say you got an A/A array. A typical A/A array is an EMC Symmetrix. From "[Using VMware vSphere with EMC Symmetrix Storage](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/h2529-vmware-esx-svr-w-symmetrix-wp-ldv.pdf)":

> **Symmetrix DMX connectivity**
> Each ESX host that uses Symmetrix DMX storage should have at least two physical HBAs, and each HBA should be connected to one front-end port on different directors. This configuration ensures two things:First, since there are two HBAs, if one goes down for any reason all connectivity is not lost. Second, this ensures continued access to the array from the ESX host even if a front-end port goes down for maintenance activities on the director.
>
> In a two-director Symmetrix DMX setup, each HBA should be connected to at least one distinct port on each director. Connectivity to the Symmetrix front-end ports should consist of first connecting unique hosts to port 0 of the front-end directors before connecting additional hosts to port 1 of the same director and processor. If more than two front-end directors are available, the HBAs from the ESX hosts should be connected to as many different directors as possible to distribute the workload fully.
>
> For instance, in a four FA director Symmetrix DMX (Figure 5), the first ESX host would be connected to two ports spread out over the first two directors, such as ports 3A:0 and 4A:0. The second ESX host would be connected to two different ports spread out over the second two directors, such as ports 13A:0 and 14C:0.

Here is a diagram from that pdf:

![dmx-vmware-bp](https://github.com/elatov/uploads/raw/master/2012/08/dmx-vmware-bp.png)

Also from the same pdf:

> **Symmetrix V-Max connectivity**
> Similar to the Symmetrix DMX, each ESX host system attached to a Symmetrix V-Max should have at least two physical HBAs, and each HBA should be connected to at least two different directors. If the Symmetrix V-Max in use has only one V-Max Engine then each HBA should be connected to the odd and even directors within it. Connectivity to the Symmetrix front-end ports should consist of first connecting unique hosts to port 0 of the front-end directors before connecting additional hosts to port 1 of the same director and processor (Figure 6). And here is diagram for the above setup:

![vmax-vmware-bp](https://github.com/elatov/uploads/raw/master/2012/08/vmax-vmware-bp.png)

The recommended PSP for A/A Arrays is fixed. A typical A/P array is an HP EVA. From "[HP Enterprise Virtual Array Family with VMware vSphere 4.0 , 4.1 and 5.0 Configuration Best Practices](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/hp-enterprise-virtual-array-family-vsphere-configuration.pdf)":

> All I/Os to Vdisks 1 – 4 are routed through one or more ports on Controller 1 and through Paths 1and/or 3, regardless of the HBA that originates the I/O. Similarly, all I/Os to Vdisks 5 – 7 are routed to Controller 2 through Paths 3 and 4, regardless of the originating HBA.The vSphere 4.x/5 implementation yields much higher system resource utilization and throughput and, most importantly, delivers a balanced system out of the box, with no intricate configuration required. Here is the diagram they are discussing:

![A-P-EVA_and_VMware_BP](https://github.com/elatov/uploads/raw/master/2012/08/A-P-EVA_and_VMware_BP.png).

The recommended PSP for A/P Arrays is MRU.

ALUA is a protocol that makes an A/P Array psuedo A/A. If you more information on ALUA, I would suggest reading my [Using EMC VNX Storage with VMware vSphere](/2012/04/seeing-a-high-number-of-trespasses-from-a-clariion-array-with-esx-hosts/)" :

> vSphere 4.1 and later include an auto-registration feature that registers each SCSI initiator with the VNX storage system. When the host adapters login to the SP, a new server record is created with the ESXi host name. Each record is configured based on the storage array type the host discovers. NMP sets the storage array type for VNX to VMW_SATP_ALUA. This sets the host port to ALUA mode and sets the PSP for each LUN to VMW_PSP_FIXED.
>
> Although Fixed Path is the preferred PSP for VNX, Round Robin (VMW_PSP_RR) is also of interest in some environments due to the ability to actively distribute host I/O across all paths.
>
> ...
> ...
>
> In an environment where optimum host throughput is required, configure additional ESXi adapters to establish a dedicated path to the VNX iSCSI network portals. The sample configuration illustrated in Figure 34 on page 87 provides additional dedicated I/O paths for four VNX iSCSI target ports. In this configuration, two dedicated paths are available to each storage processor. This provides increased bandwidth to any LUNs presented to the host. It is possible to add additional ESXi and VNX iSCSI ports to further scale the configuration, and provide additional bandwidth if it is required within the environment.

Here is the mentioned diagram from that article:

![vnx-vmware-iscsi-bp](https://github.com/elatov/uploads/raw/master/2012/08/vnx-vmware-iscsi-bp.png)

For ALUA the PSP is usually MRU or Round Robin, depends on what the array vendor recommends. In vSphere 4.1 there a new PSP called Fixed_AP and that was used.


Each of the array types are described in "[vSphere Storage Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf)". Here is a snippet from that guide:

> **Active-active storage system**
> Allows access to the LUNs simultaneously through all the storage ports that are available without significant performance degradation. All the paths are active at all times, unless a path fails.
>
> **Active-passive storage system**
> A system in which one storage processor is actively providing access to a given LUN. The other processors act as backup for the LUN and can be actively providing access to other LUN I/O. I/O can be successfully sent only to an active port for a given LUN. If access through the active storage port fails, one of the passive storage processors can be activated by the servers accessing it.
>
> **Asymmetrical storage system**
> Supports Asymmetric Logical Unit Access (ALUA). ALUA-complaint storage systems provide different levels of access per port. ALUA allows hosts to determine the states of target ports and prioritize paths. The host uses some of the active paths as primary while others as secondary.

For the pathing policies, check out VMware KB [1011340](https://knowledge.broadcom.com/external/article?legacyId=1011340), from that KB:

> These pathing policies can be used with VMware ESX/ESXi 4.x and ESXi 5.x:
>
> *   Most Recently Used (MRU) — Selects the first working path, discovered at system boot time. If this path becomes unavailable, the ESX/ESXi host switches to an alternative path and continues to use the new path while it is available. This is the default policy for Logical Unit Numbers (LUNs) presented from an Active/Passive array. ESX/ESXi does not return to the previous path when if, or when, it returns; it remains on the working path until it, for any reason, fails.
>
> **Note:** The preferred flag, while sometimes visible, is not applicable to the MRU pathing policy and can be disregarded.
>
> *   Fixed (Fixed) — Uses the designated preferred path flag, if it has been configured. Otherwise, it uses the first working path discovered at system boot time. If the ESX/ESXi host cannot use the preferred path or it becomes unavailable, ESX/ESXi selects an alternative available path. The host automatically returns to the previously-defined preferred path as soon as it becomes available again. This is the default policy for LUNs presented from an Active/Active storage array.
>
> *   Round Robin (RR) — Uses an automatic path selection rotating through all available paths, enabling the distribution of load across the configured paths. For Active/Passive storage arrays, only the paths to the active controller will used in the Round Robin policy. For Active/Active storage arrays, all paths will used in the Round Robin policy.
>
> **Note:** This policy is not currently supported for Logical Units that are part of a Microsoft Cluster Service (MSCS) virtual machine.
>
> *   Fixed path with Array Preference — The VMW_PSP_FIXED_AP policy was introduced in ESX/ESXi 4.1. It works for both Active/Active and Active/Passive storage arrays that support ALUA. This policy queries the storage array for the preferred path based on the arrays preference. If no preferred path is specified by the user, the storage array selects the preferred path based on specific criteria.
>
> **Note:** The VMW_PSP_FIXED_AP policy has been removed from ESXi 5.0. For ALUA arrays in ESXi 5.0 the PSP MRU is normally selected but some storage arrays need to use Fixed

If the array is capable of using VAAI definitely use, this allows you to offload certain tasks to array. From the [vSphere Storage Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf):

> **Hardware Acceleration for Block Storage Devices**
> With hardware acceleration, your host can integrate with block storage devices, Fibre Channel or iSCSI, and use certain storage array operations. ESXi hardware acceleration supports the following array operations:
>
> *   Full copy, also called clone blocks or copy offload. Enables the storage arrays to make full copies of data within the array without having the host read and write the data. This operation reduces the time and network load when cloning virtual machines, provisioning from a template, or migrating with vMotion.
> *   Block zeroing, also called write same. Enables storage arrays to zero out a large number of blocks to provide newly allocated storage, free of previously written data. This operation reduces the time and network load when creating virtual machines and formatting virtual disks.
>
> *   Hardware assisted locking, also called atomic test and set (ATS). Supports discrete virtual machine locking without use of SCSI reservations. This operation allows disk locking per sector, instead of the entire LUN as with SCSI reservations.

If you want more information on how VAAI I would suggest reading the VMware blog entitled "[Performance Best Practices for VMware vSphere 5.0](https://blogs.vmware.com/vsphere/2012/06/low-level-vaai-behaviour.html)":

> For the best storage performance, consider using VAAI-capable storage hardware. The performance gains from VAAI can be especially noticeable in VDI environments (where VAAI can improve boot-storm and desktop workload performance), large data centers (where VAAI can improve the performance of mass virtual machine provisioning and of thin-provisioned virtual disks), and in other large-scale deployments.

Lastly if the array support VASA, then use it as well. VASA allows you to get array specific capabilities and then you can create a storage profile depending on the capabilities. This can definitely help out with your SLAs. From "[Profile Driven Storage](https://blogs.vmware.com/virtualblocks/2017/01/16/understanding-storage-policy-based-management/)":

> Managing datastores and matching the SLA requirements of virtual machines with the appropriate datastore can be a challenging and a cumbersome task. VMware vSphere 5.0 introduces Profile Driven Storage, which will allow for rapid and intelligent provisioning of virtual machines based on SLA requirements and provided storage capabilities.
>
> Using Profile Driven Storage different storage characteristics (typically defined as a tier) can be linked to a VM Storage Profile. These VM Storage Profiles are used during provisioning to ensure only those datastores or datastore clusters that are compliant with the VM Storage Profile are presented. Profile Driven Storage will reduce the amount of manual administration required for virtual machine provisioning while improving virtual machine SLA storage compliance.
>
> Profile Driven Storage delivers these benefits by taking advantage of the following items:
>
> *   Integrating with vStorage APIs for Storage Awareness enabling usage of storage characterization supplied by storage vendors.
> *   Enabling the vSphere administrator to tag storage based on customer or business specific descriptions.
> *   Using storage characterizations to create virtual machine placement rules in the form of storage profiles.
> *   Providing easy means to check a virtual machine's compliance against these rules.

The blog "[Configuring VASA with EMC arrays – CLARiiON, VNX and VMAX](https://blogs.vmware.com/vsphere/2011/10/emcs-vasa-implementation.html)" has great examples of how to set it up. Here are the capabilities that can be setup:

![vasa-cap-emc](https://github.com/elatov/uploads/raw/master/2012/08/vasa-cap-emc.png)

### Identify proper combination of media and port criteria for given end-to-end performance requirements.

From "[Performance Best Practices for VMware vSphere 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/Perf_Best_Practices_vSphere5.0.pdf)":

> *   Make sure that end-to-end Fibre Channel speeds are consistent to help avoid performance problems
> *   For iSCSI and NFS, make sure that your network topology does not contain Ethernet bottlenecks, where multiple links are routed through fewer links, potentially resulting in oversubscription and dropped network packets. Any time a number of links transmitting near capacity are switched to a smaller number of links, such over-subscription is a possibility.
> *   Consider using server-class network interface cards (NICs) for the best performance.
> *   Make sure the network infrastructure between the source and destination NICs doesn’t introduce bottlenecks. For example, if both NICs are 10 Gigabit, make sure all cables and switches are capable of the same speed and that the switches are not configured to a lower speed.
> *   In addition to the PCI and PCI-X bus architectures, we now have the PCI Express (PCIe) architecture. Ideally single-port 10 Gigabit Ethernet network adapters should use PCIe x8 (or higher) or PCI-X 266 and dual-port 10 Gigabit Ethernet network adapters should use PCIe x16 (or higher). There should preferably be no “bridge chip” (e.g., PCI-X to PCIe or PCIe to PCI-X) in the path to the actual Ethernet device (including any embedded bridge chip on the device itself), as these chips can reduce performance.
> *   To enable jumbo frames, set the MTU size to 9000 in both the guest network driver and the virtual switch configuration. The physical NICs at both ends and all the intermediate hops/routers/switches must also support jumbo frames.

### Specify the type of zoning that conforms to best practices and documentation.

From the vSphere Storage Guide":

> **Using Zoning with Fibre Channel SANs**
> Zoning provides access control in the SAN topology. Zoning defines which HBAs can connect to which targets. When you configure a SAN by using zoning, the devices outside a zone are not visible to the devices inside the zone. Zoning has the following effects:
>
> *   Reduces the number of targets and LUNs presented to a host.
> *   Controls and isolates paths in a fabric.
> *   Can prevent non-ESXi systems from accessing a particular storage system, and from possibly destroying VMFS data.
> *   Can be used to separate different environments, for example, a test from a production environment.
>
> With ESXi hosts, use a single-initiator zoning or a single-initiator-single-target zoning. The latter is a preferred zoning practice. Using the more restrictive zoning prevents problems and misconfigurations that can occur on the SAN.

Also From "[Secure SAN Zoning Best Practices](https://raw.githubusercontent.com/elatov/upload/master/vcap-dcd/3-3/Zoning_Best_Practices_WP-00.pdf)":

> Zoning not only prevents a host from unauthorized access of storage assets, but it also stops undesired host-to-host communication and fabric-wide Registered State Change Notification (RSCN) disruptions. RSCNs are managed by the fabric Name Server and notify end devices of events in the fabric, such as a storage node or a switch going offline. Brocade isolates these notifications to only the zones that require the update, so nodes that are unaffected by the fabric change do not receive the RSCN. This is important for non-disruptive fabric operations, because RSCNs have the potential to disrupt storage traffic.
>
> There are two types of Zoning identification: port World Wide Name (pWWN) and Domain,Port (D,P). You can assign aliases to both pWWN and D,P identifiers for easier management. The pWWN, the D,P, or a combination of both can be used in a zone configuration or even in a single zone. pWWN identification uses a globally unique identifier built into storage and host interfaces. Interfaces also have node World Wide Names (nWWNs). As their names imply, pWWN refers to the port on the device, while nWWN refers to the overall device. For example, a dual-port HBA has one nWWN and two pWWNs. Always use pWWN identification instead of nWWN, since a pWWN precisely identifies the host or storage that needs to be zoned.

Lastly from [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> Use WWN zoning rather than port Zoning , allows you to move cables to different ports without affecting zoning

The last one kind of contradicts Brocades best practices, but it just depends on what your goal is. If you want flexibility use nWWNs, if you want security use pWWNs.

### Based on service level requirements utilize VMware technologies, including but not limited to: Storage I/O Control, Storage Policies, Storage vMotion, Storage DRS

From "[Performance Best Practices for VMware vSphere 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/Perf_Best_Practices_vSphere5.0.pdf)"

> **Storage I/O Resource Allocation**
> VMware vSphere provides mechanisms to dynamically allocate storage I/O resources, allowing critical workloads to maintain their performance even during peak load periods when there is contention for I/O resources. This allocation can be performed at the level of the individual host or for an entire datastore. Both methods are described below.
>
> *   The storage I/O resources available to an ESXi host can be proportionally allocated to the virtual machines running on that host by using the vSphere Client to set disk shares for the virtual machines (select Edit virtual machine settings, choose the Resources tab, select Disk, then change the Shares field).
> *   The maximum storage I/O resources available to each virtual machine can be set using limits. These limits, set in I/O operations per second (IOPS), can be used to provide strict isolation and control on certain workloads. By default, these are set to unlimited. When set to any other value, ESXi enforces the limits even if the underlying datastores are not fully utilized.
> *   An entire datastore’s I/O resources can be proportionally allocated to the virtual machines accessing that datastore using Storage I/O Control (SIOC). When enabled, SIOC evaluates the disk share values set for all virtual machines accessing a datastore and allocates that datastore’s resources accordingly. SIOC can be enabled using the vSphere Client (select a datastore, choose the Configuration tab, click Properties...(at the far right), then under Storage I/O Control add a checkmark to the Enabled box).
>
> With SIOC disabled (the default), all hosts accessing a datastore get an equal portion of that datastore’s resources. Any shares values determine only how each host’s portion is divided amongst its virtual machines.
>
> With SIOC enabled, the disk shares are evaluated globally and the portion of the datastore’s resources each host receives depends on the sum of the shares of the virtual machines running on that host relative to the sum of the shares of all the virtual machines accessing that datastore.

If you want more information on how SIOC works, I would suggest reading "[Performance Implications of Storage I/O Control– Enabled NFS Datastores in VMware vSphere 5.0](https://blogs.vmware.com/performance/2011/08/sioc-nfs.html)".

From "[VMware Storage VMotion](https://blogs.vmware.com/vsphere/2011/03/under-the-covers-with-storage-vmotion.html)":

> **How is VMware Storage VMotion Used in the Enterprise?**
> Customers use VMware Storage VMotion to:
>
> *   Simplify array migrations and storage upgrades.The traditional process of moving data to new storage is cumbersome, time-consuming and disruptive. With Storage VMotion, IT organizations can accelerate migrations while minimizing or eliminating associated service disruptions, making it easier, faster and more cost-effective to embrace new storage platforms and file formats, take advantage of flexible leasing models, retire older, hard-to-manage storage arrays and to conduct storage upgrades and migrations based on usage and priority policies. Storage VMotion works with any operating system and storage hardware platform supported by VMware ESX™, enabling customers to use a heterogeneous mix of datastores and file formats.
> *   Dynamically optimize storage I/O performance.Optimizing storage I/O performance often requires reconfiguration and reallocation of storage, which can be a highly disruptive process for both administrators and users and often requires scheduling downtime. With Storage VMotion, IT administrators can move virtual machine disk files to alternative LUNs that are properly configured to deliver optimal performance without the need for scheduled downtime, eliminating the time and cost associated with traditional methods
> *   Efficiently manage storage capacity.Increasing or decreasing storage allocation requires multiple manual steps, including coordination between groups, scheduling downtime and adding additional storage. This is then followed by a lengthy migration of virtual machine disk files to the new datastore, resulting in significant service downtime. Storage VMotion improves this process by enabling administrators to take advantage of newly allocated storage in a non-disruptive manner. Storage VMotion can also be used as a storage tiering tool by moving data to different types of storage platforms based the data value, performance requirements and storage costs.

From "[Performance Best Practices for VMware vSphere 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/Perf_Best_Practices_vSphere5.0.pdf)":

> **VMware Storage Distributed Resource Scheduler (Storage DRS)**
> A new feature in vSphere 5.0, Storage Distributed Resource Scheduler (Storage DRS), provides I/O load balancing across datastores within a datastore cluster (a new vCenter object). This load balancing can avoid storage performance bottlenecks or address them if they occur.This section lists Storage DRS practices and configurations recommended by VMware for optimal performance.
>
> *   When deciding which datastores to group into a datastore cluster, try to choose datastores that are as homogeneous as possible in terms of host interface protocol (i.e., FCP, iSCSI, NFS), RAID level, and performance characteristics. We recommend not mixing SSD and hard disks in the same datastore cluster. Don’t configure into a datastore cluster more datastores or virtual disks than the maximum allowed in Configuration Maximums for VMware vSphere 5.0.
> *   While a datastore cluster can have as few as two datastores, the more datastores a datastore cluster has, the more flexibility Storage DRS has to better balance that cluster’s I/O load.
> *   As you add workloads you should monitor datastore I/O latency in the performance chart for the datastore cluster, particularly during peak hours. If most or all of the datastores in a datastore cluster consistently operate with latencies close to the congestion threshold used by Storage I/O Control (set to 30ms by default, but sometimes tuned to reflect the needs of a particular deployment), this might be an indication that there aren't enough spare I/O resources left in the datastore cluster. In this case, consider adding more datastores to the datastore cluster or reducing the load on that datastore cluster.
> *   By default, Storage DRS affinity rules keep all of a virtual machine’s virtual disks on the same datastore (using intra-VM affinity). However you can give Storage DRS more flexibility in I/O load balancing, potentially increasing performance, by overriding the default intra-VM affinity rule. This can be done for either a specific virtual machine (from the vSphere Client, select Edit Settings > Virtual Machine Settings, then deselect Keep VMDKs together) or for the entire datastore cluster (from the vSphere Client, select Home > Inventory > Datastore and Datastore Clusters, select a datastore cluster, select the Storage DRS tab, click Edit, select Virtual Machine Settings, then deselect Keep VMDKs together).
> *   Inter-VM anti-affinity rules can be used to keep the virtual disks from two or more different virtual machines from being placed on the same datastore, potentially improving performance in some situations. They can be used, for example, to separate the storage I/O of multiple workloads that tend to have simultaneous but intermittent peak loads, preventing those peak loads from combining to stress a single datastore.
> *   If a datastore cluster contains thin-provisioned LUNs, make sure those LUNs don’t run low on backing disk space. If many thin-provisioned LUNs in a datastore cluster simultaneously run low on backing disk space (quite possible if they all share the same backing store), this could cause excessive Storage vMotion activity or limit the ability of Storage DRS to balance datastore usage.

If you want more information on Storage DRS I would suggest reading "[An Introduction to Storage DRS](http://www.yellow-bricks.com/2012/05/22/an-introduction-to-storage-drs/)", it has many other useful on how it works.

Using all the functions mentioned above you can plan for upgrades appropriately, you can make sure all the VMs get fair access/performance to a datastore, and you can dynamically move your VMs to accommodate your environment's needs.

### Determine use case for virtual storage appliances, including the vSphere Storage Appliance

If you don't plan on getting a SAN and you are an SMB (small and medium-sized business) then this might be perfect. From "[VMware vSphere Storage Appliance](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-vsa-datasheet.pdf)":

> What Does vSphere Storage Appliance Deliver?
> For many small environments (ranging from the smallest branch office to growing SMBs), virtualizing servers has required them to deal with the complexities of shared storage for the first time. Not anymore. VSA provides High Availability and automation capabilities of vSphere to any small environment without shared storage hardware. Get business continuity for all your applications, eliminate planned downtime due to server maintenance, and use policies to prioritize resources for your most important applications. VSA enables you to do all this, without shared storage hardware.

There is a good cost-comparison [here](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-vsa-datasheet.pdf):

![cost-comparison-vsa](https://github.com/elatov/uploads/raw/master/2012/08/cost-comparison-vsa.png)

By combining all the local storage and replicating between the local disks, it allows for shared storage and has redundancy built into it. From the same cost-comparison page, here is how the traditional SAN setup looks like:

![trad-san](https://github.com/elatov/uploads/raw/master/2012/08/trad-san.png)

And here is how the VSA works:

![vsa-san](https://github.com/elatov/uploads/raw/master/2012/08/vsa-san.png)

If you want more information on how the VSA works, please read "[VMware vSphere Storage Appliance Technical Deep Dive](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vm-vsphere-storage-appliance-deep-dive-white-paper.pdf)"

### Given the functional requirements, size the storage for capacity, availability and performance, including: Virtual Storage, Physical Storage

From "[VMware Virtual Machine File System: Technical Overview and Best Practices](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmware-vsphere-vmfs-best-practices-whitepaper.pdf)":

> **How Large a LUN?**
> The best way to configure a LUN for a given VMFS volume is to size for throughput first and capacity second. That is, you should aggregate the total I/O throughput for all applications/VMs that might run on a given shared pool of storage, then make sure you have provisioned enough back-end disk spindles (disk array cache) and appropriate storage service to meet the requirements.
>
> This is actually no different from what most system administrators do in a physical environment. It just requires an extra step to consider when consolidating a number of workloads onto a single ESX server, or onto a collection of ESX servers that are addressing a shared pool of storage.
>
> The storage vendor likely has its own recommendation for the size of a provisioned LUN, so it’s best to check with them. However, if the vendor’s stated optimum LUN capacity is backed with a single disk that has no storage array write cache, the configuration could result in low performance in a virtual environment. In this case, a better solution might be a smaller LUN striped within the storage array across many physical disks, with some write cache in the array. The RAID protection level also factors into the I/O throughput performance. Remember, there is no single correct answer to the question of how large your LUNs should be for a VMFS volume.

From the same document:

> **Isolation or Consolidation?**
> The decision to “isolate or consolidate” storage resources for virtual environments is a topic of some debate. The basic answer comes down to the nature of the I/O access patterns of that VM. If you have a really heavy I/O-generating application, then it might be worth the potentially inefficient use of resources to allocate a single LUN to a single VM. This can be accomplished using either an RDM or a VMFS volume that is dedicated to a single VM. Both these types of volumes perform similarly (within 5 percent of each other) with varying read and write sizes and I/O access patterns. Figure 2 illustrates the differences between isolation and consolidation.

Here is the diagram they are referring to:

![iso_vs_cons](https://github.com/elatov/uploads/raw/master/2012/08/iso_vs_cons.png)

And more information from the document:

> **Best practice: Mix consolidation with some isolation!**
> In general, it’s wise to separate heavy I/O workloads out of the shared pool of storage to optimize the performance of those high transactional throughput applications—an approach best characterized as “consolidation with some level of isolation.”
>
> Because workloads will vary, when looking at the number of VMs per LUN there is no exact rule to determine the limits of performance and scalability. These limits also depend on the number of ESX servers sharing concurrent access to a given VMFS volume. The key is to recognize the upper limit of 255 LUNs and understand that this number can limit the consolidation ratio if you take the concept of “1 LUN per VM” too far.
>
> Many different applications can easily and effectively share a clustered pool of storage. And what little might be lost to increased contention can clearly be worth the increase in disk utilization and improvements in management efficiency.

And more:

> **Why Use RDMs?**
> Even with all the advantages of VMFS, there are still some cases where it makes more sense to use RDM storage access. Two scenarios that call for raw disk mapping are:
>
> *    Migrating an existing application from a physical environment to virtualization
> *    Using Microsoft Cluster Services (MSCS) for clustering in a virtual environment

Here are some more reasons to use RDMs:

*   If you install a SAN Management Software inside a VM
*   Certain backup software requires to use RDMs (more information can be found in my [previous](/2012/03/netapp-snapmanagersnapdrivesme-causes-esx-host-to-hang/) post)

Duncan Epping also has a formula for this, from "[VMFS/LUN size?](http://www.yellow-bricks.com/2009/06/23/vmfslun-size/)":

> Most companies can use a simple formula in my opinion. First you should answer these questions:
>
> *   What’s the maximum amount of VMs you’ve set for a VMFS volume?
> *   What’s the average size of a VM in your environment? (First remove the really large VM’s that typically get an RDM.)
>
> If you don’t know what the maximum amount of VMs should be just use a safe number, anywhere between 10 and 15. Here’s the formula I always use:
>
>     round((maxVMs * avgSize) + 20% )
>
>
> I usually use increments of 25GB. This is where the round comes in to play. If you end up with 380GB round it up to 400GB and if you end up with 321GB round it up to 325GB. Let’s assume your average VM size is 30GB and your max amount of VMs per VMFS volume is 10:
>
>     (10*30) + 60 =360
>     360 rounded up -> 375GB >
>

As mentioned some array vendors provide recommendations as well, from "[Sizing LUNs – A Citrix Perspective](https://www.citrix.com/blogs/2014/01/02/new-citrix-best-practices/)":

> Most people seem to agree that 10-25 VMDKs per LUN is the “sweet spot” or “magic number” and that typically results in LUN sizes anywhere from 300-700 GB. Before you freak out, please keep in mind those are just AVERAGES and 500 GB LUNs with 16 VMs per LUN certainly won’t work in every situation.

From "[Scalable Storage Performance](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/scalable_storage_performance.pdf)":

> A maximum number of outstanding I/O commands to the shared LUN (or VMFS volume) that depends on the storage array. This number must be determined for a particular storage array configuration supporting multiple ESX hosts. If the storage array has a per‐LUN queue depth, exceeding this value causes high latencies. If the storage array does not have a per‐LUN queue depth, the bottleneck is shiftedto the disks, and latencies increase. In either case, it is important to ensure that there are enough disks tosupport the influx of commands. It is hard to recommend an upper threshold for latency because it depends on individual applications. However, a 50 millisecond latency is high enough for most applications, and you should add more physical resources if you reach that point.
>
> Table 2 illustrates how to compute the maximum number of virtual machines per LUN. The numbers in the n column represent the maximum outstanding number of I/O commands recommended for a LUN on a particular storage array. This is an array‐specific parameter that has to be determined in consultation with the storage vendor. The numbers in the a column represent the average number of active I/O commands per virtual machine sharing the same LUN.

Here is the table from that document:

![iops_per_vmfs](https://github.com/elatov/uploads/raw/master/2012/08/iops_per_vmfs.png)

There is a pretty good example from [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> Tiering Example:
>
> {:.kt}
> |Tier| Disk_Type |Disk_RPM | Raid_Level| #_of_Disks | #_of_VMs_per_Datastore 1|
> |:---|:---------:|:-------:|:----------:|:---------:|:-----------------------:|
> | FC| 15K        |10       | 8          | 10        | 2         |
> | SAS|10K        | 5       | 6          | 15        | 3         |
> | SATA | 7.2K    | 6       | 6          | 6         | 15        |


### Based on the logical design, select and incorporate an appropriate storage network into the physical design: iSCSI, NFS, FC, FCoE

From "[Fibre Channel SAN Topologies](https://github.com/elatov/uploads/raw/master/2013/01/h8074-fibre-channel-san-tb.pdf)"

> Consider the following best practices:
>
> *   Plan for failures
>     *   Connect the host and storage ports in such a way as to prevent a single point of failure from affecting redundant paths. For example, if you have a dual-attached host and each HBA accesses its storage through a different storage port, do not place both storage ports for the same server on the same Line Card or ASIC.
>     *   Use two power sources.
> *   For host and storage layout
>     *   To reduce the possibility of congestion, and maximize ease of management, connect hosts and storage port pairs to the same switch where possible.
> *   Use single initiator zoning
>     *   For Open Systems environments, ideally each initiator will be in a zone with a single target. However, due to the significant management overhead that this can impose, single initiator zones can contain multiple target ports but should never contain more than 16 target ports.

From "[Optimizing the Performance and Management of 2 GBIT/SEC SAN Fabrics with ISL Trunking](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/KG010903.pdf)":

> Long used in traditional Ethernet networking, Inter-Switch Link (ISL) Trunking can also dramatically improve the performance, manageability, and reliability for business-critical storage applications in Fibre Channel environments. By aggregating up to four ISLs into a single logical 8 Gbit/sec trunk group, this feature supports efficient high-speed communications throughout Storage Area Networks (SANs). By optimizing available switch resources, ISL Trunking decreases congestion.

From "[SAN Conceptual and Design Basics](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/esx_san_cfg_technote.pdf)":

![san-redundancy](https://github.com/elatov/uploads/raw/master/2012/08/san-redundancy.png)

So with FC use multipathing to plan for redundancy and for performance, and try to have a similar setup as the diagram above. To get rid of congestion, utilize ISL Trunking where possible. Try not to have two different vendors of HBAs. Either have all Qlogic or all Emulex. Also instead of getting 1 dual port HBA, get 2 single port HBA, this will help if a failure occurs.

From "[Performance Best Practices for VMware vSphere 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/Perf_Best_Practices_vSphere5.0.pdf)":

> *   For iSCSI and NFS, make sure that your network topology does not contain Ethernet bottlenecks, where multiple links are routed through fewer links, potentially resulting in over-subscription and dropped network packets. Any time a number of links transmitting near capacity are switched to a smaller number of links, such over-subscription is a possibility.
>     *   Recovering from these dropped network packets results in large performance degradation. In addition to time spent determining that data was dropped, the retransmission uses network bandwidth that could otherwise be used for new transactions.
> *   For iSCSI and NFS, if the network switch deployed for the data path supports VLAN, it might be beneficial to create a VLAN just for the ESXi host's vmknic and the iSCSI/NFS server. This minimizes network interference from other packet sources.
> *   Be aware that with software-initiated iSCSI and NFS the network protocol processing takes place on the host system, and thus these might require more CPU resources than other storage options.

From "[vSphere Storage Guide](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-storage-guide.pdf)":

> Configuration changes to avoid this problem involve making sure several input Ethernet links are not funneled into one output link, resulting in an oversubscribed link. When a number of links transmitting near capacity are switched to a smaller number of links, oversubscription is a possibility.
>
> Generally, applications or systems that write a lot of data to storage, such as data acquisition or transaction logging systems, should not share Ethernet links to a storage device. These types of applications perform best with multiple connections to storage devices.

Here is a diagram from the above article:

![multiple_links_over_iscsi](https://github.com/elatov/uploads/raw/master/2012/08/multiple_links_over_iscsi.png).

If using Software iSCSI use port binding to enable multipathing. From "[Multipathing Configuration for Software iSCSI Using Port Binding](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmware-multipathing-configuration-software-iscsi-port-binding-white-paper.pdf)":

> **Multipathing for Software iSCSI**
> Multipathing between a server and storage array provides the ability to load-balance between paths when all paths are present and to handle failures of a path at any point between the server and the storage. Multipathing is a de facto standard for most Fibre Channel SAN environments. In most software iSCSI environments, multipathing is possible at the VMkernel network adapter level, but not the default configuration.
>
> In a VMware vSphere® environment, the default iSCSI configuration for VMware® ESXi™ servers creates only one path from the software iSCSI adapter (vmhba) to each iSCSI target. To enable failover at the path level and to load-balance I/O traffic between paths, the administrator must configure port binding to create multiple paths between the software iSCSI adapters on ESXi servers and the storage array.
>
> Without port binding, all iSCSI LUNs will be detected using a single path per target. By default, ESX will use only one vmknic as egress port to connect to each target, and you will be unable to use path failover or to loadbalance I/O between different paths to the iSCSI LUNs. This is true even if you have configured network adapter teaming using more than one uplink for the VMkernel port group used for iSCSI. In case of simple network adapter teaming, traffic will be redirected at the network layer to the second network adapter during connectivity failure through the first network card, but failover at the path level will not be possible, nor will load balancing between multiple paths.

With iSCSI think about either getting hardware or software adapters. With hardware adapters it does save on CPU but it does waste an extra PCI slot. Now a days CPU is pretty cheap and Software iSCSI performs almost the same as the iSCSI HBA. Use Jumbo to help with performance, but make sure it's end-to-end. Also with 1Gb Jumbo Frames the performance is minimal but definitely use Jumbo Frames with 10Gb.

From "[NetApp and VMware vSphere Storage Best Practices](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/tr-3749.pdf)"

> **10GBE OR DATA CENTER ETHERNET**
> NetApp Data ONTAP and VMware ESX/ESXi 4 both provide support for 10GbE. An advantage of 10GbE is the ability to reduce the number of network ports in the infrastructure, especially for blade servers
>
> **VLAN TAGGING OR 802.1Q**
> NetApp recommends that the service console access with the VM network should be on one VLAN, and the VMkernel activities of IP storage and vMotion should be on a second VLAN.
>
> VLANs and VLAN tagging also play a simple but important role in securing an IP storage network. NFSexports can be restricted to a range of IP addresses that are available only on the IP storage VLAN. In addition, NetApp storage also allows the restriction of the iSCSI protocol to specific interfaces and/or VLAN tags. These simple configuration settings have an enormous effect on the security and availability of IP-based datastores. If you are using multiple VLANs over the same interface, make sure that sufficient throughput can be provided for all traffic.
>
> **FLOW CONTROL**
> Flow control is a low-level process for managing the rate of data transmission between two nodes to prevent a fast sender from overrunning a slow receiver. Flow control can be configured on ESX/ESXi servers, FAS storage arrays, and network switches. For modern network equipment, especially 10GbE equipment, NetApp recommends turning off flow control and allowing congestion management to be performed higher in the network stack. For older equipment, typically GbE with smaller buffers and weaker buffer management, NetApp recommends configuring the endpoints, ESX servers, and NetApp arrays with the flow control set to "send."
>
> For modern network switches, NetApp recommends disabling flow control by configuring ports as -send off‖ and -receive off.‖
>
> For older network switches, NetApp recommends either setting the switch ports connecting to the ESX hosts and FAS storage arrays to "Desired" or, if this mode is not available, setting these ports to "send off" and "receive on." The switch ports are configured with settings opposite to those of the ESX/ESXi and FAS systems

Here is a diagram for flow control from the above paper:

![flow-control-nfs](https://github.com/elatov/uploads/raw/master/2012/08/flow-control-nfs.png)

More from the same paper:

> **ROUTING AND IP STORAGE NETWORKS**
> Whenever possible, NetApp recommends configuring storage networks as a single network that does not route. This model helps to provide good performance and a layer of data security
>
> **ENABLING JUMBO FRAMES** In Ethernet networking, the maximum transmission unit (MTU) is the size of the largest unit that the layer can forward. The standard MTU size is 1,500 bytes. In an effort to reduce the number of data units and the processing associated with each, some prefer to use a large packet size. This is referred to as a jumbo frame, and it is commonly 9,000 bytes.
>
> Enabling jumbo frames requires making manual changes to all networking devices between ESX and storage, and therefore its use should be considered prior to being enabled.
>
> That maximum is typically 9,216 bytes in today’s modern data center–class switches. If the switching infrastructure being used does not accommodate this size, you must verify the endpoint frame size you configure and append the Ethernet header and VLAN tag. If your infrastructure is not configured to accommodate the payload plus header and VLAN tag, your environment either will not successfully negotiate communications or will suffer severe performance penalties.

Another diagram from the same paper:

![jumbo_frames](https://github.com/elatov/uploads/raw/master/2012/08/jumbo_frames.png)

More information, from the same article:

> **SEPARATE ETHERNET STORAGE NETWORK**
> As a best practice, NetApp recommends separating IP-based storage traffic from public IP network traffic by implementing separate physical network segments or VLAN segments. This design follows the architecture of SCSI and FC connectivity.
>
> **NETAPP VIRTUAL INTERFACES (ETHERCHANNEL)**
> A virtual network interface (VIF) or EtherChannel is a mechanism that supports aggregation of network interfaces into one logical interface unit. Once created, a VIF is indistinguishable from a physical network interface. VIFs are used to provide fault tolerance of the network connection and in some cases higher throughput to the storage device.
>
> NetApp enables the use of two types of load-balancing VIFs: manual multimode and dynamic LACP (IEEE 802.3ad). NetApp also provides an active-passive form of VIF, referred to as a single-mode VIF. NetApp VIFs may also be grouped and layered into a form of a second-level VIF, referred to in this document as layered multimode EtherChannel.

Here is a couple pictures of how to use etherchannel with a NetApp Array.

![etherchannel_netapp](https://github.com/elatov/uploads/raw/master/2012/08/etherchannel_netapp.png)

and this:

![ip_hash_with_netapp](https://github.com/elatov/uploads/raw/master/2012/08/ip_hash_with_netapp.png)

So for NFS try to use etherchannel to allow load balancing. Use jumbo frames, with 10Gb preferrebly. If using old switches, use flow control to control congestion. Make sure you have a dedicated network for your NFS traffic and don't route your NFS traffic. More information on NAS and VMware can be seen in "[Best Practices for running VMware vSphere on Network Attached Storage](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vmware-nfs-bestpractices-white-paper-en.pdf)".

From "Introduction to Fibre Channel over Ethernet (FCoE)", here is a good picture of how FCoE is setup in an environment:

![fcoe-env](https://github.com/elatov/uploads/raw/master/2012/08/fcoe-env.png)

The technology is kind of new and has it's issues. It does allow you to have all of your traffic going down one technology. The CNA can be your NIC and your HBA, the switch that we are connected to will have to encapsulate your Fibre Channel Protocol over Ethernet. These switches are really expensive but are around the same prices as SAN switches. Since FCoE is lossless, pause frames are utilized heavily during congestion, if the switch can't handle that then you will run into issues. You are also putting all of your eggs in one basket, if the FCoE switch dies then your networking and your storage are down. If you want to know more information regarding FCoE, I would suggest reading:

*   [User’s Guide Converged Network Adapter](https://raw.githubusercontent.com/elatov/upload/master/vcap-dcd/3-3/User_Guide_Converged_Network_Adapter_8100_Series_A.pdf)
*   [QLogic Adapters and Cisco Nexus 5000 Series Switches: Fibre Channel over Ethernet Design Guide](http://www.cisco.com/en/US/prod/collateral/switches/ps9441/ps9670/white_paper_c11-569320_v1.pdf)
*   [Nexus 1000V with FCoE CNA and VMWare ESX 4.0 deployment diagram](http://bradhedlund.com/2009/01/01/nexus-1000v-with-fcoe-cna-and-vmware-esx-40-deployment-diagram/)

I would suggest watching [APAC BrownBag Session 2](https://professionalvmware.com/vmware-certifications/), it covers most of the above material.

