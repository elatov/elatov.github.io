---
title: 'RHCSA and RHCE Chapter 10 - The Kernel'
author: Karim Elatov
layout: post
permalink: /2013/07/rhcsa-and-rhce-chapter-10-the-kernel/
sharing_disabled:
  - 1
dsq_thread_id:
  - 1482888063
categories:
  - Certifications
  - OS
  - RHCSA and RHCE
tags:
  - RHCE
  - RHCSA
  - RHEL
---
## Kernel

The kernel is a very complex concept, I will try to use some references to put it all together. From <a href="http://www.tldp.org/LDP/sag/html/kernel-parts.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.tldp.org/LDP/sag/html/kernel-parts.html']);">Important parts of the kernel</a>:

> The Linux kernel consists of several important parts: process management, memory management, hardware device drivers, filesystem drivers, network management, and various other bits and pieces.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/kernel_overview1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/kernel_overview1.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/kernel_overview1.png" alt="kernel overview1 RHCSA and RHCE Chapter 10   The Kernel" width="883" height="719" class="alignnone size-full wp-image-9149" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> Probably the most important parts of the kernel (nothing else works without them) are memory management and process management. Memory management takes care of assigning memory areas and swap space areas to processes, parts of the kernel, and for the buffer cache. Process management creates processes, and implements multitasking by switching the active process on the processor.
> 
> At the lowest level, the kernel contains a hardware device driver for each kind of hardware it supports.

From <a href="http://oss.org.cn/ossdocs/linux/kernel/a1/index.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://oss.org.cn/ossdocs/linux/kernel/a1/index.html']);">Conceptual Architecture of the Linux Kernel</a>:

> The Linux kernel is useless in isolation; it participates as one part in a larger system that, as a whole, is useful.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/linux_system_major_sys.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/linux_system_major_sys.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/linux_system_major_sys.png" alt="linux system major sys RHCSA and RHCE Chapter 10   The Kernel" width="477" height="253" class="alignnone size-full wp-image-9100" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> The Linux operating system is composed of four major subsystems:
> 
> 1.  **User Applications** - the set of applications in use on a particular Linux system will be different depending on what the computer system is used for, but typical examples include a word-processing application and a web-browser.
> 2.  **O/S Services** - these are services that are typically considered part of the operating system (a windowing system, command shell, etc.); also, the programming interface to the kernel (compiler tool and library) is included in this subsystem.
> 3.  **Linux Kernel** - the kernel abstracts and mediates access to the hardware resources, including the CPU.
> 4.  **Hardware Controllers** - this subsystem is comprised of all the possible physical devices in a Linux installation; for example, the CPU, memory hardware, hard disks, and network hardware are all members of this subsystem
> 
> **2.2 Purpose of the Kernel**
> 
> The Linux kernel presents a virtual machine interface to user processes. Processes are written without needing any knowledge of what physical hardware is installed on a computer - the Linux kernel abstracts all hardware into a consistent virtual interface. In addition, Linux supports multi-tasking in a manner that is transparent to user processes: each process can act as though it is the only process on the computer, with exclusive use of main memory and other hardware resources. The kernel actually runs several processes concurrently, and is responsible for mediating access to hardware resources so that each process has fair access while inter-process security is maintained.
> 
> The Linux kernel is composed of five main subsystems:
> 
> 1.  The **Process Scheduler (SCHED)** is responsible for controlling process access to the CPU. The scheduler enforces a policy that ensures that processes will have fair access to the CPU, while ensuring that necessary hardware actions are performed by the kernel on time.
> 2.  The **Memory Manager (MM)** permits multiple process to securely share the machine's main memory system. In addition, the memory manager supports virtual memory that allows Linux to support processes that use more memory than is available in the system. Unused memory is swapped out to persistent storage using the file system then swapped back in when it is needed.
> 3.  The **Virtual File System (VFS)** abstracts the details of the variety of hardware devices by presenting a common file interface to all devices. In addition, the VFS supports several file system formats that are compatible with other operating systems.
> 4.  The **Network Interface (NET)** provides access to several networking standards and a variety of network hardware.
> 5.  The **Inter-Process Communication (IPC)** subsystem supports several mechanisms for process-to-process communication on a single Linux system.
> 
> Figure 2.2 shows a high-level decomposition of the Linux kernel, where lines are drawn from dependent subsystems to the subsystems they depend on:
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/kernel_subsystem.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/kernel_subsystem.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/kernel_subsystem.png" alt="kernel subsystem RHCSA and RHCE Chapter 10   The Kernel" width="521" height="374" class="alignnone size-full wp-image-9101" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>

Another view from <a href="http://www.ibm.com/developerworks/library/l-linux-kernel/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ibm.com/developerworks/library/l-linux-kernel/']);">Anatomy of the Linux kernel</a>:

> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/gnu_linux.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/gnu_linux.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/gnu_linux.png" alt="gnu linux RHCSA and RHCE Chapter 10   The Kernel" width="433" height="288" class="alignnone size-full wp-image-9102" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>

### RHEL CPU Scheduler

From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/6.0_Release_Notes/Red_Hat_Enterprise_Linux-6-6.0_Release_Notes-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/6.0_Release_Notes/Red_Hat_Enterprise_Linux-6-6.0_Release_Notes-en-US.pdf']);">RedHat 6 Release notes</a>:

> **12.2.1. Completely Fair Scheduler (CFS)**  
> A process (or task) scheduler is a specific kernel subsystem that is responsible for assigning the order in which processes are sent to the CPU. The kernel (version 2.6.32) shipped in Red Hat Enterprise Linux 6 replaces the O(1) scheduler with the new Completely Fair Scheduler (CFS). The CFS implements the fair queuing scheduling algorithm.

We can check the scheduler information, by checking out the contents of **/proc/sched_debug**:

    [root@rhel1 ~]# cat /proc/sched_debug 
    Sched Debug Version: v0.09, 2.6.32-131.0.15.el6.i686 #1
    now at 4180191.632088 msecs
      .jiffies                                 : 3880191
      .sysctl_sched_latency                    : 5.000000
      .sysctl_sched_min_granularity            : 1.000000
      .sysctl_sched_wakeup_granularity         : 1.000000
      .sysctl_sched_child_runs_first           : 0.000000
      .sysctl_sched_features                   : 15471
      .sysctl_sched_tunable_scaling            : 1 (logaritmic)
    
    cpu#0, 2795.243 MHz
      .nr_running                    : 1
      .load                          : 1024
      .nr_switches                   : 46476
      .nr_load_updates               : 34812
      .nr_uninterruptible            : 0
      .next_balance                  : 3.880594
      .curr->pid                     : 1279
      .clock                         : 4180191.153573
      .cpu_load[0]                   : 1024
      .cpu_load[1]                   : 832
      .cpu_load[2]                   : 652
      .cpu_load[3]                   : 410
      .cpu_load[4]                   : 229
      .yld_count                     : 0
      .sched_switch                  : 0
      .sched_count                   : 47033
      .sched_goidle                  : 13369
      .avg_idle                      : 943520
      .ttwu_count                    : 26666
      .ttwu_local                    : 26666
      .bkl_count                     : 152
    
    cfs_rq[0]:/
      .exec_clock                    : 12072.940261
      .MIN_vruntime                  : 0.000001
      .min_vruntime                  : 10714.854637
      .max_vruntime                  : 0.000001
      .spread                        : 0.000000
      .spread0                       : 0.000000
      .nr_running                    : 1
      .load                          : 1024
      .nr_spread_over                : 9
      .shares                        : 0
    
    rt_rq[0]:/
      .rt_nr_running                 : 0
      .rt_throttled                  : 0
      .rt_time                       : 0.000000
      .rt_runtime                    : 950.000000
    
    runnable tasks:
                task   PID         tree-key  switches  prio     exec-runtime         sum-exec        sum-sleep
    ----------------------------------------------------------------------------------------------------------
    R            cat  1279     10714.854637         1   120     10714.854637         2.175898         0.000000 
    

We can see that CFS is used. There is a lot of resources on the scheduler:

*   <a href="http://people.redhat.com/mingo/cfs-scheduler/sched-design-CFS.txt" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://people.redhat.com/mingo/cfs-scheduler/sched-design-CFS.txt']);">cfs-scheduler</a> 
*   <a href="http://www.linuxjournal.com/magazine/completely-fair-scheduler" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.linuxjournal.com/magazine/completely-fair-scheduler']);">Completely Fair Scheduler</a> 
*   <a href="http://www.ibm.com/developerworks/library/l-completely-fair-scheduler/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ibm.com/developerworks/library/l-completely-fair-scheduler/']);">Inside the Linux 2.6 Completely Fair Scheduler</a>

From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Performance_Tuning_Guide/Red_Hat_Enterprise_Linux-6-Performance_Tuning_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Performance_Tuning_Guide/Red_Hat_Enterprise_Linux-6-Performance_Tuning_Guide-en-US.pdf']);">Performance Tuning Guide</a>:

> **4.2. CPU Scheduling**  
> The scheduler is responsible for keeping the CPUs in the system busy. The Linux scheduler implements a number of scheduling policies, which determine when and for how long a thread runs on a particular CPU core.
> 
> Scheduling policies are divided into two major categories:
> 
> 1.  Realtime policies 
>     *   SCHED_FIFO
>     *   SCHED_RR
> 2.  Normal policies 
>     *   SCHED_OTHER
>     *   SCHED_BATCH
>     *   SCHED_IDLE
> 
> **4.2.1. Realtime scheduling policies**  
> Realtime threads are scheduled first, and normal threads are scheduled after all realtime threads have been scheduled.
> 
> The realtime policies are used for time-critical tasks that must complete without interruptions.
> 
> **SCHED_FIFO**
> 
> *   This policy is also referred to as static priority scheduling, because it defines a fixed priority (between 1 and 99) for each thread. The scheduler scans a list of SCHED_FIFO threads in priority order and schedules the highest priority thread that is ready to run. This thread runs until it blocks, exits, or is preempted by a higher priority thread that is ready to run.  
>     Even the lowest priority realtime thread will be scheduled ahead of any thread with a non-realtime policy; if only one realtime thread exists, the SCHED_FIFO priority value does not matter.
> 
> **SCHED_RR**
> 
> *   A round-robin variant of the SCHED&#95;FIFO policy. SCHED&#95;RR threads are also given a fixed priority between 1 and 99. However, threads with the same priority are scheduled round-robin style within a certain quantum, or time slice. The **sched&#95;rr&#95;get_interval**(2) system call returns the value of the time slice, but the duration of the time slice cannot be set by a user. This policy is useful if you need multiple thread to run at the same priority.
> 
> Best practice in defining thread priority is to start low and increase priority only when a legitimate latency is identified. Realtime threads are not time-sliced like normal threads; **SCHED_FIFO** threads run until they block, exit, or are pre-empted by a thread with a higher priority. Setting a priority of 99 is therefore not recommended, as this places your process at the same priority level as migration and watchdog threads. If these threads are blocked because your thread goes into a computational loop, they will not be able to run. Uniprocessor systems will eventually lock up in this situation.
> 
> In the Linux kernel, the **SCHED_FIFO** policy includes a bandwidth cap mechanism. This protects realtime application programmers from realtime tasks that might monopolize the CPU. This mechanism can be adjusted through the following /proc file system parameters:
> 
> *   **/proc/sys/kernel/sched&#95;rt&#95;period_us** Defines the time period to be considered one hundred percent of CPU bandwidth, in microseconds ('us' being the closest equivalent to 'µs' in plain text). The default value is 1000000µs, or 1 second.
> *   **/proc/sys/kernel/sched&#95;rt&#95;runtime_us** Defines the time period to be devoted to running realtime threads, in microseconds ('us' being the closest equivalent to 'µs' in plain text). The default value is 950000µs, or 0.95 seconds.
> 
> **4.2.2. Normal scheduling policies**  
> There are three normal scheduling policies: **SCHED_OTHER**, **SCHED_BATCH** and **SCHED_IDLE**. However, the **SCHED_BATCH** and **SCHED_IDLE** policies are intended for very low priority jobs, and as such are of limited interest in a performance tuning guide.
> 
> *   **SCHED&#95;OTHER, or SCHED&#95;NORMAL** The default scheduling policy. This policy uses the Completely Fair Scheduler (CFS) to provide fair access periods for all threads using this policy. CFS establishes a dynamic priority list partly based on the niceness value of each process thread. This gives users some indirect level of control over process priority, but the dynamic priority list can only be directly changed by the CFS.

