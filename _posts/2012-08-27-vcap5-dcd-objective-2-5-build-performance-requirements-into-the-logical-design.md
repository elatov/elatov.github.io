---
title: VCAP5-DCD Objective 2.5 – Build Performance Requirements into the Logical Design
author: Karim Elatov
layout: post
permalink: /2012/08/vcap5-dcd-objective-2-5-build-performance-requirements-into-the-logical-design/
dsq_thread_id:
  - 1405626520
categories:
  - VCAP5-DCD
  - VMware
tags:
  - VCAP5-DCD
---
### Understand what logical performance services are provided by VMware solutions

From the <a href="http://www.virten.net/2012/07/vdcd510-objective-2-5-build-performance-requirements-into-the-logical-design/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.virten.net/2012/07/vdcd510-objective-2-5-build-performance-requirements-into-the-logical-design/']);">this</a> blog:

> **Memory**  
> VMware offers the following features to manage the memory efficiently
> 
> *   **Transparent Page Sharing:** Shares identical Memory Pages among multiple virtual machines. This feature is active by default and does not impact the performance of the virtual machine.
> *   **Ballooning: **Controls a balloon driver which is running inside each virtual machine. When the physical host runs out of memory it instructs the driver to inflate by allocating inactive physical pages. The ESX host can uses these pages to fulfill the demand from other virtual machines.
> *   **Memory Compression:** Prior to swap memory pages out to physical disks the ESX server starts to compress pages. Compared to swapping, compression can improve the overall performance in an memory overcommitment scenario.
> *   **Swapping:** As the last choice the ESX hypervisor starts to swap pages out to physical disks. This is definitely a bad situation as disk are much slower than memory.
> 
> **Disk**  
> Storage I/O Control (SIOC) allows cluster wide control of disk resources. The main goal is to prevent a single VM to use all available disk performance from a shared storage. With SIOC a virtual machine can be assigned a priority when contention arises on a defined datastore.
> 
> **Network**  
> Network I/O Control (NetIOC) enables traffic prioritization by partitioning of network bandwidth among the entire cluster.

### Identify and differentiate infrastructure qualities (Availability, Manageability, Performance,Recoverability, Security)

See previous objective

### List the key performance indicators for resource utilization

From same blog as above:

> **Key Performance Indicators**  
> According to ITIL, a Key Performance Indicator (KPI) is used to assess if a defined service is running according to expectations. The exact definition of the KPIs differs depending on the area. This objective is about server performance which is typically assessed using the following KPIs: Processor, Memory, Disk, and Network.

### Analyze current performance, identify and address gaps when building the logical design

From the <a href="http://professionalvmware.com/2012/05/apac-vbrownbag-follow-up-vcap-dcd-performance/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://professionalvmware.com/2012/05/apac-vbrownbag-follow-up-vcap-dcd-performance/']);">APAC BrownBag Session 14</a> Slide deck:  
<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/slide7of13-1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/slide7of13-1.png']);"><img class="alignnone size-full wp-image-2789" title="slide7of13-1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/slide7of13-1.png" alt="slide7of13 1 VCAP5 DCD Objective 2.5 – Build Performance Requirements into the Logical Design" width="943" height="601" /></a>

### Using a conceptual design, create a logical design that meets performance requirements.

Let&#8217;s say we say that we will have production VMs and development VMs. From the Conceptual design we will just have two different containers that represent each type of a VM. For the Logical Design we will have DRS Resource Pools and Tiered Storage. Here is an example take from a VMware article called &#8220;<a href="http://www.vmware.com/files/pdf/techpaper/VMW_10Q3_WP_vCloud_Director_Storage.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/VMW_10Q3_WP_vCloud_Director_Storage.pdf']);">Storage Considerations for VMware vCloud Director</a>&#8220;:  
<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/RP-tiered_storage.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/RP-tiered_storage.png']);"><img class="alignnone size-full wp-image-2793" title="RP-tiered_storage" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/RP-tiered_storage.png" alt="RP tiered storage VCAP5 DCD Objective 2.5 – Build Performance Requirements into the Logical Design" width="467" height="321" /></a>

