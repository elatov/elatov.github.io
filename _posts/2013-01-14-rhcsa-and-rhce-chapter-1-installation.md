---
title: 'RHCSA and RHCE Chapter 1 - Installation'
author: Karim Elatov
layout: post
permalink: /2013/01/rhcsa-and-rhce-chapter-1-installation/
categories: ['storage', 'networking', 'certifications', 'home_lab', 'rhcsa_rhce']
tags: ['grub', 'rhel', 'linux', 'mbr']
---

There is a lot of good information in "[Red Hat Enterprise Linux 6 Installation Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Installation_Guide/Red_Hat_Enterprise_Linux-6-Installation_Guide-en-US.pdf)". From that Guide:

> **9.3. Welcome to Red Hat Enterprise Linux**
>
> The Welcome screen does not prompt you for any input.
>
> ![rhel6 welcome screen RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_welcome_screen.png)
>
> Click on the **Next** button to continue.
>
> **9.4. Language Selection**
>
> Using your mouse, select the language (for example, U.S. English) you would prefer to use for the installation and as the system default (refer to the figure below).
>
> Once you have made your selection, click **Next** to continue.
>
> ![rhel6 language selection RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_language_selection.png)
>
> **9.5. Keyboard Configuration**
>
> Using your mouse, select the correct layout type (for example, U.S. English) for the keyboard you would prefer to use for the installation and as the system default (refer to the figure below).
>
> Once you have made your selection, click **Next** to continue.
>
> ![rhel6 keyboard configuration RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_keyboard_configuration.png)
>
> **9.6. Storage Devices**
>
> You can install Red Hat Enterprise Linux on a large variety of storage devices. This screen allows you to select either basic or specialized storage devices.
>
> ![rhel6 storage devices RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_storage_devices.png)
>
> **Basic Storage Devices**
>
> Select Basic Storage Devices to install Red Hat Enterprise Linux on the following storage devices:
>
> *   hard drives or solid-state drives connected directly to the local system.
>
> **Specialized Storage Devices**
>
> Select **Specialized Storage Devices** to install Red Hat Enterprise Linux on the following storage devices:
>
> *   Storage area networks (SANs)
> *   Direct access storage devices (DASDs)
> *   Firmware RAID devices
> *   Multipath devices Use the Specialized Storage Devices option to configure Internet Small Computer System Interface (iSCSI) and FCoE (Fiber Channel over Ethernet) connections
>
> **9.7. Setting the Hostname**
>
> Setup prompts you to supply a host name for this computer, either as a fully-qualified domain name (FQDN) in the format **hostname.domainname** or as a short host name in the format **hostname**. Many networks have a Dynamic Host Configuration Protocol (DHCP) service that automatically supplies connected systems with a domain name. To allow the DHCP service to assign the domain name to this machine, specify the short host name only
>
> ![rhel6 set hostname RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_set_hostname.png)
>
> **9.8. Time Zone Configuration**
>
> Set your time zone by selecting the city closest to your computer's physical location. Click on the map to zoom in to a particular geographical region of the world. Specify a time zone even if you plan to use NTP (Network Time Protocol) to maintain the accuracy of the system clock. From here there are two ways for you to select your time zone:
>
> *   Using your mouse, click on the interactive map to select a specific city (represented by a yellow dot).A red X appears indicating your selection.
> *   You can also scroll through the list at the bottom of the screen to select your time zone. Using your mouse, click on a location to highlight your selection
>
> ![rhel6 timezone RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_timezone.png)
>
> If Red Hat Enterprise Linux is the only operating system on your computer, select **System clock uses UTC**. The system clock is a piece of hardware on your computer system. Red Hat Enterprise Linux uses the timezone setting to determine the offset between the local time and UTC on the system clock. This behavior is standard for systems that use UNIX, Linux, and similar operating systems. Click **Next** to proceed.
>
> **9.9. Set the Root Password**
>
> Setting up a root account and password is one of the most important steps during your installation. The root account is used to install packages, upgrade RPMs, and perform most system maintenance. Logging in as root gives you complete control over your system.
>
> ![rhel6 install root password RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_root_password.png)
>
> **9.11. Initializing the Hard Disk**
>
> If no readable partition tables are found on existing hard disks, the installation program asks to initialize the hard disk. This operation makes any existing data on the hard disk unreadable. If your system has a brand new hard disk with no operating system installed, or you have removed all partitions on the hard disk, click **Re-initialize drive**.
>
> The installation program presents you with a separate dialog for each disk on which it cannot read a valid partition table. Click the **Ignore all** button or **Re-initialize all** button to apply the same answer to all devices.
>
> ![rhel6 install re initialize disk RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_re-initialize_disk.png)
>
> **9.12. Upgrading an Existing System**
>
> The installation system automatically detects any existing installation of Red Hat Enterprise Linux. The upgrade process updates the existing system software with new versions, but does not remove any data from users' home directories. The existing partition structure on your hard drives does not change. Your system configuration changes only if a package upgrade demands it. Most package upgrades do not change system configuration, but rather install an additional configuration file for you to examine later.
>
> Note that the installation medium that you are using might not contain all the software packages that you need to upgrade your computer.
>
> **9.12.1. The Upgrade Dialog**
>
> If your system contains a Red Hat Enterprise Linux installation, a dialog appears asking whether you want to upgrade that installation. To perform an upgrade of an existing system, choose the appropriate installation from the drop-down list and select **Next**.
>
> ![rhel6 install upgrade dialog RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_upgrade_dialog.png)
>
> **9.12.3. Upgrading Boot Loader Configuration**
>
> Your completed Red Hat Enterprise Linux installation must be registered in the boot loader to boot properly. A boot loader is software on your machine that locates and starts the operating system.
>
> ![rhel6 install grub upgrade RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_grub_upgrade.png)
>
> If the existing boot loader was installed by a Linux distribution, the installation system can modify it to load the new Red Hat Enterprise Linux system. To update the existing Linux boot loader, select Update boot loader configuration. This is the default behavior when you upgrade an existing Red Hat Enterprise Linux installation.
>
> GRUB is the standard boot loader for Red Hat Enterprise Linux on 32-bit and 64-bit x86 architectures. If your machine uses another boot loader, such as BootMagic, System Commander, or the loader installed by Microsoft Windows, then the Red Hat Enterprise Linux installation system cannot update it. In this case, select Skip boot loader updating. When the installation process completes, refer to the documentation for your product for assistance.
>
> Install a new boot loader as part of an upgrade process only if you are certain you want to replace the existing boot loader. If you install a new boot loader, you may not be able to boot other operating systems on the same machine until you have configured the new boot loader. Select Create new boot loader configuration to remove the existing boot loader and install GRUB.
>
> After you make your selection, click **Next** to continue.

