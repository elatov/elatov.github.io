---
title: PSOD Failed at vmkdrivers/src_9/vmklinux_9/vmware/linux_scsi.c:2221 — NOT REACHED
author: Karim Elatov
layout: post
permalink: /2012/08/psod-failed-at-vmkdriverssrc_9vmklinux_9vmwarelinux_scsi-c2221-not-reached/
dsq_thread_id:
  - 1404673225
categories:
  - VMware
tags:
  - esxcfg-info
  - IBM x3690 X5
  - LSI2008
  - mpt2sas
  - PSOD
---
I recently ran into the following PSOD:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/psod-lsi-.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/psod-lsi-.png']);"><img class="alignnone size-full wp-image-3079" title="psod-lsi-" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/psod-lsi-.png" alt="psod lsi  PSOD Failed at vmkdrivers/src 9/vmklinux 9/vmware/linux scsi.c:2221 — NOT REACHED" width="1163" height="677" /></a>

Some other people in the VMware communities have seen the same PSOD. Here is a <a href="http://communities.vmware.com/message/2102510" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/message/2102510']);">link</a> to the communities page. We are crashing at:

	  
	Failed at vmkdrivers/src_9/vmklinux_9/vmware/linux_scsi.c:2221 -- NOT REACHED  
	

It looks like the local disk driver is having an issue. Checking out the host's local controllers, I saw the following:

	  
	~ # lspci | grep vmhba  
	000:000:31.2 Mass storage controller: Intel Corporation ICH10 4 port SATA IDE Controller [vmhba0]  
	000:004:00.0 Mass storage controller: LSI Logic / Symbios Logic LSI2008 [vmhba1]  
	000:014:00.0 Mass storage controller: LSI Logic / Symbios Logic MegaRAID SAS SKINNY Controller [vmhba2]  
	000:019:00.0 Mass storage controller: LSI Logic / Symbios Logic LSI2008 [vmhba3]  
	

Checking for the device drivers and the Vendor IDs, I see the following:

	  
	~ # esxcfg-info -a | sed -n '/SCSI\ Interface/,/BAR\ Info/p' | grep 'Name.*vmhba1' -A 16 | egrep 'Name|Driver|Vendor\ Id|Device\ Id|Sub-Vendor\ Id|Sub-Device\ Id'  
	|----Name............................................vmhba1  
	|----Driver..........................................mpt2sas  
	|----Vendor Id....................................0x1000  
	|----Device Id....................................0x0072  
	|----Sub-Vendor Id................................0x1014  
	|----Sub-Device Id................................0x03ca  
	

vmhba3 was the same as above, and here is what I saw for vmhba2:

	  
	~ # esxcfg-info -a | sed -n '/SCSI\ Interface/,/BAR\ Info/p' | grep 'Name.*vmhba2' -A 16 | egrep 'Name|Driver|Vendor\ Id|Device\ Id|Sub-Vendor\ Id|Sub-Device\ Id'  
	|----Name............................................vmhba2  
	|----Driver..........................................megaraid_sas  
	|----Vendor Id....................................0x1000  
	|----Device Id....................................0x0073  
	|----Sub-Vendor Id................................0x1014  
	|----Sub-Device Id................................0x03b1  
	

So we are using the mpt2sas and megaraid_sas drivers for our local drives. Here is HCL <a href="http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=13971&deviceCategory=io&VID=1000&DID=0072&SVID=0000&SSID=0000&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=13971&deviceCategory=io&VID=1000&DID=0072&SVID=0000&SSID=0000&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc']);">link</a> for vmhba1 and here is the <a href="http://partnerweb.vmware.com/comp_guide2/detail.php?deviceCategory=io&productid=12373&deviceCategory=io&VID=1000&DID=0073&SVID=1014&SSID=03b1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://partnerweb.vmware.com/comp_guide2/detail.php?deviceCategory=io&productid=12373&deviceCategory=io&VID=1000&DID=0073&SVID=1014&SSID=03b1&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc']);">link</a> for vmhba2.

