---
title: RHCSA and RHCE Chapter 4 File Systems and Such
author: Karim Elatov
layout: post
permalink: /2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/
dsq_thread_id:
  - 1410720052
categories:
  - Certifications
  - Home Lab
  - RHCSA and RHCE
tags:
  - /dev/urandom
  - /etc/fstab
  - /etc/mtab
  - /proc/mounts
  - badblocks
  - blkid
  - cryptsetup
  - dd
  - df
  - dumpe2fs
  - e2label
  - edquota
  - ext2
  - ext3
  - filesystem
  - findmnt
  - getfacl
  - luks
  - mkfs
  - mount
  - quota
  - quotacheck
  - quotaoff
  - quotaon
  - repquota
  - setfacl
  - usrquota
---
### File Systems

After we have partitioned our drives to our heart&#8217;s desire, we should actually start using them. The first thing that we need to do is put a file system on our partitions so we can later mount them. From &#8220;<a href="https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Storage_Administration_Guide/Red_Hat_Enterprise_Linux-6-Storage_Administration_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Storage_Administration_Guide/Red_Hat_Enterprise_Linux-6-Storage_Administration_Guide-en-US.pdf']);">Red Hat Enterprise Linux 6 Storage Administration Guide</a>&#8220;, here are some file systems that are supported my RHEL:

> **2&#46;2. Overview of Supported File Systems**
> 
> This section shows basic technical information on each file system supported by Red Hat Enterprise Linux 6.
> 
> <a href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/fs_support/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/fs_support/']);" rel="attachment wp-att-5803"><img class="alignnone size-full wp-image-5803" alt="fs support RHCSA and RHCE Chapter 4 File Systems and Such" src="http://virtuallyhyper.com/wp-content/uploads/2013/01/fs_support.png" width="555" height="256" title="RHCSA and RHCE Chapter 4 File Systems and Such" /></a>

Now here is the process to format a partition with **ext3**:

> **5&#46;2.2. Formatting and Labeling the Partition**
> 
> To format and label the partition use the following procedure:
> 
> **Procedure 5.2. Format and label the partition**
> 
> 1.  The partition still does not have a file system. To create one use the following command:
>     
>         # /sbin/mkfs -t ext3 /dev/sda6
>         
> 
> 2.  Next, give the file system on the partition a label. For example, if the file system on the new partition is /dev/sda6 and you want to label it **/work**, use:
>     
>         # e2label /dev/sda6 /work
>         
>     
>     By default, the installation program uses the mount point of the partition as the label to make sure the label is unique. You can use any label you want.

So let&#8217;s try it out. Let&#8217;s create a single partition on our **sdb** drive and then format that partition with **ext2**:

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
    
    (parted) mkpart primary ext2 1 -1s
    (parted) print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary
    
    (parted) quit
    Information: You may need to update /etc/fstab.
    

Checking how **fdisk** sees the partition:

    [root@rhel01 ~]# fdisk -l /dev/sdb
    
    Disk /dev/sdb: 8589 MB, 8589934592 bytes
    255 heads, 63 sectors/track, 1044 cylinders
    Units = cylinders of 16065 * 512 = 8225280 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk identifier: 0x000bbb96
    
    Device Boot Start End Blocks Id System
    /dev/sdb1 1 1045 8387584 83 Linux 
    

Now to put an **ext2** filesystem on our newly created partition:

    [root@rhel01 ~]# mkfs.ext2 /dev/sdb1
    mke2fs 1.41.12 (17-May-2010)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    Stride=0 blocks, Stripe width=0 blocks
    524288 inodes, 2096896 blocks
    104844 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=2147483648
    64 block groups
    32768 blocks per group, 32768 fragments per group
    8192 inodes per group
    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
    
    Writing inode tables: done
    Writing superblocks and filesystem accounting information: done
    
    This filesystem will be automatically checked every 32 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.
    

#### Converting Ext2 to Ext3

The biggest difference between **ext2** and **ext3** is that **ext3** has journaling. So let&#8217;s convert our file system from **ext2** to **ext3**. From the same guide:

> **8&#46;2. Converting to an Ext3 File System**
> 
> The **tune2fs** allows you to convert an **ext2** file system to **ext3**. To convert an ext2 file system to ext3, log in as root and type the following command in a terminal:
> 
>     tune2fs -j block_device
>     
> 
> where **block_device** contains the **ext2** file system you wish to convert.

So let&#8217;s try that out:

    [root@rhel01 ~]# tune2fs -j /dev/sdb1
    tune2fs 1.41.12 (17-May-2010)
    Creating journal inode: done
    This filesystem will be automatically checked every 32 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.
    

To check if the filesystem is ext3, you can use **dumpe2fs** to query the file system and if it you see &#8216;**has_journal**&#8216; as a file system feature that means it&#8217;s ext3 or above:

    [root@rhel01 ~]# dumpe2fs -h /dev/sdb1 | grep has_journal
    dumpe2fs 1.41.12 (17-May-2010)
    Filesystem features: has_journal ext_attr resize_inode dir_index filetype sparse_super large_file
    

#### File System Labels

As mentioned above we can also **label** our file system. Here is what I did to **label** my file system:

    [root@rhel01 ~]# e2label /dev/sdb1
    
    [root@rhel01 ~]# e2label /dev/sdb1 test
    [root@rhel01 ~]# e2label /dev/sdb1
    test
    

### *mount* command

If we keep going in the guide, we will see this:

> **Chapter 7. Using the mount Command**
> 
> On Linux, UNIX, and similar operating systems, file systems on different partitions and removable devices (CDs, DVDs, or USB flash drives for example) can be attached to a certain point (the mount point) in the directory tree, and then detached again. To attach or detach a file system, use the **mount** or **umount** command respectively. This chapter describes the basic use of these commands, as well as some advanced topics, such as moving a mount point or creating shared subtrees.
> 
> **7&#46;1. Listing Currently Mounted File Systems**
> 
> To display all currently attached file systems, run the mount command with no additional arguments:
> 
>     mount
>     
> 
> This command displays the list of known mount points. Each line provides important information about the device name, the file system type, the directory in which it is mounted, and relevant mount options in the following form:
> 
> **device** on **directory** type **type (options)**
> 
> The **findmnt** utility, which allows users to list mounted file systems in a tree-like form, is also available from Red Hat Enterprise Linux 6.1. To display all currently attached file systems, run the **findmnt** command with no additional arguments:
> 
>     findmnt
>     
> 
> **7&#46;1.1. Specifying the File System Type**
> 
> By default, the output of the mount command includes various virtual file systems such as **sysfs** and **tmpfs**. To display only the devices with a certain file system type, supply the **-t** option on the command line:
> 
>     mount -t type
>     
> 
> Similarly, to display only the devices with a certain file system type by using the **findmnt** command, type:
> 
>     findmnt -t type
>     

Here is what I had on my system:

    [root@rhel01 ~]# mount
    /dev/mapper/VolGroup-lv_root on / type ext4 (rw)
    proc on /proc type proc (rw)
    sysfs on /sys type sysfs (rw)
    devpts on /dev/pts type devpts (rw,gid=5,mode=620)
    tmpfs on /dev/shm type tmpfs (rw,rootcontext="system_u:object_r:tmpfs_t:s0")
    /dev/sda1 on /boot type ext4 (rw)
    none on /proc/sys/fs/binfmt_misc type binfmt_misc (rw)
    [root@rhel01 ~]# findmnt
    TARGET SOURCE FSTYPE OPTIONS
    / /dev/mapper/VolGroup-lv_root ext4 rw,relatime,s
    |-/proc proc proc rw,nosuid,nod
    | |-/proc/bus/usb /proc/bus/usb usbfs rw,relatime
    | |-/proc/sys/fs/binfmt_misc binfmt_m rw,relatime
    |-/sys sysfs sysfs rw,nosuid,nod
    |-/selinux selinuxf rw,relatime
    |-/dev devtmpfs devtmpfs rw,nosuid,rel
    | |-/dev devtmpfs devtmpfs rw,nosuid,rel
    | |-/dev/pts devpts devpts rw,relatime,s
    |-|-/dev/shm tmpfs tmpfs rw,nosuid,nod
    |-/boot /dev/sda1 ext4 rw,relatime,s
    

### Mouting a File System

Now moving through the guide:

> **7&#46;2. Mounting a File System**
> 
> To attach a certain file system, use the mount command in the following form:
> 
>     mount [option…] device directory
>     
> 
> The **device** can be identified by a full path to a block device (for example, &#8220;/dev/sda3&#8243;), a universally unique identifier (UUID; for example, &#8220;UUID=34795a28-ca6d-4fd8-a347-73671d0c19cb&#8221;), or a volume label (for example, “LABEL=home”). Note that while a file system is mounted, the original content of the **directory** is not accessible.
> 
> When the **mount** command is run without all required information (that is, without the device name, the target directory, or the file system type), it reads the content of the **/etc/fstab** configuration file to see if the given file system is listed. This file contains a list of device names and the directories in which the selected file systems should be mounted, as well as the file system type and mount options. Because of this, when mounting a file system that is specified in this file, you can use one of the following variants of the command:
> 
>     mount [option…] directory 
>     mount [option…] device
>     
> 
> **7&#46;2.1. Specifying the File System Type**
> 
> In most cases, mount detects the file system automatically. However, there are certain file systems, such as **NFS** (Network File System) or **CIFS** (Common Internet File System), that are not recognized, and need to be specified manually. To specify the file system type, use the mount command in the following form:
> 
>     mount -t type device directory
>     
> 
> Table 7.1, “Common File System Types” provides a list of common file system types that can be used with the mount command.
> 
> <a href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/fs_for_mount/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/fs_for_mount/']);" rel="attachment wp-att-5804"><img class="alignnone size-full wp-image-5804" alt="fs for mount RHCSA and RHCE Chapter 4 File Systems and Such" src="http://virtuallyhyper.com/wp-content/uploads/2013/01/fs_for_mount.png" width="694" height="348" title="RHCSA and RHCE Chapter 4 File Systems and Such" /></a>

So let&#8217;s go ahead and mount my new file system by device:

    [root@rhel01 ~]# mount /dev/sdb1 /mnt
    [root@rhel01 ~]# df -h | grep sdb
    /dev/sdb1 7.9G 147M 7.4G 2% /mnt
    

#### Unmounting a File System

Now let&#8217;s un-mount the device. From the storage guide:

> **7&#46;3. Unmounting a File System**
> 
> To detach a previously mounted file system, use either of the following variants of the umount command:
> 
>     umount directory
>     umount device
>     
> 
> Note that unless this is performed while logged in as root, the correct permissions must be available to unmount the file system.
> 
> **Important: Make Sure the Directory is Not in Use**
> 
> When a file system is in use (for example, when a process is reading a file on this file system, or when it is used by the kernel), running the umount command will fail with an error. To determine which processes are accessing the file system, use the fuser command in the following form:
> 
>     fuser -m directory
>     
> 
> For example, to list the processes that are accessing a file system mounted to the /media/cdrom/ directory, type:
> 
>     $ fuser -m /media/cdrom
>     /media/cdrom: 1793 2013 2022 2435 10532c 10672c
>     

Here is what I did to un-mount my file system. Now if left a logged in session sitting in that directory, I would run into the issue the guide described:

    [root@rhel01 ~]# umount /mnt
    umount: /mnt: device is busy.
    (In some cases useful info about processes that use
    the device is found by lsof(8) or fuser(1))
    

Notice it mentions two utilities to use to get to the bottom of the issue: **lsof** and **fuser**. Here is an example of **fuser** to see what is locking a directory:

    [root@rhel01 ~]# fuser -muv /mnt
    USER PID ACCESS COMMAND
    /mnt: root 2383 ..c.. (root)bash
    

Here is a similar way with **lsof**:

    [root@rhel01 ~]# lsof /mnt
    COMMAND PID USER FD TYPE DEVICE SIZE/OFF NODE NAME
    bash   2383 root cwd DIR 8,17   4096     2   /mnt
    

From the above we can see that a root session is logged in and is currently in that directory. The **cwd** stands for current working directory. There are two ways to go about this. One is if you have have access to that session then leave that directory:

    [root@rhel01 mnt]# pwd
    /mnt
    [root@rhel01 mnt]# cd
    [root@rhel01 ~]# pwd
    /root
    

Then trying the un-mount it would be successful. Or you could use **fuser** to kill any process using that directory, like so:

    [root@rhel01 ~]# fuser -muv /mnt
    USER PID ACCESS COMMAND
    /mnt: root 2383 ..c.. (root)bash
    [root@rhel01 ~]# fuser -kuv /mnt
    USER PID ACCESS COMMAND
    /mnt: root 2383 ..c.. (root)bash
    [root@rhel01 ~]# fuser -muv /mnt
    

After doing any of the above, I was able to un-mount without any issues:

    [root@rhel01 ~]# umount /mnt
    

and then remounting by using the label:

    [root@rhel01 ~]# mount LABEL=test /mnt
    [root@rhel01 ~]# df -h | grep sdb
    /dev/sdb1 7.9G 147M 7.4G 2% /mnt
    

### File System Structure

After a file system is mounted you can then put files on it. From the same guide:

> **Chapter 6. File System Structure**
> 
> The file system structure is the most basic level of organization in an operating system. Almost all of the ways an operating system interacts with its users, applications, and security model are dependent on how the operating system organizes files on storage devices. Providing a common file system structure ensures users and programs can access and write files.
> 
> File systems break files down into two logical categories:
> 
> *   Shareable vs. unsharable files
> *   Variable vs. static files 
> 
> Shareable files can be accessed locally and by remote hosts; unsharable files are only available locally. Variable files, such as documents, can be changed at any time; static files, such as binaries, do not change without an action from the system administrator.
> 
> Categorizing files in this manner helps correlate the function of each file with the permissions assigned to the directories which hold them. How the operating system and its users interact with a file determines the directory in which it is placed, whether that directory is mounted with read-only or read/write permissions, and the level of access each user has to that file. The top level of this organization is crucial; access to the underlying directories can be restricted, otherwise security problems could arise if, from the top level down, access rules do not adhere to a rigid structure.
> 
> **6&#46;2. Overview of File System Hierarchy Standard (FHS)**
> 
> Red Hat Enterprise Linux uses the Filesystem Hierarchy Standard (FHS) file system structure, which defines the names, locations, and permissions for many file types and directories.
> 
> The FHS document is the authoritative reference to any FHS-compliant file system, but the standard leaves many areas undefined or extensible. This section is an overview of the standard and a description of the parts of the file system not covered by the standard.
> 
> The two most important elements of FHS compliance are:
> 
> *   Compatibility with other FHS-compliant systems
> *   The ability to mount a /usr/ partition as read-only. This is especially crucial, since /usr/ contains common executables and should not be changed by users. In addition, since /usr/ is mounted as read-only, it should be mountable from the CD-ROM drive or from another machine via a read-only NFS mount.
> 
> **6&#46;2.1.1. Gathering File System Information**
> 
> The **df** command reports the system&#8217;s disk space usage.
> 
> The **du** command displays the estimated amount of space being used by files in a directory, displaying the disk usage of each subdirectory. The last line in the output of du shows the total disk usage of the directory; to see only the total disk usage of a directory in human-readable format, use **du -hs**.

I already showed **df**, now for **du**:

    [root@rhel01 ~]# du -sh /mnt
    20K /mnt 
    

I just mounted the file system, I didn&#8217;t put any files on it.

### Swap File System

Another popular file system is a swap file system. From the storage guide:

> **17&#46;1. What is Swap Space?**
> 
> Swap space in Linux is used when the amount of physical memory (RAM) is full. If the system needs more memory resources and the RAM is full, inactive pages in memory are moved to the swap space. While swap space can help machines with a small amount of RAM, it should not be considered a replacement for more RAM. Swap space is located on hard drives, which have a slower access time than physical memory.
> 
> Swap space can be a dedicated swap partition (recommended), a swap file, or a combination of swap partitions and swap files. Swap should equal 2x physical RAM for up to 2 GB of physical RAM, and then an additional 1x physical RAM for any amount above 2 GB, but never less than 32 MB.
> 
> For systems with really large amounts of RAM (more than 32 GB) you can likely get away with a smaller swap partition (around 1x, or less, of physical RAM).
> 
> **17&#46;2. Adding Swap Space**
> 
> Sometimes it is necessary to add more swap space after installation. For example, you may upgrade the amount of RAM in your system from 1 GB to 2 GB, but there is only 2 GB of swap space. It might be advantageous to increase the amount of swap space to 4 GB if you perform memory-intense operations or run applications that require a large amount of memory.
> 
> You have three options: create a new swap partition, create a new swap file, or extend swap on an existing LVM2 logical volume. It is recommended that you extend an existing logical volume.
> 
> **17&#46;2.2. Creating an LVM2 Logical Volume for Swap**
> 
> 1.  Create the LVM2 logical volume of size 2 GB:
>     
>         # lvcreate VolGroup00 -n LogVol02 -L 2G    
>         
> 
> 2.  Format the new swap space:
>     
>         # mkswap /dev/VolGroup00/LogVol02
>         
> 
> 3.  Add the following entry to the **/etc/fstab** file:
>     
>         # /dev/VolGroup00/LogVol02 swap swap defaults 0 0
>         
> 
> 4.  Enable the extended logical volume:
>     
>         # swapon -v /dev/VolGroup00/LogVol02
>         
> 
> To test if the logical volume was successfully created, use cat \*\* /proc/swaps\*\* or **free** to inspect the swap space.
> 
> **17&#46;2.3. Creating a Swap File**
> 
> To add a swap file:
> 
> **Procedure 17.2. Add a swap file**
> 
> 1.  Determine the size of the new swap file in megabytes and multiply by 1024 to determine the number of blocks. For example, the block size of a 64 MB swap file is 65536. 
> 2.  At a shell, type the following command with count being equal to the desired block size:
>     
>         # dd if=/dev/zero of=/swapfile bs=1024 count=65536
>         
> 
> 3.  Setup the swap file with the command:
>     
>         # mkswap /swapfile
>         
> 
> 4.  To enable the swap file immediately but not automatically at boot time:
>     
>         # swapon /swapfile
>         
> 
> 5.  To enable it at boot time, edit /etc/fstab to include the following entry:
>     
>         /swapfile swap swap defaults 0 0
>         
>     
>     The next time the system boots, it enables the new swap file.
> 
> To test if the new swap file was successfully created, use **cat /proc/swaps** or **free** to inspect the swap space.

Let&#8217;s un-mount **sdb1** and then remove it and re-create marking it for swap. Currently we have the following:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary ext3
    

Notice the file system field is filled out, this happens after you do a **mkfs** on it. If you look in the previous section that field was blank. So let&#8217;s remove the partition and re-add it as a swap partition:

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
    1 1049kB 8590MB 8589MB primary ext3
    
    (parted) rm 1
    (parted) mkpart primary linux-swap 1 -1s
    (parted) quit
    Information: You may need to update /etc/fstab.
    
    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary ext3
    

Notice the field hasn&#8217;t changed. So now let&#8217;s make that partition into a swap partition:

    [root@rhel01 ~]# mkswap /dev/sdb1
    Setting up swapspace version 1, size = 8387580 KiB
    no label, UUID=68e2ffa6-9aee-40f4-8594-e5b947d221c2
    

Now let&#8217;s activate it:

    [root@rhel01 ~]# swapon -v /dev/sdb1
    swapon on /dev/sdb1
    swapon: /dev/sdb1: found swap signature: version 1, page-size 4, same byte order
    swapon: /dev/sdb1: pagesize=4096, swapsize=8588886016, devsize=8588886016
    [root@rhel01 ~]# swapon -s
    Filename     Type    Size   Used    Priority
    /dev/dm-1 partition 1048568 0   -1
    /dev/sdb1 partition 8387576 0   -2
    

The top one is the system created one, and the bottom one is the one I just created. Also checking out the output of **parted**, we see the following:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary linux-swap(v1)
    

So **parted** actually checks the file system and if it&#8217;s known type it will fill it in. Now also checking out **free**:

    [root@rhel01 ~]# free -m
    total used free shared buffers cached
    Mem: 499 151 347 0 46 47
    -/+ buffers/cache: 58 440
    Swap: 9214 0 9214
    

Notice under swap we have about 9GB, this is the combination of the system swap partition and mine.

#### Removing Swap Space

Now onto the removing section:

> **17&#46;3. Removing Swap Space**
> 
> Sometimes it can be prudent to reduce swap space after installation. For example, say you downgraded the amount of RAM in your system from 1 GB to 512 MB, but there is 2 GB of swap space still assigned. It might be advantageous to reduce the amount of swap space to 1 GB, since the larger 2 GB could be wasting disk space.
> 
> **17&#46;3.2. Removing an LVM2 Logical Volume for Swap**
> 
> To remove a swap volume group
> 
> **Procedure 17.4 . Remove a swap volume group**
> 
> 1.  Disable swapping for the associated logical volume:
>     
>         # swapoff -v /dev/VolGroup00/LogVol02
>         
> 
> 2.  Remove the LVM2 logical volume of size 512 MB:
>     
>         # lvremove /dev/VolGroup00/LogVol02
>         
> 
> 3.  Remove the following entry from the /etc/fstab file:
>     
>         /dev/VolGroup00/LogVol02 swap swap defaults 0 0
>         
> 
> To test if the logical volume size was successfully removed, use > **cat /proc/swaps** or **free** to inspect the swap space.
> 
> **17&#46;3.3. Removing a Swap File**
> 
> To remove a swap file:
> 
> **Procedure 17.5. Remove a swap file**
> 
> 1.  At a shell prompt, execute the following command to disable the swap file (where /swapfile is the swap file):
>     
>         # swapoff -v /swapfile
>         
> 
> 2.  Remove its entry from the **/etc/fstab** file.
> 
> 3.  Remove the actual file:
>     
>         # rm /swapfile
>         

So let&#8217;s go ahead and disable my swap partition:

    [root@rhel01 ~]# swapoff -v /dev/sdb1
    swapoff on /dev/sdb1
    [root@rhel01 ~]# cat /proc/swaps
    Filename     Type    Size   Used    Priority
    /dev/dm-1 partition 1048568 0   -1
    

And we can see only the system defined one. Lastly here is output of **free**:

    [root@rhel01 ~]# free -m
    total used free shared buffers cached
    Mem: 499 145 353 0 46 47
    -/+ buffers/cache: 52 446
    Swap: 1023 0 1023
    

### */etc/fstab* file

Through out the guide we see the mention of the **/etc/fstab** file. From the storage guide:

> **5&#46;2.3. Add to /etc/fstab**
> 
> As root, edit the **/etc/fstab** file to include the new partition using the partition&#8217;s UUID. Use the command **blkid -o list** for a complete list of the partition&#8217;s UUID, or **blkid device** for individual device details.
> 
> The first column should contain **UUID=** followed by the file system&#8217;s UUID. The second column should contain the mount point for the new partition, and the next column should be the file system type (for example, ext3 or swap). If you need more information about the format, read the man page with the command **man fstab**.
> 
> If the fourth column is the word **defaults**, the partition is mounted at boot time. To mount the partition without rebooting, as root, type the command:
> 
>     mount /work
>     

Here is how my file looked like:

    [root@rhel01 ~]# cat /etc/fstab
    # /etc/fstab
    # Created by anaconda on Thu Dec 27 17:46:04 2012
    #
    # Accessible filesystems, by reference, are maintained under '/dev/disk'
    # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
    #
    /dev/mapper/VolGroup-lv_root / ext4 defaults 1 1
    UUID=5486b50b-064a-442c-80bc-84c7cdbdd607 /boot ext4 defaults 1 2
    /dev/mapper/VolGroup-lv_swap swap swap defaults 0 0
    tmpfs /dev/shm tmpfs defaults 0 0
    devpts /dev/pts devpts gid=5,mode=620 0 0
    sysfs /sys sysfs defaults 0 0
    proc /proc proc defaults 0 0
    

Notice that either the device or the uuid of the device are used. So let&#8217;s reformat our **sdb1** partition as **ext3** and add it to our **/etc/fstab** file and then mount it. First let&#8217;s check out what file system on there now:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary linux-swap(v1)
    

Not let&#8217;s format it with **ext3**:

    [root@rhel01 ~]# mkfs.ext3 /dev/sdb1
    mke2fs 1.41.12 (17-May-2010)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    Stride=0 blocks, Stripe width=0 blocks
    524288 inodes, 2096896 blocks
    104844 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=2147483648
    64 block groups
    32768 blocks per group, 32768 fragments per group
    8192 inodes per group
    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
    
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done
    
    This filesystem will be automatically checked every 36 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.
    

Now checking out the output of **parted**:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary ext3
    

That looks good. Now to add an entry to **/etc/fstab**. Let&#8217;s look at the man page of fstab (**man 5 fstab**) to see all the fields defined:

       The first field, (fs_spec),  describes  the  block  special  device  or
       remote filesystem to be mounted.
    
       For  ordinary  mounts  it  will hold (a link to) a block special device
       node (as created by mknod(8))  for  the  device  to  be  mounted,  like
       ‘/dev/cdrom’   or   ‘/dev/sdb7’.    For   NFS   mounts  one  will  have
       <host>:<dir>, e.g., ‘knuth.aeb.nl:/’.  For procfs, use ‘proc’.
    
       Instead of giving the device explicitly, one may indicate the (ext2  or
       xfs)  filesystem that is to be mounted by its UUID or volume label (cf.
       e2label(8) or  xfs_admin(8)),  writing  LABEL=<label>  or  UUID=<uuid>,
       e.g.,   ‘LABEL=Boot’   or  ‘UUID=3e6be9de-8139-11d1-9106-a43f08d823a6’.
       This will make the system more robust: adding or removing a  SCSI  disk
       changes the disk device name but not the filesystem volume label.
    

So our first field will be **/dev/sdb1**. Going down the man page:

    The second field, (fs_file), describes the mount point for the filesys-
       tem.  For swap partitions, this field should be specified as ‘none’. If
       the  name  of  the  mount point contains spaces these can be escaped as
       ‘\040’.
    

So the second field will be **/mnt**. Onto the 3rd field:

     The third field, (fs_vfstype), describes the type  of  the  filesystem.
       Linux  supports  lots  of filesystem types, such as adfs, affs, autofs,
       coda, coherent, cramfs, devpts, efs, ext2, ext3,  hfs,  hpfs,  iso9660,
       jfs,  minix,  msdos,  ncpfs,  nfs,  ntfs,  proc, qnx4, reiserfs, romfs,
       smbfs, sysv, tmpfs, udf, ufs, umsdos, vfat, xenix,  xfs,  and  possibly
       others.  For more details, see mount(8).  For the filesystems currently
       supported by the running kernel, see /proc/filesystems.  An entry  swap
       denotes a file or partition to be used for swapping, cf. swapon(8).  An
       entry ignore causes the line to be ignored.  This  is  useful  to  show
       disk  partitions  which  are currently unused.  An entry none is useful
       for bind or move mounts.
    
       mount(8) and umount(8) support  filesystem  subtypes.  The  subtype  is
       defined  by  ’.subtype’  suffix.  For example ’fuse.sshfs’. It’s recom-
       mended to use subtype notation rather than add any prefix to the  first
       fstab field (for example ’sshfs#example.com’ is depreacated).
    

Our third field will be **ext3**. Then if we keep going:

      The  fourth  field, (fs_mntops), describes the mount options associated
       with the filesystem.
    
       It is formatted as a comma separated list of options.  It  contains  at
       least  the type of mount plus any additional options appropriate to the
       filesystem type.  For documentation on the available options  for  non-
       nfs  file systems, see mount(8).  For documentation on all nfs-specific
       options have a look at nfs(5).  Common for all types of file system are
       the options ‘‘noauto’’ (do not mount when "mount -a" is given, e.g., at
       boot time), ‘‘user’’ (allow a user  to  mount),  and  ‘‘owner’’  (allow
       device  owner  to mount), and ‘‘comment’’ (e.g., for use by fstab-main-
       taining programs).  The ‘‘owner’’ and ‘‘comment’’  options  are  Linux-
       specific.  For more details, see mount(8).
    

We won&#8217;t be doing anything special, so our 4th field will be **defaults**. The next field:

     The  fifth  field,  (fs_freq),  is  used  for  these filesystems by the
       dump(8) command to determine which filesystems need to be  dumped.   If
       the  fifth  field  is not present, a value of zero is returned and dump
       will assume that the filesystem does not need to be dumped.
    

I don&#8217;t need backups of this file system so I will use **** for the fifth field. And lastly:

     The sixth field, (fs_passno), is used by the fsck(8) program to  deter-
       mine the order in which filesystem checks are done at reboot time.  The
       root filesystem should be specified with a fs_passno of  1,  and  other
       filesystems  should  have a fs_passno of 2.  Filesystems within a drive
       will be checked sequentially, but filesystems on different drives  will
       be  checked  at  the  same time to utilize parallelism available in the
       hardware.  If the sixth field is not present or zero, a value  of  zero
       is  returned  and fsck will assume that the filesystem does not need to
       be checked.
    

If I was adding this partition permanently I would make this field **2**, but since this is a just temporary, I will make it ****. Putting it all together and adding an entry to the file, I ran this:

    [root@rhel01 ~]# echo "/dev/sdb1 /mnt ext3 defaults 0 0" >> /etc/fstab
    

Now checking out the file:

    [root@rhel01 ~]# tail /etc/fstab
    # See man pages fstab(5), findfs(8), mount(8) and/or blkid(8) for more info
    #
    /dev/mapper/VolGroup-lv_root / ext4 defaults 1 1
    UUID=5486b50b-064a-442c-80bc-84c7cdbdd607 /boot ext4 defaults 1 2
    /dev/mapper/VolGroup-lv_swap swap swap defaults 0 0
    tmpfs /dev/shm tmpfs defaults 0 0
    devpts /dev/pts devpts gid=5,mode=620 0 0
    sysfs /sys sysfs defaults 0 0
    proc /proc proc defaults 0 0
    /dev/sdb1 /mnt ext3 defaults 0 0
    

I could probably format it better, but I will remove it in a little bit anyways. Now that the entry exists, I can mount the file system by just specifying one of the 1st two entries (ie **/dev/sdb1** or **/mnt**). So let&#8217;s try it:

    [root@rhel01 ~]# mount /dev/sdb1
    [root@rhel01 ~]# df -h | grep sdb
    /dev/sdb1 7.9G 147M 7.4G 2% /mnt
    

and same thing goes for **umount**:

    [root@rhel01 ~]# umount /mnt 
    

The last thing I saw in &#8220;<a href="https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf']);">Red Hat Enterprise Linux 6 Deployment Guide</a>&#8221; is the following:

> **E.2.21. /proc/mounts**
> 
> This file provides a list of all mounts in use by the system:
> 
>     rootfs / rootfs rw 0 0
>     /proc /proc proc rw,nodiratime 0 0 none
>     /dev ramfs rw 0 0
>     /dev/mapper/VolGroup00-LogVol00 / ext3 rw 0 0
>     
> 
> The output found here is similar to the contents of **/etc/mtab**, except that **/proc/mounts** is more up-to-date.
> 
> The first column specifies the device that is mounted, the second column reveals the mount point, and the third column tells the file system type, and the fourth column tells you if it is mounted read-only (**ro**) or read-write (**rw**). The fifth and sixth columns are dummy values designed to match the format used in **/etc/mtab**.

So as you mount a file system on a machine you can check **/etc/mtab** or **/proc/mounts** even though there are no entries under **/etc/fstab** you can still mount a file system.

### Device Encryption

Now if we wanted to encrypt a file system we can also do that. From &#8220;<a href="https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf" onclick="javascript:_gaq.push(['_trackEvent','download','http://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf']);">Red Hat Enterprise Linux 6 Installation Guide</a>&#8220;:

> **C.1. What is block device encryption?**
> 
> Block device encryption protects the data on a block device by encrypting it. To access the device&#8217;s decrypted contents, a user must provide a passphrase or key as authentication. This provides additional security beyond existing OS security mechanisms in that it protects the device&#8217;s contents even if it has been physically removed from the system.
> 
> **C.2. Encrypting block devices using dm-crypt/LUKS**
> 
> Linux Unified Key Setup (LUKS) is a specification for block device encryption. It establishes an on-disk format for the data, as well as a passphrase/key management policy.
> 
> LUKS uses the kernel device mapper subsystem via the **dm-crypt** module. This arrangement provides a low-level mapping that handles encryption and decryption of the device&#8217;s data. User-level operations, such as creating and accessing encrypted devices, are accomplished through the use of the **cryptsetup** utility.
> 
> **C.2.1. Overview of LUKS**
> 
> *   What LUKS does: 
>     *   LUKS encrypts entire block devices 
>         *   LUKS is thereby well-suited for protecting the contents of mobile devices such as: 
>             *   Removable storage media
>             *   Laptop disk drives
>     *   The underlying contents of the encrypted block device are arbitrary. 
>         *   This makes it useful for encrypting swap devices.
>         *   This can also be useful with certain databases that use specially formatted block devices for data storage.
>     *   LUKS uses the existing device mapper kernel subsystem. 
>         *   This is the same subsystem used by LVM, so it is well tested.
>     *   LUKS provides passphrase strengthening. 
>         *   This protects against dictionary attacks.
>     *   LUKS devices contain multiple key slots. 
>         *   This allows users to add backup keys/passphrases.
> *   What LUKS does not do: 
>     *   LUKS is not well-suited for applications requiring many (more than eight) users to have distinct access keys to the same device.
>     *   LUKS is not well-suited for applications requiring file-level encryption.
> 
> **C.2.2. How will I access the encrypted devices after installation? (System Startup)**
> 
> During system startup you will be presented with a passphrase prompt. After the correct passphrase has been provided the system will continue to boot normally. If you used different passphrases for multiple encrypted devices you may need to enter more than one passphrase during the startup

### LUKS Encrypted Device

Now let&#8217;s see how this is actually done:

> **C.4. Creating Encrypted Block Devices on the Installed System After Installation**
> 
> Encrypted block devices can be created and configured after installation.
> 
> **C.4.1. Create the block devices**
> 
> Create the block devices you want to encrypt by using **parted**, **pvcreate**, **lvcreate** and **mdadm**.
> 
> **C.4.2. Optional: Fill the device with random data**
> 
> Filling **device** (eg: **/dev/sda3**) with random data before encrypting it greatly increases the strength of the encryption. The downside is that it can take a very long time. The best way, which provides high quality random data but takes a long time (several minutes per gigabyte on most systems):
> 
>     dd if=/dev/urandom of=device
>     
> 
> Fastest way, which provides lower quality random data:
> 
>     badblocks -c 10240 -s -w -t random -v device
>     
> 
> **C.4.3. Format the device as a dm-crypt/LUKS encrypted device**
> 
>     cryptsetup luksFormat device
>     
> 
> After supplying the passphrase twice the device will be formatted for use. To verify, use the following command:
> 
>     cryptsetup isLuks device && echo Success
>     
> 
> To see a summary of the encryption information for the device, use the following command:
> 
>     cryptsetup luksDump device
>     
> 
> **C.4.4. Create a mapping to allow access to the device&#8217;s decrypted contents**
> 
> To access the device&#8217;s decrypted contents, a mapping must be established using the kernel **device-mapper**.
> 
> It is useful to choose a meaningful name for this mapping. LUKS provides a UUID (Universally Unique Identifier) for each device. This, unlike the device name (eg: **/dev/sda3**), is guaranteed to remain constant as long as the LUKS header remains intact. To find a LUKS device&#8217;s UUID, run the following command:
> 
>     cryptsetup luksUUID device
>     
> 
> An example of a reliable, informative and unique mapping name would be **luks-uuid**, where **uuid** is replaced with the device&#8217;s LUKS UUID (eg: **luks-50ec957a-5b5a-47ee-85e6-f8085bbc97a8**). This naming convention might seem unwieldy but is it not necessary to type it often.
> 
>     cryptsetup luksOpen device name
>     
> 
> There should now be a device node, **/dev/mapper/name**, which represents the decrypted device. This block device can be read from and written to like any other unencrypted block device.
> 
> To see some information about the mapped device, use the following command:
> 
>     dmsetup info name
>     
> 
> **C.4.5. Create filesystems on the mapped device, or continue to build complex storage structures using the mapped device**
> 
> Use the mapped device node (**/dev/mapper/name**) as any other block device. To create an **ext2** filesystem on the mapped device, use the following command:
> 
>     mkfs.ext2 /dev/mapper/name
>     
> 
> To mount this filesystem on **/mnt/test**, use the following command:
> 
>     mount /dev/mapper/name /mnt/test
>     
> 
> **C.4.6. Add the mapping information to /etc/crypttab**
> 
> In order for the system to set up a mapping for the device, an entry must be present in the **/etc/crypttab** file. If the file doesn&#8217;t exist, create it and change the owner and group to **root** (**root:root**) and change the mode to **0744**. Add a line to the file with the following format:
> 
>     name device none
>     
> 
> The **device** field should be given in the form &#8220;**UUID=<luks_uuid></luks_uuid>**&#8220;, where **luks_uuid** is the LUKS uuid as given by the command **cryptsetup luksUUID device**. This ensures the correct device will be identified and used even if the device node (eg: **/dev/sda5**) changes.
> 
> **C.4.7. Add an entry to /etc/fstab**
> 
> Add an entry to **/etc/fstab**. This is only necessary if you want to establish a persistent association between the device and a mountpoint. Use the decrypted device, **/dev/mapper/name** in the\*\* /etc/fstab\*\* file.
> 
> In many cases it is desirable to list devices in **/etc/fstab** by UUID or by a filesystem label. The main purpose of this is to provide a constant identifier in the event that the device name (eg: **/dev/sda4**) changes. LUKS device names in the form of **/dev/mapper/luks-luks_uuid** are based only on the device&#8217;s LUKS UUID, and are therefore guaranteed to remain constant. This fact makes them suitable for use in **/etc/fstab**.

So let&#8217;s give it a try with my **/dev/sdb1** partition. First let&#8217;s fill it with random data, using the quick method:

    [root@rhel01 ~]# badblocks -c 10240 -s -w -t random -v /dev/sdb1
    Checking for bad blocks in read-write mode
    From block 0 to 8387583
    Testing with random pattern: done
    Reading and comparing: done
    Pass completed, 0 bad blocks found.
    

Now let&#8217;s format the device as a LUKS Encrypted device:

    [root@rhel01 ~]# cryptsetup luksFormat /dev/sdb1
    
    WARNING!
    ========
    This will overwrite data on /dev/sdb1 irrevocably.
    
    Are you sure? (Type uppercase yes): YES
    Enter LUKS passphrase:
    Verify passphrase:
    

Now let&#8217;s confirm that it was successfully formatted:

    [root@rhel01 ~]# cryptsetup isLuks /dev/sdb1 && echo Success
    Success
    

You would see the following if it didn&#8217;t work for some reason:

    [root@rhel01 ~]# cryptsetup isLuks /dev/sdb1 && echo Success
    Device /dev/sdb1 is not a valid LUKS device.
    

Now let&#8217;s see the details of our encrypted device:

    [root@rhel01 ~]# cryptsetup luksDump /dev/sdb1
    LUKS header information for /dev/sdb1
    
    Version: 1
    Cipher name: aes
    Cipher mode: cbc-essiv:sha256
    Hash spec: sha1
    Payload offset: 4096
    MK bits: 256
    MK digest: ea 2f 86 5b e8 fa 8c 5a bd b7 75 de 74 ae 9b 1b 77 3b a7 30
    MK salt: da 66 b0 98 a6 e2 02 c7 57 01 79 9f 5f ec 4e fc
    08 2b 42 b4 cf f1 82 cc b7 2e d2 a5 e2 33 ea 1a
    MK iterations: 29125
    UUID: 4bf8105f-aca1-4d13-8977-1495ca2d2a99
    

We can see the algorithms used for the device encryption. We can also see the UUID of the LUKS device. We can also run the following to get the UUID:

    [root@rhel01 ~]# cryptsetup luksUUID /dev/sdb1
    4bf8105f-aca1-4d13-8977-1495ca2d2a99
    

Now let&#8217;s go ahead and create a mapping to the de-crypted device and give the mapping a name:

    [root@rhel01 ~]# cryptsetup luksOpen /dev/sdb1 my_enc_dev
    Enter passphrase for /dev/sdb1:
    

To confirm that it worked let&#8217;s make sure the mapping exists:

    [root@rhel01 ~]# dmsetup ls
    VolGroup-lv_swap    (253:1)
    VolGroup-lv_root    (253:0)
    my_enc_dev  (253:2)
    

If we want more information regarding our mapping we can do the following:

    [root@rhel01 ~]# dmsetup info my_enc_dev
    Name: my_enc_dev
    State: ACTIVE
    Read Ahead: 256
    Tables present: LIVE
    Open count: 0
    Event number: 0
    Major, minor: 253, 2
    Number of targets: 1
    UUID: CRYPT-LUKS1-4bf8105faca14d1389771495ca2d2a99-my_enc_dev
    

That looks good. Now to format our mapped device:

    [root@rhel01 ~]# mkfs.ext4 /dev/mapper/my_enc_dev
    mke2fs 1.41.12 (17-May-2010)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    Stride=0 blocks, Stripe width=0 blocks
    524288 inodes, 2096384 blocks
    104819 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=2147483648
    64 block groups
    32768 blocks per group, 32768 fragments per group
    8192 inodes per group
    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
    
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done
    
    This filesystem will be automatically checked every 39 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.
    

Now notice parted doesn&#8217;t know the file system of the partition but it does know it for the de-crypted mapped device:

    [root@rhel01 ~]# parted /dev/sdb print
    Model: VMware Virtual disk (scsi)
    Disk /dev/sdb: 8590MB
    Sector size (logical/physical): 512B/512B
    Partition Table: msdos
    
    Number Start End Size Type File system Flags
    1 1049kB 8590MB 8589MB primary
    
    [root@rhel01 ~]# parted /dev/mapper/my_enc_dev print
    Model: Linux device-mapper (crypt) (dm)
    Disk /dev/mapper/my_enc_dev: 8587MB
    Sector size (logical/physical): 512B/512B
    Partition Table: loop
    
    Number Start End Size File system Flags
    1 0.00B 8587MB 8587MB ext4
    

This is of course expected since the partition is encrypted by LUKS. If you don&#8217;t want to keep re-creating the mapped device, you can add the following to your **/etc/crypttab** file:

    [root@rhel01 ~]# cat /etc/crypttab
    my_enc_dev UUID=4bf8105f-aca1-4d13-8977-1495ca2d2a99 none
    

Now after rebooting the machine the mapping will be re-created automatically and you won&#8217;t have to run **cryptsetup luksOpen** to create a mapping every time you reboot the machine. However since when the mapping is created you need to first de-crypt the device with the password and the boot process will pause and wait for the passphrase to be entered. If you want go further you can entry to the **/etc/fstab** file but if you set it to be auto mounted, the same things applies, you will need to enter the password in order for the device to be de-crypted first. Oh and don&#8217;t forget to set the mode of the **/etc/crypttab** file to be **744**. Here is what I did to ensure that:

    [root@rhel01 ~]# chmod 744 /etc/crypttab
    [root@rhel01 ~]# ls -l /etc/crypttab
    -rwxr--r--. 1 root root 58 Jan 6 11:20 /etc/crypttab
    

### Disk Quotas

If a file system is mounted with special options it can enable special functions. For example from the storage guide:

> **Chapter 18. Disk Quotas**
> 
> Disk space can be restricted by implementing disk quotas which alert a system administrator before a user consumes too much disk space or a partition becomes full.
> 
> Disk quotas can be configured for individual users as well as user groups. This makes it possible to manage the space allocated for user-specific files (such as email) separately from the space allocated to the projects a user works on (assuming the projects are given their own groups).
> 
> In addition, quotas can be set not just to control the number of disk blocks consumed but to control the number of inodes (data structures that contain information about files in UNIX file systems). Because inodes are used to contain file-related information, this allows control over the number of files that can be created.
> 
> The **quota** RPM must be installed to implement disk quotas.

Before we keep going let&#8217;s go ahead and install the appropriate RPM:

    [root@rhel01 ~]# yum install quota -y
    

Now to the actual configuration. From the storage guide:

#### Enables Quotas

> **18&#46;1. Configuring Disk Quotas**
> 
> To implement disk quotas, use the following steps:
> 
> 1.  Enable quotas per file system by modifying the /etc/fstab file.
> 2.  Remount the file system(s).
> 3.  Create the quota database files and generate the disk usage table.
> 4.  Assign quota policies. Each of these steps is discussed in detail in the following sections. 
> 
> **18&#46;1.1. Enabling Quotas**
> 
> As root, using a text editor, edit the **/etc/fstab** file.
> 
> **Example 18.1. Edit /etc/fstab**
> 
> For example, to use the text editor vim type the following:
> 
>     # vim /etc/fstab
>     
> 
> Add the **usrquota** and/or **grpquota** options to the file systems that require quotas:
> 
> **Example 18.2. Add quotas**
> 
>     /dev/VolGroup00/LogVol00 / ext3 defaults 1 1
>     LABEL=/boot /boot ext3 defaults 1 2
>     none /dev/pts devpts gid=5,mode=620 0 0
>     none /dev/shm tmpfs defaults 0 0
>     none /proc proc defaults 0 0
>     none /sys sysfs defaults 0 0
>     /dev/VolGroup00/LogVol02 /home ext3 defaults,usrquota,grpquota 1 2
>     /dev/VolGroup00/LogVol01 swap swap defaults 0 0 . . .
>     
> 
> In this example, the **/home** file system has both user and group quotas enabled.
> 
> **18&#46;1.2. Remounting the File Systems**
> 
> After adding the **usrquota** and/or **grpquota** options, remount each file system whose **fstab** entry has been modified. If the file system is not in use by any process, use one of the following methods:
> 
> *   Issue the **umount** command followed by the mount command to remount the file system. Refer to the man page for both **umount** and **mount** for the specific syntax for mounting and unmounting various file system types
> *   Issue the **mount -o remount file-system** command (where **file-system** is the name of the file system) to remount the file system. For example, to remount the **/home** file system, the command to issue is **mount -o remount /home**. 
> 
> If the file system is currently in use, the easiest method for remounting the file system is to reboot the system.
> 
> **18&#46;1.3. Creating the Quota Database Files**
> 
> After each quota-enabled file system is remounted run the **quotacheck** command.
> 
> The **quotacheck** command examines quota-enabled file systems and builds a table of the current disk usage per file system. The table is then used to update the operating system&#8217;s copy of disk usage. In addition, the file system&#8217;s disk quota files are updated.
> 
> To create the quota files (**aquota.user** and **aquota.group**) on the file system, use the **-c** option of the **quotacheck** command.
> 
> **Example 18.3. Create quota files**
> 
> For example, if user and group quotas are enabled for the **/home** file system, create the files in the **/home** directory:
> 
>     # quotacheck -cug /home 
>     
> 
> The **-c** option specifies that the quota files should be created for each file system with quotas enabled, the **-u** option specifies to check for user quotas, and the **-g** option specifies to check for group quotas.
> 
> If neither the **-u** or **-g** options are specified, only the user quota file is created. If only **-g** is specified, only the group quota file is created.
> 
> After the files are created, run the following command to generate the table of current disk usage per file system with quotas enabled:
> 
>     # quotacheck -avug
>     
> 
> The options used are as follows:
> 
> *   **a** Check all quota-enabled, locally-mounted file systems 
> *   **v** Display verbose status information as the quota check proceeds 
> *   **u** Check user disk quota information 
> *   **g** Check group disk quota information 
> 
> After **quotacheck** has finished running, the quota files corresponding to the enabled quotas (user and/or group) are populated with data for each quota-enabled locally-mounted file system such as **/home**.

#### Assigning Quotas to Users

> **18&#46;1.4 . Assigning Quotas per User**
> 
> The last step is assigning the disk quotas with the **edquota** command. To configure the quota for a user, as root in a shell prompt, execute the command:
> 
>     # edquota username
>     
> 
> Perform this step for each user who needs a quota. For example, if a quota is enabled in **/etc/fstab** for the /home partition (**/dev/VolGroup00/LogVol02** in the example below) and the command **edquota testuser** is executed, the following is shown in the editor configured as the default for the system:
> 
>     Disk quotas for user testuser (uid 501):
>     Filesystem blocks soft hard inodes soft hard
>     /dev/VolGroup00/LogVol02 440436 0 0 37418 0 0
>     
> 
> The first column is the name of the file system that has a quota enabled for it. The second column shows how many blocks the user is currently using. The next two columns are used to set soft and hard block limits for the user on the file system. The inodes column shows how many inodes the user is currently using. The last two columns are used to set the soft and hard inode limits for the user on the file system.
> 
> The hard block limit is the absolute maximum amount of disk space that a user or group can use. Once this limit is reached, no further disk space can be used.
> 
> The soft block limit defines the maximum amount of disk space that can be used. However, unlike the hard limit, the soft limit can be exceeded for a certain amount of time. That time is known as the **grace** period. The grace period can be expressed in seconds, minutes, hours, days, weeks, or months.
> 
> If any of the values are set to 0, that limit is not set. In the text editor, change the desired limits.
> 
> **Example 18.4 . Change desired limits** For example:
> 
>     Disk quotas for user testuser (uid 501):
>     Filesystem blocks soft hard inodes soft hard
>     /dev/VolGroup00/LogVol02 440436 500000 550000 37418 0 0
>     
> 
> To verify that the quota for the user has been set, use the command:
> 
>     # quota username
>     Disk quotas for user username (uid 501):
>     Filesystem blocks quota limit grace files quota limit grace
>     /dev/sdb 1000* 1000 1000 0 0 0
>     
> 
> **18&#46;1.6. Setting the Grace Period for Soft Limits**
> 
> If a given quota has soft limits, you can edit the grace period (i.e. the amount of time a soft limit can be exceeded) with the following command:
> 
>     # edquota -t
>     
> 
> This command works on quotas for inodes or blocks, for either users or groups.

#### Managing Disk Quotas

> **18&#46;2. Managing Disk Quotas**
> 
> If quotas are implemented, they need some maintenance — mostly in the form of watching to see if the quotas are exceeded and making sure the quotas are accurate.
> 
> Of course, if users repeatedly exceed their quotas or consistently reach their soft limits, a system administrator has a few choices to make depending on what type of users they are and how much disk space impacts their work. The administrator can either help the user determine how to use less disk space or increase the user&#8217;s disk quota.
> 
> **18&#46;2.1. Enabling and Disabling**
> 
> It is possible to disable quotas without setting them to 0. To turn all user and group quotas off, use the following command:
> 
>     # quotaoff -vaug
>     
> 
> If neither the **-u** or **-g** options are specified, only the user quotas are disabled. If only **-g** is specified, only group quotas are disabled. The **-v** switch causes verbose status information to display as the command executes.
> 
> To enable quotas again, use the **quotaon** command with the same options.
> 
> For example, to enable user and group quotas for all file systems, use the following command:
> 
>     # quotaon -vaug
>     
> 
> To enable quotas for a specific file system, such as /home, use the following command:
> 
>     # quotaon -vug /home
>     
> 
> If neither the **-u** or **-g** options are specified, only the user quotas are enabled. If only **-g** is specified, only group quotas are enabled.

#### Reporting Disk Quotas

> **18&#46;2.2. Reporting on Disk Quotas**
> 
> Creating a disk usage report entails running the **repquota** utility.
> 
> **Example 18.5. Output of repquota command**
> 
> For example, the command **repquota /home** produces this output:
> 
>     *** Report for user quotas on device /dev/mapper/VolGroup00-LogVol02
>     Block grace time: 7days; Inode grace time: 7days
>     Block limits File limits
>     User used soft hard grace used soft hard grace
>     ----------------------------------------------------------------------
>     root -- 36 0 0 4 0 0
>     kristin -- 540 0 0 125 0 0
>     testuser -- 440400 500000 550000 37418 0 0
>     
> 
> To view the disk usage report for all (option -a) quota-enabled file systems, use the command:
> 
>     # repquota -a
>     
> 
> While the report is easy to read, a few points should be explained. The **&#8211;** displayed after each user is a quick way to determine whether the block or inode limits have been exceeded. If either soft limit is exceeded, a **+** appears in place of the corresponding **-**; the first **-** represents the block limit, and the second represents the inode limit.

Let&#8217;s go ahead and setup our sdb1 partition to have user quotas. First let&#8217;s remove the encryption from that partition:

    [root@rhel01 ~]# dmsetup ls
    VolGroup-lv_swap    (253:1)
    VolGroup-lv_root    (253:0)
    my_enc_dev  (253:2)
    [root@rhel01 ~]# cryptsetup luksClose my_enc_dev
    [root@rhel01 ~]# dmsetup ls
    VolGroup-lv_swap    (253:1)
    VolGroup-lv_root    (253:0)
    

That looks good. Now let&#8217;s format device as a regular ext3 partition:

    [root@rhel01 ~]# mkfs.ext3 /dev/sdb1
    mke2fs 1.41.12 (17-May-2010)
    Filesystem label=
    OS type: Linux
    Block size=4096 (log=2)
    Fragment size=4096 (log=2)
    Stride=0 blocks, Stripe width=0 blocks
    524288 inodes, 2096896 blocks
    104844 blocks (5.00%) reserved for the super user
    First data block=0
    Maximum filesystem blocks=2147483648
    64 block groups
    32768 blocks per group, 32768 fragments per group
    8192 inodes per group
    Superblock backups stored on blocks:
    32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632
    
    Writing inode tables: done
    Creating journal (32768 blocks): done
    Writing superblocks and filesystem accounting information: done
    
    This filesystem will be automatically checked every 29 mounts or
    180 days, whichever comes first. Use tune2fs -c or -i to override.
    

Let&#8217;s make sure there is not **luks** header left:

    [root@rhel01 ~]# cryptsetup isLuks /dev/sdb1
    Device /dev/sdb1 is not a valid LUKS device.
    

That looks good. Also remove the **/etc/crypttab** file if that was setup. I had setup an entry for this partition in the above examples, and it was still there:

    [root@rhel01 ~]# tail -1 /etc/fstab
    /dev/sdb1 /mnt ext3 defaults 0 0
    

Now let&#8217;s mount that partition:

    [root@rhel01 ~]# mount /mnt
    [root@rhel01 ~]# df -h | grep sdb
    /dev/sdb1 7.9G 147M 7.4G 2% /mnt 
    

That looks good. Here are the mount parameters of the mount-point:

    [root@rhel01 ~]# mount | grep sdb
    /dev/sdb1 on /mnt type ext3 (rw)
    

I then made my **/etc/fstab** entry look like this:

    [root@rhel01 ~]# tail -1 /etc/fstab
    /dev/sdb1 /mnt ext3 defaults,usrquota 0 0
    

Now I remounted the partition and checked the quota parameter was there:

    [root@rhel01 ~]# mount -o remount /mnt
    [root@rhel01 ~]# mount | grep sdb
    /dev/sdb1 on /mnt type ext3 (rw,usrquota)
    

That looked good. Now to create the user quota files:

    [root@rhel01 log]# quotacheck -cuv /mnt
    quotacheck: Your kernel probably supports journaled quota but you are not using it. Consider switching to journaled quota to avoid running quotacheck after an unclean shutdown.
    quotacheck: Scanning /dev/sdb1 [/mnt] done
    quotacheck: Cannot stat old user quota file: No such file or directory
    quotacheck: Old group file not found. Usage will not be substracted.
    quotacheck: Checked 2 directories and 0 files
    quotacheck: Cannot create new quotafile /mnt/aquota.user.new: Permission denied
    quotacheck: Cannot initialize IO on new quotafile: Permission denied
    

Initially it gave me an error. This was due to SELinux, and will be covered in <a href="http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-11-selinux/" onclick="javascript:_gaq.push(['_trackEvent','outbound-article','http://virtuallyhyper.com/2014/03/rhcsa-rhce-chapter-11-selinux/']);">Chapter 11</a>. To fix the issue we can make the context of our **/mnt/** directory the same as of **/var**. Like so:

    [root@rhel01 log]# chcon --reference=/var /mnt 
    

Then after that, it worked:

    [root@rhel01 ~]# quotacheck -cuv /mnt
    quotacheck: Your kernel probably supports journaled quota but you are not using it. Consider switching to journaled quota to avoid running quotacheck after an unclean shutdown.
    quotacheck: Scanning /dev/sdb1 [/mnt] done
    quotacheck: Cannot stat old user quota file: No such file or directory
    quotacheck: Old group file not found. Usage will not be substracted.
    quotacheck: Checked 3 directories and 2 files
    quotacheck: Old file not found.
    

Now to confirm the quota file exist:

    [root@rhel01 ~]# ls -l /mnt
    total 24
    -rw-------. 1 root root 6144 Jan 6 14:04 aquota.user
    drwx------. 2 root root 16384 Jan 6 14:02 lost+found 
    

We can also use **quotaon** to confirm that quota has been enabled on this filesystem:

    [root@rhel01 ~]# quotaon -v /mnt
    /dev/sdb1 [/mnt]: user quotas turned on
    

Now let&#8217;s add a user called user1 and enable quotas to be soft at 20M,hard at 25M, and set the grace period to be 2 days.

    [root@rhel01 ~]# adduser user1
    [root@rhel01 ~]# getent passwd user1
    user1:x:500:500::/home/user1:/bin/bash
    Now let's edit this user's quota: 
    
    [root@rhel01 ~]# edquota user1
    Disk quotas for user user1 (uid 500):
    Filesystem blocks soft hard inodes soft hard
    /dev/sdb1 0 20000 25000 0 0 0
    

After I created some files under /mnt, then checking the quota for the user, I saw the following:

    [root@rhel01 mnt]# quota user1
    Disk quotas for user user1 (uid 500):
    Filesystem blocks quota limit grace files quota limit grace
    /dev/sdb1 4 20000 25000 2 0 0
    

To change the grace period, I did the following:

    [root@rhel01 ~]# edquota -t
    Grace period before enforcing soft limits for users:
    Time units may be: days, hours, minutes, or seconds
    Filesystem Block grace period Inode grace period
    /dev/sdb1 2days 2days
    

So now if I switch user to **user1** and create a 20MB file under /mnt:

    [root@rhel01 ~]# su - user1
    [user1@rhel01 ~]$ cd /mnt/test
    [user1@rhel01 test]$ dd if=/dev/zero of=dd bs=1M count=20
    sdb1: warning, user block quota exceeded.
    20+0 records in
    20+0 records out
    20971520 bytes (21 MB) copied, 0.0733135 s, 286 MB/s
    

We can even see that a warning shows up saying that I have exceeded the soft quota. While I am that user, I can check my own quota:

    [user1@rhel01 test]$ quota
    Disk quotas for user user1 (uid 500):
    Filesystem blocks quota limit grace files quota limit grace
    /dev/sdb1 20508* 20000 25000 47:59 4 0 0
    

Notice the grace column has already started and it&#8217;s at 47:59 hours. So I went over the soft limit, but what will happen if I go over the hard limit. Let&#8217;s create another file with a size of 5MB and that will go above the hard limit:

    [user1@rhel01 test]$ dd if=/dev/zero of=dd2 bs=1M count=5
    sdb1: write failed, user block limit reached.
    dd: writing `dd2': Disk quota exceeded
    5+0 records in
    4+0 records out
    4587520 bytes (4.6 MB) copied, 0.0182964 s, 251 MB/s 
    

This time the operation failed since I went above the hard limit. Checking over the quota as that user:

    [user1@rhel01 test]$ quota
    Disk quotas for user user1 (uid 500):
    Filesystem blocks quota limit grace files quota limit grace
    /dev/sdb1 25000* 20000 25000 47:56 5 0 0
    

We can see that the blocks is the same as limit, indicating that we have gone over the quota. As root running a quota report, I saw the following:

    [root@rhel01 ~]# repquota -v /mnt
    *** Report for user quotas on device /dev/sdb1
    Block grace time: 2days; Inode grace time: 2days
    Block limits File limits
    User used soft hard grace used soft hard grace
    ----------------------------------------------------------------------
    root -- 149628 0 0 4 0 0
    user1 +- 25000 20000 25000 47:55 5 0 0
    
    Statistics:
    Total blocks: 7
    Data blocks: 1
    Entries: 2
    Used average: 2.000000
    

We can again confirm that user1 is over quota.

### File System ACLs

Another function with file systems is advanced ACLs. From the storage guide:

> **Chapter 19. Access Control Lists**
> 
> Files and directories have permission sets for the owner of the file, the group associated with the file, and all other users for the system. However, these permission sets have limitations. For example, different permissions cannot be configured for different users. Thus, Access Control Lists (ACLs) were implemented.
> 
> The Red Hat Enterprise Linux kernel provides ACL support for the ext3 file system and NFS-exported file systems. ACLs are also recognized on ext3 file systems accessed via Samba.
> 
> Along with support in the kernel, the **acl** package is required to implement ACLs. It contains the utilities used to add, modify, remove, and retrieve ACL information. The **cp** and **mv** commands copy or move any ACLs associated with files and directories.

Going down the guide:

> **19&#46;1. Mounting File Systems**
> 
> Before using ACLs for a file or directory, the partition for the file or directory must be mounted with ACL support. If it is a local **ext3** file system, it can mounted with the following command:
> 
>     mount -t ext3 -o acl device-name partition
>     
> 
> For example:
> 
>     mount -t ext3 -o acl /dev/VolGroup00/LogVol02 /work
>     
> 
> Alternatively, if the partition is listed in the **/etc/fstab** file, the entry for the partition can include the **acl** option:
> 
>     LABEL=/work /work ext3 acl 1 2
>     
> 
> If an **ext3** file system is accessed via **Samba** and ACLs have been enabled for it, the ACLs are recognized because Samba has been compiled with the **&#8211;with-acl-support** option. No special flags are required when accessing or mounting a Samba
> 
> **19&#46;1.1. NFS**
> 
> By default, if the file system being exported by an NFS server supports ACLs and he NFS client can read ACLs, ACLs are utilized by the client system.
> 
> To disable ACLs on NFS shares when configuring the server, include the **no_acl** option in the **/etc/exports** file. To disable ACLs on an NFS share when mounting it on a client, mount it with the **no_acl** option via the command line or the **/etc/fstab** file.

#### Setting up ACLs

> **19&#46;2. Setting Access ACLs**
> 
> There are two types of ACLs: access ACLs and default ACLs. An access ACL is the access control list for a specific file or directory. A default ACL can only be associated with a directory; if a file within the directory does not have an access ACL, it uses the rules of the default ACL for the directory. Default ACLs are optional. ACLs can be configured:
> 
> 1.  Per user
> 2.  Per group
> 3.  Via the effective rights mask
> 4.  For users not in the user group for the file 
> 
> The **setfacl** utility sets ACLs for files and directories. Use the **-m** option to add or modify the ACL of a file or directory:
> 
>     # setfacl -m rules files
>     
> 
> Rules (**rules**) must be specified in the following formats. Multiple rules can be specified in the same command if they are separated by commas.
> 
> *   **u:uid:perms** Sets the access ACL for a user. The user name or UID may be specified. The user may be any valid user on the system. 
> *   **g:gid:perms** Sets the access ACL for a group. The group name or GID may be specified. The group may be any valid group on the system. 
> *   **m:perms** Sets the effective rights mask. The mask is the union of all permissions of the owning group and all of the user and group entries. 
> *   **o:perms** Sets the access ACL for users other than the ones in the group for the file. 
> 
> Permissions (**perms**) must be a combination of the characters **r**, **w**, and **x** for read, write, and execute.
> 
> If a file or directory already has an ACL, and the **setfacl** command is used, the additional rules are added to the existing ACL or the existing rule is modified.
> 
> **Example 19.1. Give read and write permissions**
> 
> For example, to give read and write permissions to user andrius:
> 
>     # setfacl -m u:andrius:rw /project/somefile
>     
> 
> To remove all the permissions for a user, group, or others, use the **-x** option and do not specify any permissions:
> 
>     # setfacl -x rules files
>     
> 
> **Example 19.2. Remove all permissions**
> 
> For example, to remove all permissions from the user with UID 500:
> 
>     # setfacl -x u:500 /project/somefile
>     
> 
> **19&#46;3. Setting Default ACLs**
> 
> To set a default ACL, add d: before the rule and specify a directory instead of a file name.
> 
> **Example 19.3. Setting default ACLs**
> 
> For example, to set the default ACL for the **/share/** directory to read and execute for users not in the user group (an access ACL for an individual file can override it):
> 
>      # setfacl -m d:o:rx /share
>     

#### Retrieving ACLs

> **19&#46;4. Retrieving ACLs**
> 
> To determine the existing ACLs for a file or directory, use the **getfacl** command. In the example below, the **getfacl** is used to determine the existing ACLs for a file.
> 
> **Example 19.4 . Retrieving ACLs**
> 
>     # getfacl home/john/picture.png
>     
> 
> The above command returns the following output:
> 
>     # file: home/john/picture.png
>     # owner: john
>     # group: john
>     user::rw
>     group::r--
>     other::r--
>     
> 
> If a directory with a default ACL is specified, the default ACL is also displayed as illustrated below. For example, **getfacl home/sales/** will display similar output:
> 
>     # file: home/sales/
>     # owner: john
>     # group: john
>     user::rwuser:barryg:r--
>     group::r--
>     mask::r--
>     other::r--
>     default:user::rwx
>     default:user:john:rwx
>     default:group::r-x
>     default:mask::rwx
>     default:other::r-x
>     

Let&#8217;s try this out, let&#8217;s mount our **sdb1** partition with the **acl** flag and then create a file with the user root and then add ACLs to allow user1 to edit the same file. To mount the partition with **acl** support I added the following to my **/etc/fstab** entry:

    [root@rhel01 ~]# tail -1 /etc/fstab
    /dev/sdb1 /mnt ext3 defaults,usrquota,acl 0 0
    

Now to remount the file system to enable the new ACL functions:

    [root@rhel01 ~]# mount -o remount /mnt
    [root@rhel01 ~]# mount | grep sdb
    /dev/sdb1 on /mnt type ext3 (rw,usrquota,acl)
    

That looks good. Now as root let&#8217;s create a file and check out it&#8217;s permissions:

    [root@rhel01 ~]# cd /mnt
    [root@rhel01 mnt]# touch root_file
    [root@rhel01 mnt]# ls -l root_file
    -rw-r--r--. 1 root root 0 Jan 6 18:13 root_file
    

Now checking it&#8217;s ACLs, I see the following:

    [root@rhel01 mnt]# getfacl root_file
    # file: root_file
    # owner: root
    # group: root
    user::rw-
    group::r--
    other::r--
    

So only root can write to that file, let&#8217;s try writing data to file as root and then as user user1:

    [root@rhel01 mnt]# echo test >> /tmp/root_file
    [root@rhel01 mnt]# cat /mnt/root_file
    test
    [root@rhel01 mnt]# su - user1
    [user1@rhel01 ~]$ echo test2 >> /mnt/root_file
    -bash: /mnt/root_file: Permission denied
    

We can see that user1 cannot edit the file. Now let&#8217;s enable user1 to be able to write to that file with ACLs with root:

    [root@rhel01 mnt]# setfacl -m u:user1:rw /mnt/root_file
    [root@rhel01 mnt]# getfacl /mnt/root_file
    # file: tmp/root_file
    # owner: root
    # group: root
    user::rw-
    user:user1:rw-
    group::r--
    mask::rw-
    other::r--
    

Now let&#8217;s switch user to user1 and try to edit the file:

    [user1@rhel01 ~]$ echo test2 >> /mnt/root_file
    [user1@rhel01 ~]$ cat /mnt/root_file
    test
    test2
    

If you want to remove those permissions for user1 we can do the following:

    [root@rhel01 ~]# setfacl -x u:user1 /mnt/root_file
    [root@rhel01 ~]# getfacl /mnt/root_file
    # file: tmp/root_file
    # owner: root
    # group: root
    user::rw-
    group::r--
    mask::r--
    other::r--
    

<p class="wp-flattr-button">
  <a class="FlattrButton" style="display:none;" href="http://virtuallyhyper.com/2013/01/rhcsa-and-rhce-chapter-4-file-systems-and-such/" title=" RHCSA and RHCE Chapter 4 File Systems and Such" rev="flattr;uid:virtuallyhyper;language:en_GB;category:text;tags:/dev/urandom,/etc/fstab,/etc/mtab,/proc/mounts,badblocks,blkid,cryptsetup,dd,df,dumpe2fs,e2label,edquota,ext2,ext3,filesystem,findmnt,getfacl,luks,mkfs,mount,quota,quotacheck,quotaoff,quotaon,repquota,setfacl,usrquota,blog;button:compact;">File Systems After we have partitioned our drives to our heart&#8217;s desire, we should actually start using them. The first thing that we need to do is put a file...</a>
</p>