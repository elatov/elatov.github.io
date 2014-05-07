---
title: VCAP5-DCA Objective 3.1 – Tune and Optimize vSphere Performance
author: Karim Elatov
layout: post
permalink: /2012/11/vcap5-dca-objective-3-1-tune-and-optimize-vsphere-performance/
dsq_thread_id:
  - 1409019313
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify appropriate BIOS and firmware setting requirements for optimal ESXi host performance

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **General BIOS Settings**
> 
> *   Make sure you are running the latest version of the BIOS available for your system.
> *   Make sure the BIOS is set to enable all populated processor sockets and to enable all cores in each socket.
> *   Enable “Turbo Boost” in the BIOS if your processors support it.
> *   Make sure hyper-threading is enabled in the BIOS for processors that support it.
> *   Some NUMA-capable systems provide an option in the BIOS to disable NUMA by enabling node interleaving. In most cases you will get the best performance by disabling node interleaving (in other words, leaving NUMA enabled).
> *   Make sure any hardware-assisted virtualization features (VT-x, AMD-V, EPT, RVI, and so on) are enabled in the BIOS.
> *   Disable from within the BIOS any devices you won’t be using. This might include, for example, unneeded serial, USB, or network ports. See “ESXi General Considerations” on page 17 for further details.
> *   Cache prefetching mechanisms (sometimes called DPL Prefetch, Hardware Prefetcher, L2 Streaming Prefetch, or Adjacent Cache Line Prefetch) usually help performance, especially when memory access patterns are regular. When running applications that access memory randomly, however, disabling these mechanisms might result in improved performance.
> *   If the BIOS allows the memory scrubbing rate to be configured, we recommend leaving it at the manufacturer’s default setting.

From &#8220;<a href="http://www.vmware.com/files/pdf/hpm-perf-vsphere5.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/hpm-perf-vsphere5.pdf']);">Host Power Management in VMware vSphere 5</a>&#8220;:

> **Power Management BIOS Settings**  
> VMware ESXi™ includes a full range of host power management capabilities in the software. These can save power when an ESXi host is not fully utilized. You should configure your BIOS settings to allow ESXi the most flexibility in using the power management features offered by your hardware and then make your power management choices within ESXi. The following are a few important points to keep in mind:
> 
> *   Some systems have Processor Clocking Control (PCC) technology, which enables ESXi 5.0 to manage power on the host system indirectly, in cooperation with the BIOS. This setting is usually located under the Advanced Power Management options in the BIOS of supported HP systems and is usually called Collaborative Power Control. It is enabled by default. With this technology, ESXi does not manage P-states directly. It instead cooperates with the BIOS to determine the processor clock rate.
> *   Alternatively, by setting power management in the BIOS to OS control mode or the equivalent, you can enable ESXi to control CPU power-saving features directly. For example, on an HP ProLiant DL785 G6 AMD system, go to System OptionsPower Regulator for ProLiant and then select OS Control Mode. On a Dell PowerEdge R710 Intel system, go to the Power Management option and set the Power Management suboption to OS Control. Even if you don’t intend to use these power-saving features, ESXi provides a convenient way to manage them.
> *   C1E is a hardware-managed state: ESXi puts the CPU into the C1 state. The CPU hardware can determine, based on its own criteria, to deepen the state to C1E. Availability of the C1E halt state typically provides a reduction in power consumption, with little or no impact on performance. When Turbo Boost is enabled, the availability of C1E can sometimes even increase the performance of certain single-threaded workloads. Therefore, you should enable C1E in the BIOS. However, for a very few multithreaded workloads that are highly sensitive to I/O latency, C1E can reduce performance. In these cases, you might obtain better performance by disabling C1E in the BIOS, if that option is available.
> *   C-states deeper than C1/C1E (that is, C3 and C6) are managed by software and enable further power savings, but with an increased chance of performance impact. However, you should enable all C-states in the BIOS and then use vSphere host power management to control their use.

### Identify appropriate driver revisions required for optimal ESXi host performance

