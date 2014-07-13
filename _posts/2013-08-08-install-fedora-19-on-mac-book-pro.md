---
title: Install Fedora 19 on Mac Book Pro
author: Karim Elatov
layout: post
permalink: /2013/08/install-fedora-19-on-mac-book-pro/
categories: ['os']
tags: ['grub', 'linux', 'fedora', 'mac_os_x', 'efi','mbr']
---

I was using my new Mac and there are just something that I missed from my previous Linux Laptops. So I decided to install Fedora on my new MacBook Pro :). The biggest challenge is getting around the EUFI interface.

## BIOS VS EUFI

The Arch Page entitled "[Unified Extensible Firmware Interface](https://wiki.archlinux.org/index.php/Unified_Extensible_Firmware_Interface)" has a good summary and helped me out during the preparation of the install:

> Unified Extensible Firmware Interface (or UEFI for short) is a new type of firmware that was initially designed by Intel (known as EFI then) mainly for its Itanium based systems. It introduces new ways of booting an OS that is distinct from the commonly used "MBR boot code" method followed for BIOS systems.
>
> **Booting an OS using BIOS**
> A BIOS or Basic Input-Output System is the very first program that is executed once the system is switched on. After all the hardware has been initialized and the POST operation has completed, the BIOS executes the first boot code in the first device in the device booting list.
>
> If the list starts with a CD/DVD drive, then the El-Torito entry in the CD/DVD is executed. This is how bootable CD/DVD works. If the list starts with a HDD, then BIOS executes the very first 440 bytes MBR boot code. The boot code then chainloads or bootstraps a much larger and complex bootloader which then loads the OS.
>
> Basically, the BIOS does not know how to read a partition table or filesystem. All it does is initialize the hardware, then load and run the 440-byte boot code.
>
> **Multiboot on BIOS**
> Since very little can be achieved by a program that fits into the 440-byte boot code area, multi-booting using BIOS requires a multi-boot capable bootloader (multi-boot refers to booting multiple operating systems, not to booting a kernel in the Multiboot format specified by the GRUB developers). So usually a common bootloader like GRUB or Syslinux or LILO would be loaded by the BIOS, and it would load an operating system by either chain-loading or directly loading the kernel.
>
> **Booting an OS using UEFI**
> UEFI firmware does not support booting through the above mentioned method which is the only way supported by BIOS. UEFI has support for reading both the partition table as well as understanding filesystems.
>
> The commonly used UEFI firmwares support both MBR and GPT partition table. EFI in Apple-Intel Macs are known to also support Apple Partition Map besides MBR and GPT. Most UEFI firmwares have support for accessing FAT12 (floppy disks), FAT16 and FAT32 filesystems in HDDs and ISO9660 (and UDF) in CD/DVDs. EFI in Apple-Intel Macs can access HFS/HFS+ filesystems also apart from the mentioned ones.
>
> UEFI does not launch any boot code in the MBR whether it exists or not. Instead it uses a special partition in the partition table called EFI SYSTEM PARTITION in which files required to be launched by the firmware are stored. Each vendor can store its files under `<EFI SYSTEM PARTITION>/EFI/<VENDOR NAME>/` folder and can use the firmware or its shell (UEFI shell) to launch the boot program. An EFI System Partition is usually formatted as FAT32.
>
> Under UEFI, every program whether it is an OS loader or a utility (e.g. a memory testing app or recovery tool), should be a UEFI Application corresponding to the EFI firmware architecture. The vast majority of UEFI firmwares, including recent Apple Macs, use x86_64 EFI firmware. The only known devices that use i386 EFI are older (pre 2008) Apple Macs.
>
> An x86_64 EFI firmware does not include support for launching 32-bit EFI apps unlike x86_64 Linux and Windows versions which include such support. Therefore the bootloader must be compiled for that specific architecture.
>
> **Multibooting on UEFI**
> Since each OS or vendor can maintain its own files within the EFI SYSTEM PARTITION without affecting the other, multi-booting using UEFI is just a matter of launching a different UEFI application corresponding to the particular OS's bootloader. This removes the need for relying on chainloading mechanisms of one bootloader to load another to switch OSes.

To confirm that my Mac was using "x86_64 EFI firmware", I ran the following:

    kelatov@kmac:~$ioreg -l -p IODeviceTree | grep firmware-abi
    | |   "firmware-abi" = <"EFI64">


## GRUB and EUFI

