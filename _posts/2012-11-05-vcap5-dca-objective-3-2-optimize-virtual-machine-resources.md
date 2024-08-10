---
title: VCAP5-DCA Objective 3.2 – Optimize Virtual Machine Resources
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-3-2-optimize-virtual-machine-resources/
dsq_thread_id:
  - 1412263375
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['performance']
---

### Compare and contrast virtual and physical hardware resources

From "[Transform your Business with Virtualization](https://raw.githubusercontent.com/elatov/upload/master/vcap-dca/3-2/transform-business-virtualization_white_paper.pdf)":

> **What is a Virtual Machine?**
> A virtual machine is a tightly isolated software container that can run its own operating systems and applications as if it were a physical computer. A virtual machine behaves exactly like a physical computer and contains it own virtual (ie, software-based) CPU, RAM hard disk and network interface card (NIC).
>
> An operating system can’t tell the difference between a virtual machine and a physical machine, nor can applications or other computers on a network. Even the virtual machine thinks it is a “real” computer. Nevertheless, a virtual machine is composed entirely of software and contains no hardware components whatsoever. As a result, virtual machines offer a number of distinct advantages over physical hardware.
>
> **Compatibility**
> Just like a physical computer, a virtual machine hosts its own guest operating system and applications, and has all the components found in a physical computer (motherboard, VGA card, network card controller, etc). As a result, virtual machines are completely compatible with all standard x86 operating systems, applications and device drivers, so you can use a virtual machine to run all the same software that you would run on a physical x86 computer.
>
> **Isolation**
> While virtual machines can share the physical resources of a single computer, they remain completely isolated from each other as if they were separate physical machines. If, for example, there are four virtual machines on a single physical server and one of the virtual machines crashes, the other three virtual machines remain available. Isolation is an important reason why the availability and security of applications running in a virtual environment is far superior to applications running in a traditional, non-virtualized system.
>
> **Encapsulation**
> A virtual machine is essentially a software container that bundles or “encapsulates” a complete set of virtual hardware resources, as well as an operating system and all its applications, inside a software package. Encapsulation makes virtual machines incredibly portable and easy to manage. For example, you can move and copy a virtual machine from one location to another just like any other software file, or save a virtual machine on any standard data storage medium, from a pocket-sized USB flash memory card to an enterprise storage area networks (SANs).
>
> **Hardware Independence**
> Virtual machines are completely independent from their underlying physical hardware. For example, you can configure a virtual machine with virtual components (eg, CPU, network card, SCSI controller) that are completely different from the physical components that are present on the underlying hardware. Virtual machines on the same physical server can even run different kinds of operating systems (Windows, Linux, etc).
>
> When coupled with the properties of encapsulation and compatibility, hardware independence gives you the freedom to move a virtual machine from one type of x86 computer to another without making any changes to the device drivers, operating system, or applications. Hardware independence also means that you can run a heterogeneous mixture of operating systems and applications on a single physical computer.

### Identify VMware memory management techniques

This was covered in Objective 3.1

### Identify VMware CPU load balancing techniques

From "[Performance Best Practices for VMware vSphere 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/Perf_Best_Practices_vSphere5.0.pdf)":

