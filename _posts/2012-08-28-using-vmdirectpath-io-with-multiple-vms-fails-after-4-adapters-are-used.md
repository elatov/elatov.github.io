---
title: Using VMDirectPath I/O with Multiple VMs Fails After 4 Adapters are Used
author: Jarret Lavallee
layout: post
permalink: /2012/08/using-vmdirectpath-io-with-multiple-vms-fails-after-4-adapters-are-used/
dsq_thread_id:
  - 1404673832
categories:
  - OS
  - Storage
  - VMware
tags:
  - Emulex
  - interrupt vectors
  - IOAPIC
  - IRQ
  - LPe12000
  - MSI
  - MSI-X
  - Passthrough
  - PCI
  - VMDirectPath I/O
  - vsish
---
I recently had a customer that was using <a href="http://kb.vmware.com/kb/1010789" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1010789']);" target="_blank">VMDirectPath I/O</a> to pass through multiple Emulex LPe12000&#8242;s to a few VMs. They were doing this because they needed to present and unpresent thousands of LUNs to the VMs. Since the ESXi hosts have a limitation of 255 LUNs, they would need to pass through the whole HBA. VMDirectPath I/O is experimentally supported for multiple devices, the LPe12000 HBA is one of them. This <a href="http://www.simonlong.co.uk/blog/2009/08/03/vmware-vmdirectpath-io/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.simonlong.co.uk/blog/2009/08/03/vmware-vmdirectpath-io/']);" target="_blank">blog post</a> goes over more details on VMDirectPath I/O.

The problem was that when they have 4 Windows VMs with 2 adapters passed through, all of the HBAs would no longer log into the fabric. If they had 2 of the VMs running Linux and the other 2 running Windows they did not experience the problem. So right off the bat we know that this is a problem that is trigger by the Windows driver.

First thing I did was check the ESXi 5 <a href="http://www.vmware.com/pdf/vsphere5/r50/vsphere-50-configuration-maximums.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/vsphere5/r50/vsphere-50-configuration-maximums.pdf']);" target="_blank">Configuration Maximums</a>.

> **VMDirectPath limits**  
> VMDirectPath PCI/PCIe devices per host 8  
> VMDirectPath PCI/PCIe devices per virtual machine 4

We can see that there can be up to 4 Pass through PCI devices per VM with a maximum of 8 on the host. This customer was using a total of 8 devices.

We booted one of the Windows VMs and all of the HBAs dropped off the fabric. Looking in the vmkernel.log we see the messages below.

	  
	2012-08-07T07:57:31.269Z cpu9:739725)WARNING: IntrVector: 290: Out of interrupt vectors  
	2012-08-07T07:57:31.269Z cpu9:739725)MSI: 570: Couldn't allocate a vector number 16 for device 000:008:00.0  
	2012-08-07T07:57:31.269Z cpu9:739725)VMKPCIPassthru: 2454: Failed to allocate 32 MSIX vectors  
	2012-08-07T07:57:49.787Z cpu12:739725)VMKPCIPassthru: 2500: BDF = 008:00.1 intrType = 4 numVectors: 32  
	2012-08-07T07:57:49.787Z cpu12:739725)WARNING: IntrVector: 290: Out of interrupt vectors  
	

From the logs above, we can see that the host cannot allocate enough interrupt vectors for the device. The device is asking for 32 MSI-X vectors. So the Windows driver is likely allocating all of the vectors up front, so I wanted to see how many vectors the host can allocate.

	  
	\# vsish -e ls /hardware/interrupts/vectorList/ |wc -l  
	170
	
	

So this ESXi host has about 170 vectors (some are shared) to allocate. With 8 devices requesting 32 vectors it would need 256. MSIs are all <a href="http://publib.boulder.ibm.com/infocenter/pseries/v5r3/index.jsp?topic=/com.ibm.aix.kernelext/doc/kernextc/interrupts.htm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://publib.boulder.ibm.com/infocenter/pseries/v5r3/index.jsp?topic=/com.ibm.aix.kernelext/doc/kernextc/interrupts.htm']);" target="_blank">edge-triggered interrupts</a>, so they cannot be shared, thus requiring 256 unique vectors.

It was clear that the problem is an overallocation of vectors with the Windows driver. The resolution was to lower the interrupt vector allocation for the windows driver. In the <a href="http://www.vmware.com/files/pdf/techpaper/vsp_4_vmdirectpath_host.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/files/pdf/techpaper/vsp_4_vmdirectpath_host.pdf']);" target="_blank">VMDirectPath I/O Troubleshooting Guide</a> we see the following:

> Setting pciPassthru0.msiEnabled = &#8220;FALSE&#8221; sets the physical mode to IOAPIC, if the virtual mode is  
> IOAPIC. The default setting for this option is TRUE, which means physical mode is MSI or MSI‐X. The default works for most supported configurations. In some cases, however, you need to change the default

We edited the VMs and set the physical mode to IOAPIC, but this did not help. We were still seeing the allocation errors as above. We then tried other various options with no avail. We decided that we needed to disable MSI-X on the driver inside Windows. I stumbled upon <a href="http://www.emulex.com/knowledge/search/viewArticle.jsp?docId=79" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.emulex.com/knowledge/search/viewArticle.jsp?docId=79']);" target="_blank" class="broken_link">this KB article</a>, which pointed to the wrong registry keys, but gave us the correct location.

On each of the Windows VMs, we opened up regedit browsed to the location of the HBA and disabled MSI-X with the following (Sorry I forgot to take a screen shot).

1.  Expand HKEY\_LOCAL\_MACHINE
2.  Expand SYSTEM
3.  Expand CurrentControlSet
4.  Expand ENUM
5.  Expand PCI
6.  Expand the VEN10DF* key
7.  Expand the device for each port. Each port will have a UUID something like 1293873984724-193247931123
8.  Expand MessageSignaledInterrupts
9.  Click on Properties
10. Change MSIEnabled to 0 from 1.

After changing the setting on all of the ports, we rebooted the VM and the LPe12000&#8242;s were able to log into the fabric across all of the VMs.

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/08/using-vmdirectpath-io-with-multiple-vms-fails-after-4-adapters-are-used/" title=" Using VMDirectPath I/O with Multiple VMs Fails After 4 Adapters are Used" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:Emulex,interrupt vectors,IOAPIC,IRQ,LPe12000,MSI,MSI-X,Passthrough,PCI,VMDirectPath I/O,vsish,blog;button:compact;">I recently had a customer that was using VMDirectPath I/O to pass through multiple Emulex LPe12000&#8242;s to a few VMs. They were doing this because they needed to present and...</a>
</p>