There was actually a little bit more info from <a href="http://doc.opensuse.org/documentation/html/openSUSE/opensuse-tuning/part.tuning.kernel.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://doc.opensuse.org/documentation/html/openSUSE/opensuse-tuning/part.tuning.kernel.html']);">Part V. Kernel Tuning</a>:

> **14.4.5. Changing Real-time Attributes of Processes with chrt**  
> The **chrt** command sets or retrieves the real-time scheduling attributes of a running process, or runs a command with the specified attributes. You can get or retrieve both the scheduling policy and priority of a process.
> 
> In the following examples, a process whose PID is 16244 is used.
> 
> To retrieve the real-time attributes of an existing task:
> 
>     saturn.example.com:~ # chrt -p 16244
>     pid 16244's current scheduling policy: SCHED_OTHER
>     pid 16244's current scheduling priority: 0
>     
> 
> Before setting a new scheduling policy on the process, you need to find out the minimum and maximum valid priorities for each scheduling algorithm:
> 
>     saturn.example.com:~ # chrt -m
>     SCHED_OTHER min/max priority : 0/0
>     SCHED_FIFO min/max priority : 1/99
>     SCHED_RR min/max priority : 1/99
>     SCHED_BATCH min/max priority : 0/0
>     SCHED_IDLE min/max priority : 0/0
>     
> 
> In the above example, SCHED&#95;OTHER, SCHED&#95;BATCH, SCHED&#95;IDLE polices only allow for priority 0, while that of SCHED&#95;FIFO and SCHED_RR can range from 1 to 99.
> 
> To set SCHED_BATCH scheduling policy:
> 
>     saturn.example.com:~ # chrt -b -p 0 16244
>     saturn.example.com:~ # chrt -p 16244
>     pid 16244's current scheduling policy: SCHED_BATCH
>     pid 16244's current scheduling priority: 0
>     

#### Tuning the CPU Scheduler

From the same page:

> **14.4.6. Runtime Tuning with sysctl**  
> The sysctl interface for examining and changing kernel parameters at runtime introduces important variables by means of which you can change the default behavior of the task scheduler. The syntax of the sysctl is simple, and all the following commands must be entered on the command line as root.
> 
> To read a value from a kernel variable, enter
> 
>     sysctl variable
>     
> 
> To assign a value, enter
> 
>     sysctl variable=value
>     
> 
> To get a list of all scheduler related sysctl variables, enter
> 
>     saturn.example.com:~ # sysctl -A | grep "sched" | grep -v "domain"
>     kernel.sched_child_runs_first = 0
>     kernel.sched_min_granularity_ns = 1000000
>     kernel.sched_latency_ns = 5000000
>     kernel.sched_wakeup_granularity_ns = 1000000
>     kernel.sched_shares_ratelimit = 250000
>     kernel.sched_tunable_scaling = 1
>     kernel.sched_shares_thresh = 4
>     kernel.sched_features = 15834238
>     kernel.sched_migration_cost = 500000
>     kernel.sched_nr_migrate = 32
>     kernel.sched_time_avg = 1000
>     kernel.sched_rt_period_us = 1000000
>     kernel.sched_rt_runtime_us = 950000
>     kernel.sched_compat_yield = 0
>     
> 
> Note that variables ending with “&#95;ns” and “&#95;us” accept values in nanoseconds and microseconds, respectively.
> 
> A list of the most important task scheduler **sysctl** tuning variables (located at **/proc/sys/kernel/**) with a short description follows:
> 
> *   **sched&#95;child&#95;runs_first** A freshly forked child runs before the parent continues execution. Setting this parameter to 1 is beneficial for an application in which the child performs an execution after fork. For example make -j NO&#95;CPUS performs better when sched&#95;child&#95;runs&#95;first is turned off. The default value is 0.
> *   **sched&#95;compat&#95;yield** Enables the aggressive yield behavior of the old 0(1) scheduler. Java applications that use synchronization extensively perform better with this value set to 1. Only use it when you see a drop in performance. The default value is 0.  
>     Expect applications that depend on the sched_yield() syscall behavior to perform better with the value set to 1.
> *   **sched&#95;migration&#95;cost** Amount of time after the last execution that a task is considered to be “cache hot” in migration decisions. A “hot” task is less likely to be migrated, so increasing this variable reduces task migrations. The default value is 500000 (ns).  
>     If the CPU idle time is higher than expected when there are runnable processes, try reducing this value. If tasks bounce between CPUs or nodes too often, try increasing it. **sched&#95;latency&#95;ns** Targeted preemption latency for CPU bound tasks. Increasing this variable increases a CPU bound task's timeslice. A task's timeslice is its weighted fair share of the scheduling period:  
>     timeslice = scheduling period * (task's weight/total weight of tasks in the run queue)  
>     The task's weight depends on the task's nice level and the scheduling policy. Minimum task weight for a SCHED_OTHER task is 15, corresponding to nice 19. The maximum task weight is 88761, corresponding to nice -20.  
>     Timeslices become smaller as the load increases. When the number of runnable tasks exceeds **sched&#95;latency&#95;ns/sched&#95;min&#95;granularity_ns**, the slice becomes **number&#95;of&#95;running&#95;tasks x sched&#95;min&#95;granularity&#95;ns**. Prior to that, the slice is equal to sched&#95;latency&#95;ns.  
>     This value also specifies the maximum amount of time during which a sleeping task is considered to be running for entitlement calculations. Increasing this variable increases the amount of time a waking task may consume before being preempted, thus increasing scheduler latency for CPU bound tasks. The default value is 20000000 (ns).
> *   **sched&#95;min&#95;granularity_ns** Minimal preemption granularity for CPU bound tasks. See **sched&#95;latency&#95;ns** for details. The default value is 4000000 (ns).
> *   **sched&#95;wakeup&#95;granularity_ns** The wake-up preemption granularity. Increasing this variable reduces wake-up preemption, reducing disturbance of compute bound tasks. Lowering it improves wake-up latency and throughput for latency critical tasks, particularly when a short duty cycle load component must compete with CPU bound components. The default value is 5000000 (ns).
> *   **sched&#95;rt&#95;period_us** Period over which real-time task bandwidth enforcement is measured. The default value is 1000000 (µs).
> *   **sched&#95;rt&#95;runtime_us** Quantum allocated to real-time tasks during sched&#95;rt&#95;period&#95;us. Setting to -1 disables RT bandwidth enforcement. By default, RT tasks may consume 95%CPU/sec, thus leaving 5%CPU/sec or 0.05s to be used by SCHED&#95;OTHER tasks.
> *   **sched_features** Provides information about specific debugging features.
> *   **sched&#95;stat&#95;granularity_ns** Specifies the granularity for collecting task scheduler statistics.
> *   **sched&#95;nr&#95;migrate** Controls how many tasks can be moved across processors through migration software interrupts (softirq). If a large number of tasks is created by SCHED&#95;OTHER policy, they will all be run on the same processor. The default value is 32. Increasing this value gives a performance boost to large SCHED&#95;OTHER threads at the expense of increased latencies for real-time tasks.

### RHEL Memory Management

From this pretty old RHEL document entitled <a href="http://people.redhat.com/nhorman/papers/rhel4_vm.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://people.redhat.com/nhorman/papers/rhel4_vm.pdf']);">Understanding Virtual Memory</a>

> **Introduction**  
> One of the most important aspects of an operating system is the Virtual Memory Management system. Virtual Memory (VM) allows an operating system to perform many of its advanced functions, such as process isolation, ﬁle caching, and swapping. As such, it is imperative that an administrator understand the functions and tunable parameters of an operating system’s virtual memory manager so that optimal performance for a given workload may be achieved. This article is intended to provide a system administrator a general overview of how a VM works, speciﬁcally the VM implemented in Red Hat Enterprise Linux 4 (RHEL4). After reading this document, the reader should have a rudimentary understanding of the data the RHEL4 VM controls and the algorithms it uses. Further, the reader should have a fairly good understanding of general Linux VM tuning techniques. It is important to note that Linux as an operating system has a proud legacy of overhaul. Items which no longer serve useful purposes or which have better implementations as technology advances are phased out. This implies that the tuning parameters described in this article may be out of date if you are using a newer or older kernel. This is particularly true of this release of Red Hat Enterprise Linux, as it is the ﬁrst RHEL release making use of the 2.6 kernel series. Fear not however! With a well grounded understanding of the general mechanics of a VM, it is fairly easy to convert ones knowledge of VM tuning to another VM
> 
> **Definitions**  
> To properly understand how a Virtual Memory Manager does its job, it helps to understand what components comprise a VM. While the low level details of a VM are overwhelming for most, a high level view is nonetheless helpful in understanding how a VM works, and how it can be optimized for various workloads. A high level overview of the components that make up a Virtual memory manager is presented in Figure 1 below:
> 
> **What Comprises a VM** <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/virtual_mem.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/virtual_mem.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/virtual_mem.png" alt="virtual mem RHCSA and RHCE Chapter 10   The Kernel" width="589" height="506" class="alignnone size-full wp-image-9105" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **2.3 Zoned Buddy Allocator**  
> The Zoned Buddy Allocator is responsible for the management of page allocations to the entire system. This code manages lists of physically contiguous pages and maps them into the MMU page tables, so as to provide other kernel subsystems with valid physical address ranges when the kernel requests them (Physical to Virtual Address mapping is handled by a higher layer of the VM and is collapsed into the kernel subsystems block of Figure 1 ). The name Buddy Allocator is derived from the algorithm this subsystem uses to maintain it free page lists. All physical pages in RAM are cataloged by the buddy allocator and grouped into lists. Each list represents clusters of 2n pages, where n is incremented in each list. There is a list of single pages, a list of 2 page clusters, a list of 4 page cluster, and so on. When a request comes in for an amount of memory, that value is rounded up to the nearest power of 2, and a entry is removed from the appropriate list, registered in the page tables of the MMU and a corresponding physical address is returned to the caller, which is then mapped into a virtual address for kernel use. If no entries exist on the requested list, an entry from the next list up is broken into two separate clusters, and 1 is returned to the caller while the other is added to the next list down. When an allocation is returned to the buddy allocator, the reverse process happens. The allocation is returned to the requisite list, and the list is then examined to determine if a larger cluster can be made from the existing entries on the list which was just updated. This algorithm is advantageous in that it automatically returns pages to the highest order free list possible. That is to say, as allocations are returned to the free pool, they automatically form larger clusters, so that when a need arises for a large amount of physically contiguous memory (i.e. for a DMA operation), it is more likely that the request can be satisﬁed. Note that the buddy allocator allocates memory in page multiples only. Other subsystems are responsible for ﬁner grained control over allocation size. For more information regarding the ﬁner details of a buddy allocator, refer to <a href="http://www.tldp.org/LDP/sag/html/kernel-parts.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.tldp.org/LDP/sag/html/kernel-parts.html']);">1</a>. Note that the Buddy allocator also manages memory zones, which deﬁne pools of memory which have diﬀerent purposes. Currently there are three memory pools which the buddy allocator manages accesses for:
> 
> *   **DMA** - This zone consists of the ﬁrst 16 MB of RAM, from which legacy devices allocate to perform direct memory operations
> *   **NORMAL** - This zone encompasses memory addresses from 16 MB to 1 GB2 and is used by the kernel for internal data structures, as well as other system and user space allocations.
> *   **HIGHMEM** - This zone includes all memory above 1 GB and is used exclusively for system allocations (ﬁle system buﬀers, user space allocations, etc).
> 
> **2.4 Slab Allocator**  
> The Slab Allocator provides a more usable front end to the Buddy Allocator for those sections of the kernel which require memory in sizes that are more ﬂexible than the standard 4 KB page. The Slab Allocator allows other kernel components to create caches of memory objects of a given size. The Slab Allocator is responsible for placing as many of the caches objects on a page as possible and monitoring which objects are free and which are allocated. When allocations are requested and no more are available, the Slab Allocator requests more pages from the Buddy Allocator to satisfy the request.This allows kernel components to use memory in a much simpler way. This way components which make use of many small portions of memory are not required to individually implement memory management code so that too many pages are not wasted
> 
> **2.5 Kernel Threads**  
> The last component in the VM subsystem are the active tasks: **kswapd**, and **pdﬂush**. These tasks are responsible for the recovery and management of in use memory. All pages of memory have an associated state (for more info on the memory state machine, refer to section 3). These two tasks are responsible for the management of swap and pagecache respectively. **Kswapd** periodically scans all **pgdat** structures in the kernel, looking for dirty pages to write out to swap space. It does this in an eﬀort to keep the number of free and clean pages above pre-calculated safe thresholds. Likewise the pdﬂush daemon is responsible for managing the migration of cached ﬁle system data to its backing store on disk. As system load increases, the eﬀective priority of the pdﬂush daemons likewise increase to continue to keep free memory at safe levels, subject to the VM tunables described in section
> 
> **3 The Life of A Page**  
> All of the memory managed by the VM is labeled by a state. These states help let the VM know what to do with a given page under various circumstances. Dependent on the current needs of the system, the VM may transfer pages from one state to the next, according to the state machine diagrammed in ﬁgure 3 below: 6 Using these states, the VM can determine what is being done with a page by the system at a given time and what actions it (the VM) may take on the page. The states that have particular meanings are as follows:
> 
> *   **FREE** - All pages available for allocation begin in this state. This indicates to the VM that the page is not being used for any purpose and is available for allocation.
> *   **ACTIVE** - Pages which have been allocated from the Buddy Allocator enter this state. It indicates to the VM that the page has been allocated and is actively in use by the kernel or a user process.
> *   **INACTIVE DIRTY** - Th state indicates that the page has fallen into disuse by the entity which allocated it, and as such is a candidate for removal from main memory. The **kscand** task periodically sweeps through all the pages in memory Taking note of the amount of time the page has been in memory since it was last accessed. If kscand ﬁnds that a page has been accessed since it last visited the page, it increments the pages age counter, otherwise, it decrements that counter. If **kscand** happens on a page which has its age counter at zero, then the page is moved to the inactive dirty state. Pages in the inactive dirty state are kept in a list of pages to be laundered.
> *   **INACTIVE CLEAN** - Pages in this state have been laundered. This means that the contents of the page are in sync with they backing data on disk. As such they may be deallocated by the VM or overwritten for other purposes.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/vm_page_states.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/vm_page_states.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/vm_page_states.png" alt="vm page states RHCSA and RHCE Chapter 10   The Kernel" width="450" height="487" class="alignnone size-full wp-image-9106" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>

Another concise summary is seen at <a href="http://www.redbooks.ibm.com/redpapers/pdfs/redp4285.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.redbooks.ibm.com/redpapers/pdfs/redp4285.pdf']);">Linux Performance and Tuning Guidelines</a>:

> **1.2 Linux memory architecture**  
> To execute a process, the Linux kernel allocates a portion of the memory area to the requesting process. The process uses the memory area as workspace and performs the required work. It is similar to you having your own desk allocated and then using the desktop to scatter papers, documents and memos to perform your work. The difference is that the kernel has to allocate space in a more dynamic manner. The number of running processes sometimes comes to tens of thousands and amount of memory is usually limited. Therefore, Linux kernel must handle the memory efficiently. In this section, we describe the Linux memory architecture, address layout, and how Linux manages memory space efficiently.
> 
> **1.2.1 Physical and virtual memory**  
> Today we are faced with the choice of 32-bit systems and 64-bit systems. One of the most important differences for enterprise-class clients is the possibility of virtual memory addressing above 4 GB. From a performance point of view, it is interesting to understand how the Linux kernel maps physical memory into virtual memory on both 32-bit and 64-bit systems.
> 
> As you can see in Figure 1-10 on page 11, there are obvious differences in the way the Linux kernel has to address memory in 32-bit and 64-bit systems. Exploring the physical-to-virtual mapping in detail is beyond the scope of this paper, so we highlight some specifics in the Linux memory architecture.
> 
> On 32-bit architectures such as the IA-32, the Linux kernel can directly address only the first gigabyte of physical memory (896 MB when considering the reserved range). Memory above the so-called ZONE&#95;NORMAL must be mapped into the lower 1 GB. This mapping is completely transparent to applications, but allocating a memory page in ZONE&#95;HIGHMEM causes a small performance degradation.
> 
> On the other hand, with 64-bit architectures such as x86-64 (also x64), ZONE&#95;NORMAL extends all the way to 64 GB or to 128 GB in the case of IA-64 systems. As you can see, the overhead of mapping memory pages from ZONE&#95;HIGHMEM into ZONE_NORMAL can be eliminated by using a 64-bit architecture.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_zones.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_zones.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_zones.png" alt="memory zones RHCSA and RHCE Chapter 10   The Kernel" width="502" height="406" class="alignnone size-full wp-image-9107" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **Virtual memory addressing layout**  
> Figure 1-11 shows the Linux virtual addressing layout for 32-bit and 64-bit architecture.
> 
> On 32-bit architectures, the maximum address space that single process can access is 4GB. This is a restriction derived from 32-bit virtual addressing. In a standard implementation, the virtual address space is divided into a 3 GB user space and a 1 GB kernel space. There is some variants like 4 G/4 G addressing layout implementing.
> 
> On the other hand, on 64-bit architecture such as x86_64 and ia64, no such restriction exits. Each single process can benefit from the vast and huge address space.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_addressing.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_addressing.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_addressing.png" alt="memory addressing RHCSA and RHCE Chapter 10   The Kernel" width="530" height="259" class="alignnone size-full wp-image-9108" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **1.2.2 Virtual memory manager**  
> The physical memory architecture of an operating system is usually hidden to the application and the user because operating systems map any memory into virtual memory. If we want to understand the tuning possibilities within the Linux operating system, we have to understand how Linux handles virtual memory. As explained in 1.2.1, “Physical and virtual memory” on page 10, applications do not allocate physical memory, but request a memory map of a certain size at the Linux kernel and in exchange receive a map in virtual memory. As you can see in Figure 1-12, virtual memory does not necessarily have to be mapped into physical memory. If your application allocates a large amount of memory, some of it might be mapped to the swap file on the disk subsystem
> 
> Figure 1-12 shows that applications usually do not write directly to the disk subsystem, but into cache or buffers. The pdflush kernel threads then flushes out data in cache/buffers to the disk when it has time to do so or if a file size exceeds the buffer cache. Refer to “Flushing a dirty buffer” on page 22.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/linux_vmm.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/linux_vmm.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/linux_vmm.png" alt="linux vmm RHCSA and RHCE Chapter 10   The Kernel" width="558" height="382" class="alignnone size-full wp-image-9109" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> Closely connected to the way the Linux kernel handles writes to the physical disk subsystem is the way the Linux kernel manages disk cache. While other operating systems allocate only a certain portion of memory as disk cache, Linux handles the memory resource far more efficiently. The default configuration of the virtual memory manager allocates all available free memory space as disk cache. Hence it is not unusual to see productive Linux systems that boast gigabytes of memory but only have 20 MB of that memory free.
> 
> In the same context, Linux also handles swap space very efficiently. Swap space being used does not indicate a memory bottleneck but proves how efficiently Linux handles system resources. See “Page frame reclaiming” on page 14 for more detail.
> 
> **Page frame allocation**  
> A page is a group of contiguous linear addresses in physical memory (page frame) or virtual memory. The Linux kernel handles memory with this page unit. A page is usually 4 K bytes in size. When a process requests a certain amount of pages, if there are available pages the Linux kernel can allocate them to the process immediately. Otherwise pages have to be taken from some other process or page cache. The kernel knows how many memory pages are available and where they are located.
> 
> Buddy system The Linux kernel maintains its free pages by using a mechanism called a buddy system. The buddy system maintains free pages and tries to allocate pages for page allocation requests. It tries to keep the memory area contiguous. If small pages are scattered without consideration, it might cause memory fragmentation and it’s more difficult to allocate a large portion of pages into a contiguous area. It could lead to inefficient memory use and performance decline. Figure 1-13 illustrates how the buddy system allocates pages.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_buddy_system.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_buddy_system.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/memory_buddy_system.png" alt="memory buddy system RHCSA and RHCE Chapter 10   The Kernel" width="560" height="187" class="alignnone size-full wp-image-9110" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> When the attempt of pages allocation fails, the page reclaiming is activated. Refer to “Page frame reclaiming” on page 14.
> 
> You can find information on the buddy system through **/proc/buddyinfo**.
> 
> **Page frame reclaiming**  
> If pages are not available when a process requests to map a certain amount of pages, the Linux kernel tries to get pages for the new request by releasing certain pages (which were used before but are not used anymore and are still marked as active pages based on certain principles) and allocating the memory to a new process. This process is called page reclaiming. kswapd kernel thread and try&#95;to&#95;free_page() kernel function are responsible for page reclaiming.
> 
> While kswapd is usually sleeping in task interruptible state, it is called by the buddy system when free pages in a zone fall short of a threshold. It tries to find the candidate pages to be taken out of active pages based on the Least Recently Used (LRU) principle. The pages least recently used should be released first. The active list and the inactive list are used to maintain the candidate pages. kswapd scans part of the active list and check how recently the pages were used and the pages not used recently are put into the inactive list. You can take a look at how much memory is considered as active and inactive using the vmstat -a command.
> 
> kswapd also follows another principle. The pages are used mainly for two purposes: page cache and process address space. The page cache is pages mapped to a file on disk. The pages that belong to a process address space (called anonymous memory because it is not mapped to any files, and it has no name) are used for heap and stack. Refer to 1.1.8, “Process memory segments” on page 8. When kswapd reclaims pages, it would rather shrink the page cache than page out (or swap out) the pages owned by processes.
> 
> **NOTE** Page out and swap out: The phrases “page out” and “swap out” are sometimes confusing. The phrase “page out” means take some pages (a part of entire address space) into swap space while “swap out” means taking entire address space into swap space. They are sometimes used interchangeably.
> 
> A large proportion of page cache that is reclaimed and process address space that is reclaimed might depend on the usage scenario and will affect performance. You can take some control of this behavior by using **/proc/sys/vm/swappiness**
> 
> **swap**  
> As we stated before, when page reclaiming occurs, the candidate pages in the inactive list which belong to the process address space may be paged out. Having swap itself is not problematic situation. While swap is nothing more than a guarantee in case of over allocation of main memory in other operating systems, Linux uses swap space far more efficiently. As you can see in Figure 1-12 on page 13, virtual memory is composed of both physical memory and the disk subsystem or the swap partition. If the virtual memory manager in Linux realizes that a memory page has been allocated but not used for a significant amount of time, it moves this memory page to swap space.
> 
> Often you will see daemons such as getty that will be launched when the system starts up but will hardly ever be used. It appears that it would be more efficient to free the expensive main memory of such a page and move the memory page to swap. This is exactly how Linux handles swap, so there is no need to be alarmed if you find the swap partition filled to 50%. The fact that swap space is being used does not indicate a memory bottleneck; instead it proves how efficiently Linux handles system resources.

### Tuning Memory Management

From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_MRG/2/pdf/Realtime_Tuning_Guide/Red_Hat_Enterprise_MRG-2-Realtime_Tuning_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_MRG/2/pdf/Realtime_Tuning_Guide/Red_Hat_Enterprise_MRG-2-Realtime_Tuning_Guide-en-US.pdf']);">Realtime Tuning Guide</a>:

> **2.8. Swapping and Out Of Memory Tips**
> 
> **Memory Swapping**  
> Swapping pages out to disk can introduce latency in any environment. To ensure low latency, the best strategy is to have enough memory in your systems so that swapping is not necessary. Always size the physical RAM as appropriate for your application and system. Use **vmstat** to monitor memory usage and watch the si (swap in) and so (swap out) fields. They should remain on zero as much as possible.
> 
> **Out of Memory (OOM)**  
> Out of Memory (OOM) refers to a computing state where all available memory, including swap space, has been allocated. Normally this will cause the system to panic and stop functioning as expected. There is a switch that controls OOM behavior in **/proc/sys/vm/panic&#95;on&#95;oom**. When set to **1** the kernel will panic on OOM. A setting of **O** instructs the kernel to call a function named **oom_killer** on an OOM. Usually, **oom_killer** can kill rogue processes and the system will survive.
> 
> 1.  The easiest way to change this is to echo the new value to **/proc/sys/vm/panic&#95;on&#95;oom**.
>     
>         # cat /proc/sys/vm/panic_on_oom
>         1
>         #  echo 0 > /proc/sys/vm/panic_on_oom
>         # cat /proc/sys/vm/panic_on_oom
>         0
>         
> 
> 2.  It is also possible to prioritize which processes get killed by adjusting the **oom_killer** score. In **/proc/PID/** there are two tools labelled **oom_adj** and **oom_score**. Valid scores for **oom_adj** are in the range -16 to +15. This value is used to calculate the 'badness' of the process using an algorithm that also takes into account how long the process has been running, amongst other factors. To see the current **oom_killer** score, view the **oom_score** for the process. **oom_killer** will kill processes with the highest scores first.  
>     This example adjusts the **oom_score** of a process with a PID of 12465 to make it less likely that **oom_killer** will kill it.
>     
>         # cat /proc/12465/oom_score 
>         79872
>         # echo -5 > /proc/12465/oom_adj
>         # cat /proc/12465/oom_score
>         78
>         
> 
> 3.  There is also a special value of -17, which disables oom&#95;killer for that process. In the example below, oom&#95;score returns a value of O, indicating that this process would not be killed.
>     
>         # cat /proc/12465/oom_score
>         78
>         # echo -17 > /proc/12465/oom_adj
>         # cat /proc/12465/oom_score
>         0
>         

From the <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Performance_Tuning_Guide/Red_Hat_Enterprise_Linux-6-Performance_Tuning_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Performance_Tuning_Guide/Red_Hat_Enterprise_Linux-6-Performance_Tuning_Guide-en-US.pdf']);">Performance Tuning Guide</a>:

> **5.2. Huge Pages and Transparent Huge Pages**  
> Memory is managed in blocks known as pages. A page is 4096 bytes. 1MB of memory is equal to 256 pages; 1GB of memory is equal to 256,000 pages, etc. CPUs have a built-in *memory management unit* that contains a list of these pages, with each page referenced through a page table entry.
> 
> There are two ways to enable the system to manage large amounts of memory:
> 
> *   Increase the number of page table entries in the hardware memory management unit
> *   Increase the page size
> 
> The first method is expensive, since the hardware memory management unit in a modern processor only supports hundreds or thousands of page table entries. Additionally, hardware and memory management algorithms that work well with thousands of pages (megabytes of memory) may have difficulty performing well with millions (or even billions) of pages. This results in performance issues: when an application needs to use more memory pages than the memory management unit supports, the system falls back to slower, software-based memory management, which causes the entire system to run more slowly.
> 
> Red Hat Enterprise Linux 6 implements the second method via the use of **huge pages**.
> 
> Simply put, huge pages are blocks of memory that come in 2MB and 1GB sizes. The page tables used by the 2MB pages are suitable for managing multiple gigabytes of memory, whereas the page tables of 1GB pages are best for scaling to terabytes of memory.
> 
> Huge pages must be assigned at boot time. They are also difficult to manage manually, and often require significant changes to code in order to be used effectively. As such, Red Hat Enterprise Linux 6 also implemented the use of transparent huge pages (THP). THP is an abstraction layer that automates most aspects of creating, managing, and using huge pages.
> 
> THP hides much of the complexity in using huge pages from system administrators and developers. As the goal of THP is improving performance, its developers (both from the community and Red Hat) have tested and optimized THP across a wide range of systems, configurations, applications, and workloads. This allows the default settings of THP to improve the performance of most system configurations.
> 
> Note that THP can currently only map anonymous memory regions such as heap and stack space.

Here are some actual tuning parameters:

> **5.4. Capacity Tuning**  
> Read this section for an outline of memory, kernel and file system capacity, the parameters related to each, and the trade-offs involved in adjusting these parameters.
> 
> To set these values temporarily during tuning, echo the desired value to the appropriate file in the proc file system. For example, to set **overcommit_memory** temporarily to 1, run:
> 
>     # echo 1 > /proc/sys/vm/overcommit_memory
>     
> 
> Note that the path to the parameter in the proc file system varies depending on the system affected by the change.
> 
> **Capacity-related Memory Tunables**  
> Each of the following parameters is located under **/proc/sys/vm/** in the proc file system.
> 
> **overcommit_memory** Defines the conditions that determine whether a large memory request is accepted or denied. There are three possible values for this parameter:
> 
> *   **O** — The default setting. The kernel performs heuristic memory overcommit handling by estimating the amount of memory available and failing requests that are blatantly invalid. Unfortunately, since memory is allocated using a heuristic rather than a precise algorithm, this setting can sometimes allow available memory on the system to be overloaded.
> *   **1** — The kernel performs no memory overcommit handling. Under this setting, the potential for memory overload is increased, but so is performance for memory-intensive tasks.
> *   **2** — The kernel denies requests for memory equal to or larger than the sum of total available swap and the percentage of physical RAM specified in **overcommit_ratio**. This setting is best if you want a lesser risk of memory overcommitment.
> 
> **overcommit_ratio** Specifies the percentage of physical RAM considered when **overcommit_memory** is set to **2**. The default value is **50**.
> 
> **max&#95;map&#95;count** Defines the maximum number of memory map areas that a process may use. In most cases, the default value of **65530** is appropriate. Increase this value if your application needs to map more than this number of files.
> 
> **nr_hugepages** Defines the number of hugepages configured in the kernel. The default value is 0. It is only possible to allocate (or deallocate) hugepages if there are sufficient physically contiguous free pages in the system. Pages reserved by this parameter cannot be used for other purposes.
> 
> **5.5. Tuning Virtual Memory**  
> Virtual memory is typically consumed by processes, file system caches, and the kernel. Virtual memory utilization depends on a number of factors, which can be affected by the following parameters:
> 
> **swappiness** A value from 0 to 100 which controls the degree to which the system swaps. A high value prioritizes system performance, aggressively swapping processes out of physical memory when they are not active. A low value prioritizes interactivity and avoids swapping processes out of physical memory for as long as possible, which decreases response latency. The default value is **60**.
> 
> **min&#95;free&#95;kbytes** The minimum number of kilobytes to keep free across the system. This value is used to compute a watermark value for each low memory zone, which are then assigned a number of reserved free pages proportional to their size.
> 
> **dirty_ratio** Defines a percentage value. Writeout of dirty data begins (via **pdflush**) when dirty data comprises this percentage of total system memory. The default value is **20**.
> 
> **dirty&#95;background&#95;ratio** Defines a percentage value. Writeout of dirty data begins in the background (via **pdflush**) when dirty data comprises this percentage of total memory. The default value is **10**.
> 
> **drop_caches** Setting this value to **1**, **2**, or **3** causes the kernel to drop various combinations of page cache and slab cache.
> 
> *   **1** The system invalidates and frees all page cache memory.
> *   **2** The system frees all unused slab cache memory.
> *   **3** The system frees all page cache and slab cache memory.
> 
> This is a non-destructive operation. Since dirty objects cannot be freed, running **sync** before setting this parameter's value is recommended.

More tuning from the original paper:

> **4 Tuning the VM**  
> Now that the picture of the VM mechanism is suﬃciently illustrated, how is it adjusted to ﬁt certain workloads? There are two methods for changing tunable parameters in the Linux VM. The ﬁrst is the **sysctl** interface. The **sysctl** interface is a programming oriented interface, which allows software programs to directly modify various tunable parameters. The **sysctl** interface is exported to system administrators via the sysctl utility, which allows an administrator to specify a speciﬁc value for any of the tunable VM parameters on the command line, as in the following example:
> 
>     sysctl -w vm.max map count=65535
>     
> 
> The sysctl utility also supports the use of a conﬁguration ﬁle (**/etc/sysctl.conf**), in which all the desirable changes to a VM can be recorded for a system and restored after a restart of the operating system, making this access method suitable for long term changes to a system VM. The ﬁle is straightforward in its layout, using simple key-value pairs, with comments for clarity, as in the following example:
> 
>     #Adjust the number of available hugepages 
>     vm.nr hugepages=64
>     #turn on memory over-commit 
>     vm.overcommit memory=2
>     #bump up the number of pdﬂush threads 
>     vm.nr pdﬂush threads=2
>     
> 
> The second method of modifying VM tunable parameters is via the proc ﬁle system. This method exports every group of VM tunables as a ﬁle, accessible via all the common Linux utilities used for modify ﬁle contents. The VM tunables are available in the directory /proc/sys/vm, and are most commonly read and modiﬁed using the Linux cat and echo utilities, as in the following example:
> 
>     # cat swappiness
>     60
>     echo 70 > /proc/sys/vm/swappiness
>     # cat /proc/sys/vm/swappiness
>     70
>     
> 
> The proc ﬁle system interface is a convenient method for making adjustments to the VM while attempting to isolate the peak performance of a system. For convenience, the following sections list the VM tunable parameters as the ﬁlenames they are exported as in **/proc/sys/vm**

