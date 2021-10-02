---
title: VCAP5-DCA Objective 6.2 – Troubleshoot CPU and Memory Performance
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/
categories: ['certifications', 'vcap5_dca', 'vmware']
tags: ['performance']
---

### Identify resxtop/esxtop metrics related to memory and CPU

From "[vSphere Monitoring and Performance](http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-monitoring-performance-guide.pdf)", here are the CPU counters:

![esxtop cpu counters p1 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_cpu_counters_p1.png)

Here are more of CPU counters:

![esxtop cpu p2 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_cpu_p2.png)

From the same pdf, here are the memory counters:

![esxtop mem p1 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_mem_p1.png)

Here are more counters from the same page:

![esxtop mem p2 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_mem_p2.png)

And here is the last page for the memory counters:

![esxtop mem p3 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_mem_p3.png)

### Identify vCenter Server Performance Chart metrics related to memory and CPU

From [this](http://communities.vmware.com/docs/DOC-5600) Communities page:

![perf charts cpu counters VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/perf_charts_cpu_counters.png)

and here are the memory counters:

![perf charts mem counters VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/perf_charts_mem_counters.png)

You can also check out the full list [here](http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.wssdk.apiref.doc_50/right-pane.html).

### Troubleshoot ESXi host and Virtual Machine CPU performance issues using appropriate metrics

From [this](https://raw.githubusercontent.com/elatov/upload/master/vcap-dca/obj_62/Esxtop_Troubleshooting_eng.pdf) pdf:

![esxtop cpu performance VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_cpu_performance.png)

Here is a good summary:

> %RDY: Percentage of time a VM was waiting to be scheduled. Possible reasons: too many vCPUs, too many vSMP VMs or a CPU limit setting (Trouble when >10)
> %CSTP: Percentage of time a ready to run VM has spent in co-descheduling state (Trouble when > 3 to resolve, decrease number of vCPUs on the VM)
> $MLMTD: Percentage of time a ready to vCPU was no schedules because of a CPU limit setting (Trouble when > 1, to resolve; remove the CPU limit)
> $SWPWT: How Long a VM has to wait for swapped pages read from disk. (Trouble when > 5, possible reason; memory overcommitment

Also this is from a 4.x document but it applies to 5.0 as well. Here is the document: "[Performance Troubleshooting for VMware vSphere 4.1](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/vsphere41-performance-troubleshooting.pdf)". From that document:

![check for host cpu saturation VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/check_for_host_cpu_saturation.png)

Here is a similar diagram for Guest CPU saturation:

![check for guest cpu saturation VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/check_for_guest_cpu_saturation.png)

### Troubleshoot ESXi host and Virtual Machine memory performance issues using appropriate metrics

From [this](https://raw.githubusercontent.com/elatov/upload/master/vcap-dca/obj_62/Esxtop_Troubleshooting_eng.pdf) pdf:

![esxtop memory issues VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/esxtop_memory_issues.png)

Here is a good summary:

> MCTLSZ: Amount of guest physical memory (MB) the ESXi Host is reclaiming by balloon driver. (Trouble when > 1)
> ZIP/s: Values larger than 0 indicates that the host is actively compressing memory (Trouble when > 1)
> UNZIP/s: Values larger than 0 indicate that the host is accessing compressed memory (Reason for this behavior is memory overcommitment)
> SWCUR: Memory (in MB) that has been swapped by VMkernel (Possible cause is memory overcommitment, Trouble when > 1)
> CACHEUSD: Memory (in MB) compressed by ESXi Host (Trouble when > 1)
> SWR/s SWW/s: Rate at which the ESXi host is writing to or reading from swapped memory (Trouble when > 1)

And from "[Performance Troubleshooting for VMware vSphere 4.1](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/vsphere41-performance-troubleshooting.pdf)":

![check for vm swapping VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/check_for_vm_swapping.png)

and here is another flow chart for VM memory issues:

![check vm fo compression VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance ](https://github.com/elatov/uploads/raw/master/2012/12/check_vm_fo_compression.png)

### Use Hot-Add functionality to resolve identified Virtual Machine CPU and memory performance issues

If you discover then the VM needs more resources, then follow the instruction laid out in [VCAP5-DCA Objective 3.2](/2012/11/vcap5-dca-objective-3-2-optimize-virtual-machine-resources/) to hot add memory or CPU

