---
title: Migrating the Root ZFS Pool to a Smaller Drive
author: Karim Elatov
layout: post
permalink: /2012/08/migrating-the-root-zfs-pool-to-a-smaller-drive/
dsq_thread_id:
  - 1404673099
categories:
  - Home Lab
  - Storage
  - VMware
  - ZFS
tags:
  - beadm
  - boot-sign
  - bootadm
  - Disk Labels
  - dumpadm
  - EFI
  - fast reboot
  - Fdisk Partitions
  - findroot
  - format utility
  - menu.lst
  - prtvtoc
  - root zpool
  - SMI
  - Solaris Slices
  - sparc
  - VTOC
  - x86
  - ZFS
  - zfs recieve
  - zfs send
  - zfs snapshot
  - zpool
  - zvol
---
I made a mistake of showing the co-author of this post, Jarret, my test lab, so he rediculed me and made fun of me. I am pretty new to ZFS and I just deployed an OpenIndiana VM for it's Comstar/iSCSI capabilities but using ZFS was definitely a plus. Just as an FYI here is the version of OpenIndiana that I was using:

    root@openindiana:~# uname -a
    SunOS openindiana 5.11 oi_151a4 i86pc i386 i86pc Solaris


The reason why my friend made fun of me was because I only had one drive and I used one pool for all of my storage needs. Here is how my zpool looked like:

    root@openindiana:~# zpool status
    pool: rpool1 state: ONLINE scan: none requested config:

            NAME        STATE     READ WRITE CKSUM
            rpool1      ONLINE       0     0     0
              c3t0d0s0  ONLINE       0     0     0


    errors: No known data errors


Just one drive and here are my ZFS volumes:

    root@openindiana:~# zfs list
    NAME                        USED    AVAIL   REFER   MOUNTPOINT
    rpool1                      244G    6.47G   46.5K   /rpool1
    rpool1/ROOT                 3.27G   6.47G   31K     legacy
    rpool1/ROOT/openindiana     8.31M   6.47G   2.10G   /
    rpool1/ROOT/openindiana-1   3.26G   6.47G   1.81G   /
    rpool1/dump                 1.00G   6.47G   1.00G   -
    rpool1/export               98K     6.47G   32K     /export
    rpool1/export/home          66K     6.47G   32K     /export/home
    rpool1/export/home/elatov   34K     6.47G   34K     /export/home/elatov
    rpool1/iscsi_share          103G    105G    4.71G   -
    rpool1/iscsi_share2         134G    141G    26.5M   -
    rpool1/nfs_share            1000M   6.47G   1000M   /rpool1/nfs_share
    rpool1/swap                 1.06G   7.41G   133M    -