Here are some generic trouble shooting steps from this <a href="http://wiki.deimos.fr/images/8/89/Memory_management_and_tuning_options_in_Red_Hat_Enterprise_Linux.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://wiki.deimos.fr/images/8/89/Memory_management_and_tuning_options_in_Red_Hat_Enterprise_Linux.pdf']);">RHEL</a> page:

> **LowMem Starvation**  
> Memory usage on 32-bit system can become problematic under some workloads, especially for I/O intensive applications such as:
> 
> *   Oracle Database or Application Server
> *   Java
> *   With the x86 architecture the first 16MB-896MB of physical memory is known as "low memory" (ZONE_NORMAL) which is permanently mapped into kernel space. Many kernel resources must live in the low memory zone. In fact, many kernel operations can only take place in this zone. This means that the low memory area is the most performance critical zone. For example, if you run many resources intensive applications/programs and/or use large physical memory, then "low memory" can become low since more kernel structures must be allocated in this area. Under heavy I/O workloads the kernel may become starved for LowMem even though there is an abundance of available HighMem. As the kernel tries to keep as much data in cache as possible this can lead to oom-killers or complete system hangs.
> *   In 64-bit systems all the memory is allocated in ZONE_NORMAL. So lowmem starvation will not affect 64-bit systems. Moving to 64-bit would be a permanent fix for lowmem starvation.
> 
> **Diagnosing**  
> The amount of LowMem can be checked in **/proc/meminfo**. If the LowFree falls below 50Mb it may be cause for concern. However this does not always indicate a problem as the kernel will try to use the entire LowMem zone and it may be able to reclaim some of the cache.
> 
>     MemTotal: 502784 kB
>     MemFree: 29128 kB
>     HighTotal: 162088 kB
>     HighFree: 22860 kB
>     LowTotal: 340696 kB
>     LowFree: 6268 kB
>     
> 
> **OOM-KILLER**  
> the kernel should print sysrq-M information to messages and the console. You may see the Normal zone reporting all_unreclaimable? yes, meaning the kernel could not reclaim any memory in this zone.
> 
>     Aug 25 15:44:24 dompar158 kernel: DMA free:12544kB min:16kB low:32kB high:48kB ac
>     Aug 25 15:44:24 dompar158 kernel: Normal free:888kB min:928kB low:1856kB high:278
>     Aug 25 15:44:24 dompar158 kernel: HighMem free:8731264kB min:512kB low:1024kB hig
>     
> 
> In this case we can also see that the largest contiguous block of memory in the LowMem range is 32kB, so if the kernel requires anything larger than that the allocation may fail.
> 
>     Aug 25 15:44:24 dompar158 kernel: DMA: 4*4kB 4*8kB 3*16kB 3*32kB 3*64kB 3*128kB 2
>     Aug 25 15:44:24 dompar158 kernel: Normal: 80*4kB 18*kB 29*16kB 3*32kB 0*64kB 0*12
>     Aug 25 15:44:24 dompar158 kernel: HighMem: 660*4kB 160*8kB 61*16kB 55*32kB 496*64
>     
> 
> **Tuning Sysctl**
> 
> *   **RHEL 5 and 6** Attempt to protect approximately 1/9 (98Mb) of LowMem from userspace allocations (defaults to 1/32, or 27.5 Mb)
>     
>         vm.lowmem_reserve_ratio=256 256 9
>         
> 
> *   **RHEL 4, 5 and 6** Have a higher tendency to swap out to disk. This value can go from 0 to 100 (default 60). Setting below 10 is not recommended
>     
>         vm.swappiness=80
>         
> 
> *   Try to keep at least 19Mb of memory free (default varies). Adjust this to something higher than what is currently in use
>     
>         vm.min_free_kbytes=19000
>         
> 
> *   Decrease the amount of time for a page to be considered old enough for flushing to disk via the pdflush daemon (default 2999). Expressed in 100'ths of a second
>     
>         vm.dirty_expire_centisecs=2000
>         
> 
> *   Shorten the interval at which the pdflush daemon wakes up to write dirty data to disk (default 499). Expressed in 100'ths of a second
>     
>         vm.dirty_writeback_centisecs=400
>         
> 
> *   Decrease the tendency of the kernel to reclaim the memory which is used for caching of directory and inode objects (default 100, do not increase this beyond 100 as it can cause excessive reclaim).
>     
>         vm.vfs_cache_pressure=50
>         
> 
> *   RHEL 6 Will take into account highmem along with lowmem when calculating dirty&#95;ratio and dirty&#95;background_ratio. This will will make page reclaiming faster.
>     
>         vm.highmem_is_dirtyable=1
>         
> 
> **Overcommit Memory**
> 
> *   Overcommitting memory allows the kernel to potentially allocate more memory than the system actually has. This is perfectly safe, and in fact default behavior, as the Linux VM will handle the management of memory. However, to tune it, consider the following information: **/proc/sys/vm/overcommit_memory** 
>     *   **O** - Heuristic overcommit handling. Obvious overcommits of address space are refused. Used for a typical system. It ensures a seriously wild allocation fails while allowing overcommit to reduce swap usage. root is allowed to allocate slighly more memory in this mode. This is the default.
>     *   **1** - Always overcommit. Appropriate for some scientific applications.
>     *   **2** - Don't overcommit. The total address space commit for the system is not permitted to exceed swap plus a configurable percentage (default is 50) of physical RAM. Depending on the percentage you use, in most situations this means a process will not be killed while attempting to use already-allocated memory but will receive errors on memory allocation as appropriate.
> 
> **HugePages**
> 
> *   Enabling an application to use HugePages provides many benefits for the VM as it allows that application to lock data into memory and prevent it from swapping. Some advantages of such a configuration: 
>     *   Increased performance by through increased TLB hits
>     *   Pages are locked in memory and are never swapped out which guarantees that shared memory like SGA remains in RAM
>     *   Contiguous pages are preallocated and cannot be used for anything else but for System V shared memory (e.g. SGA)
>     *   Less bookkeeping work for the kernel for that part of virtual memory due to larger page sizes
> *   HugePages are only useful for applications that are aware of them (i.e., don't recommend them as a way to solve all memory issues). They are only used for shared memory allocations so be sure not to allocate too many pages. By default the size of one HugePage is 2Mb. For Oracle systems allocate enough HugePages to hold the entire SGA in memory.
> *   To enable HugePages use a sysctl setting to define how many pages should be allocated. RHEL 4 onwards `vm.nr_hugepages=1024`

We talked about free a little bit. If you are on a 32bit system and you want to find out the LOW and HIGH zone memory usage you can run the following:

    [root@rhel1 ~]# free -lm
                 total       used       free     shared    buffers     cached
    Mem:          1003        989         13          0         86        601
    Low:           863        849         13
    High:          139        139          0
    -/+ buffers/cache:        301        701
    Swap:         2047          0       2047
    

To check out the available kernel tunables for memory management, you can run the following:

    [root@rhel1 ~]# sysctl -a | grep vm
    vm.overcommit_memory = 0
    vm.panic_on_oom = 0
    vm.oom_kill_allocating_task = 0
    vm.extfrag_threshold = 500
    vm.oom_dump_tasks = 0
    vm.would_have_oomkilled = 0
    vm.overcommit_ratio = 50
    vm.page-cluster = 3
    vm.dirty_background_ratio = 10
    vm.dirty_background_bytes = 0
    vm.dirty_ratio = 20
    vm.dirty_bytes = 0
    vm.dirty_writeback_centisecs = 500
    vm.dirty_expire_centisecs = 3000
    vm.nr_pdflush_threads = 0
    vm.swappiness = 60
    vm.nr_hugepages = 0
    vm.hugetlb_shm_group = 0
    vm.hugepages_treat_as_movable = 0
    vm.nr_overcommit_hugepages = 0
    vm.lowmem_reserve_ratio = 256   32  32
    vm.drop_caches = 0
    vm.min_free_kbytes = 2883
    vm.percpu_pagelist_fraction = 0
    vm.max_map_count = 65530
    vm.laptop_mode = 0
    vm.block_dump = 0
    vm.vfs_cache_pressure = 100
    vm.legacy_va_layout = 0
    vm.stat_interval = 1
    vm.mmap_min_addr = 4096
    vm.vdso_enabled = 1
    vm.highmem_is_dirtyable = 0
    vm.scan_unevictable_pages = 0
    

Most of these were covered above. To get a good overall usage of memory and swap usage, check out **vmstat**:

    [root@rhel1 proc]# vmstat -s | grep -iE 'mem|swap'
          1027456 K total memory
          1012348 K used memory
           359664 K active memory
           572968 K inactive memory
            15108 K free memory
            88440 K buffer memory
           613720 K swap cache
          2096440 K total swap
                0 K used swap
          2096440 K free swap
                0 pages swapped in
                0 pages swapped out
    

## Linux VFS

From "<a href="http://www.ibm.com/developerworks/library/l-virtual-filesystem-switch/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.ibm.com/developerworks/library/l-virtual-filesystem-switch/']);">Anatomy of the Linux virtual file system switch</a>":

> The flexibility and extensibility of support for Linux file systems is a direct result of an abstracted set of interfaces. At the core of that set of interfaces is the virtual file system switch (VFS).
> 
> The VFS provides a set of standard interfaces for upper-layer applications to perform file I/O over a diverse set of file systems. And it does it in a way that supports multiple concurrent file systems over one or more underlying devices. Additionally, these file systems need not be static but may come and go with the transient nature of the storage devices.
> 
> For example, a typical Linux desktop supports an ext3 file system on the available hard disk, as well as the ISO 9660 file system on an available CD-ROM (otherwise called the CD-ROM file system, or CDFS). As CD-ROMs are inserted and removed, the Linux kernel must adapt to these new file systems with different contents and structure. A remote file system can be accessed through the Network File System (NFS). At the same time, Linux can mount the NT File System (NTFS) partition of a Windows®/Linux dual-boot system from the local hard disk and read and write from it.
> 
> Finally, a removable USB flash drive (UFD) can be hot-plugged, providing yet another file system. All the while, the same set of file I/O interfaces can be used over these devices, permitting the underlying file system and physical device to be abstracted away from the user (see Figure 1).
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs-abstraction-layer.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs-abstraction-layer.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs-abstraction-layer.png" alt="vfs abstraction layer RHCSA and RHCE Chapter 10   The Kernel" width="613" height="348" class="alignnone size-full wp-image-9148" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **Layered abstractions**  
> Now, let's add some concrete architecture to the abstract features that the Linux VFS provides. Figure 2 shows a high-level view of the Linux stack from the point of view of the VFS. Above the VFS is the standard kernel system-call interface (SCI). This interface allows calls from user-space to transition to the kernel (in different address spaces). In this domain, a user-space application invoking the POSIX open call passes through the GNU C library (glibc) into the kernel and into system call de-multiplexing. Eventually, the VFS is invoked using the call *sys_open*.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_layered.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_layered.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_layered.png" alt="vfs layered RHCSA and RHCE Chapter 10   The Kernel" width="415" height="372" class="alignnone size-full wp-image-9150" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> The VFS provides the abstraction layer, separating the POSIX API from the details of how a particular file system implements that behavior. The key here is that Open, Read, Write, or Close API system calls work the same regardless of whether the underlying file system is ext3 or Btrfs. VFS provides a common file model that the underlying file systems inherit (they must implement behaviors for the various POSIX API functions). A further abstraction, outside of the VFS, hides the underlying physical device (which could be a disk, partition of a disk, networked storage entity, memory, or any other medium able to store information—even transiently).
> 
> In addition to abstracting the details of file operations from the underlying file systems, VFS ties the underlying block devices to the available file systems. Let's now look at the internals of the VFS to see how this works.
> 
> **VFS internals**  
> Before looking at the overall architecture of the VFS subsystem, let's have a look at the major objects that are used. This section explores the superblock, the index node (or inode), the directory entry (or dentry), and finally, the file object. Some additional elements, such as caches, are also important here, and I explore these later in the overall architecture.
> 
> **Superblock**  
> The superblock is the container for high-level metadata about a file system. The superblock is a structure that exists on disk (actually, multiple places on disk for redundancy) and also in memory. It provides the basis for dealing with the on-disk file system, as it defines the file system's managing parameters (for example, total number of blocks, free blocks, root index node).
> 
> On disk, the superblock provides information to the kernel on the structure of the file system on disk. In memory, the superblock provides the necessary information and state to manage the active (mounted) file system. Because Linux supports multiple concurrent file systems mounted at the same time, each super&#95;block structure is maintained in a list (super&#95;blocks, defined in ./linux/fs/super.c, with the structure defined in /linux/include/fs/fs.h).
> 
> Note that within the kernel, another management object called *vfsmount* provides information on mounted file systems. The list of these objects refers to the superblock and defines the mount point, name of the /dev device on which this file system resides, and other higher-level attachment information.

You can use **dumpe2fs** to get the **superblock** information. For instance here is the **superblock** information from an ext4 filesystem:

    [root@rhel1 ~]# dumpe2fs -h /dev/sda1
    dumpe2fs 1.41.12 (17-May-2010)
    Filesystem volume name:   none
    Last mounted on:          /boot
    Filesystem UUID:          a72a23d5-b485-413f-89e3-cb3060621a50
    Filesystem magic number:  0xEF53
    Filesystem revision #:    1 (dynamic)
    Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery extent flex_bg sparse_super huge_file uninit_bg dir_nlink extra_isize
    Filesystem flags:         signed_directory_hash 
    Default mount options:    user_xattr acl
    Filesystem state:         clean
    Errors behavior:          Continue
    Filesystem OS type:       Linux
    Inode count:              128016
    Block count:              512000
    Reserved block count:     25600
    Free blocks:              466892
    Free inodes:              127978
    First block:              1
    Block size:               1024
    Fragment size:            1024
    Reserved GDT blocks:      256
    Blocks per group:         8192
    Fragments per group:      8192
    Inodes per group:         2032
    Inode blocks per group:   254
    Flex block group size:    16
    Filesystem created:       Mon Feb  4 04:20:18 2013
    Last mount time:          Sun Jun 30 16:01:20 2013
    Last write time:          Sun Jun 30 16:01:20 2013
    Mount count:              30
    Maximum mount count:      -1
    Last checked:             Mon Feb  4 04:20:18 2013
    Check interval:           0 (none)
    Lifetime writes:          43 MB
    Reserved blocks uid:      0 (user root)
    Reserved blocks gid:      0 (group root)
    First inode:              11
    Inode size:           128
    Journal inode:            8
    Default directory hash:   half_md4
    Directory Hash Seed:      b83aca5e-77d1-42c6-bfc7-ba5b75f18db9
    Journal backup:           inode blocks
    Journal features:         journal_incompat_revoke
    Journal size:             8M
    Journal length:           8192
    Journal sequence:         0x00000058
    Journal start:            0
    

More from the same document:

> **The index node (inode)**  
> Linux manages all objects in a file system through an object called an inode (short for index node). An inode can refer to a file or a directory or a symbolic link to another object. Note that because files are used to represent other types of objects, such as devices or memory, inodes are used to represent them also.
> 
> Note that the inode I refer to here is the VFS layer inode (in-memory inode). Each file system also includes an inode that lives on disk and provides details about the object specific to the particular file system.
> 
> VFS inodes are allocated using the slab allocator (from the inode_cache). The inode consists of data and operations that describe the inode, its contents, and the variety of operations that are possible on it. Figure 4 is a simple illustration of a VFS inode consisting of a number of lists, one of which refers to the dentries that refer to this inode. Object-level metadata is included here, consisting of the familiar manipulation times (create time, access time, modify time), as are the owner and permission data (group-id, user-id, and permissions). The inode refers to the file operations that are possible on it, most of which map directly to the system-call interfaces (for example, open, read, write, and flush). There is also a reference to inode-specific operations (create, lookup, link, mkdir, and so on). Finally, there's a structure to manage the actual data for the object that is represented by an address space object. An address space object is an object that manages the various pages for the inode within the page cache. The address space object is used to manage the pages for a file and also for mapping file sections into individual process address spaces. The address space object comes with its own set of operations (writepage, readpage, releasepage, and so on).

We can use **stat** to figure out the inode information of a file residing on a file system, not the in-memory inode:

    [root@rhel1 ~]# stat ks.cfg 
      File: `ks.cfg'
      Size: 1622                Blocks: 8          IO Block: 4096   regular file
    Device: fd00h/64768d    Inode: 142502      Links: 1
    Access: (0644/-rw-r--r--)  Uid: (    0/    root)   Gid: (    0/    root)
    Access: 2013-03-13 08:27:36.791684448 -0600
    Modify: 2013-03-13 08:26:35.312875563 -0600
    Change: 2013-03-13 08:26:35.312875563 -0600
    

> **Directory entry (dentry)** The hierarchical nature of a file system is managed by another object in VFS called a dentry object. A file system will have one root dentry (referenced in the superblock), this being the only dentry without a parent. All other dentries have parents, and some have children. For example, if a file is opened that's made up of /home/user/name, four dentry objects are created: one for the root /, one for the home entry of the root directory, one for the name entry of the user directory, and finally, one dentry for the name entry of the user directory. In this way, dentries map cleanly into the hierarchical file systems in use today.

**stat** also tells us if a file is a directory or a regular file. Here is the output of **stat** when executed against a directory:

    [root@rhel1 ~]# stat repo
      File: `repo'
      Size: 4096                Blocks: 8          IO Block: 4096   directory
    Device: fd00h/64768d    Inode: 137310      Links: 7
    Access: (0555/dr-xr-xr-x)  Uid: (    0/    root)   Gid: (    0/    root)
    Access: 2013-06-10 11:38:37.657543746 -0600
    Modify: 2011-05-10 17:09:28.000000000 -0600
    Change: 2013-02-06 04:40:08.370000000 -0700
    

> **Object relationships**  
> Now that I've reviewed the various important objects in the VFS layer, let's look at how they relate in a single diagram. Because I've explored the object in a bottom-up fashion so far in this article, I now look at the reverse from the user perspective (see Figure 7).
> 
> At the top is the open file object, which is referenced by a process's file descriptor list. The file object refers to a dentry object, which refers to an inode. Both the inode and dentry objects refer to the underlying super_block object. Multiple file objects may refer to the same dentry (as in the case of two users sharing the same file). Note also in Figure 7 that a dentry object refers to another dentry object. In this case, a directory refers to file, which in turn refers to the inode for the particular file.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_relationships.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_relationships.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_relationships.png" alt="vfs relationships RHCSA and RHCE Chapter 10   The Kernel" width="457" height="335" class="alignnone size-full wp-image-9151" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **The VFS architecture**  
> The internal architecture of the VFS is made up of a dispatching layer that provides the file system abstraction and a number of caches to improve the performance of file system operations. This section explores the internal architecture and how the major objects interact (see Figure 8).
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_arch.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_arch.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/06/vfs_arch.png" alt="vfs arch RHCSA and RHCE Chapter 10   The Kernel" width="425" height="385" class="alignnone size-full wp-image-9152" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> The two major objects that are dynamically managed in the VFS include the dentry and inode objects. These are cached to improve the performance of accesses to the underlying file systems. When a file is opened, the dentry cache is populated with entries representing the directory levels representing the path. An inode for the object is also created representing the file. The dentry cache is built using a hash table and is hashed by the name of the object. Entries for the dentry cache are allocated from the dentry_cache slab allocator and use a least-recently-used (LRU) algorithm to prune entries when memory pressure exists. You can find the functions associated with the dentry cache in ./linux/fs/dcache.c (and ./linux/include/linux/dcache.h).
> 
> The inode cache is implemented as two lists and a hash table for faster lookup. The first list defines the inodes that are currently in use; the second list defines the inodes that are unused. Those inodes in use are also stored in the hash table. Individual inode cache objects are allocated from the inode_cache slab allocator. You can find the functions associated with the inode cache in ./linux/fs/inode.c (and ./linux/include/fs.h). From the implementation today, the dentry cache is the master of the inode cache. When a dentry object exists, an inode object will also exist in the inode cache. Lookups are performed on the dentry cache, which result in an object in the inode cache.

You can either check out **/proc/slabinfo** for the size of the *inode* cache:

    [root@rhel1 ~]# cat /proc/slabinfo | grep ^inode_cache
    inode_cache         5665   5973    352   11    1 : tunables   54   27    0 : slabdata    543    543      0
    

Or you can actually run **slabtop** and see real time usage. Here is how my **slabtop** looked like:

     Active / Total Objects (% used)    : 846824 / 855333 (99.0%)
     Active / Total Slabs (% used)      : 7807 / 7807 (100.0%)
     Active / Total Caches (% used)     : 96 / 183 (52.5%)
     Active / Total Size (% used)       : 31127.88K / 31911.36K (97.5%)
     Minimum / Average / Maximum Object : 0.01K / 0.04K / 4096.00K
    
      OBJS ACTIVE  USE OBJ SIZE  SLABS OBJ/SLAB CACHE SIZE NAME                   
    467712 467589  99%    0.02K   2304  203  9216K avtab_node
    327700 327484  99%    0.03K   2900  113     11600K size-32
     10295  10272  99%    0.13K    355   29  1420K dentry
      9828   8623  87%    0.04K    117   84   468K selinux_inode_security
      5973   5649  94%    0.34K    543   11  2172K inode_cache
    

We can see that our *inode_cache* is taking **2172K**. I didn't find that many tuning options for VFS. From <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Global_File_System_2/s2-vfstuning-gfs2.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/html/Global_File_System_2/s2-vfstuning-gfs2.html']);">RHEL Global File System</a>:

> **2.5.3. VFS Tuning Options: Research and Experiment**  
> Like all Linux file systems, GFS2 sits on top of a layer called the virtual file system (VFS). You can tune the VFS layer to improve underlying GFS2 performance by using the sysctl(8) command. For example, the values for **dirty&#95;background&#95;ratio** and **vfs&#95;cache&#95;pressure** may be adjusted depending on your situation. To fetch the current values, use the following commands:
> 
>     sysctl -n vm.dirty_background_ratio
>     sysctl -n vm.vfs_cache_pressure
>     
> 
> The following commands adjust the values:
> 
>     sysctl -w vm.dirty_background_ratio=20
>     sysctl -w vm.vfs_cache_pressure=500
>     
> 
> You can permanently change the values of these parameters by editing the **/etc/sysctl.conf** file.

## Linux Kernel Networking

From <a href="http://cd-docdb.fnal.gov/0019/001968/001/Linux-Pkt-Recv-Performance-Analysis-Final.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://cd-docdb.fnal.gov/0019/001968/001/Linux-Pkt-Recv-Performance-Analysis-Final.pdf']);">The Performance Analysis of Linux Networking – Packet Receiving</a>:

> **2. Packet Receiving Process**  
> Figure 1 demonstrates generally the trip of a packet from its ingress into a Linux end system to its final delivery to the application. In general, the packet’s trip can be classified into three stages:
> 
> *   Packet is transferred from network interface card (NIC) to ring buffer. The NIC and device driver manage and control this process. 
> *   Packet is transferred from ring buffer to a socket receive buffer, driven by a software interrupt request (softirq). The kernel protocol stack handles this stage.
> *   Packet data is copied from the socket receive buffer to the application, which we will term the Data Receiving Process.
> 
> In the following sections, we detail these three stages.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/kernel-networking.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/kernel-networking.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/kernel-networking.png" alt="kernel networking RHCSA and RHCE Chapter 10   The Kernel" width="821" height="221" class="alignnone size-full wp-image-9163" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **2.1 NIC and Device Driver Processing**  
> The NIC and its device driver perform the layer 1 and 2 functions of the OSI 7-layer network model: packets are received and transformed from raw physical signals, and placed into system memory, ready for higher layer processing. The Linux kernel uses a structure sk&#95;buff to hold any single packet up to the MTU (Maximum Transfer Unit) of the network. The device driver maintains a “ring” of these packet buffers, known as a “ring buffer”, for packet reception (and a separate ring for transmission). A ring buffer consists of a device- and driver-dependent number of packet descriptors. To be able to receive a packet, a packet descriptor should be in “ready” state, which means it has been initialized and pre-allocated with an empty sk&#95;buff which has been memory-mapped into address space accessible by the NIC over the system I/O bus. When a packet comes, one of the ready packet descriptors in the receive ring will be used, the packet will be transferred by DMA into the pre-allocated sk&#95;buff, and the descriptor will be marked as used. A used packet descriptor should be reinitialized and refilled with an empty sk&#95;buff as soon as possible for further incoming packets. If a packet arrives and there is no ready packet descriptor in the receive ring, it will be discarded. Once a packet is transferred into the main memory, during subsequent processing in the network stack, the packet remains at the same kernel memory location.
> 
> Figure 2 shows a general packet receiving process at NIC and device driver level. When a packet is received, it is transferred into main memory and an interrupt is raised only after the packet is accessible to the kernel. When CPU responds to the interrupt, the driver’s interrupt handler is called, within which the
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/kernel-networking-ring-buffer.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/kernel-networking-ring-buffer.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/kernel-networking-ring-buffer.png" alt="kernel networking ring buffer RHCSA and RHCE Chapter 10   The Kernel" width="451" height="339" class="alignnone size-full wp-image-9164" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> The softirq is serviced shortly afterward. The CPU polls each device in its poll queue to get the received packets from the ring buffer by calling the poll method of the device driver. Each received packet is passed upwards for further protocol processing. After a received packet is dequeued from its receive ring buffer for further processing, its corresponding packet descriptor in the receive ring buffer needs to be reinitialized and refilled.

