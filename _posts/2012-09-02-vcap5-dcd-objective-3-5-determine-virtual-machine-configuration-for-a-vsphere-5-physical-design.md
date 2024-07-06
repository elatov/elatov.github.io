---
title: VCAP5-DCD Objective 3.5 – Determine Virtual Machine Configuration for a vSphere 5 Physical Design
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-3-5-determine-virtual-machine-configuration-for-a-vsphere-5-physical-design/
categories: ['certifications', 'vcap5_dcd', 'vmware']
tags: ['performance', 'vhw', 'thick_provisioning', 'vapp', 'physical_design', 'rdm','thin_provisioning', 'fault_tolerance']
---

### Describe the applicability of using an RDM or a virtual disk for a given VM

This was covered in [APAC BrownBag Session 12](/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/):

![rdm_for_vms](https://github.com/elatov/uploads/raw/master/2012/09/rdm_for_vms.png)

### Based on the service catalog and given functional requirements, for each service: Determine the most appropriate virtual machine configuration for the design

From [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> **Virtual Machine CPUs:**
>
> *   How Many? Default to 1. Scale up, if there is a need
> *   If using SMP VMs, make sure apps are multi-threaded so they can use 2x or 4x CPUs
> *   If the App is not multi-threaded, use single vCPU VMs
> *   Use as few vCPUs as possible
> *   Number of vCPUs cannot exceed the core/hyperthread count in a host, it must be possible for all vCPUs to be scheduled
>
> **Virtual Machine Memory:**
>
> *   Keep all guest active memory in physical RAM
> *   Limit host memory over commitment, or set reservations, or both
> *   Reservations should best slightly higher than avg active memory size (for overhead)
> *   Always have Transparent Page Sharing Enabled
> *   Always use VMware tools and always enabled balooning

### Based on an existing logical design, determine appropriate virtual disk type and placement

From "[vSphere Virtual Machine Administration ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-703-virtual-machine-admin-guide.pdf)":

> **About Virtual Disk Provisioning Policies**
> When you perform certain virtual machine management operations, such as creating a virtual disk, cloning a virtual machine to a template, or migrating a virtual machine, you can specify a provisioning policy for the virtual disk file.
>
> NFS datastores with Hardware Acceleration and VMFS datastores support the following disk provisioning policies. On NFS datastores that do not support Hardware Acceleration, only thin format is available.
>
> You can use Storage vMotion to transform virtual disks from one format to another.
>
> *   **Thick Provision Lazy Zeroed** Creates a virtual disk in a default thick format. Space required for the virtual disk is allocated when the virtual disk is created. Data remaining on the physical device is not erased during creation, but is zeroed out on demand at a later time on first write from the virtual machine. Using the default flat virtual disk format does not zero out or eliminate the possibility of recovering deleted files or restoring old data that might be present on this allocated space. You cannot convert a flat disk to a thin disk.
> *   **Thick Provision Eager Zeroed** A type of thick virtual disk that supports clustering features such as Fault Tolerance. Space required for the virtual disk is allocated at creation time. In contrast to the flat format, the data remaining on the physical device is zeroed out when the virtual disk is created. It might take much longer to create disks in this format than to create other types of disks.
> *   **Thin Provision** Use this format to save storage space. For the thin disk, you provision as much datastore space as the disk would require based on the value that you enter for the disk size. However, the thin disk starts small and at first, uses only as much datastore space as the disk needs for its initial operations. **NOTE** If a virtual disk supports clustering solutions such as Fault Tolerance, do not make the disk thin. If the thin disk needs more space later, it can grow to its maximum capacity and occupy the entire datastore space provisioned to it. Also, you can manually convert the thin disk into a thick disk.

From the same document:

> **SCSI Controller Configuration**
> To access virtual disks, a virtual machine uses virtual SCSI controllers. These virtual controllers appear to a virtual machine as different types of controllers, including BusLogic Parallel, LSI Logic Parallel, LSI Logic SAS, and VMware Paravirtual. You can add a SCSI controller, change the SCSI controller type, and select bus sharing for a virtual machine.
>
> You configure virtual SCSI controllers on your virtual machines to attach virtual disks and RDMs to. The choice of SCSI controller does not affect whether your virtual disk is an IDE or SCSI disk. The IDE adapter is always ATAPI. The default for your guest operating system is already selected. Older guest operating systems default to the BusLogic adapter.
>
> If you create an LSI Logic virtual machine and add a virtual disk that uses BusLogic adapters, the virtual machine boots from the BusLogic adapters disk. LSI Logic SAS is available only for virtual machines with hardware version 7. Disks with snapshots might not experience performance gains when used on LSI Logic SAS, VMware Paravirtual, and LSI Logic Parallel adapters.
>
> Disks with snapshots might not experience performance gains when used on LSI Logic SAS and LSI Logic Parallel controllers.
>
> **About VMware Paravirtual SCSI Controllers**
> Paravirtual SCSI (PVSCSI) controllers are high performance storage controllers that can result in greater throughput and lower CPU use. PVSCSI controllers are best suited for high-performance storage environments. PVSCSI controllers are available for virtual machines running hardware version 7 and later.
>
> PVSCSI controllers have the following limitations:
>
> *   Hot add or remove requires a bus rescan from within the guest operating system.
> *   Disks on PVSCSI controllers might not experience performance gains if they have snapshots or if memory on the ESXi host is over committed.
> *   MSCS clusters are not supported.
> *   PVSCSI controllers do not support boot disks, the disk that contains the system software, on Red Hat Linux 5 virtual machines. Attach the boot disk to the virtual machine by using any of the other supported controller types.

From [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> VM Disks:
>
> *   Deploy a system and data disk
> *   Don't place all system disks on one datastore and data disks on another
> *   Put system and data disk on the same datastore, unless they have widely varying I/O characteristics
> *   Simplifies SRM and snapshots, unless the vdisk is very large
> *   Configure one partition per vdisk
>
> Swap Location:
>
> 1.  Default Shared datastore with VM files Con is that swap files are replicated with SRM
> 2.  Local storage: reduces replication time. Local swap should not affect VM performance. Slow vMotion Migration
> 3.  Dedicated vSwap SAN Datastore, Good vMotion performance, non-replicated LUN, Con is that there is Admin overhead
>
> Disk Adapters:
>
> *   MSCS requires SAS Adapters for shared and quorum disks
> *   Use PVSCSI adapter for performance gain
> *   Can't boot from PVSCSI adapters
> *   PVSCSI is not suited for local storage
> *   Snapshot can negate performance of PVSCSI
> *   Not Supported with FT From "

[Performance Best Practices for VMware vSphere 5.0](http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf)":

> **Guest Operating System Storage Considerations**
>
> *   The default virtual storage adapter in ESXi 5.0 is either BusLogic Parallel, LSI Logic Parallel, or LSI Logic SAS, depending on the guest operating system and the virtual hardware version. However, ESXi also includes a paravirtualized SCSI storage adapter, PVSCSI (also called VMware Paravirtual). The PVSCSI adapter offers a significant reduction in CPU utilization as well as potentially increased throughput compared to the default virtual storage adapters, and is thus the best choice for environments with very I/O-intensive guest applications.
> *   If you choose to use the BusLogic Parallel virtual SCSI adapter, and are using a Windows guest operating system, you should use the custom BusLogic driver included in the VMware Tools package.
> *   The depth of the queue of outstanding commands in the guest operating system SCSI driver can significantly impact disk performance. A queue depth that is too small, for example, limits the disk bandwidth that can be pushed through the virtual machine. See the driver-specific documentation for more information on how to adjust these settings.
> *   In some cases large I/O requests issued by applications in a virtual machine can be split by the guest storage driver. Changing the guest operating system’s registry settings to issue larger block sizes can eliminate this splitting, thus enhancing performance. For additional information see VMware KB article 9645697.
>
> Make sure the disk partitions within the guest are aligned. For further information you might want to refer to the literature from the operating system vendor regarding appropriate tools to use as well as recommendations from the array vendor.

### Size VMs appropriately according to application requirements, incorporating VMware best practices

From "[Performance Best Practices for VMware vSphere 5.0](http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf)":

> *   In most environments ESXi allows significant levels of CPU over commitment (that is, running more vCPUs on a host than the total number of physical processor cores in that host) without impacting virtual machine performance.
> *   Configuring a virtual machine with more virtual CPUs (vCPUs) than its workload can use might cause slightly increased resource usage, potentially impacting performance on very heavily loaded systems. Common examples of this include a single-threaded workload running in a multiple-vCPU virtual machine or a multi-threaded workload in a virtual machine with more vCPUs than the workload can effectively use.
> *   Even if the guest operating system doesn’t use some of its vCPUs, configuring virtual machines with those vCPUs still imposes some small resource requirements on ESXi that translate to real CPU consumption on the host. For example:
>     *   Unused vCPUs still consume timer interrupts in some guest operating systems.
>     *   Maintaining a consistent memory view among multiple vCPUs can consume additional resources,both in the guest operating system and in ESXi. (Though hardware-assisted MMU virtualization significantly reduces this cost.)
>     *   Most guest operating systems execute an idle loop during periods of inactivity. Within this loop, most of these guest operating systems halt by executing the HLT or MWAIT instructions. Some older guest operating systems (including Windows 2000 (with certain HALs), Solaris 8 and 9, and MS-DOS), however, use busy-waiting within their idle loops. This results in the consumption of resources that might otherwise be available for other uses (other virtual machines, the VMkernel, and so on).
>     *   ESXi automatically detects these loops and de-schedules the idle vCPU. Though this reduces the CPU overhead, it can also reduce the performance of some I/O-heavy workloads. For additional information see VMware KB articles 1077 and 2231.
>     *   The guest operating system’s scheduler might migrate a single-threaded workload amongst multiple vCPUs, thereby losing cache locality
> *   Size your virtual machines so they align with physical NUMA boundaries. For example, if you have a host system with six cores per NUMA node, size your virtual machines with a multiple of six vCPUs (i.e., 6 vCPUs, 12 vCPUs, 18 vCPUs, 24 vCPUs, and so on).

From the same document:

> **UP vs. SMP HALs/Kernels**
> There are two types of hardware abstraction layers (HALs) and kernels: UP and SMP. UP historically stood for “uniprocessor,” but should now be read as “single-core.” SMP historically stood for “symmetric multi-processor,” but should now be read as multi-core. Although some recent operating systems (including Windows Vista, Windows Server 2008, and Windows 7) use the same HAL or kernel for both UP and SMP installations, many operating systems can be configured to use either a UP HAL/kernel or an SMP HAL/kernel. To obtain the best performance on a single-vCPU virtual machine running an operating system that offers both UP and SMP HALs/kernels, configure the operating system with a UP HAL or kernel.
>
> The UP operating system versions are for single-core machines. If used on a multi-core machine, a UP operating system version will recognize and use only one of the cores. The SMP versions, while required in order to fully utilize multi-core machines, can also be used on single-core machines. Due to their extra synchronization code, however, SMP operating system versions used on single-core machines are slightly slower than UP operating system versions used on the same machines.

Now for memory from the same document:

> **Memory Sizing**
> Carefully select the amount of memory you allocate to your virtual machines.
>
> *   You should allocate enough memory to hold the working set of applications you will run in the virtual machine, thus minimizing thrashing.
> *   You should also avoid over-allocating memory. Allocating more memory than needed unnecessarily increases the virtual machine memory overhead, thus consuming memory that could be used to support more virtual machines.
>
> **Large Memory Pages for Hypervisor and Guest Operating System**
> In addition to the usual 4KB memory pages, ESXi also provides 2MB memory pages (commonly referred to as “large pages”). By default ESXi assigns these 2MB machine memory pages to guest operating systems that request them, giving the guest operating system the full advantage of using large pages. The use of large pages results in reduced memory management overhead and can therefore increase hypervisor performance.
>
> If an operating system or application can benefit from large pages on a native system, that operating system or application can potentially achieve a similar performance improvement on a virtual machine backed with 2MB machine memory pages. Consult the documentation for your operating system and application to determine how to configure each of them to use large memory pages.
>
> Use of large pages can also change page sharing behavior. While ESXi ordinarily uses page sharing regardless of memory demands, it does not share large pages. Therefore with large pages, page sharing might not occur until memory overcommitment is high enough to require the large pages to be broken into small pages. For further information see VMware KB articles 1021095 and 1021896.

And lastly from [APAC BrownBag Session 12](https://professionalvmware.com/vmware-certifications/):

![super-size-vm](https://github.com/elatov/uploads/raw/master/2012/09/super-size-vm.png)

### Determine appropriate reservations, shares, and limits

From [this](https://github.com/elatov/uploads/raw/master/2013/04/vcap-dcd_notes.pdf) PDF:

> **Shares,Reservations, and Limits:**
>
> *   Deploy VMs with default setting unless clear reason to do otherwise
> *   Are there Apps that need resources even during contention? Then use Reservations
> *   This adds complexity and administration overhead and from

![reser-share-limits](https://github.com/elatov/uploads/raw/master/2012/09/reser-share-limits.png)

This was also discussed in [Objective 3.4](/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/)

### Based on an existing logical design, determine virtual hardware options

From "[Performance Best Practices for VMware vSphere 5.0](http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf)":

> Allocate to each virtual machine only as much virtual hardware as that virtual machine requires. Provisioning a virtual machine with more resources than it requires can, in some cases, reduce the performance of that virtual machine as well as other virtual machines sharing the same host.
>
> Unused or unnecessary virtual hardware devices can impact performance and should be disabled. For example, Windows guest operating systems poll optical drives (that is, CD or DVD drives) quite frequently. When virtual machines are configured to use a physical drive, and multiple guest operating systems simultaneously try to access that drive, performance could suffer. This can be reduced by configuring the virtual machines to use ISO images instead of physical drives, and can be avoided entirely by disabling optical drives in virtual machines when the devices are not needed. 
>
> ESXi 5.0 introduces virtual hardware version 8. By creating virtual machines using this hardware version, or upgrading existing virtual machines to this version, a number of additional capabilities become available. Some of these, such as support for virtual machines with up to 1TB of RAM and up to 32 vCPUs, support for virtual NUMA, and support for 3D graphics, can improve performance for some workloads.

From "[vSphere Virtual Machine Administration ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-703-virtual-machine-admin-guide.pdf)":

> **Virtual Machine Hardware**
> You can add or configure some virtual machine hardware, only if the virtual machine uses the latest available hardware version. The PCI and SIO virtual hardware devices are part of the virtual motherboard, but cannot be configured or removed.
>
> | CPU | IDE 0 | PCI Controller | SCSI Device | Chipset |
> |Keyboard| PCI Device| SIO Controller | DVD/CD ROM    | Memory  |
> | Pointing Device | USB Controller | Floppy Drive | Network Adapter | Serial Port |
> | USB Device| Hard Disk | Parallel Port | SCSI Controller | VMCI |

from [APAC BrownBag Session 12](https://professionalvmware.com/vmware-certifications/):

![vHw](https://github.com/elatov/uploads/raw/master/2012/09/vHw.png)

### Design a vApp catalog of appropriate VM offerings (e.g., templates, OVFs, vCO)

from ![self_provisioning](https://github.com/elatov/uploads/raw/master/2012/09/self_provisioning.png)

If you have a service with multiple dependecies, then create a vApp with appropriate VMs in it and set the appropriate boot order respectively of the dependencies. Next if this vApp will used across multiple Datacenters, export this vApp as an OVF and put it on a file share where people can download it from. Or even put it on your USB drive and deploy the vApp as necessary. You can even use export vApps during your upgrade process.

### Describe implications of and apply appropriate use cases for vApps

from [APAC BrownBag Session 12](https://professionalvmware.com/vmware-certifications/):

![vapps](https://github.com/elatov/uploads/raw/master/2012/09/vapps.png)

and

![vapp_use-cases](https://github.com/elatov/uploads/raw/master/2012/09/vapp_use-cases.png)

This was also discussed in [Objective 3.4](/2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/)

### Decide on the suitability of using FT or 3rd party clustering products based on application requirements.

From "[VMware Fault Tolerance](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/vmware-vsphere6-ft-arch-perf.pdf)":

> **How Does VMware Fault Tolerance Work?**
>
> *   VMware Fault Tolerance, when enabled for a virtual machine,creates a live shadow instance of the primary, running on another physical server.
> *   The two instances are kept in virtual lockstep with each other using VMware vLockstep technology, which logs non-deterministic event execution by the primary and transmits them over a Gigabit Ethernet network to be replayed by the secondary virtual machine.
> *   The two virtual machines play the exact same set of events, because they get the exact same set of inputs at any given time.
> *   The two virtual machines access a common disk and appear as a single entity, with a single IP address and a single MAC address to other applications. Only the primary is allowed to perform writes.
> *   The two virtual machines constantly heartbeat against each other and if either virtual machine instance loses the heartbeat, the other takes over immediately. The heartbeats are very frequent, with millisecond intervals, making the failover instantaneous with no loss of data or state.
> *   VMware Fault Tolerance requires a dedicated network connection, separate from the VMware VMotion™ network, between the two physical servers

From "[Performance Best Practices for VMware vSphere 5.0](http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf)":

> **VMware Fault Tolerance**
>
> *   The live migration that takes place when FT is enabled can briefly saturate the vMotion network link and can also cause spikes in CPU utilization.
>     *   If the vMotion network link is also being used for other operation, such as FT logging (transmission of all the primary virtual machine’s inputs (incoming network traffic, disk reads, etc.) to the secondary host), the performance of those other operations can be impacted. For this reason it is best to have separate and dedicated NICs (or use Network I/O Control, described in “Network I/O Control (NetIOC)” on page 34) for FT logging traffic and vMotion, especially when multiple FTvirtual machines reside on the same host.
>     *   Because this potentially resource-intensive live migration takes place each time FT is enabled, we recommend that FT not be frequently enabled and disabled.
>     *   FT-enabled virtual machines must use eager-zeroed thick-provisioned virtual disks. Thus when FT is enabled for a virtual machine with thin-provisioned virtual disks or lazy-zeroed thick-provisioned virtual disks these disks need to be converted. This one-time conversion process uses fewer resources when the virtual machine is on storage hardware that supports VAAI (described in “Hardware Storage Considerations” on page 11).
> *   Because FT logging traffic is asymmetric (the majority of the traffic flows from primary to secondary), congestion on the logging NIC can be reduced by distributing primaries onto multiple hosts. For example on a cluster with two ESXi hosts and two virtual machines with FT enabled, placing one of the primary virtual machines on each of the hosts allows the network bandwidth to be utilized bidirectionally.
> *   FT virtual machines that receive large amounts of network traffic or perform lots of disk reads can create significant bandwidth on the NIC specified for the logging traffic. This is true of machines that routinely do these things as well as machines doing them only intermittently, such as during a backup operation. To avoid saturating the network link used for logging traffic limit the number of FT virtual machines on each host or limit disk read bandwidth and network receive bandwidth of those virtual machines.
> *   Make sure the FT logging traffic is carried by at least a Gigabit-rated NIC (which should in turn be connected to at least Gigabit-rated network infrastructure)
> *   Avoid placing more than four FT-enabled virtual machines on a single host. In addition to reducing the possibility of saturating the network link used for logging traffic, this also limits the number of simultaneous live-migrations needed to create new secondary virtual machines in the event of a host failure.
> *   If the secondary virtual machine lags too far behind the primary (which usually happens when the primary virtual machine is CPU bound and the secondary virtual machine is not getting enough CPU cycles), the hypervisor might slow the primary to allow the secondary to catch up. The following recommendations help avoid this situation:
>     *   Make sure the hosts on which the primary and secondary virtual machines run are relatively closely matched, with similar CPU make, model, and frequency.
>     *   Make sure that power management scheme settings (both in the BIOS and in ESXi) that cause CPU frequency scaling are consistent between the hosts on which the primary and secondary virtual machines run.
>     *   Enable CPU reservations for the primary virtual machine (which will be duplicated for the secondary virtual machine) to ensure that the secondary gets CPU cycles when it requires them.

From [APAC BrownBag Session 12](https://professionalvmware.com/vmware-certifications/):

![vm-ft](https://github.com/elatov/uploads/raw/master/2012/09/vm-ft.png)

From "[Virtualizing Business-Critical Applications on VMware](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/whitepaper/solutions/vmware-virtualizing-business-critical-apps-on-vmware_en-white-paper.pdf)"

> The siloed example of availability methods shown in Figure 11 requires expensive licenses, dedicated standby infrastructure, and highly skilled staff to configure and manage. The alternative to this expensive approach is a standardized approach using vSphere technology, though some companies choose to implement both appspecific and VMware solutions running in tandem. ![3rd-party-availability_apps](https://github.com/elatov/uploads/raw/master/2012/09/3rd-party-availability_apps.png)

Also from "[Virtualizing Business-Critical Applications on VMware vSphere](https://www.vmware.com/solutions/business-critical-apps.html)":

![percent-of-coverage_for-availability](https://github.com/elatov/uploads/raw/master/2012/09/percent-of-coverage_for-availability.png)

Here are examples of each 3rd party clustering products:

*   [Oracle Databases on VMware High Availability](http://www.vmware.com/files/pdf/partners/oracle/Oracle_Databases_on_VMware_-_High_Availability_Guidelines.pdf)
*   [Microsoft SQL Server on VMware Best Practices Guide](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/solutions/sql-server-on-vmware-best-practices-guide.pdf)
*   [Microsoft Exchange 2013 on VMware Availability and Recovery Options](http://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/solutions/business-critical-apps/exchange/exchange-2013-on-vmware-availability-and-recovery-options.pdf)
*   [Setup for Failover Clustering and Microsoft Cluster Service ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-651-setup-mscs.pdf)

and from [APAC BrownBag Session 12](https://professionalvmware.com/vmware-certifications/):

![3rd_party-clusters](https://github.com/elatov/uploads/raw/master/2012/09/3rd_party-clusters.png)

So if you have a specific application like SQL, Oracle, or Exchange that cannot be limited to 1 vCPU(FT) or just 2 nodes (MSCS), then use application level clustering/availability described in the above papers. But if you have application that requires 100% uptime and it's low resource then VMware FT will be perfect for that.

### Determine and implement an anti-virus solution

![AV-for-VMs](https://github.com/elatov/uploads/raw/master/2012/09/AV-for-VMs.png)

So if you want a centralized Anti-Virus application, setup vShield End-Point. This does add on some complexity and management over head. If you end up setting up an Anti-Virus instance per VM try to schedule the AV Scans at different times. You can over load the system when all 100 of your VMs are doing an AV Scan at the same time. If you want more information on vShield check out "[Antivirus Practices for VMware View 5](http://www.vmware.com/techpapers/2013/antivirus-best-practices-for-horizon-view-5x-10258.html)". It talks about vShield End Point and some other best practices for VMware View. Here are some excerpts from that paper:

> **Problems with Standard Antivirus Protection**
> The typical top-down virus scanning model involves desktop antivirus scanning and signature file updates, with access to an auto-update server. During these operations, it is not uncommon for system resource usage to spike or become overly committed. Performance in the desktop environment is severely impacted by these “antivirus storms.”
>
> **The VMware Solution to Antivirus Protection**
> VMware vShield™ Endpoint is the solution to the problems inherent in antivirus scanning in a large-scale virtual desktop implementation. In a VMware View environment, vShield Endpoint consolidates and offloads two antivirus operations into one centralized virtual appliance:
>
> *   Checking for virus signature update files
> *   Antivirus scanning
>
> The vShield Endpoint product offers the following benefits for large-scale antivirus protection:
>
> *   Enables VMware partners to eliminate antivirus storms that affect performance of virtual machines in a virtual desktop environment. Signature file updates and antivirus scanning are isolated and offloaded to a virtual appliance.
> *   Improves consolidation ratios of virtual desktops by offloading antivirus functions to a separate security virtual machine. The enterprise antivirus engine and the signature file are located on the virtual appliance, instead of on each virtual machine. This frees up virtual desktop system resources.
> *   Agentless solution: Instead of an antivirus agent installed on each desktop to be protected, vShield Endpoint utilizes a small-footprint driver on each desktop. This driver is part of VMware Tools, and no additional provisioning is required. The antivirus scanner and virus signatures are installed only in the virtual appliance. This saves space on each desktop.

