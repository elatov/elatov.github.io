---
title: Recreating VMFS Partitions using Hexdump
author: Jarret Lavallee
layout: post
permalink: /2012/09/recreating-vmfs-partitions-using-hexdump/
dsq_thread_id:
  - 1404673624
categories:
  - Storage
  - VMware
tags:
  - cylinders
  - fdisk
  - Fdisk Partitions
  - GPT
  - hexdump
  - MBR
  - partedUtil
  - partition
  - partitions
  - sectors
  - vmfs
  - vmfs3
---
Often I will see VMFS partitions that are not aligned to the <a href="http://www.vmware.com/pdf/esx3_partition_align.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://www.vmware.com/pdf/esx3_partition_align.pdf']);">standard 128 or 2048 sectors</a>. This occurs on datastores that are on the ESXi boot volume and partitions that were manually created. If the partition table is lost, it is important to accurately recreate the partition table on a VMFS volume.

Karim recently wrote a <a href="http://virtuallyhyper.com/2012/09/vmfs-datastore-not-auto-mounting-on-an-esxi-host/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2012/09/vmfs-datastore-not-auto-mounting-on-an-esxi-host/']);" title="VMFS Datastore not Auto-Mounting on an ESX(i) Host because the VMFS Partition is Overwritten">post about VMFS volume being overwritten with NTFS</a>. In the article he shows the output of **hexdump**. In this article we will use the utility to recreate partition tables.

The first thing is to understand the different types of partition tables. ESX/ESXi pre 5.x uses Master Boot Record (MBR/MSDOS) partitions, where as ESXi 5.0 introduced support for GUID Partition Tables (GPT) partitions. A good article about the difference between MBR and GPT partitions can be found <a href="http://www.petri.co.il/gpt-vs-mbr-based-disks.htm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.petri.co.il/gpt-vs-mbr-based-disks.htm']);">here</a>.

## MBR Partitions

MBR partition tables have a few downsides: The first is that there is no redundancy in the partition table and the second is that partitions are limited to 2TB. The MBR sits in the first sector of the disk (512 bytes) and is used for VMFS3.

To modify a MBR partition we can use the fdisk command. First let’s take a look at a healthy VMFS 3 partition.

    # fdisk -lu /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    
    Disk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001: 10.7 GB, 10737418240 bytes
    255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
    Units = sectors of 1 * 512 = 512 bytes
    
                                                        Device Boot      Start         End      Blocks  Id System
    /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001p1             128    20971519    10485696  fb VMFS
    

The *-lu* in the **fdisk** command tells **fdisk** to list the partition in sectors. There is one partition */vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001p1* that starts at 128 sectors from the beginning of the disk. It ends at 20971519 sectors from the beginning of the disk, which is the last sector (total 20971520 sectors starting at sector 0). Since the end sector is the last sector, we know that this partition spans the whole disk. The type of this partition is *fb* which is a VMFS partition type. The *10.7 GB* this is <a href="http://marco-za.blogspot.com/2007/11/gb-vs-gib.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://marco-za.blogspot.com/2007/11/gb-vs-gib.html']);">GB and not GiB</a>, so this disk would actually be 10GiB (10737418240/ 2^30). When I mention GB and KB in this article I am referring to GiB and KiB.

Here is what the partition table looks like from **hexdump**. <a href="http://thestarman.pcministry.com/asm/mbr/PartTables.htm" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://thestarman.pcministry.com/asm/mbr/PartTables.htm']);">This article</a> explains what each byte means in the output below.

    # hexdump -C -n 512 /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000001b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 02  |................|
    000001c0  03 00 fb fe ff ff 80 00  00 00 80 ff 3f 01 00 00  |............?...|
    000001d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000001f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 55 aa  |..............U.|
    00000200
    

This partition is at 128 sectors from the beginning of the disk (the default for VMFS3 volumes). 128 Sectors * 512 bytes per sector = 64KB, so partition 1 begins at 64KB from the beginning of the disk.

Let’s take a look at the first sector of the partition using **hexdump**.

    # hexdump -C -s 65536 -n 512 /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    00010000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00010200
    

The **hexdump** output shows that this sector is all zeros, so there is nothing written here. The interesting part of the output is the offset (00010000). 0×00010000 in decimal is equal to 65536 bytes, which is 64KB.

To get an idea for what these locations are we have the following.

