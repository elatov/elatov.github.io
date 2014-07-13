---
title: Experiencing PSODs on HP 465C G7 Blades with NC551i NICs
author: Karim Elatov
layout: post
permalink: /2012/11/experiencing-psods-on-hp-465c-g7-blades-with-nc551i-nics/
categories: ['networking', 'vmware']
tags: ['be2net', 'emulex', 'psod']
---

After updating our HP Virtual Connect firmware to version 3.60, our ESXi host we would see the following PSOD after a certain amount of time:

![psod_be2net_manu_c](https://github.com/elatov/uploads/raw/master/2012/11/psod_be2net_manu_c.png)

Here is the actual backtrace:


	0x412200cc7cb0:[0x418017c9ae9c]Util_Udelay'@'vmkernel#nover+0x2f stack: 0x412200010005
	0x4122012c7d20:[0x41801d247c34]be_mcc_mailbox_notify_and_wait'@'#+0x3f stack: 0x0
	0x4122012c7d50:[0x41801d248219]_be_mpu_post_wrb_mailbox'@'#+0x84 stack: 0x0
	0x412200cc7d50:[0x4180182458b7]be_function_post_mcc_wrb'@'#+0x126 stack: 0x41000f4281d0
	0x412c42c5a990:[0x41800f30183b]be_cq_create'@'#+0x284 stack: 0x4103ba1f1150
	0x412200cc7dc0:[0x4180182460e3]ring_sets_setup'@'#+0x62c stack: 0x41801903b5a9
	0x412c42c5aab0:[0x41800f2f0677]be_probe'@'#+0x15e stack: 0x41038d679978
	0x412c42c5ab40:[0x41800f15cc6d]pci_announce_device'@'com.vmware.driverAPI#9.2+0x94 stack: 0x417f00000
	0x412c42c5ab40:[0x41800f15cfe3]__pci_register_driver'@'com.vmware.driverAPI#9.2+0x152 stack: 0x417fce
	0x412c42c5aba0:[0x41800f30ae5f]be_init_module'@'#+0x2e stack: 0x42c5abd0
	0x412c42c5ac30:[0x41800e6d7a06]Mod_LoadDone'@'vmkernel#nover+0x355 stack: 0xffff
	0x412c42c5add0:[0x41800e678e88]Elf_LoadMod'@'vmkernel#nover+0x280f stack: 0x410393b2b7d0
	0x412c42c5ae50:[0x41800ef548d9]UWVMKSyscallUnpackLoadVMKModule'@'#+0x1b4 stack: 0x412c42c
	0x412c42c5aef0:[0x41800eeb8470]User_UWVMKSyscallHandler'@'#+0x1b3 stack: 0x0
	0x412c42c5af10:[0x41800e7192c2]User_UWVMKSyscallHandler'@'vmkernel#nover+0x19 stack: 0xffacfcdc
	0x412c42c5af20:[0x41800e78c073]gate_entry'@'vmkernel#nover+0x72 stack: 0x0


Whenever you see a *be* in the backtrace, that is the *be2net* driver causing the issue. We had the following versions of the NIC and OS:

{:.kt}
|ESX_Version| NIC_Model| NIC_Driver| NIC_Firmware|
|-----------|----------|-----------|-------------|
|5.0U1 Build 623860| NC551i| be2net 4.0.88| 4.0.0150|


Here is the link to the [October 2012 VMware FW and Software Recipe](http://www.vmware.com/resources/compatibility/detail.php?deviceCategory=io&productid=19068&deviceCategory=io&VID=19a2&DID=0700&SVID=103c&SSID=3314&page=1&display_interval=10&sortColumn=Partner&sortOrder=Asc)" page and I saw the following recommendation:

![hp_reciopes_nc551i](https://github.com/elatov/uploads/raw/master/2012/11/hp_reciopes_nc551i.png)

So I decided to install be2net driver 4.1.334.48, here is a [link](https://my.vmware.com/web/vmware/details?downloadGroup=DT-ESX50-EMULEX-be2net-4133448&productId=285) to that. I didn't want to go to the latest firmware just yet. So after all was said and done, I had the following driver/firmware combination:

{:.kt}
|ESX_Version| NIC_Model| NIC_Driver| NIC_Firmware|
|-----------|----------|-----------|-------------|
|5.0U1 Build 623860| NC551i| be2net 4.1.334.48| 4.1.402.20|

After that, the ESXi hosts stopped experiencing the PSODs.