Check out the VMware <a href="http://vmware.com/go/hcl" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://vmware.com/go/hcl']);">HCL</a> and(or) VMware KB <a href="http://kb.vmware.com/kb/2030818" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2030818']);">2030818</a> for recommended drivers and firmware for different vSphere versions.

### Tune ESXi host memory configuration

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **Memory Overcommit Techniques**
> 
> *    ESXi uses five memory management mechanisms—page sharing, ballooning, memory compression, swap to host cache, and regular swapping—to dynamically reduce the amount of machine physical memory required for each virtual machine. 
>     *   Page Sharing: ESXi uses a proprietary technique to transparently and securely share memory pages between virtual machines, thus eliminating redundant copies of memory pages. In most cases, page sharing is used by default regardless of the memory demands on the host system. (The exception is when using large pages, as discussed in “Large Memory Pages for Hypervisor and Guest Operating System” on page 28.)
>     *   Ballooning: If the virtual machine’s memory usage approaches its memory target, ESXi will use ballooning to reduce that virtual machine’s memory demands. Using a VMware-supplied vmmemctl module installed in the guest operating system as part of VMware Tools suite, ESXi can cause the guest operating system to relinquish the memory pages it considers least valuable. Ballooning provides performance closely matching that of a native system under similar memory constraints. To use ballooning, the guest operating system must be configured with sufficient swap space.
>     *    Memory Compression: If the virtual machine’s memory usage approaches the level at which host-level swapping will be required, ESXi will use memory compression to reduce the number of memory pages it will need to swap out. Because the decompression latency is much smaller than the swap-in latency, compressing memory pages has significantly less impact on performance than swapping out those pages.
>     *    Swap to Host Cache: If memory compression doesn’t keep the virtual machine’s memory usage low enough, ESXi will next forcibly reclaim memory using host-level swapping to a host cache (if one has been configured). Swap to host cache is a new feature in ESXi 5.0 that allows users to configure a special swap cache on SSD storage. In most cases this host cache (being on SSD) will be much faster than the regular swap files (typically on hard disk storage), significantly reducing access latency. Thus, although some of the pages ESXi swaps out might be active, swap to host cache has a far lower performance impact than regular host-level swapping.
>     *    Regular Swapping: If the host cache becomes full, or if a host cache has not been configured, ESXi will next reclaim memory from the virtual machine by swapping out pages to a regular swap file. Like swap to host cache, some of the pages ESXi swaps out might be active. Unlike swap to host cache, however, this mechanism can cause virtual machine performance to degrade significantly due to its high access latency.
> *   While ESXi uses page sharing, ballooning, memory compression, and swap to host cache to allow significant memory overcommitment, usually with little or no impact on performance, you should avoid overcommitting memory to the point that active memory pages are swapped out with regular host-level swapping.
> *   If you suspect that memory overcommitment is beginning to affect the performance of a virtual machine you can: 
>     1.  In the vSphere Client, select the virtual machine in question, select the Performance tab, then look at the value of Memory Balloon (Average). An absence of ballooning suggests that ESXi is not under heavy memory pressure and thus memory overcommitment is not affecting the performance of that virtual machine.
>     2.  In the vSphere Client, select the virtual machine in question, select the Performance tab, then compare the values of Consumed Memory and Active Memory. If consumed is higher than active, this suggests that the guest is currently getting all the memory it requires for best performance.
>     3.  In the vSphere Client, select the virtual machine in question, select the Performance tab, then look at the values of Swap-In and Decompress. Swapping in and decompressing at the host level indicate more significant memory pressure.
>     4.  Check for guest operating system swap activity within that virtual machine.This can indicate that ballooning might be starting to impact performance, though swap activity can also be related to other issues entirely within the guest (or can be an indication that the guest memory size is simply too small).

And more from the same paper:

> **Memory Swapping Optimizations**  
> As described in “Memory Overcommit Techniques,” above, ESXi supports a bounded amount of memory overcommitment without host-level swapping. If the overcommitment is large enough that the other memory reclamation techniques are not sufficient, however, ESXi uses host-level memory swapping, with a potentially significant effect on virtual machine performance. (Note that this swapping is distinct from the swapping that can occur within the virtual machine under the control of the guest operating system.)
> 
> This subsection describes ways to avoid or reduce host-level swapping, and presents techniques to reduce its impact on performance when it is unavoidable.
> 
> *    Because ESXi uses page sharing, ballooning, and memory compression to reduce the need for host-level memory swapping, don’t disable these techniques.
> *    If you choose to overcommit memory with ESXi, be sure you have sufficient swap space on your ESXi system. At the time a virtual machine is first powered on, ESXi creates a swap file for that virtual machine equal in size to the difference between the virtual machine&#8217;s configured memory size and its memory reservation. The available disk space must therefore be at least this large (plus the space required for VMX swap).
> *    You can optionally configure a special host cache on an SSD (if one is installed) to be used for the new swap to host cache feature. This swap cache will be shared by all the virtual machines running on the host, and host-level swapping of their most active pages will benefit from the low latency of SSD. This allows a relatively small amount of SSD storage to have a potentially significant performance impact
> *    Even if an overcommitted host uses swap to host cache, it still needs to create regular swap files. Swap to host cache, however, makes much less important the speed of the storage on which the regular swap files are placed.
> *   If a host does not use swap to host cache, and memory is overcommitted to the point of thrashing, placing the virtual machine swap files on low latency, high bandwidth storage systems will result in the smallest performance impact from swapping. 
>     *    The best choice will usually be local SSD.
>     *    If the host doesn’t have local SSD, the second choice would be remote SSD. This would still provide the low-latencies of SSD, though with the added latency of remote access.
>     *    If you can’t use SSD storage, place the regular swap file on the fastest available storage. This might be a Fibre Channel SAN array or a fast local disk.
>     *    Placing swap files on local storage (whether SSD or hard drive) could potentially reduce vMotion performance. This is because if a virtual machine has memory pages in a local swap file, they must be swapped in to memory before a vMotion operation on that virtual machine can proceed.
>     *    Regardless of the storage type or location used for the regular swap file, for the best performance, and to avoid the possibility of running out of space, swap files should not be placed on thin-provisioned storage.
> *   The regular swap file location for a specific virtual machine can be set in the vSphere Client (select Edit virtual machine settings, choose the Options tab, and under Advanced select Swapfile location). If this option is not set, the swap file will be created in the virtual machine’s working directory: either the directory specified by workingDir in the virtual machine’s .vmx file, or, if this variable is not set, in the directory where the .vmx file is located. The latter is the default behavior.
> *    Host-level memory swapping can be avoided for a specific virtual machine by using the vSphere Client to reserve memory for that virtual machine at least equal in size to the machine’s active working set. Be aware, however, that configuring resource reservations will reduce the number of virtual machines that can be run on a system. This is because ESXi will keep available enough host memory to fulfill all reservations and won&#8217;t power-on a virtual machine if doing so would reduce the available memory to less than the reserved amount

### Tune ESXi host networking configuration

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **Hardware Networking Considerations**
> 
> *   Before undertaking any network optimization effort, you should understand the physical aspects of the network. The following are just a few aspects of the physical layout that merit close consideration: 
>     *   Consider using server-class network interface cards (NICs) for the best performance.
>     *   Make sure the network infrastructure between the source and destination NICs doesn’t introduce bottlenecks. For example, if both NICs are 10 Gigabit, make sure all cables and switches are capable of the same speed and that the switches are not configured to a lower speed.
> *   For the best networking performance, we recommend the use of network adapters that support the following hardware features: 
>     *   Checksum offload
>     *   TCP segmentation offload (TSO)
>     *   Ability to handle high-memory DMA (that is, 64-bit DMA addresses)
>     *   Ability to handle multiple Scatter Gather elements per Tx frame
>     *   Jumbo frames (JF)
>     *   Large receive offload (LRO)
> *   On some 10 Gigabit Ethernet hardware network adapters, ESXi supports NetQueue, a technology that significantly improves performance of 10 Gigabit Ethernet network adapters in virtualized environments.
> *   In addition to the PCI and PCI-X bus architectures, we now have the PCI Express (PCIe) architecture. Ideally single-port 10 Gigabit Ethernet network adapters should use PCIe x8 (or higher) or PCI-X 266 and dual-port 10 Gigabit Ethernet network adapters should use PCIe x16 (or higher). There should preferably be no “bridge chip” (e.g., PCI-X to PCIe or PCIe to PCI-X) in the path to the actual Ethernet device (including any embedded bridge chip on the device itself), as these chips can reduce performance.
> *   Multiple physical network adapters between a single virtual switch (vSwitch) and the physical network constitute a NIC team. NIC teams can provide passive failover in the event of hardware failure or network outage and, in some configurations, can increase performance by distributing the traffic across those physical network adapters.