0×100 = 256 bytes  
0×1000 = 4096 = 4KB  
0×10000 = 65536 = 64KB  
0×100000 = 1048576 = 1MB  
0×1000000 = 16777216 = 16MB

So if we were at 0×00010200, that would be 64KB + 512 bytes from the beginning of the device. In this case it is the second sector in our partition.

VMFS has a 1MB offset from the beginning of the partition, so in this case we would expect to see it start at 1MB + 64KB from the beginning of the disk. <a href="http://blog.laspina.ca/ubiquitous/understanding-vmfs-volumes" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.laspina.ca/ubiquitous/understanding-vmfs-volumes']);">This blog post</a> goes over the details of the header.

Let’s take a look at the beginning of the VMFS volume. In this case we would expect it to be 128 sectors (64KB calculated above) + 1MB from the beginning of the disk. 64KB + 1MB = 1114112 bytes = 0×110000. So let&#8217;s **hexdump** the first sector starting at 1114112 bytes.

    # hexdump -C -s 1114112  -n 512 /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    00110000  0d d0 01 c0 05 00 00 00  15 00 00 00 02 16 05 00  |................|
    00110010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    00110020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 60 01  |..............`.|
    00110030  44 f0 e8 cb 47 00 00 00  50 53 b9 b5 00 01 43 4f  |D...G...PS....CO|
    00110040  4d 53 54 41 00 00 00 00  00 00 00 00 00 00 00 00  |MSTA............|
    00110050  00 00 00 00 00 00 00 00  00 00 00 02 00 00 00 00  |................|
    00110060  ff 7f 02 00 00 00 01 00  00 00 27 00 00 00 26 00  |..........'...&.|
    00110070  00 00 03 00 00 00 00 00  00 00 00 00 10 01 00 00  |................|
    00110080  00 00 c7 31 58 50 c0 f8  b2 72 db 6f d0 27 88 6f  |...1XP...r.o.'.o|
    00110090  38 82 76 e9 8a bd f5 c9  04 00 ee 59 a2 bd f5 c9  |8.v........Y....|
    001100a0  04 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    001100b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 01 00  |................|
    001100c0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00110200
    

If you read through <a href="http://blog.laspina.ca/ubiquitous/understanding-vmfs-volumes" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blog.laspina.ca/ubiquitous/understanding-vmfs-volumes']);">this blog post</a> you saw that the VMFS volume starts with the same sequence of digits, *0d d0 01 c0*. The VMFS driver looks for this sequence to be 1MB from the beginning of the partition. If it is not there, then it is not a VMFS volume. So recreating the partition table accurately is very important.

### Recreating the MBR partition table with a non-default offset

If the partition table was lost, we would be able to rebuild it knowing that the beginning of the partition needs to be 128 sectors from the beginning of the disk. What if we did not know that information? We would have to find the beginning of the VMFS volume and then calculate the start of the partition.

First we should check the partition table.

    # fdisk -lu /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    
    Disk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001: 10.7 GB, 10737418240 bytes
    255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
    Units = sectors of 1 * 512 = 512 bytes
    
                                                        Device Boot      Start         End      Blocks  Id System
    

**Fdisk** reported that there are no partitions on this LUN. Since we know that the VMFS volume begins with *0d d0 01 c0*, we can **hexdump** the LUN and look for that sequence.

    # hexdump -C -n 2000000 /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001 |grep -m 1 "0d d0 01 c0"
    00107e00  0d d0 01 c0 05 00 00 00  15 00 00 00 02 16 05 00  |................|
    

So this is a VMFS volume, but it does not begin where we would expect. The offset is 0x00107e00, so we can use this to find where the partition should begin. Since we know that the VMFS volume begins 1MB from the beginning of the partition we can subtract 1MB, 0×100000 as seen above, from the offset. 0x00107e00 – 0×100000 = 0x00007e00 = 32256 bytes. We can then convert that to sectors by dividing it by 512 bytes. 32256 bytes / 512 bytes = 63 sectors.

So we need to recreate the partition table with the offset of 63 sectors (the default in **fdisk**). <a href="http://kb.vmware.com/kb/1002281" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1002281']);">This KB article</a> shows how to create a partition table with a 128 sector offset, below we will create it for a 63 sector offset.

    # fdisk -u /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    
    The number of cylinders for this disk is set to 1305.
    There is nothing wrong with that, but this is larger than 1024,
    and could in certain setups cause problems with:
    1) software that runs at boot time (e.g., old versions of LILO)
    2) booting and partitioning software from other OSs
       (e.g., DOS FDISK, OS/2 FDISK)
    
    Command (m for help): n
    Command action
       e   extended
       p   primary partition (1-4)
    p
    Partition number (1-4): 1
    First sector (63-20971519, default 63): Using default value 63
    Last sector or %2Bsize or %2BsizeM or %2BsizeK (63-20971519, default 20971519): Using default value 20971519
    
    Command (m for help): t
    Selected partition 1
    Hex code (type L to list codes): fb
    Changed system type of partition 1 to fb (VMFS)
    
    Command (m for help): p
    
    Disk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001: 10.7 GB, 10737418240 bytes
    255 heads, 63 sectors/track, 1305 cylinders, total 20971520 sectors
    Units = sectors of 1 * 512 = 512 bytes
    
                                                        Device Boot      Start         End      Blocks  Id System
    /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001p1              63    20971519    10485728%2B fb VMFS
    
    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table
    

Now that we have a partition table we can take a look at the volume and confirm that the VMFS header is 1MB (0×100000) from the beginning of the partition. Notice that this time we **hexdump** the partition, denoted by the “:1″.

    # hexdump -C -s 1048576  -n 512 /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001:1
    00100000  0d d0 01 c0 05 00 00 00  15 00 00 00 02 16 05 00  |................|
    00100010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    00100020  00 00 00 00 00 00 00 00  00 00 00 00 00 00 60 01  |..............`.|
    00100030  44 f0 e8 cb 47 00 00 00  50 53 b9 b5 00 01 43 4f  |D...G...PS....CO|
    00100040  4d 53 54 41 00 00 00 00  00 00 00 00 00 00 00 00  |MSTA............|
    00100050  00 00 00 00 00 00 00 00  00 00 00 02 00 00 00 34  |...............4|
    00100060  cb 7f 02 00 00 00 01 00  00 00 27 00 00 00 26 00  |..........'...&.|
    00100070  00 00 03 00 00 00 00 00  00 00 00 00 10 01 00 00  |................|
    00100080  00 00 fa f7 58 50 22 4a  a5 9b c7 9a d0 27 88 6f  |....XP"J.....'.o|
    00100090  38 82 c8 47 d4 8d 01 ca  04 00 ee e2 f2 8d 01 ca  |8..G............|
    001000a0  04 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    001000b0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 01 00  |................|
    001000c0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    00100200
    

