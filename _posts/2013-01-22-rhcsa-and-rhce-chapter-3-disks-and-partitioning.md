---
title: RHCSA and RHCE Chapter 3 Disks and Partitioning
author: Karim Elatov
layout: post
permalink: /2013/01/rhcsa-and-rhce-chapter-3-disks-and-partitioning/
categories: ['storage','os','home_lab', 'certifications', 'rhcsa_rhce']
tags: ['ext3', 'linux', 'fdisk', 'lvm', 'mdadm', 'raid', 'yum']
---

### RHEL DVD as a Software Repository

Before we keep going with disk and partitioning, I want to setup the RHEL Install DVD as a Software Repository (I will cover this in more detail in [chapter 6](/2013/03/rhcsa-and-rhce-chapter-6-package-management/)) since I will need to install **parted** and I currently don't have that installed:

    [root@rhel01 ~]# which parted
    /usr/bin/which: no parted in (/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin)


From "[Red Hat Enterprise Linux 6 Installation Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf)":

> **35.3.1.2. Using a Red Hat Enterprise Linux Installation DVD as a Software Repository**
>
> To use a Red Hat Enterprise Linux installation DVD as a software repository, either in the form of a physical disc, or in the form of an ISO image file.
>
> 1.  If you are using a physical DVD, insert the disc into your computer.
> 2.  If you are not already root, switch users to the root account: `su -`
> 3.  Create a mount point for the repository: `mkdir -p /path/to/repo` where **/path/to/repo** is a location for the repository, for example, **/mnt/repo**
> 4.  Mount the DVD on the mount point that you just created. If you are using a physical disc, you need to know the device name of your DVD drive. You can find the names of any CD or DVD drives on your system with the command **cat /proc/sys/dev/cdrom/info**.
>
>     The first CD or DVD drive on the system is typically named sr0. When you know the device name, mount the DVD: `mount -r -t iso9660 /dev/device_name /path/to/repo` For example: **mount -r -t iso9660 /dev/sr0 /mnt/repo** If you are using an ISO image file of a disc, mount the image file like this: `mount -r -t iso9660 -o loop /path/to/image/file.iso /path/to/repo`
>
>     For example: **mount -r -o loop /home/root/Downloads/RHEL6-Server-i386-DVD.iso /mnt/repo**
>
>     Note that you can only mount an image file if the storage device that holds the image file is itself mounted. For example, if the image file is stored on a hard drive that is not mounted automatically when the system boots, you must mount the hard drive before you mount an image file stored on that hard drive. Consider a hard drive named /dev/sdb that is not automatically mounted at boot time and which has an image file stored in a directory named Downloads on its first partition:
>
>         mkdir /mnt/temp
>         mount /dev/sdb1 /mnt/temp
>         mkdir /mnt/repo
>         mount -r -o loop /mnt/temp/Downloads/RHEL6-Server-i386-DVD.iso /mnt/repo
>
>
>     If you are not sure whether a storage device is mounted, run the **mount** command to obtain a list of current mounts. If you are not sure of the device name or partition number of a storage device, run **fdisk -l** and try to identify it in the output.
>
> 5.  Create a new repo file in the **/etc/yum.repos.d/** directory. The name of the file is notimportant, as long as it ends in .repo. For example, **dvd.repo** is an obvious choice.
>
>     1.  Choose a name for the repo file and open it as a new file with the vi text editor. For example: `vi /etc/yum.repos.d/dvd.repo`
>     2.  Press the I key to enter insert mode.
>     3.  Supply the details of the repository. For example:
>
>             [dvd]
>             baseurl=file:///mnt/repo/Server
>             enabled=1
>             gpgcheck=1
>             gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
>
>
>         The name of the repository is specified in square brackets — in this example, [dvd]. The name is not important, but you should choose something that is meaningful and recognizable.
>
>         The line that specifies the **baseurl** should contain the path to the mount point that you created previously, suffixed with **/Server** for a Red Hat Enterprise Linux server installation DVD, or with **/Client** for a Red Hat Enterprise Linux client installation DVD.
>
>     4.  Press the **Esc** key to exit **insert** mode.
>
>     5.  Type **:wq** and press the **Enter** key to save the file and exit the vi text editor.
>     6.  After installing or upgrading software from the DVD, delete the repo file that you created

Here is what I did to setup up a local repo. First I mounted the iso to my VM and then I found out what is the disk device of my cd-rom:

    [root@rhel01 ~]# cat /proc/sys/dev/cdrom/info
    CD-ROM information, Id: cdrom.c 3.20 2003/12/17

    drive name: sr0
    drive speed: 1
    drive # of slots: 1
    Can close tray: 1
    Can open tray: 1
    Can lock tray: 1
    Can change speed: 1
    Can select disk: 0
    Can read multisession: 1
    Can read MCN: 1
    Reports media changed: 1
    Can play audio: 1
    Can write CD-R: 1
    Can write CD-RW: 1
    Can read DVD: 1
    Can write DVD-R: 1
    Can write DVD-RAM: 1
    Can read MRW: 0
    Can write MRW: 0
    Can write RAM: 0


And then mounting the disk, I did the following:

    [root@rhel01 ~]# mkdir /mnt/cd
    [root@rhel01 ~]# mount /dev/sr0 /mnt/cd
    mount: block device /dev/sr0 is write-protected, mounting read-only


Now checking if it's mounted, I saw the following:

    [root@rhel01 ~]# df -h | grep cd
    /dev/sr0 3.5G 3.5G 0 100% /mnt/cd


I didn't want to keep mounting the iso so I just copied the contents of the cd to **/root/repo**. I would usually use **rsync** to copy to the data, but I didn't have that installed yet, so I used **cp**:

    [root@rhel01 ~]# mkdir repo
    [root@rhel01 ~]# cp -Rv /mnt/cd/* /root/repo/.
    /mnt/cd/EULA -> /root/repo/./EULA
    /mnt/cd/GPL -> /root/repo/./GPL
    /mnt/cd/images -> /root/repo/./images
    /mnt/cd/images/README -> /root/repo/./images/README
    /mnt/cd/images/TRANS.TBL ->/root/repo/./images/TRANS.TBL
    /mnt/cd/images/install.img ->/root/repo/./images/install.img


That kept going for a while. After it was done these were the contents of /root/repo:

    [root@rhel01 ~]# ls repo
    EULA RELEASE-NOTES-fr-FR.html RELEASE-NOTES-ru-RU.html
    GPL RELEASE-NOTES-gu-IN.html RELEASE-NOTES-si-LK.html
    images RELEASE-NOTES-hi-IN.html RELEASE-NOTES-ta-IN.html
    isolinux RELEASE-NOTES-it-IT.html RELEASE-NOTES-te-IN.html
    media.repo RELEASE-NOTES-ja-JP.html RELEASE-NOTES-zh-CN.html
    Packages RELEASE-NOTES-kn-IN.html RELEASE-NOTES-zh-TW.html
    README RELEASE-NOTES-ko-KR.html repodata
    RELEASE-NOTES-as-IN.html RELEASE-NOTES-ml-IN.html RPM-GPG-KEY-redhat-beta
    RELEASE-NOTES-bn-IN.html RELEASE-NOTES-mr-IN.html RPM-GPG-KEY-redhat-release
    RELEASE-NOTES-de-DE.html RELEASE-NOTES-or-IN.html TRANS.TBL
    RELEASE-NOTES-en-US.html RELEASE-NOTES-pa-IN.html Workstation
    RELEASE-NOTES-es-ES.html RELEASE-NOTES-pt-BR.html


Now creating the **yum** repository configuration file:

    [root@rhel01 ~]# vi /etc/yum.repos.d/dvd.repo


Here are the contents of my repo file:

    [root@rhel01 ~]# cat /etc/yum.repos.d/dvd.repo
    [dvd]
    baseurl=file:///root/repo/Workstation
    name=rhel_dvd
    enabled=1
    gpgcheck=1
    gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-redhat-release


Now checking if the repo was added:

    [root@rhel01 ~]# yum repolist
    Loaded plugins: product-id, subscription-manager
    Updating certificate-based repositories.
    Unable to read consumer identity
    dvd | 4.0 kB 00:00 ...
    dvd/primary_db | 2.6 MB 00:00 ...
    repo id repo name status
    dvd dvd 3,050
    repolist: 3,050


Now to see if **parted** is part of the **dvd** repository:

    [root@rhel01 ~]# yum search parted
    Loaded plugins: product-id, subscription-manager
    Updating certificate-based repositories.
    Unable to read consumer identity
    ============================= N/S Matched: parted ==============================
    pyparted.i686 : Python module for GNU parted
    parted.i686 : The GNU disk partition manipulation program


That looks good. If you want to know which repo provides a certain package you can run '**yum list**' like so:

    [root@rhel01 ~]# yum list | grep parted
    Unable to read consumer identity
    parted.i686 2.1-18.el6 dvd
    pyparted.i686 3.4-3.el6 dvd


Now to install the package:

    [root@rhel01 ~]# yum install parted


### Hard Disks

Now to partitions, from "[Red Hat Enterprise Linux 6 Installation Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf)":