### Tune ESXi host CPU configuration

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **General CPU Considerations**
> 
> *    When selecting hardware, it is a good idea to consider CPU compatibility for VMware vMotion™ (which in turn affects DRS) and VMware Fault Tolerance.
> 
> ** Hardware-Assisted Virtualization**  
> Most recent processors from both Intel and AMD include hardware features to assist virtualization. These features were released in two generations:
> 
> *    the first generation introduced CPU virtualization;
> *    the second generation added memory management unit (MMU) virtualization;
> 
> For the best performance, make sure your system uses processors with second-generation hardware-assist features.
> 
> **Hardware-Assisted CPU Virtualization (VT-x and AMD-V)**  
> The first generation of hardware virtualization assistance, VT-x from Intel and AMD-V from AMD, became available in 2006. These technologies automatically trap sensitive events and instructions, eliminating the overhead required to do so in software. This allows the use of a hardware virtualization (HV) virtual machine monitor (VMM) as opposed to a binary translation (BT) VMM. While HV outperforms BT for the vast majority of workloads, there are a few workloads where the reverse is true.
> 
> **Hardware-Assisted MMU Virtualization (Intel EPT and AMD RVI)**  
> More recent processors also include second-generation hardware virtualization assistance that addresses the overheads due to memory management unit (MMU) virtualization by providing hardware support to virtualize the MMU. ESXi supports this feature both in AMD processors, where it is called rapid virtualization indexing (RVI) or nested page tables (NPT), and in Intel processors, where it is called extended page tables (EPT).
> 
> Without hardware-assisted MMU virtualization, the guest operating system maintains guest virtual memory to guest physical memory address mappings in guest page tables, while ESXi maintains “shadow page tables” that directly map guest virtual memory to host physical memory addresses. These shadow page tables are maintained for use by the processor and are kept consistent with the guest page tables. This allows ordinary memory references to execute without additional overhead, since the hardware translation lookaside buffer (TLB) will cache direct guest virtual memory to host physical memory address translations read from the  
> shadow page tables. However, extra work is required to maintain the shadow page tables.
> 
> Hardware-assisted MMU virtualization allows an additional level of page tables that map guest physical memory to host physical memory addresses, eliminating the need for ESXi to maintain shadow page tables. This reduces memory consumption and speeds up workloads that cause guest operating systems to frequently modify page tables. While hardware-assisted MMU virtualization improves the performance of the vast majority of workloads, it does increase the time required to service a TLB miss, thus potentially reducing the performance of workloads that stress the TLB.
> 
> **Hardware-Assisted I/O MMU Virtualization (VT-d and AMD-Vi)**  
> An even newer processor feature is an I/O memory management unit that remaps I/O DMA transfers and device interrupts. This can allow virtual machines to have direct access to hardware I/O devices, such as network cards, storage controllers (HBAs) and GPUs. In AMD processors this feature is called AMD I/O Virtualization (AMD-Vi or IOMMU) and in Intel processors the feature is called Intel Virtualization Technology for Directed I/O (VT-d).

