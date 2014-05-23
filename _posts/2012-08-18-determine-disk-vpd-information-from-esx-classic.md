---
title: Determine Disk VPD Information from ESX Classic
author: Karim Elatov
layout: post
permalink: /2012/08/determine-disk-vpd-information-from-esx-classic/
dsq_thread_id:
  - 1406778244
categories:
  - Storage
  - VMware
  - vTip
tags:
  - NAA_ID
  - page 0x80
  - page 0x83
  - SCSI Inquiry
  - sg_vpd
  - Unit Serial Number
  - Vital Product Data
  - VPD Pages
---
ESX issues an [1010244](https://github.com/elatov/uploads/raw/master/2014/01/spc3r23.pdf):

> During a re-enumeration of storage devices, the VMware ESX/ESXi VMkernel sends SCSI Report LUNs command (0xa0) to the target to retrieve a list of LUNs, and SCSI Inquiry commands (0x12) to each LUN to determine the type of device (disk, CD-ROM, USB, etc), the make and model of the device, and the features the device supports.
>
> A SCSI Inquiry requests Vital Product Data (VPD) page information from the LUN, including the unit serial number (page 0x80), a device identification number (page 0x83), and the management network address (page 0x85).
>
> If a SCSI device does not support a particular VPD page, it may respond to such a request with an error. Specifically, it may return SCSI Status 2 (Check Condition), with sense key 5 (Illegal Request) and additional sense code (ASC) and additional sense code qualifier (ASCQ) set to 0x20/0x0 or 0x24/0x0.

Usually Local devices device don't have page 83 information, but they do contain page 80 information. From the same KB:

> Local storage devices often do not support VPD page 0x83, and thus cannot be used for Raw Device Mappings (RDMs). The content of page 0x83 is used as a unique identifier for the device.
>
> CD or DVD-ROM devices often do not support VPD pages 0x80, 0x83 or 0x85. This can be ignored.
>
> Some device controllers do not support Report LUNs. If there is no LUN 0, or the SCSI version reported is 2 or lower, the ESX/ESXi host iteratively scans for LUNs on this controller.

If you are using ESX classic then you can query both pages from your devices, here is an example:

    [root@esx40u1 ~]# sg_vpd -p 0x83 /dev/sdd
    Device Identification VPD page:
      Addressed logical unit:
        designator type: NAA, code_set: Binary
             0x600144f0928c010000004fc511ec0001
        Target port:
           designator type: vendor specific [0x0], code_set: ASCII
           transport: Internet SCSI (iSCSI)
              00 69 71 6e 2e 32 30 31 30 2d 30 39 2e 6f 72 67 2e iqn.2010-09.org. 10 6f 70 65 6e 69 6e 64 69 61 6e 61 3a 30 32 3a 64
             openindiana:02:d 20 35 37 37 33 66 32 66 2d 64 35 62 31 2d 36 63 36 5773f2f-d5b1-6c6 30 31 2d 38 61 64 34 2d 62 35 61 32 64 61 63 33 34 1-8ad4-b5a2dac34 40 32 39 34 294
           designator type: Target port group, code_set: Binary
        Target port group: 0x0
           designator type: Relative target port, code_set: Binary
           Relative target port: 0x1


From the above output you can see the NAA ID of my OpenIndiana LUN presented over iSCSI. Here is an example of a device with both (it was a local drive):

    [root@localhost ~]# sg_vpd -p 0x83 /dev/sda
    Device Identification VPD page:
      Addressed logical unit:
       designator type: NAA, code_set: Binary
         0x6000c29e28495d0b9ecd280a8dc01a5c

    [root@localhost ~]# sg_vpd -p 0x80 /dev/sda
    Unit serial number VPD page:
      Unit serial number: 6000c29e28495d0b9ecd280a8dc01a5c


You can see that the device has a Unit Serial Number and an NAA ID.