> **A.1. Hard Disk Basic Concepts**
>
> Hard disks perform a very simple function — they store data and reliably retrieve it on command.
>
> When discussing issues such as disk partitioning, it is important to know a bit about the underlying hardware. Unfortunately, it is easy to become bogged down in details. Therefore, this appendix uses a simplified diagram of a disk drive to help explain what is really happening when a disk drive is partitioned. Figure A.1, “An Unused Disk Drive”, shows a brand-new, unused disk drive.
>
> ![unused disk drive RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/unused_disk_drive.png)
>
> Not much to look at, is it? But if we are talking about disk drives on a basic level, it is adequate. Say that we would like to store some data on this drive. As things stand now, it will not work. There is something we need to do first.
>
> **A.1.1. It is Not What You Write, it is How You Write It**
>
> Experienced computer users probably got this one on the first try. We need to format the drive. Formatting (usually known as "making a file system") writes information to the drive, creating order out of the empty space in an unformatted drive.
>
> ![disk drive with data RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/disk_drive_with_data.png)
>
> As Figure A.2, “Disk Drive with a File System”, implies, the order imposed by a file system involves some trade-offs:
>
> 1.  A small percentage of the drive's available space is used to store file system-related data and can be considered as overhead.
> 2.  A file system splits the remaining space into small, consistently-sized segments. For Linux, these segments are known as blocks.
>
> Given that file systems make things like directories and files possible, these trade-offs are usually seen as a small price to pay.
>
> It is also worth noting that there is no single, universal file system. As Figure A.3, “Disk Drive with a Different File System”, shows, a disk drive may have one of many different file systems written on it. As you might guess, different file systems tend to be incompatible; that is, an operating system that supports one file system (or a handful of related file system types) may not support another. This last statement is not a hard-and-fast rule, however. For example, Red Hat Enterprise Linux supports a wide variety of file systems (including many commonly used by other operating systems), making data interchange between different file systems easy.
>
> ![disk with another fs RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/disk_with_another_fs.png)
>
> Of course, writing a file system to disk is only the beginning. The goal of this process is to actually store and retrieve data. Let us take a look at our drive after some files have been written to it.
>
> ![disk data written RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/disk_data_written.png)
>
> As Figure A.4, “Disk Drive with Data Written to It”, shows, some of the previously-empty blocks are now holding data. However, by just looking at this picture, we cannot determine exactly how many files reside on this drive. There may only be one file or many, as all files use at least one block and some files use multiple blocks. Another important point to note is that the used blocks do not have to form a contiguous region; used and unused blocks may be interspersed. This is known as fragmentation. **Fragmentation** can play a part when attempting to resize an existing partition.
>
> As with most computer-related technologies, disk drives changed over time after their introduction. In particular, they got bigger. Not larger in physical size, but bigger in their capacity to store information. And, this additional capacity drove a fundamental change in the way disk drives were used.
>
> **A.1.2. Partitions: Turning One Drive Into Many**
>
> As disk drive capacities soared, some people began to wonder if having all of that formatted space in one big chunk was such a great idea. This line of thinking was driven by several issues, some philosophical, some technical. On the philosophical side, above a certain size, it seemed that the additional space provided by a larger drive created more clutter. On the technical side, some file systems were never designed to support anything above a certain capacity. Or the file systems could support larger drives with a greater capacity, but the overhead imposed by the file system to track files became excessive.
>
> The solution to this problem was to divide disks into partitions. Each partition can be accessed as if it was a separate disk. This is done through the addition of a partition table.
>
> ![disk with part table RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/disk_with_part_table.png)
>
> As Figure A.5, “Disk Drive with Partition Table” shows, the partition table is divided into four sections or four primary partitions. A primary partition is a partition on a hard drive that can contain only one logical drive (or section). Each section can hold the information necessary to define a single partition, meaning that the partition table can define no more than four partitions. Each partition table entry contains several important characteristics of the partition:
>
> 1.  The points on the disk where the partition starts and ends
> 2.  Whether the partition is "active"
> 3.  The partition's type Let us take a closer look at each of these characteristics. The starting and ending points actually define the partition's size and location on the disk. The "active" flag is used by some operating systems' boot loaders. In other words, the operating system in the partition that is marked "active" is booted.
>
> The partition's type can be a bit confusing. The type is a number that identifies the partition's anticipated usage. If that statement sounds a bit vague, that is because the meaning of the partition type is a bit vague. Some operating systems use the partition type to denote a specific file system type, to flag the partition as being associated with a particular operating system, to indicate that the partition contains a bootable operating system, or some combination of the three.
>
> By this point, you might be wondering how all this additional complexity is normally used. Refer to Figure A.6, “Disk Drive With Single Partition”, for an example.
>
> ![disk drive with one part RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/disk_drive_with_one_part.png)
>
> In many cases, there is only a single partition spanning the entire disk, essentially duplicating the method used before partitions. The partition table has only one entry used, and it points to the start of the partition.
>
> Table A.1, “Partition Types”, contains a listing of some popular (and obscure) partition types, along with their hexadecimal numeric values.
>
> ![part types RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/part_types.png)
>
> **A.1.3. Partitions within Partitions — An Overview of Extended Partitions** Of course, over time it became obvious that four partitions would not be enough. As disk drives continued to grow, it became more and more likely that a person could configure four reasonably-sized partitions and still have disk space left over. There needed to be some way of creating more partitions.
>
> Enter the extended partition. As you may have noticed in Table A.1, “Partition Types”, there is an "Extended" partition type. It is this partition type that is at the heart of extended partitions.
>
> When a partition is created and its type is set to "Extended," an extended partition table is created. In essence, the extended partition is like a disk drive in its own right — it has a partition table that points to one or more partitions (now called logical partitions, as opposed to the four primary partitions) contained entirely within the extended partition itself. Figure A.7, “Disk Drive With Extended Partition”, shows a disk drive with one primary partition and one extended partition containing two logical partitions (along with some unpartitioned free space).
>
> ![extended parts RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/extended_parts.png)
>
> As this figure implies, there is a difference between primary and logical partitions — there can only be four primary partitions, but there is no fixed limit to the number of logical partitions that can exist. However, due to the way in which partitions are accessed in Linux, you should avoid defining more than 12 logical partitions on a single disk drive.

### Partitioning with Fdisk

Now to partitioning with **fdisk**. From this old "[Partitioning with fdisk](http://www.tldp.org/HOWTO/Partition/fdisk_partitioning.html)" guide:

> **5. Partitioning with fdisk** This section shows you how to actually partition your hard drive with the fdisk utility. Linux allows only 4 primary partitions. You can have a much larger number of logical partitions by sub-dividing one of the primary partitions. Only one of the primary partitions can be sub-divided.
>
> Examples:
>
> *   Four primary partitions
> *   Mixed primary and logical partitions
>
> **5.1. fdisk usage**
>
> **fdisk** is started by typing (as root) **fdisk device** at the command prompt. device might be something like **/dev/hda** or **/dev/sda**. The basic **fdisk** commands you need are:
>
> *   **p** print the partition table
> *   **n** create a new partition
> *   **d** delete a partition
> *   **q** quit without saving changes
> *   **w** write the new partition table and exit
>
> Changes you make to the partition table do not take effect until you issue the write (**w**) command. Here is a sample partition table:

Here is how my partition table looked like on 1st SCSI disk:

    [root@rhel01 ~]# fdisk -l /dev/sda

    Disk /dev/sda: 21.5 GB, 21474836480 bytes
    255 heads, 63 sectors/track, 2610 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x00086e02

    Device Boot Start End Blocks Id System
    /dev/sda1 * 1 64 512000 83 Linux
    /dev/sda2 64 2611 20458496 8e Linux LVM


And back to guide:

> The first line shows the geometry of your hard drive. It may not be physically accurate, but you can accept it as though it were. The hard drive in this example is made of 32 double-sided platters with one head on each side (probably not true). Each platter has 2610 concentric tracks. A 3-dimensional track (the same track on all disks) is called a cylinder. Each track is divided into 63 sectors. Each sector contains 512 bytes of data. Therefore the block size in the partition table is 64 heads * 63 sectors * 512 bytes er...divided by 1024. The start and end values are cylinders.

Then the guide has an example of how to create 4 primary partitions with **fdisk**.

### Partitioning with Fdisk Example

So here is my second SCSI disk:

    [root@rhel01 ~]# fdisk -l /dev/sdb

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System


There are currently no partitions on it and it's size is 8GB. So let's create 3 partitions of size 2GB and mark them as ext3 and 1 partition of size 2GB and mark it as a swap partition. The creation of the first one looks like this:

    [root@rhel01 ~]# fdisk /dev/sdb

    WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
    switch off the mode (command 'c') and change display units to
    sectors (command 'u').

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System

    Command (m for help): n
    Command action
    e extended
    p primary partition (1-4)
    p
    Partition number (1-4): 1
    First cylinder (1-1044, default 1):
    Using default value 1
    Last cylinder, +cylinders or +size{K,M,G} (1-1044, default 1044): +2G


Now if we keep going and add another one, it will look like this:

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux

    Command (m for help): n
    Command action
    e extended
    p primary partition (1-4)
    p
    Partition number (1-4): 2
    First cylinder (263-1044, default 263):
    Using default value 263
    Last cylinder, +cylinders or +size{K,M,G} (263-1044, default 1044): +2G


And here is how the third one looks like:

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux

    Command (m for help): n
    Command action
    e extended
    p primary partition (1-4)
    p
    Partition number (1-4): 3
    First cylinder (525-1044, default 525):
    Using default value 525
    Last cylinder, +cylinders or +size{K,M,G} (525-1044, default 1044): +2G