The next section goes into the partitioning schema and it's a lot of information:

> **9.13. Disk Partitioning Setup**
>
> Partitioning allows you to divide your hard drive into isolated sections, where each section behaves as its own hard drive. Partitioning is particularly useful if you run multiple operating systems.
>
> ![rhel6 install disk partitioning RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_disk_partitioning.png)
>
> On this screen you can choose to create the default partition layout in one of four different ways, or choose to partition storage devices manually to create a custom layout.
>
> The first four options allow you to perform an automated installation without having to partition your storage devices yourself. If you do not feel comfortable with partitioning your system, choose one of these options and let the installation program partition the storage devices for you. Depending on the option that you choose, you can still control what data (if any) is removed from the system.
>
> *   **Use All Space **Select this option to remove all partitions on your hard drives (this includes partitions created by other operating systems such as Windows VFAT or NTFS partitions).
> *   **Replace Existing Linux System(s) **Select this option to remove only partitions created by a previous Linux installation. This does not remove other partitions you may have on your hard drives (such as VFAT or FAT32 partitions).
> *   **Shrink Current System** Select this option to resize your current data and partitions manually and install a default Red Hat Enterprise Linux layout in the space that is freed.
> *   **Use Free Space** Select this option to retain your current data and partitions and install Red Hat Enterprise Linux in the unused space available on the storage drives. Ensure that there is sufficient space available on the storage drives before you select this option
> *   **Create Custom Layout** Select this option to partition storage devices manually and create customized layouts. Choose your preferred partitioning method by clicking the radio button to the left of its description in the dialog box. Select Encrypt system to encrypt all partitions except the /boot partition.
>
> **9.14. Encrypt Partitions**
>
> If you selected the **Encrypt System** option, the installer prompts you for a passphrase with which to encrypt the partitions on the system. Partitions are encrypted using the Linux Unified Key Setup
>
> ![rhel6 install encrypted install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_encrypted_install.png)
>
> Choose a passphrase and type it into each of the two fields in the dialog box. You must provide this passphrase every time that the system boots.
>
> **9.15. Creating a Custom Layout or Modifying the Default Layout**
>
> If you chose to create a custom layout, you must tell the installation program where to install Red Hat Enterprise Linux. This is done by defining mount points for one or more disk partitions in which Red Hat Enterprise Linux is installed. You may also need to create and/or delete partitions at this time.
>
> At a bare minimum, you need an appropriately-sized root partition, and usually a swap partition appropriate to the amount of RAM you have on the system.
>
> Anaconda can handle the partitioning requirements for a typical installation.
>
> ![rhel6 install partitioning example RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_partitioning_example.png)
>
> The partitioning screen contains two panes. The top pane contains a graphical representation of the hard drive, logical volume, or RAID device selected in the lower pane.
>
> Above the graphical representation of the device, you can review the name of the drive (such as /dev/sda or LogVol00), its size (in MB), and its model as detected by the installation program.
>
> Using your mouse, click once to highlight a particular field in the graphical display. Double-click to edit an existing partition or to create a partition out of existing free space.
>
> The lower pane contains a list of all drives, logical volumes, and RAID devices to be used during installation, as specified earlier in the installation process.
>
> Devices are grouped by type. Click on the small triangles to the left of each device type to view or hide devices of that type.
>
> Anaconda displays several details for each device listed:
>
> *   **Device** - the name of the device, logical volume, or partition
> *   **Size (MB)** - the size of the device, logical volume, or partition (in MB)
> *   **Mount Point/RAID/Volume** - the mount point (location within a file system) on which a partition is to be mounted, or the name of the RAID or logical volume group of which it is a part
> *   **Type** - the type of partition. If the partition is a standard partition, this field displays the type of file system on the partition (for example, ext4). Otherwise, it indicates that the partition is a physical volume (LVM), or part of a software RAID
> *   **Format** - A check mark in this column indicates that the partition will be formatted during installation
>
> Beneath the lower pane are four buttons: Create, Edit, Delete, and Reset. Select a device or partition by clicking on it in either the graphical representation in the upper pane of in the list in the lower pane, then click one of the four buttons to carry out the following actions:
>
> *   **Create** - create a new partition, logical volume, or software RAID
> *   **Edit** - change an existing partition, logical volume, or software RAID. Note that you can only shrink partitions with the Resize button, not enlarge partitions.
> *   **Delete** - remove a partition, logical volume, or software RAID
> *   **Reset** - undo all changes made in this screen
>
> **9.15.1. Create Storage**
>
> The Create Storage dialog allows you to create new storage partitions, logical volumes, and software RAIDs. Anaconda presents options as available or unavailable depending on the storage already present on the system or configured to transfer to the system.
>
> ![rhel6 install create storage RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_create_storage.png)
>
> Options are grouped under Create Partition, Create Software RAID and Create LVM as follows:
>
> **Create Partition**
>
> *   **Standard Partition** — create a standard disk partition
>
> **Create Software RAID**
>
> *   **RAID Partition** — create a partition in unallocated space to form part of a software RAID device. To form a software RAID device, two or more RAID partitions must be available on the system.
> *   **RAID Device** — combine two or more RAID partitions into a software RAID device. When you choose this option, you can specify the type of RAID device to create (the RAID level). This option is only available when two or more RAID partitions are available on the system
>
> **Create LVM Logical Volume**
>
> *   **LVM Physical Volume** — create a physical volume in unallocated space.
> *   **LVM Volume Group** — create a volume group from one or more physical volumes. This option is only available when at least one physical volume is available on the system.
> *   **LVM Logical Volume** — create a logical volume on a volume group. This option is only available when at least one volume group is available on the system.
>
> **9.15.2. Adding Partitions**
>
> To add a new partition, select the Create button. A dialog box appears
>
> ![rhel6 install add partition RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_add_partition.png)
>
> *   **Mount Point:** Enter the partition's mount point. For example, if this partition should be the root partition, enter /; enter /boot for the /boot partition, and so on. You can also use the pull-down menu to choose the correct mount point for your partition. For a swap partition the mount point should not be set — setting the filesystem type to swap is sufficient.
> *   **File System Type**: Using the pull-down menu, select the appropriate file system type for this partition
> *   **Allowable Drives**: This field contains a list of the hard disks installed on your system. If a hard disk's box is highlighted, then a desired partition can be created on that hard disk. If the box is not checked, then the partition will never be created on that hard disk. By using different checkbox settings, you can have anaconda place partitions where you need them, or let anaconda decide where partitions should go
> *   **Size (MB)**: Enter the size (in megabytes) of the partition. Note, this field starts with 200 MB; unless changed, only a 200 MB partition will be created.
> *   **Additional Size Options**: Choose whether to keep this partition at a fixed size, to allow it to "grow" (fill up the available hard drive space) to a certain point, or to allow it to grow to fill any remaining hard drive space available.
> *   If you choose **Fill all space up to (MB)**, you must give size constraints in the field to the right of this option. This allows you to keep a certain amount of space free on your hard drive for future use.
> *   F**orce to be a primary partition**: Select whether the partition you are creating should be one of the first four partitions on the hard drive. If unselected, the partition is created as a logical partition
> *   **Encrypt:** Choose whether to encrypt the partition so that the data stored on it cannot be accessed without a passphrase, even if the storage device is connected to another system.
> *   **OK**: Select OK once you are satisfied with the settings and wish to create the partition.
> *   **Cancel**: Select Cancel if you do not want to create the partition.
>
> **9.15.2.1. File System Types**
>
> Red Hat Enterprise Linux allows you to create different partition types and file systems. The following is a brief description of the different partition types and file systems available, and how they can be used.
>
> **Partition types**
>
> *   **standard partition** — A standard partition can contain a file system or swap space, or it can provide a container for software RAID or an LVM physical volume.
> *   **swap** — Swap partitions are used to support virtual memory. In other words, data is written to a swap partition when there is not enough RAM to store the data your system is processing.
> *   **software RAID** — Creating two or more software RAID partitions allows you to create a RAID device.
> *   **physical volume (LVM)** — Creating one or more physical volume (LVM) partitions allows you to create an LVM logical volume. LVM can improve performance when using physical disks.
>
> **File systems**
>
> *   **ext4** — The ext4 file system is based on the ext3 file system and features a number of improvements. These include support for larger file systems and larger files, faster and more efficient allocation of disk space, no limit on the number of subdirectories within a directory, faster file system checking, and more robust journaling. The ext4 file system is selected by default and is highly recommended.
> *   **ext3** — The ext3 file system is based on the ext2 file system and has one main advantage —journaling. Using a journaling file system reduces time spent recovering a file system after a crash as there is no need to **fsck** the file system.
> *   **ext2** — An ext2 file system supports standard Unix file types (regular files, directories, symbolic links, etc). It provides the ability to assign long file names, up to 255 characters.
> *   **xfs** — XFS is a highly scalable, high-performance file system that supports filesystems up to 16 exabytes (approximately 16 million terabytes), files up to 8 exabytes (approximately 8 million terabytes) and directory structures containing tens of millions of entries. XFS supports metadata journaling, which facilitates quicker crash recovery. The XFS file system can also be defragmented and resized while mounted and active.
> *   **vfat** — The VFAT file system is a Linux file system that is compatible with Microsoft Windows long filenames on the FAT file system.
> *   **Btrfs** — Btrfs is under development as a file system capable of addressing and managing more files, larger files, and larger volumes than the ext2, ext3, and ext4 file systems. Btrfs is designed to make the file system tolerant of errors, and to facilitate the detection and repair of errors when they occur. It uses checksums to ensure the validity of data and metadata, and maintains snapshots of the file system that can be used for backup or repair.Because Btrfs is still experimental and under development, the installation program does not offer it by default. If you want to create a Btrfs partition on a drive, you must commence the installation process with the boot option

