---
title: VCAP5-DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design
author: Karim Elatov
layout: post
permalink: /2012/09/vcap5-dcd-objective-3-4-determine-appropriate-compute-resources-for-a-vsphere-5-physical-design/
dsq_thread_id:
  - 1410463732
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Describe best practices with respect to CPU family choices

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **Hardware CPU Considerations**
> 
> **General CPU Considerations**  
> When selecting hardware, it is a good idea to consider CPU compatibility for VMware vMotion™ (which in turn affects DRS) and VMware Fault Tolerance.
> 
> **Hardware-Assisted Virtualization**  
> Most recent processors from both Intel and AMD include hardware features to assist virtualization. These features were released in two generations:
> 
> *   the first generation introduced CPU virtualization;
> *   the second generation added memory management unit (MMU) virtualization; For the best performance, make sure your system uses processors with second-generation hardware-assist features. 
> 
> **Hardware-Assisted CPU Virtualization (VT-x and AMD-V)**  
> The first generation of hardware virtualization assistance, VT-x from Intel and AMD-V from AMD, became available in 2006. These technologies automatically trap sensitive events and instructions, eliminating the overhead required to do so in software. This allows the use of a hardware virtualization (HV) virtual machine monitor (VMM) as opposed to a binary translation (BT) VMM. While HV outperforms BT for the vast majority of workloads, there are a few workloads where the reverse is true.
> 
> **Hardware-Assisted MMU Virtualization (Intel EPT and AMD RVI)**  
> More recent processors also include second-generation hardware virtualization assistance that addresses the overheads due to memory management unit (MMU) virtualization by providing hardware support to virtualize the MMU. ESXi supports this feature both in AMD processors, where it is called rapid virtualization indexing (RVI) or nested page tables (NPT), and in Intel processors, where it is called extended page tables (EPT).
> 
> **Hardware-Assisted I/O MMU Virtualization (VT-d and AMD-Vi)**  
> An even newer processor feature is an I/O memory management unit that remaps I/O DMA transfers and device interrupts. This can allow virtual machines to have direct access to hardware I/O devices, such as network cards, storage controllers (HBAs) and GPUs. In AMD processors this feature is called AMD I/O Virtualization (AMD-Vi or IOMMU) and in Intel processors the feature is called Intel Virtualization Technology for Directed I/O (VT-d).

If you want more information on the different technologies, I would suggest reading &#8220;<a href="http://www.vmware.com/files/pdf/software_hardware_tech_x86_virt.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/software_hardware_tech_x86_virt.pdf']);">Software and Hardware Techniques for x86 Virtualization</a>&#8220;. Both AMD and Intel support similar functions, as long as you pick a CPU family that supports the above features you will be good. Also make sure you stay consistent with your hosts. This will help with vMotion and DRS. You can also check out &#8220;<a href="http://www.vmware.com/a/vmmark/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/a/vmmark/']);">VMware VMmark 2.0</a>&#8221; to see how your server performed in the benchmark.

### Based on the service catalog and given functional requirements, for each service: Determine the most appropriate compute technologies for the design

From <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">this</a> PDF:

> CPU Features
> 
> *   Buy the fastest CPU and the most Cache you can afford
> *   64-bit
> *   Intel-VT
> *   AMD-VI and RVI (Rapid Virtualization Index) 

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf']);">vSphere Installation and Setup vSphere 5.0</a>&#8220;:

> Hosts running virtual machines with 64-bit guest operating systems have the following hardware requirements:
> 
> *   For AMD Opteron-based systems, the processors must be Opteron Rev E or later.
> *   For Intel Xeon-based systems, the processors must include support for Intel Virtualization Technology (VT). Many servers that include CPUs with VT support might have VT disabled by default, so you must enable VT manually. If your CPUs support VT ,but you do not see this option in the BIOS, contact your vendor to request a BIOS version that lets you enable VT support. 

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf']);">vSphere Resource Management ESXi 5.0</a>&#8220;:

> **Using CPU Affinity**  
> By specifying a CPU affinity setting for each virtual machine, you can restrict the assignment of virtual machines to a subset of the available processors in multiprocessor systems. By using this feature, you can assign each virtual machine to processors in the specified affinity set.
> 
> CPU affinity specifies virtual machine-to-processor placement constraints and is different from the relationship created by a VM-VM or VM-Host affinity rule, which specifies virtual machine-to-virtual machine host placement constraints. In this context, the term CPU refers to a logical processor on a hyperthreaded system and refers to a core on a non-hyperthreaded system.
> 
> The CPU affinity setting for a virtual machine applies to all of the virtual CPUs associated with the virtual machine and to all other threads (also known as worlds) associated with the virtual machine. Such virtual machine threads perform processing required for emulating mouse, keyboard, screen, CD-ROM, and miscellaneous legacy devices.
> 
> In some cases, such as display-intensive workloads, significant communication might occur between the virtual CPUs and these other virtual machine threads. Performance might degrade if the virtual machine&#8217;s affinity setting prevents these additional threads from being scheduled concurrently with the virtual machine&#8217;s virtual CPUs. Examples of this include a uniprocessor virtual machine with affinity to a single CPU or a two-way SMP virtual machine with affinity to only two CPUs.
> 
> For the best performance, when you use manual affinity settings, VMware recommends that you include at least one additional physical CPU in the affinity setting to allow at least one of the virtual machine&#8217;s threads to be scheduled at the same time as its virtual CPUs. Examples of this include a uniprocessor virtual machine with affinity to at least two CPUs or a two-way SMP virtual machine with affinity to at least three CPUs
> 
> &#8230;  
> &#8230;
> 
> **Potential Issues with CPU Affinity**  
> Before you use CPU affinity, you might need to consider certain issues. Potential issues with CPU affinity include:
> 
> *   For multiprocessor systems, ESXi systems perform automatic load balancing. Avoid manual specification of virtual machine affinity to improve the scheduler’s ability to balance load across processors.
> *   Affinity can interfere with the ESXi host’s ability to meet the reservation and shares specified for a virtual machine.
> *   Because CPU admission control does not consider affinity, a virtual machine with manual affinity settings might not always receive its full reservation. Virtual machines that do not have manual affinity settings are not adversely affected by virtual machines with manual affinity settings.
> *   When you move a virtual machine from one host to another, affinity might no longer apply because the new host might have a different number of processors.
> *   The NUMA scheduler might not be able to manage a virtual machine that is already assigned to certain processors using affinity.
> *   Affinity can affect the host&#8217;s ability to schedule virtual machines on multi-core or hyper-threaded processors to take full advantage of resources shared on such processors. 

