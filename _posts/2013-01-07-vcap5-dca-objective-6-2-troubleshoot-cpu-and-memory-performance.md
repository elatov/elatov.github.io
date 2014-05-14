---
title: VCAP5-DCA Objective 6.2 – Troubleshoot CPU and Memory Performance
author: Karim Elatov
layout: post
permalink: /2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/
dsq_thread_id:
  - 1405551371
categories:
  - Certifications
  - VCAP5-DCA
  - VMware
tags:
  - VCAP5-DCA
---
### Identify resxtop/esxtop metrics related to memory and CPU

From &#8220;<a href="http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-monitoring-performance-guide.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://pubs.vmware.com/vsphere-50/topic/com.vmware.ICbase/PDF/vsphere-esxi-vcenter-server-501-monitoring-performance-guide.pdf']);">vSphere Monitoring and Performance</a>&#8220;, here are the CPU counters:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_cpu_counters_p1/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_cpu_counters_p1/']);" rel="attachment wp-att-5283"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_cpu_counters_p1.png" alt="esxtop cpu counters p1 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="595" height="886" class="alignnone size-full wp-image-5283" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

Here are more of CPU counters:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_cpu_p2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_cpu_p2/']);" rel="attachment wp-att-5284"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_cpu_p2.png" alt="esxtop cpu p2 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="598" height="641" class="alignnone size-full wp-image-5284" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

From the same pdf, here are the memory counters:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_mem_p1/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_mem_p1/']);" rel="attachment wp-att-5285"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_mem_p1.png" alt="esxtop mem p1 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="587" height="801" class="alignnone size-full wp-image-5285" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

Here are more counters from the same page:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_mem_p2/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_mem_p2/']);" rel="attachment wp-att-5286"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_mem_p2.png" alt="esxtop mem p2 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="589" height="868" class="alignnone size-full wp-image-5286" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

And here is the last page for the memory counters:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_mem_p3/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_mem_p3/']);" rel="attachment wp-att-5287"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_mem_p3.png" alt="esxtop mem p3 VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="595" height="401" class="alignnone size-full wp-image-5287" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

### Identify vCenter Server Performance Chart metrics related to memory and CPU

From <a href="http://communities.vmware.com/docs/DOC-5600" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/docs/DOC-5600']);">this</a> Communities page:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/perf_charts_cpu_counters/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/perf_charts_cpu_counters/']);" rel="attachment wp-att-5288"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/perf_charts_cpu_counters.png" alt="perf charts cpu counters VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="669" height="328" class="alignnone size-full wp-image-5288" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

and here are the memory counters:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/perf_charts_mem_counters/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/perf_charts_mem_counters/']);" rel="attachment wp-att-5289"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/perf_charts_mem_counters.png" alt="perf charts mem counters VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="667" height="743" class="alignnone size-full wp-image-5289" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

You can also check out the full list <a href="http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.wssdk.apiref.doc_50/right-pane.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://pubs.vmware.com/vsphere-50/index.jsp?topic=/com.vmware.wssdk.apiref.doc_50/right-pane.html']);">here</a>.

### Troubleshoot ESXi host and Virtual Machine CPU performance issues using appropriate metrics

From <a href="http://www.vmworld.net/wp-content/uploads/2012/05/Esxtop_Troubleshooting_eng.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmworld.net/wp-content/uploads/2012/05/Esxtop_Troubleshooting_eng.pdf']);">this</a> pdf:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_cpu_performance/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_cpu_performance/']);" rel="attachment wp-att-5282"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_cpu_performance.png" alt="esxtop cpu performance VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="864" height="370" class="alignnone size-full wp-image-5282" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

Here is a good summary:

> %RDY: Percentage of time a VM was waiting to be scheduled. Possible reasons: too many vCPUs, too many vSMP VMs or a CPU limit setting (Trouble when >10)  
> %CSTP: Percentage of time a ready to run VM has spent in co-descheduling state (Trouble when > 3 to resolve, decrease number of vCPUs on the VM)  
> $MLMTD: Percentage of time a ready to vCPU was no schedules because of a CPU limit setting (Trouble when > 1, to resolve; remove the CPU limit)  
> $SWPWT: How Long a VM has to wait for swapped pages read from disk. (Trouble when > 5, possible reason; memory overcommitment 

Also this is from a 4.x document but it applies to 5.0 as well. Here is the document: &#8220;<a href="http://communities.vmware.com/servlet/JiveServlet/previewBody/14905-102-2-17952/vsphere41-performance-troubleshooting.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://communities.vmware.com/servlet/JiveServlet/previewBody/14905-102-2-17952/vsphere41-performance-troubleshooting.pdf']);">Performance Troubleshooting for VMware vSphere 4.1</a>&#8220;. From that document:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_for_host_cpu_saturation/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_for_host_cpu_saturation/']);" rel="attachment wp-att-5292"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/check_for_host_cpu_saturation.png" alt="check for host cpu saturation VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="640" height="536" class="alignnone size-full wp-image-5292" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

Here is a similar diagram for Guest CPU saturation:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_for_guest_cpu_saturation/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_for_guest_cpu_saturation/']);" rel="attachment wp-att-5293"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/check_for_guest_cpu_saturation.png" alt="check for guest cpu saturation VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="588" height="299" class="alignnone size-full wp-image-5293" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

### Troubleshoot ESXi host and Virtual Machine memory performance issues using appropriate metrics

From <a href="http://www.vmworld.net/wp-content/uploads/2012/05/Esxtop_Troubleshooting_eng.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmworld.net/wp-content/uploads/2012/05/Esxtop_Troubleshooting_eng.pdf']);">this</a> pdf:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_memory_issues/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/esxtop_memory_issues/']);" rel="attachment wp-att-5294"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/esxtop_memory_issues.png" alt="esxtop memory issues VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="746" height="421" class="alignnone size-full wp-image-5294" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

Here is a good summary:

> MCTLSZ: Amount of guest physical memory (MB) the ESXi Host is reclaiming by balloon driver. (Trouble when > 1)  
> ZIP/s: Values larger than 0 indicates that the host is actively compressing memory (Trouble when > 1)  
> UNZIP/s: Values larger than 0 indicate that the host is accessing compressed memory (Reason for this behavior is memory overcommitment)  
> SWCUR: Memory (in MB) that has been swapped by VMkernel (Possible cause is memory overcommitment, Trouble when > 1)  
> CACHEUSD: Memory (in MB) compressed by ESXi Host (Trouble when > 1)  
> SWR/s SWW/s: Rate at which the ESXi host is writing to or reading from swapped memory (Trouble when > 1) 

And from &#8220;<a href="http://communities.vmware.com/servlet/JiveServlet/previewBody/14905-102-2-17952/vsphere41-performance-troubleshooting.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://communities.vmware.com/servlet/JiveServlet/previewBody/14905-102-2-17952/vsphere41-performance-troubleshooting.pdf']);">Performance Troubleshooting for VMware vSphere 4.1</a>&#8220;:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_for_vm_swapping/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_for_vm_swapping/']);" rel="attachment wp-att-5297"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/check_for_vm_swapping.png" alt="check for vm swapping VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="621" height="424" class="alignnone size-full wp-image-5297" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

and here is another flow chart for VM memory issues:

<a href="http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_vm_fo_compression/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/vcap5-dca-objective-6-2-troubleshoot-cpu-and-memory-performance/check_vm_fo_compression/']);" rel="attachment wp-att-5298"><img src="http://virtuallyhyper.com/wp-content/uploads/2012/12/check_vm_fo_compression.png" alt="check vm fo compression VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " width="629" height="427" class="alignnone size-full wp-image-5298" title="VCAP5 DCA Objective 6.2 – Troubleshoot CPU and Memory Performance " /></a>

### Use Hot-Add functionality to resolve identified Virtual Machine CPU and memory performance issues

If you discover then the VM needs more resources, then follow the instruction laid out in <a href="http://virtuallyhyper.com/2012/11/vcap5-dca-objective-3-2-optimize-virtual-machine-resources/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/11/vcap5-dca-objective-3-2-optimize-virtual-machine-resources/']);">VCAP5-DCA Objective 3.2</a> to hot add memory or CPU