The next section is about recommendations for partitioning. From the same guide:

> **9.15.5. Recommended Partitioning Scheme**
>
> Unless you have a reason for doing otherwise, we recommend that you create the following partitions for x86, AMD64, and Intel 64 systems:
>
> *   A swap partition
> *   A /boot partition
> *   A / partition
> *   A home partition
> *   A swap partition (at least 256 MB) — swap partitions are used to support virtual memory. In other words, data is written to a swap partition when there is not enough RAM to store the data your system is processing.
>
> In years past, the recommended amount of swap space increased linearly with the amount of RAM in the system. But because the amount of memory in modern systems has increased into the hundreds of gigabytes, it is now recognized that the amount of swap space that a system needs is a function of the memory workload running on that system. The following table provides the recommended size of a swap partition depending on the amount of RAM in your system and whether you want sufficient memory for your system to hibernate. The recommended swap space is established automatically during installation, but to also allow for hibernation you will need to edit the swap space in the custom partitioning stage.
>
> ![ram recommendations RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/ram_recommendations.png)
>
> Note that you can obtain better performance by distributing swap space over multiple storage devices, particularly on systems with fast drives, controllers, and interfaces.
>
> **A /boot/ partition (250 MB)**
>
> The partition mounted on /boot/ contains the operating system kernel (which allows your system to boot Red Hat Enterprise Linux), along with files used during the bootstrap process. For most users, a 250 MB boot partition is sufficient.
>
> **A root partition (3.0 GB - 5.0 GB)**
>
> This is where "/" (the root directory) is located. In this setup, all files (except those stored in /boot) are on the root partition.
>
> A 3.0 GB partition allows you to install a minimal installation, while a 5.0 GB root partition lets you perform a full installation, choosing all package groups.
>
> **A home partition (at least 100 MB)**
>
> To store user data separately from system data, create a dedicated partition within a volume group for the /home directory. This will enable you to upgrade or reinstall Red Hat Enterprise Linux without erasing user data files.
>
> Many systems have more partitions than the minimum listed above. Choose partitions based on your particular system needs.
>
> The following table summarizes minimum partition sizes for the partitions containing the listed directories.
>
> ![rhel6 minimum partition size RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_minimum_partition_size.png)