### Tune ESXi host storage configuration

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **Hardware Storage Considerations**  
> Back-end storage configuration can greatly affect performance.
> 
> Lower than expected storage performance is most often the result of configuration issues with underlying storage devices rather than anything specific to ESXi.
> 
> Storage performance is a vast topic that depends on workload, hardware, vendor, RAID level, cache size, stripe size, and so on. Consult the appropriate documentation from VMware as well as the storage vendor.
> 
> Many workloads are very sensitive to the latency of I/O operations. It is therefore important to have storage devices configured correctly. The remainder of this section lists practices and configurations recommended by VMware for optimal storage performance.
> 
> *   VMware Storage vMotion performance is heavily dependent on the available storage infrastructure bandwidth.
> *   Consider choosing storage hardware that supports VMware vStorage APIs for Array Integration (VAAI). VAAI can improve storage scalability by offloading some operations to the storage hardware instead of performing them in ESXi.
> *   On SANs, VAAI offers the following features: 
>     *   Hardware-accelerated cloning (sometimes called “full copy” or “copy offload”) frees resources on the host and can speed up workloads that rely on cloning, such as Storage vMotion.
>     *   Block zeroing speeds up creation of eager-zeroed thick disks and can improve first-time write performance on lazy-zeroed thick disks and on thin disks.
>     *   Scalable lock management (sometimes called “atomic test and set,” or ATS) can reduce locking-related overheads, speeding up thin-disk expansion as well as many other administrative and file system-intensive tasks. This helps improve the scalability of very large deployments by speeding up provisioning operations like boot storms, expansion of thin disks, snapshots, and other tasks.
>     *   Thin provision UNMAP allows ESXi to return no-longer-needed thin-provisioned disk space to the storage hardware for reuse.
> *   On NAS devices, VAAI offers the following features: 
>     *   Hardware-accelerated cloning (sometimes called “full copy” or “copy offload”) frees resources on the host and can speed up workloads that rely on cloning. (Note that Storage vMotion does not make use of this feature on NAS devices.)
>     *   Space reservation allows ESXi to fully preallocate space for a virtual disk at the time the virtual disk is created. Thus, in addition to the thin provisioning and eager-zeroed thick provisioning options that non-VAAI NAS devices support, VAAI NAS devices also support lazy-zeroed thick provisioning.
> *   Though the degree of improvement is dependent on the storage hardware, VAAI can reduce storage latency for several types of storage operations, can reduce the ESXi host CPU utilization for storage operations, and can reduce storage network traffic.
> *   Performance design for a storage network must take into account the physical constraints of the network, not logical allocations. Using VLANs or VPNs does not provide a suitable solution to the problem of link oversubscription in shared configurations. VLANs and other virtual partitioning of a network provide a way of logically configuring a network, but don&#8217;t change the physical capabilities of links and trunks between switches.
> *   If you have heavy disk I/O loads, you might need to assign separate storage processors (SPs) to separate systems to handle the amount of traffic bound for storage.
> *   To optimize storage array performance, spread I/O loads over the available paths to the storage (that is, across multiple host bus adapters (HBAs) and storage processors).
> *   Make sure that end-to-end Fibre Channel speeds are consistent to help avoid performance problems. For more information, see KB article 1006602.
> *   Configure maximum queue depth for Fibre Channel HBA cards. For additional information see VMware KB article 1267.
> *   Applications or systems that write large amounts of data to storage, such as data acquisition or transaction logging systems, should not share Ethernet links to a storage device with other applications or systems. These types of applications perform best with dedicated connections to storage devices.
> *   For iSCSI and NFS, make sure that your network topology does not contain Ethernet bottlenecks, where multiple links are routed through fewer links, potentially resulting in oversubscription and dropped network packets. Any time a number of links transmitting near capacity are switched to a smaller number of links, such oversubscription is a possibility.Recovering from these dropped network packets results in large performance degradation. In addition to time spent determining that data was dropped, the retransmission uses network bandwidth that could otherwise be used for new transactions.
> *   For iSCSI and NFS, if the network switch deployed for the data path supports VLAN, it might be beneficial to create a VLAN just for the ESXi host&#8217;s vmknic and the iSCSI/NFS server. This minimizes network interference from other packet sources.
> *   Be aware that with software-initiated iSCSI and NFS the network protocol processing takes place on the host system, and thus these might require more CPU resources than other storage options.
> *   Local storage performance might be improved with write-back cache. If your local storage has write-back cache installed, make sure it’s enabled and contains a functional battery module. For more information, see KB article 1006602.