Since I will be installing Fedora, I will be using GRUB for my boot loader. Here is how GRUB handles EUFI, from [GRUB and the boot process on UEFI-based x86 systems](http://docs.fedoraproject.org/en-US/Fedora/19/html/Installation_Guide/s2-grub-whatis-booting-uefi.html)":

> GRUB loads itself into memory in the following stages:
>
> 1.  The UEFI-based platform reads the partition table on the system storage and mounts the EFI System Partition (ESP), a VFAT partition labeled with a particular globally unique identifier (GUID). The ESP contains EFI applications such as bootloaders and utility software, stored in directories specific to software vendors. Viewed from within the Fedora 19 file system, the ESP is **/boot/efi/**, and EFI software provided by Red Hat is stored in **/boot/efi/EFI/fedora/**.
> 2.  The **/boot/efi/EFI/fedora/** directory contains **grub.efi**, a version of GRUB compiled for the EFI firmware architecture as an EFI application. In the simplest case, the EFI boot manager selects **grub.efi** as the default bootloader and reads it into memory.
>
>     If the ESP contains other EFI applications, the EFI boot manager might prompt you to select an application to run, rather than load **grub.efi** automatically.
>
> 3.  GRUB determines which operating system or kernel to start, loads it into memory, and transfers control of the machine to that operating system.
>
> Because each vendor maintains its own directory of applications in the ESP, chain loading is not normally necessary on UEFI-based systems. The EFI boot manager can load any of the operating system bootloaders that are present in the ESP.

The above sounds great, but with Fedora 19, there is a known bug. From "[Common F19 bugs](https://fedoraproject.org/wiki/Common_F19_bugs#Apple_EFI_Macs:_EFI_install_alongside_existing_EFI_installed_OS_.28including_OS_X.29_results_in_you_have_not_created_a_bootloader_stage1_target_device_error)":

> If you try to do a native UEFI install of Fedora 19 alongside a native UEFI install of OS X and re-use the existing EFI system partition, the installer will incorrectly consider the existing EFI system partition as invalid and report that you have not created a bootloader stage1 target device. Unfortunately, the Fedora automatic partitioning algorithm will actually attempt to re-use the EFI system partition, and so you will run into this bug in any Fedora 19 installation attempt where you use the automatic partitioning algorithm and do not choose to delete the existing EFI system partition.
>
> Practically speaking, there are a few different approaches to dealing with this problem. If you do not mind losing your OS X installation, you can simply choose to delete it (including the EFI system partition), and let Fedora occupy the rest of the disk. Fedora should create a new EFI system partition and install successfully.
>
> If you wish to preserve your OS X installation, install Fedora 19 Final, and dual boot, you must use the installer's 'custom partitioning' path. Make sure to leave the existing EFI system partition intact, but do not set a mount point for it. Do not use the Create partitions for me button. Instead, manually create a new EFI system partition, and set it to be mounted at /boot/efi. Manually create other partitions as usual. Complete custom partitioning, and your installation should proceed successfully.
>
> You could also try installing Fedora 18 or Fedora 19 Beta. These should allow you to use automatic partitioning to install alongside OS X, assuming you do not run into any other bugs they may have contained. You could then upgrade to Fedora 19 Final - with FedUp from Fedora 18, or yum from Fedora 19 Beta. You will still wind up with two EFI system partitions in this case.
>
> We are investigating the possibility of producing an updates image to make it easier to deal with this bug. We apologize for any inconvenience it causes you.

It looks like there are still some issues with the new UEFI and different OSes.

## Download Appropriate Install Media

From [Fedora's Installation Guide](http://docs.fedoraproject.org/en-US/Fedora/19/html/Installation_Guide/ch-Boot-x86.html#s1-x86-starting):

> **Important — UEFI for 32-bit x86 systems**
> Fedora 19 does not support UEFI booting for 32-bit x86 systems. Only BIOS booting is supported.
>
> **Important — UEFI for AMD64 and Intel 64**
> Note that the boot configurations of UEFI and BIOS differ significantly from each other. Therefore, the installed system must boot using the same firmware that was used during installation. You cannot install the operating system on a system that uses BIOS and then boot this installation on a system that uses UEFI. Fedora 19 supports version 2.2 of the UEFI specification.

I was going to install to install Fedora 19 64bit from the get-go so this didn't really impact me.

## Shrinking the OS Disk

I just needed 50GB for my Linux install. Before I made any changes, here is how disk was partitioned:

    kelatov@kmac:~$diskutil list
    /dev/disk0
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *500.1 GB   disk0
       1:                        EFI                         209.7 MB   disk0s1
       2:                  Apple_HFS Macintosh HD            499.2 GB   disk0s2
       3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3


While in Mac OS X, From Utilities (Command-Shift-U), I started up DiskUtility. Then I selected the OS Hard-Drive, selected the Partition tab, re-sized the OS partition , and clicked apply:

![DiskUtility Resize partition Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/DiskUtility_Resize_partition.png)

That was really easy.

## Install Fedora 19 on Mac Book Pro

After I burned the DVD ISO, I inserted into the Disk drive and rebooted. Right after I rebooted, I held down the "Alt/Option" key and I saw that the following media was bootable:

![MAC BOOT MEDIA Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/MAC_BOOT_MEDIA.jpg)

I selected the Fedora Media and booted from it. During the install I selected the "Custom partition" method and I made the follow partitioning schema:

![Partitions added fedora install Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/Partitions_added_fedora_install.jpg)

Even after following the instruction in the bug, it still gave the "you have not created a bootloader stage1 target device" error. So I decided not to install a boot-loader at all. This is done by clicking on "Full Disk Summary and bootloader" and then selecting "Do not install bootloader":

![do not install bl f19 Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/do-not-install-bl-f19.jpg)

After opting out of the bootloading, the install started.

## Boot into Rescue Mode and Create the GRUB Configuration manually

After the install finished, I rebooted into the Install DVD again and selected "Troubleshooting":

![troubleshoot fedora dvd Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/troubleshoot_fedora_dvd.png)

I selected to discover any previous Linux installs and the rescue CD mounted it under **/mnt/sysimage**. After it dropped me into the shell, I did the following to create the GRUB configuration:

    Starting installer, one moment...
    anaconda 19.30.13-1 for Fedora 19 started.

    Your system is mounted under /mnt/sysimage directory.
    When finished please exit from the shell and your system will reboot.

    Starting Shell...
    bash-4.2# chroot /mnt/sysimage
    bash-4.2# grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg
    Generating grub.cfg
    Found Linux image: /boot/vmlinuz-3.9.5-301.fc19.x86_64
    Found initrd image: /boot/initramfs-3.9.5-301.fc19.x86_64.img
    Found Linux image: /boot/vmlinuz-0-rescue-95a9e97960424f00f4952d7e7a90eca
    Found initrd image: /boot/initramfs-0-rescue-95a9e97960424f00f4952d7e7a90eca.img
    Found Mac OS X on /dev/sda2
    done
    bash-4.2#


I then exited from the recovery shell and let the OS boot. Since I didn't install any boot loader it booted into Mac OS X.

### Bless the Other EFI Partition

To boot from the other EFI partition we need to **bless** it and set it as bootable. After you boot back into Mac OS X, you will see the following partitions:

    kelatov@kmac:~$diskutil list
    /dev/disk0
       #:                       TYPE NAME                    SIZE       IDENTIFIER
       0:      GUID_partition_scheme                        *500.1 GB   disk0
       1:                        EFI                         209.7 MB   disk0s1
       2:                  Apple_HFS Macintosh HD            444.2 GB   disk0s2
       3:                 Apple_Boot Recovery HD             650.0 MB   disk0s3
       4:       Microsoft Basic Data NO NAME                 209.7 MB   disk0s4
       5:                  Linux LVM                         54.8 GB    disk0s5


You will also notice the second EFI Partition automatically mounted:

    kelatov@kmac:~$df -Ph /Volumes/*
    Filesystem        Size   Used  Avail Capacity  Mounted on
    /dev/disk0s2     414Gi  185Gi  229Gi    45%    /
    /dev/disk0s4     200Mi   11Mi  189Mi     6%    /Volumes/NO NAME


So to bless our second EFI partition, we can run the following:

    kelatov@kmac:~$sudo bless  --mount /Volumes/NO\ NAME --setBoot --file /Volumes/NO\ NAME/EFI/fedora/grubx64.efi


I rebooted one more time and I saw the GRUB menu. After it auto-selected the "Fedora" Menu, it showed the following error:

> error: failure to read sector 0x0 from hd0

But then kept booting without issues :) Apparently there is workaround described [here](http://forums.gentoo.org/viewtopic-t-942130-start-0.html), but I wasn't too worried about it.

### Installing the Wireless Firmware

Initially the wireless card won't be recognized. Here is the **lspci** output of the card:

    [elatov@kmac ~]$ lspci | grep 802
    03:00.0 Network controller: Broadcom Corporation BCM4331 802.11a/b/g/n (rev 02)


I downloaded the firmware from here:

    [elatov@kmac ~]$ wget http://mirror.yandex.ru/fedora/russianfedora/russianfedora/nonfree/fedora/releases/19/Everything/i386/os/b43-firmware-5.100.138-1.fc17.noarch.rpm


and then installed it like so:

    [elatov@kmac ~]$ sudo rpm -Uvh b43-firmware-5.100.138-1.fc17.noarch.rpm


After one more reboot, it came up without issues:

    [elatov@kmac ~]$ iwconfig
    enp2s0f0  no wireless extensions.

    wlp3s0    IEEE 802.11bg  ESSID:"Guest"
              Mode:Managed  Frequency:2.437 GHz  Access Point: 00:19:77:9B:CE:53
              Bit Rate=24 Mb/s   Tx-Power=27 dBm
              Retry  long limit:7   RTS thr:off   Fragment thr:off
              Power Management:off
              Link Quality=70/70  Signal level=-30 dBm
              Rx invalid nwid:0  Rx invalid crypt:0  Rx invalid frag:0
              Tx excessive retries:134  Invalid misc:48   Missed beacon:0

    lo        no wireless extensions.


### Fixing the Fn Keys

By default the **Fn** keys will be mapped to the media keys of the Mac Keyboard. To temporarily fix it, you can run the following:

    [elatov@kmac ~]$ sudo su -c 'echo 2 > /sys/module/hid_apple/parameters/fnmode'


You can then run **xev** and confirm that your keys are reporting the appropriate key code. Here is how my **F1** key looked like after the fix:

    KeyPress event, serial 38, synthetic NO, window 0x1e00001,
        root 0x31a, subw 0x0, time 7573861, (488,1123), root:(1943,1142),
        state 0x0, keycode 67 (keysym 0xffbe, F1), same_screen YES,
        XLookupString gives 0 bytes:
        XmbLookupString gives 0 bytes:
        XFilterEvent returns: False


To make it permanent, you should be able to add the following into the **/etc/modprobe.d/hid_apple.conf** file:

    [elatov@kmac ~]$ cat /etc/modprobe.d/hid_apple.conf
    options hid_apple fnmode=2


But it actually didn't work out for me. Doing some research it looks like we need to set as a kernel parameter. This is discussed [here](http://superuser.com/questions/461710/update-kernel-module-option-on-fedora-17). You can usually do this with the **/etc/sysconfig/grub** file on Fedora. For some reason that file didn't exist on my install (or rather the link was missing). Usually **/etc/sysconfig/grub** points to **/etc/default/grub**, but the **/etc/default/grub** file was missing. I even re-installed the package that provided that file:

    [elatov@kmac ~]$ yum provides /etc/default/grub
    Loaded plugins: langpacks, refresh-packagekit, remove-with-leaves
    1:grub2-tools-2.00-22.fc19.x86_64 : Support tools for GRUB.
    Repo        : fedora
    Matched from:
    Filename    : /etc/default/grub

    [elatov@kmac ~]$ sudo yum reinstall grub2-tools


But it still didn't help out, so I created one manually with the following contents:

    [elatov@kmac ~]$ cat /etc/default/grub
    GRUB_CMDLINE_LINUX="hid_apple.fnmode=2"
    GRUB_DEFAULT=saved


After that I regenerated the GRUB config:

    [elatov@kmac ~]$ sudo grub2-mkconfig -o /boot/efi/EFI/fedora/grub.cfg
    Generating grub.cfg ...
    Found linux image: /boot/vmlinuz-3.10.3-300.fc19.x86_64
    Found initrd image: /boot/initramfs-3.10.3-300.fc19.x86_64.img
    Found linux image: /boot/vmlinuz-3.9.5-301.fc19.x86_64
    Found initrd image: /boot/initramfs-3.9.5-301.fc19.x86_64.img
    Found linux image: /boot/vmlinuz-0-rescue-95a9e97960424f009f4952d7e7a80eca
    Found initrd image: /boot/initramfs-0-rescue-95a9e97960424f009f4952d7e7a80eca.img
    Found Mac OS X on /dev/sda2
    done


Then after yet another reboot, the **Fn** keys were permanently fixed. Another person wrote a **systemd** service to run the above command upon boot. Check out the instructions at "[Changing the default Function key behaviour in Fedora](https://www.dalemacartney.com/2013/06/14/changing-the-default-function-key-behaviour-in-fedora/)".

## Rebooting into Mac OS X

If you want to reboot into Mac OS X, you can reboot the MacBook Pro and hold down 'Alt/Option" during the boot and you will available bootable media, like so:

![mac osx bootable media Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/mac-osx-bootable_media.jpg)

Select "Macintosh HD" and it will boot back into Mac OS X. To set it permanently to boot into Mac OS X. While in Mac OS X, open up System Preferences and select the "Start Up Disk":

![Startup disk Install Fedora 19 on Mac Book Pro](https://github.com/elatov/uploads/raw/master/2013/07/Startup_disk.png)

Then select "Macintosh HD" and it will reboot into Mac OS X permanently. Or you can run this command to re-enable boot in the Mac OS HD:

    sudo bless --mount "/Volumes/Macintosh HD/" --setboot


