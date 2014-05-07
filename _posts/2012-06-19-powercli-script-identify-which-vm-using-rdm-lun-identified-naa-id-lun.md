---
title: PowerCLI Script to Identify Which VM is using an RDM LUN Identified by the NAA-ID of the LUN
author: Karim Elatov
layout: post
permalink: /2012/06/powercli-script-identify-which-vm-using-rdm-lun-identified-naa-id-lun/
dsq_thread_id:
  - 1404673258
categories:
  - VMware
  - vTip
tags:
  - NAA_ID
  - Physical RDM
  - powercli
  - RDM
  - Virtual RDM
  - vmkfstools
  - VML_ID
---
I recently had a interesting query: &#8220;Given the naa_id of a LUN which is an RDM, how do you find which VM that LUN is connected to?&#8221; Doing some quick searching in the VMware KB, I found VMware articles <a href="http://kb.vmware.com/kb/1005937" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005937']);">1005937</a> and <a href="http://kb.vmware.com/kb/2001823 " onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2001823']);">2001823</a>. KB <a href="http://kb.vmware.com/kb/1005937" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005937']);">1005937</a> had a powercli script which showed the size of the RDM and the full path of the RDM:

	  
	Get-Datastore | Get-HardDisk -DiskType "RawPhysical","RawVirtual" | Select "Filename","CapacityKB" | fl  
	

Sample ouput:

> Filename : [DatastoreName] DirectoryName/virtualrdm.vmdk  
> CapacityKB : 5760

Although helpful, but not exactly what we were looking for. The same KB (<a href="http://kb.vmware.com/kb/1005937" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1005937']);">1005937</a>) also had a way of doing through the command line of the esx host:

	  
	~ # find /vmfs/volumes/ -type f -name '\*.vmdk' -size -1024k -exec grep -l '^createType=.\*RawDeviceMap' {} \; | xargs -L 1 vmkfstools -q  
	

Sample output:

> Virtual Mode RDM:
> 
> Disk /vmfs/volumes/&#8230;/virtualrdm.vmdk is a Non-passthrough Raw Device Mapping  
> Maps to: vml.02000000006006048000019030091953303030313253594d4d4554
> 
> Physical Mode RDM:
> 
> Disk /vmfs/volumes/&#8230;/physicalrdm.vmdk is a Passthrough Raw Device Mapping  
> Maps to: vml.02000000006006048000019030091953303030313253594d4d4554

This is perfect however this had to be run on each individual host since there is lock on the vmdk files from the host where the VM resides. Again helpful but a lot work. In the second KB <a href="http://kb.vmware.com/kb/2001823 " onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/2001823']);">2001823</a>, there was another powercli script:

	  
	Get-VM | Get-HardDisk -DiskType "RawPhysical","RawVirtual" | Select Parent,Name,DiskType,ScsiCanonicalName,DeviceName | fl  
	

Sample output:

> Parent:                           Virtual Machine Display Name  
> Name:                            Hard Disk n  
> DiskType:                       RawVirtual  
> ScsiCanonicalName:       naa.60123456789abcdef0123456789abcde  
> DeviceName:                  vml.020000000060123456789abcdef0123456789abcde1234567890ab

This was actually very close but it listed all the VMs with an RDM disk, where we wanted to just find one LUN. I took the above command and rewrote it to be a little bit more comprehensive. Here is what I ended up with:

	  
	\# define the IP of your vCenter  
	$vc = "10.x.x.x"  
	\# Connect to your vCenter, this will ask your for your credentials  
	\# * you can pass in the user and password parameters, but I left those out  
	Connect-VIserver $vc  
	\# Get the list of all the VMs in the Vcenter Inventory  
	$vms = Get-VM  
	\# Iterate over all the VMs  
	foreach ($vm in $vms){  
	\# Iterate over each hard-disk of each VM that is a virtual or Physical RDM  
	foreach ($hd in ($vm | Get-HardDisk -DiskType "RawPhysical","RawVirtual" )){  
	\# Check to see if a certain hard disk matches our naa_id  
	if ( $hd.ScsiCanonicalName -eq "naa.600601607290250060ae06da248be111"){  
	\# Print out VM Name  
	write $hd.Parent.Name  
	\# Print Hard Disk Name  
	write $hd.Name  
	\# Print Hard Disk Type  
	write $hd.DidkType  
	\# Print NAA Device ID  
	write $hd.ScsiCanonicalName  
	\# Print out the VML Device ID  
	write $hd.DeviceName  
	}  
	}  
	}  
	

Sample output:

> VM_Name  
> Hard disk 2  
> naa.600601607290250060ae06da248be111  
> vml.0200000000600601607290250060ae06da248be111524149442035

If you prefer one liners, there is a version for that:

	  
	Get-VM | Get-HardDisk -DiskType "RawPhysical","RawVirtual" | where { $_.ScsiCanonicalName -eq  
	"naa.600601607290250060ae06da248be111"} | Select Parent,Name,DiskType,ScsiCanonicalName,DeviceName | fl  
	

Sample Output:

> Parent : VM_Name  
> Name : Hard disk 2  
> DiskType : RawPhysical  
> ScsiCanonicalName : naa.600601607290250060ae06da248be111  
> DeviceName : vml.0200000000600601607290250060ae06da248be111524149442035

Hope this helps someone out.

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="Determine Disk VPD Information from ESX Classic" href="http://virtuallyhyper.com/2012/08/determine-disk-vpd-information-from-esx-classic/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/08/determine-disk-vpd-information-from-esx-classic/']);" rel="bookmark">Determine Disk VPD Information from ESX Classic</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/06/powercli-script-identify-which-vm-using-rdm-lun-identified-naa-id-lun/" title=" PowerCLI Script to Identify Which VM is using an RDM LUN Identified by the NAA-ID of the LUN" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:NAA_ID,Physical RDM,powercli,RDM,Virtual RDM,vmkfstools,VML_ID,blog;button:compact;">ESX issues an INQUIRY to get the list of supported Vital Product Data (VPD) pages. If page 83 is supported, ESX issues an INQUIRY on that page and extracts an...</a>
</p>