### Configure and apply advanced ESXi host attributes

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf']);">vSphere Resource Management ESXi 5.0</a>&#8220;:

> **Set Advanced Host Attributes**
> 
> 1.  In the vSphere Client, select the host in the inventory.
> 2.  Click the Configuration tab.
> 3.  Under Software, click Advanced Settings.
> 4.  In the Advanced Settings dialog box, select the appropriate item (for example, CPU or Mem).
> 5.  Locate the attribute in the right panel and edit the value.
> 6.  Click OK.

Here is how it looks in the vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/host_advanced_settings.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/host_advanced_settings.png']);"><img class="alignnone size-full wp-image-4581" title="host_advanced_settings" src="http://virtuallyhyper.com/wp-content/uploads/2012/10/host_advanced_settings.png" alt="host advanced settings VCAP5 DCA Objective 3.1 – Tune and Optimize vSphere Performance " width="721" height="596" /></a>

### Configure and apply advanced Virtual Machine attributes

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf']);">vSphere Resource Management ESXi 5.0</a>&#8220;:

> **Set Advanced Virtual Machine Attributes**
> 
> 1.  In the vSphere Client, right-click the virtual machine in the inventory and select Edit Settings.
> 2.  Click Options and click Advanced > General.
> 3.  Click Configuration Parameters.
> 4.  In the dialog box that appears, click Add Row to enter a new parameter and its value.
> 5.  Click OK.

Here is how it looks like in vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/advanced_settings_VM.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/advanced_settings_VM.png']);"><img class="alignnone size-full wp-image-4582" title="advanced_settings_VM" src="http://virtuallyhyper.com/wp-content/uploads/2012/10/advanced_settings_VM.png" alt="advanced settings VM VCAP5 DCA Objective 3.1 – Tune and Optimize vSphere Performance " width="694" height="617" /></a>

### Configure advanced cluster attributes

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>&#8220;:

> **Set Advanced vSphere HA Options**
> 
> 1.  In the cluster’s Settings dialog box, select vSphere HA.
> 2.  Click the Advanced Options button to open the Advanced Options (HA) dialog box.
> 3.  Enter each advanced attribute you want to change in a text box in the Option column and enter a value in the Valuecolumn.
> 4.  Click OK

Here is how it looks like from vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/advanced_settings_HA.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/advanced_settings_HA.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/10/advanced_settings_HA.png" alt="advanced settings HA VCAP5 DCA Objective 3.1 – Tune and Optimize vSphere Performance " title="advanced_settings_HA" width="708" height="586" class="alignnone size-full wp-image-4584" /></a>

In the same Cluster Settings Window you can edit DRS options as well. Here is how it looks like from vCenter:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/10/DRS_Advanced_options.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/10/DRS_Advanced_options.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/10/DRS_Advanced_options.png" alt="DRS Advanced options VCAP5 DCA Objective 3.1 – Tune and Optimize vSphere Performance " title="DRS_Advanced_options" width="708" height="582" class="alignnone size-full wp-image-4585" /></a>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/11/vcap5-dca-objective-3-1-tune-and-optimize-vsphere-performance/" title=" VCAP5-DCA Objective 3.1 – Tune and Optimize vSphere Performance" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:VCAP5-DCA,blog;button:compact;">Identify appropriate BIOS and firmware setting requirements for optimal ESXi host performance From &#8220;Performance Best Practices for VMware vSphere 5.0&#8220;: General BIOS Settings Make sure you are running the latest...</a>
</p>