Now to the GRUB section of the installation. From the same guide:

> **9.16. Write changes to disk**
>
> The installer prompts you to confirm the partitioning options that you selected. Click Write changes to disk to allow the installer to partition your hard drive and install Red Hat Enterprise Linux.
>
> ![rhel6 install write changes RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_write_changes.png)
>
> If you are certain that you want to proceed, click **Write changes to disk**.
>
> **9.17. x86, AMD64, and Intel 64 Boot Loader Configuration**
>
> To boot the system without boot media, you usually need to install a boot loader. A boot loader is the first software program that runs when a computer starts. It is responsible for loading and transferring control to the operating system kernel software. The kernel, in turn, initializes the rest of the operating system.
>
> GRUB (GRand Unified Bootloader), which is installed by default, is a very powerful boot loader. GRUB can load a variety of free operating systems, as well as proprietary operating systems with chain-loading (the mechanism for loading unsupported operating systems, such as Windows, by loading another boot loader). Note that the version of GRUB in Red Hat Enterprise Linux 6 is an old and stable version now known as "GRUB Legacy" since upstream development moved to GRUB 2. Red Hat remains committed to maintaining the version of GRUB that we ship with Red Hat Enterprise Linux 6, just as we do with all packages that we ship.
>
> ![rhel6 install grub installer RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_grub_installer.png)
>
> **9.17.1. Advanced Boot Loader Configuration**
>
> Now that you have chosen which boot loader to install, you can also determine where you want the boot loader to be installed. You may install the boot loader in one of two places:
>
> **The master boot record (MBR)** — This is the recommended place to install a boot loader, unless the MBR already starts another operating system loader, such as System Commander. The MBR is a special area on your hard drive that is automatically loaded by your computer's BIOS, and is the earliest point at which the boot loader can take control of the boot process. If you install it in the MBR, when your machine boots, GRUB presents a boot prompt. You can then boot Red Hat Enterprise Linux or any other operating system that you have configured the boot loader to boot.
>
> **The first sector of your boot partition** — This is recommended if you are already using another boot loader on your system. In this case, your other boot loader takes control first. You can then configure that boot loader to start GRUB, which then boots Red Hat Enterprise Linux.
>
> ![rhel6 install advanced boot loader options RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_advanced_boot_loader_options.png)