As we expected *0d d0 01 c0* is at 0×00100000 from the beginning of the partition. We should be able to rescan and remount the VMFS volume.

**Note:** If the VMFS3 volume was created through the GUI, the offset should be 128 sectors. If it was created using an ESXi 5 host or vCenter 5, the offset may be 2048 sectors.

If it is not at 128 sectors or 2048 it will be somewhere else on the disk. We will often see it at 63 sectors as above. Another common one is when someone uses cylinders instead of sectors in **fdisk**.

    # hexdump -C /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001 |grep -m 1 "0d d0 01 c0"
    3e537e00  0d d0 01 c0 03 00 00 00  15 00 00 00 02 16 05 00  |................|
    

0x3e537e00 = 1045659136 bytes ~= 997MB, which is really far into the disk to start a partition. It is a common mistake when people create partitions manually. Instead of offsetting in sectors, they offset the partition in cylinders. Cylinders are the default unit in **fdisk**, so when they created the partition they did not send in the *-u* flag to **fdisk** to use sectors instead of cylinders. We can get the output of **fdisk** to see the size of the units.

    # fdisk -l /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    
    Disk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001: 10.7 GB, 10737418240 bytes
    255 heads, 63 sectors/track, 1305 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    
                                                        Device Boot      Start         End      Blocks  Id System
    