Some power management features from the same document:

> **Host Power Management Policies**  
> ESXi can take advantage of several power management features that the host hardware provides to adjust the trade-off between performance and power use. You can control how ESXi uses these features by selecting a power management policy.
> 
> In general, selecting a high-performance policy provides more absolute performance, but at lower efficiency (performance per watt). Lower-power policies provide less absolute performance, but at higher efficiency. ESXi provides five power management policies. If the host does not support power management, or if the BIOS settings specify that the host operating system is not allowed to manage power, only the Not Supported policy is available.
> 
> You select a policy for a host using the vSphere Client. If you do not select a policy, ESXi uses Balanced by default.

From the same document:

> **Sharing Memory Across Virtual Machines**  
> Many ESXi workloads present opportunities for sharing memory across virtual machines (as well as within a single virtual machine).
> 
> For example, several virtual machines might be running instances of the same guest operating system, have the same applications or components loaded, or contain common data. In such cases, a host uses a proprietary transparent page sharing technique to securely eliminate redundant copies of memory pages. With memory sharing, a workload running in virtual machines often consumes less memory than it would when running on physical machines. As a result, higher levels of overcommitment can be supported efficiently.
> 
> Use the Mem.ShareScanTime and Mem.ShareScanGHz advanced settings to control the rate at which the system scans memory to identify opportunities for sharing memory.
> 
> You can also disable sharing for individual virtual machines by setting the sched.mem.pshare.enable option to FALSE (this option defaults to TRUE)

and more

> **Memory Compression**  
> ESXi provides a memory compression cache to improve virtual machine performance when you use memory overcommitment. Memory compression is enabled by default. When a host&#8217;s memory becomes overcommitted, ESXi compresses virtual pages and stores them in memory.
> 
> Because accessing compressed memory is faster than accessing memory that is swapped to disk, memory compression in ESXi allows you to overcommit memory without significantly hindering performance. When a virtual page needs to be swapped, ESXi first attempts to compress the page. Pages that can be compressed to 2 KB or smaller are stored in the virtual machine&#8217;s compression cache, increasing the capacity of the host.
> 
> You can set the maximum size for the compression cache and disable memory compression using the Advanced Settings dialog box in the vSphere Client.

Some information regarding NUMA from the same document:

> **Resource Management in NUMA Architectures**  
> You can perform resource management with different types of NUMA architecture.
> 
> With the proliferation of highly multicore systems, NUMA architectures are becoming more popular as these architectures allow better performance scaling of memory intensive workloads. All modern Intel and AMD systems have NUMA support built into the processors. Additionally, there are traditional NUMA systems like the IBM Enterprise X-Architecture that extend Intel and AMD processors with NUMA behavior with specialized chipset support.
> 
> Typically, you can use BIOS settings to enable and disable NUMA behavior. For example, in AMD Opteronbased HP Proliant servers, NUMA can be disabled by enabling node interleaving in the BIOS. If NUMA is enabled, the BIOS builds a system resource allocation table (SRAT) which ESXi uses to generate the NUMA information used in optimizations. For scheduling fairness, NUMA optimizations are not enabled for systems with too few cores per NUMA node or too few cores overall. You can modify the numa.rebalancecorestotal and numa.rebalancecoresnode options to change this behavior.

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> **General BIOS Settings**
> 
> *   Make sure you are running the latest version of the BIOS available for your system.
> *   Make sure the BIOS is set to enable all populated processor sockets and to enable all cores in each socket.
> *   Enable “Turbo Boost” in the BIOS if your processors support it.
> *   Make sure hyper-threading is enabled in the BIOS for processors that support it.
> *   Some NUMA-capable systems provide an option in the BIOS to disable NUMA by enabling node interleaving. In most cases you will get the best performance by disabling node interleaving (in other words, leaving NUMA enabled).
> *   Make sure any hardware-assisted virtualization features (VT-x, AMD-V, EPT, RVI, and so on) are enabledin the BIOS.
> *   Disable from within the BIOS any devices you won’t be using. This might include, for example, unneeded serial, USB, or network ports. See “ESXi General Considerations” on page 17 for further details.
> *   Cache prefetching mechanisms (sometimes called DPL Prefetch, Hardware Prefetcher, L2 Streaming Prefetch, or Adjacent Cache Line Prefetch) usually help performance, especially when memory access patterns are regular. When running applications that access memory randomly, however, disabling these mechanisms might result in improved performance.
> *   If the BIOS allows the memory scrubbing rate to be configured, we recommend leaving it at the manufacturer’s default setting 

More from the same doc:

> **Power Management BIOS Settings**  
> VMware ESXi includes a full range of host power management capabilities in the software that can save power when a host is not fully utilized (see “Host Power Management in ESXi” on page 23). We recommend that you configure your BIOS settings to allow ESXi the most flexibility in using (or not using) the power management features offered by your hardware, then make your power-management choices within ESXi.
> 
> *   In order to allow ESXi to control CPU power-saving features, set power management in the BIOS to “OS Controlled Mode” or equivalent. Even if you don’t intend to use these power-saving features, ESXi provides a convenient way to manage them.
> *   Availability of the C1E halt state typically provides a reduction in power consumption with little or no impact on performance. When “Turbo Boost” is enabled, the availability of C1E can sometimes even increase the performance of certain single-threaded workloads. We therefore recommend that you enable C1E in BIOS. 
>     *   However, for a very few workloads that are highly sensitive to I/O latency, especially those with low CPUutilization, C1E can reduce performance. In these cases, you might obtain better performance by disabling C1E in BIOS, if that option is available.
> *   C-states deeper than C1/C1E (i.e., C3, C6) allow further power savings, though with an increased chance of performance impacts. We recommend, however, that you enable all C-states in BIOS, then use ESXi host power management to control their use. 

