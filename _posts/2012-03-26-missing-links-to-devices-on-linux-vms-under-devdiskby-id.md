---
title: Missing links to devices on Linux VMs under /dev/disk/by-id/
author: Karim Elatov
layout: post
permalink: /2012/03/missing-links-to-devices-on-linux-vms-under-devdiskby-id/
dsq_thread_id:
  - 1405116090
categories:
  - OS
  - Storage
  - VMware
tags:
  - vpd scsi_0x83 disk.enableuuid scsi_id
---
Recently, I ran into an issue where all links under **/dev/disk/by-id** were missing. The way that devices show up under **/dev/disk/by-id** is when the **scsi_id** command queries the devices for VPD (SCSI inquiry Vital Product Data) and when the disk returns the information it can create the appropriate link. There are two ways of checking for that data, to do so run the following:

    [root@rac2 ~]# scsi_id -p 0x80 -g -s /block/sda
    [root@rac2 ~]# scsi_id -p 0x83 -g -s /block/sda
    

*   **0&#215;83** is Device Identification Vital Product Data and **0&#215;80** is Unit Serial Number 

as you can see, nothing is returned. I did some research and I found that after ESX 4.0, a SCSI inquiry will not be answered within the VM. There is actually a VMware KB that talks about it, VMware KB <a href="http://kb.vmware.com/kb/1029157" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1029157']);">1029157</a> and here is another blog that talks about the same, <a href="http://www.dizwell.com/wiki/doku.php?id=blog:the_case_of_vmware_and_the_missing_scsi_id" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','']);">The Case of VMware and the missing SCSI ID</a>. Now to fix the issue we can set the following in the **vmx** file:

    disk.EnableUUID = "TRUE"
    

and then it will correctly answer to the SCSI inquiry. I made the above change to a Linux VM, and here is what I saw:

    [root@rac1 ~]# scsi_id -p 0x80 -g -s /block/sda
    SVMware Virtual disk 6000c2907159c1057f111400f66d4642
    [root@rac1 ~]# scsi_id -p 0x83 -g -s /block/sda
    36000c2907159c1057f111400f66d4642
    

Now they are returning the VPD information. And also looking under **/dev/disk/by-id**, I see the following:

    [root@rac1 ~]# ls -l /dev/disk/by-id/*
    lrwxrwxrwx 1 root root 9 Mar 25 13:55 /dev/disk/by-id/ata-VMware_Virtual_IDE_CDROM_Drive_10000000000000000001 -> ../../hdc
    lrwxrwxrwx 1 root root 9 Mar 25 13:55 /dev/disk/by-id/scsi-36000c2907159c1057f111400f66d4642 -> ../../sda
    lrwxrwxrwx 1 root root 10 Mar 25 13:55 /dev/disk/by-id/scsi-36000c2907159c1057f111400f66d4642-part1 -> ../../sda1
    lrwxrwxrwx 1 root root 10 Mar 25 13:55 /dev/disk/by-id/scsi-36000c2907159c1057f111400f66d4642-part2 -> ../../sda2
    lrwxrwxrwx 1 root root 9 Mar 25 13:55 /dev/disk/by-id/scsi-36000c2993b74b940e6952b381d6be0d5 -> ../../sdb
    lrwxrwxrwx 1 root root 10 Mar 25 13:55 /dev/disk/by-id/scsi-36000c2993b74b940e6952b381d6be0d5-part1 -> ../../sdb1
    [root@rac1 ~]#
    

As a side note, under different distros the **scsi_id** command might be under different locations and might accept other flags. For Fedora 16, it looks like this:

    [root@fed ~]$ /lib/udev/scsi_id -p 0x83 -g -d /dev/sda
    35000c50024837909
    

and on Ubuntu:

    root@ub: ~$ /lib/udev/scsi_id -p 0x83 -g -d /dev/sda
    35000c86787963
    

and on RHEL

    [root@rac1 ~]# /sbin/scsi_id -p 0x83 -g -s /block/sdb
    36000c2993b74b940e6952b381d6be0d5
    