In this case each cylinder is 8225280 bytes. If we take our offset, subtract out the 1MB as above we can find how many cylinders from the beginning of the disk the partition starts. (1045659136 bytes – 1048576 bytes)/ 8225280 bytes per cylinder = 127 cylinders. You can recreate the partition at the 128th cylinder with **fdisk** as below.

    # fdisk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    
    The number of cylinders for this disk is set to 1305.
    There is nothing wrong with that, but this is larger than 1024,
    and could in certain setups cause problems with:
    1) software that runs at boot time (e.g., old versions of LILO)
    2) booting and partitioning software from other OSs
       (e.g., DOS FDISK, OS/2 FDISK)
    
    Command (m for help): n
    Command action
       e   extended
       p   primary partition (1-4)
    p
    Partition number (1-4): 1
    First cylinder (1-1305, default 1): 128
    Last cylinder or %2Bsize or %2BsizeM or %2BsizeK (128-1305, default 1305): Using default value 1305
    
    Command (m for help): t
    Selected partition 1
    Hex code (type L to list codes): fb
    Changed system type of partition 1 to fb (VMFS)
    
    Command (m for help): p
    
    Disk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001: 10.7 GB, 10737418240 bytes
    255 heads, 63 sectors/track, 1305 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    
                                                        Device Boot      Start         End      Blocks  Id System
    /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001p1             128        1305     9462285  fb VMFS
    
    Command (m for help): w
    The partition table has been altered.
    Calling ioctl() to re-read partition table
    

## GPT Partitions

Since MBR partitions are limited to 2TB, the size of the LUN is limited to 2TB for a VMFS volume. VMFS5 changed to double-indirect pointers which allowed it to handle around 64TB LUNs, but the partition table could only allow for 2TB LUNs. This called for VMware to <a href="http://blogs.vmware.com/vsphere/2011/08/vsphere-50-storage-features-part-7-gpt.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://blogs.vmware.com/vsphere/2011/08/vsphere-50-storage-features-part-7-gpt.html']);">change to GPT partitions</a>.

The GPT partition sits in LBA1, after a protective MBR partition. The GPT partition takes up 16KB + 512 bytes for the header and partition definitions by default. It also has a backup header in the last sector of the disk and backup partition entries the 16KB before the last sector. More information on the location can be <a href="https://wiki.archlinux.org/index.php/GUID_Partition_Table" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://wiki.archlinux.org/index.php/GUID_Partition_Table']);">found here</a> and more information about the GPT header can be <a href="http://asher2003.wordpress.com/2010/11/09/gpt-partition-table-header/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://asher2003.wordpress.com/2010/11/09/gpt-partition-table-header/']);" class="broken_link">found here</a>.

Let’s take a look at the format of a GPT partition. First we have the protective MBR partition. **Fdisk** shows us that we have a protective MBR and that the partition is actually GPT.

    # fdisk -l /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    Found valid GPT with protective MBR; using GPT
    
    Disk /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001: 20971520 sectors, 20.0M
    Logical sector size: 512
    Disk identifier (GUID): f4d64a05-1e54-4e6d-80d4-cd91fed08846
    Partition table holds up to 128 entries
    First usable sector is 34, last usable sector is 20971486
    
    Number  Start (sector)    End (sector)  Size       Code  Name
       1            2048        20964824       19.9M   0700  
    

Here is the protective MBR on disk.

    00000000  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000001b0  00 00 00 00 00 00 00 00  00 00 00 00 1d 9a 00 00  |................|
    000001c0  01 00 ee fe ff ff 01 00  00 00 ff ff 3f 01 00 00  |............?...|
    000001d0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000001f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 55 aa  |..............U.|
    

Next we have the GPT header that sits in the second sector on disk. Read <a href="http://petio.org/boot/disk_hacking_page2.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://petio.org/boot/disk_hacking_page2.html']);">this article</a> for a detailed description of the headers contents.

    00000200  45 46 49 20 50 41 52 54  00 00 01 00 5c 00 00 00  |EFI PART.......|
    00000210  a5 5f f4 18 00 00 00 00  01 00 00 00 00 00 00 00  |._..............|
    00000220  ff ff 3f 01 00 00 00 00  22 00 00 00 00 00 00 00  |..?.....".......|
    00000230  de ff 3f 01 00 00 00 00  05 4a d6 f4 54 1e 6d 4e  |..?......J..T.mN|
    00000240  80 d4 cd 91 fe d0 88 46  02 00 00 00 00 00 00 00  |.......F........|
    00000250  80 00 00 00 80 00 00 00  b9 a4 c3 d3 00 00 00 00  |................|
    00000260  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    000003f0  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    

Now we have the partition definitions. Each partition definition is 128 bytes (0×50 bytes), so we see the first one in lines 0×400-0×440 as each line is 0×10 bytes (16 bytes). In this case we have a single partition. <a href="http://petio.org/boot/disk_hacking_page3.html" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://petio.org/boot/disk_hacking_page3.html']);">This article</a> shows how the information is laid out.

    00000400  2a e0 31 aa 0f 40 db 11  95 90 00 0c 29 11 d1 b8  |*.1..@......)...|
    00000410  91 20 e5 c5 92 55 8b 41  94 a0 00 5f 84 f6 83 ac  |. ...U.A..._....|
    00000420  00 08 00 00 00 00 00 00  d8 e5 3f 01 00 00 00 00  |..........?.....|
    00000430  00 00 00 00 00 00 00 00  00 00 ff ff ff ff ff ff  |................|
    00000440  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|
    *
    00000480  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|
    *
    

