---
title: RHCSA and RHCE Chapter 2 System Initialization
author: Karim Elatov
layout: post
permalink: /2013/01/rhcsa-and-rhce-chapter-2-system-initialization/
dsq_thread_id:
  - 1404673723
categories: ['home_lab', 'os','certifications', 'rhcsa_rhce']
tags: ['mbr', 'linux','grub', 'inittab', 'rc_local', 'linux_rescue', 'sysv']
---

### Red Hat Boot Process

The process is described in "[Red Hat Enterprise Linux 6 Installation Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf)":

> **F.2. A Detailed Look at the Boot Process**
>
> The beginning of the boot process varies depending on the hardware platform being used. However, once the kernel is found and loaded by the boot loader, the default boot process is identical across all architectures. This chapter focuses primarily on the x86 architecture.
>
> **F.2.1. The firmware interface**
>
> **F.2.1.1. BIOS-based x86 systems**
>
> The Basic Input/Output System (BIOS) is a firmware interface that controls not only the first step of the boot process, but also provides the lowest level interface to peripheral devices. On x86 systems equipped with BIOS, the program is written into read-only, permanent memory and is always available for use. When the system boots, the processor looks at the end of system memory for the BIOS program, and runs it.
>
> Once loaded, the BIOS tests the system, looks for and checks peripherals, and then locates a valid device with which to boot the system. Usually, it checks any optical drives or USB storage devices present for bootable media, then, failing that, looks to the system's hard drives. In most cases, the order of the drives searched while booting is controlled with a setting in the BIOS, and it looks on the master IDE on the primary IDE bus or for a SATA device with a boot flag set. The BIOS then loads into memory whatever program is residing in the first sector of this device, called the Master Boot Record (MBR). The MBR is only 512 bytes in size and contains machine code instructions for booting the machine, called a boot loader, along with the partition table. Once the BIOS finds and loads the boot loader program into memory, it yields control of the boot process to it.
>
> This first-stage boot loader is a small machine code binary on the MBR. Its sole job is to locate the second stage boot loader (GRUB) and load the first part of it into memory.
>
> **F.2.1.2. UEFI-based x86 systems**
>
> The Unified Extensible Firmware Interface (UEFI) is designed, like BIOS, to control the boot process (through boot services) and to provide an interface between system firmware and an operating system (through runtime services). Unlike BIOS, it features its own architecture, independent of the CPU, and its own device drivers. UEFI can mount partitions and read certain file systems.
>
> When an x86 computer equipped with UEFI boots, the interface searches the system storage for a partition labeled with a specific globally unique identifier (GUID) that marks it as the EFI System Partition (ESP). This partition contains applications compiled for the EFI architecture, which might include bootloaders for operating systems and utility software. UEFI systems include an EFI boot manager that can boot the system from a default configuration, or prompt a user to choose an operating system to boot. When a bootloader is selected, manually or automatically, UEFI reads it into memory and yields control of the boot process to it.

### Boot Loader

From the same guide:

> **F.2.2. The Boot Loader**
> **F.2.2.1. The GRUB boot loader for x86 systems**
>
> The system loads GRUB into memory, as directed by either a first-stage bootloader in the case of systems equipped with BIOS, or read directly from an EFI System Partition in the case of systems equipped with UEFI.
>
> GRUB has the advantage of being able to read ext2, ext3, and ext4 partitions and load its configuration file — **/boot/grub/grub.conf** (for BIOS) or **/boot/efi/EFI/redhat/grub.conf** (for UEFI) — at boot time.
>
> Once the second stage boot loader is in memory, it presents the user with a graphical screen showing the different operating systems or kernels it has been configured to boot (when you update the kernel, the boot loader configuration file is updated automatically). On this screen a user can use the arrow keys to choose which operating system or kernel they wish to boot and press Enter. If no key is pressed, the boot loader loads the default selection after a configurable period of time has passed.
>
> Once the second stage boot loader has determined which kernel to boot, it locates the corresponding kernel binary in the **/boot/** directory. The kernel binary is named using the following format — **/boot/vmlinuz-kernel-version** file (where **kernel-version** corresponds to the kernel version specified in the boot loader's settings).
>
> The boot loader then places one or more appropriate **initramfs** images into memory. The **initramfs** is used by the kernel to load drivers and modules necessary to boot the system. This is particularly important if SCSI hard drives are present or if the systems use the ext3 or ext4 file system.
>
> Once the kernel and the **initramfs** image(s) are loaded into memory, the boot loader hands control of the boot process to the kernel.

At this point the kernel takes over:

> **F.2.3. The Kernel**
>
> When the kernel is loaded, it immediately initializes and configures the computer's memory and configures the various hardware attached to the system, including all processors, I/O subsystems, and storage devices. It then looks for the compressed **initramfs** image(s) in a predetermined location in memory, decompresses it directly to **/sysroot/**, and loads all necessary drivers. Next, it initializes virtual devices related to the file system, such as LVM or software RAID, before completing the **initramfs** processes and freeing up all the memory the disk image once occupied.
>
> The kernel then creates a root device, mounts the root partition read-only, and frees any unused memory.
>
> At this point, the kernel is loaded into memory and operational. However, since there are no user applications that allow meaningful input to the system, not much can be done with the system. To set up the user environment, the kernel executes the **/sbin/init** program

### /sbin/init

And then the init process starts:

> **F.2.4 . The /sbin/init Program**
>
> The **/sbin/init** program (also called **init**) coordinates the rest of the boot process and configures the environment for the user.
>
> When the **init** command starts, it becomes the parent or grandparent of all of the processes that start up automatically on the system. First, it runs the **/etc/rc.d/rc.sysinit** script, which sets the environment path, starts swap, checks the file systems, and executes all other steps required for system initialization. For example, most systems use a clock, so **rc.sysinit** reads the **/etc/sysconfig/clock** configuration file to initialize the hardware clock. Another example is if there are special serial port processes which must be initialized, **rc.sysinit** executes the **/etc/rc.serial** file.
>
> The **init** command then processes the jobs in the **/etc/event.d** directory, which describe how the system should be set up in each SysV init runlevel. Runlevels are a state, or mode, defined by the services listed in the SysV **/etc/rc.d/rcX.d/** directory, where **X** is the number of the runlevel.
>
> Next, the init command sets the source function library, **/etc/rc.d/init.d/functions**, for the system, which configures how to start, kill, and determine the PID of a program.
>
> The init program starts all of the background processes by looking in the appropriate rc directory for the runlevel specified as the default in **/etc/inittab**. The rc directories are numbered to correspond to the runlevel they represent. For instance, **/etc/rc.d/rc5.d/** is the directory for runlevel 5.
>
> When booting to runlevel 5, the **init** program looks in the **/etc/rc.d/rc5.d/** directory to determine which processes to start and stop.

Here is what I saw in my system:

    [root@rhel01 rc5.d]# ls -l
    total 0
    lrwxrwxrwx. 1 root root 19 Dec 27 17:52 K10saslauthd -> ../init.d/saslauthd
    lrwxrwxrwx. 1 root root 20 Dec 27 17:52 K50netconsole -> ../init.d/netconsole
    lrwxrwxrwx. 1 root root 21 Dec 27 17:52 K87restorecond -> ../init.d/restorecond
    lrwxrwxrwx. 1 root root 15 Dec 27 17:51 K89rdisc -> ../init.d/rdisc
    lrwxrwxrwx. 1 root root 22 Dec 27 17:56 S02lvm2-monitor -> ../init.d/lvm2-monitor
    lrwxrwxrwx. 1 root root 19 Dec 27 17:50 S08ip6tables -> ../init.d/ip6tables
    lrwxrwxrwx. 1 root root 18 Dec 27 17:49 S08iptables -> ../init.d/iptables
    lrwxrwxrwx. 1 root root 17 Dec 27 17:52 S10network -> ../init.d/network
    lrwxrwxrwx. 1 root root 16 Dec 27 17:56 S11auditd -> ../init.d/auditd
    lrwxrwxrwx. 1 root root 17 Dec 27 17:52 S12rsyslog -> ../init.d/rsyslog
    lrwxrwxrwx. 1 root root 15 Dec 27 17:52 S25netfs -> ../init.d/netfs
    lrwxrwxrwx. 1 root root 19 Dec 27 17:52 S26udev-post -> ../init.d/udev-post
    lrwxrwxrwx. 1 root root 14 Dec 27 17:56 S55sshd -> ../init.d/sshd
    lrwxrwxrwx. 1 root root 17 Dec 27 17:52 S80postfix -> ../init.d/postfix
    lrwxrwxrwx. 1 root root 15 Dec 27 17:52 S90crond -> ../init.d/crond
    lrwxrwxrwx. 1 root root 15 Dec 27 17:53 S97rhnsd -> ../init.d/rhnsd
    lrwxrwxrwx. 1 root root 19 Dec 27 17:56 S97rhsmcertd -> ../init.d/rhsmcertd
    lrwxrwxrwx. 1 root root 11 Dec 27 17:52 S99local -> ../rc.local


and here is my default init level:

    [root@rhel01 ~]# tail -1 /etc/inittab
    id:3:initdefault:


More information from the above guide:

> As illustrated in this listing, none of the scripts that actually start and stop the services are located in the **/etc/rc.d/rc5.d/** directory. Rather, all of the files in **/etc/rc.d/rc5.d/** are symbolic links pointing to scripts located in the **/etc/rc.d/init.d/** directory. Symbolic links are used in each of the rc directories so that the runlevels can be reconfigured by creating, modifying, and deleting the symbolic links without affecting the actual scripts they reference.
>
> The name of each symbolic link begins with either a **K** or an **S**. The **K** links are processes that are killed on that runlevel, while those beginning with an **S** are started.
>
> The **init** command first stops all of the **K** symbolic links in the directory by issuing the **/etc/rc.d/init.d/command stop** command, where **command** is the process to be killed. It then starts all of the **S** symbolic links by issuing **/etc/rc.d/init.d/command start**.
>
> Each of the symbolic links are numbered to dictate start order. The order in which the services are started or stopped can be altered by changing this number. The lower the number, the earlier it is started. Symbolic links with the same number are started alphabetically.
>
> After the **init** command has progressed through the appropriate rc directory for the runlevel, **Upstart** forks an **/sbin/mingetty** process for each virtual console (login prompt) allocated to the runlevel by the job definition in the **/etc/event.d** directory. Runlevels 2 through 5 have all six virtual consoles, while runlevel 1 (single user mode) has one, and runlevels 0 and 6 have none. The **/sbin/mingetty** process opens communication pathways to tty devices, sets their modes, prints the login prompt, accepts the user's username and password, and initiates the login process.
>
> In runlevel 5, **Upstart** runs a script called **/etc/X11/prefdm**. The **prefdm** script executes the preferred X display manager — **gdm**, **kdm**, or **xdm**, depending on the contents of the **/etc/sysconfig/desktop** file. Once finished, the system operates on runlevel 5 and displays a login screen.
>
> **F.2.5. Job definitions**
>
> Previously, the sysvinit package provided the init daemon for the default configuration. When the system started, this **init** daemon ran the **/etc/inittab** script to start system processes defined for each runlevel. The default configuration now uses an event-driven init daemon provided by the Upstart package. Whenever particular events occur, the init daemon processes jobs stored in the **/etc/event.d** directory. The **init** daemon recognizes the start of the system as such an event.
>
> Each job typically specifies a program, and the events that trigger **init** to run or to stop the program. Some jobs are constructed as tasks, which perform actions and then terminate until another event triggers the job again. Other jobs are constructed as services, which **init** keeps running until another event (or the user) stops it.
>
> For example, the **/etc/events.d/tty2** job is a service to maintain a virtual terminal on **tty2** from the time that the system starts until the system shuts down, or another event (such as a change in runlevel) stops the job. The job is constructed so that **init** will restart the virtual terminal if it stops unexpectedly during that time:
>
>     # tty2 - getty
>     #
>     # This service maintains a getty on tty2 from the point the system is
>     # started until it is shut down again.
>     start on stopped rc2
>     start on stopped rc3
>     start on stopped rc4
>     start on started prefdm
>     stop on runlevel 0
>     stop on runlevel 1
>     stop on runlevel 6
>     respawn
>     exec /sbin/mingetty tty2
>

#### rc.local

> **F.3. Running Additional Programs at Boot Time**
>
> The **/etc/rc.d/rc.local** script is executed by the init command at boot time or when changing runlevels. Adding commands to the bottom of this script is an easy way to perform necessary tasks like starting special services or initialize devices without writing complex initialization scripts in the **/etc/rc.d/init.d/** directory and creating symbolic links.

#### SysV Init RunLevels

> **F.4. SysV Init Runlevels**
>
> The SysV init runlevel system provides a standard process for controlling which programs **init** launches or halts when initializing a runlevel. SysV init was chosen because it is easier to use and more flexible than the traditional BSD-style init process.
>
> The configuration files for SysV init are located in the /etc/rc.d/ directory. Within this directory, are the **rc**, **rc.local**, **rc.sysinit**, and, optionally, the **rc.serial** scripts as well as the following directories:
>
>     init.d/ rc0.d/ rc1.d/ rc2.d/ rc3.d/ rc4.d/ rc5.d/ rc6.d/
>
>
> The **init.d/** directory contains the scripts used by the **/sbin/init** command when controlling services. Each of the numbered directories represent the six runlevels configured by default under Red Hat Enterprise Linux.
>
> **F.4 .1. Runlevels**
>
> The idea behind SysV init runlevels revolves around the idea that different systems can be used in different ways. For example, a server runs more efficiently without the drag on system resources created by the X Window System. Or there may be times when a system administrator may need to operate the system at a lower runlevel to perform diagnostic tasks, like fixing disk corruption in **runlevel 1**.
>
> The characteristics of a given runlevel determine which services are halted and started by **init**. For instance, runlevel 1 (single user mode) halts any network services, while runlevel 3 starts these services. By assigning specific services to be halted or started on a given runlevel, **init** can quickly change the mode of the machine without the user manually stopping and starting services. The following runlevels are defined by default under Red Hat Enterprise Linux:
>
> *   **** — Halt
> *   **1** — Single-user text mode
> *   **2** — Not used (user-definable)
> *   **3** — Full multi-user text mode
> *   **4** — Not used (user-definable)
> *   **5** — Full multi-user graphical mode (with an X-based login screen)
> *   **6** — Reboot
>
> In general, users operate Red Hat Enterprise Linux at runlevel 3 or runlevel 5 — both full multi-user modes. Users sometimes customize runlevels 2 and 4 to meet specific needs, since they are not used. The default runlevel for the system is listed in **/etc/inittab**. To find out the default runlevel for a system, look for the line similar to the following near the bottom of **/etc/inittab**:
>
>     id:5:initdefault:
>
>
> The default runlevel listed in this example is five, as the number after the first colon indicates. To change it, edit **/etc/inittab** as root.

As seen above my default runlevel is 3. You can also run the following commands to check your current runlevel:

    [root@rhel01 ~]# who -r
    run-level 3 2012-12-28 12:44


and also this:

    [root@rhel01 ~]# runlevel -v
    N 3


### RunLevel Utilities

Here are some utilities to configure runlevels and services:

> **F.4 .2. Runlevel Utilities**
>
> One of the best ways to configure runlevels is to use an **initscript** utility. These tools are designed to simplify the task of maintaining files in the SysV init directory hierarchy and relieves system administrators from having to directly manipulate the numerous symbolic links in the subdirectories of **/etc/rc.d/**.
>
> Red Hat Enterprise Linux provides three such utilities:
>
> *   **/sbin/chkconfig** — The **/sbin/chkconfig** utility is a simple command line tool for maintaining the** /etc/rc.d/init.d/** directory hierarchy.
> *   **/usr/sbin/ntsysv** — The ncurses-based /sbin/ntsysv utility provides an interactive text-based interface, which some find easier to use than **chkconfig**.
> *   Services Configuration Tool — The graphical **Services Configuration Tool** (**system-config-services**) program is a flexible utility for configuring runlevels.

Here is a list of all the services on my machine and which runlevel they start up on:

    [root@rhel01 ~]# chkconfig --list
    auditd 0:off    1:off   2:on    3:on    4:on    5:on    6:off
    crond 0:off 1:off   2:on    3:on    4:on    5:on    6:off
    ip6tables 0:off 1:off   2:on    3:on    4:on    5:on    6:off
    iptables 0:off  1:off   2:on    3:on    4:on    5:on    6:off
    lvm2-monitor 0:off  1:on    2:on    3:on    4:on    5:on    6:off
    netconsole 0:off    1:off   2:off   3:off   4:off   5:off   6:off
    netfs 0:off 1:off   2:off   3:on    4:on    5:on    6:off
    network 0:off   1:off   2:on    3:on    4:on    5:on    6:off
    postfix 0:off   1:off   2:on    3:on    4:on    5:on    6:off
    rdisc 0:off 1:off   2:off   3:off   4:off   5:off   6:off
    restorecond 0:off   1:off   2:off   3:off   4:off   5:off   6:off
    rhnsd 0:off 1:off   2:on    3:on    4:on    5:on    6:off
    rhsmcertd 0:off 1:off   2:off   3:on    4:on    5:on    6:off
    rsyslog 0:off   1:off   2:on    3:on    4:on    5:on    6:off
    saslauthd 0:off 1:off   2:off   3:off   4:off   5:off   6:off
    sshd 0:off  1:off   2:on    3:on    4:on    5:on    6:off
    udev-post 0:off 1:on    2:on    3:on    4:on    5:on    6:off


To change any of the above settings we can check out the help page:

    [root@rhel01 ~]# chkconfig --help
    chkconfig version 1.3.49.3 - Copyright (C) 1997-2000 Red Hat, Inc.
    This may be freely redistributed under the terms of the GNU Public License.

    usage: chkconfig [--list] [--type <type>] [name]
    chkconfig --add <name>
    chkconfig --del <name>
    chkconfig --override <name>
    chkconfig [--level <levels>] [--type <type>] <name> <on|off|reset|resetpriorities>


And lastly here is a way to shutdown a RHEL machine:

> **F.5. Shutting Down**
>
> To shut down Red Hat Enterprise Linux, the root user may issue the **/sbin/shutdown** command. The shutdown man page has a complete list of options, but the two most common uses are:
>
>     /sbin/shutdown -h now
>
>
> and
>
>     /sbin/shutdown -r now
>
>
> After shutting everything down, the -h**strong text** option halts the machine, and the **-r** option reboots. PAM console users can use the **reboot** and **halt** commands to shut down the system while in runlevels 1 through 5

### GRUB

Here is more information regarding GRUB:

> **E.7. GRUB Menu Configuration File**
>
> The configuration file (**/boot/grub/grub.conf**), which is used to create the list of operating systems to boot in GRUB's menu interface, essentially allows the user to select a pre-set group of commands to execute.
>
> **E.7.1. Configuration File Structure**
>
> The GRUB menu interface configuration file is **/boot/grub/grub.conf**. The commands to set the global preferences for the menu interface are placed at the top of the file, followed by stanzas for each operating kernel or operating system listed in the menu. The following is a very basic GRUB menu configuration file designed to boot either Red Hat Enterprise Linux or Microsoft Windows Vista:
>
>     default=0
>     timeout=10
>     splashimage=(hd0,0)/grub/splash.xpm.gz
>     hiddenmenu
>     title Red Hat Enterprise Linux Server (2.6.32.130.el6.i686)
>     root (hd0,0)
>     kernel /boot/vmlinuz-2.6.32.130.el6.i686 ro root=LABEL=/1 rhgb quiet
>     initrd /boot/initrd-2.6.32.130.el6.i686.img
>
>     # section to load Windows
>     title Windows
>     rootnoverify (hd0,0)
>     chainloader +1
>
>
> This file configures GRUB to build a menu with Red Hat Enterprise Linux as the default operating system and sets it to **autoboot** after 10 seconds. Two sections are given, one for each operating system entry, with commands specific to the system disk partition table.
>
> **E.7.2. Configuration File Directives**
>
> The following are directives commonly used in the GRUB menu configuration file:
>
> *   **chainloader** **/path/to/file** — Loads the specified file as a chain loader. Replace **/path/to/file** with the absolute path to the chain loader. If the file is located on the first sector of the specified partition, use the blocklist notation, +1.
> *   **color** **normal-color** **selected-color** — Allows specific colors to be used in the menu, where two colors are configured as the foreground and background. Use simple color names such as red/black.
> *   **default**=**integer** — Replace **integer** with the default entry title number to be loaded if the menu interface times out
> *   **fallback=integer** — Replace **integer** with the entry title number to try if the first attempt fails.
> *   **hiddenmenu** — Prevents the GRUB menu interface from being displayed, loading the **default** entry when the **timeout** period expires. The user can see the standard GRUB menu by pressing the **Esc** key.
> *   **initrd /path/to/initrd** — Enables users to specify an initial RAM disk to use when booting. Replace **/path/to/initrd** with the absolute path to the initial RAM disk.
> *   **kernel /path/to/kernel option-1 option-N** — Specifies the kernel file to load when booting the operating system. Replace **/path/to/kernel** with an absolute path from the partition specified by the root directive. Multiple options can be passed to the kernel when it is loaded. These options include:
>
>     *   **rhgb** (Red Hat graphical boot) — displays an animation during the boot process, rather than lines of text.
>     *   **quiet** — suppresses all but the most important messages in the part of the boot sequence before the Red Hat graphical boot animation begins.
>
> *   **password=password** — Prevents a user who does not know the password from editing the entries for this menu option
>
> *   **map** — Swaps the numbers assigned to two hard drives. For example:
>
>         map (hd0) (hd3)
>         map (hd3) (hd0)
>
>
>     assigns the number 0 to the fourth hard drive, and the number 3 to the first hard drive. This option is especially useful if you configure your system with an option to boot a Windows operating system, because the Windows boot loader must find the Windows installation on the first hard drive. For example, if your Windows installation is on the fourth hard drive, the following entry in grub.conf will allow the Windows boot loader to load Windows correctly:
>
>         title Windows
>         map (hd0) (hd3)
>         map (hd3) (hd0)
>         rootnoverify (hd3,0)
>         chainloader +1
>
>
> *   **root (device-type><device-number,partition)** — Configures the root partition for GRUB, such as **(hd0,0)**, and mounts the partition.
>
> *   **rootnoverify (device-type><device-number,partition)** — Configures the root partition for GRUB, just like the root command, but does not mount the partition.
> *   **timeout=integer** — Specifies the interval, in seconds, that GRUB waits before loading the entry designated in the **default** command.
> *   **splashimage=path-to-image** — Specifies the location of the splash screen image to be used when GRUB boots.
> *   **title group-title** — Specifies a title to be used with a particular group of commands used to load a kernel or operating system.

There is a pretty good article from the Red Hat Magazine: "[Using GRUB to overcome boot problems](http://magazine.redhat.com/2007/03/21/using-grub-to-overcome-boot-problems/)" and in the comments there is an example of how to re-install grub if ever needed. Boot from a cd and type in '**linux rescue**' after the cd boots, you will have a shell from which you can re-install grub to fix any MBR issues that you may have. Here is how that looks like:

    # grub
    Probing devices to guess BIOS drives. This may take a long time.

    GNU GRUB version 0.97 (640K lower / 3072K upper memory)

    [ Minimal BASH-like line editing is supported. For the first word, TAB
    lists possible command completions. Anywhere else TAB lists the possible
    completions of a device/filename.]

    grub> root (hd0,0)
    root (hd0,0)
    Filesystem type is ext2fs, partition type 0x83
    grub> find /grub/grub.conf
    find /grub/grub.conf
    (hd0,0)
    grub> setup (hd0)
    setup (hd0)
    Checking if "/boot/grub/stage1" exists... no
    Checking if "/grub/stage1" exists... yes
    Checking if "/grub/stage2" exists... yes
    Checking if "/grub/e2fs_stage1_5" exists... yes
    Running "embed /grub/e2fs_stage1_5 (hd0)"... 27 sectors are embedded.
    succeeded
    Running "install /grub/stage1 (hd0) (hd0)1+27 p (hd0,0)/grub/stage2 /grub/grub.conf"... succeeded
    Done.


The first command sets up what device to be used as root. The second command confirms that our device contains the grub.conf file which usually means it will contain the other stage files as well. And lastly the '**setup**' command actually installs grub onto that device. Here is a similar process from the guide:

> **36.1.2.1. Reinstalling the Boot Loader**
>
> In many cases, the GRUB boot loader can mistakenly be deleted, corrupted, or replaced by other operating systems. The following steps detail the process on how GRUB is reinstalled on the master boot record:
>
> *   Boot the system from an installation boot medium.
> *   Type** linux rescue** at the installation boot prompt to enter the rescue environment.
> *   Type **chroot /mnt/sysimage** to mount the root partition.
> *   Type **/sbin/grub-install bootpart** to reinstall the GRUB boot loader, where **bootpart** is the boot partition (typically, /dev/sda).
> *   Review the **/boot/grub/grub.conf** file, as additional entries may be needed for GRUB to control additional operating systems.
> *   Reboot the system. Here are instructions on how to boot into different modes:

### Booting into Different Modes

> **36.1.3. Booting into Single-User Mode**
>
> One of the advantages of single-user mode is that you do not need a boot CD-ROM; however, it does not give you the option to mount the file systems as read-only or not mount them at all.
>
> If your system boots, but does not allow you to log in when it has completed booting, try single-user mode.
>
> In single-user mode, your computer boots to runlevel 1. Your local file systems are mounted, but your network is not activated. You have a usable system maintenance shell. Unlike rescue mode, single-user mode automatically tries to mount your file system. Do not use single-user mode if your file system cannot be mounted successfully. You cannot use single-user mode if the runlevel 1 configuration on your system is corrupted. On an x86 system using GRUB, use the following steps to boot into single-user mode:
>
> 1.  At the GRUB splash screen at boot time, press any key to enter the GRUB interactive menu.
> 2.  Select **Red Hat Enterprise Linux** with the version of the kernel that you wish to boot and type a to append the line.
> 3.  Go to the end of the line and type **single** as a separate word (press the **Spacebar** and then type **single**). Press **Enter** to exit edit mode.

And here is emergency mode:

> **36.1.4 . Booting into Emergency Mode**
>
> In emergency mode, you are booted into the most minimal environment possible. The root file system is mounted read-only and almost nothing is set up. The main advantage of emergency mode over single user mode is that the init files are not loaded. If init is corrupted or not working, you can still mount file systems to recover data that could be lost during a re-installation.
>
> To boot into emergency mode, use the same method as described for single-user mode, with one exception, replace the keyword **single** with the keyword **emergency**.

### Grub Example

Let's add an entry to our **grub.conf** menu to have a new entry for recovery mode, but leave the regular mode as the default boot mode. Here is what I had from the default install for my **grub.conf** file:

    [root@rhel1 ~]# cat /boot/grub/grub.conf
    # grub.conf generated by anaconda
    #
    # Note that you do not have to rerun grub after making changes to this file
    # NOTICE: You have a /boot partition. This means that
    # all kernel and initrd paths are relative to /boot/, eg.
    # root (hd0,0)
    # kernel /vmlinuz-version ro root=/dev/mapper/VolGroup-lv_root
    # initrd /initrd-[generic-]version.img
    #boot=/dev/sda
    default=0
    timeout=5
    splashimage=(hd0,0)/grub/splash.xpm.gz
    hiddenmenu
    title Red Hat Enterprise Linux (2.6.32-131.0.15.el6.i686)
    root (hd0,0)
    kernel /vmlinuz-2.6.32-131.0.15.el6.i686 ro root=/dev/mapper/VolGroup-lv_root rd_LVM_LV=VolGroup/lv_root rd_LVM_LV=VolGroup/lv_swap rd_NO_LUKS rd_NO_MD rd_NO_DM LANG=en_US.UTF-8 SYSFONT=latarcyrheb-sun16 KEYBOARDTYPE=pc KEYTABLE=us nomodeset crashkernel=auto quiet
    initrd /initramfs-2.6.32-131.0.15.el6.i686.img


Here is entry that I added:

    title Red Hat Enterprise Linux Single UserMode (2.6.32-131.0.15.el6.i686)
    root (hd0,0)
    kernel /vmlinuz-2.6.32-131.0.15.el6.i686 ro root=/dev/mapper/VolGroup-lv_root rd_LVM_LV=VolGroup/lv_root rd_LVM_LV=VolGroup/lv_swap rd_NO_LUKS rd_NO_MD rd_NO_DM LANG=en_US.UTF-8 SYSFONT=latarcyrheb-sun16 KEYBOARDTYPE=pc KEYTABLE=us nomodeset crashkernel=auto quiet single
    initrd /initramfs-2.6.32-131.0.15.el6.i686.img


To the bottom of the file. After I rebooted I saw the following on my GRUB Menu:

![grub with single RHCSA and RHCE Chapter 2 System Initialization](https://github.com/elatov/uploads/raw/master/2013/01/grub_with_single.png)

Selecting that entry from GRUB yielded in the OS booting into *single* user mode, like so:

![boot single user mode RHCSA and RHCE Chapter 2 System Initialization](https://github.com/elatov/uploads/raw/master/2013/01/boot_single_user_mode.png)

Another thing that was mentioned thought the guide is **Upstart**. RHEL 6 doesn't have that many service converted to that, but to list the services that are using Upstart to start up you can do the following:

    [root@rhel01 ~]# initctl list
    rc stop/waiting
    tty (/dev/tty3) start/running, process 1339
    tty (/dev/tty2) start/running, process 1337
    tty (/dev/tty1) start/running, process 1335
    tty (/dev/tty6) start/running, process 1352
    tty (/dev/tty5) start/running, process 1343
    tty (/dev/tty4) start/running, process 1341
    plymouth-shutdown stop/waiting
    control-alt-delete stop/waiting
    rcS-emergency stop/waiting
    kexec-disable stop/waiting
    quit-plymouth stop/waiting
    rcS stop/waiting
    prefdm stop/waiting
    init-system-dbus stop/waiting
    splash-manager stop/waiting
    start-ttys stop/waiting
    rcS-sulogin stop/waiting
    serial stop/waiting