and lastly here is partition 4:

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux
    /dev/sdb3 525 786 2104515 83 Linux

    Command (m for help): n
    Command action
    e extended
    p primary partition (1-4)
    p
    Selected partition 4
    First cylinder (787-1044, default 787):
    Using default value 787
    Last cylinder, +cylinders or +size{K,M,G} (787-1044, default 1044):
    Using default value 1044


Notice for the last one I just selected the default so it takes all the available space. Here is how the final partition table looks like:

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux
    /dev/sdb3 525 786 2104515 83 Linux
    /dev/sdb4 787 1044 2072385 83 Linux


The '**Id**' for all the partitions is '**83**'. To see the list of all the **Ids** we can do this:

    Command (m for help): t
    Partition number (1-4): 4
    Hex code (type L to list codes): L

    Hex code (type L to list codes): L

     0  Empty           24  NEC DOS         81  Minix / old Lin bf  Solaris
     1  FAT12           39  Plan 9          82  Linux swap / So c1  DRDOS/sec (FAT-
     2  XENIX root      3c  PartitionMagic  83  Linux           c4  DRDOS/sec (FAT-
     3  XENIX usr       40  Venix 80286     84  OS/2 hidden C:  c6  DRDOS/sec (FAT-
     4  FAT16 <32M      41  PPC PReP Boot   85  Linux extended  c7  Syrinx
     5  Extended        42  SFS             86  NTFS volume set da  Non-FS data
     6  FAT16           4d  QNX4.x          87  NTFS volume set db  CP/M / CTOS / .
     7  HPFS/NTFS       4e  QNX4.x 2nd part 88  Linux plaintext de  Dell Utility
     8  AIX             4f  QNX4.x 3rd part 8e  Linux LVM       df  BootIt
     9  AIX bootable    50  OnTrack DM      93  Amoeba          e1  DOS access
     a  OS/2 Boot Manag 51  OnTrack DM6 Aux 94  Amoeba BBT      e3  DOS R/O
     b  W95 FAT32       52  CP/M            9f  BSD/OS          e4  SpeedStor
     c  W95 FAT32 (LBA) 53  OnTrack DM6 Aux a0  IBM Thinkpad hi eb  BeOS fs
     e  W95 FAT16 (LBA) 54  OnTrackDM6      a5  FreeBSD         ee  GPT
     f  W95 Ext'd (LBA) 55  EZ-Drive        a6  OpenBSD         ef  EFI (FAT-12/16/
    10  OPUS            56  Golden Bow      a7  NeXTSTEP        f0  Linux/PA-RISC b
    11  Hidden FAT12    5c  Priam Edisk     a8  Darwin UFS      f1  SpeedStor
    12  Compaq diagnost 61  SpeedStor       a9  NetBSD          f4  SpeedStor
    14  Hidden FAT16 <3 63  GNU HURD or Sys ab  Darwin boot     f2  DOS secondary
    16  Hidden FAT16    64  Novell Netware  af  HFS / HFS+      fb  VMware VMFS
    17  Hidden HPFS/NTF 65  Novell Netware  b7  BSDI fs         fc  VMware VMKCORE
    18  AST SmartSleep  70  DiskSecure Mult b8  BSDI swap       fd  Linux raid auto
    1b  Hidden W95 FAT3 75  PC/IX           bb  Boot Wizard hid fe  LANstep
    1c  Hidden W95 FAT3 80  Old Minix       be  Solaris boot    ff  BBT
    1e  Hidden W95 FAT1


So we can see that '**83**' is Linux which is usually **EXT3**. Now for **swap** the id is **82**. So let's change that for the 4th partition:

    Hex code (type L to list codes): 82
    Changed system type of partition 4 to 82 (Linux swap / Solaris)

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux
    /dev/sdb3 525 786 2104515 83 Linux
    /dev/sdb4 787 1044 2072385 82 Linux swap / Solaris


Now to write the partition we can do this:

    Command (m for help): w
    The partition table has been altered!

    Calling ioctl() to re-read partition table.
    Syncing disks.


Now checking the partition table we see this:

    [root@rhel01 ~]# fdisk -l /dev/sdb

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux
    /dev/sdb3 525 786 2104515 83 Linux
    /dev/sdb4 787 1044 2072385 82 Linux swap / Solaris


If the table didn't show up properly, we could run **partprobe** to re-check the partition table of disk:

    [root@rhel01 ~]# partprobe --help
    Usage: partprobe [OPTION] [DEVICE]...
    Inform the operating system about partition table changes.

    -d, --dry-run do not actually inform the operating system
    -s, --summary print a summary of contents
    -h, --help display this help and exit
    -v, --version output version information and exit

    When no DEVICE is given, probe all partitions.


Here is how the output looks like:

    [root@rhel01 ~]# partprobe -s /dev/sdb
    /dev/sdb: msdos partitions 1 2 3 4


We had 4 partitions so that looks good. To delete a partition with **fdisk**, we can do this:

    [root@rhel01 ~]# fdisk /dev/sdb

    WARNING: DOS-compatible mode is deprecated. It's strongly recommended to
    switch off the mode (command 'c') and change display units to
    sectors (command 'u').

    Command (m for help): p

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux
    /dev/sdb3 525 786 2104515 83 Linux
    /dev/sdb4 787 1044 2072385 82 Linux swap / Solaris

    Command (m for help): d
    Partition number (1-4): 3

    Command (m for help): w
    The partition table has been altered!

    Calling ioctl() to re-read partition table.
    Syncing disks.


So I deleted the 3rd partition. So let's see how **fdisk** looks like now:

    [root@rhel01 ~]# fdisk -l /dev/sdb

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 262 2104483+ 83 Linux
    /dev/sdb2 263 524 2104515 83 Linux
    /dev/sdb4 787 1044 2072385 82 Linux swap / Solaris


Notice there is a gap between **End** of the 2nd partition and the **Start** of the 4th partition.

Now let's do similar functions with **parted**.

### Partitioning with *parted*

From "[Red Hat Enterprise Linux 6 Storage Administration Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Storage_Administration_Guide/Red_Hat_Enterprise_Linux-6-Storage_Administration_Guide-en-US.pdf)"

> **Chapter 5. Partitions**
>
> The utility **parted** allows users to:
>
> 1.  View the existing partition table
> 2.  Change the size of existing partitions
> 3.  Add partitions from free space or additional hard drives
>
> By default, the **parted** package is included when installing Red Hat Enterprise Linux. To start **parted**, log in as root and type the command **parted /dev/sda** at a shell prompt (where **/dev/sda** is the device name for the drive you want to configure).
>
> If you want to remove or resize a partition, the device on which that partition resides must not be in use. Creating a new partition on a device which is in use—while possible—is not recommended.
>
> For a device to not be in use, none of the partitions on the device can be mounted, and any swap space on the device must not be enabled.
>
> As well, the partition table should not be modified while it is in use because the kernel may not properly recognize the changes. If the partition table does not match the actual state of the mounted partitions, information could be written to the wrong partition, resulting in lost and overwritten data.
>
> The easiest way to achieve this it to boot your system in rescue mode. When prompted to mount the file system, select **Skip**.
>
> Alternately, if the drive does not contain any partitions in use (system processes that use or lock the file system from being unmounted), you can unmount them with the **umount** command and turn off all the swap space on the hard drive with the **swapoff** command.
>
> ![parted commands RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/parted_commands.png)
>
> **5.1. Viewing the Partition Table**
>
> After starting **parted**, use the command print to view the partition table. A table similar to the following appears:
>
> **Example 5.1. Partition table**
>
>     Model: ATA ST3160812AS (scsi)
>     Disk /dev/sda: 160GB
>     Sector size (logical/physical): 512B/512B
>     Partition Table: msdos
>     Number Start End Size Type File system Flags
>     1 32.3kB 107MB 107MB primary ext3 boot
>     2 107MB 105GB 105GB primary ext3
>     3 105GB 107GB 2147MB primary linux-swap
>     4 107GB 160GB 52.9GB extended root
>     5 107GB 133GB 26.2GB logical ext3
>     6 133GB 133GB 107MB logical ext3
>     7 133GB 160GB 26.6GB logical lvm
>
>
> The first line contains the disk type, manufacturer, model number and interface, and the second line displays the disk label type. The remaining output below the fourth line shows the partition table.
>
> In the partition table, the Minor number is the partition **number**. For example, the partition with minor number 1 corresponds to **/dev/sda1**. The **Start** and **End** values are in megabytes. Valid **Type** are metadata, free, primary, extended, or logical. The **Filesystem** is the file system type, which can be any of the following:
>
> *   ext2
> *   ext3
> *   fat16
> *   fat32
> *   hfs
> *   jfs
> *   linux-swap
> *   ntfs
> *   reiserfs
> *   hp-ufs
> *   sun-ufs
> *   xfs
>
> If a **Filesystem** of a device shows no value, this means that its file system type is unknown. The **Flags** column lists the flags set for the partition. Available flags are **boot**, **root**, **swap**, **hidden**, **raid**, **lvm**, or **lba**.

Now let's actually create some partitions:

> **5.2. Creating a Partition**
>
> **Procedure 5.1. Creating a partition**
>
> 1.  Before creating a partition, boot into rescue mode (or unmount any partitions on the device and turn off any swap space on the device).
> 2.  Start parted, where /dev/sda is the device on which to create the partition: `# parted /dev/sda`
> 3.  View the current partition table to determine if there is enough free space: `# print`
>
> If there is not enough free space, you can resize an existing partition
>
> **5.2.1. Making the Partition**
>
> From the partition table, determine the start and end points of the new partition and what partition type it should be. You can only have four primary partitions (with no extended partition) on a device. If you need more than four partitions, you can have three primary partitions, one extended partition, and multiple logical partitions within the extended.
>
> For example, to create a primary partition with an ext3 file system from 1024 megabytes until 2048 megabytes on a hard drive type the following command:
>
>     # mkpart primary ext3 1024 2048
>
>
> The changes start taking place as soon as you press **Enter**, so review the command before executing to it. After creating the partition, use the **print** command to confirm that it is in the partition table with the correct partition type, file system type, and size. Also remember the minor number of the new partition so that you can label any file systems on it. You should also view the output of **cat /proc/partitions** after parted is closed to make sure the kernel recognizes the new partition.

### Partitioning with *parted* Example

So let's use **parted** to remove the rest of partitions on **/dev/sdb** and then create 3 partitions of equal size, 2 of which are **ext** and 1 is **swap**. First to list the partitions:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags
    1 32.3kB 2155MB 2155MB primary
    2 2155MB 4310MB 2155MB primary
    4 6465MB 8587MB 2122MB primary


Now to remove the partitions:

    [root@rhel01 ~]# parted /dev/sdb
    GNU Parted 2.1
    Using /dev/sdb
    Welcome to GNU Parted! Type 'help' to view a list of commands.
    (parted) print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags
    1 32.3kB 2155MB 2155MB primary
    2 2155MB 4310MB 2155MB primary
    4 6465MB 8587MB 2122MB primary

    (parted) rm 1
    (parted) rm 2
    (parted) rm 4
    (parted) print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags


Now let's create the first one, taking 33% of the space:

    (parted) help mkpart
      mkpart PART-TYPE [FS-TYPE] START END     make a partition

        PART-TYPE is one of: primary, logical, extended
            FS-TYPE is one of: ext4, ext3, ext2, fat32, fat16, hfsx, hfs+, hfs, jfs,
            swsusp, linux-swap(v1), linux-swap(v0), ntfs, reiserfs, hp-ufs, sun-ufs,
            xfs, apfs2, apfs1, asfs, amufs5, amufs4, amufs3, amufs2, amufs1, amufs0,
            amufs, affs7, affs6, affs5, affs4, affs3, affs2, affs1, affs0,
            linux-swap, linux-swap(new), linux-swap(old)
            START and END are disk locations, such as 4GB or 10%.  Negative values
            count from the end of the disk.  For example, -1s specifies exactly the
            last sector.

            'mkpart' makes a partition without creating a new file system on the
            partition.  FS-TYPE may be specified to set an appropriate partition
            ID.
    (parted) mkpart primary ext3 1 33%
    (parted) print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags
    1 1049kB 2834MB 2833MB primary


Now for the second one:

    (parted) mkpart primary ext3 2835MB 66%
    (parted) print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags
    1 1049kB 2834MB 2833MB primary
    2 2835MB 5670MB 2834MB primary


Now the last one:

    (parted) mkpart primary linux-swap 67% -1s
    (parted) print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags
    1 1049kB 2834MB 2833MB primary
    2 2835MB 5670MB 2834MB primary
    3 5756MB 8590MB 2834MB primary


As soon as your quit the parted utility it writes the new partition table:

    (parted) quit
    Information: You may need to update /etc/fstab.


Now to check the partition table:

    [root@rhel01 ~]# fdisk -l /dev/sdb

    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96

    Device Boot Start End Blocks Id System
    /dev/sdb1 1 345 2766848 83 Linux
    Partition 1 does not end on cylinder boundary.
    /dev/sdb2 345 690 2767872 83 Linux
    Partition 2 does not end on cylinder boundary.
    /dev/sdb3 700 1045 2767872 82 Linux swap / Solaris


### Logical Volume Manager (LVM)

Now onto LVMs, from "[Red Hat Enterprise Linux 6 Logical Volume Manager Administration](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Logical_Volume_Manager_Administration/Red_Hat_Enterprise_Linux-6-Logical_Volume_Manager_Administration-en-US.pdf)":

> The underlying physical storage unit of an LVM logical volume is a block device such as a partition or whole disk. This device is initialized as an LVM physical volume (PV).
>
> To create an LVM logical volume, the physical volumes are combined into a volume group (VG). This creates a pool of disk space out of which LVM logical volumes (LVs) can be allocated. This process is analogous to the way in which disks are divided into partitions. A logical volume is used by file systems and applications (such as databases).
>
> Figure 1.1, “LVM Logical Volume Components” shows the components of a simple LVM logical volume:
>
> ![lvm components RHCSA and RHCE Chapter 3 Disks and Partitioning](https://github.com/elatov/uploads/raw/master/2012/12/lvm_components.png)

And here more information regarding each layer:

#### LVM Physical Volumes

> **2.1. Physical Volumes**
>
> The underlying physical storage unit of an LVM logical volume is a block device such as a partition or whole disk. To use the device for an LVM logical volume the device must be initialized as a physical volume (PV). Initializing a block device as a physical volume places a label near the start of the device.
>
> By default, the LVM label is placed in the second 512-byte sector. You can overwrite this default by placing the label on any of the first 4 sectors. This allows LVM volumes to co-exist with other users of these sectors, if necessary.
>
> An LVM label provides correct identification and device ordering for a physical device, since devices can come up in any order when the system is booted. An LVM label remains persistent across reboots and throughout a cluster.
>
> The LVM label identifies the device as an LVM physical volume. It contains a random unique identifier (the UUID) for the physical volume. It also stores the size of the block device in bytes, and it records where the LVM metadata will be stored on the device.
>
> The LVM metadata contains the configuration details of the LVM volume groups on your system. By default, an identical copy of the metadata is maintained in every metadata area in every physical volume within the volume group. LVM metadata is small and stored as ASCII.
>
> Currently LVM allows you to store 0, 1 or 2 identical copies of its metadata on each physical volume. The default is 1 copy. Once you configure the number of metadata copies on the physical volume, you cannot change that number at a later time. The first copy is stored at the start of the device, shortly after the label. If there is a second copy, it is placed at the end of the device. If you accidentally overwrite the area at the beginning of your disk by writing to a different disk than you intend, a second copy of the metadata at the end of the device will allow you to recover the metadata.

#### LVM Logical Volumes

> **2.2. Volume Groups**
>
> Physical volumes are combined into volume groups (VGs). This creates a pool of disk space out of which logical volumes can be allocated.
>
> Within a volume group, the disk space available for allocation is divided into units of a fixed-size called extents. An extent is the smallest unit of space that can be allocated. Within a physical volume, extents are referred to as physical extents. A logical volume is allocated into logical extents of the same size as the physical extents.
>
> The extent size is thus the same for all logical volumes in the volume group. The volume group maps the logical extents to physical extents.

#### LVM Logical Volumes

> **2.3. LVM Logical Volumes**
>
> In LVM, a volume group is divided up into logical volumes. There are three types of LVM logical volumes: linear volumes, striped volumes, and mirrored volumes.

### LVM Administration

Here are the command utilities used to manage LVMs:

> **4.2. Physical Volume Administration**
>
> This section describes the commands that perform the various aspects of physical volume administration.
>
> **4.2.1. Creating Physical Volumes**
>
> The following subsections describe the commands used for creating physical volumes.
>
> **4.2.1.2. Initializing Physical Volumes**
>
> Use the **pvcreate** command to initialize a block device to be used as a physical volume. Initialization is analogous to formatting a file system. The following command initializes **/dev/sdd**, **/dev/sde**, and **/dev/sdf** as LVM physical volumes for later use as part of LVM logical volumes.
>
>     # pvcreate /dev/sdd /dev/sde /dev/sdf
>
>
> To initialize partitions rather than whole disks: run the **pvcreate** command on the partition. The following example initializes the partition **/dev/hdb1** as an LVM physical volume for later use as part of an LVM logical volume.
>
>     # pvcreate /dev/hdb1
>
>
> **4.2.1.3. Scanning for Block Devices** You can scan for block devices that may be used as physical volumes with the **lvmdiskscan** command.
>
> **4.2.2. Displaying Physical Volumes**
>
> There are three commands you can use to display properties of LVM physical volumes: **pvs**, **pvdisplay**, and **pvscan**.
>
> The **pvdisplay** command provides a verbose multi-line output for each physical volume. It displays physical properties (size, extents, volume group, etc.) in a fixed format.
>
> The **pvscan** command scans all supported LVM block devices in the system for physical volumes.
>
> **4.2.5. Removing Physical Volumes**
>
> If a device is no longer required for use by LVM, you can remove the LVM label with the **pvremove** command. Executing the **pvremove** command zeroes the LVM metadata on an empty physical volume.
>
> If the physical volume you want to remove is currently part of a volume group, you must remove it from the volume group with the **vgreduce** command.

    # pvremove /dev/ram15
    Labels on physical volume "/dev/ram15" successfully wiped


Now onto Volume Groups:

> **4.3.1. Creating Volume Groups**
>
> To create a volume group from one or more physical volumes, use the **vgcreate** command. The **vgcreate** command creates a new volume group by name and adds at least one physical volume to it.
>
> The following command creates a volume group named **vg1** that contains physical volumes **/dev/sdd1** and **/dev/sde1**.
>
>     # vgcreate vg1 /dev/sdd1 /dev/sde1
>
>
> When physical volumes are used to create a volume group, its disk space is divided into 4MB extents, by default. This extent is the minimum amount by which the logical volume may be increased or decreased in size. Large numbers of extents will have no impact on I/O performance of the logical volume.
>
> You can specify the extent size with the **-s** option to the **vgcreate** command if the default extent size is not suitable. You can put limits on the number of physical or logical volumes the volume group can have by using the **-p** and **-l** arguments of the **vgcreate** command.
>
> LVM volume groups and underlying logical volumes are included in the device special file directory tree in the **/dev** directory with the following layout:
>
>     /dev/vg/lv/
>
>
> For example, if you create two volume groups myvg1 and myvg2, each with three logical volumes named lvo1, lvo2, and lvo3, this create six device special files:
>
>     /dev/myvg1/lv01
>     /dev/myvg1/lv02
>     /dev/myvg1/lv03
>     /dev/myvg2/lv01
>     /dev/myvg2/lv02
>     /dev/myvg2/lv03
>
>
> **4.3.3. Adding Physical Volumes to a Volume Group**
>
> To add additional physical volumes to an existing volume group, use the **vgextend** command. The **vgextend** command increases a volume group's capacity by adding one or more free physical volumes.
>
> The following command adds the physical volume /dev/sdf1 to the volume group vg1.
>
>     # vgextend vg1 /dev/sdf1
>
>
> **4.3.4 . Displaying Volume Groups**
>
> There are two commands you can use to display properties of LVM volume groups: **vgs** and **vgdisplay**
>
> The **vgscan** command, which scans all the disks for volume groups and rebuilds the LVM cache file, also displays the volume groups. The **vgs** command provides volume group information in a configurable form, displaying one line per volume group.
>
> The **vgs** command provides a great deal of format control, and is useful for scripting.
>
> The **vgdisplay** command displays volume group properties (such as size, extents, number of physical volumes, etc.) in a fixed form.
>
> **4.3.6. Removing Physical Volumes from a Volume Group**
>
> To remove unused physical volumes from a volume group, use the **vgreduce** command. The **vgreduce** command shrinks a volume group's capacity by removing one or more empty physical volumes. This frees those physical volumes to be used in different volume groups or to be removed from the system.
>
> The following command removes the physical volume **/dev/hda1** from the volume group **my_volume_group**.
>
>      # vgreduce my_volume_group /dev/hda1
>
>
> **4.3.9. Removing Volume Groups**
>
> To remove a volume group that contains no logical volumes, use the **vgremove** command.
>
>     # vgremove officevg
>     Volume group "officevg" successfully removed
>

Lastly onto the Logical Volumes:

> **4.4.1. Creating Linear Logical Volumes**
>
> To create a logical volume, use the **lvcreate** command. If you do not specify a name for the logical volume, the default name **lvol#** is used where # is the internal number of the logical volume.
>
> When you create a logical volume, the logical volume is carved from a volume group using the free extents on the physical volumes that make up the volume group. Normally logical volumes use up any space available on the underlying physical volumes on a next-free basis. Modifying the logical volume frees and reallocates space in the physical volumes.
>
> The following command creates a logical volume 10 gigabytes in size in the volume group **vg1**.
>
>     # lvcreate -L 10G vg1
>
>
> The following command creates a 1500 MB linear logical volume named **testlv** in the volume group **testvg**, creating the block device **/dev/testvg/testlv**.
>
>     # lvcreate -L1500 -n testlv testvg
>
>
> You can use the **-l** argument of the **lvcreate** command to specify the size of the logical volume in extents. You can also use this argument to specify the percentage of the volume group to use for the logical volume. The following command creates a logical volume called **mylv** that uses 60% of the total space in volume group **testvol**.
>
>     # lvcreate -l 60%VG -n mylv testvg
>
>
> You can also use the **-l** argument of the **lvcreate** command to specify the percentage of the remaining free space in a volume group as the size of the logical volume. The following command creates a logical volume called **yourlv** that uses all of the unallocated space in the volume group **testvol**.
>
>     # lvcreate -l 100%FREE -n yourlv testvg
>
>
> You can use **-l** argument of the **lvcreate** command to create a logical volume that uses the entire volume group. Another way to create a logical volume that uses the entire volume group is to use the **vgdisplay** command to find the "Total PE" size and to use those results as input to the **lvcreate** command.
>
> The following commands create a logical volume called **mylv** that fills the volume group named **testvg**.
>
>     # vgdisplay testvg | grep "Total PE"
>     Total PE 10230
>     # lvcreate -l 10230 testvg -n mylv
>
>
> The underlying physical volumes used to create a logical volume can be important if the physical volume needs to be removed, so you may need to consider this possibility when you create the logical volume.
>
> To create a logical volume to be allocated from a specific physical volume in the volume group, specify the physical volume or volumes at the end at the **lvcreate** command line. The following command creates a logical volume named **testlv** in volume group **testvg** allocated from the physical volume **/dev/sdg1**,
>
>     # lvcreate -L 1500 -ntestlv testvg /dev/sdg1
>
>
> **4.4.7. Resizing Logical Volumes**
>
> To reduce the size of a logical volume, use the **lvreduce** command. If the logical volume contains a file system, be sure to reduce the file system first (or use the LVM GUI) so that the logical volume is always at least as large as the file system expects it to be.
>
> The following command reduces the size of logical volume **lvol1** in volume group **vg00** by 3 logical extents.
>
>     # lvreduce -l -3 vg00/lvol1
>
>
> **4.4.10. Removing Logical Volumes**
>
> To remove an inactive logical volume, use the **lvremove** command. If the logical volume is currently mounted, unmount the volume before removing it. In addition, in a clustered environment you must deactivate a logical volume before it can be removed.
>
> The following command removes the logical volume **/dev/testvg/testlv** from the volume group **testvg**. Note that in this case the logical volume has not been deactivated.
>
>     # lvremove /dev/testvg/testlv
>     Do you really want to remove active logical volume "testlv"? [y/n]: y
>     Logical volume "testlv" successfully removed
>
>
> You could explicitly deactivate the logical volume before removing it with the **lvchange -an** command, in which case you would not see the prompt verifying whether you want to remove an active logical volume.
>
> **4.4.11. Displaying Logical Volumes** There are three commands you can use to display properties of LVM logical volumes: **lvs**, **lvdisplay**, and **lvscan**.
>
> The **lvs** command provides logical volume information in a configurable form, displaying one line per logical volume. The **lvs** command provides a great deal of format control, and is useful for scripting.
>
> The **lvdisplay** command displays logical volume properties (such as size, layout, and mapping) in a fixed format.
>
> The **lvscan** command scans for all logical volumes in the system and lists them.
>
> **4.4.12. Growing Logical Volumes**
>
> To increase the size of a logical volume, use the **lvextend** command.
>
> When you extend the logical volume, you can indicate how much you want to extend the volume, or how large you want it to be after you extend it.
>
> The following command extends the logical volume **/dev/myvg/homevol** to 12 gigabytes.
>
>     # lvextend -L12G /dev/myvg/homevol
>     lvextend -- extending logical volume "/dev/myvg/homevol" to 12 GB
>     lvextend -- doing automatic backup of volume group "myvg"
>     lvextend -- logical volume "/dev/myvg/homevol" successfully extended
>
>
> The following command adds another gigabyte to the logical volume **/dev/myvg/homevol**.
>
>     # lvextend -L+1G /dev/myvg/homevol
>     lvextend -- extending logical volume "/dev/myvg/homevol" to 13 GB
>     lvextend -- doing automatic backup of volume group "myvg"
>     lvextend -- logical volume "/dev/myvg/homevol" successfully extended
>
>
> As with the **lvcreate** command, you can use the -l argument of the **lvextend** command to specify the number of extents by which to increase the size of the logical volume. You can also use this argument to specify a percentage of the volume group, or a percentage of the remaining free space in the volume group. The following command extends the logical volume called **testlv** to fill all of the unallocated space in the volume group **myvg**.
>
>     # lvextend -l +100%FREE /dev/myvg/testlv
>     Extending logical volume testlv to 68.59 GB
>     Logical volume testlv successfully resized
>
>
> After you have extended the logical volume it is necessary to increase the file system size to match

### LVM Example

I don't want to add my other disks, do let's partition my one drive (**sdb**) into 3 different partitions and first add the first 2 as Physical Volumes. Then let's create a Volume Group and add both of the Physical Volumes to it. Then let's create a Logical Volume from our Logical Group. Lastly let's extend the Volume Group with the 3rd partition and then extend the Logical Volume as well. Here is how my partitioning looked like for **sdb**:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos

    Number Start End Size Type File system Flags
    1 1049kB 2834MB 2833MB primary
    2 2920MB 5670MB 2749MB primary
    3 5756MB 8590MB 2834MB primary


Now let's add the first two into the LVM (Logical Volume Manager):

    [root@rhel01 ~]# pvcreate /dev/sdb1 /dev/sdb2
    Writing physical volume data to disk "/dev/sdb1"
    Physical volume "/dev/sdb1" successfully created
    Writing physical volume data to disk "/dev/sdb2"
    Physical volume "/dev/sdb2" successfully created
    [root@rhel01 ~]# pvs
    PV VG Fmt Attr PSize PFree
    /dev/sda2 VolGroup lvm2 a-- 19.51g 0
    /dev/sdb1 lvm2 a-- 2.64g 2.64g
    /dev/sdb2 lvm2 a-- 2.56g 2.56g


The top partition (/dev/sda2) was setup by the system install, so let's not mess with that. Now let's add both into a Volume Group and call the volume group **kvg**:

>     [root@rhel01 ~]# vgcreate kvg /dev/sdb1 /dev/sdb2
>     Volume group "kvg" successfully created
>     [root@rhel01 ~]# vgs
>     VG #PV #LV #SN Attr VSize VFree
>     VolGroup 1 2 0 wz--n- 19.51g 0
>     kvg 2 0 0 wz--n- 5.20g 5.20g
>

Now let's create a Logical Volume called **kvol** and make it 60% of the total size:

    [root@rhel01 ~]# lvcreate -l 60%VG -n kvol kvg
    Logical volume "kvol" created
    [root@rhel01 ~]# lvs
    LV VG Attr LSize Pool Origin Data% Move Log Copy% Convert
    lv_root VolGroup -wi-ao-- 18.51g
    lv_swap VolGroup -wi-ao-- 1.00g
    kvol kvg -wi-a--- 3.12g


Now let's add the third partition into the LVM:

    [root@rhel01 ~]# pvcreate /dev/sdb3
    Writing physical volume data to disk "/dev/sdb3"
    Physical volume "/dev/sdb3" successfully created


Now let's extend Volume Group **kvg** with the 3rd partition:

    [root@rhel01 ~]# vgextend kvg /dev/sdb3
    Volume group "kvg" successfully extended
    [root@rhel01 ~]# vgs
    VG #PV #LV #SN Attr VSize VFree
    VolGroup 1 2 0 wz--n- 19.51g 0
    kvg 3 1 0 wz--n- 7.83g 4.71g


Now let's extend our Logical Volume to use all the available space:

    [root@rhel01 ~]# lvextend -l +100%FREE /dev/kvg/kvol
    Extending logical volume kvol to 7.83 GiB
    Logical volume kvol successfully resized
    [root@rhel01 ~]# lvs
    LV VG Attr LSize Pool Origin Data% Move Log Copy% Convert
    lv_root VolGroup -wi-ao-- 18.51g
    lv_swap VolGroup -wi-ao-- 1.00g
    kvol kvg -wi-a--- 7.83g


Checking out the device, I see the following:

    [root@rhel01 ~]# fdisk -l /dev/kvg/kvol

    Disk /dev/kvg/kvol: 8409 MB, 8409579520 bytes
    255 heads, 63 sectors/track, 1022 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x00000000


So it looks like it's taking up all the space. Of course this was a round about way of doing it. First partition the drive then create a volume group that spans all the partitions, but it made a good working example to show how LVM works.

### RAID

Now let's move to **mdadm**. From "[Red Hat Enterprise Linux 6 Storage Administration Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Storage_Administration_Guide/Red_Hat_Enterprise_Linux-6-Storage_Administration_Guide-en-US.pdf)":

> **Chapter 16. Redundant Array of Independent Disks (RAID)**
>
> The basic idea behind RAID is to combine multiple small, inexpensive disk drives into an array to accomplish performance or redundancy goals not attainable with one large and expensive drive. This array of drives appears to the computer as a single logical storage unit or drive.
>
> **16.1. What is RAID?** RAID allows information to be spread across several disks. RAID uses techniques such as disk striping (RAID Level 0), disk mirroring (RAID Level 1), and disk striping with parity (RAID Level 5) to achieve redundancy, lower latency, increased bandwidth, and maximized ability to recover from hard disk crashes.
>
> RAID distributes data across each drive in the array by breaking it down into consistently-sized chunks (commonly 256K or 512k, although other values are acceptable). Each chunk is then written to a hard drive in the RAID array according to the RAID level employed. When the data is read, the process is reversed, giving the illusion that the multiple drives in the array are actually one large drive.
>
> **16.2. Who Should Use RAID?**
>
> System Administrators and others who manage large amounts of data would benefit from using RAID technology. Primary reasons to deploy RAID include:
>
> 1.  Enhances speed
> 2.  Increases storage capacity using a single virtual disk
> 3.  Minimizes data loss from disk failure
>
> **16.3. RAID Types**
>
> There are three possible RAID approaches: Firmware RAID, Hardware RAID and Software RAID
>
> **Firmware RAID** Firmware RAID (also known as ATARAID) is a type of software RAID where the RAID sets can be configured using a firmware-based menu. The firmware used by this type of RAID also hooks into the BIOS, allowing you to boot from its RAID sets. Different vendors use different on-disk metadata formats to mark the RAID set members. The Intel Matrix RAID is a good example of a firmware RAID system.
>
> **Hardware RAID** The hardware-based array manages the RAID subsystem independently from the host. It presents a single disk per RAID array to the host.
>
> A Hardware RAID device may be internal or external to the system, with internal devices commonly consisting of a specialized controller card that handles the RAID tasks transparently to the operating system and with external devices commonly connecting to the system via SCSI, fiber channel, iSCSI, InfiniBand, or other high speed network interconnect and presenting logical volumes to the system.
>
> RAID controller cards function like a SCSI controller to the operating system, and handle all the actual drive communications. The user plugs the drives into the RAID controller (just like a normal SCSI controller) and then adds them to the RAID controllers configuration. The operating system will not be able to tell the difference.
>
> **Software RAID**
>
> Software RAID implements the various RAID levels in the kernel disk (block device) code. It offers the cheapest possible solution, as expensive disk controller cards or hot-swap chassis are not required. Software RAID also works with cheaper IDE disks as well as SCSI disks. With today's faster CPUs, Software RAID also generally outperforms Hardware RAID.
>
> The Linux kernel contains a multi-disk (MD) driver that allows the RAID solution to be completely hardware independent. The performance of a software-based array depends on the server CPU performance and load. Here are some of the key features of the Linux software RAID stack:
>
> *   Multi-threaded design
> *   Portability of arrays between Linux machines without reconstruction
> *   Backgrounded array reconstruction using idle system resources
> *   Hot-swappable drive support
> *   Automatic CPU detection to take advantage of certain CPU features such as streaming SIMD support
> *   Automatic correction of bad sectors on disks in an array
> *   Regular consistency checks of RAID data to ensure the health of the array
> *   Proactive monitoring of arrays with email alerts sent to a designated email address on important events
> *   Write-intent bitmaps which drastically increase the speed of resync events by allowing the kernel to know precisely which portions of a disk need to be resynced instead of having to resync the entire array
> *   Resync checkpointing so that if you reboot your computer during a resync, at startup the resync will pick up where it left off and not start all over again
> *   The ability to change parameters of the array after installation. For example, you can grow a 4-disk RAID5 array to a 5-disk RAID5 array when you have a new disk to add. This grow operation is done live and does not require you to reinstall on the new array.

### RAID Levels

> **16.4. RAID Levels and Linear Support** RAID supports various configurations, including levels 0, 1, 4, 5, 6, 10, and linear. These RAID types are defined as follows:
>
> **Level 0**
>
> RAID level 0, often called "striping," is a performance-oriented striped data mapping technique. This means the data being written to the array is broken down into strips and written across the member disks of the array, allowing high I/O performance at low inherent cost but provides no redundancy.
>
> Many RAID level 0 implementations will only stripe the data across the member devices up to the size of the smallest device in the array. This means that if you have multiple devices with slightly different sizes, each device will get treated as though it is the same size as the smallest drive. Therefore, the common storage capacity of a level 0 array is equal to the capacity of the smallest member disk in a Hardware RAID or the capacity of smallest member partition in a Software RAID multiplied by the number of disks or partitions in the array.
>
> **Level 1**
>
> RAID level 1, or "mirroring," has been used longer than any other form of RAID. Level 1 provides redundancy by writing identical data to each member disk of the array, leaving a "mirrored" copy on each disk. Mirroring remains popular due to its simplicity and high level of data availability. Level 1 operates with two or more disks, and provides very good data reliability and improves performance for read-intensive applications but at a relatively high cost.
>
> The storage capacity of the level 1 array is equal to the capacity of the smallest mirrored hard disk in a Hardware RAID or the smallest mirrored partition in a Software RAID. Level 1 redundancy is the highest possible among all RAID types, with the array being able to operate with only a single disk present.
>
> **Level 5**
>
> This is the most common type of RAID. By distributing parity across all of an array's member disk drives, RAID level 5 eliminates the write bottleneck inherent in level 4. The only performance bottleneck is the parity calculation process itself. With modern CPUs and Software RAID, that is usually not a bottleneck at all since modern CPUs can generate parity very fast. However, if you have a sufficiently large number of member devices in a software RAID5 array such that the combined aggregate data transfer speed across all devices is high enough, then this bottleneck can start to come into play.
>
> As with level 4, level 5 has asymmetrical performance, with reads substantially outperforming writes. The storage capacity of RAID level 5 is calculated the same way as with level 4.
>
> **Level 10**
>
> This RAID level attempts to combine the performance advantages of level 0 with the redundancy of level 1. It also helps to alleviate some of the space wasted in level 1 arrays with more than 2 devices. With level 10, it is possible to create a 3-drive array configured to store only 2 copies of each piece of data, which then allows the overall array size to be 1.5 times the size of the smallest devices instead of only equal to the smallest device (like it would be with a 3-device, level 1 array).
>
> The number of options available when creating level 10 arrays (as well as the complexity of selecting the right options for a specific use case) make it impractical to create during installation. It is possible to create one manually using the command line **mdadm** tool. For details on the options and their respective performance trade-offs, refer to man **md**.

### Linux Raid Subsystems

> **16.5. Linux RAID Subsystems**
>
> RAID in Linux is composed of the following subsystems:
>
> **Linux Hardware RAID controller drivers**
>
> Hardware RAID controllers have no specific RAID subsystem in Linux. Because they use special RAID chipsets, hardware RAID controllers come with their own drivers; these drivers allow the system to detect the RAID sets as regular disks.
>
> **mdraid**
>
> The **mdraid** subsystem was designed as a software RAID solution for Linux; it is also the preferred solution for software RAID under Linux. This subsystem uses its own metadata format, generally referred to as native **mdraid** metadata. **mdraid** also supports other metadata formats, known as external metadata. Red Hat Enterprise Linux 6 uses **mdraid** with external metadata to access ISW / IMSM (Intel firmware RAID) sets.
>
> **mdraid** sets are configured and controlled through the **mdadm** utility. **dmraid** Device-mapper RAID or **dmraid** refers to device-mapper kernel code that offers the mechanism to piece disks together into a RAID set. This same kernel code does not provide any RAID configuration mechanism.
>
> **dmraid** is configured entirely in user-space, making it easy to support various on-disk metadata formats. As such, **dmraid** is used on a wide variety of firmware RAID implementations. **dmraid** also supports Intel firmware RAID, although Red Hat Enterprise Linux 6 uses **mdraid** to access Intel firmware RAID sets.

### RAID Device with *mdadm*

From an older guide "[Red Hat Enterprise Linux 5 Installation Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/5/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-5-Installation_Guide-en-US.pdf)", here is an example of creating a raid configuration with **dmadm**:

> **22.3.1. Creating a RAID Device With mdadm**
>
> To create a RAID device, edit the **/etc/mdadm.conf** file to define appropriate **DEVICE** and **ARRAY** values:
>
>     DEVICE /dev/sd[abcd]1
>     ARRAY /dev/md0 devices=/dev/sda1,/dev/sdb1,/dev/sdc1,/dev/sdd1
>
>
> In this example, the **DEVICE** line is using traditional file name globbing (refer to the glob(7) man page for more information) to define the following SCSI devices:
>
> *   **/dev/sda1**
> *   **/dev/sdb1**
> *   **/dev/sdc1**
> *   **/dev/sdd1**
>
> The **ARRAY** line defines a RAID device (**/dev/md0**) that is comprised of the SCSI devices defined by the **DEVICE** line. Prior to the creation or usage of any RAID devices, the **/proc/mdstat** file shows no active RAID devices:
>
>     Personalities :
>     read_ahead not set
>     Event: 0
>     unused devices: none
>
>
> Next, use the above configuration and the **mdadm** command to create a RAID 0 array:
>
>     mdadm -C /dev/md0 --level=raid0 --raid-devices=4 /dev/sda1 /dev/sdb1 /dev/sdc1 /dev/sdd1
>     Continue creating array? yes
>     mdadm: array /dev/md0 started.
>
>
> Once created, the RAID device can be queried at any time to provide status information. The following example shows the output from the command **mdadm -detail /dev/md0**:
>
>     /dev/md0:
>     Version : 00.90.00
>     Creation Time : Mon Mar 1 13:49:10 2004
>     Raid Level : raid0
>     Array Size : 15621632 (14.90 GiB 15.100 GB)
>     Raid Devices : 4
>     Total Devices : 4
>     Preferred Minor : 0
>     Persistence : Superblock is persistent
>     Update Time : Mon Mar 1 13:49:10 2004
>     State : dirty, no-errors
>     Active Devices : 4
>     Working Devices : 4
>     Failed Devices : 0
>     Spare Devices : 0
>     Chunk Size : 64K
>     Number Major Minor RaidDevice State
>     0 8 1 0 active sync /dev/sda1
>     1 8 17 1 active sync /dev/sdb1
>     2 8 33 2 active sync /dev/sdc1
>     3 8 49 3 active sync /dev/sdd1
>     UUID : 25c0f2a1:e882dfc0:c0fe135e:6940d932
>     Events : 0.1
>

### RAID with *mdadm* Example

So let's create a raid 5 configuration with my 3 previously created partitions and then pretend to replace one since it failed. First let's go ahead and remove my partitions from the LVM setup. Here is the Logical Volume that I created:

    [root@rhel01 ~]# lvs
    LV VG Attr LSize Pool Origin Data% Move Log Copy% Convert
    lv_root VolGroup -wi-ao-- 18.51g
    lv_swap VolGroup -wi-ao-- 1.00g
    kvol kvg -wi-a--- 7.83g


Let's remove the Logical Volume:

    [root@rhel01 ~]# lvremove /dev/kvg/kvol
    Do you really want to remove active logical volume kvol? [y/n]: y
    Logical volume "kvol" successfully removed


Now here is the Volume Group that I had:

    [root@rhel01 ~]# vgs
    VG #PV #LV #SN Attr VSize VFree
    VolGroup 1 2 0 wz--n- 19.51g 0
    kvg 3 0 0 wz--n- 7.83g 7.83g


First let's remove all the Physical Volumes from this Volume Group and then remove the Volume Group. Here are the three partitions inside the Volume Group:

    [root@rhel01 ~]# pvs
    PV VG Fmt Attr PSize PFree
    /dev/sda2 VolGroup lvm2 a-- 19.51g 0
    /dev/sdb1 kvg lvm2 a-- 2.64g 2.64g
    /dev/sdb2 kvg lvm2 a-- 2.56g 2.56g
    /dev/sdb3 kvg lvm2 a-- 2.64g 2.64g


Now to remove them:

    [root@rhel01 ~]# vgreduce kvg /dev/sdb1 /dev/sdb2 /dev/sdb3
    Removed "/dev/sdb1" from volume group "kvg"
    Removed "/dev/sdb2" from volume group "kvg"
    Removed "/dev/sdb3" from volume group "kvg"


Now to remove the Volume Group:

    [root@rhel01 ~]# vgremove kvg
    Volume group "kvg" successfully removed


Now to finally remove the partitions (Physical Volumes) from LVM:

    [root@rhel01 ~]# pvremove /dev/sdb1 /dev/sdb2 /dev/sdb3
    Labels on physical volume "/dev/sdb1" successfully wiped
    Labels on physical volume "/dev/sdb2" successfully wiped
    Labels on physical volume "/dev/sdb3" successfully wiped


Now let's install the **mdadm** utility:

    [root@rhel01 ~]# yum install mdadm


Now let's create the raid configuration:

    [root@rhel01 ~]# mdadm --help-options
    Any parameter that does not start with '-' is treated as a device name
    or, for --examine-bitmap, a file name.
    The first such name is often the name of an md device. Subsequent
    names are often names of component devices.

    Some common options are:
    --help -h : General help message or, after above option, mode specific help message
    --help-options : This help message
    --version -V : Print version information for mdadm
    --verbose -v : Be more verbose about what is happening
    --quiet -q : Don't print un-necessary messages
    --brief -b : Be less verbose, more brief
    --export -Y : With --detail, use key=value format for easy import into environment
    --force -f : Override normal checks and be more forceful

    --assemble -A : Assemble an array
    --build -B : Build an array without metadata
    --create -C : Create a new array
    --detail -D : Display details of an array
    --examine -E : Examine superblock on an array component
    --examine-bitmap -X: Display the detail of a bitmap file
    --monitor -F : monitor (follow) some arrays
    --grow -G : resize/ reshape and array
    --incremental -I : add/remove a single device to/from an array as appropriate
    --query -Q : Display general information about how a device relates to the md driver
    --auto-detect : Start arrays auto-detected by the kernel


and more information:

    [root@rhel01 ~]# mdadm -C --help
    Usage: mdadm --create device -chunk=X --level=Y --raid-devices=Z devices

    This usage will initialise a new md array, associate some
    devices with it, and activate the array. In order to create an
    array with some devices missing, use the special word 'missing' in
    place of the relevant device name.

    Before devices are added, they are checked to see if they already contain
    raid superblocks or filesystems. They are also checked to see if
    the variance in device size exceeds 1%.
    If any discrepancy is found, the user will be prompted for confirmation
    before the array is created. The presence of a '--run' can override this
    caution.

    If the --size option is given then only that many kilobytes of each
    device is used, no matter how big each device is.
    If no --size is given, the apparent size of the smallest drive given
    is used for raid level 1 and greater, and the full device is used for
    other levels.

    Options that are valid with --create (-C) are:
    --bitmap= : Create a bitmap for the array with the given filename
    --chunk= -c : chunk size of kibibytes
    --rounding= : rounding factor for linear array (==chunk size)
    --level= -l : raid level: 0,1,4,5,6,linear,multipath and synonyms
    --parity= -p : raid5/6 parity algorithm: {left,right}-{,a}symmetric
    --layout= : same as --parity
    --raid-devices= -n : number of active devices in array
    --spare-devices= -x: number of spares (eXtras) devices in initial array
    --size= -z : Size (in K) of each drive in RAID1/4/5/6/10 - optional
    --force -f : Honour devices as listed on command line. Don't
    : insert a missing drive for RAID5.
    --run -R : insist of running the array even if not all
    : devices are present or some look odd.
    --readonly -o : start the array readonly - not supported yet.
    --name= -N : Textual name for array - max 32 characters
    --bitmap-chunk= : bitmap chunksize in Kilobytes.
    --delay= -d : bitmap update delay in seconds.


So let's get to it:

    [root@rhel01 ~]# mdadm -Cv /dev/md0 -l 5 -n 3 /dev/sdb1 /dev/sdb2 /dev/sdb3
    mdadm: layout defaults to left-symmetric
    mdadm: layout defaults to left-symmetric
    mdadm: chunk size defaults to 512K
    mdadm: layout defaults to left-symmetric
    mdadm: layout defaults to left-symmetric
    mdadm: size set to 2683392K
    mdadm: largest drive (/dev/sdb3) exceeds size (2683392K) by more than 1%
    Continue creating array? y
    mdadm: Defaulting to version 1.2 metadata
    mdadm: array /dev/md0 started.


Now checking the status of our raid, we see the following:

    [root@rhel01 ~]# cat /proc/mdstat
    Personalities : [raid6] [raid5] [raid4]
    md0 : active raid5 sdb3[3] sdb2[1] sdb1[0]
    5366784 blocks super 1.2 level 5, 512k chunk, algorithm 2 [3/2] [UU_]
    [====>................] recovery = 24.1% (647424/2683392) finish=0.8min speed=40464K/sec

    unused devices: <none>


We can see that the devices are getting initialized, after it's done the output will look similar to this:

    [root@rhel01 ~]# cat /proc/mdstat
    Personalities : [raid6] [raid5] [raid4]
    md0 : active raid5 sdb3[3] sdb2[1] sdb1[0]
    5366784 blocks super 1.2 level 5, 512k chunk, algorithm 2 [3/3] [UUU]

    unused devices: <none>


You can always check the information regarding the raid device with **mdadm**, like so:

    [root@rhel01 ~]# mdadm -D /dev/md0
    /dev/md0:
    Version : 1.2
    Creation Time : Tue Jan 1 17:02:32 2013
    Raid Level : raid5
    Array Size : 5366784 (5.12 GiB 5.50 GB)
    Used Dev Size : 2683392 (2.56 GiB 2.75 GB)
    Raid Devices : 3
    Total Devices : 3
    Persistence : Superblock is persistent

    Update Time : Tue Jan 1 17:03:40 2013
    State : clean

    Active Devices : 3
    Working Devices : 3
    Failed Devices : 0
    Spare Devices : 0

    Layout : left-symmetric
    Chunk Size : 512K

    Name : rhel01:0 (local to host rhel01)
    UUID : 73a30958:0d00c98d:1cf3f91b:fb500ba6
    Events : 18

    Number Major Minor RaidDevice State
    0 8 17 0 active sync /dev/sdb1
    1 8 18 1 active sync /dev/sdb2
    3 8 19 2 active sync /dev/sdb3


Now let's say that device **/dev/sdb3** needed to be replaced cause it's gone bad. So first let's set the disk as faulty:

    [root@rhel01 ~]# mdadm /dev/md0 -f /dev/sdb3
    mdadm: set /dev/sdb3 faulty in /dev/md0


Now checking the status of our raid, we see the following:

    [root@rhel01 ~]# mdadm -D /dev/md0
    /dev/md0:
    Version : 1.2
    Creation Time : Tue Jan 1 17:02:32 2013
    Raid Level : raid5
    Array Size : 5366784 (5.12 GiB 5.50 GB)
    Used Dev Size : 2683392 (2.56 GiB 2.75 GB)
    Raid Devices : 3
    Total Devices : 3
    Persistence : Superblock is persistent

    Update Time : Tue Jan 1 17:08:09 2013
    State : clean, degraded

    Active Devices : 2
    Working Devices : 2
    Failed Devices : 1
    Spare Devices : 0

    Layout : left-symmetric
    Chunk Size : 512K

    Name : rhel01:0 (local to host rhel01)
    UUID : 73a30958:0d00c98d:1cf3f91b:fb500ba6
    Events : 19

    Number Major Minor RaidDevice State
    0 8 17 0 active sync /dev/sdb1
    1 8 18 1 active sync /dev/sdb2
    2 0 0 2 removed

    3 8 19 - faulty spare /dev/sdb3


We can see the device is set as faulty. Now let's remove the disk completely from the raid:

    [root@rhel01 ~]# mdadm /dev/md0 -r /dev/sdb3
    mdadm: hot removed /dev/sdb3 from /dev/md0


Now checking the status:

    [root@rhel01 ~]# mdadm -D /dev/md0
    /dev/md0:
    Version : 1.2
    Creation Time : Tue Jan 1 17:02:32 2013
    Raid Level : raid5
    Array Size : 5366784 (5.12 GiB 5.50 GB)
    Used Dev Size : 2683392 (2.56 GiB 2.75 GB)
    Raid Devices : 3
    Total Devices : 2
    Persistence : Superblock is persistent

    Update Time : Tue Jan 1 17:10:17 2013
    State : clean, degraded

    Active Devices : 2
    Working Devices : 2
    Failed Devices : 0
    Spare Devices : 0

    Layout : left-symmetric
    Chunk Size : 512K

    Name : rhel01:0 (local to host rhel01)
    UUID : 73a30958:0d00c98d:1cf3f91b:fb500ba6
    Events : 22

    Number Major Minor RaidDevice State
    0 8 17 0 active sync /dev/sdb1
    1 8 18 1 active sync /dev/sdb2
    2 0 0 2 removed


The device is gone now. Now to re-add a brand new disk to the raid configuration:

    [root@rhel01 ~]# mdadm /dev/md0 -a /dev/sdb3
    mdadm: added /dev/sdb3


And now checking the status:

    [root@rhel01 ~]# mdadm -D /dev/md0
    /dev/md0:
    Version : 1.2
    Creation Time : Tue Jan 1 17:02:32 2013
    Raid Level : raid5
    Array Size : 5366784 (5.12 GiB 5.50 GB)
    Used Dev Size : 2683392 (2.56 GiB 2.75 GB)
    Raid Devices : 3
    Total Devices : 3
    Persistence : Superblock is persistent

    Update Time : Tue Jan 1 17:12:42 2013
    State : clean, degraded, recovering

    Active Devices : 2
    Working Devices : 3
    Failed Devices : 0
    Spare Devices : 1

    Layout : left-symmetric
    Chunk Size : 512K

    Rebuild Status : 6% complete

    Name : rhel01:0 (local to host rhel01)
    UUID : 73a30958:0d00c98d:1cf3f91b:fb500ba6
    Events : 26

    Number Major Minor RaidDevice State
    0 8 17 0 active sync /dev/sdb1
    1 8 18 1 active sync /dev/sdb2
    3 8 19 2 spare rebuilding /dev/sdb3


We can see that the disk is added to configuration and then rebuild process has started. When it's done our **/proc/mdstat** will look like this:

    [root@rhel01 ~]# cat /proc/mdstat
    Personalities : [raid6] [raid5] [raid4]
    md0 : active raid5 sdb3[3] sdb2[1] sdb1[0]
    5366784 blocks super 1.2 level 5, 512k chunk, algorithm 2 [3/3] [UUU]

    unused devices: <none>


Since we are coming to the end of partitions let's remove all the raid configurations and partitions to have a clean drive. To remove the raid configuration, let's set all the drives as faulty:

    [root@rhel01 ~]# mdadm /dev/md0 -f /dev/sdb1 /dev/sdb2 /dev/sdb3
    mdadm: set /dev/sdb1 faulty in /dev/md0
    mdadm: set /dev/sdb2 faulty in /dev/md0
    mdadm: set /dev/sdb3 faulty in /dev/md0


Then let's remove all the drives:

    [root@rhel01 ~]# mdadm /dev/md0 -r /dev/sdb1 /dev/sdb2 /dev/sdb3
    mdadm: hot removed /dev/sdb1 from /dev/md0
    mdadm: hot removed /dev/sdb2 from /dev/md0
    mdadm: hot removed /dev/sdb3 from /dev/md0


Finally let's stop the **md0** raid:

    [root@rhel01 ~]# mdadm -S /dev/md0
    mdadm: stopped /dev/md0


Now checking the status:

    [root@rhel01 ~]# cat /proc/mdstat
    Personalities : [raid6] [raid5] [raid4]
    unused devices: <none>


Nothing is utilized. Now using **parted** let's remove all the partitions:

    [root@rhel01 ~]# parted /dev/sdb
    GNU Parted 2.1
    Using /dev/sdb
    Welcome to GNU Parted! Type 'help' to view a list of commands.
    (parted) rm 1
    (parted) rm 2
    (parted) rm 3
    (parted) quit
    Information: You may need to update /etc/fstab.


Lastly make sure no partitions are there after re-reading the table:

    [root@rhel01 ~]# partprobe -s /dev/sdb
    /dev/sdb: msdos partitions


That looks good.