Nothing complicated. I did some research and I actually found a very good website which talked about best practices for ZFS, here is a [link](http://www.open-tech.com/2011/10/zfs-best-practices-guide-from-solaris-internals/) to that web page. And here are some points from that article:

> *   Run ZFS on a system that runs a 64-bit kernel
> *   Set up one storage pool using whole disks per system, if possible.
> *   Run zpool scrub on a regular basis to identify data integrity problems.
> *   A root pool must be created with disk slices rather than whole disks. Allocate the entire disk capacity for the root pool to slice 0, for example, rather than partition the disk that is used for booting for many different uses.
> *   A root pool must be labeled with a VTOC (SMI) label rather than an EFI label.
> *   Keep all root pool components, such as the /usr and /var directories, in the root pool.
> *   Consider keeping the root pool separate from pool(s) that are used for data.

There are a lot more in that article. My main concern was having my data ZFS volumes inside the root pool. So I decided to add a new disk of 8GB and migrate the OS to it and leave original zpool as the data pool. Here are my disks prior to any change:

    root@openindiana:~# cfgadm -as "select=type(disk)"
    Ap_Id           Type    Receptacle  Occupant    Condition
    c3::dsk/c3t0d0  disk    connected   configured  unknown


You can also check with format:

    root@openindiana:~# echo | format
    Searching for disks...done

    AVAILABLE DISK SELECTIONS:
             0. c3t0d0
                /pci@0,0/pci15ad,1976@10/sd@0,0
    Specify disk (enter its number):


# Creating the new root ZFS Pool

I went ahead and added another disk and then rescanned for new devices:

    root@openindiana:~# devfsadm -c disk


Now looking for the new disk, I saw the following:

    root@openindiana:~# cfgadm -as "select=type(disk)"
    Ap_Id                   Type    Receptacle  Occupant    Condition
    c3::dsk/c3t0d0          disk    connected   configured  unknown
    mpt1:scsi::dsk/c4t0d0   disk    connected   configured  unknown


and with format:

    root@openindiana:~# echo | format
    Searching for disks...done

    AVAILABLE DISK SELECTIONS:
        0. c3t0d0
            /pci@0,0/pci15ad,1976@10/sd@0,0
        1. c4t0d0
            /pci@0,0/pci15ad,790@11/pci15ad,1976@2/sd@0,0

    Specify disk (enter its number):


The new disk is **c4t0d0**. Now we need to label the disk with a VTOC label and not an EFI label. The Oracle article entitled "[Overview of Disk Management](http://docs.oracle.com/cd/E19963-01/html/821-1459/disksconcepts-1.html)" describes the difference between the two labels. From that article:

> **About Disk Labels**
>
> A special area of every disk is set aside for storing information about the disk's controller, geometry, and slices. This information is called the disk's label. Another term that is used to described the disk label is the VTOC (Volume Table of Contents) on a disk with a VTOC label. To label a disk means to write slice information onto the disk. You usually label a disk after you change its slices.
>
> The Solaris release supports the following two disk labels:
>
> *   SMI – The traditional VTOC label for disks that are less than 2 TB in size.
> *   EFI – Provides support for disks that are larger than 2 TB on systems that run a 64-bit Solaris kernel. The Extensible Firmware Interface GUID Partition Table (EFI GPT) disk label is also available for disks less than 2 TB that are connected to a system that runs a 32-bit Solaris kernel.
>
> If you fail to label a disk after you create slices, the slices will be unavailable because the OS has no way of “knowing” about the slices.

If you are getting confused with all the terms, I would recommend reading [this page](http://content.hccfl.edu/pollock/AUnix1/DiskTech.htm). I really like how the author describes all the different OSes and how they differ, here are a couple of experts from the above page that allowed me to stay sane:

> **Partitions and Slices**
>
> There are different schemes for partitioning a disk. For workstations DOS partitions (a “DOS” or “MBR” disk) are common (including for Linux). Sadly there is no formal standard for “DOS” partitions, the most common disk type! (Typical MS tactic.) Other OSes (Solaris, *BSD) use their own partitioning scheme, inside one DOS (primary) partition on IA. The concepts are the same for all schemes.
>
> Older Sparc servers use “VTOC” and new ones “EFI” partitioning schemes. Macintosh uses “APM” (Apple Partition Map) for PowerPC Macs and a GPT for x86 Macs. The Sun schemes as well as the more common (and vendor-neutral) GPT scheme are discussed below.
>
> The scheme used matters since the BIOS (or equivalent) as well as the boot loader must be able to determine the type and location of partitions on a disk. This is why you can’t dual-boot Windows on Mac hardware: the Windows loader assumes DOS partitions and doesn't understand GPT partitions.

Also here another excerpt:

> Unix servers don’t use the DOS disk scheme, but use a related concepts known as disk slices. Some OSes confusingly call slices “partitions”. Annoyingly, many Unix documents and man pages mix up the terms partition and slice. You have been warned!
>
> ...
> ...
>
> The Unix partitioning scheme doesn't have an MBR but a similar data structure called the “disk label”, which contains the partition table/map.
>
> The term disk label can be confusing. Each disk has a disk label which may be called the MBR, VTOC, or EFI. However each storage volume can also have a label (and a type). This is technically the volume label but is often called the disk label. A volume label is 8 bytes in length and often contains the mount-point pathname.
>
> The fdisk utility (both Linux and Solaris) is used to label a DOS disk with an MBR. One of these primary partitions is then divided into slices by labeling that partition using the format command to write the VTOC or EFI disk label to it. The Solaris format command used to define the slices has a sub-command to label the disk, but you must remember to use it!

From the Oracle documentation, here is how they describe slices:

> **About Disk Slices**
>
> Files stored on a disk are contained in file systems. Each file system on a disk is assigned to a slice, which is a group of sectors set aside for use by that file system. Each disk slice appears to the Oracle Solaris OS (and to the system administrator) as though it were a separate disk drive.
>
> **Note** - Slices are sometimes referred to as partitions. Certain interfaces, such as the format utility, refer to slices as partitions.
>
> When setting up slices, remember these rules:
>
> *   Each disk slice holds only one file system.
> *   No file system can span multiple slices.
> *   Slices are set up slightly differently on SPARC and x86 platforms.
>
> **SPARC Platform**
> The entire disk is devoted to Oracle Solaris OS.
>
> *   VTOC – The disk is divided into 8 slices, numbered 0-7.
> *   EFI – The disk is divided into 7 slices, numbered 0-6.
>
> **x86 Platform**
> Disk is divided into fdisk partitions, one fdisk partition per operating system
>
> *   VTOC – The Solaris fdisk partition is divided into 10 slices, numbered 0–9.
> *   EFI – The disk is divided into 7 slices, numbered 0-6

As I was reading up on slices and partitions, I found [this](http://constantin.glez.de/blog/2011/03/how-set-zfs-root-pool-mirror-oracle-solaris-11-express) great blog, that describes them in a way that I liked, from the blog:

> Solaris disk partitioning works differently in the SPARC and in the x86 world:
>
> *   **SPARC:** Disks are labeled using special, Solaris-specific "SMI labels". No need for special boot magic or GRUB, etc. here, as the SPARC systems' OpenBoot PROM is intelligent enough to handle the boot process by itself.
> *   **x86:** For reasons of compatibility with the rest of the x86 world, Solaris uses a primary fdisk partition labeled Solaris2, so it can coexist with other OSes. Solaris then treats its fdisk partition as if it were the whole disk and proceeds by using an SMI label on top of that to further slice the disk into smaller partitions. These are then called "slices".The boot process uses GRUB, again for compatibility reasons, with a special module that is capable of booting off a ZFS root pool.
>
> So for x86, the first thing to do now is to make sure that the disk has an fdisk partition of type "Solaris2" that spans the whole disk. For SPARC, we can skip this step.
>
> fdisk doesn't know about Solaris slices, it only cares about DOS-style partitions. Therefore, device names are different when dealing with fdisk: We'll refer to the first partition now and call it "p0". This will work even if there are no partitions defined on the disk, it's just a way to address the disk in DOS partition mode.

The first thing I need to do is to create an "fdisk partition", so let's do that:

    root@openindiana:~# fdisk /dev/rdsk/c4t0d0p0
    No fdisk table exists. The default partition for the disk is:

        a 100% "SOLARIS System" partition

    Type "y" to accept the default partition, otherwise type "n" to edit the partition table. n


It then goes through an interactive menu, here is how it looked like. First select to "create a partition":

![create_new_partition](http://virtuallyhyper.com/wp-content/uploads/2012/08/create_new_partition.png)

and then select the partition type:

![select_partition_type](http://virtuallyhyper.com/wp-content/uploads/2012/08/select_partition_type.png)

then select to use the whole partition (100%):

![select_to_use_100](http://virtuallyhyper.com/wp-content/uploads/2012/08/select_to_use_100.png)

Then let's go ahead and activate the partition:

![activate_the_partition](http://virtuallyhyper.com/wp-content/uploads/2012/08/activate_the_partition.png)

and finally let's write the changes to disk:

![commit_changes](http://virtuallyhyper.com/wp-content/uploads/2012/08/commit_changes.png)

If you didn't want to go through the interactive menu you could've run this command to create a partition using 100% of the space, like so:

    root@openindiana:~# fdisk -B /dev/rdsk/c4t0d0p0


Now checking the partition table I see the following:

    root@openindiana:~# prtvtoc /dev/rdsk/c4t0d0p0
    * /dev/rdsk/c4t0d0p0 partition map
    *
    * Dimensions:
    *     512 bytes/sector
    *      32 sectors/track
    *     128 tracks/cylinder
    *    4096 sectors/cylinder
    *    4095 cylinders
    *    4093 accessible cylinders
    *
    * Flags:
    *   1: unmountable
    *  10: read-only
    *
    * Unallocated space:
    *       First     Sector    Last
    *       Sector     Count    Sector
    *           0      4096      4095
    *
    *                          First     Sector    Last
    * Partition  Tag  Flags    Sector     Count    Sector  Mount Directory
           0      2    00       4096  16760832  16764927
           2      5    01          0  16764928  16764927
           8      1    01          0      4096      4095


Remember partition 2 is the whole disk and partition 8 is used for grub. From the Oracle documentation:

> **Slice 2**
>
> *   VTOC – Refers to the entire disk, by convention. The size of this slice should not be changed.
> *   EFI – Optional slice to be defined based on your site's needs.
>
> **Slice 8**
>
> *   VTOC – Contains GRUB boot information.
> *   EFI – A reserved slice created by default. This area is similar to the VTOC's alternate cylinders. Do not modify or delete this slice.

More information on fdisk can be seen at the oracle document called "[Creating and Changing Solaris fdisk Partitions](http://docs.oracle.com/cd/E23824_01/html/821-1459/disksxadd-50.html)".

Right after we created an fdisk partition all of the Slices get automatically created. You can also use format to call fdisk, instructions are laid out in "[x86: Setting Up Disks for ZFS File Systems](http://docs.oracle.com/cd/E23824_01/html/821-1459/disksxadd-50.html)". Let's go ahead and check out the partition with the format output:

    root@openindiana:~# format
    Searching for disks...done

    AVAILABLE DISK SELECTIONS:
           0. c3t0d0
              /pci@0,0/pci15ad,1976@10/sd@0,0
           1. c4t0d0
              /pci@0,0/pci15ad,790@11/pci15ad,1976@2/sd@0,0
    Specify disk (enter its number): 1
    selecting c4t0d0
    [disk formatted]

    FORMAT MENU:
            disk       - select a disk
            type       - select (define) a disk type
            partition  - select (define) a partition table
            current    - describe the current disk
            format     - format and analyze the disk
            fdisk      - run the fdisk program
            repair     - repair a defective sector
            label      - write label to the disk
            analyze    - surface analysis
            defect     - defect list management
            backup     - search for backup labels
            verify     - read and display labels
            save       - save new disk/partition definitions
            inquiry    - show vendor, product and revision
            volname    - set 8-character volume name
            !     - execute , then return
            quit
    format> partition

    PARTITION MENU:
            0      - change '0' partition
            1      - change '1' partition
            2      - change '2' partition
            3      - change '3' partition
            4      - change '4' partition
            5      - change '5' partition
            6      - change '6' partition
            7      - change '7' partition
            select - select a predefined table
            modify - modify a predefined partition table
            name   - name the current table
            print  - display the current table
            label  - write partition map and label to the disk
            ! - execute , then return
            quit
    partition> print
    Current partition table (original):
    Total disk cylinders available: 4093 + 2 (reserved cylinders)

    Part      Tag    Flag     Cylinders        Size            Blocks
      0 unassigned    wm       0               0         (0/0/0)           0
      1 unassigned    wm       0               0         (0/0/0)           0
      2     backup    wu       0 - 4092        7.99GB    (4093/0/0) 16764928
      3 unassigned    wm       0               0         (0/0/0)           0
      4 unassigned    wm       0               0         (0/0/0)           0
      5 unassigned    wm       0               0         (0/0/0)           0
      6 unassigned    wm       0               0         (0/0/0)           0
      7 unassigned    wm       0               0         (0/0/0)           0
      8       boot    wu       0 -    0        2.00MB    (1/0/0)        4096
      9 unassigned    wm       0               0         (0/0/0)           0


You can also run *verify* from format and it will give you similar output:

    format> verify

    Primary label contents:

    Volume name = root
    ascii name  = vmware -Virtualdisk-1.0 cyl 4093 alt 2 hd 128 sec 32
    pcyl        = 4095
    ncyl        = 4093
    acyl        =    2
    bcyl        =    0
    nhead       =  128
    nsect       =   32
    Part      Tag    Flag     Cylinders        Size            Blocks
      0 unassigned    wm       0               0         (0/0/0)           0
      1 unassigned    wm       0               0         (0/0/0)           0
      2     backup    wu       0 - 4092        7.99GB    (4093/0/0) 16764928
      3 unassigned    wm       0               0         (0/0/0)           0
      4 unassigned    wm       0               0         (0/0/0)           0
      5 unassigned    wm       0               0         (0/0/0)           0
      6 unassigned    wm       0               0         (0/0/0)           0
      7 unassigned    wm       0               0         (0/0/0)           0
      8       boot    wu       0 -    0        2.00MB    (1/0/0)        4096
      9 unassigned    wm       0               0         (0/0/0)           0


So we have slices 0-9, that means that this is a VTOC disk label which is what we wanted. If we wanted to change the disk label to EFI, we would run 'format -e' and then we could change the label.

Now we need to create/set slice 0 to take the whole fdisk partition (8GB). I first checked how the original drive looks like:

    format> verify

    Primary label contents:

    Volume name = root
    ascii name  =
    pcyl        = 33417
    ncyl        = 33415
    acyl        =    2
    bcyl        =    0
    nhead       =  255
    nsect       =   63
    Part      Tag    Flag     Cylinders         Size            Blocks
      0       root    wm       1 - 33414      255.96GB    (33414/0/0) 536795910
      1 unassigned    wm       0                0         (0/0/0)             0
      2     backup    wu       0 - 33414      255.97GB    (33415/0/0) 536811975
      3 unassigned    wm       0                0         (0/0/0)             0
      4 unassigned    wm       0                0         (0/0/0)             0
      5 unassigned    wm       0                0         (0/0/0)             0
      6 unassigned    wm       0                0         (0/0/0)             0
      7 unassigned    wm       0                0         (0/0/0)             0
      8       boot    wu       0 -     0        7.84MB    (1/0/0)         16065
      9 unassigned    wm       0                0         (0/0/0)             0


The installation process set partition/slice 0 to have the tag of 'root' and to use the whole "fdisk partition". Here is what I did to setup the same slice 0 on my new drive:

    root@openindiana:~# format
    Searching for disks...done

    AVAILABLE DISK SELECTIONS:
           0. c3t0d0
              /pci@0,0/pci15ad,1976@10/sd@0,0
           1. c4t0d0
              /pci@0,0/pci15ad,790@11/pci15ad,1976@2/sd@0,0
    Specify disk (enter its number): 1
    selecting c4t0d0
    [disk formatted]

    FORMAT MENU:
            disk       - select a disk
            type       - select (define) a disk type
            partition  - select (define) a partition table
            current    - describe the current disk
            format     - format and analyze the disk
            fdisk      - run the fdisk program
            repair     - repair a defective sector
            label      - write label to the disk
            analyze    - surface analysis
            defect     - defect list management
            backup     - search for backup labels
            verify     - read and display labels
            save       - save new disk/partition definitions
            inquiry    - show vendor, product and revision
            volname    - set 8-character volume name
            !          - execute , then return
            quit
    format> partition

    PARTITION MENU:
            0      - change '0' partition
            1      - change '1' partition
            2      - change '2' partition
            3      - change '3' partition
            4      - change '4' partition
            5      - change '5' partition
            6      - change '6' partition
            7      - change '7' partition
            select - select a predefined table
            modify - modify a predefined partition table
            name   - name the current table
            print  - display the current table
            label  - write partition map and label to the disk
            !      - execute , then return
            quit
    partition> 0
    Part Tag        Flag     Cylinders        Size            Blocks
      0 unassigned    wm       0               0             (0/0/0)  0

    Enter partition id tag[unassigned]: root
    Enter partition permission flags[wm]:
    Enter new starting cyl[1]:
    Enter partition size[0b, 0c, 1e, 0.00mb, 0.00gb]: 4092c
    partition> print
    Current partition table (unnamed):
    Total disk cylinders available: 4093 + 2 (reserved cylinders)

    Part      Tag    Flag     Cylinders        Size            Blocks
      0       root    wm       1 - 4092        7.99GB    (4092/0/0) 16760832
      1 unassigned    wm       0               0         (0/0/0)           0
      2     backup    wu       0 - 4092        7.99GB    (4093/0/0) 16764928
      3 unassigned    wm       0               0         (0/0/0)           0
      4 unassigned    wm       0               0         (0/0/0)           0
      5 unassigned    wm       0               0         (0/0/0)           0
      6 unassigned    wm       0               0         (0/0/0)           0
      7 unassigned    wm       0               0         (0/0/0)           0
      8       boot    wu       0 -    0        2.00MB    (1/0/0)        4096
      9 unassigned    wm       0               0         (0/0/0)           0

    partition> quit

    FORMAT MENU:
            disk       - select a disk
            type       - select (define) a disk type
            partition  - select (define) a partition table
            current    - describe the current disk
            format     - format and analyze the disk
            fdisk      - run the fdisk program
            repair     - repair a defective sector
            label      - write label to the disk
            analyze    - surface analysis
            defect     - defect list management
            backup     - search for backup labels
            verify     - read and display labels
            save       - save new disk/partition definitions
            inquiry    - show vendor, product and revision
            volname    - set 8-character volume name
            !     - execute , then return
            quit

    format> quit
    root@openindiana:~#


Now we can start migrating the OS ZFS Volumes to the new smaller disk. There a couple of prerequisites to boot from a ZFS root filesystem, the oracle article "[Installing and Booting a ZFS Root File System](http://docs.oracle.com/cd/E19082-01/817-2271/zfsboot-2/index.html)" has a good list:

> *   The pool that is intended for the root pool must have an SMI label. This requirement should be met if the pool is created with disk slices.
> *   The pool must exist either on a disk slice or on disk slices that are mirrored.
> *   On an x86 based system, the disk must contain a Solaris fdisk partition. A Solaris fdisk partition is created automatically when the x86 based system is installed.
> *   Disks that are designated for booting in a ZFS root pool must be limited to 1 TB in size on both SPARC based and x86 based systems.
> *   Compression can be enabled on the root pool but only after the root pool is installed. No way exists to enable compression on a root pool during installation. The gzip compression algorithm is not supported on root pools.
> *   Do not rename the root pool after it is created by an initial installation or after Solaris Live Upgrade migration to a ZFS root file system. Renaming the root pool might cause an unbootable system.

There is also an extensive list in an 'Solaris Internals' page called "[ZFS Best Practices Guide](http://www.open-tech.com/2011/10/zfs-best-practices-guide-from-solaris-internals/)".

We covered all the prerequisites, so let's get started. First, let's create a new pool from the new slice that we created:

    root@openindiana:~# zpool create -f syspool c4t0d0s0


Let's make sure it looks good:

    root@openindiana:~# zpool status syspool
    pool: syspool
    state: ONLINE
    scan: none requested
    config:
            NAME        STATE     READ WRITE CKSUM
            syspool     ONLINE       0     0     0
              c4t0d0s0  ONLINE       0     0     0

    errors: No known data errors


Since we can enable compression, let's do that:

    root@openindiana:~# zfs set compression=on syspool


Now we can create a BE in our smaller pool. Most of the intructions can be found in the Oracle document called "[Managing Your ZFS Root Pool](http://docs.oracle.com/cd/E23824_01/html/821-1448/gjtuk.html)". Here is how beadm looks like prior to any changes:

    root@openindiana:~# beadm list -d
    BE/Dataset                   Active Mountpoint Space Policy Created
    openindiana
       rpool1/ROOT/openindiana   -      -          8.31M static 2012-05-29 10:09
    openindiana-1
       rpool1/ROOT/openindiana-1 NR     /          3.27G static 2012-05-29 11:26


NR stands for "Now Running", and BE stands for "Boot Environment". If you want to see more examples using **beadm**, check out the Oracle man page for [beadm](http://docs.oracle.com/cd/E19963-01/html/821-1462/beadm-1m.html). So let's create a new BE from the active BE (openindiana-1) in the smaller pool and call it "openindiana-os":

    root@openindiana:~# beadm create -p syspool openindiana-os
    Created successfully


So here is how the setup looks like after the new BE is created:

    root@openindiana:~# zfs list -r syspool
    NAME                          USED  AVAIL  REFER  MOUNTPOINT
    syspool                      1021M  6.82G    36K  /syspool
    syspool/ROOT                 1020M  6.82G    31K  legacy
    syspool/ROOT/openindiana-os  1020M  6.82G  1020M  /

    root@openindiana:~# beadm list -d
    BE/Dataset                     Active Mountpoint Space Policy Created
    openindiana
       rpool1/ROOT/openindiana     -      -          8.31M static 2012-05-29 10:09
    openindiana-1
       rpool1/ROOT/openindiana-1   NR     /          3.27G static 2012-05-29 11:26
    openindiana-os
       syspool/ROOT/openindiana-os R      -          1020M static 2012-08-21 16:36


As we can see only the OS ZFS volume was copied. The way that **beadm** works is described in "[Creating a Boot Environment](http://docs.oracle.com/cd/E23824_01/html/E21801/createbe.html)", from that article:

> **beadm create BE2**
>
> The original boot environment in this example is BE1. The new boot environment, BE2, contains separate datasets cloned from BE1. If BE1 contains separate datasets for traditional file systems, such as /var, then those datasets are also cloned.
>
> rpool/ROOT/BE1
> rpool/ROOT/BE1/var
>
> rpool/ROOT/BE2
> rpool/ROOT/BE2/var
>
> rpool in this example is the name of the storage pool. The pool was previously set up by the initial installation or upgrade and, therefore, already exists on the system. ROOT is a special dataset that was also created previously by the initial installation or upgrade. ROOT is reserved exclusively for use by boot environment roots.

And here is another good tidbit:

> **beadm create BE2**
>
> The shared datasets, rpool/export and rpool/export/home, are not cloned when the boot environment is cloned. The shared datasets are located outside the rpool/ROOT/ datasets and are referenced at their original locations by the cloned boot environment. The original boot environment, BE1, and datasets are as follows:
>
> rpool/ROOT/BE1
> rpool/ROOT/BE1/var
> rpool/export
> rpool/export/home
>
> The cloned boot environment, BE2, has new root datasets but the original shared datasets, rpool/export and rpool/export/home, are unchanged.
>
> rpool/ROOT/BE2
> rpool/ROOT/BE2/var
> rpool/export
> rpool/export/home

That is why our "export" ZFS Volumes are not copied. So anything within ROOT ZFS volume gets copied over but the rest is left behind. Also another resource for how beadm works can be found at "[Using beadm Utility](http://docs.oracle.com/cd/E19963-01/html/820-6565/tasks.html)":

> *   A boot environment is a bootable Oracle Solaris environment, consisting of a root dataset and, optionally, other datasets mounted underneath it. Exactly one boot environment can be active at a time.
> *   A clone of a boot environment is created by copying another boot environment. A clone is bootable.
>
> **Note** - A clone of the boot environment includes everything hierarchically under the main root dataset of the original boot environment.
>
> Shared datasets are not under the root dataset and are not cloned. Instead, the boot environment accesses the original, shared dataset.
>
> *   A dataset is a generic name for ZFS entities such as clones, file systems, or snapshots. In the context of boot environment administration, the dataset more specifically refers to the file system specifications for a particular boot environment or snapshot.
> *   Shared datasets are user-defined directories, such as /export, that contain the same mount point in both the active and inactive boot environments. Shared datasets are located outside the root dataset area of each boot environment.
> *   A boot environment's critical datasets are included within the root dataset area for that environment.

Now let's set the **bootfs** for the second smaller pool:

    root@openindiana:~# zpool set bootfs=syspool/ROOT/openindiana-os syspool


Then let's active the new BE:

    root@openindiana:~# beadm activate openindiana-os
    Activated successfully


The **beadm** command also creates an appropriate *menu.lst* file:

    root@openindiana:~# cat /syspool/boot/grub/menu.lst
    splashimage /boot/solaris.xpm
    foreground 343434
    background F7FBFF
    default 0
    timeout 30
    title openindiana-os
    bootfs syspool/ROOT/openindiana-os
    kernel$ /platform/i86pc/kernel/$ISADIR/unix -B $ZFS-BOOTFS
    module$ /platform/i86pc/$ISADIR/boot_archive

    #============ End of LIBBE entry =============#


Finally let's install grub on the our new slice, more information can be seen from "[Booting From a ZFS Root File System](http://docs.oracle.com/cd/E19963-01/html/821-1448/ggpco.html)":

    root@openindiana:~# installgrub /boot/grub/stage1 /boot/grub/stage2 /dev/rdsk/c4t0d0s0
    stage2 written to partition 0, 275 sectors starting at 50 (abs 4146)
    stage1 written to partition 0 sector 0 (abs 4096)


# Configuring the system to use the new ZFS Pool

From here we have a couple of options.

## 1. Reboot into the New ZFS Pool Using Fast Reboot

From the man page of reboot:

> On x86 systems, when the -f flag is specified, the running kernel will load the next kernel into memory, then transfer control to the newly loaded kernel. This form of reboot is shown in the second synopsis, above.
>
> **-f** Fast reboot, bypassing firmware and boot loader. The new kernel will be loaded into memory by the running kernel, and control will be transferred to the newly loaded kernel. If disk or kernel arguments are specified, they must be specified before other boot arguments. This option is currently available only on x86 systems.
>
> The following command reboots to another ZFS root pool. example# `reboot -f -- 'rpool/ROOT/root2'`

Here is what I ran to do a fast reboot.

    root@openindiana:~# reboot -f -- 'syspool/ROOT/openindiana-os'


And then you will see the following:

    root@openindiana:~# df .
    Filesystem           1K-blocks      Used Available Use% Mounted on
    syspool/ROOT/openindiana-os
                           8102131   1044912   7057219  13% /

    root@openindiana:~# beadm list
    BE             Active Mountpoint Space Policy Created
    openindiana    -      -          8.31M static 2012-05-29 10:09
    openindiana-1  R      -          4.05G static 2012-05-29 11:26
    openindiana-os NR     /          1.17G static 2012-08-21 16:36


## 2. Edit the Grub Menu from the primary ZFS Pool to boot from the new Pool

When we add a new BE by default that gets added into the *menu.lst* file. Here is how the **beadm** and **bootadm** look like:

    root@openindiana:~# beadm list
    BE             Active Mountpoint Space Policy Created
    openindiana    -      -          8.31M static 2012-05-29 10:09
    openindiana-1  NR     /          4.05G static 2012-05-29 11:26
    openindiana-os R      -          1.17G static 2012-08-21 16:36

    root@openindiana:~# bootadm list-menu
    the location for the active GRUB menu is: /rpool1/boot/grub/menu.lst
    default 1
    timeout 30
    0 OpenIndiana Development oi_151a X86
    1 openindiana-1


Now if we create a new BE within the same pool everything will work fine:

    root@openindiana:~# beadm create test
    Created successfully

    root@openindiana:~# bootadm list-menu
    the location for the active GRUB menu is: /rpool1/boot/grub/menu.lst
    default 1
    timeout 30
    0 OpenIndiana Development oi_151a X86
    1 openindiana-1
    2 test


The reason why this works is because it just updates the *menul.lst* within the pool. Each ZFS pool has it's own *menu.lst* file:

    root@openindiana:~# ls -l /rpool1/boot/grub/menu.lst
    -rw-r--r-- 1 root root 1298 2012-08-21 21:16 /rpool1/boot/grub/menu.lst
    root@openindiana:~# ls -l /syspool/boot/grub/menu.lst
    -rw-r--r-- 1 root root 294 2012-08-21 19:03 /syspool/boot/grub/menu.lst


To get around this we can append the menu.lst from the smaller pool to the original pool. So I basically copied the following:

    title openindiana-os
    bootfs syspool/ROOT/openindiana-os
    kernel$ /platform/i86pc/kernel/$ISADIR/unix -B $ZFS-BOOTFS
    module$ /platform/i86pc/$ISADIR/boot_archive


into **/rpool1/boot/grub/menu.lst**. But I also had to add this line:

    findroot (pool_syspool,0,a)


There is a little caveat regarding **findroot**. It's described in "[Modifying Boot Behavior on x86 Based Systems](http://docs.oracle.com/cd/E19963-01/html/821-1451/gkkvs.html)". From that document:

> **x86: Implementation of the findroot Command**
>
> All installation methods now use the findroot command for specifying which disk slice on an x86 based system to boot. This enhancement supports booting systems with Oracle Solaris ZFS roots. This information is located in the menu.lst file that is used by GRUB. Previously, the root command, root (hd0.0.a), was explicitly used to specify which disk slice to boot.
>
> In addition to the findroot command, is a signature file on the slice, (mysign, 0, a), where mysign is the name of a signature file that is located in the /boot/grub/bootsign directory. When booting a system from a ZFS root, the ZFS GRUB plug-in looks for and tries to mount a ZFS file system in slice a of fdisk partition 0. The name of the signature file varies, depending on the installation method that was used.
>
> **Caution** - The boot signature must be unique. Do not use or remove system-generated signatures or user signatures that are duplicated across multiple instances of the Oracle Solaris software. Doing so might result in booting an incorrect OS instance or prevent the system from booting.

From the same page they have an example:

> **x86: How to Add GRUB Menu Entries That Use the findroot Command**
>
> This procedure shows how to manually update the menu.lst file with user-defined entries that use the findroot command. Typically, these entries are added after an installation or an upgrade. For guidelines on adding user-defined entries that use the findroot command, see x86: Implementation of the findroot Command.
>
> 1.  Become the root user..
> 2.  Create a boot signature file on the root (/) file system or root pool that will be booted.
>
> For a ZFS pool, my-pool, create the boot signature file in the /my-pool/boot/grub/bootsign directory.
>
>     # touch /my-pool/boot/grub/bootsign/user-sign
>

So I created my user-sign file:

    root@openindiana:~# mkdir /syspool/boot/grub/bootsign
    root@openindiana:~# touch /syspool/boot/grub/bootsign/pool_syspool


and I of course had the following in the original pool's *menu.lst* file:

    root@openindiana:~# tail -5 /rpool1/boot/grub/menu.lst
    title openindiana-os
    findroot (pool_syspool,0,a)
    bootfs syspool/ROOT/openindiana-os
    kernel$ /platform/i86pc/kernel/$ISADIR/unix -B $ZFS-BOOTFS
    module$ /platform/i86pc/$ISADIR/boot_archive


After that, looking at the bootadm command yielded the following:

    root@openindiana:~# bootadm list-menu
    the location for the active GRUB menu is: /rpool1/boot/grub/menu.lst
    default 1
    timeout 30
    0 OpenIndiana Development oi_151a X86
    1 openindiana-1
    2 test
    3 openindiana-os


I then set the default to be '3', our new BE (openindiana-os):

    root@openindiana:~# bootadm set-menu default=3
    root@openindiana:~# bootadm list-menu
    the location for the active GRUB menu is: /rpool1/boot/grub/menu.lst
    default 3
    timeout 30
    0 OpenIndiana Development oi_151a X86
    1 openindiana-1
    2 test
    3 openindiana-os


Now I can do a regular reboot.

    root@openindiana:~# reboot


After the reboot I saw the following:

    root@openindiana:~# bootadm list-menu
    the location for the active GRUB menu is: /syspool/boot/grub/menu.lst
    default 0
    timeout 30
    0 openindiana-os

    root@openindiana:~# beadm list
    BE             Active Mountpoint Space Policy Created
    openindiana    -      -          8.31M static 2012-05-29 10:09
    openindiana-1  -      -          4.06G static 2012-05-29 11:26
    openindiana-os NR     /          1.17G static 2012-08-21 16:36
    test           -      -          37.0K static 2012-08-21 21:16

    root@openindiana:~# df .
    Filesystem           1K-blocks      Used Available Use% Mounted on
    syspool/ROOT/openindiana-os
                           8099231   1044922   7054309  13% /


We can see that we only have one output from **bootadm**, and that is because we are reading from the pool that we are booting from and there is only one BE there. But we successfully booted into the new BE. If for some reason you want to boot back into the original pool you can edit the **/rpool1/boot/grub/menu.lst** file and change the default line to point at your BE.

## 3. Make the original ZFS pool not bootable

The easiest way to accomplish this would be to make the fdisk partition not active/bootable. Let's fire up fdisk:

    root@openindiana:~# fdisk /dev/rdsk/c3t0d0p0
                 Total disk size is 33418 cylinders
                 Cylinder size is 16065 (512 byte) blocks

                                                    Cylinders
      Partition   Status    Type          Start   End   Length    %
      =========   ======    ============  =====   ===   ======   ===
          1       Active    Solaris2          1  33417    33417    100

    SELECT ONE OF THE FOLLOWING:
       1. Create a partition
       2. Specify the active partition
       3. Delete a partition
       4. Change between Solaris and Solaris2 Partition IDs
       5. Edit/View extended partitions
       6. Exit (update disk configuration and exit)
       7. Cancel (exit without updating disk configuration)
    Enter Selection: 2


Then select '0'; to not have any bootable partitions:

![select_none_to_boot_from](http://virtuallyhyper.com/wp-content/uploads/2012/08/select_none_to_boot_from.png)

then exit and commit the changes:

![deactivate-bootable-parition](http://virtuallyhyper.com/wp-content/uploads/2012/08/deactivate-bootable-parition1.png)

So checking the partition prior to the change, I saw the following:

    root@openindiana:~# fdisk -W - /dev/rdsk/c3t0d0p0
    *   /dev/rdsk/c3t0d0p0 default fdisk table
    *   Dimensions:
    *   512 bytes/sector
    *   63 sectors/track
    *   255 tracks/cylinder
    *   33418 cylinders
    *
    *   systid:
    *   1: DOSOS12
    *   2: PCIXOS
    *   4: DOSOS16
    *   5: EXTDOS
    *   6: DOSBIG
    *   7: FDISK_IFS
    *   8: FDISK_AIXBOOT
    *   9: FDISK_AIXDATA
    *   10: FDISK_0S2BOOT
    *   11: FDISK_WINDOWS
    *   12: FDISK_EXT_WIN
    *   14: FDISK_FAT95
    *   15: FDISK_EXTLBA
    *   18: DIAGPART
    *   65: FDISK_LINUX
    *   82: FDISK_CPM
    *   86: DOSDATA
    *   98: OTHEROS
    *   99: UNIXOS
    *   100: FDISK_NOVELL2
    *   101: FDISK_NOVELL3
    *   119: FDISK_QNX4
    *   120: FDISK_QNX42
    *   121: FDISK_QNX43
    *   130: SUNIXOS
    *   131: FDISK_LINUXNAT
    *   134: FDISK_NTFSVOL1
    *   135: FDISK_NTFSVOL2
    *   165: FDISK_BSD
    *   167: FDISK_NEXTSTEP
    *   183: FDISK_BSDIFS
    *   184: FDISK_BSDISWAP
    *   190: X86BOOT
    *   191: SUNIXOS2
    *   238: EFI_PMBR
    *   239: EFI_FS
    *
    Id    Act  Bhead  Bsect  Bcyl    Ehead  Esect  Ecyl    Rsect      Numsect
    191   128  0      1      1       254    63     1023    16065      536844105
    0     0    0      0      0       0      0      0       0          0
    0     0    0      0      0       0      0      0       0          0
    0     0    0      0      0       0      0      0       0          0


Then checking it afterwards:

    root@openindiana:~# fdisk -W - /dev/rdsk/c3t0d0p0
    *   /dev/rdsk/c3t0d0p0 default fdisk table
    *   Dimensions:
    *   512 bytes/sector
    *   63 sectors/track
    *   255 tracks/cylinder
    *   33418 cylinders
    *
    *   systid:
    *   1: DOSOS12
    *   2: PCIXOS
    *   4: DOSOS16
    *   5: EXTDOS
    *   6: DOSBIG
    *   7: FDISK_IFS
    *   8: FDISK_AIXBOOT
    *   9: FDISK_AIXDATA
    *   10: FDISK_0S2BOOT
    *   11: FDISK_WINDOWS
    *   12: FDISK_EXT_WIN
    *   14: FDISK_FAT95
    *   15: FDISK_EXTLBA
    *   18: DIAGPART
    *   65: FDISK_LINUX
    *   82: FDISK_CPM
    *   86: DOSDATA
    *   98: OTHEROS
    *   99: UNIXOS
    *   100: FDISK_NOVELL2
    *   101: FDISK_NOVELL3
    *   119: FDISK_QNX4
    *   120: FDISK_QNX42
    *   121: FDISK_QNX43
    *   130: SUNIXOS
    *   131: FDISK_LINUXNAT
    *   134: FDISK_NTFSVOL1
    *   135: FDISK_NTFSVOL2
    *   165: FDISK_BSD
    *   167: FDISK_NEXTSTEP
    *   183: FDISK_BSDIFS
    *   184: FDISK_BSDISWAP
    *   190: X86BOOT
    *   191: SUNIXOS2
    *   238: EFI_PMBR
    *   239: EFI_FS
    *
    Id    Act  Bhead  Bsect  Bcyl    Ehead  Esect  Ecyl    Rsect      Numsect
    191   0    0      1      1       254    63     1023    16065      536844105
    0     0    0      0      0       0      0      0       0          0
    0     0    0      0      0       0      0      0       0          0
    0     0    0      0      0       0      0      0       0          0


We can see that the Act field goes from 128 to 0. From the man page of fdisk:

    Change Active (Boot from) partition

             This option allows the user  to  specify  the  partition
             where  the  first-stage  bootstrap  will  look  for  the
             second-stage bootstrap, otherwise known  as  the  active
             partition.


    ...
    ...
    act
             This is the active partition flag; 0 means not active and
             128 means active. For logical drives, this flag will always
             be set to 0 even if specified as 128 by the user.


This is just to make sure that we don't accidentally boot from the old ZFS Pool. You can reboot now, however make sure you BIOS will boot from the second drive if it can't boot from the first one. You might have to set your secondary drive as a slave in the BIOS.

    root@openindiana:~# reboot


## 4. Change the boot order in the BIOS to boot from the second drive

This one is the least work and probably the most appropriate. Just go to the bios and change the boot order. Then just reboot and hope all is well, before the reboot here is how df looks like

    root@openindiana:~# df .
    Filesystem           1K-blocks      Used Available Use% Mounted on
    rpool1/ROOT/openindiana-1
                           8686293   1904522   6781771  22% /
    root@openindiana:~# reboot


and this is after:

    root@openindiana:~# beadm list
    BE             Active Mountpoint Space Policy Created
    openindiana    -      -          8.31M static 2012-05-29 10:09
    openindiana-1  R      -          4.08G static 2012-05-29 11:26
    openindiana-os NR     /          1.18G static 2012-08-21 16:36
    test           -      -          37.0K static 2012-08-21 21:16

    root@openindiana:~# df .
    Filesystem           1K-blocks      Used Available Use% Mounted on
    syspool/ROOT/openindiana-os
                           8096823   1044935   7051889  13% /


# Cleaning up the system

Now for the clean up. First let's move out export dataset to the smaller pool (syspool). First let's take a recursive snapshot of my export dataset:

    root@openindiana:~# zfs snapshot -r rpool1/export@migrate


Then let's make sure it created snapshots for all the descendents:

    root@openindiana:~# zfs list -t snapshot -r rpool1 | grep export
    rpool1/export@migrate                              0      -    32K  -
    rpool1/export/home@migrate                         0      -    32K  -
    rpool1/export/home/elatov@migrate                  0      -  34.5K  -


That looks good, now let's migrate the whole export dataset:

    root@openindiana:~# zfs send -R rpool1/export@migrate | zfs receive syspool/export
    cannot mount '/export': directory is not empty


The error is okay, since I am already mounting /export from the original pool (rpool1). But let's ensure the data transferred:

    root@openindiana:~# zfs list -r syspool | grep export
    syspool/export               97.5K  6.72G    32K  /export
    syspool/export/home          65.5K  6.72G    32K  /export/home
    syspool/export/home/elatov   33.5K  6.72G  33.5K  /export/home/elatov


That is perfect. BTW there a lot of good example of how to use 'zfs send and receive' in the Oracle documentation "[Sending and Receiving ZFS Data](http://docs.oracle.com/cd/E23824_01/html/821-1448/gbchx.html)".

Remove the old export ZFS volume so there are no mounting issues:

    root@openindiana:~# zfs destroy -r rpool1/export


Now go ahead and create a swap partition on the new pool and set it up to be auto mounted:

    root@openindiana:~# zfs create -V 1g syspool/swap
    root@openindiana:~# vi /etc/vfstab


modify the swap line to look like this:

    /dev/zvol/dsk/syspool/swap - - swap - no -


Then let's fix the dump partition:

    root@openindiana:~# zfs create -V 1g syspool/dump
    root@openindiana:~# dumpadm -d /dev/zvol/dsk/syspool/dump
          Dump content: kernel pages
           Dump device: /dev/zvol/dsk/syspool/dump (dedicated)
    Savecore directory: /var/crash/openindiana
      Savecore enabled: no
       Save compressed: on


Let's reboot and make sure it looks good. Prior to the reboot here is how the swap looked like:

    root@openindiana:~# swap -l
    swapfile             dev    swaplo   blocks     free
    /dev/zvol/dsk/rpool1/swap 179,2         8  2097144  2097144


And here is how it looked like after the reboot:

    root@openindiana:~# swap -l
    swapfile             dev    swaplo   blocks     free
    /dev/zvol/dsk/syspool/swap 179,2         8  2097144  2097144

    root@openindiana:~# df -h | grep export
    syspool/export        4.7G   32K  4.7G   1% /export
    syspool/export/home   4.7G   32K  4.7G   1% /export/home
    syspool/export/home/elatov
                          4.7G   34K  4.7G   1% /export/home/elatov
    /export/home/elatov   4.7G   34K  4.7G   1% /home/elatov


Now let's clean up my beadm setup:

    root@openindiana:~# beadm list
    BE             Active Mountpoint Space Policy Created
    openindiana    -      -          8.31M static 2012-05-29 10:09
    openindiana-1  R      -          4.08G static 2012-05-29 11:26
    openindiana-os NR     /          1.18G static 2012-08-21 16:36
    test           -      -          37.0K static 2012-08-21 21:16


Let's remove everything expect 'openindiana-os':

    root@openindiana:~# beadm destroy test
    Are you sure you want to destroy test?
    This action cannot be undone (y/[n]): y
    Destroyed successfully

    root@openindiana:~# beadm destroy openindiana
    Are you sure you want to destroy openindiana?
    This action cannot be undone (y/[n]): y
    Destroyed successfully

    root@openindiana:~# beadm destroy -s openindiana-1
    Are you sure you want to destroy openindiana-1?
    This action cannot be undone (y/[n]): y
    Destroyed successfully


Let's see how it looks:

    root@openindiana:~# beadm list
    BE             Active Mountpoint Space Policy Created
    openindiana-os NR     /          1.18G static 2012-08-21 16:36

    root@openindiana:~# bootadm list-menu
    the location for the active GRUB menu is: /syspool/boot/grub/menu.lst
    default 0
    timeout 30
    0 openindiana-os


That is perfect, now let's go ahead and clean up some left over ZFS volumes under rpool1:

    root@openindiana:~# zfs list -r rpool1
    NAME                  USED  AVAIL  REFER  MOUNTPOINT
    rpool1                240G  9.74G    46K  /rpool1
    rpool1/ROOT            31K  9.74G    31K  legacy
    rpool1/dump          1.00G  10.7G    16K  -
    rpool1/iscsi_share    103G   108G  4.71G  -
    rpool1/iscsi_share2   134G   144G  26.5M  -
    rpool1/nfs_share     1000M  9.74G  1000M  /rpool1/nfs_share
    rpool1/swap          1.06G  10.7G   133M  -


This was pretty easy:

    root@openindiana:~# zfs destroy rpool1/ROOT
    root@openindiana:~# zfs destroy rpool1/dump
    root@openindiana:~# zfs destroy rpool1/swap
    root@openindiana:~# zfs list -r rpool1
    NAME                  USED  AVAIL  REFER  MOUNTPOINT
    rpool1                238G  11.8G    46K  /rpool1
    rpool1/iscsi_share    103G   110G  4.71G  -
    rpool1/iscsi_share2   134G   146G  26.5M  -
    rpool1/nfs_share     1000M  11.8G  1000M  /rpool1/nfs_share


and that is it. Now my OS has a separate pool from my data pool:

    root@openindiana:~# zpool status
      pool: rpool1
     state: ONLINE
      scan: none requested
    config:

            NAME        STATE     READ WRITE CKSUM
            rpool1      ONLINE       0     0     0
              c3t0d0s0  ONLINE       0     0     0

    errors: No known data errors

      pool: syspool
     state: ONLINE
      scan: none requested
    config:

            NAME        STATE     READ WRITE CKSUM
            syspool     ONLINE       0     0     0
              c4t0d0s0  ONLINE       0     0     0

    errors: No known data errors

    root@openindiana:~# zfs list
    NAME                          USED  AVAIL  REFER  MOUNTPOINT
    rpool1                        238G  11.8G    46K  /rpool1
    rpool1/iscsi_share            103G   110G  4.71G  -
    rpool1/iscsi_share2           134G   146G  26.5M  -
    rpool1/nfs_share             1000M  11.8G  1000M  /rpool1/nfs_share
    syspool                      3.12G  4.69G    37K  /syspool
    syspool/ROOT                 1.09G  4.69G    31K  legacy
    syspool/ROOT/openindiana-os  1.09G  4.69G  1020M  /
    syspool/dump                 1.00G  4.69G  1.00G  -
    syspool/export                116K  4.69G    32K  /export
    syspool/export/home          65.5K  4.69G    32K  /export/home
    syspool/export/home/elatov   33.5K  4.69G  33.5K  /export/home/elatov
    syspool/swap                 1.03G  5.72G    16K  -
    root@openindiana:~#


That was pretty easy.

