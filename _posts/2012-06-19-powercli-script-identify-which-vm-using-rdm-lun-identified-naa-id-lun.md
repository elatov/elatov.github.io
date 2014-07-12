---
published: true
title: PowerCLI Script to Identify Which VM is using an RDM LUN Identified by the NAA-ID of the LUN
author: Karim Elatov
layout: post
permalink: /2012/06/powercli-script-identify-which-vm-using-rdm-lun-identified-naa-id-lun/
categories: ['vmware', 'storage']
tags: ['naa_id', 'powercli', 'rdm', 'vmkfstools', 'vml_id']
---

I recently had a interesting query: "Given the naa_id of a LUN which is an RDM, how do you find which VM that LUN is connected to?" Doing some quick searching in the VMware KB, I found VMware articles [1005937](http://kb.vmware.com/kb/1005937) had a powercli script which showed the size of the RDM and the full path of the RDM:


	Get-Datastore | Get-HardDisk -DiskType "RawPhysical","RawVirtual" | Select "Filename","CapacityKB" | fl


Sample ouput:

> Filename : [DatastoreName] DirectoryName/virtualrdm.vmdk
> CapacityKB : 5760

Although helpful, but not exactly what we were looking for. The same KB ([1005937](http://kb.vmware.com/kb/1005937)) also had a way of doing through the command line of the esx host:


	~ # find /vmfs/volumes/ -type f -name '*.vmdk' -size -1024k -exec grep -l '^createType=.*RawDeviceMap' {} \; | xargs -L 1 vmkfstools -q


Sample output:

> Virtual Mode RDM:
>
> Disk /vmfs/volumes/.../virtualrdm.vmdk is a Non-passthrough Raw Device Mapping
> Maps to: vml.02000000006006048000019030091953303030313253594d4d4554
>
> Physical Mode RDM:
>
> Disk /vmfs/volumes/.../physicalrdm.vmdk is a Passthrough Raw Device Mapping
> Maps to: vml.02000000006006048000019030091953303030313253594d4d4554

This is perfect however this had to be run on each individual host since there is lock on the vmdk files from the host where the VM resides. Again helpful but a lot work. In the second KB [2001823](http://kb.vmware.com/kb/2001823 ), there was another powercli script:


	Get-VM | Get-HardDisk -DiskType "RawPhysical","RawVirtual" | Select Parent,Name,DiskType,ScsiCanonicalName,DeviceName | fl


Sample output:

> Parent:                           Virtual Machine Display Name
> Name:                            Hard Disk n
> DiskType:                       RawVirtual
> ScsiCanonicalName:       naa.60123456789abcdef0123456789abcde
> DeviceName:                  vml.020000000060123456789abcdef0123456789abcde1234567890ab

This was actually very close but it listed all the VMs with an RDM disk, where we wanted to just find one LUN. I took the above command and rewrote it to be a little bit more comprehensive. Here is what I ended up with:


	# define the IP of your vCenter
	$vc = "10.x.x.x"
	# Connect to your vCenter, this will ask your for your credentials
	# * you can pass in the user and password parameters, but I left those out
	Connect-VIserver $vc
	# Get the list of all the VMs in the Vcenter Inventory
	$vms = Get-VM
	# Iterate over all the VMs
	foreach ($vm in $vms){
	# Iterate over each hard-disk of each VM that is a virtual or Physical RDM
	foreach ($hd in ($vm | Get-HardDisk -DiskType "RawPhysical","RawVirtual" )){
	# Check to see if a certain hard disk matches our naa_id
	if ( $hd.ScsiCanonicalName -eq "naa.600601607290250060ae06da248be111"){
	# Print out VM Name
	write $hd.Parent.Name
	# Print Hard Disk Name
	write $hd.Name
	# Print Hard Disk Type
	write $hd.DidkType
	# Print NAA Device ID
	write $hd.ScsiCanonicalName
	# Print out the VML Device ID
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

### Related Posts

- [Determine Disk VPD Information from ESX Classic](/2012/08/determine-disk-vpd-information-from-esx-classic/)