We can check the size of the **sk_buff** cache from the **/proc/slabinfo** file:

    [root@rhel1 ~]# grep skb /proc/slabinfo 
    skbuff_fclone_cache     10     10    384   10    1 : tunables   54   27    0 : slabdata      1      1      0
    skbuff_head_cache    520    520    192   20    1 : tunables  120   60    0 : slabdata     26     26      0
    

To determine which driver is used for a NIC we can use **dmesg**:

    [root@rhel1 ~]# dmesg | grep eth0
    e1000 0000:00:03.0: eth0: (PCI:33MHz:32-bit) 08:00:27:f1:be:13
    e1000 0000:00:03.0: eth0: Intel(R) PRO/1000 Network Connection
    e1000: eth0 NIC Link is Up 1000 Mbps Full Duplex, Flow Control: RX
    ADDRCONF(NETDEV_UP): eth0: link is not ready
    ADDRCONF(NETDEV_CHANGE): eth0: link becomes ready
    eth0: no IPv6 routers present
    

Or we can use ethtool:

    [root@rhel1 ~]# ethtool -i eth0
    driver: e1000
    version: 7.3.21-k6-1-NAPI
    firmware-version: N/A
    bus-info: 0000:00:03.0
    

We are using the *e1000* driver. To check how much size the NIC driver is using, we can use **lsmod**:

    [root@rhel1 ~]# lsmod | head -1; lsmod | grep -i e1000
    Module                  Size  Used by
    e1000                 146952  0 
    

Using **modinfo** we can check available parameters of the NIC driver:

    [root@rhel1 etc]# modinfo e1000 | grep ^parm
    parm:           TxDescriptors:  Number of transmit descriptors (array of int)
    parm:           RxDescriptors:  Number of receive descriptors (array of int)
    parm:           Speed:     Speed setting (array of int)
    parm:           Duplex:    Duplex setting (array of int)
    parm:           AutoNeg:   Advertised auto-negotiation setting (array of int)
    parm:           FlowControl:   Flow Control setting (array of int)
    parm:           XsumRX:    Disable or enable Receive Checksum offload (array of int)
    parm:           TxIntDelay:   Transmit Interrupt Delay (array of int)
    parm:           TxAbsIntDelay:  Transmit Absolute Interrupt Delay (array of int)
    parm:           RxIntDelay:   Receive Interrupt Delay (array of int)
    parm:           RxAbsIntDelay:  Receive Absolute Interrupt Delay (array of int)
    parm:           InterruptThrottleRate:   Interrupt Throttling Rate (array of int)
    parm:           SmartPowerDownEnable:   Enable PHY smart power down (array of int)
    parm:           KumeranLockLoss:  Enable Kumeran lock loss workaround (array of int)
    parm:           copybreak:   Maximum size of packet that is copied to a new buffer on receive (uint)
    parm:           debug:  Debug level (0=none,...,16=all) (int)
    