Now onto the Packaging:

> **9.18. Package Group Selection**
>
> Now that you have made most of the choices for your installation, you are ready to confirm the default package selection or customize packages for your system.
>
> The **Package Installation Defaults** screen appears and details the default package set for your Red Hat Enterprise Linux installation. This screen varies depending on the version of Red Hat Enterprise Linux you are installing.
>
> ![rhel6 install package selection RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_package_selection.png)
>
> By default, the Red Hat Enterprise Linux installation process loads a selection of software that is suitable for a system deployed as a basic server. Note that this installation does not include a graphical environment. To include a selection of software suitable for other roles, click the radio button that corresponds to one of the following options:
>
> *   **Basic Server** - This option provides a basic installation of Red Hat Enterprise Linux for use on a server.
> *   **Database Server** - This option provides the MySQL and PostgreSQL databases.
> *   **Web server** - This option provides the Apache web server.
> *   **Enterprise Identity Server Base** -This option provides OpenLDAP and the System Security Services Daemon (SSSD) to create an identity and authentication server.
> *   **Virtual Host** - This option provides the KVM and Virtual Machine Manager tools to create a host for virtual machines.
> *   **Desktop** - This option provides the OpenOffice.org productivity suite, graphical tools such as the GIMP,and multimedia applications.
> *   **Software Development Workstation** - This option provides the necessary tools to compile software on your Red Hat Enterprise Linux system.
> *   **Minimal** - This option provides only the packages essential to run Red Hat Enterprise Linux. A minimal installation provides the basis for a single-purpose server or desktop appliance and maximizes performance and security on such an installation.
>
> To select a component, click on the checkbox beside it. To customize your package set further, select the Customize now option on the screen. Clicking **Next** takes you to the Package Group Selection screen.
>
> **9.18.2. Customizing the Software Selection**
>
> Select** Customize now** to specify the software packages for your final system in more detail. This option causes the installation process to display an additional customization screen when you select **Next**
>
> ![rhel6 install package customize now RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_package_customize_now.png)
>
> Now to the final section of the install:
>
> **9.19. Installing Packages**
>
> At this point there is nothing left for you to do until all the packages have been installed. How quickly this happens depends on the number of packages you have selected and your computer's speed.
>
> Depending on the available resources, you might see the following progress bar while the installer resolves dependencies of the packages you selected for installation:
>
> ![rhel6 install packages installing RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_install_packages_installing.png)
>
> **9.20. Installation Complete**
>
> Congratulations! Your Red Hat Enterprise Linux installation is now complete! The installation program prompts you to prepare your system for reboot.
>
> Remember to remove any installation media if it is not ejected automatically upon reboot. After your computer's normal power-up sequence has completed, Red Hat Enterprise Linux loads and starts. By default, the start process is hidden behind a graphical screen that displays a progress bar. Eventually, a login: prompt or a GUI login screen (if you installed the X Window System and chose to start X automatically) appears.
>
> The first time you start your Red Hat Enterprise Linux system in run level 5 (the graphical run level), the FirstBoot tool appears, which guides you through the Red Hat Enterprise Linux configuration. Using this tool, you can set your system time and date, install software, register your machine with Red Hat Network, and more. FirstBoot lets you configure your environment at the beginning, so that you can get started using your Red Hat Enterprise Linux system quickly.