For GPT partitions, ESXi has included a tool called **<a href="http://kb.vmware.com/kb/1036609" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1036609']);">partedUtil</a>**. With **fdisk** and MBR partitions we had partition types such as *fb* (VMFS) and *fc* (vmkcore). GPT uses GUIDs which allow for many more partition types. Below is the list of common partition GUIDs.

    # partedUtil showGuids
     Partition Type       GUID
     vmfs                 AA31E02A400F11DB9590000C2911D1B8
     vmkDiagnostic        9D27538040AD11DBBF97000C2911D1B8
     vsan                 381CFCCC728811E092EE000C2911D0B2
     VMware Reserved      9198EFFC31C011DB8F78000C2911D1B8
     Basic Data           EBD0A0A2B9E5443387C068B6B72699C7
     Linux Swap           0657FD6DA4AB43C484E50933C84B4F4F
     Linux Lvm            E6D6D379F50744C2A23C238F2A3DF928
     Linux Raid           A19D880F05FC4D3BA006743F0F84911E
     Efi System           C12A7328F81F11D2BA4B00A0C93EC93B
     Microsoft Reserved   E3C9E3160B5C4DB8817DF92DF00215AE
     Unused Entry         00000000000000000000000000000000
    

**AA31E02A400F11DB9590000C2911D1B8** is the VMFS GUID used to identify VMFS partitions. Note that the one titled *vsan* is for <a href="http://www.yellow-bricks.com/2012/09/04/inf-sto2192-tech-preview-of-vcloud-distributed-storage/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://www.yellow-bricks.com/2012/09/04/inf-sto2192-tech-preview-of-vcloud-distributed-storage/']);">VMware vCloud Distributed Storage</a>.

Let’s look at an existing VMFS5 GPT partition.

    # partedUtil getptbl /vmfs/devices/disks/naa.600144f070cc440000004dd9c9310002
    gpt
    133674 255 63 2147483648
    1 2048 2147472809 AA31E02A400F11DB9590000C2911D1B8 vmfs 0
    

We can break this down by the line. The first line of the output is *gpt*. This tells us that this is a GPT type partition. If it had said *msdos*, it would be an MBR partition.

    gpt
    

The second line of output is a series of numbers that describe the properties of the LUN.

![VMware PatredUtil Output Recreating VMFS Partitions using Hexdump][1]

The third line and subsequent lines will be the partitions on the LUN.

![VMware PatredUtil Output partition Recreating VMFS Partitions using Hexdump][2]

### Recovering a lost GPT partition

One great thing about GPT partitions is that they are redundant. There is a backup of the partition table that is stored at the end of the LUN. Since there is a backup, partedUtil now comes with a *fix* option.

There is a interactive fix and a automated fix.

    # partedUtil 
    Usage: 
    ...
     Fix Partition Table : fix  
    ...
     Fix GPT Table interactively : fixGpt  
    

Let’s run the automated fix on a LUN with a corrupted GPT partition.

    # partedUtil fix /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    Error: The primary GPT table is corrupt, but the backup appears OK, so that will be used. Fix primary table ? diskPath (/dev/disks/naa.600144f0e8cb470000005053b9b50001) diskSize (20971520) AlternateLBA (1) LastUsableLBA (20971486)
    

Despite the error, it said that it was going to fix the partition table so let’s check it again.

    # partedUtil getptbl /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    gpt
    1305 255 63 20971520
    1 2048 20964824 AA31E02A400F11DB9590000C2911D1B8 vmfs 0
    

So **partedUtil** read the backup partition table and restored it. We can also use the interactive *fixGpt*.

    # partedUtil fixGpt /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    
    FixGpt tries to fix any problems detected in GPT table.
    Please ensure that you don't run this on any RDM (Raw Device Mapping) disk.
    Are you sure you want to continue (Y/N): Y
    Error: The primary GPT table is corrupt, but the backup appears OK, so that will be used. Fix primary table ? diskPath (/dev/disks/naa.600144f0e8cb470000005053b9b50001) diskSize (20971520) AlternateLBA (1) LastUsableLBA (20971486)
    Fix/Ignore/Cancel? Fix
    gpt
    1305 255 63 20971520
    1 2048 20964824 AA31E02A400F11DB9590000C2911D1B8 vmfs 0
    