For vmhba1:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/hcl-vmhba1.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/hcl-vmhba1.png']);"><img class="alignnone size-full wp-image-3084" title="hcl-vmhba1" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/hcl-vmhba1.png" alt="hcl vmhba1 PSOD Failed at vmkdrivers/src 9/vmklinux 9/vmware/linux scsi.c:2221 — NOT REACHED" width="939" height="420" /></a>

and for vmhba2:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/hcl-vmhba2.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/hcl-vmhba2.png']);"><img class="alignnone size-full wp-image-3085" title="hcl-vmhba2" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/hcl-vmhba2.png" alt="hcl vmhba2 PSOD Failed at vmkdrivers/src 9/vmklinux 9/vmware/linux scsi.c:2221 — NOT REACHED" width="939" height="421" /></a>

Here is our hardware and VMware versions:

	  
	~ # vmware -l  
	VMware ESXi 5.0.0 GA
	
	~ # $ vsish -e cat /hardware/bios/dmiInfo | head -3  
	System Information (type1) {  
	Product Name:System x3690 X5 -[7147AC1]-  
	Vendor Name:IBM
	
	~ # $ vsish -e cat /hardware/bios/biosInfo  
	BIOS Information (type 0) {  
	BIOS Version:-[MLE170CUS-1.70]-  
	BIOS Release Date:09/23/2011  
	}  
	

So we are running ESXi 5.0GA on a IBM x3690 X5 host. Very close to the same guy from <a href="http://communities.vmware.com/message/2101833" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://communities.vmware.com/message/2101833']);">this</a> VMware communities page. Now from the HCL we can see that for vmhba2 the recommended version of the driver is:

> megaraid_sas version 4.32-1vmw

Now checking the version on the host, I saw the following:

	  
	~ # esxcli software vib list | grep megaraid-sas  
	scsi-megaraid-sas 4.32-1vmw.500.1.11.469512 VMware VMwareCertified 2012-02-28  
	

The recommended version for vmhba1 and vmhba3 is :

> mpt2sas version 06.00.00.00-5vmw

Checking the current version, I saw the following:

	  
	~ # esxcli software vib list | grep mpt2sas  
	scsi-mpt2sas 06.00.00.00-6vmw.500.1.11.469512 VMware VMwareCertified 2012-02-28  
	

So we were at the latest version for both. Searching for the available mpt2sas drivers from the VMware downloads page, I saw the following:

<a href="http://virtuallyhyper.com/wp-content/uploads/2012/08/mp2sas-drivers.png" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/wp-content/uploads/2012/08/mp2sas-drivers.png']);"><img class="alignnone size-full wp-image-3086" title="mp2sas-drivers" src="http://virtuallyhyper.com/wp-content/uploads/2012/08/mp2sas-drivers.png" alt="mp2sas drivers PSOD Failed at vmkdrivers/src 9/vmklinux 9/vmware/linux scsi.c:2221 — NOT REACHED" width="717" height="734" /></a>

So these version of the drivers are available:

> 10.10.10.01.vmw  
> 10.10.21.00.1vmw  
> 11.00.00.00.2vmw  
> 12.00.00.00.1vmw  
> 13.00.00.00.1vmw  
> 13.10.02.00.1vmw  
> 14.00.00.00.1vmw

Even though version "13.10.02.00.1vmw" wasn't on HCL for this device, we went ahead and installed it on our hardware and the PSODs haven't happened for over two weeks now. Here is the <a href="https://my.vmware.com/web/vmware/details?downloadGroup=DT-ESXI50-LSI-mpt2sas-131002001vmw&productId=24" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://my.vmware.com/web/vmware/details?downloadGroup=DT-ESXI50-LSI-mpt2sas-131002001vmw&productId=24']);">link</a> to that driver. Hopefully this helps someone out.