If performance is your goal, get hardware that can support all the power saving features. And check for advanced features like Cache prefetching. Also see if you can efficiently utilized NUMA. Also check to make sure Hardware Assisted Virtualization is supported on the hardware, this will help with performance. If performance is not a big deal, then buy hardware that can support the calculated load. All those features are great but for non-critical application and non-latency sensitive applications the current/latest hardware (without any special features) will be more than enough.

### Explain the impact of a technical design on the choice of server density: Scale Up, Scale Out, Auto Deploy

From <a href="http://professionalvmware.com/2012/03/apac-vbrownbag-follow-up-vcap-dcd-host-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://professionalvmware.com/2012/03/apac-vbrownbag-follow-up-vcap-dcd-host-design/']);">APAC BrownBag Session 8</a>

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_up_vs_out.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_up_vs_out.png']);"><img class="alignnone size-full wp-image-3216" title="scale_up_vs_out" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_up_vs_out.png" alt="scale up vs out VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="887" height="286" /></a>

From <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">this</a> PDF:

> **Host Hardware Type**  
> Blades or Pizza boxes?
> 
> **Blades**

| Good                        |                             Bad                              |
| --------------------------- |:------------------------------------------------------------:|
| Flexible                    |                      Locks into Vendor                       |
| Easy to Install and Replace |             More Power and Cooling per Enclosure             |
| Simpler Cabling             | Shared Chassis and components could be SPOF (larger outages) |
| Fewer I/O Ports             |                    Not as much expansion                     |
| Management (Opex)           |                                                              |
| More DC Engineering         |                                                              |
| Smaller Footprint           |                                                              |

From the <a href="http://professionalvmware.com/2012/03/apac-vbrownbag-follow-up-vcap-dcd-host-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://professionalvmware.com/2012/03/apac-vbrownbag-follow-up-vcap-dcd-host-design/']);">APAC Brownbag Session 8</a>:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/blades_racks.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/blades_racks.png']);"><img class="alignnone size-full wp-image-3218" title="blades_racks" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/blades_racks.png" alt="blades racks VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="819" height="432" /></a>

There is a also a great article from IBM &#8220;<a href="http://www.redbooks.ibm.com/redpapers/pdfs/redp3953.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.redbooks.ibm.com/redpapers/pdfs/redp3953.pdf']);">VMware ESX Server: Scale Up or Scale Out?</a>&#8220;, from that paper:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_out_example.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_out_example.png']);"><img class="alignnone size-full wp-image-3219" title="scale_out_example" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_out_example.png" alt="scale out example VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="468" height="397" /></a>

and also this:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_up_example.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_up_example.png']);"><img class="alignnone size-full wp-image-3220" title="scale_up_example" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/scale_up_example.png" alt="scale up example VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="539" height="380" /></a>

Duncap Epping has two posts about these topics &#8220;<a href="http://www.yellow-bricks.com/2010/03/17/scale-up/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2010/03/17/scale-up/']);">Scale UP!</a>&#8221; and &#8220;<a href="http://www.yellow-bricks.com/2011/07/21/scale-upout-and-impact-of-vram-part-2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2011/07/21/scale-upout-and-impact-of-vram-part-2/']);">Scale Up/Out and impact of vRAM?!? (part 2)</a>&#8220;. It has good examples of each. From the blog:

> Lets assume the following:
> 
> *   To virtualize: 300 servers
> *   Average Mem configured: 3GB
> *   Average vCPU configured: 1.3 
> 
> That would be a total of 900GB and 390 vCPUs. Now from a CPU perspective the recommended best practice that VMware PSO has had for the last years has been 5-8 vCPUs per core and we’ll come back to why this is important in second. Lets assume we will use 2U servers for now with different configurations. (When you do the math fiddle around with the RAM/Core/Server ratio, 96 vs 192 vs 256 could make a nice difference!)
> 
> Config 1:
> 
> *   Dell r710
> *   2 x 4 Core – Intel
> *   96GB of memory
> *   $ 5500 per host 
> 
> Config 2:
> 
> *   Dell R810
> *   2 x 8 Core – Intel
> *   192GB of memory
> *   $13,000 per host 

Check out the blog for more in depth look into the examples.

### Determine a consolidation ratio based upon capacity analysis data

From &#8220;<a href="http://searchservervirtualization.techtarget.com/tip/Defining-an-ideal-virtual-server-consolidation-ratio" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://searchservervirtualization.techtarget.com/tip/Defining-an-ideal-virtual-server-consolidation-ratio']);">Defining an ideal virtual server consolidation ratio</a>&#8220;:

> Virtual server consolidation ratios vary widely  
> With that as the backdrop, what kinds of server consolidation ratios are IT administrators working with these days? The answer is, not surprisingly, it depends.
> 
> Back in the days of VMware ESX 3.x, a good rule of thumb for virtual server consolidation was four VMs per core, said Joe Sanchez, an IT manager at hosting provider Go Daddy. Given a dual-processor, quad-core server, for example, that resulted in about eight VMs per host, or an 8:1 consolidation ratio.
> 
> These days, most hypervisors can theoretically support higher numbers of VMs per core, but even so, four VMs of one or two virtual CPUs (vCPUs) per core is still a good guide if balanced performance is the goal, Sanchez said.
> 
> “The new servers and ESX versions can handle more VMs,” he said, “but the CPU wait time is still affected and can cause performance issues with too many VMs waiting on the same core.”
> 
> And if performance isn’t a concern, what about test and development environments? “Then load the cores up until the cows come home,” Sanchez said.
> 
> Walz Group, a provider of regulated document management services, uses that model for their virtual server consolidation strategy and very conservative VM-to-host ratios for production systems, while it uses much higher ratios for environments such as test and development and quality assurance.
> 
> “On production systems, we hardly ever run more than 15 VMs per host,” said Bart Falzarano, chief information security officer at the Temecula, Calif., firm, which runs VMware, Cisco dual-processor, four-core UCS B-series blades and NetApp storage configured in a certified FlexPod configuration.
> 
> Outside production, however, there are no such restrictions, with virtual server consolidation ratios often reaching 40:1, said Falzarano. He said he knew of environments at other organizations that drove VM densities much higher—in the neighborhood of 100:1.