### Red Hat Install Example

Here is how my install process looked like. First I booted from the DVD, and I saw the following:

![rhel6 boot install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/rhel6_boot_install.png)

Then skipping the media check, I saw the welcome screen:

![welcome screen rhel5 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/welcome_screen_rhel5_install.png)

Here is how my language selection page looked like:

![lang selection rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/lang_selection_rhel6_install.png)

And here is how my Keyboard Selection screen looked like: ![key selection rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/key_selection_rhel6_install.png)

Then I re-initialized my disks:

![reinitialized disk rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/reinitialized_disk_rhel6_install.png)

I then set my timezone:

![tz sel rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/tz_sel_rhel6_install.png)

I then set the root password:

![root passwd rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/root_passwd_rhel6_install.png)

I then selected to use the whole driver and only selected the 20GB drive:

![partition type rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/partition_type_rhel6_install.png)

I then wrote the changes to disk:

![write changes to disk rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/write_changes_to_disk_rhel6_install.png)

After all the formatting and partition setup the installation process started:

![starting installation rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/starting_installation_rhel6_install.png)

and then the packages started to install:

![package installing rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/package_installing_rhel6_install.png)

After the packages finished installing I saw the following:

![installation finished rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/installation_finished_rhel6_install.png)

When the OS rebooted, I saw the following:

![reboot after rhel6 install RHCSA and RHCE Chapter 1   Installation](https://github.com/elatov/uploads/raw/master/2012/12/reboot_after_rhel6_install.png)

I then logged and started to setup network.

### RedHat Networking Configuration

From "[Red Hat Enterprise Linux 6 Deployment Guide](https://access.redhat.com/knowledge/docs/en-US/Red_Hat_Enterprise_Linux/6/pdf/Deployment_Guide/Red_Hat_Enterprise_Linux-6-Deployment_Guide-en-US.pdf)":

> **8.2. Interface Configuration Files**
>
> Interface configuration files control the software interfaces for individual network devices. As the system boots, it uses these files to determine what interfaces to bring up and how to configure them. These files are usually named ifcfg-name, where name refers to the name of the device that the configuration file controls.
>
> **8.2.1. Ethernet Interfaces**
>
> One of the most common interface files is **/etc/sysconfig/network-scripts/ifcfg-eth0**, which controls the first Ethernet network interface card or NIC in the system. In a system with multiple NICs, there are multiple ifcfg-ethX files (where X is a unique number corresponding to a specific interface). Because each device has its own configuration file, an administrator can control how each interface functions individually.
>
> The following is a sample **ifcfg-eth0** file for a system using a fixed IP addresss:
>
>     DEVICE=eth0
>     BOOTPROTO=none
>     ONBOOT=yes
>     NETMASK=255.255.255.0
>     IPADDR=10.0.1.27
>     USERCTL=no
>
>
> The values required in an interface configuration file can change based on other values. For example, the **ifcfg-eth0** file for an interface using DHCP looks different because IP information is provided by the DHCP server:
>
>     DEVICE=eth0
>     BOOTPROTO=dhcp
>     ONBOOT=yes
>
>
> NetworkManager is graphical configuration tool which provides an easy way to make changes to the various network interface configuration files. However, it is also possible to manually edit the configuration files for a given network interface. Below is a listing of the configurable parameters in an Ethernet interface configuration file:
>
> **BONDING_OPTS=parameters** sets the configuration parameters for the bonding device, and is used in **/etc/sysconfig/network-scripts/ifcfg-bondN**. These parameters are identical to those used for bonding devices in **/sys/class/net/bonding_device/bonding**.
>
> This configuration method is used so that multiple bonding devices can have different configurations. It is highly recommended to place all of your bonding options after the **BONDING_OPTS** directive in **ifcfg-name**. Do not specify options for the bonding device in **/etc/modprobe.d/bonding.conf**, or in the deprecated **/etc/modprobe.conf** file.
>
> **BOOTPROTO=protocol** where **protocol** is one of the following:
>
> *   **none** — No boot-time protocol should be used.
> *   **bootp** — The BOOTP protocol should be used.
> *   **dhcp** — The DHCP protocol should be used.
>
> **BROADCAST=address** where **address** is the broadcast address. This directive is deprecated, as the value is calculated automatically with **ipcalc**.
>
> **DEVICE=name** where **name** is the name of the physical device (except for dynamically-allocated PPP devices where it is the logical name).
>
> **DHCP_HOSTNAME=name** where **name** is a short hostname to be sent to the DHCP server. Use this option only if the DHCP server requires the client to specify a hostname before receiving an IP address.
>
> **DNS{1,2}=address** where **address** is a name server address to be placed in **/etc/resolv.conf** if the **PEERDNS** directive is set to **yes**.
>
> **ETHTOOL_OPTS=options** where options are any device-specific options supported by **ethtool**. For example, if you wanted to force 100Mb, full duplex:
>
>     ETHTOOL_OPTS="autoneg off speed 100 duplex full"
>
>
> Instead of a custom initscript, use **ETHTOOL_OPTS** to set the interface speed and duplex settings. Custom initscripts run outside of the network init script lead to unpredictable results during a post-boot network service restart.
>
> **HOTPLUG=answer** where **answer** is one of the following:
> * **yes** — This device should be activated when it is hot-plugged (this is the default option).
> * **no** — This device should not be activated when it is hot-plugged. The
>
> **HOTPLUG=no** option can be used to prevent a channel bonding interface from being activated when a bonding kernel module is loaded.
>
> **HWADDR=MAC-address** where **MAC-address** is the hardware address of the Ethernet device in the form **AA:BB:CC:DD:EE:FF**. This directive must be used in machines containing more than one NIC to ensure that the interfaces are assigned the correct device names regardless of the configured load order for each NIC's module. This directive should **not** be used in conjunction with **MACADDR**.
>
> **IPADDR=address** where **address** is the IP address.
>
> **LINKDELAY=time** where **time** is the number of seconds to wait for link negotiation before configuring the device.
>
> **MACADDR=MAC-address** where MAC-address is the hardware address of the Ethernet device in the form **AA:BB:CC:DD:EE:FF**. This directive is used to assign a MAC address to an interface, overriding the one assigned to the physical NIC. This directive should not be used in conjunction with the **HWADDR** directive.
>
> **MASTER=bond-interface** where **bond-interface** is the channel bonding interface to which the Ethernet interface is linked. This directive is used in conjunction with the **SLAVE** directive.
>
> **NETMASK=mask** where mask is the **netmask** value.
>
> **NETWORK=address** where **address** is the network address. This directive is deprecated, as the value is calculated automatically with **ipcalc**.
>
> **NM_CONTROLLED=answer** where **answer** is one of the following:
>
> *   **yes** — NetworkManager is permitted to configure this device.This is the default behavior and can be omitted.
> *   **no** — NetworkManager is not permitted to configure this device.
>
> **ONBOOT=answer** where **answer** is one of the following:
>
> *   **yes** — This device should be activated at boot-time.
> *   **no** — This device should not be activated at boot-time
>
> **PEERDNS=answer** where **answer** is one of the following:
>
> *   **yes** — Modify **/etc/resolv.conf** if the DNS directive is set. If using DHCP, then **yes** is the default.
> *   **no** — Do not modify **/etc/resolv.conf**.
>
> **SLAVE=answer** where **answer** is one of the following:
>
> *   **yes** — This device is controlled by the channel bonding interface specified in the **MASTER** directive.
> *   **no** — This device is not controlled by the channel bonding interface specified in the **MASTER** directive.
>
> **SRCADDR=address** where **address** is the specified source IP address for outgoing packets.
>
> **USERCTL=answer** where **answer** is one of the following:
>
> *   **yes** — Non-**root** users are allowed to control this device.
> *   **no** — Non-**root** users are not allowed to control this device.

And here is the information on how to set the hostname and default route on the host:

> **The Default Gateway**
>
> The default gateway is specified by means of the GATEWAY directive and can be specified either globally or in interface-specific configuration files. Specifying the default gateway globally has certain advantages especially if more than one network interface is present and it can make fault finding simpler if applied consistently. There is also the **GATEWAYDEV** directive, which is a global option. If multiple devices specify **GATEWAY**, and one interface uses the **GATEWAYDEV** directive, that directive will take precedence. This option is not recommend as it can have unexpected consequences if an interface goes down and it can complicate fault finding.
>
> Global default gateway configuration is stored in the **/etc/sysconfig/network** file. This file specifies gateway and host information for all network interfaces.
>
> ...
>
> **D.1.13. /etc/sysconfig/network**
>
> The **/etc/sysconfig/network** file is used to specify information about the desired network configuration. By default, it contains the following options:
>
> **NETWORKING=boolean** A Boolean to enable (**yes**) or disable (**no**) the networking. For example:
>
>     NETWORKING=yes
>
>
> **HOSTNAME=value** The hostname of the machine. For example:
>
>     HOSTNAME=penguin.example.com
>
>
> **GATEWAY=value** The IP address of the network's gateway. For example:
>
>     GATEWAY=192.168.1.0
>

### RedHat Networking Configuration Example

Here is how my **/etc/sysconfig/networking-scripts/ifcfg-eth0** look like in the beginning:

    [root@localhost ~]# cat ifcfg-eth0
    DEVICE="eth0"
    BOOTPROTO="dhcp"
    HWADDR="00:50:56:17:1B:A4"
    NM_CONTROLLED="yes"
    ONBOOT="no"
    TYPE="Ethernet"
    UUID="acd8dd1f-f38f-4916-a989-3b7a7ef9b379"


I changed it to look like this:

    [root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth0
    DEVICE="eth0"
    BOOTPROTO="none"
    HWADDR="00:50:56:17:1B:A4"
    ONBOOT="yes"
    IPADDR=10.131.65.22
    NETMASK=255.255.240.0
    USERCTL=no


Here is how my **/etc/sysconfig/network** file looked like in the beginning:

    [root@localhost ~]# cat network
    NETWORKING=yes
    HOSTNAME=localhost.localdomain


and here is what I changed it to:

    [root@localhost ~]# cat /etc/sysconfig/network
    NETWORKING=yes
    HOSTNAME=rhel01
    GATEWAY=10.131.79.254


I know this is insecure but I also allowed root to be logged in via ssh, so set the following option under **/etc/ssh/sshd_config**:

    [root@localhost ~]# grep ^PermitRootLogin /etc/ssh/sshd_config
    PermitRootLogin yes


Then restarting both services:

    [root@localhost ~]# service network restart
    Shutting down interface eth0: [ OK ]
    Shutting down loopback interface: [ OK ]
    Bringing up loopback interface: [ OK ]
    Bringing up interface eth0: [ OK ]
    [root@localhost ~]# service sshd restart
    Stopping sshd: [ OK ]
    Starting sshd: [ OK ]


And then I was able to ssh to my first RHEL machine. I then configured my second ethernet interface. Here is how it looked like right after the install:

    [root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth1
    DEVICE="eth1"
    BOOTPROTO="dhcp"
    HWADDR="00:50:56:17:1B:A5"
    NM_CONTROLLED="yes"
    ONBOOT="no"
    TYPE="Ethernet"
    UUID="2fd2ad81-06d6-414b-9528-bf79c1584d96"


And here is how it looked like after I was done:

    [root@localhost ~]# cat /etc/sysconfig/network-scripts/ifcfg-eth1
    DEVICE="eth1"
    BOOTPROTO="none"
    HWADDR="00:50:56:17:1B:A5"
    ONBOOT="yes"
    IPADDR=192.168.2.100
    NETMASK=255.255.255.0
    USERCTL=no


I did the other installs and configured the network as necessary.