> **ESXi CPU Considerations**
> This subsection provides guidance regarding CPU considerations in VMware ESXi.
>
> CPU virtualization adds varying amounts of overhead depending on the percentage of the virtual machine’s workload that can be executed on the physical processor as is and the cost of virtualizing the remainder of the workload:
>
> *   For many workloads, CPU virtualization adds only a very small amount of overhead, resulting in performance essentially comparable to native.
> *   Many workloads to which CPU virtualization does add overhead are not CPU-bound—that is, most of their time is spent waiting for external events such as user interaction, device input, or data retrieval, rather than executing instructions. Because otherwise-unused CPU cycles are available to absorb the virtualization overhead, these workloads will typically have throughput similar to native, but potentially with a slight increase in latency.
> *   For a small percentage of workloads, for which CPU virtualization adds overhead and which are CPU-bound, there might be a noticeable degradation in both throughput and latency.
>
> The rest of this subsection lists practices and configurations recommended by VMware for optimal CPU performance.
>
> *   In most environments ESXi allows significant levels of CPU overcommitment (that is, running more vCPUs on a host than the total number of physical processor cores in that host) without impacting virtual machine performance.
> *   If an ESXi host becomes CPU saturated (that is, the virtual machines and other loads on the host demand all the CPU resources the host has), latency-sensitive workloads might not perform well. In this case you might want to reduce the CPU load, for example by powering off some virtual machines or migrating them to a different host (or allowing DRS to migrate them automatically).
> *   It is a good idea to periodically monitor the CPU usage of the host. This can be done through the vSphere Client or by using esxtop or resxtop. Below we describe how to interpret esxtop data:
> *   If the load average on the first line of the esxtop CPU panel is equal to or greater than 1, this indicates that the system is overloaded.
> *   The usage percentage for the physical CPUs on the PCPU line can be another indication of a possibly overloaded condition. In general, 80% usage is a reasonable ceiling and 90% should be a warning that the CPUs are approaching an overloaded condition. However organizations will have varying standards regarding the desired load percentage.
> *   Configuring a virtual machine with more virtual CPUs (vCPUs) than its workload can use might cause slightly increased resource usage, potentially impacting performance on very heavily loaded systems. Common examples of this include a single-threaded workload running in a multiple-vCPU virtual machine or a multi-threaded workload in a virtual machine with more vCPUs than the workload can effectively use.
> *   Even if the guest operating system doesn’t use some of its vCPUs, configuring virtual machines with those vCPUs still imposes some small resource requirements on ESXi that translate to real CPU consumption on the host. For example:
> *   Unused vCPUs still consume timer interrupts in some guest operating systems. (Though this is not true with “tickless timer” kernels, described in “Guest Operating System CPU Considerations” on page 39.)
> *   Maintaining a consistent memory view among multiple vCPUs can consume additional resources, both in the guest operating system and in ESXi. (Though hardware-assisted MMU virtualization significantly reduces this cost.)
> *   Most guest operating systems execute an idle loop during periods of inactivity. Within this loop, most of these guest operating systems halt by executing the HLT or MWAIT instructions. Some older guest operating systems (including Windows 2000 (with certain HALs), Solaris 8 and 9, and MS-DOS), however, use busy-waiting within their idle loops. This results in the consumption of resources that might otherwise be available for other uses (other virtual machines, the VMkernel, and so on).
> *   ESXi automatically detects these loops and de-schedules the idle vCPU. Though this reduces the CPU overhead, it can also reduce the performance of some I/O-heavy workloads. For additional information see VMware KB articles 1077 and 2231.
> *   The guest operating system’s scheduler might migrate a single-threaded workload amongst multiple vCPUs, thereby losing cache locality.
>
> These resource requirements translate to real CPU consumption on the host.

### Identify pre-requisites for Hot Add features

From the [vSphere Documenation](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-285BB774-CE69-4477-9011-598FEF1E9ACB.html):

> Prerequisites Verify that the virtual machine is running under the following conditions:
>
> *   VMware Tools is installed. This condition is required for hot plug functionality with Linux guest operating systems.
> *   The virtual machine has a guest operating system that supports CPU hot plug.
> *   The virtual machine is using hardware version 7 or later.
> *   The virtual machine is powered off.
> *   Required privileges: Virtual Machine.Configuration.Settings on the virtual machine

Also from the same page:

> Procedure
>
> 1.  In the vSphere Client inventory, right-click the virtual machine and select Edit Settings.
> 2.  Click the Options tab and under Advanced, select Memory/CPU Hotplug.
> 3.  Change the CPU Hot Plug setting.
> 4.  Click OK to save your changes and close the dialog box.

Similar settings for the hot-add of the memory. Here is how the option looks like in vCenter:

![cpu_memory_hot-add](https://github.com/elatov/uploads/raw/master/2012/10/cpu_memory_hot-add.png)

There are also a lot of OS'es that support it and that don't. From the blog "[VMware vSphere Hot Add and Hot Plug](http://www.petenetlive.com/KB/Article/0000527.htm)":

![hot-add_matrix](https://github.com/elatov/uploads/raw/master/2012/10/hot-add_matrix.png)

Also check out "[VMware Hot-Add Memory/CPU Support](https://www.petri.com/vsphere-hot-add-memory-and-cpu)"

### Tune Virtual Machine memory configurations

From "[Performance Best Practices for VMware vSphere 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dcd/Perf_Best_Practices_vSphere5.0.pdf)":

> **Memory Overhead**
>
> 1.   An additional memory space overhead for each virtual machine. The per-virtual-machine memory space overhead can be further divided into the following categories:
>     *    Memory reserved for the virtual machine executable (VMX) process.This is used for data structures needed to bootstrap and support the guest (i.e., thread stacks, text, and heap).
>     *    Memory reserved for the virtual machine monitor (VMM).This is used for data structures required by the virtual hardware (i.e., TLB, memory mappings, and CPU state).
>     *    Memory reserved for various virtual devices (i.e., mouse, keyboard, SVGA, USB, etc.)
>     *    Memory reserved for other subsystems, such as the kernel, management agents, etc.
> 2.  The amounts of memory reserved for these purposes depend on a variety of factors, including the number of vCPUs, the configured memory for the guest operating system, whether the guest operating system is 32-bit or 64-bit, and which features are enabled for the virtual machine

And more from the same document:

> **Memory Sizing**
> Carefully select the amount of memory you allocate to your virtual machines.
>
> *   You should allocate enough memory to hold the working set of applications you will run in the virtual machine, thus minimizing thrashing.
> *   You should also avoid over-allocating memory. Allocating more memory than needed unnecessarily increases the virtual machine memory overhead, thus consuming memory that could be used to support more virtual machines.

And some more information:

> **Large Memory Pages for Hypervisor and Guest Operating System**
> In addition to the usual 4KB memory pages, ESXi also provides 2MB memory pages (commonly referred to as “large pages”). By default ESXi assigns these 2MB machine memory pages to guest operating systems that request them, giving the guest operating system the full advantage of using large pages. The use of large pages results in reduced memory management overhead and can therefore increase hypervisor performance.
>
> If an operating system or application can benefit from large pages on a native system, that operating system or application can potentially achieve a similar performance improvement on a virtual machine backed with 2MB machine memory pages. Consult the documentation for your operating system and application to determine how to configure each of them to use large memory pages.
>
> Use of large pages can also change page sharing behavior. While ESXi ordinarily uses page sharing regardless of memory demands, it does not share large pages. Therefore with large pages, page sharing might not occur until memory overcommitment is high enough to require the large pages to be broken into small pages. For further information see VMware KB articles 1021095 and 1021896.

### Tune Virtual Machine networking configurations

From the [vSphere Documenation](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-285BB774-CE69-4477-9011-598FEF1E9ACB.html):

> **DirectPath I/O**
> In the case of networking, DirectPath I/O allows the virtual machine to access a physical NIC directly rather than using an emulated device (E1000) or a para-virtualized device (VMXNET, VMXNET3). While DirectPath I/O provides limited increases in throughput, it reduces CPU cost for networking-intensive workloads.
>
> DirectPath I/O is not compatible with certain core virtualization features, however. This list varies with the hardware on which ESXi is running:
>
> *   New for vSphere 5.0, when ESXi is running on certain configurations of the Cisco Unified Computing System (UCS) platform, DirectPath I/O for networking is compatible with vMotion, physical NIC sharing, snapshots, and suspend/resume. It is not compatible with Fault Tolerance, NetIOC, memory overcommit, VMCI, or VMSafe.
> *   For server hardware other than the Cisco UCS platform, DirectPath I/O is not compatible with vMotion, physical NIC sharing, snapshots, suspend/resume, Fault Tolerance, NetIOC, memory overcommit, or VMSafe.
>
> Typical virtual machines and their workloads don't require the use of DirectPath I/O. For workloads that are very networking intensive and don't need the core virtualization features mentioned above, however, DirectPath I/O might be useful to reduce CPU usage.

More from the same document:

> **SplitRx Mode**
> SplitRx mode, a new feature in ESXi 5.0, uses multiple physical CPUs to process network packets received in a single network queue. This feature can significantly improve network performance for certain workloads. These workloads include:
>
> *   Multiple virtual machines on one ESXi host all receiving multicast traffic from the same source.(SplitRx mode will typically improve throughput and CPU efficiency for these workloads.)
> *   Traffic via the vNetwork Appliance (DVFilter) API between two virtual machines on the same ESXi host.(SplitRx mode will typically improve throughput and maximum packet rates for these workloads.)
>
> This feature, which is supported only for VMXNET3 virtual network adapters, is individually configured for each virtual NIC using the ethernetX.emuRxMode variable in each virtual machine’s .vmx file (where X is replaced with the network adapter’s ID).
>
> **Running Network Latency Sensitive Applications**
>
> *   Use VMXNET3 virtual network adapters
> *   Set the ESXi host power policy to Maximum performance
> *   Disable C1E and other C-states in BIOS
> *   Enable Turbo Boost in BIOS
> *   Disable VMXNET3 virtual interrupt coalescing for the desired NIC
>
> In some cases this can improve performance for latency-sensitive applications. In other cases—most notably applications with high numbers of outstanding network requests—it can reduce performance. To do this through the vSphere Client:
>
> 1.  Select the virtual machine you wish to change, then click Edit virtual machine settings.
> 2.  Under the Options tab, select General, then click Configuration Parameters.
> 3.  Look for ethernetX.coalescingScheme (where X is the number of the desired NIC). If the variableisn’t present, click Add Row and enter it as a new variable.
> 4.  Click on the value to be changed and set it to disabled.
>
> The change will not take effect until the virtual machine has been restarted

And more information:

> **Guest Operating System Networking Considerations**
>
> *   For the best performance, use the VMXNET3 paravirtualized network adapter for operating systems in which it is supported. This requires that the virtual machine use The VMXNET3, Enhanced VMXNET, and E1000 devices support jumbo frames for better performance. (Note that the vlance device does not support jumbo frames.) To enable jumbo frames, set the MTU size to 9000 in both the guest network driver and the virtual switch configuration. The physical NICs at both ends and all the intermediate hops/routers/switches must also support jumbo frames.
> *   In ESXi, TCP Segmentation Offload (TSO) is enabled by default in the VMkernel, but is supported in virtual machines only when they are using the VMXNET3 device, the Enhanced VMXNET device, or the E1000 device. TSO can improve performance even if the underlying hardware does not support TSO.
> *   In some cases, low receive throughput in a virtual machine can be caused by insufficient receive buffers
> *   in the receiver network device. If the receive ring in the guest operating system’s network driver overflows, packets will be dropped in the VMkernel, degrading network throughput. A possible workaround is to increase the number of receive buffers, though this might increase the host physical CPU workload.
> *   Receive-side scaling (RSS) allows network packet receive processing to be scheduled in parallel on multiple CPUs. Without RSS, receive interrupts can be handled on only one CPU at a time. With RSS, received packets from a single NIC can be processed on multiple CPUs concurrently. This helps receive throughput in cases where a single CPU would otherwise be saturated with receive processing and become a bottleneck. To prevent out-of-order packet delivery, RSS schedules all of a flow’s packets to the same CPU.

### Tune Virtual Machine CPU configurations

From the [vSphere Documenation](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-285BB774-CE69-4477-9011-598FEF1E9ACB.html):

> **Guest Operating System CPU Considerations**
>
> *   In SMP virtual machines the guest operating system can migrate processes from one vCPU to another. This migration can incur a small CPU overhead. If the migration is very frequent it might be helpful to pin guest threads or processes to specific vCPUs. (Note that this is another reason not to configure virtual machines with more vCPUs than they need.)
> *   Many operating systems keep time by counting timer interrupts. The timer interrupt rates vary between different operating systems and versions. For example:
>     *    Unpatched 2.4 and earlier Linux kernels typically request timer interrupts at 100 Hz (that is, 100 interrupts per second), though this can vary with version and distribution.
>     *    2.6 Linux kernels have used a variety of timer interrupt rates, including 100 Hz, 250 Hz, and 1000 Hz, again varying with version and distribution.
>     *    The most recent 2.6 Linux kernels introduce the NO_HZ kernel configuration option (sometimes called “tickless timer”) that uses a variable timer interrupt rate.
>     *    Microsoft Windows operating system timer interrupt rates are specific to the version of Microsoft Windows and the Windows HAL that is installed. Windows systems typically use a base timer interrupt rate of 64 Hz or 100 Hz.
>     *    Running applications that make use of the Microsoft Windows multimedia timer functionality can increase the timer interrupt rate. For example, some multimedia applications or Java applications increase the timer interrupt rate to approximately 1000 Hz.
> *   Delivering many virtual timer interrupts negatively impacts virtual machine performance and increases host CPU consumption. If you have a choice, use guest operating systems that require fewer timer interrupts. For example:
>     *    If you have a UP virtual machine use a UP HAL/kernel.
>     *    In some Linux versions, such as RHEL 5.1 and later, the “divider=10” kernel boot parameter reduces the timer interrupt rate to one tenth its default rate
>
> **Virtual NUMA (vNUMA)**
> Virtual NUMA (vNUMA), a new feature in ESXi 5.0, exposes NUMA topology to the guest operating system, allowing NUMA-aware guest operating systems and applications to make the most efficient use of the underlying hardware’s NUMA architecture.
>
> Virtual NUMA, which requires virtual hardware version 8, can provide significant performance benefits, though the benefits depend heavily on the level of NUMA optimization in the guest operating system and applications.
>
> *   You can obtain the maximum performance benefits from vNUMA if your clusters are composed entirely of hosts with matching NUMA architecture.
> *   This is because the very first time a vNUMA-enabled virtual machine is powered on, its vNUMA topology is set based in part on the NUMA topology of the underlying physical host on which it is running. Once a virtual machine’s vNUMA topology is initialized it doesn’t change unless the number of vCPUs in that virtual machine is changed. This means that if a vNUMA virtual machine is moved to a host with a different NUMA topology, the virtual machine’s vNUMA topology might no longer be optimal for the underlying physical NUMA topology, potentially resulting in reduced performance.
> *    Size your virtual machines so they align with physical NUMA boundaries. For example, if you have a host system with six cores per NUMA node, size your virtual machines with a multiple of six vCPUs (i.e., 6 vCPUs, 12 vCPUs, 18 vCPUs, 24 vCPUs, and so on).
> *   By default, vNUMA is enabled only for virtual machines with more than eight vCPUs. This feature can be enabled for smaller virtual machines, however, by adding to the .vmx file the line:numa.vcpu.maxPerVirtualNode = X

### Tune Virtual Machine storage configurations From the

[vSphere Documenation](https://docs.vmware.com/en/VMware-vSphere/7.0/com.vmware.vsphere.vm_admin.doc/GUID-285BB774-CE69-4477-9011-598FEF1E9ACB.html):

> **Guest Operating System Storage Considerations**
>
> *   The default virtual storage adapter in ESXi 5.0 is either BusLogic Parallel, LSI Logic Parallel, or LSI Logic SAS, depending on the guest operating system and the virtual hardware version. However, ESXi also includes a paravirtualized SCSI storage adapter, PVSCSI (also called VMware Paravirtual). The PVSCSI adapter offers a significant reduction in CPU utilization as well as potentially increased throughput compared to the default virtual storage adapters, and is thus the best choice for environments with very I/O-intensive guest applications.
> *   If you choose to use the BusLogic Parallel virtual SCSI adapter, and are using a Windows guest operating system, you should use the custom BusLogic driver included in the VMware Tools package.
> *   The depth of the queue of outstanding commands in the guest operating system SCSI driver can significantly impact disk performance. A queue depth that is too small, for example, limits the disk bandwidth that can be pushed through the virtual machine. See the driver-specific documentation for more information on how to adjust these settings.
> *   In some cases large I/O requests issued by applications in a virtual machine can be split by the guest storage driver. Changing the guest operating system’s registry settings to issue larger block sizes can eliminate this splitting, thus enhancing performance. For additional information see VMware KB article 9645697.
> *   Make sure the disk partitions within the guest are aligned. For further information you might want to refer to the literature from the operating system vendor regarding appropriate tools to use as well as recommendations from the array vendor.

### Calculate available resources

Under "Hosts and Cluster" View you can select the Cluster and then select the "Hosts" Tab. The tab looks like this:

![cluster_resources](https://github.com/elatov/uploads/raw/master/2012/10/cluster_resources.png)

Also under the Summary Tab you can select "View Resource Distribution Chart", here is that option in vCenter:

![cluster_view_distribution_chart](https://github.com/elatov/uploads/raw/master/2012/10/cluster_view_distribution_chart.png)

It will show you a similar output of the CPU and Memory usage. You can also check out esxtop on the host. More on esxtop in later objectives.

### Properly size a Virtual Machine based on application workload

I actually covered this in [DCD Objective 3.5](/2012/09/vcap5-dcd-objective-3-5-determine-virtual-machine-configuration-for-a-vsphere-5-physical-design/).

### Modify large memory page settings

From the [vSphere Documenation](https://docs.vmware.com/en/VMware-vSphere/8.0/vsphere-resource-management/GUID-D98E6EC9-3730-4BC0-A9FC-93B9079E1AEE.html):

> **Advanced Memory Attributes**
> You can use the advanced memory attributes to customize memory resource usage. ![Large_Page_Options](https://github.com/elatov/uploads/raw/master/2012/10/Large_Page_Options.png)

and here are some more options:

![more_lp_options](https://github.com/elatov/uploads/raw/master/2012/10/more_lp_options.png)

All of the above options can be modified by going to the "Host and Clusters" View -> Select a Host -> Click the "Configuration" Tab -> Select "Advanced Setting" under the Software Section. Here is how it looks like in vCenter:

![large_page_settings_on_host](https://github.com/elatov/uploads/raw/master/2012/10/large_page_settings_on_host.png)

### Understand appropriate use cases for CPU affinity

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Using CPU Affinity**
> By specifying a CPU affinity setting for each virtual machine, you can restrict the assignment of virtual machines to a subset of the available processors in multiprocessor systems. By using this feature, you can assign each virtual machine to processors in the specified affinity set.
>
> CPU affinity specifies virtual machine-to-processor placement constraints and is different from the relationship created by a VM-VM or VM-Host affinity rule, which specifies virtual machine-to-virtual machine host placement constraints.
>
> In this context, the term CPU refers to a logical processor on a hyperthreaded system and refers to a core on a non-hyperthreaded system.
>
> The CPU affinity setting for a virtual machine applies to all of the virtual CPUs associated with the virtual machine and to all other threads (also known as worlds) associated with the virtual machine. Such virtual machine threads perform processing required for emulating mouse, keyboard, screen, CD-ROM, and miscellaneous legacy devices.
>
> In some cases, such as display-intensive workloads, significant communication might occur between the virtual CPUs and these other virtual machine threads. Performance might degrade if the virtual machine's affinity setting prevents these additional threads from being scheduled concurrently with the virtual machine's virtual CPUs. Examples of this include a uniprocessor virtual machine with affinity to a single CPU or a two-way SMP virtual machine with affinity to only two CPUs.
>
> For the best performance, when you use manual affinity settings, VMware recommends that you include at least one additional physical CPU in the affinity setting to allow at least one of the virtual machine's threads to be scheduled at the same time as its virtual CPUs. Examples of this include a uniprocessor virtual machine with affinity to at least two CPUs or a two-way SMP virtual machine with affinity to at least three CPUs.

Here is how to set it up:

> **Assign a Virtual Machine to a Specific Processor**
>
> 1.  In the vSphere Client inventory panel, select a virtual machine and select Edit Settings.
> 2.  Select the Resources tab and select Advanced CPU.
> 3.  Click the Run on processor(s) button.
> 4.  Select the processors where you want the virtual machine to run and click OK.

And here is one section from the same document:

> **Potential Issues with CPU Affinity**
> Before you use CPU affinity, you might need to consider certain issues. Potential issues with CPU affinity include:
>
> *   For multiprocessor systems, ESXi systems perform automatic load balancing. Avoid manual specification of virtual machine affinity to improve the scheduler’s ability to balance load across processors.
> *   Affinity can interfere with the ESXi host’s ability to meet the reservation and shares specified for a virtual machine.
> *   Because CPU admission control does not consider affinity, a virtual machine with manual affinity settings might not always receive its full reservation. Virtual machines that do not have manual affinity settings are not adversely affected by virtual machines with manual affinity settings.
> *   When you move a virtual machine from one host to another, affinity might no longer apply because the new host might have a different number of processors.
> *   The NUMA scheduler might not be able to manage a virtual machine that is already assigned to certain processors using affinity.
> *   Affinity can affect the host's ability to schedule virtual machines on multicore or hyperthreaded processors to take full advantage of resources shared on such processors.

### Configure alternate virtual machine swap locations

From "[vSphere Resource Management ESXi 5.0](https://storage.googleapis.com/grand-drive-196322.appspot.com/blog_pics/vcap5-dca/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf)":

> **Swap File Location**
> By default, the swap file is created in the same location as the virtual machine's configuration file.
>
> A swap file is created by the ESXi host when a virtual machine is powered on. If this file cannot be created, the virtual machine cannot power on. Instead of accepting the default, you can also:
>
> *   Use per-virtual machine configuration options to change the datastore to another shared storage location.
> *   Use host-local swap, which allows you to specify a datastore stored locally on the host. This allows you to swap at a per-host level, saving space on the SAN. However, it can lead to a slight degradation in performance for vSphere vMotion because pages swapped to a local swap file on the source host must be transferred across the network to the destination host.

From the same document:

> **Enable Host-Local Swap for a DRS Cluster**
> Host-local swap allows you to specify a datastore stored locally on the host as the swap file location. You can enable host-local swap for a DRS cluster.
>
> **Procedure**
>
> 1.  In the vSphere Client, right-click the cluster in the inventory and select Edit Settings.
> 2.  In the left pane of the cluster Settings dialog box, click Swapfile Location.
> 3.  Select the Store the swapfile in the datastore specified by the host option and click OK.
> 4.  In the vSphere Client inventory, select one of the hosts in the cluster and click the Configuration tab.
> 5.  Under Software, select Virtual Machine Swapfile Location.
> 6.  Select the local datastore to use and click OK.
> 7.  Repeat Step 4 through Step 6 for each host in the cluster.
>
> Host-local swap is now enabled for the DRS cluster.

Here is how the setup looks in the vCenter:

![cluster_swap_settings](https://github.com/elatov/uploads/raw/master/2012/10/cluster_swap_settings.png)

Also from the same document:

> **Enable Host-Local Swap for a Standalone Host**
> Host-local swap allows you to specify a datastore stored locally on the host as the swap file location. You can enable host-local swap for a standalone host.
>
> **Procedure**
>
> 1.  In the vSphere Client, select the host in the inventory.
> 2.  Click the Configuration tab.
> 3.  Under Software, select Virtual Machine Swapfile Location.
> 4.  Select Store the swapfile in the swapfile datastore.
> 5.  Select a local datastore from the list and click OK.
>
> Host-local swap is now enabled for the standalone host. Here is how it looks like in vCenter:

![host_swap_settings](https://github.com/elatov/uploads/raw/master/2012/10/host_swap_settings.png)

For the VM it self, you can go "Edit Settings" of the VM and then go to "Options" and then select "Swapfile Location". Here is how it looks like in vCenter:

![vm_swap_setting](https://github.com/elatov/uploads/raw/master/2012/10/vm_swap_setting.png)