And from &#8220;<a href="http://www.ittoday.info/Articles/VMWare_ESX_Performance_Optimization.htm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ittoday.info/Articles/VMWare_ESX_Performance_Optimization.htm']);">VMWare ESX Performance Optimization</a>&#8220;:

> You might be one of those users of VMware ESX that is happy with the performance of your virtualization platform or the performance of your individual or collective virtual machines. But what happens tomorrow if something in the environment changes and it negatively affects your performance? What happens if you need to achieve a 12:1 server consolidation ratio on an existing VMware ESX that today only hosts eight virtual machines? At that point, it may become extremely important to fine tune the environment in order to squeeze out every ounce of performance that your environment can offer.
> 
> **Host Server Memory Performance**  
> Much like the processor in a VMware ESX host server, the memory of the host server is also considered a significant bottleneck. And just like the processor scenario, it is important to add as much memory to your VMware ESX host server as possible. Having a sufficient amount of memory for all of your virtual machines is important to achieving good performance. A sufficient amount of memory is roughly equivalent to the amount of memory you would have assigned to each virtual machine if they were physical. As an example, to effectively run a Windows XP Professional virtual machine you might allocate 512MB of memory to it.
> 
> It is important to note here that system memory has quickly become one of the most expensive components found in today&#8217;s modern server; so you need to make sure that you properly match up the amount of memory in the system to the virtual machine density that can be achieved with the amount of processing power available. In other words, if you have enough processor resources in your host server to support ten virtual machines, don&#8217;t overpopulate your host server with expensive additional memory beyond what that density is capable of consuming if you cannot achieve a higher consolidation ratio due to processor limitations.

During your initial capacity analysis figure out what the actual CPU and RAM usage is. Then purchase the necessary hardware to fill the need of the usage. Also keep in mind if Scale Out or Scale Up is your goal. If you decide to go for redundancy then Scale Out is your plan, in which case your consolidation ratio will be a little smaller since you will have smaller physical servers. If you decide to go with scale up (bigger servers) then your consolidation ratio will be better since the physical servers will have more CPU and RAM. A good thing to keep in mind, from <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">this</a> PDF:

> Cores per CPU:  
> The number of cores per host must match or exceed the number of vCPUs of the Largest VM

Here is a real life example for the UCS blades, &#8220;<a href="http://blog.colovirt.com/2010/05/24/cisco-vmware-cisco-ucs-b6620-vmware-consolidation-ratio/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.colovirt.com/2010/05/24/cisco-vmware-cisco-ucs-b6620-vmware-consolidation-ratio/']);">Cisco, VMware: Cisco UCS B200-M1 VMware Consolidation Ratio</a>&#8220;, from that page:

> There are a total of 7 blades in our VMware environment, but only 5 of those are dedicated to our main HA/DRS cluster. That gives us ~240 gigs of RAM for the main cluster. Currently, I am seeing a VM consolidation ratio of about 24 VMs (virtual machines) per B200-M1 blade. The limitation here is definitely the RAM. The CPU itself is less than 25% utilized per blade.

Also if you are using Capacity Planner you can check your consolidation ratio, by running different reports. For more information check out &#8220;<a href="http://www.virtualizationteam.com/virtualization-vmware/capacity-planner/optimize-your-vmware-capacity-planning-report.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virtualizationteam.com/virtualization-vmware/capacity-planner/optimize-your-vmware-capacity-planning-report.html']);">Optimize Your VMware Capacity Planning Report</a>&#8221; Lastly here is a picture of consolidation from &#8220;<a href="http://www.avarsys.com/pdfs/Intel_Server_Consolidation_Whitepaper.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.avarsys.com/pdfs/Intel_Server_Consolidation_Whitepaper.pdf']);">Twenty-to-One Consolidation on Intel Architecture</a>&#8220;:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/consolidation.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/consolidation.png']);"><img class="alignnone size-full wp-image-3221" title="consolidation" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/consolidation.png" alt="consolidation VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="601" height="363" /></a>

### Calculate the number of nodes in an HA cluster based upon host failure count and resource guarantees.

From &#8220;<a href="http://www.vmware.com/files/pdf/techpaper/vmw-vsphere-high-availability.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/vmw-vsphere-high-availability.pdf']);">vSphere High Availability Deployment Best Practices</a>&#8220;:

> **Host Selection**
> 
> Overall vSphere availability starts with proper host selection. This includes items such as redundant power supplies, error-correcting memory, remote monitoring and notification, and so on. Consideration should also be given to removing single points of failure in host location. This includes distributing hosts across multiple racks or blade chassis to remove the ability for rack or chassis failure to impact an entire cluster.
> 
> When deploying a VMware HA cluster, it is a best practice to build the cluster out of identical server hardware. Using identical hardware provides a number of key advantages, such as the following ones:
> 
> *   Simplifies configuration and management of the servers using Host Profiles
> *   Increases ability to handle server failures and reduces resource fragmentation. 
> 
> Using drastically different hardware will lead to an unbalanced cluster, as described in the “Admission Control” section. By default, HA prepares for the worst-case scenario in that the largest host in the cluster could fail. To handle the worst case, more resources across all hosts must be reserved, making them essentially unusable.
> 
> Additionally, care should be taken to remove any inconsistencies that would prevent a virtual machine from being started on any cluster host. Inconsistencies such as mounting datastores to a subset of the cluster hosts or the implementation of DRS “required” virtual machine–to–host required affinity rules are examples of items to carefully consider. Avoiding these conditions will increase the portability of the virtual machine and provide a higher level of availability. Inconsistencies can be checked for a given virtual machine by using the VMware vSphere® Client™ and selecting the migrate option to determine whether any error conditions would prevent vMotion from being able to migrate the virtual machine to other hosts in the cluster.
> 
> The overall size of a cluster is another important factor to consider. Smaller-sized clusters require a larger relative percentage of the available cluster resources to be set aside as reserve capacity to adequately handle failures. For example, for a cluster of three nodes to tolerate a single host failure, about 33 percent of the cluster resources will be reserved for failover. A 10-node cluster requires that only 10 percent be reserved.
> 
> In contrast, as cluster size increases, so does the HA management complexity of the cluster. This complexity is associated with general configuration factors as well as ongoing management tasks such as troubleshooting. This increase in management complexity, however, is overshadowed by the benefits a large cluster can provide. Features such as DRS and vSphere Distributed Power Management (VMware DPM) become very compelling with large clusters. In general, it is recommended that customers establish the largest clusters possible to reap the full benefits of these solutions.