The only real difference between the two is that the interactive one asks if you want to try to fix it. The great news is that we can recover the partition table from the backup. If this fails, we can manually rebuild the partition table.

### Recreating a GPT partition with partedUtil

Just as we did with the MBR partitions, we need to find the beginning of the partition and then recreate the partition. The difference will be that we use **partedUtil** instead of **fdisk**. <a href="http://kb.vmware.com/kb/1036609" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://kb.vmware.com/kb/1036609']);">This KB</a> goes over the process of creating a partition with GPT.

First we need to find the offset for the partition. We will do this with **hexdump** as we did with MBR partitions.

     # hexdump -C /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001 | grep -m 1 "0d d0 01 c0"
    00200000  0d d0 01 c0 05 00 00 00  15 00 00 00 02 16 05 00  |................|
    

Now the VMFS volume begins at 0×00200000, but we know that this is 0×00100000 from the beginning of the partition. So we can subtract 0×00100000 from 0×00200000 to find the correct beginning of the partition. 0×00200000 – 0×00100000 = 0×00100000 = 1MB. So we can take this and divide it by the sector size to get the beginning in sectors. 1MB / 512 bytes per sector = 2048 sectors. 2048 sectors is the default offset for the VMFS5 volume.

Now we know the offset of the partition, but we still need to figure out the end of the partition. To do this we need to get the properties of the LUN.

    # partedUtil getptbl /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    gpt
    1305 255 63 20971520
    

To calculate the ending sector, we take the cylinders, multiply it by the heads, multiply by the sectors per track, and subtract 1. cylinders \* heads \* sectors per track – 1 = 1305 \* 255 \* 63 &#8211; 1 = 20964824 sectors.

Next we need to find the GUID for the VMFS partition. I mentioned this earlier in the post, but it can be found by running the **partedUtil** command.

    # partedUtil showGuids |grep vmfs
     vmfs                 AA31E02A400F11DB9590000C2911D1B8
    

Now we have the starting sector, ending sector and GUID so we can create the partition. The format of the command is below.

    Set Partitions : setptbl   ["partNum startSector endSector type/guid attr"]*
    

Now let’s fill in the correct values. We will use 0 for the attributes because we do not want any special attributes on this partition.

    # partedUtil setptbl /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001 gpt "1 2048 20964824 AA31E02A400F11DB9590000C2911D1B8 0"
    gpt
    0 0 0 0
    1 2048 20964824 AA31E02A400F11DB9590000C2911D1B8 0
    

Now let’s check that the partition was created correctly.

    # partedUtil getptbl /vmfs/devices/disks/naa.600144f0e8cb470000005053b9b50001
    gpt
    1305 255 63 20971520
    1 2048 20964824 AA31E02A400F11DB9590000C2911D1B8 vmfs 0
    

<div class="SPOSTARBUST-Related-Posts">
  <H3>
    Related Posts
  </H3>
  
  <ul class="entry-meta">
    <li class="SPOSTARBUST-Related-Post">
      <a title="RHCSA and RHCE Chapter 1 &#8211; Installation" href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-1-installation/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-1-installation/']);" rel="bookmark">RHCSA and RHCE Chapter 1 &#8211; Installation</a>
    </li>
  </ul>
</div>

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2012/09/recreating-vmfs-partitions-using-hexdump/" title=" Recreating VMFS Partitions using Hexdump" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:cylinders,fdisk,Fdisk Partitions,GPT,hexdump,MBR,partedUtil,partition,partitions,sectors,vmfs,vmfs3,blog;button:compact;">There is a lot of good information in &#8220;Red Hat Enterprise Linux 6 Installation Guide&#8220;. From that Guide: 9&#046;3. Welcome to Red Hat Enterprise Linux The Welcome screen does not...</a>
</p>

 [1]: http://virtuallyhyper.com/wp-content/uploads/2013/05/VMware-PatredUtil-Output.jpg "Recreating VMFS Partitions using Hexdump"
 [2]: http://virtuallyhyper.com/wp-content/uploads/2013/05/VMware-PatredUtil-Output-partition.jpg "Recreating VMFS Partitions using Hexdump"