To check most of the those parameters you can use ethtool:

    [root@rhel1 ~]# ethtool -g eth0
    Ring parameters for eth0:
    Pre-set maximums:
    RX:     4096
    RX Mini:    0
    RX Jumbo:   0
    TX:     4096
    Current hardware settings:
    RX:     256
    RX Mini:    0
    RX Jumbo:   0
    TX:     256
    
    [root@rhel1 ~]# ethtool -a eth0
    Pause parameters for eth0:
    Autonegotiate:  on
    RX:     on
    TX:     off
    
    [root@rhel1 ~]# ethtool -k eth0
    Offload parameters for eth0:
    rx-checksumming: on
    tx-checksumming: on
    scatter-gather: on
    tcp-segmentation-offload: on
    udp-fragmentation-offload: off
    generic-segmentation-offload: on
    generic-receive-offload: off
    large-receive-offload: off
    
    [root@rhel1 ~]# ethtool -c eth0
    Coalesce parameters for eth0:
    Adaptive RX: off  TX: off
    stats-block-usecs: 0
    sample-interval: 0
    pkt-rate-low: 0
    pkt-rate-high: 0
    
    rx-usecs: 0
    rx-frames: 0
    rx-usecs-irq: 0
    rx-frames-irq: 0
    
    tx-usecs: 0
    tx-frames: 0
    tx-usecs-irq: 0
    tx-frames-irq: 0
    
    rx-usecs-low: 0
    rx-frame-low: 0
    tx-usecs-low: 0
    tx-frame-low: 0
    
    rx-usecs-high: 0
    rx-frame-high: 0
    tx-usecs-high: 0
    tx-frame-high: 0
    

To check how many interrupts a device is using, you can check out the contents of **/proc/interrupts**:

    [root@rhel1 ~]# cat /proc/interrupts 
               CPU0       
      0:        147    XT-PIC-XT        timer
      1:          8    XT-PIC-XT        i8042
      2:          0    XT-PIC-XT        cascade
      5:      11186    XT-PIC-XT        ahci
      8:          0    XT-PIC-XT        rtc0
      9:       4631    XT-PIC-XT        acpi, eth1
     10:       2265    XT-PIC-XT        eth0
     12:        141    XT-PIC-XT        i8042
     14:          0    XT-PIC-XT        ata_piix
     15:        119    XT-PIC-XT        ata_piix
    

More from the same document:

> **2.2 Kernel Protocol Stack**
> 
> **2.2.1 IP Processing**  
> The IP protocol receive function is called during the processing of a softirq for each IP packet that is dequeued from the ring buffer. This function performs initial checks on the IP packet, which mainly involve verifying its integrity, applying firewall rules, and disposing the packet for forwarding or local delivery to a higher level protocol. For each transport layer protocol, a corresponding handler function is defined: tcp&#95;v4&#95;rcv() and udp_rcv() are two examples.
> 
> **2.2.2 TCP Processing**  
> When a packet is handed upwards for TCP processing, the function tcp&#95;v4&#95;rcv() first performs the TCP header processing. Then the socket associated with the packet is determined, and the packet dropped if none exists. A socket has a lock structure to protect it from un-synchronized access. If the socket is locked, the packet waits on the backlog queue before being processed further. If the socket is not locked, and its Data Receiving Process is sleeping for data, the packet is added to the socket’s prequeue and will be processed in batch in the process context, instead of the interrupt context . Placing the first packet in the prequeue will wake up the sleeping data receiving process. If the prequeue mechanism does not accept the packet, which means that the socket is not locked and no process is waiting for input on it, the packet must be processed immediately by a call to tcp&#95;v4&#95;do_rcv(). The same function also is called to drain the backlog queue and prequeue. Those queues (except in the case of prequeue overflow) are drained in the process context, not the interrupt context of the softirq. In the case of prequeue overflow, which means that packets within the prequeue reach/exceed the socket’s receive buffer quota, those packets should be processed as soon as possible, even in the interrupt context.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/linux_kernel_ip_proce.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/linux_kernel_ip_proce.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/linux_kernel_ip_proce.png" alt="linux kernel ip proce RHCSA and RHCE Chapter 10   The Kernel" width="286" height="514" class="alignnone size-full wp-image-9165" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> **2.2.3 The UDP Processing**  
> When a UDP packet arrives from the IP layer, it is passed on to udp&#95;rcv(). udp&#95;rcv()’s mission is to verify the integrity of the UDP packet and to queue one or more copies for delivery to multicast and broadcast sockets and exactly one copy to unicast sockets. When queuing the received packet in the receive queue of the matching socket, if there is insufficient space in the receive buffer quota of the socket, the packet may be discarded. Data within the socket’s receive buffer are ready for delivery to the user space.
> 
> **2.3 Data Receiving Process**  
> Packet data is finally copied from the socket’s receive buffer to user space by data receiving process through socket-related receive system calls. The receiving process supplies a memory address and number of bytes to be transferred, either in a struct iovec, or as two parameters gathered into such a struct by the kernel. As mentioned above, all the TCP socket-related receive system calls result in the final calling of tcp&#95;recvmsg(), which will copy packet data from socket’s buffers (receive queue, prequeue, backlog queue) through iovec. For UDP, all the socket-related receiving system calls result in the final calling of udp&#95;recvmsg(). When udp_recvmsg() is called, data inside receive queue is copied through iovec to user space directly.

## RHEL Network Tuning

There are a lot of parameters to tune the kernel networking. From the "<a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Performance_Tuning_Guide/Red_Hat_Enterprise_Linux-6-Performance_Tuning_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Performance_Tuning_Guide/Red_Hat_Enterprise_Linux-6-Performance_Tuning_Guide-en-US.pdf']);">Performance Tuning Guide</a>":

> **8.2. Optimized Network Settings**  
> Performance tuning is usually done in a pre-emptive fashion. Often, we adjust known variables before running an application or deploying a system. If the adjustment proves to be ineffective, we try adjusting other variables. The logic behind such thinking is that by default, the system is not operating at an optimal level of performance; as such, we think we need to adjust the system accordingly. In some cases, we do so via calculated guesses.
> 
> As mentioned earlier, the network stack is mostly self-optimizing. In addition, effectively tuning the network requires a thorough understanding not just of how the network stack works, but also of the specific system's network resource requirements. Incorrect network performance configuration can actually lead to degraded performance.
> 
> For example, consider the bufferfloat problem. Increasing buffer queue depths results in TCP connections that have congestion windows larger than the link would otherwise allow (due to deep buffering). However, those connections also have huge RTT values since the frames spend so much time in-queue. This, in turn, actually results in sub-optimal output, as it would become impossible to detect congestion.
> 
> When it comes to network performance, it is advisable to keep the default settings unless a particular performance issue becomes apparent. Such issues include frame loss, significantly reduced throughput, and the like. Even then, the best solution is often one that results from meticulous study of the problem, rather than simply tuning settings upward (increasing buffer/queue lengths, reducing interrupt latency, etc).
> 
> To properly diagnose a network performance problem, use the following tools:
> 
> **netstat**- A command-line utility that prints network connections, routing tables, interface statistics, masquerade connections and multicast memberships. It retrieves information about the networking subsystem from the **/proc/net/** file system. These files include:
> 
> *   /proc/net/dev (device information)
> *   /proc/net/tcp (TCP socket information)
> *   /proc/net/unix (Unix domain socket information)
> 
> **dropwatch** - A monitoring utility that monitors packets dropped by the kernel.
> 
> **ip** - A utility for managing and monitoring routes, devices, policy routing, and tunnels.
> 
> **ethtool** - A utility for displaying and changing NIC settings.
> 
> **/proc/net/snmp** - A file that displays ASCII data needed for the IP, ICMP, TCP, and UDP management information bases for an snmp agent. It also displays real-time UDP-lite statistics.
> 
> After collecting relevant data on a network performance problem, you should be able to formulate a theory — and, hopefully, a solution. For example, an increase in UDP input errors in **/proc/net/snmp** indicates that one or more socket receive queues are full when the network stack attempts to queue new frames into an application's socket.
> 
> This indicates that packets are bottlenecked at at least one socket queue, which means either the socket queue drains packets too slowly, or packet volume is too large for that socket queue. If it is the latter, then verify the logs of any network-intensive application for lost data - to resolve this, you would need to optimize or reconfigure the offending application.
> 
> **Socket receive buffer size** - Socket send and receive sizes are dynamically adjusted, so they rarely need to be manually edited. If further analysis, such as the analysis presented in the SystemTap network example, **sk&#95;stream&#95;wait_memory.stp**, suggests that the socket queue's drain rate is too slow, then you can increase the depth of the application's socket queue. To do so, increase the size of receive buffers used by sockets by configuring either of the following values:
> 
> **rmem_default** - A kernel parameter that controls the default size of receive buffers used by sockets. To configure this, run the following command:
> 
>     sysctl -w net.core.rmem_default=N
>     
> 
> Replace **N** with the desired buffer size, in bytes. To determine the value for this kernel parameter, view **/proc/sys/net/core/rmem_default**. Bear in mind that the value of **rmem_default** should be no greater than **rmem_max** (**/proc/sys/net/core/rmem_max**); if need be, increase the value of **rmem_max**.
> 
> **SO_RCVBUF** A socket option that controls the maximum size of a socket's receive buffer, in bytes. For more information on **SO_RCVBUF**, refer to the man page for more details: **man 7 socket**. To configure **SO_RCVBUF**, use the **setsockopt** utility. You can retrieve the current **SO_RCVBUF** value with **getsockopt**.
> 
> **8.3. Overview of Packet Reception**  
> To better analyze network bottlenecks and performance issues, you need to understand how packet reception works. Packet reception is important in network performance tuning because the receive path is where frames are often lost. Lost frames in the receive path can cause a significant penalty to network performance.
> 
> <a href="http://virtuallyhyper.com/wp-content/uploads/2013/07/RHEL_packet_recv.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2013/07/RHEL_packet_recv.png']);"><img src="http://virtuallyhyper.com/wp-content/uploads/2013/07/RHEL_packet_recv.png" alt="RHEL packet recv RHCSA and RHCE Chapter 10   The Kernel" width="595" height="118" class="alignnone size-full wp-image-9174" title="RHCSA and RHCE Chapter 10   The Kernel" /></a>
> 
> The Linux kernel receives each frame and subjects it to a four-step process:
> 
> 1.  *Hardware Reception*: the network interface card (NIC) receives the frame on the wire. Depending on its driver configuration, the NIC transfers the frame either to an internal hardware buffer memory or to a specified ring buffer.
> 2.  *Hard IRQ*: the NIC asserts the presence of a net frame by interrupting the CPU. This causes the NIC driver to acknowledge the interrupt and schedule the soft IRQ operation.
> 3.  *Soft IRQ*: this stage implements the actual frame-receiving process, and is run in **softirq** context. This means that the stage pre-empts all applications running on the specified CPU, but still allows hard IRQs to be asserted.
>     
>     In this context (running on the same CPU as hard IRQ, thereby minimizing locking overhead), the kernel actually removes the frame from the NIC hardware buffers and processes it through the network stack. From there, the frame is either forwarded, discarded, or passed to a target listening socket.
>     
>     When passed to a socket, the frame is appended to the application that owns the socket. This process is done iteratively until the NIC hardware buffer runs out of frames, or until the device weight (**dev_weight**).
> 
> 4.  *Application receive*: the application receives the frame and dequeues it from any owned sockets via the standard POSIX calls (**read**, **recv**, **recvfrom**). At this point, data received over the network no longer exists on the network stack.
> 
> **CPU/cache affinity**  
> To maintain high throughput on the receive path, it is recommended that you keep the L2 cache hot. As described earlier, network buffers are received on the same CPU as the IRQ that signaled their presence. This means that buffer data will be on the L2 cache of that receiving CPU.
> 
> To take advantage of this, place process affinity on applications expected to receive the most data on the NIC that shares the same core as the L2 cache. This will maximize the chances of a cache hit, and thereby improve performance.
> 
> **8.4.1. NIC Hardware Buffer**  
> The NIC fills its hardware buffer with frames; the buffer is then drained by the softirq, which the NIC asserts via an interrupt. To interrogate the status of this queue, use the following command:
> 
>     ethtool -S ethX
>     
> 
> Replace ethX with the NIC's corresponding device name. This will display how many frames have been dropped within ethX. Often, a drop occurs because the queue runs out of buffer space in which to store frames.
> 
> There are different ways to address this problem, namely:
> 
> **Input traffic** - You can help prevent queue overruns by slowing down input traffic. This can be achieved by filtering, reducing the number of joined multicast groups, lowering broadcast traffic, and the like. **Queue length** - Alternatively, you can also increase the queue length. This involves increasing the number of buffers in a specified queue to whatever maximum the driver will allow. To do so, edit the rx/tx ring parameters of **ethX** using:
> 
>     ethtool --set-ring ethX
>     
> 
> Append the appropriate rx or tx values to the aforementioned command.
> 
> **Device weight** You can also increase the rate at which a queue is drained. To do this, adjust the NIC's device weight accordingly. This attribute refers to the maximum number of frames that the NIC can receive before the softirq context has to yield the CPU and reschedule itself. It is controlled by the **/proc/sys/net/core/dev_weight** variable.
> 
> Most administrators have a tendency to choose the third option. However, keep in mind that there are consequences for doing so. Increasing the number of frames that can be received from a NIC in one iteration implies extra CPU cycles, during which no applications can be scheduled on that CPU.
> 
> **8.4.2. Socket Queue**  
> Like the NIC hardware queue, the socket queue is filled by the network stack from the **softirq** context. Applications then drain the queues of their corresponding sockets via calls to **read**, **recvfrom**, and the like.
> 
> To monitor the status of this queue, use the **netstat** utility; the **Recv-Q** column displays the queue size. Generally speaking, overruns in the socket queue are managed in the same way as NIC hardware buffer overruns.
> 
> **Input traffic** The first option is to slow down input traffic by configuring the rate at which the queue fills. To do so, either filter frames or pre-emptively drop them. You can also slow down input traffic by lowering the NIC's device weight.
> 
> **Queue depth** You can also avoid socket queue overruns by increasing the queue depth. To do so, increase the value of either the rmem&#95;default kernel parameter or the SO&#95;RCVBUF socket option.
> 
> **Application call frequency** - Whenever possible, optimize the application to perform calls more frequently. This involves modifying or reconfiguring the network application to perform more frequent POSIX calls (such as **recv**, **read**). In turn, this allows an application to drain the queue faster.
> 
> For many administrators, increasing the queue depth is the preferable solution. This is the easiest solution, but it may not always work long-term. As networking technologies get faster, socket queues will continue to fill more quickly. Over time, this means having to re-adjust the queue depth accordingly.
> 
> The best solution is to enhance or configure the application to drain data from the kernel more quickly, even if it means queuing the data in application space. This lets the data be stored more flexibly, since it can be swapped out and paged back in as needed.