There is also an example in &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-availability-guide.pdf']);">vSphere Availability ESXi 5.0</a>&#8220;:

> **Example: Admission Control Using Host Failures Cluster Tolerates Policy**  
> The way that slot size is calculated and used with this admission control policy is shown in an example. Make the following assumptions about a cluster:
> 
> *   The cluster is comprised of three hosts, each with a different amount of available CPU and memory resources. The first host (H1) has 9GHz of available CPU resources and 9GB of available memory, while Host 2 (H2) has 9GHz and 6GB and Host 3 (H3) has 6GHz and 6GB.
> *   There are five powered-on virtual machines in the cluster with differing CPU and memory requirements. VM1 needs 2GHz of CPU resources and 1GB of memory, while VM2 needs 2GHz and 1GB, VM3 needs1GHz and 2GB, VM4 needs 1GHz and 1GB, and VM5 needs 1GHz and 1GB.
> *   The Host Failures Cluster Tolerates is set to one.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/ha-host_failures_set_example.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/ha-host_failures_set_example.png']);"><img class="alignnone size-full wp-image-3224" title="ha-host_failures_set_example" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/ha-host_failures_set_example.png" alt="ha host failures set example VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="465" height="318" /></a>

> 1.  Slot size is calculated by comparing both the CPU and memory requirements of the virtual machines and selecting the largest. The largest CPU requirement (shared by VM1 and VM2) is 2GHz, while the largest memory requirement (for VM3) is 2GB. Based on this, the slot size is 2GHz CPU and 2GB memory.
> 2.  Maximum number of slots that each host can support is determined. H1 can support four slots. H2 can support three slots (which is the smaller of 9GHz/2GHz and 6GB/2GB) and H3 can also support three slots.
> 3.  Current Failover Capacity is computed. The largest host is H1 and if it fails, six slots remain in the cluster, which is sufficient for all five of the powered-on virtual machines. If both H1 and H2 fail, only three slots remain, which is insufficient.Therefore, the Current Failover Capacity is one. The cluster has one available slot (the six slots on H2 and H3 minus the five used slots) 

And another example from the same document:

> **Example: Admission Control Using Percentage of Cluster Resources Reserved Policy**  
> The way that Current Failover Capacity is calculated and used with this admission control policy is shown with an example. Make the following assumptions about a cluster:
> 
> *   The cluster is comprised of three hosts, each with a different amount of available CPU and memory resources. The first host (H1) has 9GHz of available CPU resources and 9GB of available memory, while Host 2 (H2) has 9GHz and 6GB and Host 3 (H3) has 6GHz and 6GB.
> *   There are five powered-on virtual machines in the cluster with differing CPU and memory requirements. VM1 needs 2GHz of CPU resources and 1GB of memory, while VM2 needs 2GHz and 1GB, VM3 needs 1GHz and 2GB, VM4 needs 1GHz and 1GB, and VM5 needs 1GHz and 1GB.
> *   The Configured Failover Capacity is set to 25%.

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/ha-percent-example.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/ha-percent-example.png']);"><img class="alignnone size-full wp-image-3227" title="ha-percent-example" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/ha-percent-example.png" alt="ha percent example VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="518" height="301" /></a>