### Identify performance-related functional requirements based on given non-functional requirements and service dependencies

Let&#8217;s say a non-functional requirement is we can only spend $50,000 for our storage needs. This will of course translate to what kind of disks we can afford, SSD Vs. SAS and how many of the disks. Depending on what type and how many disk we buy, we will limited to certain amount of IOPS.

### Define capacity management practices and create a capacity plan

From the linked document in the blue print &#8220;<a href="http://communities.vmware.com/docs/DOC-11484" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-11484']);">Proven Practice: Implementing ITIL v3 Capacity Management in a VMware environment</a>&#8220;:

> A key goal for Capacity management is to provide value to the business; this can be done to great effect using VMware and consolidation. Using consolidation it is possible to reduce the number of physical servers and to utilize those reduced physical servers at a more optimal rate.  
> &#8230;  
> &#8230;  
> Within Business Capacity Management we are looking to provide metrics to demonstrate our value to the business and whether we are meeting their requirements. The sort of metrics we could look at producing are:
> 
> *   % reduction in physical estate
> *   % reduction in power consumption (useful as documented evidence in obtaining any environmental standard e.g. ISO14001)
> *   % cost reduction in maintenance contracts
> 
> ..  
> ..  
> For a consolidation exercise we would look to use a tool such as VMware Capacity Planner that will analyze the current utilization of your server estate and determine your optimum consolidation requirements.

Make sure to define what the capacity is of the current environment.

### Incorporate scalability requirements into the logical design.

Use <a href="http://www.vmware.com/products/capacity-planner/overview.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/products/capacity-planner/overview.html']);" target="_blank">VMware Capacity Planner</a> to determine how much capacity they can handle with the current environment, and if the business wants to expand, provide a plan as to how many hosts are necessary to handle any additional load. Similar features are available in <a href="http://www.vmware.com/products/datacenter-virtualization/vcenter-operations-management/overview.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/products/datacenter-virtualization/vcenter-operations-management/overview.html']);" target="_blank">vCops</a>.

### Determine performance component of SLAs and service level management processes

From the same article as mentioned in the previous objective:

> As we know, the response time of a service/application is a key performance metric and it is used to determine the end user experience of using a service that conventional metrics like CPU utilization, memory consumption, etc won’t necessarily show.
> 
> Data relating to the response time of a service can be difficult to obtain, but is critical to determining how a service is performing. This sort of data will also become more important when we look at consolidating servers into a VMware environment as the resource limits that are applied when viewing the hardware as a whole will have a greater impact.
> 
> Figure 2 shows the relationship between utilization and the response time. As you can see the relationship isn’t a linear one; as the utilization starts to get closer to 100% the response time starts to increase greatly. As discussed previously this issue will become more apparent as the number of Virtual Machines hosted increases and will need perhaps more management than if the servers were physical. The key to managing this is to ensure accurate collection of the response time.  
> ..  
> ..  
> If you currently use a terminal emulation tool to graphically recreate a number of standard user steps to calculate the response time, then you may not need to alter the capture at all, but remember that the data captured prior to implementation will then provide a useful comparison from the SLA perspective. It will also provide a valuable business metric as to the benefits of moving to a VMware environment i.e. “We have consolidated Service A to VMware and it has reduced the user response time by 25%”.

For Troubleshooting Performance issues, I would suggest to read the following:

*   <a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-monitoring-performance-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-50-monitoring-performance-guide.pdf']);">vSphere Monitoring and Performance Guide</a>
*   <a href="http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/Perf_Best_Practices_vSphere5.0.pdf']);">Performance Best Practices for VMware vSphere 5.0</a>
*   <a href="http://www.vmware.com/products/vmmark/overview.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/products/vmmark/overview.html']);">Virtual Performance</a>