<a href="http://kaivanov.blogspot.com/2010/09/linux-tcp-tuning.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kaivanov.blogspot.com/2010/09/linux-tcp-tuning.html']);">This</a> site covers a lot of good examples for kernel network tunables:

> Like all operating systems, the default maximum Linux TCP buffer sizes are way too small. I suggest changing them to the following settings:
> 
> To increase TCP max buffer size setable using setsockopt():
> 
>     net.core.rmem_max = 33554432
>     net.core.wmem_max = 33554432
>     
> 
> To increase Linux autotuning TCP buffer limits min, default, and max number of bytes to use set max to 16MB for 1GE, and 32M or 54M for 10GE:
> 
>     net.ipv4.tcp_rmem = 4096 87380 33554432
>     net.ipv4.tcp_wmem = 4096 65536 33554432
>     
> 
> You should also verify that the following are all set to the default value of 1:
> 
>     sysctl net.ipv4.tcp_window_scaling
>     sysctl net.ipv4.tcp_timestamps
>     sysctl net.ipv4.tcp_sack
>     
> 
> Another thing you can do to help increase TCP throughput with 1GB NICs is to increase the size of the interface queue. For paths with more than 50 ms RTT, a value of 5000-10000 is recommended. To increase txqueuelen, do the following:
> 
>     ifconfig eth0 txqueuelen 5000
>     
> 
> You can achieve increases in bandwidth of up to 10x by doing this on some long, fast paths. This is only a good idea for Gigabit Ethernet connected hosts, and may have other side effects such as uneven sharing between multiple streams.
> 
> Other kernel settings that help with the overall server performance when it comes to network traffic are the following:
> 
> **TCP&#95;FIN&#95;TIMEOUT** - This setting determines the time that must elapse before TCP/IP can release a closed connection and reuse its resources. During this TIME&#95;WAIT state, reopening the connection to the client costs less than establishing a new connection. By reducing the value of this entry, TCP/IP can release closed connections faster, making more resources available for new connections. Addjust this in the presense of many connections sitting in the TIME&#95;WAIT state:
> 
>     echo 30 > /proc/sys/net/ipv4/tcp_fin_timeout
>     
> 
> **TCP&#95;KEEPALIVE&#95;INTERVAL** - This determines the wait time between isAlive interval probes. To set:
> 
>     echo 30 > /proc/sys/net/ipv4/tcp_keepalive_intvl
>     
> 
> **TCP&#95;KEEPALIVE&#95;PROBES** - This determines the number of probes before timing out. To set:
> 
>     echo 5 > /proc/sys/net/ipv4/tcp_keepalive_probes
>     
> 
> **TCP&#95;TW&#95;RECYCLE** - This enables fast recycling of TIME_WAIT sockets. The default value is 0 (disabled). Should be used with caution with loadbalancers.
> 
>     echo 1 > /proc/sys/net/ipv4/tcp_tw_recycle
>     
> 
> **TCP&#95;TW&#95;REUSE** - This allows reusing sockets in TIME_WAIT state for new connections when it is safe from protocol viewpoint. Default value is 0 (disabled). It is generally a safer alternative to **tcp&#95;tw&#95;recycle**
> 
>     echo 1 > /proc/sys/net/ipv4/tcp_tw_reuse
>     
> 
> There are a couple additional sysctl settings for kernels 2.6 and newer, Not to cache ssthresh from previous connection:
> 
>     net.ipv4.tcp_no_metrics_save = 1
>     
> 
> To increase this for 10G NICS:
> 
>     net.core.netdev_max_backlog = 30000
>     
> 
> Starting with version 2.6.13, Linux supports pluggable congestion control algorithms . The congestion control algorithm used is set using the sysctl variable **net.ipv4.tcp&#95;congestion&#95;control**, which is set to bic/cubic or reno by default, depending on which version of the 2.6 kernel you are using. To get a list of congestion control algorithms that are available in your kernel (if you are running 2.6.20 or higher), run:
> 
>     sysctl net.ipv4.tcp_available_congestion_control
>     
> 
> The choice of congestion control options is selected when you build the kernel. The following are some of the options are available in the 2.6.23 kernel:
> 
> *   reno: Traditional TCP used by almost all other OSes. (default)
> *   cubic: CUBIC-TCP (NOTE: There is a cubic bug in the Linux 2.6.18 kernel used by Redhat Enterprise Linux 5.3 and Scientific Linux 5.3. Use 2.6.18.2 or higher!)
> *   bic: BIC-TCP
> *   htcp: Hamilton TCP
> *   vegas: TCP Vegas
> *   westwood: optimized for lossy networks
> 
> If cubic and/or htcp are not listed when you do '**sysctl net.ipv4.tcp&#95;available&#95;congestion_control**', try the following, as most distributions include them as loadable kernel modules:
> 
>     /sbin/modprobe tcp_htcp
>     /sbin/modprobe tcp_cubic
>     
> 
> If you are often dealing with SYN floods the following tunning can be helpful:
> 
>     sysctl -w net.ipv4.tcp_max_syn_backlog="16384"
>     

### The proc File System

As you have noticed most of the kernel tuning is done under **/proc** or via **sysctl**. So let's cover that, from the <a href="https://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/site/documentation/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf']);">Deployment Guide</a>:

> **The proc File System**  
> The Linux kernel has two primary functions: to control access to physical devices on the computer and to schedule when and how processes interact with these devices. The /proc/ directory (also called the proc file system) contains a hierarchy of special files which represent the current state of the kernel, allowing applications and users to peer into the kernel's view of the system.
> 
> The **/proc/** directory contains a wealth of information detailing system hardware and any running processes. In addition, some of the files within **/proc/** can be manipulated by users and applications to communicate configuration changes to the kernel.
> 
> **E.1. A Virtual File System** Linux systems store all data as files. Most users are familiar with the two primary types of files: text and binary. But the /proc/ directory contains another type of file called a virtual file. As such, /proc/ is often referred to as a virtual file system.
> 
> Virtual files have unique qualities. Most of them are listed as zero bytes in size, but can still contain a large amount of information when viewed. In addition, most of the time and date stamps on virtual files reflect the current time and date, indicative of the fact they are constantly updated.
> 
> Virtual files such as **/proc/interrupts**, **/proc/meminfo**, **/proc/mounts**, and **/proc/partitions** provide an up-to-the-moment glimpse of the system's hardware. Others, like the **/proc/filesystems** file and the **/proc/sys/** directory provide system configuration information and interfaces.
> 
> For organizational purposes, files containing information on a similar topic are grouped into virtual directories and sub-directories. Process directories contain information about each running process on the system.
> 
> **E.1.1. Viewing Virtual Files**  
> Most files within **/proc/** files operate similarly to text files, storing useful system and hardware data in human-readable text format. As such, you can use cat, more, or less to view them. For example, to display information about the system's CPU, run **cat /proc/cpuinfo**. This will return output similar to the following:
> 
>     processor : 0
>     vendor_id : AuthenticAMD
>     cpu family    : 5
>     model     : 9
>     model name    : AMD-K6(tm) 3D+
>     Processor stepping    : 1 cpu
>     MHz       : 400.919
>     cache size    : 256 KB
>     fdiv_bug  : no
>     hlt_bug       : no
>     f00f_bug  : no
>     coma_bug  : no
>     fpu       : yes
>     fpu_exception : yes
>     cpuid level   : 1
>     wp        : yes
>     flags     : fpu vme de pse tsc msr mce cx8 pge mmx syscall 3dnow k6_mtrr
>     bogomips  : 799.53
>     
> 
> Some files in **/proc/** contain information that is not human-readable. To retrieve information from such files, use tools such as **lspci**, **apm**, **free**, and **top**.
> 
> **E.1.2. Changing Virtual Files**  
> As a general rule, most virtual files within the **/proc/** directory are read-only. However, some can be used to adjust settings in the kernel. This is especially true for files in the **/proc/sys/** subdirectory.
> 
> To change the value of a virtual file, use the following command:
> 
>     echo value > /proc/file
>     
> 
> For example, to change the hostname on the fly, run:
> 
>     echo www.example.com > /proc/sys/kernel/hostname
>     
> 
> Other files act as binary or Boolean switches. Typing **cat /proc/sys/net/ipv4/ip_forward** returns either a **O** (off or false) or a **1** (on or true). A **O** indicates that the kernel is not forwarding network packets. To turn packet forwarding on, run **echo 1 > /proc/sys/net/ipv4/ip_forward**.

### Sysctl Command

From the deployment guide:

> **E.4. Using the sysctl Command**  
> The **/sbin/sysctl** command is used to view, set, and automate kernel settings in the **/proc/sys/** directory.
> 
> or a quick overview of all settings configurable in the **/proc/sys/** directory, type the **/sbin/sysctl -a** command as root. This creates a large, comprehensive list, a small portion of which looks something like the following:
> 
>     net.ipv4.route.min_delay = 2 kernel.sysrq = 0 kernel.sem = 250     32000     32     128
>     
> 
> This is the same information seen if each of the files were viewed individually. The only difference is the file location. For example, the **/proc/sys/net/ipv4/route/min_delay** file is listed as **net.ipv4.route.min_delay**, with the directory slashes replaced by dots and the **proc.sys** portion assumed.
> 
> The **sysctl** command can be used in place of echo to assign values to writable files in the **/proc/sys/** directory. For example, instead of using the command:
> 
>     echo 1 > /proc/sys/kernel/sysrq
>     
> 
> use the equivalent **sysctl** command as follows:
> 
>     sysctl -w kernel.sysrq="1"
>     kernel.sysrq = 1
>     
> 
> While quickly setting single values like this in **/proc/sys/** is helpful during testing, this method does not work as well on a production system as special settings within **/proc/sys/** are lost when the machine is rebooted. To preserve custom settings, add them to the **/etc/sysctl.conf** file.
> 
> Each time the system boots, the init program runs the **/etc/rc.d/rc.sysinit** script. This script contains a command to execute **sysctl** using **/etc/sysctl.conf** to determine the values passed to the kernel. Any values added to **/etc/sysctl.conf** therefore take effect each time the system boots.