> The total resource requirements for the powered-on virtual machines is 7GHz and 6GB. The total host resources available for virtual machines is 24GHz and 21GB. Based on this, the Current CPU Failover Capacity is 70% ((24GHz &#8211; 7GHz)/24GHz). Similarly, the Current Memory Failover Capacity is 71% ((21GB-6GB)/21GB).Because the cluster&#8217;s Configured Failover Capacity is set to 25%, 45% of the cluster&#8217;s total CPU resources and 46% of the cluster&#8217;s memory resources are still available to power on additional virtual machines.

Depending on what your HA policy is (decided from the above examples) calculate the total amount of resources used and total available resource. Then decide what kind of hardware will be capable of running the decided load with the failure scenario in mind. Back in the 4.x days, HA worked in a different manner and how many hosts added to a cluster from an enclosure chosen mattered, now with 5.x HA works in a different manner. If you want to know best practices for vSphere 4.x HA, check out:

*   <a href="http://www.vmware.com/files/pdf/techpaper/VMW-Server-WP-BestPractices.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/VMW-Server-WP-BestPractices.pdf']);">VMware High Availability (VMware HA): Deployment Best Practices VMware vSphere 4.1</a>
*   <a href="http://www.yellow-bricks.com/2009/02/09/blades-and-ha-cluster-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2009/02/09/blades-and-ha-cluster-design/']);">Blades and HA / Cluster design</a>
*   <a href="http://www.cloud-buddy.com/?p=786" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.cloud-buddy.com/?p=786']);">HA Cluster design considerations in vSphere 5</a>

### Explain the implications of using reservations, limits, and shares on the physical design

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf']);">vSphere Resource Management ESXi 5.0</a>&#8220;:

> **Resource Allocation Shares**  
> Shares specify the relative importance of a virtual machine (or resource pool). If a virtual machine has twice as many shares of a resource as another virtual machine, it is entitled to consume twice as much of that resource when these two virtual machines are competing for resources.
> 
> Shares are typically specified as **High**, **Normal**, or **Low** and these values specify share values with a 4:2:1 ratio, respectively. You can also select Custom to assign a specific number of shares (which expresses a proportional weight) to each virtual machine.
> 
> Specifying shares makes sense only with regard to sibling virtual machines or resource pools, that is, virtual machines or resource pools with the same parent in the resource pool hierarchy. Siblings share resources according to their relative share values, bounded by the reservation and limit. When you assign shares to a virtual machine, you always specify the priority for that virtual machine relative to other powered-on virtual machines.
> 
> The following table shows the default CPU and memory share values for a virtual machine. For resource pools, the default CPU and memory share values are the same, but must be multiplied as if the resource pool were a virtual machine with four virtual CPUs and 16 GB of memory.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/share_values.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/share_values.png']);"><img class="alignnone size-full wp-image-3231" title="share_values" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/share_values.png" alt="share values VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="588" height="154" /></a>
> 
> For example, an SMP virtual machine with two virtual CPUs and 1GB RAM with CPU and memory shares set to Normal has 2&#215;1000=2000 shares of CPU and 10&#215;1024=10240 shares of memory.
> 
> **NOTE** Virtual machines with more than one virtual CPU are called SMP (symmetric multiprocessing) virtual machines. ESXi supports up to 32 virtual CPUs per virtual machine.
> 
> The relative priority represented by each share changes when a new virtual machine is powered on. This affects all virtual machines in the same resource pool. All of the virtual machines have the same number of virtual CPUs. Consider the following examples.
> 
> *   Two CPU-bound virtual machines run on a host with 8GHz of aggregate CPU capacity. Their CPU shares are set to Normal and get 4GHz each.
> *   A third CPU-bound virtual machine is powered on. Its CPU shares value is set to High, which means it should have twice as many shares as the machines set to Normal. The new virtual machine receives 4GHz and the two other machines get only 2GHz each. The same result occurs if the user specifies a custom share value of 2000 for the third virtual machine. 

Now onto Reservations, from the same document:

> **Resource Allocation Reservation**  
> A reservation specifies the guaranteed minimum allocation for a virtual machine.
> 
> vCenter Server or ESXi allows you to power on a virtual machine only if there are enough unreserved resources to satisfy the reservation of the virtual machine. The server guarantees that amount even when the physical server is heavily loaded. The reservation is expressed in concrete units (megahertz or megabytes).
> 
> For example, assume you have 2GHz available and specify a reservation of 1GHz for VM1 and 1GHz for VM2. Now each virtual machine is guaranteed to get 1GHz if it needs it. However, if VM1 is using only 500MHz, VM2 can use 1.5GHz.  
> Reservation defaults to 0. You can specify a reservation if you need to guarantee that the minimum required amounts of CPU or memory are always available for the virtual machine.

Lastly the Limits:

> **Resource Allocation Limit**  
> Limit specifies an upper bound for CPU, memory, or storage I/O resources that can be allocated to a virtual machine.
> 
> A server can allocate more than the reservation to a virtual machine, but never allocates more than the limit, even if there are unused resources on the system. The limit is expressed in concrete units (megahertz, megabytes, or I/O operations per second).
> 
> CPU, memory, and storage I/O resource limits default to unlimited. When the memory limit is unlimited, the amount of memory configured for the virtual machine when it was created becomes its effective limit.
> 
> In most cases, it is not necessary to specify a limit. There are benefits and drawbacks:
> 
> *   Benefits &#8211; Assigning a limit is useful if you start with a small number of virtual machines and want to manage user expectations. Performance deteriorates as you add more virtual machines. You can simulate having fewer resources available by specifying a limit.
> *   Drawbacks &#8211; You might waste idle resources if you specify a limit. The system does not allow virtual machines to use more resources than the limit, even when the system is underutilized and idle resources are available. Specify the limit only if you have good reasons for doing so. 

From the same document, here are some recommendations:

> **Resource Allocation Settings Suggestions**  
> Select resource allocation settings (shares, reservation, and limit) that are appropriate for your ESXi environment. The following guidelines can help you achieve better performance for your virtual machines.
> 
> *   If you expect frequent changes to the total available resources, use Shares to allocate resources fairly across virtual machines. If you use Shares, and you upgrade the host, for example, each virtual machine stays at the same priority (keeps the same number of shares) even though each share represents a larger amount of memory, CPU, or storage I/O resources.
> *   Use Reservation to specify the minimum acceptable amount of CPU or memory, not the amount you want to have available. The host assigns additional resources as available based on the number of shares, estimated demand, and the limit for your virtual machine. The amount of concrete resources represented by a reservation does not change when you change the environment, such as by adding or removing virtual machines.
> *   When specifying the reservations for virtual machines, do not commit all resources (plan to leave at least 10% unreserved). As you move closer to fully reserving all capacity in the system, it becomes increasingly difficult to make changes to reservations and to the resource pool hierarchy without violating admission control. In a DRS-enabled cluster, reservations that fully commit the capacity of the cluster or of individual hosts in the cluster can prevent DRS from migrating virtual machines between hosts. 

Limits are rarely used:

*   <a href="http://www.yellow-bricks.com/2010/07/06/memory-limits/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2010/07/06/memory-limits/']);">Memory Limits</a> 
*   <a href="http://www.yellow-bricks.com/2010/05/18/limiting-your-vcpu/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2010/05/18/limiting-your-vcpu/']);">Limiting your vCPU</a> 
*   <a href="http://www.warmetal.nl/vmwareresources" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.warmetal.nl/vmwareresources']);">VMWare Resources: Reservations &#8211; Limits &#8211; Shares</a> 

Reservations should be used for critical VMs that you want to ensure that they will have a certain amount of resources even if it&#8217;s not currently using it (a guarantee). Reservations should be set slightly higher than the Avg. Active memory size (for overhead): <a href="http://www.yellow-bricks.com/2010/07/08/reservations-primer/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2010/07/08/reservations-primer/']);">Reservations primer</a> <a href="http://www.yellow-bricks.com/2010/03/03/cpumem-reservation-behaviour/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2010/03/03/cpumem-reservation-behaviour/']);">CPU/MEM Reservation Behavior</a>

### Specify the resource pool and vApp configuration based upon resource requirements.

From <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-resource-management-guide.pdf']);">vSphere Resource Management ESXi 5.0</a>:

> **Why Use Resource Pools?**  
> Resource pools allow you to delegate control over resources of a host (or a cluster), but the benefits are evident when you use resource pools to compartmentalize all resources in a cluster. Create multiple resource pools as direct children of the host or cluster and configure them. You can then delegate control over the resource pools to other individuals or organizations. Using resource pools can result in the following benefits.
> 
> *   Flexible hierarchical organization—Add, remove, or reorganize resource pools or change resource allocations as needed. 
> *   Isolation between pools, sharing within pools—Top-level administrators can make a pool of resources available to a department-level administrator. Allocation changes that are internal to one departmental resource pool do not unfairly affect other unrelated resource pools. 
> *   Access control and delegation—When a top-level administrator makes a resource pool available to a department-level administrator, that administrator can then perform all virtual machine creation and management within the boundaries of the resources to which the resource pool is entitled by the current shares, reservation, and limit settings. Delegation is usually done in conjunction with permissions settings. 
> *   Separation of resources from hardware—If you are using clusters enabled for DRS, the resources of all hosts are always assigned to the cluster. That means administrators can perform resource management independently of the actual hosts that contribute to the resources. If you replace three 2GB hosts with two 3GB hosts, you do not need to make changes to your resource allocations. This separation allows administrators to think more about aggregate computing capacity and less about individual hosts. 
> *   Management of sets of virtual machines running a multitier service— Group virtual machines for a multitier service in a resource pool. You do not need to set resources on each virtual machine. Instead, you can control the aggregate allocation of resources to the set of virtual machines by changing settings on their enclosing resource pool.
> 
> For example, assume a host has a number of virtual machines. The marketing department uses three of the virtual machines and the QA department uses two virtual machines. Because the QA department needs larger amounts of CPU and memory, the administrator creates one resource pool for each group. The administrator sets CPU Shares to High for the QA department pool and to Normal for the Marketing department pool so that the QA department users can run automated tests. The second resource pool with fewer CPU and memory resources is sufficient for the lighter load of the marketing staff. Whenever the QA department is not fully using its allocation, the marketing department can use the available resources. The numbers in the following figure show the effective allocations to the resource pools.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2012/09/resource_pools.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/09/resource_pools.png']);"><img class="alignnone size-full wp-image-3247" title="resource_pools" src="http://virtuallyhyper.com/wp-content/uploads/2012/09/resource_pools.png" alt="resource pools VCAP5 DCD Objective 3.4 – Determine Appropriate Compute Resources for a vSphere 5 Physical Design " width="484" height="218" /></a>

So if you have some SLA&#8217;s defined, then define Resource Pools for each SLA. Also as mentioned you can use them to separate departments for organizational purposes.

As for vApps, from &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-virtual-machine-admin-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-virtual-machine-admin-guide.pdf']);">vSphere Virtual Machine AdministrationESXi 5.0</a>&#8220;:

> **Managing Multi-Tiered Applications with vSphere vApp**  
> You can use VMware vSphere as a platform for running applications, in addition to using it as a platform for running virtual machines. The applications can be packaged to run directly on top of VMware vSphere. The format of how the applications are packaged and managed is called vSphere vApp. A vApp is a container, like a resource pool and can contain one or more virtual machines. A vApp also shares some functionality with virtual machines. A vApp can power on and power off, and can also be cloned. In the vSphere Client, a vApp is represented in both the Host and Clusters view and the VM and Template view. Each view has a specific summary page with the current status of the service and relevant summary information, as well as operations on the service.

The title describes it best. If you have a multi-tiered application (ie DB,Web,and App). You can create a VM for each service and then put them in a vApp. With a vApp you can export the configuration as one container. You can also define a boot order if there are dependencies within the vApp. And you can also define how the IPs are assigned within the vApp. vApps definitely help out with application management and dependencies. Within vCloud, vApps are heavily utilized.

### Size compute resources: Memory, CPU, I/O devices, Internal storage

From &#8220;<a href="http://searchservervirtualization.techtarget.com/tip/Sizing-server-hardware-for-virtual-machines" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://searchservervirtualization.techtarget.com/tip/Sizing-server-hardware-for-virtual-machines']);">Sizing server hardware for virtual machines</a>&#8220;:

> CPU With the advent of multi-core CPUs, it has become easier and cheaper to increase the number of CPUs in a host server. Nowadays, almost all servers come with two or four cores per physical CPU. A good rule of thumb is that four single CPU VMs can be supported per CPU core. This can vary by as much as 1-2 per core, and up to 8-10 per core based on the average CPU utilization of applications running on VMs.
> 
> A common misconception with virtual servers is that a VM can utilize as much CPU megahertz as needed from the combined total available. For example, a four CPU, quad core 2.6 GHz would have a combined total of 20,800 megahertz (8 x 2.6 GHz). A single vCPU VM however, can never use more megahertz then the maximum of one CPU/core. If a VM has 2 vCPUs, it can never use more megahertz than the maximum of each CPU/core. How many cores needed will also depend on whether multiple vCPU VMs are used or not.
> 
> You should always have at least one more core than the maximum number of vCPUs that will be assigned to a single VM. For example, don&#8217;t buy a two processor dual-core server with a total of four cores and try to run a four vCPU VM on it. The reason being that the CPU scheduler of the hypervisor needs to find 4 free cores simultaneously each time the VM makes a CPU request. If there are only a total of four available cores, the performance will be very slow. My recommendation would be to use quad core CPUs because more cores provide the CPU scheduler with more flexibility to process requests.

From <a href="http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://virtuallyhyper.com/wp-content/uploads/2013/04/vcap-dcd_notes.pdf']);">this</a> PDF:

> CPU Capacity:
> 
> *   Determine Requirement by using capacity planner; OS and App 
>     *   Vendor guidelines/documentation, talking to SME and StakeHolders
> *   Add needed growth to current usage for CPU capacity
> *   Do NOT plan to fully utilize CPU 
>     *   Plan for AVG Utilization of 60-80%
>     *   Leave headroom for: 
>         *   Short term utilization spikes
>         *   Patching/Maintenance
>         *   DataCenter Failover
>         *   VMkernel and Service OverHead
>         *   Growth 
> 
> Number of Hosts: CPU Capacity
> 
> *   No matter what, host config must meet CPU requirements
> *   How many CPUs per host? 
>     *   Cost of dense vs non-dense server
>     *   Consider no just the initial purchase, but the operational cost over time
>     *   Can enough memory be installed to keep the CPUs busy
>     *   Are there enough Storage and Network ports available to provide bandwidth to support VMs that could run on dense server
>     *   Isolation policies may drive more smaller (non-dense) services 
> 
> Number of vCPUs per Core:
> 
> *   VM performance drives this limit
> *   Goal is to efficiently use the CPU capacity without reducing performance
> *   More Cores = more sharing of memory and data buses 

Onto Memory, from &#8220;<a href="http://searchservervirtualization.techtarget.com/tip/Sizing-server-hardware-for-virtual-machines" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://searchservervirtualization.techtarget.com/tip/Sizing-server-hardware-for-virtual-machines']);">Sizing server hardware for virtual machines</a>&#8220;:

> Memory  
> When it comes to figuring out how much RAM to put in a host server, I would recommend installing the maximum amount if possible.
> 
> Yet, the opposite mentality should be taken when it comes to allocating memory for virtual servers, by only giving a VM the exact amount of memory it needs. Usually with physical servers, more memory than what is needed is installed and much of it ends up being wasted. With a VM, it is simple to increase the RAM at any time, so start out with the minimum amount of memory that you will think it will need and increase it later if necessary. It is possible to over-commit memory to virtual machines and assign more RAM to them then the physical host actually has. By doing this you run the risk of having your VMs swapping to disk when the host memory is exhausted which can cause decreased performance.

From the same PDF:

> Memory Capacity
> 
> *   Same as CPU 
> *   Do NOT plan to fully utilize memory/resources; 70-90%
> *   Leave head room for maintenance (*same as CPU) 
> 
> Memory Over-commitment
> 
> *   2 Types 
>     *   Total; does not affect performance
>     *   Active; does affect performance
> *   Active memory = active guest memory 
>     *   Amount of memory in use by guest OS and Applications
> *   Avoid active memory over-commitment 
>     *   Add more memory to host
>     *   Reduce consolidation Ratio
>     *   Reduce vRAM allocation
> *   Large memory pages will reduce memory over-commitment 
>     *   Large Pages are not shared For I/O Devices (HBAs and NICs), 

from &#8220;<a href="http://searchservervirtualization.techtarget.com/tip/Sizing-server-hardware-for-virtual-machines" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://searchservervirtualization.techtarget.com/tip/Sizing-server-hardware-for-virtual-machines']);">Sizing server hardware for virtual machines</a>&#8220;:

> Network  
> The number of network interface cards (NICs) needed in a virtual server will vary based on how much redundancy is desired, whether or not network storage will be used and which features will be selected. Using 802.1Q VLAN tagging provides the flexibility of using multiple VLANs on a single NIC, thus eliminating the need to have a separate NIC for each VLAN on a host server. For smaller servers, you can get away with using two NICs, but it is best to a have a minimum of four NICs on your host server. If you are using network storage, such as iSCSI, it would be wise to have more than four NICs, especially if you are going to use features like VMware&#8217;s vMotion. When creating vSwitches it&#8217;s best to assign multiple NIC&#8217;s to them for redundancy and increased capacity available to VMs.

From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> *   Make sure that end-to-end Fibre Channel speeds are consistent to help avoid performance problems.
> *   Configure maximum queue depth for Fibre Channel HBA cards.
> *   For the best networking performance, we recommend the use of network adapters that support the following hardware features: 
>     *    Checksum offload
>     *    TCP segmentation offload (TSO)
>     *    Ability to handle high-memory DMA (that is, 64-bit DMA addresses)
>     *    Ability to handle multiple Scatter Gather elements per Tx frame
>     *    Jumbo frames (JF)
>     *    Large receive offload (LRO)
> *   On some 10 Gigabit Ethernet hardware network adapters, ESXi supports NetQueue, a technology that significantly improves performance of 10 Gigabit Ethernet network adapters in virtualized environments.
> *   In addition to the PCI and PCI-X bus architectures, we now have the PCI Express (PCIe) architecture. Ideally single-port 10 Gigabit Ethernet network adapters should use PCIe x8 (or higher) or PCI-X 266 and dual-port 10 Gigabit Ethernet network adapters should use PCIe x16 (or higher). There should preferably be no “bridge chip” (e.g., PCI-X to PCIe or PCIe to PCI-X) in the path to the actual Ethernet device (including any embedded bridge chip on the device itself), as these chips can reduce performance. 

For Internal storage, from &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-installation-setup-guide.pdf']);">vSphere Installation and Setup vSphere 5.0</a>&#8220;:

> **Storage Requirements for ESXi 5.0 Installation**  
> Installing ESXi 5.0 requires a boot device that is a minimum of 1GB in size. When booting from a local disk or SAN/iSCSI LUN, a 5.2GB disk is required to allow for the creation of the VMFS volume and a 4GB scratch partition on the boot device. If a smaller disk or LUN is used, the installer will attempt to allocate a scratch region on a separate local disk. If a local disk cannot be found the scratch partition, /scratch, will be located on the ESXi host ramdisk, linked to /tmp/scratch. You can reconfigure /scratch to use a separate disk or LUN. For best performance and memory optimization, VMware recommends that you do not leave /scratch on the ESXi host ramdisk.

Since there is such a small requirement for the OS, you should install the OS on a USB flash card or an SD flash card. Having a local VMFS data-store doesn&#8217;t allow you to use any advanced features like HA, DRS, vMotion.. etc. Put your VMs on VMFS datastores that are located on a SAN for best practices. If you don&#8217;t have a SAN then you can use the VMware VSA, described in <a href="http://virtuallyhyper.com/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/vcap5-dcd-objective-3-3-create-a-vsphere-5-physical-storage-design-from-an-existing-logical-design/']);">Objective 3.3</a>. If you plan on having just one host and using the local storage for storing your VMs, then set up the local storage as RAID 1. This way you at least have some redundancy. From &#8220;<a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>&#8220;:

> Local storage performance might be improved with write-back cache. If your local storage has write-back cache installed, make sure it’s enabled and contains a functional battery module
> 
> &#8230;  
> &#8230;
> 
> vMotion performance could be reduced if host-level swap files are placed on local storage (whether SSD or hard drive).

### Given a constraint to use existing hardware, determine suitability of the hardware for the design

Make sure it&#8217;s a similar CPU family. If it&#8217;s an older CPU set, enable EVC to use the host for HA, vMotion&#8230; etc Make sure the PCI slot config is similar, this way you can use Host profiles. Also make sure the CPU size and Memory Size is similar, if it&#8217;s too big of a difference it will throw off the HA calculations. Of course check to make sure the Host is on the HCL. Make sure you can enabled HT, Intel VT, and eXecute Disable. Make sure it can handle 64bit.

