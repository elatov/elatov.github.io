---
published: true
title: '"Thin on Thin" With VMware Thin Provisioned Disks and EMC Symmetrix Virtual Provisioning'
author: Karim Elatov
layout: post
permalink: /2012/04/thin-on-thin-with-vmware-thin-provisioned-disks-and-emc-symmetrix-virtual-provisioning/
categories: ['storage', 'vmware']
tags: ['thick_provisioning', 'thin_provisioning', 'vmfs', 'vmdk']
---

Recently, someone me asked with the following question.

> I added a VM and didn't specify an option for thin or thick, which should result in zeroedthick rather than eagerzerothick. I added a new VM w/250GB disk. It takes no space on the Symmetrix LUN, but takes 250GB from the 500 GB LUN on VMware. One more 250GB disk like this and there would be no free space to VMWare, but 500 GB still free on Symmetrix. What am I missing?

This VMware article [Dynamic Storage Provisioning](http://www.vmware.com/techpapers/2009/dynamic-storage-provisioning-10073.html) has a good table of what some differences between the VMware disk provisioning types are:

> {:.kt}
> |VMDK Format| Space Dedicated| Zeroed Out Blocks|Incremental Growth|
> |-----------|----------------|------------------|------------------|
> | Thin      | Reservation only| As it Grows     |1 VMFS block at a time|
> |Zeroed Thick| Full Amount   | As It Grows      | No               |
> |Eager Zeroed Thick| Zeroed Thick| At Creation Time| No            |

The most confusing one might be the thin vmdk and this article [Implementing EMC Symmetrix Virtual Provisioning with VMware vShpere](https://dl.dropboxusercontent.com/u/24136116/blog_pics/thin-thin-symm/h2529vmwareesxsvrwsymmetrixwp.pdf). The article has good description why the above is expected:

> The "Thick Provision Lazy Zeroed" or “Thick” selection is actually the "zeroedthick" format. In this allocation scheme, the storage required for the virtual disks is reserved in the datastore but the VMware kernel does not initialize all the blocks. The blocks are initialized by the guest operating system as write activities to
> previously uninitialized blocks are performed. The VMFS will return zeros to the guest operating system if it attempts to read blocks of data that it has not previously written to.
> ...
> ...
> The virtual disks will not require more space on the VMFS volume as their reserved size is static with this allocation mechanism and more space will be needed only if additional virtual disks are added. Therefore, the only free capacity that must be monitored diligently is the free capacity on the thin pool itself.
> ...
> ...
> since the VMware kernel does not actually initialize unused blocks, the full 10 GB is not consumed on the thin device

So even though we create a thick vmdk it's not zeroed out (like eager-zeroed thick would be) and therefore the thin provisioned LUN will show that the total used space on the LUN is only the size of the pre-allocated space of the thick vmdk (not the total vmdk size). Now for VMFS, thick is thick, so it will show the utilized space as the total space of the thick disk even though it's not pre-allocated.
Going back to original question, what type of vmdk format would only show the used(zeroed out) space both on VMFS and on a thin provisioned LUN? That would be a thin vmdk on a thin (virtuallly) provisioned LUN. It used to be best practice to do thick vmdks on thin provisioned LUNS, per [Using EMC Symmetrix Storage in VMware vSphere Environments](http://www.emc.com/collateral/hardware/solution-overview/h2529-vmware-esx-svr-w-symmetrix-wp-ldv.pdf):

> Virtual disk type recommendations
> In general, before vSphere 4.1, EMC recommended using “zeroedthick” instead of “thin” virtual disks when using Symmetrix Virtual Provisioning. The reason that “thin on thin” was not always recommended is that using thin provisioning on two separate layers (host and array) increases the risk of out-of-space conditions for the virtual machines. vSphere 4.1 (and even more so in vSphere 5) in conjunction with the latest release of Enginuity integrate these layers better than ever. Consequently, using thin on thin is now acceptable in far more situations, but it is important to remember that risks still remain in doing so. For this reason, EMC recommends “zeroedthick” (for better reliability as only the array must be monitored) or “eagerzeroedthick” (for absolute reliability as all space is completely reserved) for mission critical virtual machines.

But this has changed, thin on thin can be used as long as you properly monitor your space usage. From the [Implementing EMC Symmetrix Virtual Provisioning with VMware vSphere](http://www.vmware.com/files/pdf/techpaper/wp_symmetrix_virtual_provisioning_vsphere4.pdf):

> Like zeroedthick, the "thin" allocation mechanism is also Virtual Provisioning-friendly, but, as will be explained in this section, should only be used with caution in conjunction with Symmetrix Virtual Provisioning. "Thin" virtual disks increase the efficiency of storage utilization for virtualization environments by using only the amount of underlying storage resources needed for that virtual disk, exactly like zeroedthick. But unlike zeroedthick, thin devices do not reserve space on the VMFS volume-allowing more virtual disks per VMFS. Upon the initial provisioning of the virtual disk, the disk is provided with an allocation equal to one block size worth of storage from the datastore. As that space is filled, additional chunks of storage in multiples of the VMFS block size are allocated for the virtual disk so that the underlying storage demand will grow as its size increases.
> ..
> ..
> However, as previously mentioned, VMware and EMC have recently ameliorated the practicality of using thin virtual disks with Symmetrix Virtual Provisioning. This has been achieved through:
>
> 1.  Refining vCenter and array reporting while also widening the breadth of directSymmetrix integration through features such as the vStorage API for StorageAwareness (VASA—vSphere 5 only).
> 2.  Removing the slight performance overhead that existed with thin VMDKs. This was caused by zeroing-on-demand and intermittent expansion of the virtual disk as new blocks were written to by the guest OS and has been respectively significantly diminished with the advent of Block Zero and Hardware-Assisted Locking (ATS).
> 3.  The introduction of Storage Dynamic Resource Scheduler in vSphere 5 (SDRS) further reduces the risk of running out of space on a VMFS volume as it can be configured to migrate virtual machines from a datastore when that datastore reaches a user-specified percent-full threshold. This all but eliminates the risk of running out of space on VMFS volumes, with the only assumption being that there is available capacity elsewhere to move the virtual machines to.
>
> These improvements can make "thin on thin" a much more viable option—especially in vSphere 5. Essentially, it depends on how risk-averse an organization is and the importance/priority of an application running in a virtual machine. If virtual machine density and storage efficiency is valued above the added protection provided by a thick virtual disk (or simply the possible risk of an out-of-space condition is acceptable), “thin on thin” may be used. If "thin on thin" is used, alerts on the vCenter level and the array level should be configured.

The same article has a section entitled "Thin pool management" and it has great examples on how to configure the array and vCenter to monitor the space usage of a thin Lun. All in all, using thin provisioned vmdks on thin provisioned LUNs is not a bad thing as long as you running ESX 4.1 or above and you monitor the disk usage appropriately. Here are some blogs that talk about similar topics: [VMware Thin Disks on EMC Virtual Provisioning](http://virtualgeek.typepad.com/virtual_geek/2009/04/thin-on-thin-where-should-you-do-thin-provisioning-vsphere-40-or-array-level.html).

Along the same topic, sometimes performance between thick and thin VMDKs comes up. There is a good study that was done regarding that: [Performance Study of VMware vStorage Thin Provisioning](http://www.vmware.com/pdf/vsp_4_thinprov_perf.pdf). I don't want to get side tracked, so I might discuss that specific topic in another post.

### Related Posts

- [VMFS Datastore not Auto-Mounting on an ESX(i) Host because the VMFS Partition is Overwritten](/2012/09/vmfs-datastore-not-auto-mounting-on-an-esxi-host/)

